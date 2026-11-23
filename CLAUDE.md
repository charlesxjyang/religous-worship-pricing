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
- [ ] Step 4b: extraction, waiting for `WORSHIP_ANTHROPIC_API_KEY`
  (run `--estimate`, then `--limit 50` as a pilot, then all).
- [ ] Step 4c–6: rerun after 4b. Until then they run on listing lots only.
- [ ] Charles checks the 50 rows.
- [x] Cross-checks (Charles, 2026-11-23: "add other deconflict strategies, e.g.
  IRS"): step 2c loads IRS EO BMF religious organizations and geocodes them;
  step 2d loads OSM religious buildings; step 5 merges listings on a lot by
  website, phone, `names.names_match` and IRS EIN, and grades each "shared"
  flag (`shared_evidence`).
- Scope (Charles, 2026-11-23): NYC plus about two other cities to start.
  Washington, DC is the second (Charles, 2026-11-23); the third is open.

## Cities

Every script takes the city from the `CITY` environment variable (`nyc`,
the default, or `dc`); `v0/config.py` holds the per-city settings and
`v0/dc.py` the DC loaders. Outputs: NYC in `v0/`, DC in `v0/dc/`, each with a
gitignored `private/` folder. Rebuild a city end to end with
`v0/run_city.sh nyc|dc` (extraction excluded), then `--after-extract`.

| Input | NYC | Washington, DC |
| --- | --- | --- |
| Subareas | 5 boroughs | 8 wards (DCGIS Ward - 2022) |
| Parcels | PLUTO + DOF tax lots; key BBL | OTR owner polygons (ITSPE); key SSL, surrogate `bbl` |
| Building type | DOF building class | DC use code mapped to DOF classes (`dc.USE_TO_CLASS`; 081 Religious = M1) |
| Religious ownership | class M, owner name | class M, owner name, RPTA exemption E1 (religious) |
| Geocoder | GeoSearch (BBL and BIN) | exact match to a parcel's premise address, else Census geocoder + parcel under the point; no building ID |
| IRS file | eo_ny.csv | eo_dc.csv |

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
