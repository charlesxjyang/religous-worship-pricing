"""Do congregations share space more where commercial space is dear? (NYC and DC)

Price: assessed market value of land per square foot of lot, for retail and
office lots, the kind of space a congregation rents (NYC building classes K
and O; DC use codes that step 1 maps to K and O).

- NYC: PLUTO's assessed land value / 0.45 (retail and office lots are tax
  class 4, assessed at 45% of DOF market value), over lot area.
- DC: OTR's land value (NEWLAND, full market value) over land area, pulled
  here for commercial use codes only (step 1 kept total value only).

Each congregation gets the median over commercial lots within 1 km of its
listing point (2 km where fewer than 10 lie within 1 km). Areas for maps and
clustered errors: NYC community districts, DC neighborhood clusters.

The test is a linear probability model at the congregation level: outcome
(sharing worship space, sharing the property, multi-use, meeting in a store or
office unit) on log2 local price, with city fixed effects, then adding
tradition and the number of congregations within 1 km. Standard errors are
clustered by area. Coefficients read as percentage points per doubling of
the local land price.

Placement is the listing address (cong_sharing_raw), so in a session without
website extraction this runs on listings only; the report says which.

Run after step 5 and analysis_sharing.py / analysis_services.py for both cities:
    .venv/bin/python v0/analysis_price.py
Writes tables commercial_lots and cong_price in each city's database,
v0/analysis_price.md (aggregates only) and v0/private/price_viz.json
(area aggregates and boundaries for the map page).
"""

import json
import math
import urllib.parse

import duckdb
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

import config
from common import download

CITIES = ("nyc", "dc")
RADIUS_M = 1000
FALLBACK_M = 2000
MIN_LOTS = 10
COMMERCIAL = ("store or office building", "apartments or house with stores", "industrial, garage or loft")
NYC_CD = "https://data.cityofnewyork.us/resource/5crt-au7u.geojson"
DC_CLUSTERS = f"{config.DCGIS}/Administrative_Other_Boundaries_WebMercator/MapServer/17"
DC_OWNER = config.DC_OWNER_POLYGONS
DC_RETAIL_OFFICE = ["004", "041", "042", "043", "044", "045", "046", "047", "048", "049", "067", "068",
                    "006", "069", "005", "051", "052", "053", "056", "057", "058", "059", "061"]
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
    areas_sql = nyc_areas(cfg["raw"]) if city == "nyc" else dc_areas(cfg["raw"])
    con.execute(f"CREATE OR REPLACE TEMP TABLE areas AS {areas_sql}")

    # Commercial lots: a point and a land price per square foot.
    if city == "nyc":
        con.execute("""CREATE OR REPLACE TABLE commercial_lots AS
            SELECT bbl, latitude AS lat, longitude AS lon, left(bldgclass, 1) AS kind,
                   assessland / 0.45 / lotarea AS land_psf
            FROM pluto
            WHERE left(bldgclass, 1) IN ('K', 'O') AND lotarea >= 200 AND assessland > 0
              AND latitude IS NOT NULL""")
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

    com = ", ".join(f"'{x}'" for x in COMMERCIAL)
    df = con.execute(f"""
        SELECT s.cong_id, '{city}' AS city, s.tradition, s.building_use,
               s.shares_space::INT AS shares_space,
               ((s.others_headline >= 1 AND NOT coalesce(s.multi_unit, false)) OR coalesce(s.site_says_shared, false))::INT AS sharing_property,
               (u.uses >= 2)::INT AS multi_use,
               (s.building_use IN ({com}))::INT AS commercial_units,
               (s.building_use LIKE 'religious building%') AS in_religious,
               p.area_id, p.area_name, p.local_psf, p.radius_m, p.cong_1km,
               b.bldgarea, b.yearbuilt
        FROM cong_sharing_raw s JOIN cong_price p USING (cong_id)
        LEFT JOIN cong_util_full u USING (cong_id)
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
    con.close()
    return df, lots, area_price, geo, with_extraction


def wilson(k, n, z=1.96):
    p = k / n
    den = 1 + z * z / n
    c, h = (p + z * z / (2 * n)) / den, z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return 100 * (c - h), 100 * (c + h)


def fit(d, y, rhs):
    d = d.dropna(subset=[y, "lp", "area_id"])
    m = smf.ols(f"{y} ~ {rhs}", data=d).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(d["city"] + d["area_id"])[0]})
    return 100 * m.params["lp"], 100 * m.bse["lp"], m.pvalues["lp"], int(m.nobs)


def md_table(rows, cols):
    out = ["| " + " | ".join(cols) + " |", "| " + " | ".join("---" for _ in cols) + " |"]
    out += ["| " + " | ".join(str(r[c]) for c in cols) + " |" for r in rows]
    return "\n".join(out) + "\n"


def main():
    frames, lots_info, viz, extracted = [], {}, {"areas": [], "geo": {"type": "FeatureCollection", "features": []}}, {}
    for city in CITIES:
        df, lots, area_price, geo, extracted[city] = build_city(city)
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
        for sample, sub in (("Both cities", has), ("NYC", has[has.city == "nyc"]), ("DC", has[has.city == "dc"])):
            for mlab, rhs in models:
                rhs_s = rhs if sample == "Both cities" else rhs.replace(" + C(city)", "")
                b, se, p, n = fit(sub, y, rhs_s)
                reg.append({"outcome": ylab, "sample": sample, "model": mlab, "b": round(b, 2), "se": round(se, 2),
                            "p": float(p), "n": n})
        if y == "shares_space":
            for sample, sub in (("Both cities, religious buildings only", has[has.in_religious]),):
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
    viz["lots"] = {c: {"n": int(v[0]), "median": round(v[1]), "p25": round(v[2]), "p75": round(v[3])} for c, v in lots_info.items()}

    # Report (aggregates only).
    basis = ("website gathering addresses where extraction found them, else the listing"
             if all(extracted.values()) else "the Overture listing address (website extraction was not run in this database)")
    w = []
    w.append("# Sharing and the local price of commercial space, NYC and DC\n")
    w.append(f"Congregations placed at {basis}. Price: assessed market value of land per square foot for retail "
             f"and office lots, median within {RADIUS_M:,} m of each congregation ({FALLBACK_M:,} m where fewer than "
             f"{MIN_LOTS} lots lie within {RADIUS_M:,} m). NYC: PLUTO land assessment / 0.45; DC: OTR land value. "
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
             "(NYC) or neighborhood cluster (DC). Nearby congregations = log(1 + congregations within 1 km).\n\n")
    rrows = [{"outcome": r["outcome"], "sample": r["sample"], "model": r["model"],
              "pp per doubling (SE)": f"{r['b']:+.2f} ({r['se']:.2f})",
              "p": "<0.001" if r["p"] < 0.001 else f"{r['p']:.3f}", "n": f"{r['n']:,}"} for r in reg]
    w.append(md_table(rrows, list(rrows[0])))
    w.append("\n## Caveats\n")
    w.append("- Assessed land values are model estimates; NYC's class 4 land values in particular are an allocation "
             "of an income-based total. They rank places by price well, less well as levels.\n"
             "- Sharing in NYC is likely understated where pairs are split across neighbouring lots (the near-miss check "
             "in the map page), and that happens more in dense, expensive areas.\n"
             "- Prices and congregation density rise together; the third model holds nearby congregations fixed.\n"
             "- Charlotte is not included: its parcel pull has no value fields yet.\n")
    out = config.ROOT / "v0" / "analysis_price.md"
    out.write_text("\n".join(w).replace("\n\n\n", "\n\n"))
    priv = config.ROOT / "v0" / "private"
    priv.mkdir(parents=True, exist_ok=True)
    (priv / "price_viz.json").write_text(json.dumps(viz, separators=(",", ":"), default=float))
    print(out.read_text())


if __name__ == "__main__":
    main()
