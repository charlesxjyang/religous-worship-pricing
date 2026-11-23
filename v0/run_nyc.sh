#!/usr/bin/env bash
# Rebuild NYC Version 0 from scratch: data/ is not in git, so a new session
# starts empty. About an hour, mostly polite downloads and geocoding.
# Extraction (step 4b) is left out: run its pilot and review it by hand
# (see CLAUDE.md), then rerun from step 4c with:  v0/run_nyc.sh --after-extract
set -euo pipefail
cd "$(dirname "$0")/.."
[ -d .venv ] || python3 -m venv .venv
.venv/bin/pip install -q -r requirements.txt
py=.venv/bin/python
if [ "${1:-}" != "--after-extract" ]; then
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
echo "done: v0/report.md, v0/analysis_sharing.md, v0/private/"
