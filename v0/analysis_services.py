"""Services and building utilization (Charles, 2026-11-24).

Question: even in single-use religious buildings, do congregations use their
space more intensively by holding more services? Where space is dear, the
plan expects more services per building.

From the website extraction (step 4b), per congregation, weekly services only:
  main services      gatherings most members attend (per-tradition rules in
                     the extraction prompt: weekend Masses incl. the Saturday
                     vigil, Sunday or Sabbath services, Shabbat services,
                     each Jumu'ah session, ...)
  same-day repeats   the most main services held on any one day
  languages          distinct languages among main services
  building-hours     hours of weekly worship of every type (main, weekday,
                     daily prayer); a service with no posted end time gets a
                     default duration by tradition (DEFAULT_MIN, placeholders
                     until the plan's Pope (2024) durations are wired in)

Buildings are grouped as in analysis_sharing.py (same tax lot):
  single-use religious  religious building, no other congregation on the lot
  shared religious      religious building with other congregations
  other-use building    store, office, home, school, hall, industrial ...
Compare within a tradition only: daily prayer cycles and Mass schedules make
raw totals incomparable across traditions.

Run after analysis_sharing.py (it reads cong_sharing):
    CITY=nyc .venv/bin/python v0/analysis_services.py
Writes <report dir>/analysis_services.md (aggregates only).
"""

import datetime as dt

import pandas as pd

import config
from common import connect
from step1_load import md_table

OUT = config.REPORT_DIR / "analysis_services.md"
MIN_N = 15  # suppress cells with fewer congregations

# Minutes, used only when a website gives no end time.
DEFAULT_MIN = {
    ("Catholic", "main_worship"): 60, ("Orthodox Christian", "main_worship"): 120,
    ("Protestant and other Christian", "main_worship"): 105, ("Jewish", "main_worship"): 120,
    ("Muslim", "main_worship"): 45, ("Hindu", "main_worship"): 90, ("Buddhist", "main_worship"): 90,
    ("Sikh", "main_worship"): 120,
}
DEFAULT_BY_TYPE = {"main_worship": 90, "weekday_worship": 45, "daily_prayer": 20, "other": 60}

GROUP = """
    CASE WHEN s.location_unknown THEN NULL
         WHEN s.other_use THEN 'other-use building'
         WHEN s.shares_space THEN 'shared religious building'
         ELSE 'single-use religious building' END
"""


# Multi-use count (Charles, 2026-11-24): how many distinct bodies use the same
# worship space. 1 for the congregation, +1 for each other congregation sharing
# its worship space (analysis_sharing.shares_space: same building, not a
# building split into units, or the website says so), +1 for a school that is
# not its own (public, charter, independent, college), +1 for a rented hall
# (community center, hotel, theater...). A church alone = 1; with a nesting
# congregation, or a charter school in its building, or meeting in a public
# school = 2. Congregations in separate units of a strip mall, office, flex or
# apartment building are separate places, each 1. Homes that look like a
# mailing address (location unknown) get no count.
OTHER_SCHOOL = ("public school", "independent school", "unrelated school building", "college")
USES = f"""
    CASE WHEN s.location_unknown THEN NULL ELSE
         1
         + CASE WHEN s.shares_space THEN greatest(s.others_space, 1) ELSE 0 END
         + CASE WHEN s.school_check IN ({', '.join(f"'{x}'" for x in OTHER_SCHOOL)}) THEN 1 ELSE 0 END
         + CASE WHEN s.building_use = 'other institution or hall' THEN 1 ELSE 0 END
    END
"""


def build(con):
    con.execute("""
        CREATE OR REPLACE TABLE cong_services AS
        SELECT DISTINCT c.cong_id, s.day, s.start, s."end", s.type, coalesce(s.language, '') AS language
        FROM place_cong c
        JOIN place_gathering g USING (id)
        JOIN extract_services s ON s.site_key = g.site_key AND g.site_ok
             AND (g.n_site_locations <= 1 OR s.location_id IS NULL OR s.location_id = g.location_id)
        WHERE s.recurrence = 'weekly'
    """)
    default_case = "CASE " + " ".join(
        f"WHEN k.tradition = '{t}' AND v.type = '{ty}' THEN {m}" for (t, ty), m in DEFAULT_MIN.items()
    ) + " " + " ".join(f"WHEN v.type = '{ty}' THEN {m}" for ty, m in DEFAULT_BY_TYPE.items()) + " ELSE 60 END"
    con.execute(f"""
        CREATE OR REPLACE TABLE cong_util AS
        WITH v AS (
          SELECT *, TRY_CAST(split_part(start, ':', 1) AS INT) * 60 + TRY_CAST(split_part(start, ':', 2) AS INT) AS s_min,
                    TRY_CAST(split_part("end", ':', 1) AS INT) * 60 + TRY_CAST(split_part("end", ':', 2) AS INT) AS e_min
          FROM cong_services
        ), d AS (
          SELECT v.*, k.tradition,
                 CASE WHEN e_min - s_min BETWEEN 15 AND 300 THEN e_min - s_min ELSE {default_case} END AS minutes,
                 coalesce(e_min - s_min BETWEEN 15 AND 300, false) AS posted_end  -- NULL end = not posted
          FROM v JOIN cong_sharing k USING (cong_id)
        ), main_day AS (
          SELECT cong_id, max(n) AS max_same_day FROM (
            SELECT cong_id, day, count(*) AS n FROM d WHERE type = 'main_worship' GROUP BY 1, 2) GROUP BY 1
        )
        SELECT d.cong_id,
               count(*) FILTER (WHERE type = 'main_worship') AS main_services,
               count(*) AS weekly_events,
               coalesce(any_value(m.max_same_day), 0) AS max_same_day,
               count(DISTINCT nullif(language, '')) FILTER (WHERE type = 'main_worship') AS main_languages,
               round(sum(minutes) / 60.0, 2) AS building_hours,
               round(sum(minutes) FILTER (WHERE type = 'main_worship') / 60.0, 2) AS main_hours,
               avg(posted_end::INT) AS share_posted_end
        FROM d LEFT JOIN main_day m USING (cong_id)
        GROUP BY d.cong_id
    """)
    con.execute(f"""
        CREATE OR REPLACE TABLE cong_util_full AS
        SELECT s.cong_id, s.bbl, s.tradition, s.borough, s.headline, {GROUP} AS building_group,
               s.building_use, coalesce(u.main_services, 0) AS main_services,
               coalesce(u.weekly_events, 0) AS weekly_events, coalesce(u.max_same_day, 0) AS max_same_day,
               coalesce(u.main_languages, 0) AS main_languages, coalesce(u.building_hours, 0) AS building_hours,
               u.share_posted_end, u.cong_id IS NOT NULL AND u.main_services > 0 AS has_schedule,
               s.cong_id IN (SELECT c.cong_id FROM place_cong c JOIN place_gathering g USING (id) WHERE g.site_ok)
                 AS has_matched_site,
               {USES} AS uses, s.space_key, s.shares_space, s.cotenant
        FROM cong_sharing s LEFT JOIN cong_util u USING (cong_id)
    """)


def report(con) -> str:
    q = lambda sql: con.execute(sql).df()  # noqa: E731
    one = lambda sql: con.execute(sql).fetchone()  # noqa: E731
    out = []
    w = out.append
    n, n_site, n_sched = one("""SELECT count(*), count(*) FILTER (WHERE has_matched_site),
                                       count(*) FILTER (WHERE has_schedule)
                                FROM cong_util_full WHERE headline""")
    w(f"# Services and building use in {config.CITY_SHORT}: first pass\n")
    w(f"Run {dt.date.today().isoformat()}. Of {n:,} congregations, {n_site:,} have a website that "
      f"matched their listing and {n_sched:,} posted weekly main services that extraction found, with a "
      "quote on the page for each. Everything below is about those congregations; they are likely "
      "larger and better established than those without a website or schedule.\n")
    if not n_sched:
        w("**No service data in this database.** Website extraction (step 4b) has not run here.\n")
        return "\n".join(out) + "\n"

    w("## City summary\n")
    w("All traditions. Multi-use and sharing cover every congregation except homes that look like "
      "a mailing address; the service columns cover those that posted a schedule.\n")
    w(md_table(q("""
        SELECT count(*) AS congregations,
               round(avg(uses), 2) AS avg_multi_use,
               round(100 * avg((uses >= 2)::INT)) AS pct_multi_use,
               round(100 * avg(shares_space::INT), 1) AS pct_sharing_worship_space,
               round(100 * avg(cotenant::INT), 1) AS pct_cotenants_separate_units,
               count(*) FILTER (WHERE has_schedule) AS with_schedule,
               round(avg(main_services) FILTER (WHERE has_schedule), 2) AS avg_main_services,
               round(100 * avg((main_services >= 2)::INT) FILTER (WHERE has_schedule)) AS pct_2plus_services,
               round(avg(building_hours) FILTER (WHERE has_schedule), 1) AS hours_per_week
        FROM cong_util_full WHERE headline AND uses IS NOT NULL
    """)))
    w("")

    w("## Multi-use and services, by tradition\n")
    w("Multi-use counts the distinct bodies using a congregation's worship space: 1 for the "
      "congregation, +1 for each other congregation sharing that space (same building, not a "
      "building split into units, or its website says so), +1 for a school that is not its own "
      "(public, charter, independent, college), +1 for a rented hall (community center, hotel, "
      "theater). A church alone is 1.0; with a nesting congregation, a charter school in its "
      "building, or meeting in a public school, 2.0. Congregations in separate units of one "
      "strip mall, office, flex or apartment building are separate places, each 1.0. The "
      "service columns cover congregations that posted a schedule.\n")
    w(md_table(q(f"""
        SELECT tradition, count(*) AS congregations,
               round(avg(uses), 2) AS mean_uses,
               round(100 * avg((uses = 1)::INT)) AS pct_one_use,
               round(100 * avg((uses = 2)::INT)) AS pct_two_uses,
               round(100 * avg((uses >= 3)::INT)) AS pct_three_plus,
               count(*) FILTER (WHERE has_schedule) AS with_schedule,
               round(avg(main_services) FILTER (WHERE has_schedule), 1) AS mean_main_services,
               round(100 * avg((main_services >= 2)::INT) FILTER (WHERE has_schedule)) AS pct_2plus_services,
               round(avg(building_hours) FILTER (WHERE has_schedule), 1) AS mean_hours_week
        FROM cong_util_full WHERE headline AND uses IS NOT NULL
        GROUP BY 1 HAVING count(*) >= {MIN_N} ORDER BY 2 DESC
    """)))
    w(f"\nBy {config.AREA_LABEL}, all traditions (service columns as above):\n")
    w(md_table(q(f"""
        SELECT borough AS "{config.AREA_LABEL}", count(*) AS congregations,
               round(avg(uses), 2) AS mean_uses,
               round(100 * avg((uses >= 2)::INT)) AS pct_multi_use,
               count(*) FILTER (WHERE has_schedule) AS with_schedule,
               round(avg(main_services) FILTER (WHERE has_schedule), 1) AS mean_main_services,
               round(100 * avg((main_services >= 2)::INT) FILTER (WHERE has_schedule)) AS pct_2plus_services
        FROM cong_util_full WHERE headline AND uses IS NOT NULL
        GROUP BY 1 ORDER BY 1
    """)))
    w("\nMulti-use within each kind of building:\n")
    w(md_table(q("""
        SELECT building_group, count(*) AS congregations, round(avg(uses), 2) AS mean_uses,
               max(uses) AS max_uses
        FROM cong_util_full WHERE headline AND uses IS NOT NULL AND building_group IS NOT NULL
        GROUP BY 1 ORDER BY 3
    """)))

    w("\n## Who has a schedule\n")
    w(md_table(q("""
        SELECT building_group, count(*) AS congregations,
               count(*) FILTER (WHERE has_matched_site) AS with_matched_site,
               count(*) FILTER (WHERE has_schedule) AS with_schedule,
               round(100 * avg(has_schedule::INT)) AS pct_with_schedule
        FROM cong_util_full WHERE headline AND building_group IS NOT NULL GROUP BY 1 ORDER BY 2 DESC
    """)))

    w("\n## Single-use religious buildings: services per week, within tradition\n")
    w("One congregation in its own religious building. Several main services, especially on the "
      "same day, means the building is used more intensively than one service a week.\n")
    w(md_table(q(f"""
        SELECT tradition, count(*) AS with_schedule,
               round(avg(main_services), 1) AS mean_main,
               median(main_services) AS median_main,
               round(100 * avg((main_services = 1)::INT)) AS pct_one,
               round(100 * avg((main_services = 2)::INT)) AS pct_two,
               round(100 * avg((main_services >= 3)::INT)) AS pct_three_plus,
               round(100 * avg((max_same_day >= 2)::INT)) AS pct_2plus_same_day,
               round(100 * avg((main_languages >= 2)::INT)) AS pct_2plus_languages,
               round(avg(building_hours), 1) AS mean_hours_week
        FROM cong_util_full
        WHERE headline AND has_schedule AND building_group = 'single-use religious building'
        GROUP BY 1 HAVING count(*) >= {MIN_N} ORDER BY 2 DESC
    """)))

    w("\n## The same, by kind of building\n")
    w("Main services per congregation, within tradition. A guest congregation in a shared building "
      "counts its own services, not its host's.\n")
    w(md_table(q(f"""
        PIVOT (SELECT tradition, building_group, main_services FROM cong_util_full
               WHERE headline AND has_schedule AND building_group IS NOT NULL
                 AND tradition IN (SELECT tradition FROM cong_util_full WHERE headline AND has_schedule
                                   GROUP BY 1 HAVING count(*) >= {MIN_N}))
        ON building_group USING round(avg(main_services), 1) GROUP BY tradition ORDER BY tradition
    """)))
    w("\nShare holding two or more main services:\n")
    w(md_table(q(f"""
        PIVOT (SELECT tradition, building_group, (main_services >= 2)::INT AS two_plus FROM cong_util_full
               WHERE headline AND has_schedule AND building_group IS NOT NULL
                 AND tradition IN (SELECT tradition FROM cong_util_full WHERE headline AND has_schedule
                                   GROUP BY 1 HAVING count(*) >= {MIN_N}))
        ON building_group USING round(100 * avg(two_plus)) GROUP BY tradition ORDER BY tradition
    """)))

    w("\n## Per place of worship: all congregations together\n")
    w("A place of worship is one worship space: a congregation on its own, or several sharing one "
      "space (co-tenants in separate units are separate places). Total weekly main services and "
      "worship hours per place, adding host and guests. Only places where every congregation "
      "posted a schedule, so totals are not undercounted.\n")
    w(md_table(q(f"""
        WITH place AS (
          SELECT CASE WHEN shares_space THEN space_key ELSE cong_id END AS place,
                 any_value(building_group) AS building_group,
                 count(*) AS congregations, bool_and(has_schedule) AS all_have_schedule,
                 sum(main_services) AS main_services, sum(building_hours) AS hours, max(uses) AS uses
          FROM cong_util_full WHERE headline AND building_group IS NOT NULL GROUP BY 1
        )
        SELECT building_group, count(*) AS places, round(avg(congregations), 2) AS congregations_per_place,
               round(avg(uses), 2) AS mean_uses,
               round(avg(main_services), 1) AS mean_main_services, median(main_services) AS median_main,
               round(avg(hours), 1) AS mean_hours_week
        FROM place WHERE all_have_schedule GROUP BY 1 ORDER BY 1
    """)))

    w(f"\n## Single-use religious buildings by {config.AREA_LABEL}\n")
    w(f"A rough look at place until land values are added (the plan's next phase). Within the two "
      f"largest traditions; cells under {MIN_N} congregations left blank.\n")
    top = [r[0] for r in con.execute("""
        SELECT tradition FROM cong_util_full WHERE headline AND has_schedule
          AND building_group = 'single-use religious building' AND tradition <> 'Unknown'
        GROUP BY 1 ORDER BY count(*) DESC LIMIT 2""").fetchall()]
    rows = []
    for t in top:
        df = q(f"""
            SELECT borough AS area, count(*) AS n, round(avg(main_services), 1) AS mean_main,
                   round(100 * avg((main_services >= 2)::INT)) AS pct_two_plus,
                   round(avg(building_hours), 1) AS hours
            FROM cong_util_full
            WHERE headline AND has_schedule AND building_group = 'single-use religious building'
              AND tradition = '{t.replace("'", "''")}'
            GROUP BY 1 ORDER BY 1
        """)
        df.insert(0, "tradition", t)
        rows.append(df)
    if rows:
        df = pd.concat(rows)
        for c in ("mean_main", "pct_two_plus", "hours"):
            df[c] = df[c].where(df["n"] >= MIN_N)
        df = df.rename(columns={"area": config.AREA_LABEL})
        w(md_table(df))

    posted = one("SELECT round(100 * avg(share_posted_end)) FROM cong_util_full WHERE has_schedule")[0]
    w("\n## Caveats\n")
    w(f"- Only {posted:.0f}% of services posted an end time; the rest use a default duration by "
      "tradition (`DEFAULT_MIN` in v0/analysis_services.py), so building-hours are approximate.")
    w("- Schedules are as posted on the day of the crawl; summer, holiday and Ramadan schedules differ. "
      "The plan recrawls a sample in a second season.")
    w("- Congregations without a matched website or posted schedule are not in these tables, and "
      "they skew small and renting, so the single-use figures speak for established congregations.")
    w("- Compare across rows only within a tradition.")
    return "\n".join(out) + "\n"


def main():
    con = connect(config.DB_PATH)
    build(con)
    OUT.write_text(report(con))
    print(OUT.read_text())


if __name__ == "__main__":
    main()
