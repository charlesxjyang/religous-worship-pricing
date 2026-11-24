"""Building footprints for cities without building IDs (DC, Charlotte).

NYC's geocoder returns a building ID (BIN). DC's and Charlotte's parcel data
have none, and their parcels are often large (a church campus, a shopping
center, an industrial park), so two congregations on one parcel may be in
different buildings. This step loads every building footprint in the city
from Overture's buildings theme (OpenStreetMap, Microsoft and other sources)
into table `buildings`; step 5 then puts each congregation's meeting point in
the footprint that contains it, or the nearest one on its parcel, and uses
that footprint as the building ("ov:<id>") wherever no BIN exists.

Run after step 1:  CITY=charlotte .venv/bin/python v0/step2e_buildings.py
(NYC needs nothing: it already has BINs.)
"""

import config
from common import connect, latest_overture_release


def main():
    if config.CITY == "nyc":
        print("NYC has building IDs (BIN) from GeoSearch; nothing to do.")
        return
    release = config.OVERTURE_RELEASE or latest_overture_release()
    path = config.RAW / f"overture_buildings_all_{release}_{config.CITY}.parquet"
    if not path.exists():
        tmp = connect()  # in-memory, so the S3 scan does not hold the city database
        b = config.BBOX
        tmp.execute(f"""
            COPY (SELECT id, ST_GeomFromWKB(ST_AsWKB(geometry))::GEOMETRY AS geom
                  FROM read_parquet('s3://{config.OVERTURE_BUCKET}/release/{release}/theme=buildings/type=building/*',
                                    hive_partitioning = 1)
                  WHERE bbox.xmin BETWEEN {b['xmin']} AND {b['xmax']} AND bbox.ymin BETWEEN {b['ymin']} AND {b['ymax']})
            TO '{path}' (FORMAT parquet)
        """)
        tmp.close()
    con = connect(config.DB_PATH)
    con.execute(f"CREATE OR REPLACE TABLE buildings AS SELECT id AS bid, geom FROM read_parquet('{path}')")
    print(f"{con.execute('SELECT count(*) FROM buildings').fetchone()[0]:,} building footprints loaded")


if __name__ == "__main__":
    main()
