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


def latest_overture_release() -> str:
    url = (f"https://{config.OVERTURE_BUCKET}.s3.{config.OVERTURE_REGION}.amazonaws.com/"
           "?list-type=2&prefix=release/&delimiter=/")
    with urllib.request.urlopen(
        urllib.request.Request(url, headers={"User-Agent": user_agent()}), timeout=60
    ) as r:
        releases = re.findall(r"<Prefix>release/([^<]+)/</Prefix>", r.read().decode())
    return sorted(releases)[-1]
