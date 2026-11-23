"""Version 0, step 3 (NYC): recall check.

Lists worship-type lots with no Overture place on them: likely misses.

A worship-type lot is building class M1 (church, synagogue, chapel) or M9
(miscellaneous religious facility), or a religious-owned institutional lot
(land use 08) with a building that is not a school or hospital. A lot counts
as covered if a place sits on it or within NEAR_M of it, since a large
church's listing point often lands on a neighbouring lot.

Writes table recall_lots and v0/private/nyc_recall_misses.csv.
Run after step 2:  .venv/bin/python v0/step3_recall.py
"""

import config
from common import connect

NEAR_M = 40
NOT_WORSHIP_OWNER = r"\b(YESHIVA|TALMUD|MESIVTA|KOLLEL|ACADEMY|SCHOOL|MEDICAL|HOSPITAL|CHARITIES|UNIVERSITY|COLLEGE|SEMINARY)\b"


def main():
    con = connect(config.DB_PATH)
    deg = NEAR_M / 80_000
    # NYC's BBL starts with the borough number; elsewhere, find the area spatially.
    area_join = ("LEFT JOIN boroughs b ON b.borocode = CAST(left(CAST(w.bbl AS VARCHAR), 1) AS INT)"
                 if config.CITY == "nyc" else
                 "LEFT JOIN boroughs b ON ST_Contains(b.geom, ST_Centroid(w.geom))")
    con.execute(f"""
        CREATE OR REPLACE TABLE recall_lots AS
        WITH worship_lots AS (
          SELECT f.*, t.geom,
                 CASE WHEN f.bldgclass IN ('M1', 'M9') THEN 'M1/M9 building class'
                      ELSE 'religious owner, institutional use' END AS why
          FROM lot_flags f
          JOIN (SELECT bbl, ST_Union_Agg(geom) AS geom FROM taxlots GROUP BY bbl) t USING (bbl)
          WHERE f.bldgclass IN ('M1', 'M9')
             OR (f.rel_owner AND f.landuse = 8 AND f.bldgarea > 0
                 AND NOT regexp_matches(f.ownername, '{NOT_WORSHIP_OWNER}'))
        ), on_lot AS (
          SELECT bbl, count(*) AS n_on_lot FROM place_lot GROUP BY bbl
        ), near AS (
          SELECT w.bbl, count(*) AS n_near
          FROM worship_lots w JOIN places p ON ST_DWithin(w.geom, p.geom, {deg})
          WHERE ST_Distance(ST_Transform(w.geom, 'EPSG:4326', 'EPSG:2263', always_xy := true),
                            ST_Transform(p.geom, 'EPSG:4326', 'EPSG:2263', always_xy := true))
                * 0.3048 <= {NEAR_M}
          GROUP BY w.bbl
        )
        SELECT w.bbl, w.why, w.bldgclass, w.ownername, w.lot_address,
               b.boroname, w.bldgarea,
               coalesce(o.n_on_lot, 0) AS places_on_lot,
               coalesce(n.n_near, 0) AS places_within_{NEAR_M}m,
               ST_Y(ST_Centroid(w.geom)) AS lat, ST_X(ST_Centroid(w.geom)) AS lon
        FROM worship_lots w
        LEFT JOIN on_lot o USING (bbl)
        LEFT JOIN near n USING (bbl)
        {area_join}
    """)
    config.PRIVATE_DIR.mkdir(parents=True, exist_ok=True)
    out = config.PRIVATE_DIR / f"{config.CITY}_recall_misses.csv"
    con.execute(f"""
        COPY (SELECT * EXCLUDE (places_on_lot) FROM recall_lots
              WHERE places_within_{NEAR_M}m = 0 ORDER BY boroname, bbl)
        TO '{out}' (HEADER)
    """)
    print(con.execute(f"""
        SELECT why, count(*) AS lots,
               count(*) FILTER (WHERE places_on_lot = 0) AS no_place_on_lot,
               count(*) FILTER (WHERE places_within_{NEAR_M}m = 0) AS none_within_{NEAR_M}m
        FROM recall_lots GROUP BY 1 ORDER BY 1
    """).df().to_string(index=False))
    print(f"wrote {out.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
