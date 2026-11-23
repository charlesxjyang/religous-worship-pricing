"""First-pass analysis (NYC): congregations that share space.

Two questions, per congregation:
  1. Does it share its building with other congregations?
  2. Is its building also used for something other than worship?

Unit: a congregation at a tax lot, after the step 5 merges (website, phone,
name, IRS EIN). The lot is the gathering lot from step 5: the website's
address where extraction found one, else the Overture listing lot.

Population (headline): Overture listings in the worship categories with
confidence >= 0.5, not permanently closed, plus "religious_organization"
listings matched to an IRS-registered congregation. Sensitivity rows widen it.

Writes v0/analysis_sharing.md (aggregates, committed) and
v0/private/nyc_congregation_sites.csv (one row per congregation, not committed).

Run after step 5:  .venv/bin/python v0/analysis_sharing.py
"""

import datetime as dt

import checks
import config
from common import connect
from step1_load import md_table

OUT = config.REPORT_DIR / "analysis_sharing.md"
CSV = config.PRIVATE_DIR / f"{config.CITY}_congregation_sites.csv"

USE_GROUP = """
    CASE
      WHEN f.bldgclass IS NULL OR left(f.bldgclass, 1) = 'V' THEN 'vacant or no lot record'
      WHEN left(f.bldgclass, 1) = 'M' AND f.n_schools > 0 THEN 'religious building with a school on the lot'
      WHEN left(f.bldgclass, 1) = 'M' THEN 'religious building only'
      WHEN left(f.bldgclass, 1) = 'W' OR f.n_schools > 0 THEN 'school building'
      WHEN left(f.bldgclass, 1) IN ('K', 'O') THEN 'store or office building'
      WHEN left(f.bldgclass, 1) = 'S' OR f.bldgclass IN ('C7', 'D7') THEN 'apartments or house with stores'
      WHEN left(f.bldgclass, 1) IN ('A', 'B', 'C', 'D', 'R') THEN 'residential'
      WHEN left(f.bldgclass, 1) IN ('E', 'F', 'G', 'L', 'T', 'U') THEN 'industrial, garage or loft'
      ELSE 'other institution or hall' END
"""


def build(con):
    con.execute(f"""
        CREATE OR REPLACE TABLE cong_sites AS
        WITH listing AS (
          SELECT g.*, c.cong_id, i.irs_kind, i.basis AS irs_basis
          FROM place_gathering g
          JOIN place_cong c USING (id)            -- already excludes closed and non-congregations
          LEFT JOIN place_irs i USING (id)
        ), cong AS (
          SELECT cong_id,
                 any_value(gathering_bbl) AS bbl,
                 any_value(gathering_bin) AS bin,
                 any_value(listing_lot_method) AS lot_method,
                 any_value(boroname) AS borough,
                 -- a known tradition beats Unknown; ties go to the most confident listing
                 first(tradition ORDER BY tradition IN ('Unknown', 'Other'), confidence DESC, id) AS tradition,
                 count(*) AS listings,
                 string_agg(DISTINCT name, ' | ') AS names,
                 max(confidence) AS confidence,
                 bool_or(basic_category <> 'religious_organization') AS worship_category,
                 bool_or(irs_kind = 'congregation') AS irs_congregation,
                 bool_or(irs_kind = 'congregation' AND irs_basis = 'lot') AS irs_on_same_lot,
                 bool_or(address_basis = 'website') AS from_website
          FROM listing GROUP BY cong_id
        )
        SELECT c.*,
               (c.worship_category OR c.irs_congregation) AND c.confidence >= 0.5 AS headline,
               f.bldgclass, f.landuse_label, f.religious_owned, f.n_schools,
               p.numbldgs, {USE_GROUP} AS building_use
        FROM cong c
        LEFT JOIN lot_flags f ON f.bbl = c.bbl
        LEFT JOIN (SELECT bbl, any_value(numbldgs) AS numbldgs FROM pluto GROUP BY 1) p ON p.bbl = c.bbl
    """)
    # Other congregations on the same lot, within each population variant.
    con.execute("""
        CREATE OR REPLACE TABLE cong_sharing_raw AS
        WITH irs_lot AS (
          SELECT bbl, count(DISTINCT ein) AS irs_congs FROM irs_orgs
          WHERE kind = 'congregation' AND bbl IS NOT NULL GROUP BY 1
        ), irs_bin AS (
          SELECT bin, count(DISTINCT ein) AS irs_congs_bin FROM irs_orgs
          WHERE kind = 'congregation' AND bin IS NOT NULL AND bin NOT LIKE '%000000' GROUP BY 1
        )
        SELECT s.*,
               count(*) FILTER (WHERE s.headline) OVER (PARTITION BY s.bbl) - (s.headline::INT) AS others_headline,
               count(*) OVER (PARTITION BY s.bbl) - 1 AS others_all,
               CASE WHEN s.bin IS NOT NULL AND s.bin NOT LIKE '%000000'   -- x000000 = no real building
                    THEN count(*) FILTER (WHERE s.headline) OVER (PARTITION BY s.bin) - (s.headline::INT)
               END AS others_same_building,
               coalesce(il.irs_congs, 0) AS irs_congregations_on_lot,
               coalesce(ib.irs_congs_bin, 0) AS irs_congregations_in_building,
               s.building_use <> 'religious building only' AS other_use
        FROM cong_sites s LEFT JOIN irs_lot il USING (bbl) LEFT JOIN irs_bin ib USING (bin)
    """)
    # Check homes (mailing address?) and schools (the congregation's own?).
    checks.home_checks(con)
    checks.school_checks(con)
    con.execute("""
        CREATE OR REPLACE TABLE cong_sharing AS
        WITH r AS (
          SELECT s.* EXCLUDE (building_use, other_use), s.building_use AS building_use_raw,
                 h.home_check, h.home_evidence, k.school_check, k.schools_on_lot,
                 CASE
                   WHEN s.building_use IN ('residential', 'apartments or house with stores')
                        AND h.home_check = 'suggests mailing' THEN 'location unknown (home looks like a mailing address)'
                   WHEN s.building_use = 'religious building with a school on the lot' AND k.school_check = 'own school'
                     THEN 'religious building only'
                   WHEN s.building_use = 'religious building with a school on the lot'
                     THEN 'religious building hosting another school'
                   WHEN s.building_use = 'school building' AND k.school_check = 'own school'
                     THEN 'its own school (religious complex)'
                   WHEN s.building_use = 'school building' AND k.school_check = 'public school'
                     THEN 'public or charter school building'
                   WHEN s.building_use = 'school building' AND k.school_check = 'independent school'
                     THEN 'independent private school building'
                   WHEN s.building_use = 'school building' AND k.school_check = 'college'
                     THEN 'college or university building'
                   WHEN s.building_use = 'school building' THEN 'school building, owner unrelated'
                   ELSE s.building_use END AS building_use
          FROM cong_sharing_raw s
          LEFT JOIN home_checks h USING (cong_id)
          LEFT JOIN school_checks k USING (cong_id)
        )
        SELECT *, building_use NOT IN ('religious building only', 'its own school (religious complex)',
                                       'location unknown (home looks like a mailing address)') AS other_use,
               building_use LIKE 'location unknown%' AS location_unknown
        FROM r
    """)


def analysis(con) -> str:
    q = lambda sql: con.execute(sql).df()  # noqa: E731
    one = lambda sql: con.execute(sql).fetchone()  # noqa: E731
    out = []
    w = out.append
    n, n_web = one("SELECT count(*), count(*) FILTER (WHERE from_website) FROM cong_sharing WHERE headline")

    w(f"# Shared and multi-use worship space in {config.CITY_SHORT}: first pass\n")
    w(f"Run {dt.date.today().isoformat()}. {n:,} congregations (after merging duplicate "
      "listings), each placed on the tax lot where it gathers. "
      + (f"For {n_web:,} the lot comes from the congregation's own website; for the rest it is "
         "the Overture listing." if n_web else
         "Website extraction has not run yet, so every lot here is the Overture listing's, "
         "which is usually but not always where people gather.")
      + " The unit is the tax lot (BBL); the same-building (BIN) rows below are the stricter "
      "test.\n")

    # ---- 1. shared with other congregations
    s = one("""
        SELECT count(*) FILTER (WHERE others_headline >= 1),
               count(*) FILTER (WHERE others_headline >= 1 AND irs_congregations_on_lot >= 2),
               count(*) FILTER (WHERE others_same_building >= 1),
               count(*) FILTER (WHERE others_same_building >= 1 AND irs_congregations_in_building >= 2),
               count(*) FILTER (WHERE others_same_building IS NOT NULL)
        FROM cong_sharing WHERE headline""")
    pct = lambda x: f"{100 * x / n:.1f}%"  # noqa: E731
    w("## 1. Congregations sharing a building with other congregations\n")
    rows = [("Same tax lot as at least one other congregation", s[0]),
            ("... and the IRS shows 2+ congregations registered on the lot", s[1])]
    if s[4]:  # building IDs exist (NYC's BIN); DC's records have none
        rows += [("Same building (BIN) as at least one other congregation", s[2]),
                 ("... and the IRS shows 2+ registered in the building", s[3])]
    import pandas as pd
    w(md_table(pd.DataFrame([(t, c, pct(c)) for t, c in rows], columns=["test", "congregations", "share"])))
    bin_note = (f"Building IDs (BIN) come from geocoding the listing's street address; {s[4]:,} of "
                f"{n:,} congregations have one, so the building rows are a floor. " if s[4] else
                "This city's parcel records carry no building IDs, so only the lot test is "
                "available; a lot can hold more than one building. ")
    w("\n" + bin_note + "The lot row is an upper bound: a congregation listed twice under "
      "unrelated names still looks like two. The IRS-corroborated rows are closer to lower "
      "bounds, since many congregations are registered at another address or not at all. "
      "Lots with 2+ congregations, by how many share:\n")
    w(md_table(q("""
        SELECT CASE WHEN others_headline + 1 >= 5 THEN '5 or more' ELSE (others_headline + 1)::VARCHAR END
                 AS congregations_on_lot,
               count(DISTINCT bbl) AS lots, count(*) AS congregations
        FROM cong_sharing WHERE headline AND others_headline >= 1 GROUP BY 1 ORDER BY 1
    """)))

    # ---- 2. building also used for other purposes
    w("\n## 2. Congregations in a building also used for something else\n")
    o = one("""SELECT count(*) FILTER (WHERE other_use), count(*) FILTER (WHERE other_use AND irs_on_same_lot),
                      count(*) FILTER (WHERE location_unknown),
                      count(*) FILTER (WHERE other_use AND home_check = 'unconfirmed')
               FROM cong_sharing WHERE headline""")
    w(f"{o[0]:,} congregations ({pct(o[0])}) gather on a lot whose building is not a "
      f"religious building or its own school. For {o[1]:,} of them the IRS registration is "
      f"on the same lot, which corroborates that the congregation is based there. "
      f"{o[3]:,} of the {o[0]:,} are homes with no evidence either way (see the check "
      f"below). {o[2]:,} more are set aside as location unknown, because their home address "
      "looks like a mailing address. By building type (DOF building class, NCES schools on "
      "the lot, and the checks below):\n")
    w(md_table(q(f"""
        SELECT building_use, count(*) AS congregations,
               round(100 * count(*) / {n}, 1) AS pct,
               count(*) FILTER (WHERE others_headline >= 1) AS also_shared_with_other_congregations,
               count(*) FILTER (WHERE irs_on_same_lot) AS irs_registered_on_lot
        FROM cong_sharing WHERE headline GROUP BY 1 ORDER BY 2 DESC
    """)))

    w("\n### Checking homes: gathering place or mailing address?\n")
    w("Congregations on residential lots (houses, apartment buildings, and apartments over "
      "stores). Evidence from OpenStreetMap, the listing address, the IRS registration and "
      "the crawled website text; strongest first. \"Suggests mailing\" cases are moved to "
      "\"location unknown\" above.\n")
    w(md_table(q("""
        SELECT h.home_check, h.home_evidence, count(*) AS congregations,
               count(*) FILTER (WHERE s.building_use_raw = 'residential') AS residential,
               count(*) FILTER (WHERE s.building_use_raw = 'apartments or house with stores') AS with_stores
        FROM home_checks h JOIN cong_sharing s USING (cong_id)
        WHERE s.headline GROUP BY 1, 2 ORDER BY 1 DESC, 3 DESC
    """)))
    w("\n### Checking schools: the congregation's own, or another body's?\n")
    w("Congregations on a lot holding an NCES school, or in a school-class building. Own "
      "school: the school carries the congregation's name; or a Catholic parish with a "
      "Catholic-named school on Catholic-owned land; or, for a school building with no NCES "
      "record, the congregation owns it or it is a parochial school (class W2) on religious "
      "land. Public, charter and independent schools (independent religious schools "
      "included) count as other use; own schools do not.\n")
    w(md_table(q("""
        SELECT k.school_check, s.building_use_raw AS lot_building, count(*) AS congregations
        FROM school_checks k JOIN cong_sharing s USING (cong_id)
        WHERE s.headline GROUP BY 1, 2 ORDER BY 1, 3 DESC
    """)))

    # ---- both
    w("\n## Both questions together\n")
    w(md_table(q(f"""
        SELECT CASE WHEN other_use THEN 'other-use building' ELSE 'religious building only' END AS building,
               count(*) FILTER (WHERE others_headline = 0) AS alone_on_lot,
               count(*) FILTER (WHERE others_headline >= 1) AS with_other_congregations,
               count(*) AS total
        FROM cong_sharing WHERE headline GROUP BY 1 ORDER BY 1 DESC
    """)))
    w("\nThe plan's price signal sits in the three cells other than \"religious building only, "
      "alone\": congregations that economize on space by sharing a sanctuary, renting a "
      "storefront or school, or meeting in a home.\n")

    # ---- by tradition and borough
    w("## By tradition\n")
    w(md_table(q("""
        SELECT tradition, count(*) AS congregations,
               round(100 * avg((others_headline >= 1)::INT), 0) AS pct_sharing,
               round(100 * avg(other_use::INT), 0) AS pct_other_use_building,
               round(100 * avg((others_headline >= 1 OR other_use)::INT), 0) AS pct_either
        FROM cong_sharing WHERE headline GROUP BY 1 HAVING count(*) >= 15 ORDER BY 2 DESC
    """)))
    w("\nTradition comes from the congregation's own website where extraction read one, else "
      "from the Overture category; \"Unknown\" is mostly Overture's generic categories with no "
      "usable website.\n")
    w(f"## By {config.AREA_LABEL}\n")
    w(md_table(q(f"""
        SELECT borough AS {config.AREA_LABEL}, count(*) AS congregations,
               round(100 * avg((others_headline >= 1)::INT), 0) AS pct_sharing,
               round(100 * avg(other_use::INT), 0) AS pct_other_use_building,
               round(100 * avg((others_headline >= 1 OR other_use)::INT), 0) AS pct_either
        FROM cong_sharing WHERE headline GROUP BY 1 ORDER BY 1
    """)))

    # ---- sensitivity
    w("\n## How the population changes the answer\n")
    w(md_table(q("""
        WITH v AS (
          SELECT 'Headline (worship categories, confidence 0.5+)' AS population, *,
                 others_headline AS others FROM cong_sharing WHERE headline
          UNION ALL
          SELECT 'All listings, any category or confidence', *, others_all FROM cong_sharing
          UNION ALL
          SELECT 'Headline, IRS-registered congregations only', *, others_headline
          FROM cong_sharing WHERE headline AND irs_congregation
        )
        SELECT population, count(*) AS congregations,
               round(100 * avg((others >= 1)::INT), 1) AS pct_sharing,
               round(100 * avg(other_use::INT), 1) AS pct_other_use_building
        FROM v GROUP BY 1 ORDER BY 2 DESC
    """)))

    w("\n## Caveats\n")
    w("- Duplicate listings under unrelated names inflate sharing. Merges use website, phone, "
      "a conservative name match and IRS EIN; the IRS-corroborated row is the safer number.")
    w("- A lot can hold several buildings (a church and its school or rectory). The "
      "same-building (BIN) rows remove those, but only for congregations whose address geocoded.")
    w("- Each listing sits on the lot of its geocoded street address where that agrees with "
      "its map point to within 150 m, else on the point's lot. Listing addresses are what "
      "Overture's sources publish and can be a mailing address; website extraction replaces "
      "them with the address where services are held.")
    w("- Building class describes the main building. A church building whose basement hosts "
      "a day care, or a store building with a church upstairs, is classed by its main use.")
    n_irs_only = one("SELECT count(*) FROM irs_only")[0]
    w(f"- Places with no listing are missing. The IRS file holds {n_irs_only:,} registered "
      "congregations that no listing matched, many on commercial lots or in other bodies' "
      "buildings, so the true shares of sharing and other-use space are likely higher.")
    return "\n".join(out) + "\n"


def main():
    config.PRIVATE_DIR.mkdir(parents=True, exist_ok=True)
    con = connect(config.DB_PATH)
    build(con)
    OUT.write_text(analysis(con))
    con.execute(f"COPY (SELECT * FROM cong_sharing ORDER BY borough, bbl) TO '{CSV}' (HEADER)")
    print(OUT.read_text())


if __name__ == "__main__":
    main()
