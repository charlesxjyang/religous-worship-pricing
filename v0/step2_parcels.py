"""Version 0, step 2 (NYC): attach places and schools to tax lots; flag lots.

- Each Overture place goes to the lot that contains its point. Points that fall
  in a street or yard go to the nearest lot within NEAREST_LOT_M, flagged
  "nearest". This is the *listing* lot; step 4 looks for the lot where the
  congregation actually gathers.
- Each lot gets flags: religious-owned (building class M*, or a religious
  owner name), commercial use, residential use, and any NCES school on it.

Run after step 1:  .venv/bin/python v0/step2_parcels.py
"""

import config
from common import connect

NEAREST_LOT_M = 30

# PLUTO owner names are upper case and cut at about 21 characters.
RELIGIOUS_OWNER_RE = (
    r"\b(CHURCH|CHURCHES|CONGREGATION|CONG|SYNAGOGUE|SYNAGOG|TEMPLE|MASJID|MOSQUE|"
    r"ISLAMIC|MUSLIM|DIOCESE|ARCHDIOCESE|PARISH|MINISTRY|MINISTRIES|TABERNACLE|"
    r"CHAPEL|CATHEDRAL|BAPTIST|METHODIST|EPISCOPAL|LUTHERAN|PRESBYTERIAN|PRESBYTERY|"
    r"PENTECOSTAL|EVANGELICAL|GOSPEL|ASSEMBLY OF GOD|ASSEMBLIES|KINGDOM HALL|JEHOVAH|"
    r"WATCHTOWER|CHABAD|TORAH|YESHIVA|GURDWARA|SIKH|HINDU|MANDIR|BUDDHIST|MONASTERY|"
    r"CONVENT|CATHOLIC|ORTHODOX|ADVENTIST|APOSTOLIC|MISSIONARY|FELLOWSHIP|HOLY|"
    r"SANCTUARY|RECTOR|SHUL|BAIS|KHAL|KEHILLA|AGUDATH|AGUDAS|KOLLEL|TALMUD|"
    r"MESIVTA|BIBLE|CHRIST|SHRINE|VEDANTA)\b"
)
# Owner names that match above but are not religious bodies: firms named after
# Church St or Convent Ave, and individuals ("SURNAME, GIVEN").
NOT_RELIGIOUS_OWNER_RE = (
    r"(\b(LLC|L\.L\.C|MANAGEMENT|REALTY|RLTY|RLTYCP|DEVELOPMENT|REDEVELOPMENT|"
    r"STORAGE|ASSOCIATES|HOLDINGS?|PROPERTIES|EQUITIES|TOWERS)\b"
    r"|\b(CHURCH|CONVENT|TEMPLE|CHAPEL|CATHEDRAL)\s+(ST|STREET|AVE|AVENUE|PL|PLACE|"
    r"RD|ROAD|LN|LANE|TER|TERRACE|HILL|SQ|PKWY|PARKWAY)\b"
    r"|^[\d-]+\s+(CHURCH|CONVENT|TEMPLE|CHAPEL)\b)"
)
# "SURNAME, GIVEN NAMES" with no INC or CORP is a person.
PERSON_OWNER_RE = r"^[A-Z'-]+( [A-Z'-]+)?, [A-Z ]+$"
FIRM_WORD_RE = r"\b(INC|CORP)\b"


def sql_str(s: str) -> str:
    """Quote a Python string as a SQL string literal."""
    return "'" + s.replace("'", "''") + "'"


def attach_points(con, src_table, id_col, out_table):
    """Point-in-lot, then nearest lot within NEAREST_LOT_M for the rest."""
    con.execute(f"""
        CREATE OR REPLACE TEMP TABLE _within AS
        SELECT s.{id_col} AS id, t.bbl
        FROM {src_table} s JOIN taxlots t ON ST_Contains(t.geom, s.geom)
    """)
    # A point can sit on two overlapping lots (rare); keep the smaller lot.
    con.execute(f"""
        CREATE OR REPLACE TEMP TABLE _within1 AS
        SELECT w.id, arg_min(w.bbl, ST_Area(t.geom)) AS bbl
        FROM _within w JOIN taxlots t USING (bbl) GROUP BY w.id
    """)
    deg = NEAREST_LOT_M / 80_000  # generous degree pre-filter at NYC latitude
    con.execute(f"""
        CREATE OR REPLACE TEMP TABLE _nearest AS
        WITH miss AS (
          SELECT s.{id_col} AS id, s.geom FROM {src_table} s
          WHERE s.{id_col} NOT IN (SELECT id FROM _within1)
        ), cand AS (
          SELECT m.id, t.bbl,
                 ST_Distance(ST_Transform(m.geom, 'EPSG:4326', 'EPSG:2263', always_xy := true),
                             ST_Transform(t.geom, 'EPSG:4326', 'EPSG:2263', always_xy := true))
                   * 0.3048 AS dist_m
          FROM miss m JOIN taxlots t ON ST_DWithin(t.geom, m.geom, {deg})
        )
        SELECT id, arg_min(bbl, dist_m) AS bbl, min(dist_m) AS dist_m
        FROM cand GROUP BY id HAVING min(dist_m) <= {NEAREST_LOT_M}
    """)
    con.execute(f"""
        CREATE OR REPLACE TABLE {out_table} AS
        SELECT s.{id_col} AS id,
               coalesce(w.bbl, n.bbl) AS bbl,
               CASE WHEN w.bbl IS NOT NULL THEN 'within'
                    WHEN n.bbl IS NOT NULL THEN 'nearest' ELSE 'none' END AS lot_match,
               CASE WHEN w.bbl IS NOT NULL THEN 0 ELSE n.dist_m END AS lot_dist_m
        FROM {src_table} s
        LEFT JOIN _within1 w ON w.id = s.{id_col}
        LEFT JOIN _nearest n ON n.id = s.{id_col}
    """)


def flag_lots(con):
    con.execute(f"""
        CREATE OR REPLACE TABLE lot_flags AS
        WITH sch AS (
          SELECT ss.bbl, count(*) AS n_schools,
                 string_agg(s.name || ' (' || replace(s.source, 'nces_', '') || ')', '; '
                            ORDER BY s.name) AS school_names,
                 bool_or(s.source = 'nces_public') AS has_public_school,
                 bool_or(s.source = 'nces_private') AS has_private_school
          FROM school_lot ss JOIN schools s ON s.school_id = ss.id
          WHERE ss.bbl IS NOT NULL GROUP BY ss.bbl
        )
        SELECT p.bbl, p.bldgclass, p.landuse, p.ownertype, p.ownername, p.exempttot,
               p.address AS lot_address, p.bldgarea, p.numfloors,
               p.bldgclass LIKE 'M%' AS rel_bldgclass,
               coalesce(regexp_matches(p.ownername, {sql_str(RELIGIOUS_OWNER_RE)})
                        AND NOT regexp_matches(p.ownername, {sql_str(NOT_RELIGIOUS_OWNER_RE)})
                        AND NOT (regexp_matches(p.ownername, {sql_str(PERSON_OWNER_RE)})
                                 AND NOT regexp_matches(p.ownername, {sql_str(FIRM_WORD_RE)})),
                        false) AS rel_owner,
               (p.bldgclass LIKE 'M%' OR rel_owner) AS religious_owned,
               (p.landuse IN (4, 5) OR left(p.bldgclass, 1) IN ('K', 'O', 'S'))
                 AS commercial_use,
               p.landuse IN (1, 2, 3) AS residential_use,
               CASE p.landuse WHEN 1 THEN 'one-two family' WHEN 2 THEN 'walk-up'
                    WHEN 3 THEN 'elevator apts' WHEN 4 THEN 'mixed res-commercial'
                    WHEN 5 THEN 'commercial-office' WHEN 6 THEN 'industrial'
                    WHEN 7 THEN 'transport-utility' WHEN 8 THEN 'public-institution'
                    WHEN 9 THEN 'open space' WHEN 10 THEN 'parking'
                    WHEN 11 THEN 'vacant' END AS landuse_label,
               coalesce(sch.n_schools, 0) AS n_schools, sch.school_names,
               coalesce(sch.has_public_school, false) AS has_public_school,
               coalesce(sch.has_private_school, false) AS has_private_school
        FROM parcels p LEFT JOIN sch USING (bbl)
    """)


def main():
    con = connect(config.DB_PATH)
    print("attaching places to lots ...")
    attach_points(con, "places", "id", "place_lot")
    print("attaching schools to lots ...")
    attach_points(con, "schools", "school_id", "school_lot")
    print("flagging lots ...")
    flag_lots(con)
    print(con.execute("""
        SELECT lot_match, count(*) AS places, round(avg(lot_dist_m), 1) AS avg_dist_m
        FROM place_lot GROUP BY 1 ORDER BY 2 DESC
    """).df().to_string(index=False))
    print(con.execute("""
        SELECT count(*) FILTER (WHERE religious_owned) AS religious_owned_lots,
               count(*) FILTER (WHERE rel_bldgclass) AS m_class_lots,
               count(*) FILTER (WHERE rel_owner AND NOT rel_bldgclass) AS owner_name_only,
               count(*) FILTER (WHERE n_schools > 0) AS lots_with_school
        FROM lot_flags
    """).df().to_string(index=False))


if __name__ == "__main__":
    main()
