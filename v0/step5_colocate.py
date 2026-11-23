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

from collections import defaultdict

import config
from common import connect
from names import names_match

MAX_SHIFT_M = 150  # trust the listing's geocoded address over its map point up to this far

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


def match_irs(con):
    """Match each listing to an IRS-registered organization, if one fits.

    Candidates are IRS records geocoded to the listing's own lot or its
    gathering lot; failing that, records in the listing's ZIP code, accepted
    only when exactly one EIN matches by name. Writes table place_irs.
    """
    con.execute("""CREATE OR REPLACE TABLE place_irs (id VARCHAR, ein VARCHAR, irs_name VARCHAR,
                   irs_kind VARCHAR, basis VARCHAR)""")
    if not con.execute("SELECT count(*) FROM duckdb_tables() WHERE table_name = 'irs_orgs'").fetchone()[0]:
        return
    irs = con.execute("SELECT ein, name, kind, bbl, zip5 FROM irs_orgs").fetchall()
    by_bbl, by_zip = defaultdict(list), defaultdict(list)
    for rec in irs:
        if rec[3] is not None:
            by_bbl[rec[3]].append(rec)
        by_zip[rec[4]].append(rec)
    places = con.execute("""
        SELECT g.id, g.name, left(p.postcode, 5), g.listing_bbl, g.gathering_bbl
        FROM place_gathering g JOIN places p USING (id)
    """).fetchall()
    out = []
    kind_rank = {"congregation": 0, "other": 1, "support": 2, "school": 3}
    for pid, name, zip5, lbbl, gbbl in places:
        lot_cands = by_bbl.get(lbbl, []) + (by_bbl.get(gbbl, []) if gbbl != lbbl else [])
        hits = [r for r in lot_cands if names_match(name, r[1])]
        basis = "lot"
        if not hits and zip5:
            zhits = [r for r in by_zip.get(zip5, []) if names_match(name, r[1])]
            if len({r[0] for r in zhits}) == 1:
                hits, basis = zhits, "zip"
        if hits:
            best = min(hits, key=lambda r: kind_rank.get(r[2], 9))
            out.append((pid, best[0], best[1], best[2], basis))
    if out:
        con.executemany("INSERT INTO place_irs VALUES (?, ?, ?, ?, ?)", out)


def assign_congregations(con):
    """Group listings on one gathering lot into congregations.

    Listings on the same lot are one congregation when they share (in the
    order the report counts them):
      1. a website or an identical normalized name
      2. a phone number
      3. a matching name (names.names_match: abbreviations expanded,
         denominations must agree)
      4. an IRS registration (same EIN)
    Listings with none of these in common stay separate: that overlap is
    what is measured. Writes place_cong and dedupe_stages.
    """
    rows = con.execute("""
        SELECT g.id, g.gathering_bbl, g.cong_key, g.name, coalesce(p.phones, []) AS phones, i.ein
        FROM place_gathering g JOIN places p USING (id)
        LEFT JOIN place_irs i USING (id)
        WHERE coalesce(g.operating_status, '') <> 'permanently_closed'
          -- A website judged someone else's (site_match "no", often a namesake
          -- in another city) is ignored through site_ok; the listing stays.
          -- its own website says it is an office, school or charity, not a congregation
          AND NOT (g.site_ok AND g.is_congregation = false)
    """).fetchall()
    by_lot = defaultdict(list)
    for r in rows:
        by_lot[r[1]].append(r)

    def components(stage):
        parent = {}

        def find(x):
            while parent.setdefault(x, x) != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a, b):
            parent[find(a)] = find(b)

        for bbl, lot in by_lot.items():
            for pid, _, ckey, name, phones, ein in lot:
                find(pid)
                union(f"{bbl}|{ckey}", pid)
                if stage >= 2:
                    for ph in phones:
                        if ph:
                            union(f"{bbl}|tel:{ph[-10:]}", pid)
                if stage >= 4 and ein:
                    union(f"{bbl}|ein:{ein}", pid)
            if stage >= 3:
                for i, a in enumerate(lot):
                    for b in lot[i + 1:]:
                        if names_match(a[3], b[3]):
                            union(a[0], b[0])
        return {r[0]: find(r[0]) for r in rows}

    stage_names = {1: "website or same name", 2: "+ phone", 3: "+ name match", 4: "+ IRS EIN"}
    stats = []
    for stage in (1, 2, 3, 4):
        comp = components(stage)
        per_lot = defaultdict(set)
        for pid, bbl, *_ in rows:
            per_lot[bbl].add(comp[pid])
        stats.append((stage, stage_names[stage], len(set(comp.values())),
                      sum(1 for s in per_lot.values() if len(s) >= 2),
                      sum(len(s) for s in per_lot.values() if len(s) >= 2)))
    con.execute("""CREATE OR REPLACE TABLE dedupe_stages (stage INT, merge_keys VARCHAR,
                   congregations INT, lots_with_2plus INT, congregations_on_those_lots INT)""")
    con.executemany("INSERT INTO dedupe_stages VALUES (?, ?, ?, ?, ?)", stats)
    con.execute("CREATE OR REPLACE TABLE place_cong (id VARCHAR, cong_id VARCHAR)")
    con.executemany("INSERT INTO place_cong VALUES (?, ?)", list(comp.items()))


def main():
    con = connect(config.DB_PATH)
    for t, ddl in {
        "extract_sites": "site_key VARCHAR, site_match VARCHAR, tradition VARCHAR, schedule_found BOOLEAN, online_only BOOLEAN, is_congregation BOOLEAN, mailing_address VARCHAR, stop_reason VARCHAR",
        "extract_locations": "site_key VARCHAR, location_id INT, address VARCHAR, venue_name VARCHAR, venue_kind VARCHAR, is_primary BOOLEAN, evidence VARCHAR",
        "extract_services": 'site_key VARCHAR, day VARCHAR, start VARCHAR, "end" VARCHAR, type VARCHAR, language VARCHAR, recurrence VARCHAR, location_id INT, evidence VARCHAR',
        "extract_shares": "site_key VARCHAR, name VARCHAR, relation VARCHAR, evidence VARCHAR",
        "gathering_geo": "site_key VARCHAR, location_id INT, method VARCHAR, outside_nyc BOOLEAN, label VARCHAR, bbl BIGINT, bin VARCHAR",
        "irs_orgs": "ein VARCHAR, name VARCHAR, kind VARCHAR, bbl BIGINT, zip5 VARCHAR, street_unit VARCHAR, po_box BOOLEAN, ruling_year VARCHAR",
        "osm_lot_flags": "bbl BIGINT, osm_buildings INT, osm_classes VARCHAR, osm_names VARCHAR",
        "listing_geo": "id VARCHAR, confidence DOUBLE, bbl BIGINT, bin VARCHAR, shift_m DOUBLE",
    }.items():  # so step 5 runs, listing-only, before any extraction exists
        con.execute(f"CREATE TABLE IF NOT EXISTS {t} ({ddl})")

    con.execute(f"""
        CREATE OR REPLACE TABLE place_gathering AS
        WITH base AS (
          SELECT p.id, p.name, p.basic_category, p.taxonomy_primary, p.boroname, p.address,
                 p.confidence, p.operating_status, ps.start_url AS website, ps.site_key,
                 ps.social_urls,
                 -- the listing's own street address, geocoded, beats its map point
                 CASE WHEN lg.confidence >= 0.8 AND lg.shift_m <= {MAX_SHIFT_M} THEN lg.bbl ELSE pl.bbl END AS listing_bbl,
                 CASE WHEN lg.confidence >= 0.8 AND lg.shift_m <= {MAX_SHIFT_M} THEN lg.bin END AS listing_bin,
                 CASE WHEN lg.confidence >= 0.8 AND lg.shift_m <= {MAX_SHIFT_M} THEN 'address'
                      WHEN lg.confidence >= 0.8 THEN 'point (address ' || round(lg.shift_m) || ' m away)'
                      ELSE 'point' END AS listing_lot_method,
                 pl.lot_match,
                 es.site_match, es.stop_reason,
                 coalesce(es.site_match IN ('yes', 'likely'), false) AS site_ok,
                 {TRADITION_FROM_TAXONOMY} AS tradition_overture,
                 es.tradition AS tradition_site, es.online_only, es.is_congregation,
                 es.mailing_address
          FROM places p
          JOIN place_lot pl USING (id)
          JOIN place_site ps USING (id)
          LEFT JOIN listing_geo lg USING (id)
          LEFT JOIN extract_sites es USING (site_key)
        ), locs AS (
          -- Gathering places from the site, best first: the one on this
          -- listing's own lot, then the site's primary, then by order given.
          SELECT b.id, l.location_id, l.address AS g_address, l.venue_name, l.venue_kind,
                 l.evidence AS g_evidence, g.bbl AS g_bbl, g.bin AS g_bin, g.method AS g_method, g.label AS g_label,
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
               CASE WHEN l.g_bbl IS NOT NULL THEN l.g_bin ELSE b.listing_bin END AS gathering_bin,
               (l.g_bbl IS NOT NULL AND l.g_bbl <> b.listing_bbl) AS gathering_differs_from_listing,
               -- Congregation identity for counting congregations per lot.
               CASE WHEN b.site_ok THEN 'site:' || b.site_key
                    ELSE 'name:' || trim(regexp_replace(
                         regexp_replace(lower(b.name), '[^a-z0-9 ]', ' ', 'g'),
                         '\\b(the|inc|incorporated|corp|of|ny|nyc|new york)\\b|\\s+', ' ', 'g'))
               END AS cong_key
        FROM base b LEFT JOIN locs l ON l.id = b.id AND l.rk = 1
    """)

    match_irs(con)
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
        ), irs_lot AS (     -- IRS congregations registered at the lot
          SELECT bbl, count(DISTINCT ein) AS n_irs_congregations
          FROM irs_orgs WHERE kind = 'congregation' AND bbl IS NOT NULL GROUP BY 1
        ), ein_lot AS (     -- distinct IRS congregations the lot's listings matched
          SELECT a.gathering_bbl, count(DISTINCT i.ein) AS n_matched_eins
          FROM active a JOIN place_irs i USING (id) WHERE i.irs_kind = 'congregation' GROUP BY 1
        )
        SELECT g.id, f.bldgclass, f.landuse_label, f.ownername, f.religious_owned,
               f.commercial_use, f.residential_use, f.n_schools, f.school_names,
               coalesce(pl.n_congregations, 1) AS n_congregations_on_lot, pl.names_on_lot,
               coalesce(il.n_irs_congregations, 0) AS n_irs_congregations_on_lot,
               coalesce(el.n_matched_eins, 0) AS n_matched_eins_on_lot,
               i.ein, i.irs_name, i.irs_kind, i.basis AS irs_match_basis,
               coalesce(ol.osm_buildings, 0) AS osm_religious_buildings_on_lot, ol.osm_classes,
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
        LEFT JOIN irs_lot il ON il.bbl = g.gathering_bbl
        LEFT JOIN ein_lot el ON el.gathering_bbl = g.gathering_bbl
        LEFT JOIN place_irs i ON i.id = g.id
        LEFT JOIN osm_lot_flags ol ON ol.bbl = g.gathering_bbl
    """)
    # How strong the evidence for "shared" is, strongest first.
    con.execute("""
        ALTER TABLE place_colocation ADD COLUMN shared_evidence VARCHAR;
        UPDATE place_colocation c SET shared_evidence = CASE
            WHEN c.colocation <> 'shared' THEN NULL
            WHEN c.shares_text IS NOT NULL OR g.venue_kind = 'another_congregation' THEN 'website says so'
            WHEN c.n_matched_eins_on_lot >= 2 OR c.n_irs_congregations_on_lot >= 2 THEN 'two or more IRS congregations'
            ELSE 'listings only' END
        FROM place_gathering g WHERE g.id = c.id;
    """)

    # IRS congregations that no listing matched: what Overture missed, by the
    # kind of lot their registered address is on.
    con.create_function("names_match", names_match, ["VARCHAR", "VARCHAR"], "BOOLEAN",
                        null_handling="special")
    con.execute("""
        CREATE OR REPLACE TABLE irs_only AS
        WITH lots AS (
          SELECT gathering_bbl AS bbl FROM place_gathering
          UNION SELECT listing_bbl FROM place_gathering
        )
        SELECT o.ein, o.name, o.ruling_year, o.bbl, o.street_unit IS NOT NULL AS has_unit, o.po_box,
               f.landuse_label, f.ownername, f.bldgclass,
               o.bbl IN (SELECT bbl FROM lots) AS lot_has_listing,
               CASE WHEN o.po_box THEN 'PO box'
                    WHEN o.bbl IS NULL THEN 'address not placed'
                    WHEN f.n_schools > 0 THEN 'school lot'
                    WHEN f.religious_owned AND coalesce(names_match(o.name, f.ownername), false)
                      THEN 'religious lot it owns'
                    WHEN f.religious_owned THEN 'religious lot owned by another body'
                    WHEN f.residential_use AND o.street_unit IS NOT NULL THEN 'apartment'
                    WHEN f.residential_use THEN 'house or residential building'
                    WHEN f.commercial_use THEN 'commercial lot'
                    ELSE 'other lot' END AS lot_type
        FROM irs_orgs o LEFT JOIN lot_flags f ON f.bbl = o.bbl
        WHERE o.kind = 'congregation'
          AND o.ein NOT IN (SELECT ein FROM place_irs WHERE ein IS NOT NULL)
    """)
    print(con.execute("""
        SELECT c.colocation, g.address_basis, count(*) AS places
        FROM place_colocation c JOIN place_gathering g USING (id)
        GROUP BY ALL ORDER BY 1, 2
    """).df().to_string(index=False))


if __name__ == "__main__":
    main()
