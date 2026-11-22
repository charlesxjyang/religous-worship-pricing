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

Outputs: `v0/nyc.csv` and `v0/report.md` (the plan's `v0/richmond.csv`), plus
`v0/step1_report.md` from step 1.

Status:

- [x] Step 1: inputs loaded, counts and 20 samples in `v0/step1_report.md`.
  **Stop here** until Charles says step 1 looks right.
- [ ] Steps 2–6.

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
- NYC is about 30 times Richmond's size: expect about 10,000 Overture places,
  so the step 4 crawl needs a cost estimate before it runs at full size.

## Environment

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python v0/step1_load.py
```

- DuckDB extensions come from PyPI wheels (`duckdb-extension-*`), pinned to
  the DuckDB version. The extension server is blocked in cloud sessions.
- Overture's bucket is public. `common.connect()` sets an S3 secret with empty
  keys, because cloud sessions export placeholder `AWS_*` variables that S3 rejects.
- The cloud environment `religous-worship-pricing` allows
  `data.cityofnewyork.us`, `s-media.nyc.gov`, `www.nyc.gov` and `nces.ed.gov`.
  `www.nyc.gov` (DCP's Bytes of the Big Apple pages) answers 403 to scripted
  requests. Do not work around that; use NYC Open Data copies instead.
- HTTP etiquette is in `v0/common.py`: a project user agent (add a contact
  with the `CONTACT_EMAIL` environment variable), one request at a time, a 1 s
  pause, and cached downloads under `data/nyc/raw/`, which is not committed.
