#!/usr/bin/env bash
# Rebuild one city end to end:  v0/run_city.sh nyc|dc [--after-extract]
# data/ is not in git, so a new session starts empty (about an hour for NYC,
# less for DC). Extraction (step 4b) is left out: pilot it and review it by
# hand (see CLAUDE.md), then rerun from step 4c with --after-extract.
set -euo pipefail
cd "$(dirname "$0")/.."
export CITY="${1:?usage: v0/run_city.sh nyc|dc [--after-extract]}"
[ -d .venv ] || python3 -m venv .venv
.venv/bin/pip install -q -r requirements.txt
py=.venv/bin/python
if [ "${2:-}" != "--after-extract" ]; then
  $py v0/step1_load.py
  $py v0/step2_parcels.py
  $py v0/step2b_listing_geocode.py
  $py v0/step2c_irs.py
  $py v0/step2d_osm.py
  $py v0/step3_recall.py
  $py v0/step4_crawl.py
  $py v0/step4_extract.py --estimate
fi
$py v0/step4_geocode.py
$py v0/step5_colocate.py
$py v0/step6_report.py > /dev/null
$py v0/analysis_sharing.py > /dev/null
echo "done: CITY=$CITY reports written"
