"""Version 0, step 1: load the three inputs into DuckDB and report (CITY=nyc|dc).

Inputs: Overture places, PLUTO + DOF tax-lot polygons, NCES schools.
Prints category counts and 20 sample rows, writes v0/step1_report.md, and
stops for a human sanity check. Nothing here calls a paid API.

Run:  .venv/bin/python v0/step1_load.py
"""

import datetime as dt
import zipfile

import config
from common import connect, download, latest_overture_release, socrata_pages

BLDGCLASS_M = {
    "M1": "Church, synagogue, chapel",
    "M2": "Mission house (non-residential)",
    "M3": "Parsonage, rectory",
    "M4": "Convent",
    "M9": "Miscellaneous religious facility",
}


# ---------------------------------------------------------------- loaders --

def load_boroughs(con):
    path = download(f"{config.SOCRATA}/resource/{config.BOROUGHS_DATASET}.geojson",
                    config.RAW / "borough_boundaries_wi.geojson")
    con.execute(f"""
        CREATE OR REPLACE TABLE boroughs AS
        SELECT CAST(borocode AS INT) AS borocode, boroname, geom::GEOMETRY AS geom
        FROM ST_Read('{path}')
    """)
    con.execute("CREATE OR REPLACE TABLE city AS SELECT ST_Union_Agg(geom) AS geom FROM boroughs")


def load_overture(con, release):
    src = (f"s3://{config.OVERTURE_BUCKET}/release/{release}/"
           "theme=places/type=place/*")
    keep = ", ".join(f"'{c}'" for c in config.KEEP_CATEGORIES)
    b = config.NYC_BBOX
    out = config.RAW / f"overture_places_{release}_{config.CITY}.parquet"
    if not out.exists():
        print(f"  scanning Overture {release} on S3 ...")
        # Religious-looking categories outside the keep list are pulled too,
        # flagged kept = false, so the report can show what is left out.
        con.execute(f"""
            COPY (
              SELECT p.id, p.names.primary AS name, p.basic_category,
                     p.taxonomy.primary AS taxonomy_primary,
                     array_to_string(p.taxonomy.hierarchy, ' > ') AS taxonomy_path,
                     p.basic_category IN ({keep}) AS kept,
                     p.websites, p.socials, p.phones,
                     p.addresses[1].freeform AS address,
                     p.addresses[1].postcode AS postcode,
                     p.confidence, p.operating_status,
                     list_transform(p.sources, lambda s: s.dataset) AS source_datasets,
                     ST_X(p.geometry) AS lon, ST_Y(p.geometry) AS lat
              FROM read_parquet('{src}', hive_partitioning = 1) p
              WHERE p.bbox.xmin BETWEEN {b['xmin']} AND {b['xmax']}
                AND p.bbox.ymin BETWEEN {b['ymin']} AND {b['ymax']}
                AND (p.basic_category IN ({keep})
                     OR p.taxonomy.primary IN ('religious_school',
                                               'religious_and_spiritual_goods_store')
                     OR list_contains(p.taxonomy.hierarchy, 'place_of_worship'))
            ) TO '{out}' (FORMAT parquet)
        """)
    con.execute(f"""
        CREATE OR REPLACE TABLE overture_nyc AS
        SELECT o.*, b.boroname, ST_Point(o.lon, o.lat) AS geom
        FROM read_parquet('{out}') o
        JOIN boroughs b ON ST_Contains(b.geom, ST_Point(o.lon, o.lat))
    """)
    con.execute("CREATE OR REPLACE VIEW places AS SELECT * FROM overture_nyc WHERE kept")
    return out


def load_parcels(con):
    pluto_parts = socrata_pages(config.PLUTO_DATASET, config.PLUTO_COLUMNS,
                                config.RAW / "pluto_26v2", order=":id")
    lot_parts = socrata_pages(config.TAXLOT_DATASET, config.TAXLOT_COLUMNS,
                              config.RAW / "dof_taxlots", order=":id")
    pluto_glob = str(pluto_parts[0].parent / "part-*.csv")
    lot_glob = str(lot_parts[0].parent / "part-*.csv")
    num = ["lotarea", "bldgarea", "comarea", "resarea", "officearea", "retailarea",
           "numbldgs", "numfloors", "unitsres", "unitstotal", "assessland",
           "assesstot", "exempttot", "yearbuilt", "latitude", "longitude"]
    num_sql = ",\n               ".join(f"TRY_CAST({c} AS DOUBLE) AS {c}" for c in num)
    con.execute(f"""
        CREATE OR REPLACE TABLE pluto AS
        SELECT CAST(CAST(bbl AS DOUBLE) AS BIGINT) AS bbl,
               borough, cd, bct2020, address, zipcode, bldgclass,
               TRY_CAST(landuse AS INT) AS landuse, ownertype, ownername,
               {num_sql},
               version
        FROM read_csv('{pluto_glob}', header = true, all_varchar = true)
    """)
    con.execute(f"""
        CREATE OR REPLACE TABLE taxlots AS
        SELECT CAST(bbl AS BIGINT) AS bbl, condo_flag,
               ST_GeomFromText(the_geom) AS geom
        FROM read_csv('{lot_glob}', header = true, all_varchar = true)
        WHERE the_geom IS NOT NULL
    """)
    # One row per lot polygon, with PLUTO attributes where the BBL matches.
    con.execute("""
        CREATE OR REPLACE TABLE parcels AS
        SELECT t.bbl, t.condo_flag, p.* EXCLUDE (bbl), t.geom
        FROM taxlots t LEFT JOIN pluto p USING (bbl)
    """)


def load_schools(con):
    pub_zip = download(f"{config.NCES_BASE}/{config.NCES_PUBLIC_ZIP}",
                       config.RAW / config.NCES_PUBLIC_ZIP)
    prv_zip = download(f"{config.NCES_BASE}/{config.NCES_PRIVATE_ZIP}",
                       config.RAW / config.NCES_PRIVATE_ZIP)
    pub_txt = config.RAW / config.NCES_PUBLIC_TXT
    if not pub_txt.exists():
        with zipfile.ZipFile(pub_zip) as z:
            z.extract(config.NCES_PUBLIC_TXT, config.RAW)
    cols = "{" + ", ".join(f"'{c}': 'VARCHAR'" for c in config.NCES_PUBLIC_FIELDS) + "}"
    con.execute(f"""
        CREATE OR REPLACE TABLE schools AS
        WITH pub AS (
          SELECT 'nces_public' AS source, NCESSCH AS school_id, NAME AS name,
                 STREET AS street, CITY AS city, ZIP AS zip,
                 CAST(LAT AS DOUBLE) AS lat, CAST(LON AS DOUBLE) AS lon,
                 SCHOOLYEAR AS school_year
          FROM read_csv('{pub_txt}', delim = '|', header = false, columns = {cols},
                        quote = '"', encoding = 'latin-1')
          WHERE STATE = '{config.STATE}'
        ), prv AS (
          SELECT 'nces_private' AS source, PPIN AS school_id, NAME AS name,
                 STREET AS street, CITY AS city, ZIP AS zip, LAT AS lat, LON AS lon,
                 SCHOOLYEAR AS school_year
          FROM ST_Read('/vsizip/{prv_zip}/{config.NCES_PRIVATE_SHP}')
          WHERE STATE = '{config.STATE}'
        )
        SELECT s.*, b.boroname, ST_Point(s.lon, s.lat) AS geom
        FROM (SELECT * FROM pub UNION ALL SELECT * FROM prv) s
        JOIN boroughs b ON ST_Contains(b.geom, ST_Point(s.lon, s.lat))
    """)


# ----------------------------------------------------------------- report --

def md_table(df, max_chars=60):
    def cell(v):
        if isinstance(v, (list, tuple)) or hasattr(v, "tolist"):
            v = ", ".join(str(x) for x in list(v)) if v is not None else ""
        s = "" if v is None or (isinstance(v, float) and v != v) else str(v)
        s = s.replace("|", "\\|").replace("\n", " ")
        return s if len(s) <= max_chars else s[: max_chars - 1] + "…"
    head = "| " + " | ".join(df.columns) + " |"
    sep = "| " + " | ".join("---" for _ in df.columns) + " |"
    rows = ["| " + " | ".join(cell(v) for v in r) + " |" for r in df.itertuples(index=False)]
    return "\n".join([head, sep, *rows])


def build_report(con, release, overture_file):
    q = lambda sql: con.execute(sql).df()  # noqa: E731
    n = lambda sql: con.execute(sql).fetchone()[0]  # noqa: E731
    out = []
    w = out.append

    n_places = n("SELECT count(*) FROM places")
    n_web = n("SELECT count(*) FROM places WHERE len(websites) > 0")
    n_lots = n("SELECT count(*) FROM taxlots")
    n_pluto = n("SELECT count(*) FROM pluto")
    n_lot_match = n("SELECT count(*) FROM parcels WHERE bldgclass IS NOT NULL OR landuse IS NOT NULL OR ownername IS NOT NULL")
    pluto_version = n("SELECT any_value(version) FROM pluto")

    w(f"# Version 0, step 1: {config.CITY_NAME} inputs loaded\n")
    w(f"Run {dt.date.today().isoformat()}. Overture release {release}; "
      f"parcels {pluto_version}; NCES public 2024-25 and private 2023-24. "
      "Stop here for a sanity check before step 2.\n")

    if config.CITY == "dc":
        area, area_src = "Ward", "DCGIS Ward - 2022"
        lot_src, rec_src = "DC OTR owner polygons", "ITSPE, with RPTA tax exemptions"
    else:
        area, area_src = "Borough", f"NYC Open Data {config.BOROUGHS_DATASET}, water included"
        lot_src = f"DOF tax lots, NYC Open Data {config.TAXLOT_DATASET}"
        rec_src = f"PLUTO, NYC Open Data {config.PLUTO_DATASET}"
    w("## Inputs\n")
    w(md_table(q(f"""
        SELECT * FROM (VALUES
          ('Overture places, kept categories', {n_places}, 'inside the city'),
          ('{area} boundaries', {n("SELECT count(*) FROM boroughs")}, '{area_src}'),
          ('Parcel polygons', {n_lots}, '{lot_src}'),
          ('Parcel records', {n_pluto}, '{rec_src}'),
          ('Polygons with a parcel record', {n_lot_match}, '{100 * n_lot_match / n_lots:.1f}% of polygons'),
          ('NCES public schools', {n("SELECT count(*) FROM schools WHERE source = 'nces_public'")}, 'EDGE 2024-25'),
          ('NCES private schools', {n("SELECT count(*) FROM schools WHERE source = 'nces_private'")}, 'EDGE 2023-24')
        ) t(input, rows, note)
    """)))

    w("\n## Overture: counts by basic category\n")
    w(f"{n_places:,} places in the kept categories; {n_web:,} "
      f"({100 * n_web / n_places:.0f}%) carry a website.\n")
    w(md_table(q("""
        SELECT basic_category, count(*) AS places,
               round(100 * avg((coalesce(len(websites), 0) > 0)::INT)) AS pct_website,
               round(100 * avg((coalesce(len(phones), 0) > 0)::INT)) AS pct_phone,
               round(median(confidence), 2) AS median_confidence
        FROM places GROUP BY 1 ORDER BY 2 DESC
    """)))

    w("\n## Overture: confidence bands\n")
    w("Overture's confidence that the place exists. Low bands are candidates "
      "for a cutoff in step 2.\n")
    w(md_table(q("""
        SELECT CASE WHEN confidence < 0.5 THEN 'a. under 0.50'
                    WHEN confidence < 0.7 THEN 'b. 0.50-0.69'
                    WHEN confidence < 0.9 THEN 'c. 0.70-0.89'
                    ELSE 'd. 0.90 and up' END AS band,
               count(*) AS places,
               count(*) FILTER (WHERE operating_status = 'permanently_closed') AS closed
        FROM places GROUP BY 1 ORDER BY 1
    """)))
    zips = ", ".join(f"'{z}'" for z in config.ZIP3)
    n_zip_out = n(f"""
        SELECT count(*) FROM places
        WHERE postcode IS NOT NULL AND left(postcode, 3) NOT IN ({zips})
    """)
    w(f"\n{n_zip_out:,} places sit inside the city but list a ZIP code outside "
      f"{config.CITY_SHORT}, a sign the point or the address is wrong.\n")

    w(f"\n## Overture: category by {config.AREA_LABEL}\n")
    w(md_table(q("""
        PIVOT (SELECT basic_category, boroname FROM places)
        ON boroname USING count(*) GROUP BY basic_category ORDER BY basic_category
    """)))

    w("\n## Overture: detailed taxonomy within kept categories\n")
    w(md_table(q("""
        SELECT taxonomy_primary, basic_category, count(*) AS places
        FROM places GROUP BY 1, 2 ORDER BY 3 DESC
    """)))

    w("\n## Overture: operating status and source datasets\n")
    w(md_table(q("""
        SELECT coalesce(operating_status, '(null)') AS operating_status, count(*) AS places
        FROM places GROUP BY 1 ORDER BY 2 DESC
    """)))
    w("")
    w(md_table(q("""
        SELECT ds AS source_dataset, count(DISTINCT id) AS places
        FROM (SELECT id, unnest(source_datasets) AS ds FROM places)
        GROUP BY 1 ORDER BY 2 DESC
    """)))

    w("\n## Overture: religious-looking places left out by the category filter\n")
    w(md_table(q("""
        SELECT taxonomy_primary, basic_category, count(*) AS places
        FROM overture_nyc WHERE NOT kept GROUP BY 1, 2 ORDER BY 3 DESC
    """)))

    # Sample rows name places and addresses: point-level, so they go to the
    # gitignored private folder, not the committed report.
    samples = md_table(q(f"""
        SELECT name, taxonomy_primary AS category, boroname AS borough, address,
               websites[1] AS website, round(confidence, 2) AS conf, operating_status AS status
        FROM (SELECT * FROM places ORDER BY id)
        USING SAMPLE reservoir(20 ROWS) REPEATABLE ({config.SAMPLE_SEED})
        ORDER BY borough, name
    """), max_chars=45)
    config.PRIVATE_DIR.mkdir(parents=True, exist_ok=True)
    sample_path = config.PRIVATE_DIR / "step1_samples.md"
    sample_path.write_text(f"# 20 random places (seed {config.SAMPLE_SEED})\n\n{samples}\n")
    w(f"\n## Overture: 20 random places\n")
    w(f"In `{sample_path.relative_to(config.ROOT)}` (not committed: it names places and addresses).\n")

    w("\n## Parcels: religious building classes\n")
    m = q("""
        SELECT bldgclass, count(*) AS lots, count(*) FILTER (WHERE ownertype = 'X') AS owner_type_x,
               round(sum(bldgarea)) AS bldg_area_sqft
        FROM pluto WHERE bldgclass LIKE 'M%' GROUP BY 1 ORDER BY 1
    """)
    m.insert(1, "label", m["bldgclass"].map(BLDGCLASS_M).fillna(""))
    w(md_table(m))
    n_lu8 = n("SELECT count(*) FROM pluto WHERE landuse = 8")
    n_x = n("SELECT count(*) FROM pluto WHERE ownertype = 'X'")
    w(f"\nLand use 08 (public facilities and institutions): {n_lu8:,} lots. "
      f"Owner type X (fully exempt, privately owned): {n_x:,} lots.\n")

    w(f"## Schools by {config.AREA_LABEL}\n")
    w(md_table(q("""
        PIVOT (SELECT source, boroname FROM schools)
        ON boroname USING count(*) GROUP BY source ORDER BY source
    """)))
    w("\nFive random schools of each kind:\n")
    w(md_table(q(f"""
        SELECT source, name, street, boroname AS borough FROM (
          SELECT *, row_number() OVER (PARTITION BY source ORDER BY hash(school_id || '{config.SAMPLE_SEED}')) AS r
          FROM schools) WHERE r <= 5 ORDER BY source, name
    """)))

    w("\n## Files\n")
    w(f"- DuckDB: `{config.DB_PATH.relative_to(config.ROOT)}` "
      "(tables boroughs, city, overture_nyc, pluto, taxlots, parcels, schools; view places)")
    w(f"- Overture extract: `{overture_file.relative_to(config.ROOT)}`")
    w(f"- Raw downloads: `data/{config.CITY}/raw/` (not committed)")
    return "\n".join(out) + "\n"


def main():
    config.RAW.mkdir(parents=True, exist_ok=True)
    release = config.OVERTURE_RELEASE or latest_overture_release()
    con = connect(config.DB_PATH)
    if config.CITY == "dc":
        import dc
        print("wards ...");     dc.load_boundary(con)
        print("overture ...");  overture_file = load_overture(con, release)
        print("parcels ...");   dc.load_parcels(con)
    else:
        print("boroughs ...");  load_boroughs(con)
        print("overture ...");  overture_file = load_overture(con, release)
        print("parcels ...");   load_parcels(con)
    print("schools ...");   load_schools(con)
    config.REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report = build_report(con, release, overture_file)
    (config.REPORT_DIR / "step1_report.md").write_text(report)
    print("\n" + report)
    print(f"Step 1 done. Review {(config.REPORT_DIR / 'step1_report.md').relative_to(config.ROOT)} "
          "before running step 2.")


if __name__ == "__main__":
    main()
