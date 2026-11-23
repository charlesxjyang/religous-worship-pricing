"""Version 0, step 5 (NYC): flag colocation at the place people gather.

The site judged for each place is its GATHERING lot: the lot of the gathering
place its own website names (address_basis = "website"), or, when the website
names none we could place, the lot of the Overture listing (address_basis =
"listing"). Websites judged to belong to someone else (site_match "no") are
ignored.

Flag, first match wins (plan, Version 0 step 5):
  school      the lot holds an NCES school, or the website says it meets in one
  shared      two or more differently named congregations gather on the lot,
              or the website says it shares or borrows space
  commercial  the lot is in commercial use and not religious-owned, or the
              website says it meets in commercial space
  single-use  the lot is religious-owned
  unknown     none of the above

Two listings on a lot are the same congregation when they share a website, a
phone number or a normalized name; no fuzzy matching in v0.

Run after step 4c:  .venv/bin/python v0/step5_colocate.py
"""

import config
from common import connect

TRADITION_FROM_TAXONOMY = """
    CASE
      WHEN taxonomy_primary = 'roman_catholic_place_of_worship' THEN 'Catholic'
      WHEN taxonomy_primary LIKE '%orthodox%' THEN 'Orthodox Christian'
      WHEN basic_category = 'christian_place_of_worship' THEN 'Protestant and other Christian'
      WHEN basic_category = 'jewish_place_of_worship' THEN 'Jewish'
      WHEN basic_category = 'muslim_place_of_worship' THEN 'Muslim'
      WHEN basic_category = 'hindu_place_of_worship' THEN 'Hindu'
      WHEN basic_category = 'buddhist_place_of_worship' THEN 'Buddhist'
      WHEN taxonomy_primary = 'sikh_place_of_worship' THEN 'Sikh'
      ELSE 'Unknown' END
"""


def assign_congregations(con):
    """Group listings on one gathering lot into congregations.

    Two listings on the same lot are one congregation when they share a
    website, a phone number or a normalized name (the plan's merge keys, used
    exactly; no fuzzy matching in v0). Differently named listings with none of
    these in common stay separate: that overlap is what is measured.
    """
    rows = con.execute("""
        SELECT g.id, g.gathering_bbl, g.cong_key, coalesce(p.phones, []) AS phones
        FROM place_gathering g JOIN places p USING (id)
        WHERE coalesce(g.operating_status, '') <> 'permanently_closed'
          AND coalesce(g.site_match, '') <> 'no'
          -- its own website says it is an office, school or charity, not a congregation
          AND NOT (g.site_ok AND g.is_congregation = false)
    """).fetchall()
    parent = {}

    def find(x):
        while parent.setdefault(x, x) != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for pid, bbl, ckey, phones in rows:
        keys = [f"{bbl}|{ckey}"] + [f"{bbl}|tel:{ph[-10:]}" for ph in phones if ph]
        for k in keys:
            parent[find(k)] = find(f"id:{pid}")
    con.execute("CREATE OR REPLACE TABLE place_cong (id VARCHAR, cong_id VARCHAR)")
    con.executemany("INSERT INTO place_cong VALUES (?, ?)", [(r[0], find(f"id:{r[0]}")) for r in rows])


def main():
    con = connect(config.DB_PATH)
    for t, ddl in {
        "extract_sites": "site_key VARCHAR, site_match VARCHAR, tradition VARCHAR, schedule_found BOOLEAN, online_only BOOLEAN, is_congregation BOOLEAN, mailing_address VARCHAR, stop_reason VARCHAR",
        "extract_locations": "site_key VARCHAR, location_id INT, address VARCHAR, venue_name VARCHAR, venue_kind VARCHAR, is_primary BOOLEAN, evidence VARCHAR",
        "extract_services": 'site_key VARCHAR, day VARCHAR, start VARCHAR, "end" VARCHAR, type VARCHAR, language VARCHAR, recurrence VARCHAR, location_id INT, evidence VARCHAR',
        "extract_shares": "site_key VARCHAR, name VARCHAR, relation VARCHAR, evidence VARCHAR",
        "gathering_geo": "site_key VARCHAR, location_id INT, method VARCHAR, outside_nyc BOOLEAN, label VARCHAR, bbl BIGINT, bin VARCHAR",
    }.items():  # so step 5 runs, listing-only, before any extraction exists
        con.execute(f"CREATE TABLE IF NOT EXISTS {t} ({ddl})")

    con.execute(f"""
        CREATE OR REPLACE TABLE place_gathering AS
        WITH base AS (
          SELECT p.id, p.name, p.basic_category, p.taxonomy_primary, p.boroname, p.address,
                 p.confidence, p.operating_status, ps.start_url AS website, ps.site_key,
                 ps.social_urls, pl.bbl AS listing_bbl, pl.lot_match,
                 es.site_match, es.stop_reason,
                 coalesce(es.site_match IN ('yes', 'likely'), false) AS site_ok,
                 {TRADITION_FROM_TAXONOMY} AS tradition_overture,
                 es.tradition AS tradition_site, es.online_only, es.is_congregation,
                 es.mailing_address
          FROM places p
          JOIN place_lot pl USING (id)
          JOIN place_site ps USING (id)
          LEFT JOIN extract_sites es USING (site_key)
        ), locs AS (
          -- Gathering places from the site, best first: the one on this
          -- listing's own lot, then the site's primary, then by order given.
          SELECT b.id, l.location_id, l.address AS g_address, l.venue_name, l.venue_kind,
                 l.evidence AS g_evidence, g.bbl AS g_bbl, g.method AS g_method, g.label AS g_label,
                 g.outside_nyc,
                 row_number() OVER (PARTITION BY b.id ORDER BY
                     (g.bbl = b.listing_bbl) DESC NULLS LAST, (g.bbl IS NOT NULL) DESC,
                     l.is_primary DESC, l.location_id) AS rk,
                 count(*) OVER (PARTITION BY b.id) AS n_site_locations
          FROM base b
          JOIN extract_locations l ON l.site_key = b.site_key AND b.site_ok
          LEFT JOIN gathering_geo g ON g.site_key = l.site_key AND g.location_id = l.location_id
        )
        SELECT b.*,
               CASE WHEN b.site_ok AND b.tradition_site NOT IN ('Unknown', 'Other')
                    THEN b.tradition_site ELSE b.tradition_overture END AS tradition,
               l.location_id, l.g_address, l.venue_name, l.venue_kind, l.g_evidence, l.g_method,
               l.g_label, l.outside_nyc, coalesce(l.n_site_locations, 0) AS n_site_locations,
               l.g_bbl,
               CASE WHEN l.g_bbl IS NOT NULL THEN 'website' ELSE 'listing' END AS address_basis,
               coalesce(l.g_bbl, b.listing_bbl) AS gathering_bbl,
               (l.g_bbl IS NOT NULL AND l.g_bbl <> b.listing_bbl) AS gathering_differs_from_listing,
               -- Congregation identity for counting congregations per lot.
               CASE WHEN b.site_ok THEN 'site:' || b.site_key
                    ELSE 'name:' || trim(regexp_replace(
                         regexp_replace(lower(b.name), '[^a-z0-9 ]', ' ', 'g'),
                         '\\b(the|inc|incorporated|corp|of|ny|nyc|new york)\\b|\\s+', ' ', 'g'))
               END AS cong_key
        FROM base b LEFT JOIN locs l ON l.id = b.id AND l.rk = 1
    """)

    assign_congregations(con)

    con.execute("""
        CREATE OR REPLACE TABLE place_services AS
        SELECT g.id,
               count(*) FILTER (WHERE s.type = 'main_worship' AND s.recurrence = 'weekly') AS main_weekly_services,
               count(*) FILTER (WHERE s.recurrence = 'weekly') AS total_weekly_services,
               string_agg(s.day || ' ' || s.start || coalesce(' (' || s.language || ')', ''), '; '
                          ORDER BY list_position(['Sun','Mon','Tue','Wed','Thu','Fri','Sat'], s.day), s.start)
                 FILTER (WHERE s.type = 'main_worship' AND s.recurrence = 'weekly') AS main_services,
               any_value(s.evidence) FILTER (WHERE s.type = 'main_worship') AS service_evidence
        FROM place_gathering g
        JOIN extract_services s ON s.site_key = g.site_key AND g.site_ok
             -- a multi-site congregation: count services at this place, or unassigned ones
             AND (g.n_site_locations <= 1 OR s.location_id IS NULL OR s.location_id = g.location_id)
        GROUP BY g.id
    """)

    con.execute("""
        CREATE OR REPLACE TABLE place_colocation AS
        WITH active AS (
          SELECT g.*, c.cong_id FROM place_gathering g JOIN place_cong c USING (id)
        ), per_lot AS (
          SELECT gathering_bbl, count(DISTINCT cong_id) AS n_congregations,
                 string_agg(DISTINCT name, ' | ') AS names_on_lot
          FROM active GROUP BY 1
        ), shares AS (
          SELECT site_key, string_agg(relation || ': ' || name, '; ') AS shares_text
          FROM extract_shares GROUP BY 1
        )
        SELECT g.id, f.bldgclass, f.landuse_label, f.ownername, f.religious_owned,
               f.commercial_use, f.residential_use, f.n_schools, f.school_names,
               coalesce(pl.n_congregations, 1) AS n_congregations_on_lot, pl.names_on_lot,
               CASE WHEN g.site_ok THEN sh.shares_text END AS shares_text,
               CASE
                 WHEN f.n_schools > 0 OR g.venue_kind IN ('public_school', 'private_school') THEN 'school'
                 WHEN coalesce(pl.n_congregations, 1) >= 2 OR g.venue_kind = 'another_congregation'
                      OR (g.site_ok AND sh.shares_text IS NOT NULL) THEN 'shared'
                 WHEN (f.commercial_use AND NOT f.religious_owned) OR g.venue_kind = 'commercial_space' THEN 'commercial'
                 WHEN f.religious_owned THEN 'single-use'
                 ELSE 'unknown' END AS colocation,
               concat_ws('; ',
                 CASE WHEN f.n_schools > 0 THEN 'school on lot: ' || f.school_names END,
                 CASE WHEN g.venue_kind IN ('public_school', 'private_school', 'another_congregation',
                                            'commercial_space', 'home', 'community_or_other_institution')
                      THEN 'website says venue is ' || g.venue_kind END,
                 CASE WHEN coalesce(pl.n_congregations, 1) >= 2
                      THEN pl.n_congregations || ' congregations on lot' END,
                 CASE WHEN g.site_ok AND sh.shares_text IS NOT NULL THEN 'website: ' || sh.shares_text END,
                 CASE WHEN f.commercial_use AND NOT f.religious_owned THEN 'commercial lot (' || f.landuse_label || ')' END,
                 CASE WHEN f.religious_owned THEN 'religious-owned lot (' || coalesce(f.bldgclass, '') || ', ' || coalesce(f.ownername, '') || ')' END
               ) AS colocation_reason
        FROM place_gathering g
        LEFT JOIN lot_flags f ON f.bbl = g.gathering_bbl
        LEFT JOIN per_lot pl ON pl.gathering_bbl = g.gathering_bbl
        LEFT JOIN shares sh ON sh.site_key = g.site_key
    """)
    print(con.execute("""
        SELECT c.colocation, g.address_basis, count(*) AS places
        FROM place_colocation c JOIN place_gathering g USING (id)
        GROUP BY ALL ORDER BY 1, 2
    """).df().to_string(index=False))


if __name__ == "__main__":
    main()
