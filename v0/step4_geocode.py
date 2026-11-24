"""Version 0, step 4c (NYC): load extractions and geocode gathering places.

Reads data/<city>/interim/extract/*.json into tables, then finds the tax lot of
each gathering place:
- a street address goes to NYC Planning Labs GeoSearch, which returns BBL and
  BIN (no key needed); addresses outside NYC are skipped, not forced into it;
- a public school named without an address ("we meet at P.S. 123") is matched
  to the NCES list by school number within the listing's borough.

Run after step 4b:  .venv/bin/python v0/step4_geocode.py
"""

import json
import re
import threading

import config
from common import assign_lots, connect, make_geocoder

EXTRACT_DIR = config.DATA / "interim" / "extract"
CACHE = config.DATA / "interim" / "geosearch_cache.json"
MIN_CONFIDENCE = 0.8
CITY_ZIP_RE = re.compile(r"\b(" + "|".join(config.ZIP3) + r")\d{2}\b")
STATE_RE = re.compile(r",?\s+\b(A[LKZR]|C[AOT]|D[EC]|FL|GA|HI|I[DLNA]|K[SY]|LA|M[EDAINSOT]|"
                      r"N[EVHJMCD]|O[HKR]|PA|RI|S[CD]|T[NX]|UT|V[TA]|W[AVIY])\b\s*\d{5}")
SCHOOL_NO_RE = re.compile(r"\b(P\.?\s?S|I\.?\s?S|J\.?\s?H\.?\s?S|M\.?\s?S|H\.?\s?S)\.?\s*(\d{1,3})\b", re.I)


def load_extractions(con):
    sites, locs, svcs, shares = [], [], [], []
    for p in sorted(EXTRACT_DIR.glob("*.json")):
        rec = json.loads(p.read_text())
        r = rec.get("result") or {}
        k = rec["site_key"]
        sites.append((k, rec.get("stop_reason"), r.get("site_match"), r.get("site_match_evidence"),
                      r.get("is_worshipping_congregation"), r.get("tradition"), r.get("denomination"),
                      r.get("schedule_found"), r.get("online_only"),
                      r.get("mailing_or_office_address"), rec.get("cost_usd"),
                      json.dumps(rec.get("verification", {}))))
        for g in r.get("gathering_locations", []):
            locs.append((k, g["location_id"], g.get("address"), g.get("venue_name"), g["venue_kind"],
                         g["is_primary"], g["evidence"]))
        for s in r.get("services", []):
            svcs.append((k, s["day"], s["start"], s.get("end"), s["type"], s.get("language"),
                         s["recurrence"], s.get("location_id"), s["evidence"]))
        for s in r.get("shares_space_with", []):
            shares.append((k, s["name"], s["relation"], s["evidence"]))
    con.execute("""CREATE OR REPLACE TABLE extract_sites (site_key VARCHAR, stop_reason VARCHAR,
        site_match VARCHAR, site_match_evidence VARCHAR, is_congregation BOOLEAN, tradition VARCHAR,
        denomination VARCHAR, schedule_found BOOLEAN, online_only BOOLEAN, mailing_address VARCHAR,
        cost_usd DOUBLE, verification VARCHAR)""")
    con.execute("""CREATE OR REPLACE TABLE extract_locations (site_key VARCHAR, location_id INT,
        address VARCHAR, venue_name VARCHAR, venue_kind VARCHAR, is_primary BOOLEAN, evidence VARCHAR)""")
    con.execute("""CREATE OR REPLACE TABLE extract_services (site_key VARCHAR, day VARCHAR,
        start VARCHAR, "end" VARCHAR, type VARCHAR, language VARCHAR, recurrence VARCHAR,
        location_id INT, evidence VARCHAR)""")
    con.execute("""CREATE OR REPLACE TABLE extract_shares (site_key VARCHAR, name VARCHAR,
        relation VARCHAR, evidence VARCHAR)""")
    for table, rows in (("extract_sites", sites), ("extract_locations", locs),
                        ("extract_services", svcs), ("extract_shares", shares)):
        if rows:
            con.executemany(f"INSERT INTO {table} VALUES ({', '.join('?' * len(rows[0]))})", rows)
    print(f"loaded {len(sites):,} sites, {len(locs):,} gathering places, "
          f"{len(svcs):,} services, {len(shares):,} space-sharing mentions")


def outside_city(address: str) -> bool:
    z = re.findall(r"\b(\d{5})(?:-\d{4})?\b", address)
    if z and z[-1][:3] not in config.ZIP3:
        return True
    m = STATE_RE.search(address)
    return bool(m and m.group(1).upper() != config.STATE)


def main():
    con = connect(config.DB_PATH)
    load_extractions(con)
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    geo, lock = make_geocoder(con), threading.Lock()

    # Each gathering place, with the borough of the listing that points to it.
    rows = con.execute("""
        SELECT l.site_key, l.location_id, l.address, l.venue_name, l.venue_kind,
               any_value(p.boroname) AS boro
        FROM extract_locations l
        JOIN place_site s USING (site_key) JOIN places p USING (id)
        GROUP BY ALL
    """).fetchall()
    schools = con.execute("""
        SELECT s.name, s.boroname, sl.bbl FROM schools s JOIN school_lot sl ON sl.id = s.school_id
        WHERE s.source = 'nces_public' AND sl.bbl IS NOT NULL
    """).fetchall()

    out = []
    for key, lid, address, venue, kind, boro in rows:
        rec = dict(site_key=key, location_id=lid, query=None, method="none", outside_nyc=False,
                   label=None, confidence=None, match_type=None, bbl=None, bin=None, lat=None, lon=None,
                   gkey=f"{key}:{lid}")
        if kind in ("online_only",):
            out.append(rec)
            continue
        if address and re.search(r"\d", address):
            if outside_city(address):
                rec["outside_nyc"] = True      # column name kept; means outside this city
            else:
                hint = boro if config.CITY == "nyc" else config.GEO_HINT
                q = address if config.PLACE_RE.search(address) or CITY_ZIP_RE.search(address) \
                    else f"{address}, {hint}"
                rec["query"] = q
                hit = geo(q, cache, lock)
                if hit and (hit.get("confidence") or 0) >= MIN_CONFIDENCE and (hit.get("bbl") or hit.get("lat")):
                    rec |= {k: hit.get(k) for k in ("label", "confidence", "match_type", "bin", "lat", "lon")}
                    rec |= {"bbl": int(hit["bbl"]) if hit.get("bbl") else None,
                            "method": hit.get("method", "geosearch")}
        if rec["method"] == "none" and kind == "public_school":
            m = SCHOOL_NO_RE.search(f"{venue or ''} {address or ''}")
            if m:
                prefix = re.sub(r"[^A-Z]", "", m.group(1).upper())
                cands = [b for n, bo, b in schools
                         if bo == boro and re.search(rf"\b{prefix}\s*0*{int(m.group(2))}\b", n.upper())]
                if len(set(cands)) == 1:
                    rec |= {"bbl": cands[0], "method": "school_name", "query": m.group(0)}
        out.append(rec)
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(cache))

    con.execute("""CREATE OR REPLACE TABLE gathering_geo (site_key VARCHAR, location_id INT,
        query VARCHAR, method VARCHAR, outside_nyc BOOLEAN, label VARCHAR, confidence DOUBLE,
        match_type VARCHAR, bbl BIGINT, bin VARCHAR, lat DOUBLE, lon DOUBLE, gkey VARCHAR)""")
    if out:
        cols = list(out[0])
        con.executemany(f"INSERT INTO gathering_geo VALUES ({', '.join('?' * len(cols))})",
                        [[r[c] for c in cols] for r in out])
    assign_lots(con, "gathering_geo", "gkey")   # points without a parcel (DC's Census fallback)
    print(con.execute("""SELECT method, outside_nyc, count(*) AS places FROM gathering_geo
                         GROUP BY ALL ORDER BY 3 DESC""").df().to_string(index=False))


if __name__ == "__main__":
    main()
