"""Occupancy and utilization of worship spaces, five cities.

A worship space is the building a congregation gathers in (space_key from the
sharing analysis); congregations that share worship space are one space, every
other congregation is a space of its own. For each space:

- occupancy: the number of congregations using it;
- utilization: weekly hours of worship held in it (each congregation's main and
  other weekly services times their posted or typical length, from
  analysis_services.py), and the share of the 168-hour week that is;
- intensity: weekly hours per 10,000 square feet of building (floor area from
  the parcel record in NYC, SF and Houston, footprint elsewhere).

Hours are known only where the congregation's own website gave a schedule, so
utilization uses spaces where every congregation using it has one. That is a
selected group (larger, web-present congregations); the report says how many.

The question: where space is dear, do buildings carry more congregations and
more hours? Within cities the price is the local retail and office land price
(analysis_price.py); across cities it is the value of commercial floor space,
which is roughly comparable between cities.

Run after analysis_price.py:  .venv/bin/python v0/analysis_utilization.py
Writes v0/analysis_utilization.md (aggregates) and v0/private/utilization_viz.json.
"""

import json
import os

import duckdb
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

import config

CITIES = tuple(os.environ.get("PRICE_CITIES", "nyc,dc,charlotte,sf,houston").split(","))
GROUP = {"sf": "hard", "nyc": "hard", "dc": "hard", "houston": "easy", "charlotte": "easy"}
ELASTICITY = {"sf": 0.66, "nyc": 0.76, "dc": 1.61, "houston": 2.30, "charlotte": 3.09}


def load(city):
    db = config.ROOT / "data" / city / config.CITIES[city]["db_name"]
    con = duckdb.connect(str(db), read_only=True)
    con.execute("LOAD spatial")
    has_fp = con.execute("SELECT count(*) FROM duckdb_tables() WHERE table_name = 'buildings'").fetchone()[0] > 0
    fp = ("""LEFT JOIN (SELECT 'ov:' || bid AS space_key,
                         ST_Area(ST_Transform(geom, 'EPSG:4326', 'EPSG:3857', always_xy := true))
                           * cos(radians(ST_Y(ST_Centroid(geom)))) ^ 2 * 10.7639 AS fp_sqft
                  FROM buildings) fp ON fp.space_key = u.space_key""" if has_fp else "")
    d = con.execute(f"""
        SELECT u.cong_id, u.space_key, u.shares_space, u.tradition, u.building_use, u.main_services,
               u.weekly_events, u.building_hours, u.has_schedule,
               p.local_psf, p.local_space_psf, p.area_id, p.area_name,
               coalesce(CASE WHEN b.bldgarea > 0 THEN b.bldgarea END, {"fp.fp_sqft" if has_fp else "NULL::DOUBLE"}) AS size_sqft
        FROM cong_util_full u
        JOIN cong_sharing_raw s USING (cong_id)
        LEFT JOIN cong_price p USING (cong_id)
        LEFT JOIN (SELECT bbl, any_value(bldgarea) AS bldgarea FROM pluto GROUP BY bbl) b ON b.bbl = s.bbl
        {fp}
        WHERE s.headline""").df()
    con.close()
    d["city"] = city
    return d


def spaces(d):
    """One row per worship space."""
    d = d.copy()
    d["space"] = np.where(d.shares_space.fillna(False), d.city + "|" + d.space_key.astype(str), d.city + "|c" + d.cong_id.astype(str))
    d["rel"] = d.building_use.fillna("").str.startswith("religious building")
    g = d.groupby("space")
    s = pd.DataFrame({
        "city": g.city.first(), "occupancy": g.size(), "all_sched": g.has_schedule.all(),
        "any_sched": g.has_schedule.any(),
        "hours": g.building_hours.sum(), "main": g.main_services.sum(), "events": g.weekly_events.sum(),
        "religious": g.rel.any(), "local_psf": g.local_psf.median(), "space_psf": g.local_space_psf.median(),
        "size_sqft": g.size_sqft.max(), "area_id": g.area_id.first(), "area_name": g.area_name.first(),
        "tradition": g.tradition.agg(lambda t: t.mode().iloc[0] if t.notna().any() else "Unknown"),
    }).reset_index()
    s["group"] = s.city.map(GROUP)
    s["shared"] = (s.occupancy >= 2).astype(int)
    s["week_pct"] = 100 * s.hours / 168
    s["intensity"] = np.where(s.size_sqft >= 1000, 1e4 * s.hours / s.size_sqft, np.nan)
    return s


def fit(df, y, rhs, cluster="area_id"):
    used = [c for c in ("lp", "ls", "lsize", "locc") if c in rhs]
    df = df.dropna(subset=[y, cluster, *used])
    df = df[np.isfinite(df[used].astype(float)).all(axis=1)] if used else df
    if len(df) < 30:
        return None
    m = smf.ols(f"{y} ~ {rhs}", data=df).fit(cov_type="cluster",
                                            cov_kwds={"groups": pd.factorize(df["city"] + df[cluster].astype(str))[0]})
    k = "lp" if "lp" in rhs else "ls"
    return {"b": float(m.params[k]), "se": float(m.bse[k]), "p": float(m.pvalues[k]), "n": int(m.nobs)}


def md(rows, cols):
    out = ["| " + " | ".join(cols) + " |", "| " + " | ".join("---" for _ in cols) + " |"]
    out += ["| " + " | ".join(str(r[c]) for c in cols) + " |" for r in rows]
    return "\n".join(out) + "\n"


def fmt(r, pct=False):
    if r is None:
        return "–"
    star = " *" if r["p"] < 0.05 else ""
    return f"{r['b']:+.{1 if pct else 2}f} ({r['se']:.{1 if pct else 2}f}){star}"


def main():
    raw = pd.concat([load(c) for c in CITIES], ignore_index=True)
    s = spaces(raw)
    s["lp"] = np.log2(s.local_psf)
    s["ls"] = np.log2(s.space_psf)
    s["lsize"] = np.log2(s.size_sqft.where(s.size_sqft >= 1000))
    s["lhours"] = np.log(s.hours.where(s.hours > 0))
    s["locc"] = np.log(s.occupancy)
    rel = s[s.religious]
    obs = rel[rel.all_sched & (rel.hours > 0)]
    order = sorted(CITIES, key=lambda c: ELASTICITY[c])
    name = lambda c: config.CITIES[c]["name"]

    w = ["# Occupancy and utilization of worship spaces\n",
         "A worship space is the building a congregation gathers in; congregations sharing worship space are one space. "
         "Occupancy is congregations per space; utilization is weekly hours of worship held there (from congregations' "
         "own posted schedules), counted only where every congregation in the space has a schedule. Religious "
         "buildings only, unless stated. Placement: website gathering address where extraction found one, else the listing.\n"]

    # 1. Levels by city
    rows = []
    for c in order:
        r, o = rel[rel.city == c], obs[obs.city == c]
        single, shared = o[o.occupancy == 1], o[o.occupancy >= 2]
        rows.append({"city": name(c), "supply elasticity": ELASTICITY[c], "religious worship spaces": f"{len(r):,}",
                     "with 2+ congregations": f"{100 * r.shared.mean():.1f}%",
                     "congregations per space": f"{r.occupancy.mean():.2f}",
                     "spaces with full schedules": f"{len(o):,} ({100 * len(o) / len(r):.0f}%)",
                     "weekly hours, median": f"{o.hours.median():.1f}",
                     "share of week in use": f"{o.week_pct.median():.1f}%",
                     "main services per week, mean": f"{o.main.mean():.2f}",
                     "hours: single-use / shared": f"{single.hours.median():.1f} / {shared.hours.median():.1f}"})
    w.append("## 1. Occupancy and utilization by city\n")
    w.append(md(rows, list(rows[0])))

    # 2. Occupancy and utilization against each other and against price, within cities
    w.append("\n## 2. Within each city: what goes with dearer land?\n")
    w.append("Each cell: change per doubling of the local retail and office land price, with the space's tradition held "
             "fixed (SE; * p < 0.05). Occupancy is in congregations per 100 spaces; hours are percent changes "
             "(log points x 100); services are per 100 spaces. Religious buildings.\n\n")
    rows = []
    for c in order:
        r, o = rel[rel.city == c].copy(), obs[obs.city == c].copy()
        r["occ100"] = 100 * (r.occupancy - 1)
        o["lh100"] = 100 * o.lhours
        o["main100"] = 100 * o.main
        single = o[o.occupancy == 1].copy()
        rows.append({"city": name(c),
                     "extra congregations per 100 spaces": fmt(fit(r, "occ100", "lp + C(tradition)"), True),
                     "weekly hours, % change": fmt(fit(o, "lh100", "lp + C(tradition)"), True),
                     "weekly hours, % change, holding size": fmt(fit(o, "lh100", "lp + C(tradition) + lsize"), True),
                     "single-use spaces: main services per 100": fmt(fit(single, "main100", "lp + C(tradition)"), True)})
    w.append(md(rows, list(rows[0])))

    # 3. Does sharing raise utilization?
    w.append("\n## 3. Do shared buildings get more use?\n")
    w.append("Weekly hours in a space against the number of congregations using it (log-log, tradition and city held "
             "fixed): an elasticity of 1 means hours rise in proportion to congregations.\n\n")
    o = obs.copy()
    rows = []
    for lab, sub in (("All five cities", o), ("Hard to build (SF, NYC, DC)", o[o.group == "hard"]),
                     ("Easy to build (Houston, Charlotte)", o[o.group == "easy"])):
        if sub.empty:
            continue
        m = smf.ols("lhours ~ locc + C(city) + C(tradition)", data=sub.dropna(subset=["lhours"])).fit(
            cov_type="cluster", cov_kwds={"groups": pd.factorize(sub.dropna(subset=["lhours"])["city"] + sub.dropna(subset=["lhours"])["area_id"].astype(str))[0]})
        rows.append({"sample": lab, "hours elasticity to congregations": f"{m.params['locc']:.2f} ({m.bse['locc']:.2f})",
                     "spaces": f"{int(m.nobs):,}", "shared spaces": f"{int((sub.occupancy >= 2).sum()):,}"})
    w.append(md(rows, list(rows[0])))

    # 4. Across cities, on the comparable floor-space price
    w.append("\n## 4. Across cities: the value of commercial floor space\n")
    w.append("Same outcomes against the floor-space price, with no city effects, so congregations in dear cities "
             "are compared with those in cheap ones (tradition held fixed).\n\n")
    rows = []
    r_all, o_all = rel.copy(), obs.copy()
    r_all["occ100"] = 100 * (r_all.occupancy - 1)
    o_all["lh100"] = 100 * o_all.lhours
    for lab, rr, oo in (("All five cities", r_all, o_all),
                        ("Hard to build", r_all[r_all.group == "hard"], o_all[o_all.group == "hard"]),
                        ("Easy to build", r_all[r_all.group == "easy"], o_all[o_all.group == "easy"])):
        rows.append({"sample": lab, "extra congregations per 100 spaces": fmt(fit(rr, "occ100", "ls + C(tradition)"), True),
                     "weekly hours, % change": fmt(fit(oo, "lh100", "ls + C(tradition)"), True),
                     "weekly hours, % change, holding size": fmt(fit(oo, "lh100", "ls + C(tradition) + lsize"), True)})
    w.append(md(rows, list(rows[0])))
    w.append("\n## Caveats\n")
    w.append("- Hours come from congregations' own websites and cover only spaces where every congregation posts a schedule; "
             "small and renting congregations post less, so utilization describes the better-documented spaces.\n"
             "- A schedule lists services, not other uses (meetings, schools, community programs), so hours understate how "
             "much a building is used.\n"
             "- Durations not posted are filled with typical lengths by tradition (analysis_services.py).\n")
    out = config.ROOT / "v0" / "analysis_utilization.md"
    out.write_text("\n".join(w))

    # Area-level points for the scatter page (aggregates only).
    pts = []
    for (c, aid), g in rel.groupby(["city", "area_id"]):
        if len(g) < 8:
            continue
        go = g[g.all_sched & (g.hours > 0)]
        pts.append({"city": c, "group": GROUP[c], "area": g.area_name.iloc[0], "spaces": int(len(g)),
                    "space_psf": round(float(g.space_psf.median()), 1) if g.space_psf.notna().any() else None,
                    "occupancy": round(float(g.occupancy.mean()), 3), "pct_shared": round(100 * float(g.shared.mean()), 1),
                    "hours": round(float(go.hours.median()), 2) if len(go) >= 3 else None, "n_hours": int(len(go))})
    viz = {"points": pts}
    (config.ROOT / "v0" / "private" / "utilization_viz.json").write_text(json.dumps(viz))
    print(out.read_text())


if __name__ == "__main__":
    main()
