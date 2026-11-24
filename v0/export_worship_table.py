"""One table of houses of worship per city: one row per congregation, private.

Columns: name(s), tradition, the address where it gathers (from its website where
extraction found one, else its listing) and which that is, the tax lot and
building, the building's type, weekly services (main and all) and weekly hours,
the other congregations using the same worship space (count and names),
co-tenants in other units of the building, schools on the lot and how they
relate, IRS registration, and the local commercial land and floor-space prices.

Point-level, so it is written to v0/<city>/private/ (gitignored) and never
committed. Run after analysis_price.py:
    CITY=dc .venv/bin/python v0/export_worship_table.py      (or --all)
"""

import sys

import duckdb

import config


def export(city):
    c = config.CITIES[city]
    con = duckdb.connect(str(config.ROOT / "data" / city / c["db_name"]), read_only=True)
    has_price = con.execute("SELECT count(*) FROM duckdb_tables() WHERE table_name = 'cong_price'").fetchone()[0] > 0
    price_cols = ("p.local_psf AS land_usd_per_sqft_1km, p.local_space_psf AS floor_space_usd_per_sqft_1km, "
                  "p.area_name AS area" if has_price else "NULL AS land_usd_per_sqft_1km, NULL AS floor_space_usd_per_sqft_1km, NULL AS area")
    price_join = "LEFT JOIN cong_price p USING (cong_id)" if has_price else ""
    df = con.execute(f"""
        WITH addr AS (
          SELECT pc.cong_id,
                 first(CASE WHEN g.address_basis = 'website' THEN g.g_address ELSE g.address END
                       ORDER BY g.address_basis = 'website' DESC, g.confidence DESC) AS gathering_address,
                 first(g.address_basis ORDER BY g.address_basis = 'website' DESC) AS address_from,
                 first(g.venue_name ORDER BY g.venue_name IS NULL) AS venue_name,
                 first(g.website ORDER BY g.website IS NULL) AS website
          FROM place_cong pc JOIN place_gathering g USING (id) GROUP BY 1
        ), space AS (
          SELECT space_key, list(split_part(names, ';', 1) ORDER BY cong_id) AS names_in_space
          FROM cong_sharing WHERE headline AND shares_space GROUP BY 1
        )
        SELECT s.cong_id, s.names, s.tradition, a.gathering_address, a.address_from, a.venue_name, a.website,
               s.bbl AS lot, s.space_key AS building, s.building_use, s.bldgclass AS lot_class, s.religious_owned,
               u.main_services AS main_weekly_services, u.weekly_events AS all_weekly_services,
               u.building_hours AS weekly_hours, u.has_schedule,
               s.shares_space, CASE WHEN s.shares_space THEN s.others_space END AS other_congregations_in_space,
               CASE WHEN s.shares_space THEN array_to_string(list_filter(sp.names_in_space,
                    lambda x: x <> split_part(s.names, ';', 1)), '; ') END AS other_congregation_names,
               s.cotenant, s.others_same_building AS congregations_elsewhere_in_building,
               s.schools_on_lot, s.school_check, s.home_check, s.other_use,
               s.irs_congregation AS irs_registered, s.irs_on_same_lot,
               {price_cols}
        FROM cong_sharing s
        LEFT JOIN cong_util_full u USING (cong_id)
        LEFT JOIN addr a USING (cong_id)
        LEFT JOIN space sp ON sp.space_key = s.space_key AND s.shares_space
        {price_join}
        WHERE s.headline
        ORDER BY s.cong_id""").df()
    con.close()
    out = c["report_dir"] / "private" / f"{city}_worship_places.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)
    print(f"{city}: {len(df):,} congregations, {int(df.has_schedule.fillna(False).sum()):,} with services, "
          f"{int((df.address_from == 'website').sum()):,} addressed from their website -> {out.relative_to(config.ROOT)}")


if __name__ == "__main__":
    for city in (list(config.CITIES) if "--all" in sys.argv else [config.CITY]):
        export(city)
