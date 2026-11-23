"""Shared helpers: polite cached downloads and a DuckDB connection."""

import os
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

import duckdb

import config


def user_agent() -> str:
    email = os.environ.get("CONTACT_EMAIL")
    return f"{config.USER_AGENT[:-1]}; {email})" if email else config.USER_AGENT


def download(url: str, dest: Path, *, retries: int = 4, timeout: int = 600) -> Path:
    """Fetch url to dest unless dest already exists. Writes atomically."""
    if dest.exists() and dest.stat().st_size > 0:
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    req = urllib.request.Request(url, headers={"User-Agent": user_agent()})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r, open(tmp, "wb") as f:
                while chunk := r.read(1 << 20):
                    f.write(chunk)
            tmp.rename(dest)
            time.sleep(config.REQUEST_PAUSE_S)
            return dest
        except Exception as e:  # network errors: back off and retry
            wait = 2 ** (attempt + 1)
            print(f"  retry {attempt + 1}/{retries} for {url} after {e!r}; sleeping {wait}s")
            time.sleep(wait)
    raise RuntimeError(f"failed to download {url}")


def socrata_pages(dataset: str, columns: list[str], dest_dir: Path, order: str = "bbl",
                  page: int = config.SOCRATA_PAGE) -> list[Path]:
    """Download a whole Socrata dataset as CSV pages, one request at a time."""
    count_url = f"{config.SOCRATA}/resource/{dataset}.json?$select=count(*)"
    with urllib.request.urlopen(
        urllib.request.Request(count_url, headers={"User-Agent": user_agent()}), timeout=120
    ) as r:
        total = int(re.search(r'"(\d+)"', r.read().decode()).group(1))
    parts = []
    for i, offset in enumerate(range(0, total, page)):
        q = urllib.parse.urlencode({
            "$select": ",".join(columns), "$order": order,
            "$limit": page, "$offset": offset,
        })
        part = dest_dir / f"part-{i:04d}.csv"
        if not part.exists():
            print(f"  {dataset}: rows {offset:,}-{min(offset + page, total):,} of {total:,}")
        parts.append(download(f"{config.SOCRATA}/resource/{dataset}.csv?{q}", part))
    return parts


def connect(path: Path | None = None) -> duckdb.DuckDBPyConnection:
    """DuckDB with spatial + httpfs, and anonymous access to Overture's bucket.

    Extensions come from the duckdb-extension-* wheels in requirements.txt, so
    no call to extensions.duckdb.org is needed.
    """
    from duckdb_extensions import import_extension

    for ext in ("httpfs", "spatial"):
        import_extension(ext)
    con = duckdb.connect(str(path) if path else ":memory:")
    con.execute("LOAD httpfs; LOAD spatial;")
    # Explicit empty keys: the bucket is public, and some environments set
    # placeholder AWS_* variables that S3 would otherwise reject.
    con.execute(f"""
        CREATE OR REPLACE SECRET overture (
            TYPE s3, PROVIDER config, KEY_ID '', SECRET '',
            REGION '{config.OVERTURE_REGION}')
    """)
    return con


GEOSEARCH = "https://geosearch.planninglabs.nyc/v2/search"


def geosearch(text, cache, lock):
    """NYC Planning Labs GeoSearch: address -> lot (BBL) and building (BIN)."""
    import json

    with lock:
        if text in cache:
            return cache[text]
    url = GEOSEARCH + "?" + urllib.parse.urlencode({"text": text, "size": 1})
    hit = None
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": user_agent()})
            with urllib.request.urlopen(req, timeout=30) as r:
                feats = json.load(r).get("features", [])
            if feats:
                p, g = feats[0]["properties"], feats[0]["geometry"]["coordinates"]
                pad = p.get("addendum", {}).get("pad", {})
                hit = {"label": p.get("label"), "confidence": p.get("confidence"),
                       "match_type": p.get("match_type"), "borough": p.get("borough"),
                       "bbl": pad.get("bbl"), "bin": pad.get("bin"), "lon": g[0], "lat": g[1]}
            break
        except Exception:
            time.sleep(2 ** attempt)
    time.sleep(0.25)
    with lock:
        cache[text] = hit
    return hit


def make_geocoder(con):
    """The city's address geocoder: geocode(text, cache, lock) -> dict or None.

    The dict has label, confidence, bbl, bin, lat, lon. bbl may be None (DC's
    Census fallback); assign_lots() then finds the parcel for the point.
    """
    if config.GEOCODER == "geosearch":
        return geosearch
    import dc
    return dc.make_geocoder(con)


def assign_lots(con, table: str, key: str, near_m: float = 30):
    """Fill table.bbl from the parcel under (lat, lon), else the nearest within near_m."""
    deg = near_m / 80_000
    con.execute(f"""
        CREATE OR REPLACE TEMP TABLE _pts AS
        SELECT {key} AS k, ST_Point(lon, lat) AS geom FROM {table}
        WHERE bbl IS NULL AND lat IS NOT NULL AND lon IS NOT NULL
    """)
    con.execute("""
        CREATE OR REPLACE TEMP TABLE _hit AS
        SELECT k, arg_min(t.bbl, ST_Area(t.geom)) AS bbl FROM _pts p
        JOIN taxlots t ON ST_Contains(t.geom, p.geom) GROUP BY k
    """)
    con.execute(f"""
        INSERT INTO _hit
        SELECT p.k, arg_min(t.bbl, ST_Distance(t.geom, p.geom)) FROM _pts p
        JOIN taxlots t ON ST_DWithin(t.geom, p.geom, {deg})
        WHERE p.k NOT IN (SELECT k FROM _hit) GROUP BY p.k
    """)
    con.execute(f"UPDATE {table} SET bbl = h.bbl FROM _hit h WHERE {table}.{key} = h.k AND {table}.bbl IS NULL")


def latest_overture_release() -> str:
    url = (f"https://{config.OVERTURE_BUCKET}.s3.{config.OVERTURE_REGION}.amazonaws.com/"
           "?list-type=2&prefix=release/&delimiter=/")
    with urllib.request.urlopen(
        urllib.request.Request(url, headers={"User-Agent": user_agent()}), timeout=60
    ) as r:
        releases = re.findall(r"<Prefix>release/([^<]+)/</Prefix>", r.read().decode())
    return sorted(releases)[-1]
