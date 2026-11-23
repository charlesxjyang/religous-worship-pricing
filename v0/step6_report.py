"""Version 0, step 6 (NYC): write the CSV, the 50-row check and the report.

Point-level files go to v0/private/ (gitignored: the repo is public and the
plan publishes aggregates only):
  v0/private/nyc.csv          one row per place
  v0/private/nyc_check50.csv  50 random rows with evidence and URLs
  v0/private/check50.md       the same 50 rows as a table
Aggregates go to v0/report.md, which is committed.

Run after step 5:  .venv/bin/python v0/step6_report.py
"""

import datetime as dt

import config
from common import connect
from step1_load import md_table

CSV = config.PRIVATE_DIR / "nyc.csv"
CHECK = config.PRIVATE_DIR / "nyc_check50.csv"
CHECK_MD = config.PRIVATE_DIR / "check50.md"
REPORT = config.REPORT_DIR / "report.md"
RECALL_CSV = config.PRIVATE_DIR / "nyc_recall_misses.csv"


def build_table(con):
    con.execute("""
        CREATE OR REPLACE TABLE v0_nyc AS
        WITH home AS (
          SELECT site_key, any_value(CASE WHEN n_chars > 0 THEN 'ok' ELSE coalesce(error, 'empty') END) AS crawl_status
          FROM crawl_pages WHERE role = 'home' GROUP BY 1
        )
        SELECT g.id AS overture_id, g.name, g.tradition, g.taxonomy_primary AS overture_category,
               g.boroname AS borough, g.address AS listing_address, g.listing_bbl,
               g.website, array_to_string(g.social_urls, ' ') AS social_urls,
               CASE WHEN g.website IS NULL THEN NULL ELSE coalesce(h.crawl_status, 'not crawled') END AS crawl_status,
               g.site_match,
               g.g_address AS gathering_address, g.venue_name AS gathering_venue,
               g.venue_kind AS gathering_venue_kind, g.g_evidence AS gathering_evidence,
               g.g_label AS gathering_geocoded, g.gathering_bbl, g.address_basis,
               g.gathering_differs_from_listing,
               CASE WHEN g.site_ok THEN g.mailing_address END AS mailing_address,
               coalesce(s.main_weekly_services, 0) AS main_weekly_services,
               coalesce(s.total_weekly_services, 0) AS total_weekly_services,
               s.main_services, s.service_evidence,
               coalesce(s.main_weekly_services, 0) > 0 AS schedule_found,
               c.colocation, c.colocation_reason, c.n_congregations_on_lot, c.names_on_lot,
               c.bldgclass AS lot_bldgclass, c.landuse_label AS lot_landuse, c.ownername AS lot_owner,
               c.religious_owned AS lot_religious_owned, c.school_names AS schools_on_lot,
               c.shared_evidence, c.ein AS irs_ein, c.irs_name, c.irs_kind, c.irs_match_basis,
               c.n_irs_congregations_on_lot, c.osm_religious_buildings_on_lot, c.osm_classes,
               g.online_only, round(g.confidence, 2) AS overture_confidence, g.operating_status
        FROM place_gathering g
        JOIN place_colocation c USING (id)
        LEFT JOIN place_services s USING (id)
        LEFT JOIN home h USING (site_key)
    """)


def chapman(n1, n2, m):
    """Chapman's capture-recapture estimate of a population seen by two lists."""
    return (n1 + 1) * (n2 + 1) / (m + 1) - 1


def cross_checks(con, w, q, one):
    """Deconfliction: what IRS records, OSM buildings and merge rules change."""
    w("\n## Cross-checks across sources\n")
    w("Four sources describe the same places independently: Overture listings, tax-lot "
      "records (building class and owner), OpenStreetMap religious buildings, and IRS "
      "registrations. IRS addresses are registered addresses (often an office, PO box or "
      "pastor's apartment), so they confirm *who* a listing is, not where it gathers.\n")

    w("### Duplicate listings or real sharing\n")
    w("Lots where two or more congregations seem to gather, as each merge rule is added:\n")
    w(md_table(q("SELECT merge_keys, congregations, lots_with_2plus, congregations_on_those_lots "
                 "FROM dedupe_stages ORDER BY stage")))
    w("\nEvidence behind each \"shared\" flag after merging:\n")
    w(md_table(q("""
        SELECT shared_evidence, count(*) AS places, count(DISTINCT gathering_bbl) AS lots
        FROM v0_nyc WHERE colocation = 'shared' GROUP BY 1 ORDER BY 2 DESC
    """)))

    n_irs = one("SELECT count(*) FROM irs_orgs")[0]
    if n_irs:
        w("\n### IRS registrations\n")
        w(md_table(q("""
            SELECT kind, count(*) AS orgs,
                   count(*) FILTER (WHERE po_box) AS po_box,
                   count(*) FILTER (WHERE street_unit IS NOT NULL) AS apartment_or_suite,
                   count(*) FILTER (WHERE bbl IS NOT NULL) AS placed_on_a_lot
            FROM irs_orgs GROUP BY 1 ORDER BY 2 DESC
        """)))
        w("\nOverture listings matched to an IRS registration (same lot, or a unique name "
          "match in the same ZIP code):\n")
        w(md_table(q("""
            SELECT tradition, count(*) AS places,
                   count(*) FILTER (WHERE irs_ein IS NOT NULL) AS matched,
                   round(100 * avg((irs_ein IS NOT NULL)::INT)) AS pct_matched,
                   count(*) FILTER (WHERE irs_match_basis = 'lot') AS on_same_lot,
                   count(*) FILTER (WHERE irs_kind IN ('school', 'support')) AS matched_school_or_support
            FROM v0_nyc GROUP BY 1 ORDER BY 2 DESC
        """)))
        w("\nIRS congregations that no Overture listing matched, by the lot of their "
          "registered address (listed in `v0/private/nyc_irs_only.csv`). Those registered on "
          "another body's religious lot, a school or a commercial lot are candidate renters "
          "and guests. Those at a house or apartment are mostly a pastor's or treasurer's "
          "address, not where people gather. PLUTO cuts owner names at about 21 characters, "
          "so some \"owned by another body\" lots are the congregation's own:\n")
        w(md_table(q("""
            SELECT lot_type, count(*) AS congregations,
                   count(*) FILTER (WHERE lot_has_listing) AS lot_has_an_overture_listing,
                   count(*) FILTER (WHERE ruling_year >= '2010') AS registered_since_2010
            FROM irs_only GROUP BY 1 ORDER BY 2 DESC
        """)))

    w("\n### Agreement at the lot level\n")
    w("Lots named by each source. Worship lot = building class M1/M9, or a religious owner "
      "with institutional use (the step 3 definition).\n")
    w(md_table(q("""
        WITH o AS (SELECT DISTINCT gathering_bbl AS bbl FROM v0_nyc WHERE gathering_bbl IS NOT NULL),
             p AS (SELECT bbl FROM recall_lots),
             m AS (SELECT bbl FROM osm_lot_flags),
             i AS (SELECT DISTINCT bbl FROM irs_orgs WHERE kind = 'congregation' AND bbl IS NOT NULL),
             u AS (SELECT bbl FROM o UNION SELECT bbl FROM p UNION SELECT bbl FROM m UNION SELECT bbl FROM i)
        SELECT (bbl IN (SELECT bbl FROM o))::INT AS overture, (bbl IN (SELECT bbl FROM p))::INT AS worship_lot,
               (bbl IN (SELECT bbl FROM m))::INT AS osm_building, (bbl IN (SELECT bbl FROM i))::INT AS irs,
               count(*) AS lots
        FROM u GROUP BY ALL ORDER BY lots DESC LIMIT 12
    """)))

    # Rough sizes. Both pairs violate the method's assumptions (the lists are
    # not independent, and IRS keeps closed churches), so treat as indicative.
    rows = []
    n1 = one("SELECT count(DISTINCT cong_id) FROM place_cong")[0]
    if n_irs:
        n2 = one("SELECT count(*) FROM irs_orgs WHERE kind = 'congregation'")[0]
        m = one("""SELECT count(DISTINCT c.cong_id) FROM place_cong c JOIN place_irs i USING (id)
                   WHERE i.irs_kind = 'congregation'""")[0]
        rows.append(("Congregations: Overture x IRS", n1, n2, m, round(chapman(n1, n2, m))))
    o_lots = one("SELECT count(DISTINCT gathering_bbl) FROM v0_nyc")[0]
    m_lots = one("SELECT count(*) FROM osm_lot_flags")[0]
    om = one("SELECT count(*) FROM osm_lot_flags WHERE bbl IN (SELECT gathering_bbl FROM v0_nyc)")[0]
    if m_lots:
        rows.append(("Lots: Overture x OSM buildings", o_lots, m_lots, om, round(chapman(o_lots, m_lots, om))))
    if rows:
        import pandas as pd
        w("\nCapture-recapture (Chapman). The lists are not independent and IRS keeps closed "
          "churches on file, so these are rough indications, not counts:\n")
        w(md_table(pd.DataFrame(rows, columns=["pair", "list_1", "list_2", "in_both", "estimated_total"])))


def report(con) -> str:
    q = lambda sql: con.execute(sql).df()  # noqa: E731
    one = lambda sql: con.execute(sql).fetchone()  # noqa: E731
    w, out = None, []
    w = out.append

    n = one("SELECT count(*) FROM v0_nyc")[0]
    (n_web, n_fetch, n_ok, n_match, n_sched, n_gather, n_differ) = one("""
        SELECT count(*) FILTER (WHERE website IS NOT NULL OR social_urls <> ''),
               count(*) FILTER (WHERE website IS NOT NULL),
               count(*) FILTER (WHERE crawl_status = 'ok'),
               count(*) FILTER (WHERE site_match IN ('yes', 'likely')),
               count(*) FILTER (WHERE schedule_found),
               count(*) FILTER (WHERE address_basis = 'website'),
               count(*) FILTER (WHERE gathering_differs_from_listing)
        FROM v0_nyc""")
    n_extracted = one("SELECT count(*) FROM extract_sites")[0]
    cost = one("SELECT coalesce(sum(cost_usd), 0) FROM extract_sites")[0]
    pct = lambda a: f"{100 * a / n:.0f}%" if n else "-"  # noqa: E731

    w("# Version 0 report: New York City\n")
    w(f"Run {dt.date.today().isoformat()}. {n:,} Overture places in the seven worship "
      f"categories. Colocation is judged at the lot where each congregation gathers: the "
      f"address its own website gives for services when we could place it, otherwise its "
      f"listing. Extraction used Claude Haiku 5.5 on {n_extracted:,} sites "
      f"(${cost:.2f}).\n")
    if n_extracted == 0:
        w("**Extraction has not run yet** (no API key in this session), so every row below "
          "uses the listing lot, and service counts are empty. Rerun steps 4b–6 once "
          "`WORSHIP_ANTHROPIC_API_KEY` is set.\n")

    w("## From listing to gathering place\n")
    w(md_table(q(f"""
        SELECT * FROM (VALUES
          ('Places', {n}, '100%'),
          ('With any website or social link', {n_web}, '{pct(n_web)}'),
          ('With a fetchable website (not social media)', {n_fetch}, '{pct(n_fetch)}'),
          ('Homepage fetched', {n_ok}, '{pct(n_ok)}'),
          ('Website confirmed as this congregation''s (yes or likely)', {n_match}, '{pct(n_match)}'),
          ('Weekly main services found, with evidence', {n_sched}, '{pct(n_sched)}'),
          ('Gathering place from website, placed on a lot', {n_gather}, '{pct(n_gather)}'),
          ('... on a different lot than the listing', {n_differ}, '{pct(n_differ)}')
        ) t(stage, places, share)
    """)))

    w("\n## Colocation by tradition\n")
    w(md_table(q("""
        PIVOT (SELECT tradition, colocation FROM v0_nyc)
        ON colocation IN ('school', 'shared', 'commercial', 'single-use', 'unknown')
        USING count(*) GROUP BY tradition ORDER BY tradition
    """)))
    w("\nColocation by where the address came from:\n")
    w(md_table(q("""
        PIVOT (SELECT address_basis, colocation FROM v0_nyc)
        ON colocation IN ('school', 'shared', 'commercial', 'single-use', 'unknown')
        USING count(*) GROUP BY address_basis ORDER BY address_basis
    """)))
    priv = one("""SELECT count(*) FROM v0_nyc WHERE colocation = 'school' AND lot_religious_owned
                  AND schools_on_lot LIKE '%(private)%' AND schools_on_lot NOT LIKE '%(public)%'""")[0]
    w(f"\nOf the school flags, {priv:,} are a private school on a religious-owned lot: most "
      "likely the congregation's own school, not a rental. The full rules split these out "
      "as \"own school on campus\".\n")

    w("## Weekly main services, where found\n")
    w(md_table(q("""
        SELECT tradition, count(*) AS places_with_schedule,
               round(avg(main_weekly_services), 1) AS mean_main,
               median(main_weekly_services) AS median_main,
               round(100 * avg((main_weekly_services >= 2)::INT)) AS pct_two_or_more,
               round(avg(total_weekly_services), 1) AS mean_all_weekly
        FROM v0_nyc WHERE schedule_found GROUP BY 1 ORDER BY 2 DESC
    """)))

    w("\n## Websites\n")
    w(md_table(q("""
        SELECT coalesce(crawl_status, '(no website)') AS homepage, count(*) AS places
        FROM (SELECT CASE WHEN crawl_status LIKE 'URLError%Tunnel%' THEN 'dead domain (proxy could not connect)'
                          WHEN crawl_status LIKE 'URLError%' OR crawl_status LIKE 'no_https%' THEN 'connection or TLS error'
                          ELSE crawl_status END AS crawl_status FROM v0_nyc)
        GROUP BY 1 ORDER BY 2 DESC LIMIT 12
    """)))
    if n_extracted:
        w("\nWebsite judged against the listing:\n")
        w(md_table(q("""SELECT coalesce(site_match, '(not extracted)') AS site_match, count(*) AS places
                        FROM v0_nyc WHERE crawl_status = 'ok' GROUP BY 1 ORDER BY 2 DESC""")))
        w("\nEvidence check (items whose quote was not found on the page are dropped):\n")
        w(md_table(q("""
            SELECT key, sum(CAST(value AS INT)) AS items FROM (
              SELECT unnest(map_keys(m)) AS key, unnest(map_values(m)) AS value
              FROM (SELECT CAST(json(verification) AS MAP(VARCHAR, INT)) AS m FROM extract_sites
                    WHERE verification <> '{}'))
            GROUP BY 1 ORDER BY 1
        """)))

    cross_checks(con, w, q, one)

    w("\n## Recall check: worship lots with no Overture place\n")
    w(md_table(q("""
        SELECT why, boroname AS borough, count(*) AS lots,
               count(*) FILTER (WHERE places_within_40m = 0) AS likely_misses
        FROM recall_lots GROUP BY ALL ORDER BY 1, 2
    """)))
    w("\nThe likely misses, with owner and address, are in `v0/private/nyc_recall_misses.csv`.\n")

    w("## 50 random rows for checking\n")
    w(f"Drawn with seed {config.SAMPLE_SEED}. They name places and addresses, so they are in "
      "`v0/private/check50.md` and `v0/private/nyc_check50.csv` (with evidence quotes and "
      "URLs), which are not committed.\n")

    w("## Known gaps in this run\n")
    w("- The cloud session reaches websites only over HTTPS; sites with no HTTPS show as "
      "connection or TLS errors and would load from a normal network.")
    w("- Version 0 reads static HTML only: no JavaScript rendering, PDFs or social media.")
    w("- Listings on one lot count as one congregation when they share a website, a phone "
      "number, a matching name or an IRS registration. Two names for one body with none of "
      "these in common still show as \"shared\"; the evidence column says how strong each "
      "flag is.")
    w("- Places with no website (about a third) can only be judged at their listing lot.")
    return "\n".join(out) + "\n"


def main():
    config.PRIVATE_DIR.mkdir(parents=True, exist_ok=True)
    con = connect(config.DB_PATH)
    build_table(con)
    con.execute(f"COPY (SELECT * FROM v0_nyc ORDER BY borough, name) TO '{CSV}' (HEADER)")
    con.execute(f"""COPY (SELECT * FROM irs_only ORDER BY lot_type, name)
                    TO '{config.PRIVATE_DIR / "nyc_irs_only.csv"}' (HEADER)""")
    con.execute(f"""
        CREATE OR REPLACE TABLE check50 AS
        SELECT * FROM (SELECT * FROM v0_nyc ORDER BY overture_id)
        USING SAMPLE reservoir(50 ROWS) REPEATABLE ({config.SAMPLE_SEED})
    """)
    con.execute(f"COPY (SELECT * FROM check50 ORDER BY borough, name) TO '{CHECK}' (HEADER)")
    con.execute("""
        CREATE OR REPLACE TABLE check50_short AS
        SELECT name, tradition, borough,
               coalesce(gathering_address, gathering_venue, listing_address) AS gathering_or_listing,
               address_basis AS basis, main_weekly_services AS main_svc, colocation,
               website
        FROM check50 ORDER BY borough, name
    """)
    REPORT.write_text(report(con))
    CHECK_MD.write_text(
        "# 50 random rows for checking (NYC Version 0)\n\n"
        "Check each against its website: is it a congregation, is the gathering place right, "
        "are the main weekly services right, is the colocation flag right? Evidence quotes "
        f"and URLs are in `{CHECK.name}`.\n\n"
        + md_table(con.execute("SELECT * FROM check50_short").df(), max_chars=45) + "\n")
    print(f"wrote {CSV.relative_to(config.ROOT)}, {CHECK.relative_to(config.ROOT)}, "
          f"{CHECK_MD.relative_to(config.ROOT)}, {REPORT.relative_to(config.ROOT)}")
    print(con.execute("SELECT colocation, count(*) FROM v0_nyc GROUP BY 1 ORDER BY 2 DESC").df().to_string(index=False))


if __name__ == "__main__":
    main()
