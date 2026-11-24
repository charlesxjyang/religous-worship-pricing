"""San Francisco loaders: supervisor districts, parcels and the address geocoder.

Sources (DataSF, data.sf.gov):
- Supervisor Districts (2022), f2zs-jevy: 11 districts, SF's subareas.
- Parcels - Active and Retired, acdm-wktn: lot polygons (blklot; condominium
  units share their base lot, mapblklot).
- Assessor Historical Secured Property Tax Rolls, wv5m-vpq2, closed roll 2025:
  use and property class codes, exemption codes, assessed values, lot and
  building area, last sale date. State law bars publishing owner names
  online, so the roll has none; religious use comes from the property class
  (W, churches, convents, rectories) and the church (7) and religious (6)
  exemptions.
- Enterprise Addressing System, 3mea-di5p: every address with its parcel.

Assessed values follow Proposition 13: the base is the price at the last sale
plus at most 2% a year, so only recently sold parcels carry a near-market
value (last_sale is kept for that reason).

The lot key is mapblklot; bbl is a surrogate integer, as for DC and Charlotte.
"""

import json
import urllib.parse

import addrgeo
import config
from common import download

SODA = "https://data.sf.gov/resource"
DISTRICTS = "f2zs-jevy"
PARCELS = "acdm-wktn"
ROLL = "wv5m-vpq2"
ADDRESSES = "3mea-di5p"
ROLL_YEAR = "2025"
PAGE = 50_000

# Assessor property class code -> NYC DOF building class (first letter is what later steps read).
_CLASS = {
    "M1": ["W"],
    "W1": ["EG"], "W8": ["E"],
    "K1": ["C", "CZ", "CM", "CD", "CG", "B", "BZ", "OC"], "K4": ["C1", "C1G"],
    "O1": ["O", "OZ", "OG", "OMD", "OCL", "OCH", "OCM", "OAL", "OAH", "OBH", "OBM", "OBL", "OAM", "O35", "OZEU"],
    "H1": ["H", "H1", "H2", "HC", "HG", "M", "MG", "RH1"], "H8": ["RH", "RHG"],
    "F1": ["I", "IG", "IX", "IXG", "IZ", "IDC"], "E1": ["IW"],
    "G0": ["G", "GG", "GZ", "PZ", "PL", "PLG"], "G5": ["S"],
    "P8": ["LIBG"], "P9": ["U", "UG"], "J1": ["T", "EC", "ECG"],
    "I1": ["N1", "N1G"], "I6": ["N2", "N2G"],
    "Y9": ["FIRG", "POLG", "SP", "PI"], "Z9": ["CONG", "X"], "Q9": ["GC"],
    "V0": ["V", "VPUB", "VR", "VRX", "VCI", "VA15", "VG", "VSP", "UWL", "TDR"],
    "R4": ["Z", "ZBM", "ZEU", "LZ", "LZBM", "TS", "TSF", "TSU"], "D4": ["CO", "COS"],
    "A1": ["D", "DBM", "DCON", "PD", "TH", "THBM"],
    "B1": ["F", "DD", "DF", "FA", "XV"],
    "C0": ["A", "DA", "AG", "TIC", "TIA", "F5", "FA5", "DD5"],
    "C1": ["A5", "A5G", "DA5", "F15", "DD15"], "D1": ["A15", "DA15", "TI15"],
    "S9": ["FS", "FS5", "FS15", "F2", "AC", "ACG", "OA", "OA5", "OA15"],
}
CLASS_OF = {code: cls for cls, codes in _CLASS.items() for code in codes}
CONDO = {"Z", "ZBM", "ZEU", "LZ", "LZBM", "CZ", "OZ", "OZEU", "BZ", "IZ", "GZ", "PZ", "COS"}
CLASS_TO_LANDUSE = {"A": 1, "B": 1, "C": 2, "D": 3, "R": 3, "S": 4, "K": 5, "O": 5, "H": 5, "J": 5,
                    "E": 6, "F": 6, "G": 10, "M": 8, "W": 8, "I": 8, "Y": 8, "P": 8, "Z": 8,
                    "Q": 9, "V": 11}


def soda_pages(dataset, params, dest_dir, ext):
    """All pages of a DataSF query, PAGE rows per request, cached as files."""
    count = json.loads(download(
        f"{SODA}/{dataset}.json?" + urllib.parse.urlencode(
            {"$select": "count(*)", **({"$where": params["$where"]} if "$where" in params else {})}),
        dest_dir / "count.json").read_text())[0]
    total = int(next(iter(count.values())))
    parts = []
    for i, offset in enumerate(range(0, total, PAGE)):
        q = urllib.parse.urlencode({**params, "$limit": PAGE, "$offset": offset})
        part = dest_dir / f"part-{i:04d}.{ext}"
        if not part.exists():
            print(f"  {dataset}: rows {offset:,}-{min(offset + PAGE, total):,} of {total:,}")
        parts.append(download(f"{SODA}/{dataset}.{ext}?{q}", part))
    return parts


def load_boundary(con):
    path = download(f"{SODA}/{DISTRICTS}.geojson?$limit=100", config.RAW / "sf_supervisor_districts_2022.geojson")
    con.execute(f"""
        CREATE OR REPLACE TABLE boroughs AS
        SELECT CAST(sup_dist_num AS INT) AS borocode, 'District ' || CAST(CAST(sup_dist_num AS INT) AS VARCHAR) AS boroname,
               geom::GEOMETRY AS geom
        FROM ST_Read('{path}')
    """)
    con.execute("CREATE OR REPLACE TABLE city AS SELECT ST_Union_Agg(geom) AS geom FROM boroughs")


def load_parcels(con):
    pdir, rdir = config.RAW / "sf_parcels", config.RAW / f"sf_roll_{ROLL_YEAR}"
    for d in (pdir, rdir):
        d.mkdir(parents=True, exist_ok=True)
    parcel_parts = soda_pages(PARCELS, {"$select": "blklot,mapblklot,from_address_num,street_name,street_type,shape",
                                        "$where": "active = true", "$order": "blklot"}, pdir, "geojson")
    roll_parts = soda_pages(ROLL, {"$select": "parcel_number,use_code,property_class_code,year_property_built,"
                                              "number_of_units,number_of_stories,property_area,lot_area,"
                                              "exemption_code,current_sales_date,assessed_land_value,"
                                              "assessed_improvement_value",
                                   "$where": f"closed_roll_year = '{ROLL_YEAR}'", "$order": "parcel_number"},
                            rdir, "csv")
    union = " UNION ALL ".join(f"SELECT blklot, mapblklot, from_address_num, street_name, street_type, geom "
                               f"FROM ST_Read('{p}')" for p in parcel_parts)
    con.execute(f"""
        CREATE OR REPLACE TABLE sf_parcels_raw AS
        SELECT trim(blklot) AS blklot, coalesce(nullif(trim(mapblklot), ''), trim(blklot)) AS mapblklot,
               nullif(trim(concat_ws(' ', from_address_num, street_name, street_type)), '') AS address,
               geom::GEOMETRY AS geom
        FROM ({union}) WHERE blklot IS NOT NULL AND geom IS NOT NULL
    """)
    files = ", ".join(f"'{p}'" for p in roll_parts)
    con.execute(f"""
        CREATE OR REPLACE TABLE sf_roll AS
        SELECT trim(parcel_number) AS blklot, trim(use_code) AS use_code, trim(property_class_code) AS class_code,
               TRY_CAST(year_property_built AS INT) AS yearbuilt, TRY_CAST(number_of_units AS DOUBLE) AS units,
               TRY_CAST(number_of_stories AS DOUBLE) AS stories, TRY_CAST(property_area AS DOUBLE) AS bldgarea,
               TRY_CAST(lot_area AS DOUBLE) AS lot_area, nullif(trim(exemption_code), 'NA') AS exemption,
               TRY_CAST(current_sales_date AS TIMESTAMP)::DATE AS last_sale,
               TRY_CAST(assessed_land_value AS DOUBLE) AS land_value,
               TRY_CAST(assessed_improvement_value AS DOUBLE) AS impr_value
        FROM read_csv([{files}], all_varchar = true, header = true)
    """)
    cls_case = "CASE " + " ".join(f"WHEN r.class_code = '{k}' THEN '{v}'" for k, v in CLASS_OF.items()) + " END"
    condo = ", ".join(f"'{c}'" for c in CONDO)
    con.execute("""CREATE OR REPLACE TABLE sf_lot AS SELECT mapblklot, row_number() OVER (ORDER BY mapblklot) AS bbl
                   FROM (SELECT DISTINCT mapblklot FROM sf_parcels_raw)""")
    con.execute("""CREATE OR REPLACE TABLE taxlots AS
        SELECT l.bbl, NULL::VARCHAR AS condo_flag, ST_Union_Agg(p.geom) AS geom
        FROM sf_parcels_raw p JOIN sf_lot l USING (mapblklot) GROUP BY l.bbl""")
    lu_case = ("CASE " + " ".join(f"WHEN left(bldgclass, 1) = '{k}' THEN {v}"
                                  for k, v in CLASS_TO_LANDUSE.items()) + " END")
    con.execute(f"""
        CREATE OR REPLACE TABLE pluto AS
        WITH units AS (
          SELECT p.mapblklot, p.blklot, p.address, r.*, {cls_case} AS cls, r.class_code IN ({condo}) AS is_condo,
                 coalesce(r.exemption IN ('6', '7'), false) AS rel_ex
          FROM sf_parcels_raw p LEFT JOIN sf_roll r ON r.blklot = p.blklot
        ), lot AS (
          SELECT mapblklot,
                 -- the lot's character: a church first, then a religious exemption, then the biggest unit
                 first(cls ORDER BY (cls LIKE 'M%') DESC, rel_ex DESC, cls IS NULL, bldgarea DESC NULLS LAST) AS bldgclass,
                 first(class_code ORDER BY (cls LIKE 'M%') DESC, rel_ex DESC, cls IS NULL, bldgarea DESC NULLS LAST) AS class_code,
                 first(address ORDER BY address IS NULL, blklot) AS address,
                 bool_or(rel_ex) AS exempt_religious,
                 first(exemption ORDER BY exemption IS NULL, exemption) AS exemption,
                 bool_and(coalesce(is_condo, false)) AND count(*) > 1 AS condo_lot,
                 sum(land_value) AS assessland, sum(land_value + coalesce(impr_value, 0)) AS assesstot,
                 max(lot_area) AS lotarea, sum(bldgarea) AS bldgarea, sum(units) AS unitstotal,
                 max(stories) AS numfloors, min(nullif(yearbuilt, 0)) AS yearbuilt,
                 max(last_sale) AS last_sale, count(*) AS n_units
          FROM units GROUP BY mapblklot
        )
        SELECT l.bbl, NULL::VARCHAR AS borough, NULL AS cd, NULL AS bct2020, x.address, x.bldgclass,
               NULL::INT AS landuse,
               CASE WHEN x.exemption IN ('2', '3', '6', '7', '8', '14') THEN 'X' END AS ownertype,
               NULL::VARCHAR AS ownername,
               x.lotarea, x.bldgarea, NULL::DOUBLE AS comarea, NULL::DOUBLE AS resarea, NULL::DOUBLE AS officearea,
               NULL::DOUBLE AS retailarea, NULL::DOUBLE AS numbldgs, x.numfloors, NULL::DOUBLE AS unitsres,
               x.unitstotal, x.assessland, x.assesstot, NULL::DOUBLE AS exempttot, x.yearbuilt,
               NULL::DOUBLE AS latitude, NULL::DOUBLE AS longitude, 'SF secured roll {ROLL_YEAR}' AS version,
               x.mapblklot, x.class_code, x.exemption, x.exempt_religious, x.condo_lot, x.last_sale, x.n_units,
               false AS owner_is_person
        FROM lot x JOIN sf_lot l USING (mapblklot)
    """)
    # As in DC and Charlotte: a church or religious exemption means religious use,
    # unless the lot is a school (the religious exemption also covers parish schools).
    con.execute("ALTER TABLE pluto ADD COLUMN bldgclass_landuse VARCHAR")
    con.execute("UPDATE pluto SET bldgclass_landuse = bldgclass")
    con.execute("UPDATE pluto SET bldgclass = 'M9' WHERE exempt_religious AND left(coalesce(bldgclass, ''), 1) NOT IN ('M', 'W')")
    con.execute(f"UPDATE pluto SET landuse = {lu_case}")
    con.execute("""
        CREATE OR REPLACE TABLE parcels AS
        SELECT t.bbl, t.condo_flag, p.* EXCLUDE (bbl), t.geom
        FROM taxlots t LEFT JOIN pluto p USING (bbl)
    """)


def _keys(text):
    full, loose = addrgeo.us_address_keys(text)
    return [full, loose]


def make_geocoder(con):
    adir = config.RAW / "sf_eas_addresses"
    adir.mkdir(parents=True, exist_ok=True)
    parts = soda_pages(ADDRESSES, {"$select": "address,parcel_number,latitude,longitude", "$order": "eas_address_id"},
                       adir, "csv")
    files = ", ".join(f"'{p}'" for p in parts)
    rows = con.execute(f"""
        SELECT a.address, l.bbl, NULL, TRY_CAST(a.latitude AS DOUBLE), TRY_CAST(a.longitude AS DOUBLE)
        FROM read_csv([{files}], all_varchar = true, header = true) a
        JOIN sf_parcels_raw p ON p.blklot = trim(a.parcel_number)
        JOIN sf_lot l USING (mapblklot)
        WHERE a.address IS NOT NULL
    """).fetchall()
    rows += con.execute("""
        SELECT p.address, p.bbl, NULL, ST_Y(ST_Centroid(t.geom)), ST_X(ST_Centroid(t.geom))
        FROM pluto p JOIN taxlots t USING (bbl) WHERE p.address IS NOT NULL
    """).fetchall()
    return addrgeo.make_geocoder(rows, _keys, "CA")
