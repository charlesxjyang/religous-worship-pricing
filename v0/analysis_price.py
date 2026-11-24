"""Do congregations share space more where commercial space is dear? (NYC, DC, Charlotte, SF, Houston)

Price: assessed market value of land per square foot of lot, for retail and
office lots, the kind of space a congregation rents (NYC building classes K
and O; DC use codes and Charlotte land-use descriptions that step 1 maps to K
and O; condominium lots left out, since their land value is a share).

- NYC: PLUTO's assessed land value / 0.45 (retail and office lots are tax
  class 4, assessed at 45% of DOF market value), over lot area.
- DC: OTR's land value (NEWLAND, full market value) over land area, pulled
  here for commercial use codes only (step 1 kept total value only).
- Charlotte: Mecklenburg County's CAMA land value (amt_landvalue, 2023
  revaluation, market value) over the parcel polygon's area, pulled here for
  retail and office property uses in the city.
- San Francisco: assessed land value over parcel area for retail and office
  parcels sold since 2015. Proposition 13 keeps a parcel's assessment at its
  last sale price plus at most 2% a year, so older assessments are far below
  market (a median $158 per sq ft for retail parcels last sold before 2000,
  against $554 for those sold since 2015).
- Houston: HCAD market land value over land area (Texas appraises at market
  every year).

Each congregation gets the median over commercial lots within 1 km of its
listing point (2 km where fewer than 10 lie within 1 km). Areas for maps and
clustered errors: NYC community districts, DC neighborhood clusters,
Charlotte's 15 community planning areas (few clusters: treat Charlotte's own
standard errors as rough), SF's 41 analysis neighborhoods, Houston's 88 super
neighborhoods.

The test is a linear probability model at the congregation level: outcome
(sharing worship space, sharing the property, multi-use, meeting in a store or
office unit) on log2 local price, with city fixed effects, then adding
tradition and the number of congregations within 1 km. Standard errors are
clustered by area. Coefficients read as percentage points per doubling of
the local land price.

Placement is the listing address (cong_sharing_raw), so in a session without
website extraction this runs on listings only; the report says which.

Run after step 5 and analysis_sharing.py / analysis_services.py for every city:
    .venv/bin/python v0/analysis_price.py
Writes tables commercial_lots and cong_price in each city's database,
v0/analysis_price.md (aggregates only) and v0/private/price_viz.json
(area aggregates and boundaries for the map page).
"""

import json
import math
import os
import urllib.parse

import duckdb
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

import config
from common import download

# PRICE_CITIES=nyc,dc runs a subset (for testing while another city's database is busy).
CITIES = tuple(os.environ.get("PRICE_CITIES", "nyc,dc,charlotte,sf,houston").split(","))
LABEL = {"nyc": "NYC", "dc": "DC", "charlotte": "Charlotte", "sf": "SF", "houston": "Houston"}
SF_SOLD_SINCE = "2015-01-01"
# Saiz (2010, QJE), Table VI: long-run housing supply elasticity of the metro area, with
# Table III's share of land undevelopable (water, wetlands, steep slopes) and the Wharton
# regulation index. Metro names as printed there.
SAIZ = {"sf": (0.66, 73.14, 0.72, "San Francisco, CA"), "nyc": (0.76, 40.42, 0.65, "New York, NY"),
        "dc": (1.61, 13.95, 0.31, "Washington, DC-MD-VA-WV"), "houston": (2.30, 8.40, -0.40, "Houston, TX"),
        "charlotte": (3.09, 4.69, -0.53, "Charlotte-Gastonia-Rock Hill, NC-SC")}
RADIUS_M = 1000
FALLBACK_M = 2000
MIN_LOTS = 10
COMMERCIAL = ("store or office building", "apartments or house with stores", "industrial, garage or loft")
NYC_CD = "https://data.cityofnewyork.us/resource/5crt-au7u.geojson"
DC_CLUSTERS = f"{config.DCGIS}/Administrative_Other_Boundaries_WebMercator/MapServer/17"
DC_OWNER = config.DC_OWNER_POLYGONS
DC_RETAIL_OFFICE = ["004", "041", "042", "043", "044", "045", "046", "047", "048", "049", "067", "068",
                    "006", "069", "005", "051", "052", "053", "056", "057", "058", "059", "061"]
CLT_CAMA = "https://meckgis.mecklenburgcountync.gov/server/rest/services/TaxParcel_Camaownershipvalues/FeatureServer/0"
CLT_AREAS = "https://services.arcgis.com/9Nl857LBlQVyzq54/arcgis/rest/services/Community_Planning_Areas/FeatureServer/0"
CENSUS_REPORTER = "https://api.censusreporter.org/1.0"
ZCTA_GROUPS = {"nyc": ["05000US36005", "05000US36047", "05000US36061", "05000US36081", "05000US36085"],
               "dc": ["04000US11"], "charlotte": ["05000US37119"], "sf": ["05000US06075"], "houston": ["05000US48201"]}
SF_NHOODS = "https://data.sf.gov/resource/j2bu-swwd.geojson?$limit=100"
HOU_SUPER = "https://services.arcgis.com/NummVBqZSIJKUeVR/arcgis/rest/services/COH_Super_Neighborhoods_view/FeatureServer/3"
CLT_OFFICE = ["OFFICE", "MEDICAL OFFICE", "BANK", "OFFICE HIGH RISE - > 6 STORIES", "LABORATORY / RESEARCH"]
CLT_RETAIL = ["COMMERCIAL", "RESTAURANT", "FAST FOOD", "AUTO SALES AND SERVICE", "CONVENIENCE STORE",
              "SHOPPING CENTER - STRIP", "CAR WASH", "SERVICE GARAGE", "SUPERMARKET", "SHOPPING CENTER - MALL",
              "DEPARTMENT STORE", "CONVIENCE/FAST FOOD STORE", "COMMERCIAL SERVICE(LAUNDRY,TV,RADIO,ETC)",
              "LUMBER YARD", "SERVICE STATION", "FURNITURE STORE", "LOUNGE, NIGHT CLUB, BAR"]
OUTCOMES = [("shares_space", "Sharing worship space"),
            ("sharing_property", "Sharing, same property"),
            ("multi_use", "Multi-use (2+ uses)"),
            ("commercial_units", "In a store, office or loft unit")]


def city_cfg(city):
    c = config.CITIES[city]
    root = config.ROOT / "data" / city
    return {"db": root / c["db_name"], "raw": root / "raw", "name": c["name"]}


def nyc_areas(raw):
    path = download(f"{NYC_CD}?$limit=200", raw / "nyc_community_districts.geojson")
    return f"""SELECT CAST(boro_cd AS INT)::VARCHAR AS area_id,
                      CASE left(CAST(boro_cd AS VARCHAR), 1) WHEN '1' THEN 'Manhattan' WHEN '2' THEN 'Bronx'
                           WHEN '3' THEN 'Brooklyn' WHEN '4' THEN 'Queens' ELSE 'Staten Island' END
                      || ' CD ' || CAST(CAST(boro_cd AS INT) % 100 AS VARCHAR) AS area_name,
                      CAST(boro_cd AS INT) % 100 > 20 AS non_residential, geom
               FROM ST_Read('{path}')"""


def dc_areas(raw):
    q = urllib.parse.urlencode({"where": "1=1", "outFields": "NAME,NBH_NAMES,TYPE", "outSR": 4326, "f": "geojson"})
    path = download(f"{DC_CLUSTERS}/query?{q}", raw / "dc_neighborhood_clusters.geojson")
    return f"""SELECT NAME AS area_id, NAME || ': ' || NBH_NAMES AS area_name,
                      TYPE <> 'Original' AS non_residential, geom
               FROM ST_Read('{path}')"""


def clt_areas(raw):
    q = urllib.parse.urlencode({"where": "1=1", "outFields": "Name", "outSR": 4326, "f": "geojson"})
    path = download(f"{CLT_AREAS}/query?{q}", raw / "charlotte_community_planning_areas.geojson")
    return f"""SELECT Name AS area_id, Name AS area_name, false AS non_residential, geom FROM ST_Read('{path}')"""


def load_zcta(con, city):
    """ZIP code areas (ZCTAs) with ACS 2020-2024 median household income, from Census Reporter."""
    zdir = config.ROOT / "data" / "zcta"
    parts, income = [], {}
    for g in ZCTA_GROUPS[city]:
        geo = download(f"{CENSUS_REPORTER}/geo/show/tiger2023?geo_ids=860|{g}", zdir / f"cr_{g}.geojson")
        inc = download(f"{CENSUS_REPORTER}/data/show/latest?table_ids=B19013,B01003&geo_ids=860|{g}", zdir / f"inc_{g}.json")
        parts.append(f"SELECT name AS zip, geom FROM ST_Read('{geo}')")
        for gid, v in json.loads(inc.read_text())["data"].items():
            income[gid[-5:]] = v["B19013"]["estimate"].get("B19013001")
    con.execute(f"CREATE OR REPLACE TEMP TABLE zcta AS SELECT zip, any_value(geom) AS geom FROM ({' UNION ALL '.join(parts)}) GROUP BY zip")
    con.register("zinc", pd.DataFrame({"zip": list(income), "zip_income": [income[z] for z in income]}))


def sf_areas(raw):
    path = download(SF_NHOODS, raw / "sf_analysis_neighborhoods.geojson")
    return f"""SELECT nhood AS area_id, nhood AS area_name, false AS non_residential, geom FROM ST_Read('{path}')"""


def houston_areas(raw):
    q = urllib.parse.urlencode({"where": "1=1", "outFields": "POLYID,SNBNAME", "outSR": 4326, "f": "geojson"})
    path = download(f"{HOU_SUPER}/query?{q}", raw / "houston_super_neighborhoods.geojson")
    return f"""SELECT CAST(POLYID AS VARCHAR) AS area_id, SNBNAME AS area_name, false AS non_residential, geom
               FROM ST_Read('{path}')"""


def arcgis_rows(layer, where, fields, dest):
    """All rows of an ArcGIS layer matching where, 2,000 per request, cached under dest."""
    parts, offset = [], 0
    while True:
        q = urllib.parse.urlencode({"where": where, "outFields": fields, "orderByFields": "OBJECTID",
                                    "resultOffset": offset, "resultRecordCount": 2000,
                                    "returnGeometry": "false", "f": "json"})
        p = download(f"{layer}/query?{q}", dest / f"part-{offset // 2000:04d}.json")
        page = json.loads(p.read_text())
        if "error" in page:  # don't keep a cached error as if it were an empty page
            p.unlink()
            raise RuntimeError(f"{layer}: {page['error']}")
        feats = page.get("features", [])
        parts += [f["attributes"] for f in feats]
        if len(feats) < 2000:
            return pd.DataFrame(parts)
        offset += 2000


def church_years(city, raw):
    """Year built of church buildings where the parcel records lack it: DC's commercial CAMA
    records with use code 081 (religious), and Charlotte's CAMA buildings typed CHURCH on
    parcels whose property use is CHURCH in the city."""
    if city == "dc":
        rows = arcgis_rows(f"{config.DCGIS}/Property_and_Land_WebMercator/MapServer/23", "USECODE = 81",
                           "OBJECTID,SSL,AYB", raw / "dc_church_years")
        return rows.groupby("SSL")["AYB"].min().tolist() if len(rows) else []
    if city == "charlotte":
        bld = arcgis_rows("https://meckgis.mecklenburgcountync.gov/server/rest/services/CamaDataTables/FeatureServer/1",
                          "buildingtype = 'CHURCH'", "objectid,propertyid,yearbuilt", raw / "clt_church_years")
        own = arcgis_rows(CLT_CAMA, "municipality_desc = 'CHARLOTTE' AND txt_propertyuse_desc = 'CHURCH'",
                          "OBJECTID,propertyid", raw / "clt_church_parcels")
        bld = bld[bld["propertyid"].isin(set(own["propertyid"]))]
        return bld.groupby("propertyid")["yearbuilt"].min().tolist() if len(bld) else []
    return []


def clt_land_values(raw):
    """Land value for Charlotte retail and office parcels (owner fields are not requested)."""
    uses = ",".join("'" + u.replace("'", "''") + "'" for u in CLT_OFFICE + CLT_RETAIL)
    return arcgis_rows(CLT_CAMA, f"municipality_desc = 'CHARLOTTE' AND txt_propertyuse_desc IN ({uses})",
                       "OBJECTID,pid,txt_propertyuse_desc,amt_landvalue", raw / "clt_commercial_values")


def dc_land_values(raw):
    """Land value and area for DC retail and office lots (one request per 2,000 lots)."""
    where = "USECODE IN (" + ",".join(f"'{u}'" for u in DC_RETAIL_OFFICE) + ")"
    parts, offset = [], 0
    while True:
        q = urllib.parse.urlencode({"where": where, "outFields": "OBJECTID,SSL,USECODE,LANDAREA,NEWLAND,NEWTOTAL",
                                    "orderByFields": "OBJECTID", "resultOffset": offset,
                                    "resultRecordCount": 2000, "returnGeometry": "false", "f": "json"})
        p = download(f"{DC_OWNER}/query?{q}", raw / "dc_commercial_values" / f"part-{offset // 2000:04d}.json")
        feats = json.loads(p.read_text()).get("features", [])
        parts += [f["attributes"] for f in feats]
        if len(feats) < 2000:
            return pd.DataFrame(parts)
        offset += 2000


def build_city(city):
    cfg = city_cfg(city)
    con = duckdb.connect(str(cfg["db"]))
    con.execute("LOAD spatial")
    areas_sql = {"nyc": nyc_areas, "dc": dc_areas, "charlotte": clt_areas,
                 "sf": sf_areas, "houston": houston_areas}[city](cfg["raw"])
    con.execute(f"CREATE OR REPLACE TEMP TABLE areas AS {areas_sql}")

    # Commercial lots: a point and a land price per square foot.
    if city == "nyc":
        con.execute("""CREATE OR REPLACE TABLE commercial_lots AS
            SELECT bbl, latitude AS lat, longitude AS lon, left(bldgclass, 1) AS kind,
                   assessland / 0.45 / lotarea AS land_psf
            FROM pluto
            WHERE left(bldgclass, 1) IN ('K', 'O') AND lotarea >= 200 AND assessland > 0
              AND latitude IS NOT NULL""")
    elif city in ("sf", "houston"):
        # Both loaders keep land value and lot area on pluto; SF keeps only recent sales
        # (Proposition 13), and lot area comes from the parcel polygon in both.
        recent = (f"AND NOT p.condo_lot AND p.last_sale >= DATE '{SF_SOLD_SINCE}'" if city == "sf" else "")
        con.execute(f"""CREATE OR REPLACE TABLE commercial_lots AS
            WITH lots AS (SELECT p.bbl, left(p.bldgclass, 1) AS kind, p.assessland,
                                 ST_Area(ST_Transform(t.geom, 'EPSG:4326', 'EPSG:3857', always_xy := true))
                                   * cos(radians(ST_Y(ST_Centroid(t.geom)))) ^ 2 * 10.7639 AS area_sqft,
                                 ST_Centroid(t.geom) AS pt
                          FROM pluto p JOIN taxlots t USING (bbl)
                          WHERE left(p.bldgclass, 1) IN ('K', 'O') AND p.assessland > 0 {recent})
            SELECT bbl, ST_Y(pt) AS lat, ST_X(pt) AS lon, kind, assessland / area_sqft AS land_psf
            FROM lots WHERE area_sqft >= 200""")
    elif city == "charlotte":
        vals = clt_land_values(cfg["raw"])
        con.register("vals", vals)
        office = ",".join(f"'{u}'" for u in CLT_OFFICE)
        con.execute(f"""CREATE OR REPLACE TABLE commercial_lots AS
            WITH lots AS (SELECT p.pid, any_value(p.bbl) AS bbl FROM pluto p GROUP BY 1),
                 polys AS (SELECT bbl, ST_Union_Agg(geom) AS g FROM taxlots GROUP BY 1)
            SELECT l.bbl, ST_Y(ST_Centroid(t.g)) AS lat, ST_X(ST_Centroid(t.g)) AS lon,
                   CASE WHEN v.txt_propertyuse_desc IN ({office}) THEN 'O' ELSE 'K' END AS kind,
                   v.amt_landvalue / ST_Area(ST_Transform(t.g, 'EPSG:4326', 'EPSG:2264', always_xy := true)) AS land_psf
            FROM vals v JOIN lots l ON l.pid = trim(v.pid) JOIN polys t ON t.bbl = l.bbl
            WHERE v.amt_landvalue > 0
              AND ST_Area(ST_Transform(t.g, 'EPSG:4326', 'EPSG:2264', always_xy := true)) >= 200""")
    else:
        vals = dc_land_values(cfg["raw"])
        con.register("vals", vals)
        con.execute("""CREATE OR REPLACE TABLE commercial_lots AS
            WITH lots AS (SELECT p.ssl, any_value(p.bbl) AS bbl FROM pluto p GROUP BY 1),
                 pts AS (SELECT bbl, ST_Centroid(ST_Union_Agg(geom)) AS pt FROM taxlots GROUP BY 1)
            SELECT l.bbl, ST_Y(t.pt) AS lat, ST_X(t.pt) AS lon,
                   CASE WHEN v.USECODE IN ('005','051','052','053','056','057','058','059','061') THEN 'O' ELSE 'K' END AS kind,
                   v.NEWLAND / v.LANDAREA AS land_psf
            FROM vals v JOIN lots l ON l.ssl = trim(v.SSL) JOIN pts t ON t.bbl = l.bbl
            WHERE v.LANDAREA >= 200 AND v.NEWLAND > 0""")
    # Congregation points (listing point) with area, local price and nearby congregations.
    g = "geometry" if "geometry" in [r[0] for r in con.execute("DESCRIBE places").fetchall()] else "geom"
    lat0 = con.execute(f"SELECT avg(ST_Y({g})) FROM places").fetchone()[0]
    kx, ky = 111320 * math.cos(math.radians(lat0)), 110540
    con.execute(f"""CREATE OR REPLACE TEMP TABLE cpts AS
        SELECT s.cong_id, ST_X(any_value(p.{g})) AS lon, ST_Y(any_value(p.{g})) AS lat
        FROM cong_sharing_raw s JOIN place_cong pc USING (cong_id) JOIN places p ON p.id = pc.id
        WHERE s.headline GROUP BY 1""")
    for t in ("cpts", "commercial_lots"):
        con.execute(f"""CREATE OR REPLACE TEMP TABLE {t}_xy AS
            SELECT *, lon * {kx} AS x, lat * {ky} AS y, floor(lon * {kx} / 1000)::INT AS cx, floor(lat * {ky} / 1000)::INT AS cy
            FROM {t}""")
    near = lambda tbl, r, extra="": f"""
        SELECT a.cong_id, median(b.land_psf) AS psf, count(*) AS n
        FROM cpts_xy a JOIN {tbl} b ON b.cx BETWEEN a.cx - {r // 1000} AND a.cx + {r // 1000}
                                 AND b.cy BETWEEN a.cy - {r // 1000} AND a.cy + {r // 1000}
        WHERE (a.x - b.x) ^ 2 + (a.y - b.y) ^ 2 <= {r} ^ 2 {extra} GROUP BY 1"""
    con.execute(f"""CREATE OR REPLACE TABLE cong_price AS
        WITH r1 AS ({near('commercial_lots_xy', RADIUS_M)}),
             r2 AS ({near('commercial_lots_xy', FALLBACK_M)}),
             cn AS (SELECT a.cong_id, count(*) - 1 AS cong_1km
                    FROM cpts_xy a JOIN cpts_xy b ON b.cx BETWEEN a.cx - 1 AND a.cx + 1 AND b.cy BETWEEN a.cy - 1 AND a.cy + 1
                    WHERE (a.x - b.x) ^ 2 + (a.y - b.y) ^ 2 <= {RADIUS_M} ^ 2 GROUP BY 1)
        SELECT c.cong_id, ar.area_id, ar.area_name,
               CASE WHEN coalesce(r1.n, 0) >= {MIN_LOTS} THEN r1.psf ELSE r2.psf END AS local_psf,
               CASE WHEN coalesce(r1.n, 0) >= {MIN_LOTS} THEN {RADIUS_M} WHEN r2.n >= {MIN_LOTS} THEN {FALLBACK_M} END AS radius_m,
               coalesce(r1.n, 0) AS lots_1km, coalesce(cn.cong_1km, 0) AS cong_1km
        FROM cpts c
        LEFT JOIN r1 USING (cong_id) LEFT JOIN r2 USING (cong_id) LEFT JOIN cn USING (cong_id)
        LEFT JOIN areas ar ON ST_Contains(ar.geom, ST_Point(c.lon, c.lat))""")
    con.execute("UPDATE cong_price SET local_psf = NULL WHERE radius_m IS NULL")

    load_zcta(con, city)
    con.execute("""CREATE OR REPLACE TEMP TABLE czip AS
        SELECT c.cong_id, (SELECT zip FROM zcta z WHERE ST_Contains(z.geom, ST_Point(c.lon, c.lat)) LIMIT 1) AS zip
        FROM cpts c""")
    # Building size: floor area where the parcel record has it (NYC, SF, Houston), else the
    # building footprint's area (DC, Charlotte), in square feet. Compared only within a city.
    has_fp = con.execute("SELECT count(*) FROM duckdb_tables() WHERE table_name = 'buildings'").fetchone()[0] > 0
    fp_join = ("""LEFT JOIN (SELECT 'ov:' || bid AS space_key,
                         ST_Area(ST_Transform(geom, 'EPSG:4326', 'EPSG:3857', always_xy := true))
                           * cos(radians(ST_Y(ST_Centroid(geom)))) ^ 2 * 10.7639 AS fp_sqft
                  FROM buildings) fp ON fp.space_key = s.space_key""" if has_fp else "")
    fp_col = "fp.fp_sqft" if has_fp else "NULL::DOUBLE"
    com = ", ".join(f"'{x}'" for x in COMMERCIAL)
    df = con.execute(f"""
        SELECT s.cong_id, '{city}' AS city, s.tradition, s.building_use,
               s.shares_space::INT AS shares_space,
               ((s.others_headline >= 1 AND NOT coalesce(s.multi_unit, false)) OR coalesce(s.site_says_shared, false))::INT AS sharing_property,
               (u.uses >= 2)::INT AS multi_use,
               (s.building_use IN ({com}))::INT AS commercial_units,
               (s.building_use LIKE 'religious building%') AS in_religious,
               p.area_id, p.area_name, p.local_psf, p.radius_m, p.cong_1km,
               b.bldgarea, b.yearbuilt, zi.zip_income,
               coalesce(CASE WHEN b.bldgarea > 0 THEN b.bldgarea END, {fp_col}) AS size_sqft
        FROM cong_sharing_raw s JOIN cong_price p USING (cong_id)
        LEFT JOIN cong_util_full u USING (cong_id)
        LEFT JOIN czip cz USING (cong_id) LEFT JOIN zinc zi ON zi.zip = cz.zip
        {fp_join}
        LEFT JOIN (SELECT bbl, any_value(bldgarea) AS bldgarea, any_value(yearbuilt) AS yearbuilt
                   FROM pluto GROUP BY bbl) b ON b.bbl = s.bbl
        WHERE s.headline""").df()
    lots = con.execute("SELECT count(*), median(land_psf), quantile_cont(land_psf, 0.25), quantile_cont(land_psf, 0.75) FROM commercial_lots").fetchone()
    # Area aggregates and boundaries for the map page.
    area_price = con.execute("""SELECT a.area_id, median(l.land_psf) AS area_psf, count(*) AS area_lots
        FROM areas a JOIN commercial_lots l ON ST_Contains(a.geom, ST_Point(l.lon, l.lat)) GROUP BY 1""").df()
    geo = con.execute("""SELECT area_id, area_name, non_residential,
                                ST_AsGeoJSON(ST_SimplifyPreserveTopology(geom, 0.0003)) AS gj FROM areas""").df()
    with_extraction = con.execute("SELECT count(*) FROM extract_sites").fetchone()[0] > 0
    # Church buildings' age: where land is easy to build on, congregations put up their own.
    built = con.execute("""SELECT count(*), count(*) FILTER (WHERE yearbuilt > 1700),
                                  median(yearbuilt) FILTER (WHERE yearbuilt > 1700),
                                  avg((yearbuilt >= 1980)::INT) FILTER (WHERE yearbuilt > 1700)
                           FROM pluto WHERE bldgclass = 'M1'""").fetchone()
    con.close()
    if built[1] < 0.5 * built[0]:
        yrs = [y for y in church_years(city, cfg["raw"]) if y and y > 1700]
        if yrs:
            built = (len(yrs), len(yrs), float(np.median(yrs)), float(np.mean([y >= 1980 for y in yrs])))
    return df, lots, area_price, geo, with_extraction, built


def wilson(k, n, z=1.96):
    p = k / n
    den = 1 + z * z / n
    c, h = (p + z * z / (2 * n)) / den, z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return 100 * (c - h), 100 * (c + h)


def fit(d, y, rhs):
    used = [v for v in ("lp", "ld", "la", "old", "linc", "lsize", "tradition") if v in rhs]
    d = d.dropna(subset=[y, "area_id", *used])
    d = d[np.isfinite(d[[v for v in used if v not in ("tradition",)]].astype(float)).all(axis=1)]
    m = smf.ols(f"{y} ~ {rhs}", data=d).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(d["city"] + d["area_id"])[0]})
    return 100 * m.params["lp"], 100 * m.bse["lp"], m.pvalues["lp"], int(m.nobs)


def md_table(rows, cols):
    out = ["| " + " | ".join(cols) + " |", "| " + " | ".join("---" for _ in cols) + " |"]
    out += ["| " + " | ".join(str(r[c]) for c in cols) + " |" for r in rows]
    return "\n".join(out) + "\n"


def main():
    frames, lots_info, viz, extracted, built = [], {}, {"areas": [], "geo": {"type": "FeatureCollection", "features": []}}, {}, {}
    for city in CITIES:
        df, lots, area_price, geo, extracted[city], built[city] = build_city(city)
        frames.append(df)
        lots_info[city] = lots
        # area measures
        a = df.dropna(subset=["area_id"]).groupby("area_id").agg(
            n=("cong_id", "size"), sharing=("shares_space", "mean"), sharing_property=("sharing_property", "mean"),
            multi_use=("multi_use", "mean"), commercial_units=("commercial_units", "mean"),
            k_sharing=("shares_space", "sum"), k_property=("sharing_property", "sum"),
            k_multi=("multi_use", "sum"), n_multi=("multi_use", "count"), k_commercial=("commercial_units", "sum"),
            local_psf=("local_psf", "median")).reset_index()
        a = geo[["area_id", "area_name", "non_residential"]].merge(a, on="area_id", how="left").merge(area_price, on="area_id", how="left")
        for _, r in a.iterrows():
            rec = {"city": city, **{k: (None if pd.isna(v) else v) for k, v in r.items()}}
            for k in ("sharing", "sharing_property", "multi_use", "commercial_units"):
                if rec.get(k) is not None:
                    rec[k] = round(100 * rec[k], 1)
            for k in ("area_psf", "local_psf"):
                if rec.get(k) is not None:
                    rec[k] = round(rec[k], 1)
            for k in ("n", "k_sharing", "k_property", "k_multi", "n_multi", "k_commercial", "area_lots"):
                if rec.get(k) is not None:
                    rec[k] = int(rec[k])
            rec["non_residential"] = bool(rec["non_residential"])
            viz["areas"].append(rec)
        for _, r in geo.iterrows():
            gj = json.loads(r["gj"])
            if gj["type"] not in ("Polygon", "MultiPolygon"):
                continue
            rnd = lambda x: [rnd(v) for v in x] if isinstance(x, list) else round(x, 4)
            gj["coordinates"] = rnd(gj["coordinates"])
            viz["geo"]["features"].append({"type": "Feature", "properties": {"city": city, "area_id": r["area_id"]}, "geometry": gj})

    d = pd.concat(frames, ignore_index=True)
    d["lp"] = np.log2(d["local_psf"])
    d["ld"] = np.log1p(d["cong_1km"])
    d["tradition"] = d["tradition"].fillna("Unknown")
    d["linc"] = np.log2(d["zip_income"].astype(float))
    d["lsize"] = np.log2(d["size_sqft"].astype(float).where(d["size_sqft"] > 0))
    has = d.dropna(subset=["lp"])

    # Pooled rates by local-price quintile within each city.
    quint = []
    for city in CITIES:
        c = has[has.city == city].copy()
        c["q"] = pd.qcut(c["local_psf"], 5, labels=False) + 1
        for q, g in c.groupby("q"):
            row = {"city": city, "q": int(q), "psf_min": round(g.local_psf.min()), "psf_max": round(g.local_psf.max()),
                   "psf_mid": round(g.local_psf.median(), 1), "n": len(g)}
            for y, _ in OUTCOMES:
                gg = g.dropna(subset=[y])
                k, n = int(gg[y].sum()), len(gg)
                lo, hi = wilson(k, n)
                row[y] = round(100 * k / n, 1)
                row[y + "_lo"], row[y + "_hi"] = round(lo, 1), round(hi, 1)
            quint.append(row)
    viz["quintiles"] = quint

    # Regressions.
    models = [("City only", "lp + C(city)"), ("+ tradition", "lp + C(city) + C(tradition)"),
              ("+ tradition, nearby congregations", "lp + C(city) + C(tradition) + ld")]
    reg = []
    for y, ylab in OUTCOMES:
        for sample, sub in (("All cities", has), *((LABEL[c], has[has.city == c]) for c in CITIES)):
            for mlab, rhs in models:
                rhs_s = rhs if sample == "All cities" else rhs.replace(" + C(city)", "")
                b, se, p, n = fit(sub, y, rhs_s)
                reg.append({"outcome": ylab, "sample": sample, "model": mlab, "b": round(b, 2), "se": round(se, 2),
                            "p": float(p), "n": n})
        if y == "shares_space":
            for sample, sub in (("All cities, religious buildings only", has[has.in_religious]),):
                for mlab, rhs in models:
                    b, se, p, n = fit(sub, y, rhs)
                    reg.append({"outcome": ylab, "sample": sample, "model": mlab, "b": round(b, 2), "se": round(se, 2),
                                "p": float(p), "n": n})
            # Bigger, older church buildings have room to host and stand in dearer places.
            # Only NYC's lot records carry floor area and year built.
            nyc = has[(has.city == "nyc") & has.in_religious & (has.bldgarea > 0)].copy()
            nyc["la"] = np.log2(nyc["bldgarea"].astype(float))
            nyc["old"] = ((nyc["yearbuilt"] > 0) & (nyc["yearbuilt"] < 1930)).astype(int)
            for mlab, rhs in (("+ tradition, nearby congregations", "lp + C(tradition) + ld"),
                              ("+ building floor area, built before 1930", "lp + C(tradition) + ld + la + old")):
                b, se, p, n = fit(nyc, y, rhs)
                reg.append({"outcome": ylab, "sample": "NYC, religious buildings only", "model": mlab,
                            "b": round(b, 2), "se": round(se, 2), "p": float(p), "n": n})
    viz["regression"] = reg

    # Robustness, city by city: does the price slope survive neighbourhood income (richer
    # congregations need guests less) and building size (big buildings have room to host)?
    base = "lp + C(tradition) + ld"
    checks = [("Price, tradition, nearby congregations", base, False),
              ("+ ZIP income", base + " + linc", False),
              ("+ building size", base + " + lsize", False),
              ("+ ZIP income and building size", base + " + linc + lsize", False),
              ("Religious buildings only, + income and size", base + " + linc + lsize", True)]
    robust = []
    for city in CITIES:
        c = has[has.city == city]
        row = {"city": city}
        for lab, rhs, rel in checks:
            b, se, p, n = fit(c[c.in_religious] if rel else c, "shares_space", rhs)
            row[lab] = {"b": round(b, 2), "se": round(se, 2), "p": float(p), "n": n}
        robust.append(row)
    viz["robust"] = robust
    viz["saiz"] = {c: {"elasticity": v[0], "undevelopable": v[1], "wri": v[2], "metro": v[3]} for c, v in SAIZ.items()}
    viz["lots"] = {c: {"n": int(v[0]), "median": round(v[1]), "p25": round(v[2]), "p75": round(v[3])} for c, v in lots_info.items()}

    # Report (aggregates only).
    basis = ("website gathering addresses where extraction found them, else the listing"
             if all(extracted.values()) else "the Overture listing address (website extraction was not run in this database)")
    w = []
    w.append("# Sharing and the local price of commercial space, five cities\n")
    w.append(f"Congregations placed at {basis}. Price: assessed market value of land per square foot for retail "
             f"and office lots, median within {RADIUS_M:,} m of each congregation ({FALLBACK_M:,} m where fewer than "
             f"{MIN_LOTS} lots lie within {RADIUS_M:,} m). NYC: PLUTO land assessment / 0.45; DC: OTR land value; Charlotte: county CAMA land value over parcel area; "
             f"SF: assessed land value of parcels sold since {SF_SOLD_SINCE[:4]} (Proposition 13); Houston: HCAD market land value. "
             "Assessed values are the assessor's estimate of market value, not observed rents.\n")
    w.append("## The price measure\n")
    rows = []
    for city in CITIES:
        li, c = viz["lots"][city], has[has.city == city]
        rows.append({"city": config.CITIES[city]["name"], "retail and office lots": f"{li['n']:,}",
                     "land $/sq ft, median (IQR)": f"${li['median']:,} (${li['p25']:,}–${li['p75']:,})",
                     "congregations priced": f"{len(c):,} of {len(d[d.city == city]):,}",
                     "using 2 km": f"{int((c.radius_m == FALLBACK_M).sum()):,}"})
    w.append(md_table(rows, list(rows[0])))
    w.append("\n## Pooled by local price quintile, within each city\n")
    w.append("Quintiles of congregations by the land price around them. 95% Wilson intervals treat congregations as "
             "independent, so they are somewhat too narrow.\n\n")
    qrows = [{"city": config.CITIES[r["city"]]["name"] if r["q"] == 1 else "", "quintile": r["q"],
              "land $/sq ft": f"${r['psf_min']:,}–${r['psf_max']:,}", "congregations": f"{r['n']:,}",
              **{lab: f"{r[y]}% ({r[y + '_lo']}–{r[y + '_hi']})" for y, lab in OUTCOMES}} for r in quint]
    w.append(md_table(qrows, list(qrows[0])))
    w.append("\n## Regression: percentage points per doubling of local land price\n")
    w.append("Linear probability models at the congregation level, standard errors clustered by community district "
             "(NYC), neighborhood cluster (DC), community planning area (Charlotte), analysis neighborhood (SF) or super neighborhood (Houston). Nearby congregations = log(1 + congregations within 1 km).\n\n")
    rrows = [{"outcome": r["outcome"], "sample": r["sample"], "model": r["model"],
              "pp per doubling (SE)": f"{r['b']:+.2f} ({r['se']:.2f})",
              "p": "<0.001" if r["p"] < 0.001 else f"{r['p']:.3f}", "n": f"{r['n']:,}"} for r in reg]
    w.append(md_table(rrows, list(rrows[0])))
    w.append("\n## Robustness: sharing worship space, by city\n")
    w.append("Percentage points per doubling of local land price (SE). ZIP income: ACS 2020-2024 median household "
             "income of the congregation's ZIP code. Building size: floor area from the parcel record (NYC, SF, "
             "Houston) or the building footprint's area (DC, Charlotte).\n\n")
    rob = []
    for r in robust:
        rob.append({"city": config.CITIES[r["city"]]["name"],
                    **{lab: f"{r[lab]['b']:+.1f} ({r[lab]['se']:.1f})" for lab, _, _ in checks}})
    w.append(md_table(rob, list(rob[0])))
    w.append("\n## Levels by city\n")
    w.append("Shares of congregations (listing placement). Church buildings are lots whose use code says church, "
             "synagogue or chapel; for DC and Charlotte, whose parcel records carry no year built, they are the "
             "assessor's commercial building records with a religious use (DC use code 081, Charlotte building "
             "type CHURCH), counted per parcel.\n\n")
    lv = []
    for city in sorted(CITIES, key=lambda c: SAIZ[c][0]):
        c = d[d.city == city]
        rel = c[c.in_religious]
        n_m1, n_yr, med_yr, new = built[city]
        has_yr = n_yr >= 0.5 * n_m1
        lv.append({"city": config.CITIES[city]["name"], "supply elasticity": SAIZ[city][0],
                   "congregations": f"{len(c):,}", "sharing worship space": f"{100 * c.shares_space.mean():.1f}%",
                   "in a religious building": f"{100 * c.in_religious.mean():.1f}%",
                   "sharing, of those in religious buildings": f"{100 * rel.shares_space.mean():.1f}%",
                   "in store, office or loft units": f"{100 * c.commercial_units.mean():.1f}%",
                   "church buildings": f"{n_m1:,}",
                   "median year built": f"{med_yr:.0f}" if has_yr else "n/a",
                   "built since 1980": f"{100 * new:.0f}%" if has_yr else "n/a"})
    w.append(md_table(lv, list(lv[0])))
    viz["levels"] = lv
    w.append("\n## Against how easily each metro can build\n")
    w.append("Saiz (2010, Quarterly Journal of Economics), Table VI: long-run housing supply elasticity (low = hard "
             "to build), with the share of land that is undevelopable and the Wharton regulation index from Table III.\n\n")
    el = []
    for city in sorted(CITIES, key=lambda c: SAIZ[c][0]):
        r = next(x for x in robust if x["city"] == city)["Price, tradition, nearby congregations"]
        el.append({"city": config.CITIES[city]["name"], "supply elasticity": SAIZ[city][0],
                   "undevelopable land": f"{SAIZ[city][1]:.0f}%", "regulation index": SAIZ[city][2],
                   "sharing, pts per doubling (SE)": f"{r['b']:+.1f} ({r['se']:.1f})", "p": "<0.001" if r["p"] < 0.001 else f"{r['p']:.3f}"})
    w.append(md_table(el, list(el[0])))
    w.append("\n## Caveats\n")
    w.append("- Assessed land values are model estimates; NYC's class 4 land values in particular are an allocation "
             "of an income-based total. They rank places by price well, less well as levels.\n"
             "- Sharing in NYC is likely understated where pairs are split across neighbouring lots (the near-miss check "
             "in the map page), and that happens more in dense, expensive areas.\n"
             "- Prices and congregation density rise together; the third model holds nearby congregations fixed.\n"
             "- Charlotte has only 15 planning areas to cluster on, so its own standard errors are rough.\n")
    out = config.ROOT / "v0" / "analysis_price.md"
    out.write_text("\n".join(w).replace("\n\n\n", "\n\n"))
    priv = config.ROOT / "v0" / "private"
    priv.mkdir(parents=True, exist_ok=True)
    (priv / "price_viz.json").write_text(json.dumps(viz, separators=(",", ":"), default=float))
    print(out.read_text())


if __name__ == "__main__":
    main()
