# Worship census: notes for Claude Code

The plan lives in a Claude doc and is mirrored here; read it first:

@docs/plan.md

`docs/plan.md` is an export of the [plan doc](https://claude.ai/artifact/RNXJiTk3gGheVYh2Ydh1vH).
When the doc changes, re-export it rather than editing the copy by hand.

## Current task: Version 0 in NYC

Version 0 runs in **New York City**, not Richmond (Charles, 2026-11-22). The
steps are the plan's Version 0 steps; only the inputs and output names change.

| Plan's Richmond input | NYC input used | Where |
| --- | --- | --- |
| Census place 51760 boundary | DCP borough boundaries, water included | NYC Open Data `wh2p-dxnf` |
| Assessor parcels with owner, land use, exemption code | PLUTO 26v2 attributes joined on BBL to DOF Digital Tax Map lot polygons | `64uk-42ks` (its geometry column is empty), `i38t-6if2` |
| NCES public and private schools | Same NCES EDGE files (public 2024-25, private 2023-24), clipped to the boroughs | nces.ed.gov |
| Overture places | Same: latest release on S3, the seven kept basic categories | `s3://overturemaps-us-west-2` |

**Gathering address, not business address** (Charles, 2026-11-23). What
matters is where people physically gather for worship, not a mailing, office
or registered address. Step 4 asks each congregation's own website where it
holds services, geocodes that to a lot, and step 5 judges colocation at that
lot. The Overture listing lot is only the fallback (`address_basis`).

Outputs: `v0/report.md` (aggregates, committed) and, in `v0/private/`
(gitignored), `nyc.csv`, `nyc_check50.csv`, `check50.md` and
`nyc_recall_misses.csv`. The repo is **public** and the plan publishes
aggregates only, so never commit point-level files (names, addresses, lots);
send them to Charles directly.

Status:

- [x] Step 1: inputs loaded, `v0/step1_report.md`.
- [x] Step 2: places and schools attached to lots; lots flagged.
- [x] Step 3: recall check.
- [x] Step 4a: websites crawled (`data/nyc/raw/web/`).
- [x] Step 4b: extraction (prompt v0.2) rerun for all five cities on
  2026-11-24 ($7.92 in all: NYC $3.96, Houston $1.91, DC $0.81, Charlotte
  $0.75, SF $0.49); steps 4c–6, the analyses and the price test rerun after it.
- Only a session that has run extraction holds its results (data/ is not in
  git): do not regenerate a city's committed reports from a database without
  them, or the post-extraction numbers are overwritten.
- [ ] Charles checks the 50 rows.
- [x] Cross-checks (Charles, 2026-11-23: "add other deconflict strategies, e.g.
  IRS"): step 2c loads IRS EO BMF religious organizations and geocodes them;
  step 2d loads OSM religious buildings; step 5 merges listings on a lot by
  website, phone, `names.names_match` and IRS EIN, and grades each "shared"
  flag (`shared_evidence`).
- Scope (Charles, 2026-11-23): NYC plus about two other cities to start.
  Washington, DC is the second and Charlotte, NC the third (Charles, 2026-11-23/24).
  San Francisco and Houston added (Charles, 2026-11-24) to test whether the price
  slope follows how easily a metro can build: Saiz (2010) supply elasticities SF
  0.66, NYC 0.76, DC 1.61, Houston 2.30, Charlotte 3.09.
- [x] Price test, all five cities (Charles, 2026-11-24, brought forward from the
  plan's later phase): `v0/analysis_price.py` prices each congregation by the
  assessed land value of retail and office lots within 1 km and regresses
  sharing, multi-use and storefront use on it (`v0/analysis_price.md`). Use
  this local-radius price, not ZIP codes or housing prices, which Charles
  judged the wrong scale and the wrong market. First run used listing
  addresses (no extraction in that session); rerun after extraction.
  Charlotte land values come from the county CAMA layer, pulled in the script.
  SF prices only retail and office parcels sold since 2015 (Proposition 13 keeps
  older assessments near the purchase price). The script also checks each
  city's slope against ZIP income and building size. `PRICE_CITIES=nyc,dc`
  runs a subset. For comparisons across cities it adds the value of retail and
  office floor space per sq ft, scaled to 2021+ sale prices where published
  (NYC DOF market values x2.42, Charlotte x1.31, DC x1.02; Houston cannot be
  checked); assessed land values are not comparable between cities.
- [x] Occupancy and utilization (Charles, 2026-11-24): `v0/analysis_utilization.py`
  (congregations per worship space, weekly hours of worship) after the price
  test. `v0/export_worship_table.py --all` writes one private row per
  congregation (address, services, building, co-located uses, prices) to
  `<city>_worship_places.csv` in each private folder.

## Cities

Every script takes the city from the `CITY` environment variable (`nyc`,
the default, `dc`, `charlotte`, `sf` or `houston`); `v0/config.py` holds the
per-city settings, `v0/dc.py`, `v0/charlotte.py`, `v0/sf.py` and
`v0/houston.py` the city loaders, and `v0/arcgis.py` and
`v0/addrgeo.py` the shared ArcGIS paging and address-to-parcel geocoding.
Outputs: NYC in `v0/`, others in `v0/<city>/`, each with a gitignored
`private/` folder. Rebuild a city end to end with
`v0/run_city.sh <city>` (extraction excluded), then `--after-extract`.

| Input | NYC | Washington, DC | Charlotte, NC | San Francisco | Houston |
| --- | --- | --- | --- | --- | --- |
| Subareas | 5 boroughs | 8 wards (DCGIS Ward - 2022) | 7 city council districts | 11 supervisor districts (DataSF 2022) | 11 council districts (COH 2024) |
| Parcels | PLUTO + DOF tax lots; key BBL | OTR owner polygons (ITSPE); key SSL, surrogate `bbl` | Mecklenburg Parcel_Landuse, Charlotte tax district; key PID, surrogate `bbl` | DataSF active parcels + secured roll 2025; key mapblklot, surrogate `bbl` | HCAD 2026 real_acct + parcel geodatabase, accounts in jurisdiction 061; key acct, surrogate `bbl` |
| Building type | DOF building class | DC use code mapped to DOF classes (`dc.USE_TO_CLASS`; 081 Religious = M1) | land-use description mapped to DOF classes (`charlotte.class_for`; CHURCH = M1) | property class code (`sf.CLASS_OF`; W churches = M1) | commercial building type (`houston.TYPE_CLASS`; 4620 Religious = M1), else state class |
| Religious ownership | class M, owner name | class M, owner name, RPTA exemption E1 | class M, owner name, exemption RELIGIOUS | class W, church (7) and religious (6) exemptions; no owner names (state law) | type 4620, state class X3, owner name |
| Geocoder | GeoSearch (BBL and BIN) | exact match to a parcel's premise address, else Census geocoder + parcel under the point; no building ID | exact match to county address points (with parent parcel), else Census; no building ID | exact match to EAS addresses (with parcel), else Census; no building ID | exact match to HCAD site addresses, else Census; no building ID |
| IRS file | eo_ny.csv | eo_dc.csv | eo_nc.csv, ZIP 282xx and city CHARLOTTE | eo_ca.csv, ZIP 941xx and city SAN FRANCISCO | eo_tx.csv, ZIP 770xx/772xx and city HOUSTON |

Outside NYC a lot with a religious tax exemption counts as a religious
building whatever its use code (the exemption requires religious use).
HCAD's files are zips and a file geodatabase under `data/houston/raw/hcad/`,
unzipped to `hcad_x/` and `hcad_gis/` before step 1 (curved parcel shapes are
linearised in `houston.linear_wkb`). Houston's parts outside Harris County are
not covered. DataSF moved to data.sf.gov.

**Sharing and multi-use** (Charles, 2026-11-24). Sharing means two distinct
congregations using the same worship space: another congregation in the same
*building* (NYC: BIN; elsewhere: Overture building footprint, step 2e),
where the building is not split into units, or the congregation's website says
it shares space. Congregations in separate units of one strip mall, office,
flex, industrial or apartment building are **co-tenants**: separate places of
worship, not sharing. Multi-use = 1 + each congregation sharing the space + a
school that is not its own + a rented hall. A house church counts 1.

A new cloud session gets environment variables (the API key) but not
`data/`, which is gitignored: rebuild with `v0/run_city.sh` first.

```bash
.venv/bin/python v0/step2_parcels.py
.venv/bin/python v0/step2c_irs.py      # IRS registrations, geocoded (about 30 min)
.venv/bin/python v0/step2d_osm.py      # OSM religious buildings via Overture
.venv/bin/python v0/step3_recall.py
.venv/bin/python v0/step4_crawl.py
.venv/bin/python v0/step4_extract.py --estimate
.venv/bin/python v0/step4_geocode.py
.venv/bin/python v0/step5_colocate.py
.venv/bin/python v0/step6_report.py
.venv/bin/python v0/analysis_price.py  # all five cities, after analysis_sharing/services for each
.venv/bin/python v0/analysis_utilization.py
.venv/bin/python v0/export_worship_table.py --all
```

Only one process can open a city's DuckDB file at a time; run steps in order.
Prefix any command with `CITY=dc` for Washington, DC.

## NYC notes for steps 2–6

- Religious parcel test (step 2): building class `M1`–`M9`; or owner name
  matching church, congregation, synagogue, temple, masjid, mosque, Islamic,
  diocese, parish, ministries and similar. PLUTO has no exemption code; owner
  type `X` and `exempttot` are proxies. DOF exemption detail on NYC Open Data
  carries the codes if needed.
- PLUTO keys condominiums by billing BBL (lot 75xx) while DOF polygons carry
  the base lot, so some PLUTO rows have no polygon. Report the gap, don't drop it.
- Colocation unit in v0 is the tax lot (BBL). BIN (building) is an open
  decision in the plan.
- NYC is about 30 times Richmond's size: about 9,500 Overture places and 5,300
  distinct websites. Run `step4_extract.py --estimate` before a full run.
- Many Overture websites belong to a namesake elsewhere (a Norfolk, VA church
  for a Bronx listing). Extraction reports `site_match`; "no" sites are ignored.
- IRS addresses are registered addresses (offices, PO boxes, pastors'
  apartments). Use them to tell who a listing is and to find missed
  congregations, never as the gathering place. The "in care of" field names
  people and is not stored.
- Overpass (OSM's API) is unreachable from cloud sessions; OSM building tags
  come from Overture's buildings theme instead (source "OpenStreetMap" only).
- `v0/names.py` holds the name matcher; run it to see its test cases. Use it
  only within one lot or ZIP code, never citywide.

## Environment

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python v0/step1_load.py
```

- DuckDB extensions come from PyPI wheels (`duckdb-extension-*`), pinned to
  the DuckDB version. The extension server is blocked in cloud sessions.
- Overture's bucket is public. `common.connect()` sets an S3 secret with empty
  keys, because cloud sessions export placeholder `AWS_*` variables that S3 rejects.
- The cloud environment `religous-worship-pricing` has unrestricted network
  access (needed to crawl thousands of congregation sites). Its proxy carries
  **HTTPS only**, so the crawler upgrades `http://` links; HTTP-only sites fail
  here and would load from a normal network.
- `www.nyc.gov` (DCP's Bytes of the Big Apple pages) answers 403 to scripted
  requests. Do not work around that; use NYC Open Data copies instead.
- Extraction reads the key from `WORSHIP_ANTHROPIC_API_KEY`, set as an
  environment variable in the environment's settings. Not `ANTHROPIC_API_KEY`,
  which Claude Code itself would pick up. The client sets
  `base_url="https://api.anthropic.com"` because cloud sessions set
  `ANTHROPIC_BASE_URL`. Model `claude-haiku-5-5` (the plan's small model for
  bulk extraction), hard cap `MAX_SPEND_USD` in `v0/step4_extract.py`.
- Gathering addresses are geocoded with NYC Planning Labs GeoSearch
  (`geosearch.planninglabs.nyc`, no key), which returns BBL and BIN.
- HTTP etiquette is in `v0/common.py`: a project user agent (add a contact
  with the `CONTACT_EMAIL` environment variable), one request at a time, a 1 s
  pause, and cached downloads under `data/nyc/raw/`, which is not committed.
