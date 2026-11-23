"""Version 1 addition (NYC): OpenStreetMap religious buildings.

OSM's Overpass API is unreachable from cloud sessions, so the same mapping is
read from Overture's buildings theme, which carries OSM building tags
(building=church, mosque, synagogue, temple, ...). Only records whose source
is OpenStreetMap are kept: volunteer-mapped, independent of the Overture
places used for discovery. License: ODbL (share-alike if a derived database
is published).

Each building's centroid is attached to its tax lot. Writes osm_buildings
and adds osm_religious_building to lot_flags.

Run after step 2 (step 1 wrote the parquet extract; this script writes it if
missing):  .venv/bin/python v0/step2d_osm.py
"""

import config
from common import connect, latest_overture_release
from step2_parcels import attach_points

RELIGIOUS_CLASSES = ("church", "chapel", "cathedral", "mosque", "synagogue", "temple",
                     "shrine", "monastery", "religious", "presbytery", "kingdom_hall")


def main():
    release = config.OVERTURE_RELEASE or latest_overture_release()
    path = config.RAW / f"overture_buildings_religious_{release}_nyc.parquet"
    con = connect(config.DB_PATH)
    if not path.exists():
        b = config.NYC_BBOX
        classes = ", ".join(f"'{c}'" for c in RELIGIOUS_CLASSES)
        con.execute(f"""
            COPY (
              SELECT id, subtype, class, names.primary AS name, height, num_floors,
                     list_transform(sources, lambda s: s.dataset) AS source_datasets,
                     ST_Centroid(geometry) AS centroid, geometry
              FROM read_parquet('s3://{config.OVERTURE_BUCKET}/release/{release}/theme=buildings/type=building/*',
                                hive_partitioning = 1)
              WHERE bbox.xmin BETWEEN {b['xmin']} AND {b['xmax']} AND bbox.ymin BETWEEN {b['ymin']} AND {b['ymax']}
                AND (subtype = 'religious' OR class IN ({classes}))
            ) TO '{path}' (FORMAT parquet)
        """)
    con.execute(f"""
        CREATE OR REPLACE TABLE osm_buildings AS
        SELECT o.id, o.class, o.name, o.height, o.num_floors, o.c AS geom, b.boroname
        FROM (SELECT *, centroid::GEOMETRY AS c FROM read_parquet('{path}')) o
        JOIN boroughs b ON ST_Contains(b.geom, o.c)
        WHERE list_contains(o.source_datasets, 'OpenStreetMap')
    """)
    attach_points(con, "osm_buildings", "id", "osm_lot")
    con.execute("""
        CREATE OR REPLACE TABLE osm_lot_flags AS
        SELECT l.bbl, count(*) AS osm_buildings,
               string_agg(DISTINCT coalesce(b.class, 'religious'), ', ') AS osm_classes,
               string_agg(DISTINCT b.name, ' | ') AS osm_names
        FROM osm_lot l JOIN osm_buildings b USING (id)
        WHERE l.bbl IS NOT NULL GROUP BY 1
    """)
    print(con.execute("""
        SELECT count(*) AS osm_religious_buildings,
               count(DISTINCT l.bbl) AS lots,
               count(*) FILTER (WHERE l.lot_match = 'none') AS not_on_a_lot
        FROM osm_buildings b JOIN osm_lot l USING (id)
    """).df().to_string(index=False))
    print(con.execute("""
        SELECT f.rel_bldgclass AS m_class, f.religious_owned, count(*) AS osm_lots
        FROM osm_lot_flags o JOIN lot_flags f USING (bbl) GROUP BY ALL ORDER BY 3 DESC
    """).df().to_string(index=False))


if __name__ == "__main__":
    main()
