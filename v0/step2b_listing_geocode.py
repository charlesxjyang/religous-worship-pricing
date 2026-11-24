"""Version 1 addition (NYC): geocode each listing's street address.

Overture's map points often sit on the street or the lot next door, so a
church's listing can land on its rectory, its school or a neighbour's house.
The plan says to assign parcels from open geocoding of addresses, so each
listing's address goes to GeoSearch, which returns the lot (BBL) and the
building (BIN). Step 5 uses the address lot when the geocode is confident and
within MAX_SHIFT_M of the map point, and the point's lot otherwise.

Writes table listing_geo.  Run after step 2:
    .venv/bin/python v0/step2b_listing_geocode.py
"""

import json
import math
import re
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import config
from common import assign_lots, connect, make_geocoder

CACHE = config.DATA / "interim" / "listing_geosearch_cache.json"
WORKERS = 4
MIN_CONFIDENCE = 0.8


def dist_m(lat1, lon1, lat2, lon2):
    dy = (lat2 - lat1) * 111_320
    dx = (lon2 - lon1) * 111_320 * math.cos(math.radians((lat1 + lat2) / 2))
    return math.hypot(dx, dy)


def main():
    con = connect(config.DB_PATH)
    rows = con.execute("""
        SELECT id, address, left(postcode, 5) AS zip5, boroname, lat, lon
        FROM places WHERE address IS NOT NULL
    """).fetchall()
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    lock = threading.Lock()
    out, t0, done = [], time.monotonic(), [0]
    geo = make_geocoder(con)

    def work(r):
        pid, address, zip5, boro, lat, lon = r
        if not re.match(r"^\s*\d", address):
            rec = (pid, None, None, None, None, None, None, None, None)
        else:
            hint = boro if config.CITY == "nyc" else config.GEO_HINT
            q = f"{address}, {hint}" + (f" {zip5}" if zip5 and zip5.isdigit() else "")
            hit = geo(q, cache, lock)
            if hit and (hit.get("bbl") or hit.get("lat")):
                d = dist_m(lat, lon, hit["lat"], hit["lon"])
                rec = (pid, q, hit["label"], hit["confidence"],
                       int(hit["bbl"]) if hit.get("bbl") else None, hit["bin"],
                       hit["lat"], hit["lon"], d)
            else:
                rec = (pid, q, None, None, None, None, None, None, None)
        with lock:
            out.append(rec)
            done[0] += 1
            if done[0] % 1000 == 0:
                print(f"  {done[0]:,}/{len(rows):,}, {time.monotonic() - t0:,.0f}s", flush=True)
                CACHE.parent.mkdir(parents=True, exist_ok=True)
                CACHE.write_text(json.dumps(cache))

    with ThreadPoolExecutor(WORKERS) as ex:
        list(ex.map(work, rows))
    CACHE.write_text(json.dumps(cache))
    con.execute("""CREATE OR REPLACE TABLE listing_geo (id VARCHAR, query VARCHAR, label VARCHAR,
                   confidence DOUBLE, bbl BIGINT, bin VARCHAR, lat DOUBLE, lon DOUBLE, shift_m DOUBLE)""")
    con.executemany("INSERT INTO listing_geo VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", out)
    assign_lots(con, "listing_geo", "id")   # points without a parcel (DC's Census fallback)
    print(con.execute(f"""
        SELECT count(*) AS listings,
               count(*) FILTER (WHERE confidence >= {MIN_CONFIDENCE}) AS confident,
               round(median(shift_m) FILTER (WHERE confidence >= {MIN_CONFIDENCE})) AS median_shift_m,
               count(*) FILTER (WHERE confidence >= {MIN_CONFIDENCE} AND g.bbl <> pl.bbl) AS different_lot_than_point
        FROM listing_geo g JOIN place_lot pl USING (id)
    """).df().to_string(index=False))


if __name__ == "__main__":
    main()
