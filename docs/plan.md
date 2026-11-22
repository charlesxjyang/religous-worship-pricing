# Houses of Worship Scraping Plan: NYC, Richmond, San Francisco, Chicago

2026-11-22 · @Charles

This plan is written for Claude Code. Read Background, build Version 0 only, and stop for review. Sections after Version 0 describe the full build and are reference for later versions.

## Background for Claude Code

The project tests whether houses of worship reveal how expensive space is in a city. Where space is dear, congregations should economize on it, much as developers build taller. They share a building with other congregations, rent a public school or a storefront, or pack more services into one building. Where space is cheap, each congregation owns its own building and uses it a few hours a week.

If that holds, counts of shared buildings, school rentals and services per building become a new measure of commercial-space affordability across neighborhoods and cities. A [literature review](https://claude.ai/artifact/BFEz8c6Tfh6HDpQQjnfFnp) found no study that measures it this way. The closest evidence:

- In Boston's Four Corners, 29 congregations used 20 buildings, drawn by vacant storefronts renting at about half nearby rates (McRoberts, late 1990s).
- 32% of congregations in Boston, Cambridge and Brookline shared worship space in 2011 (Emmanuel Gospel Center).
- Nationally, 84% of congregations own their building, 1.3% meet in schools and about 4% host another congregation (National Congregations Study, 2018–19).

What this means for the data:

1. **Renters and guests carry the price signal.** Long-time owners bought decades ago and pay no property tax, so their behavior says little about today's prices. Finding congregations that do not own their space is the priority, and they are the hardest to find: storefronts, schools, borrowed sanctuaries, often no website.
2. **A congregation is not a building.** A congregation is the organization; a site is the building or tax lot. One site can hold several congregations, and one congregation can use several sites. Never merge two congregations because they share an address; that overlap is what is being measured.
3. **Services are counted per week, within a tradition.** A mosque's five daily prayers and a church's Sunday service are not comparable; see Counting services.
4. **Every fact needs evidence.** Store the URL, fetch date and a short quote behind each extracted value so a person can audit it.

Out of scope for now: land values, the index itself, and any city not named here.

## Version 0: start simple

Version 0 is one city, free data and a 50-row hand check, to learn where each step breaks before paying for APIs. It produces one CSV for Richmond: each house of worship, its website, its weekly service count, and a colocation flag.

Inputs, all free; only an Anthropic key is needed:

- **Overture Maps places** inside Richmond's city limits (Census place FIPS 51760), from the latest release on S3 via DuckDB. Keep basic categories `place_of_worship`, `christian_place_of_worship`, `jewish_place_of_worship`, `muslim_place_of_worship`, `hindu_place_of_worship`, `buddhist_place_of_worship` and `religious_organization` ([taxonomy](https://github.com/OvertureMaps/docs/blob/main/static/taxonomy/2026-09-23.0/basic_categories.csv)). Many places carry a website.
- **Richmond assessor parcels** with owner, land use and tax-exempt code ([layer](https://services1.arcgis.com/k3vhq11XkBNeeOfM/ArcGIS/rest/services/Parcels/FeatureServer/layers)).
- **NCES school locations**, public and private, for Richmond ([private](https://catalog.data.gov/dataset/private-school-locations-current); public from the same EDGE program).

Steps:

1. Load the three inputs into DuckDB. Print category counts and 20 sample rows, and stop for Charles to sanity-check.
2. Attach each place to a parcel by point-in-polygon. Mark parcels whose owner, land use or exemption code is religious.
3. Recall check: list religious parcels with no Overture place on them. These are likely misses; count them.
4. For each place with a website, fetch the homepage and up to 3 linked pages whose link text or URL mentions worship, service, mass, times, schedule, visit, prayer or jumuah. Ask Claude for main weekly services and any "we meet at" address, each with an evidence quote.
5. Flag colocation, first match wins: "school" if the parcel also holds a school; "shared" if two or more differently named congregations sit on it; "commercial" if it is commercial and not religious-owned; "single-use" if it is religious-owned. Otherwise mark "unknown".
6. Write `v0/richmond.csv` and `v0/report.md`: counts by tradition and colocation flag, share with a website, share with a schedule found, the recall-check misses, and 50 random rows for Charles to check.

Done when Charles has checked the 50 rows. Version 1 then adds what the check shows is missing, probably Google Places for recall, a search API for missing websites, and the fuller rules below.

Not in version 0: Google Places, search APIs, IRS and OSM data, Playwright rendering, fuzzy deduplication and other cities.

## Full build: goal and outputs

Each city run produces a building-level census of houses of worship. It records every congregation found, its website, its weekly services, and whether its address is shared with a school, another congregation or another kind of building. After version 0, run the full build in Richmond, then NYC, San Francisco and Chicago.

Files written per city:

- `congregations.parquet`: one row per congregation, with tradition, denomination and website
- `sites.parquet`: one row per physical building or tax lot
- `occupancy.parquet`: congregation × site, with role (owner, host, guest, tenant, school renter)
- `services.parquet`: one row per recurring service
- `evidence.parquet`: the page, snippet and fetch date behind every extracted field
- `summary.md`: headline counts by tradition: share single-use, congregations per building, services per building, share meeting in schools

Land values and the index itself come in a later phase. This plan builds only the dataset they need.

## Cities

The four cities span a wide price range, and each publishes parcel data that flags religious or tax-exempt property. Chicago is the suggested Midwest pick: Cook County publishes a tax-exempt parcel file, and the city already has a literature on storefront churches and zoning.

| City | Boundary | Rough price tier | Parcel and building source | Notes |
| --- | --- | --- | --- | --- |
| Richmond, VA (pilot) | City limits (independent city) | Lowest of the four | [City assessor parcel layer](https://services1.arcgis.com/k3vhq11XkBNeeOfM/ArcGIS/rest/services/Parcels/FeatureServer/layers) with tax-exempt code, property class, land use and owner; [monthly public data set](https://www.rva.gov/node/2210) | Small enough to hand-check fully |
| Chicago, IL | City limits, within Cook County | Middle | Cook County [tax-exempt parcels](https://catalog.data.gov/dataset/assessor-property-tax-exempt-parcels) (religious, charitable, educational, tax year 2022 on) and [parcel universe](https://catalog-beta.data.gov/dataset/assessor-parcel-universe) | Zero-pad PINs to 14 digits |
| San Francisco, CA | City and county | High | DataSF [secured roll](https://catalog.data.gov/dataset/assessor-historical-secured-property-tax-rolls) with class, use and exemption codes | State law bars posting owner names online ([SF Assessor](https://www.sf.gov/resource--secured-property-tax-data)) |
| New York, NY | Five boroughs | Highest | PLUTO (BBL, religious building classes), building footprints (BIN), Geoclient geocoder | About 5,600 houses of faith ([Bricks and Mortals](https://urbanomnibus.net/holding-on-to-the-halo-effect)); run borough by borough |

School lists for every city: district open data for public and charter schools, plus NCES [private school locations](https://catalog.data.gov/dataset/private-school-locations-current), which the Private School Survey collects every two years with religious orientation ([PolicyMap](https://policymap.com/data/sources/national-center-for-education-statistics-private-school-universe-survey)).

Midwest alternatives: Minneapolis, where aging churches openly lease to immigrant congregations ([MPR](https://www.mprnews.org/story/2016/07/01/church-rentals-immigrant-congregations)), or a cheaper fast-growing city such as Columbus.

## Discovery sources

No single source is complete, so the agent takes the union of all of them and deduplicates. Renting congregations matter most and are the easiest to miss, so the sources that catch them get extra weight.

| Source | What it gives | Access | Limits and terms |
| --- | --- | --- | --- |
| Google Places API (New) | Places typed `church`, `synagogue`, `mosque`, `hindu_temple`, `buddhist_temple`, `shinto_shrine` ([types](https://developers.google.com/maps/documentation/places/web-service/place-types)); website field | Text Search: 20 per page, 60 max per query, one type per request, rectangle restriction ([docs](https://developers.google.com/maps/documentation/places/web-service/text-search)) | Only place IDs may be stored indefinitely; using Places coordinates for point-in-polygon analysis is barred ([policy](https://developers.google.com/maps/documentation/geocoding/policies)) |
| [Overture Maps places](https://docs.overturemaps.org/guides/places) | Meta, Microsoft, Foursquare and other POIs, including religious organizations | Parquet on S3/Azure, or BigQuery `bigquery-public-data.overture_maps.place` ([Earth Engine catalog](https://developers.google.com/earth-engine/datasets/catalog/overture-maps_places_place?hl=en)) | Per-record license by source: CDLA-Permissive, Apache or CC0 |
| OpenStreetMap (Overpass) | `amenity=place_of_worship` with religion and denomination tags | Overpass query by city area | ODbL share-alike; NYC extract holds about half the estimated total |
| IRS [EO Business Master File](https://www.irs.gov/charities-non-profits/exempt-organizations-business-master-file-extract-eo-bmf) | Registered religious organizations (NTEE group X) with addresses | Monthly CSV by state | Churches need not apply for exemption, so many are absent ([IRS](https://www.irs.gov/node/6165)); registered addresses can reveal congregations based at a school or another church |
| Local exempt-parcel data | Religious-owned lots, even with no web presence | See Cities table | Captures owners, not renters |
| Denominational finders | Diocesan parish lists, synagogue and mosque directories, ChurchFinder | Per-site crawl | Check each site's terms; MassTimes data needs written permission ([MassTimes](https://masstimes.org/components/about/about.html)) |
| Web search API | Website lookup by name and city; queries like "church meets at P.S." | Brave, SerpApi, Serper and others; Bing's API closed August 11, 2025 ([The Register](https://www.theregister.com/2025/05/15/bing_search_apis_retired/)) | Paid per query; Brave dropped its free plan ([Geekflare](https://geekflare.com/guides/brave-search-api-alternatives/)) |

The Google terms shape the design. Use Places to find candidates and their websites, keep only the place ID, and re-derive address and schedule from the congregation's own site and open data. Geocode with open tools (Census Geocoder, NYC Geoclient) for every spatial join. Have someone confirm this reading of the terms before the full run.

## Pipeline

Eight stages, each writing its own table so any stage can be rerun alone:

1. **Set up the city.** Load the boundary, parcels, building footprints and school lists into a local DuckDB. Tile the city into search rectangles, roughly 1 km in NYC and larger elsewhere.
2. **Discover candidates.** For each rectangle and each Google worship type, run Text Search with strict type filtering. If a rectangle returns the 60-result cap, split it into four and rerun. Then add Overture, OSM, IRS records (NTEE group X, city ZIP codes), exempt parcels and denominational finders.
3. **Catch untyped congregations.** Run name queries that type filters miss: ministries, fellowship, iglesia, masjid, Islamic center, shul, Chabad, Kingdom Hall, gurdwara, temple. Storefront and home-based congregations are often typed as businesses or not at all.
4. **Normalize and geocode.** Parse addresses with `usaddress` or libpostal, keeping floor and suite separately, since storefront churches are often upstairs. Geocode with the Census Geocoder in batches, or NYC Geoclient to get BIN and BBL directly. Assign parcel and building by point-in-polygon on these open coordinates.
5. **Deduplicate into congregations and sites.** Merge records that share a parcel and a similar name, a website domain or a phone number. Never merge two differently named congregations at one address; that overlap is the signal being measured.
6. **Find websites.** Use website fields from Places, OSM and Overture first, then a search API on name plus city. Accept a site only if its address or phone matches. Record Facebook and Instagram URLs, but do not scrape them.
7. **Crawl and extract schedules.** Respecting robots.txt, fetch the homepage and up to 8 likely pages (visit, worship, services, times, schedule, mass-times, prayer-times, jumuah, contact, locations), plus linked bulletin PDFs. Render with Playwright when static text is thin, and parse schema.org events and prayer-time widgets. Claude extracts services into the schema in Data model, quoting the evidence for each one.
8. **Match addresses and classify colocation.** Compare the listing address, any "we meet at" address on the website, the parcel's owner and use code, the school lists, and other congregations on the same building or lot. Apply the rules in Colocation rules, then run the checks in Quality checks.

Stamp every record with its fetch date. Schedules shift in summer, on holidays and during Ramadan, so recrawl a 10% subsample in a second season.

## Data model

Congregations and sites are separate entities joined by an occupancy table. That split is what lets one building hold several congregations, and one congregation hold several campuses.

| Table | Key fields |
| --- | --- |
| `congregations` | id, name, alternate names, tradition, denomination, languages, website, phone, Google place ID, OSM ID, Overture ID, EIN, sources, confidence |
| `sites` | id, normalized address, floor or unit, open-geocoder lat/lon, parcel ID (BBL, PIN or APN), building ID (BIN or footprint), land-use and exemption codes, owner where published, matched school ID, site type |
| `occupancy` | congregation ID, site ID, role (owner, host, guest, tenant, school renter, unknown), evidence ID |
| `services` | congregation ID, site ID, day, start, end, type, language, recurrence (weekly, monthly, seasonal), evidence ID, confidence |
| `evidence` | id, URL, fetch time, HTTP status, content hash, quote under 30 words, extractor version |

The extraction prompt returns this JSON per congregation, with `evidence` holding a short verbatim quote:

```json
{
  "schedule_found": true,
  "services": [
    {"day": "Sun", "start": "10:30", "end": null, "type": "main_worship",
     "language": "Spanish", "recurrence": "weekly", "evidence": "Domingos 10:30 am"}
  ],
  "meeting_address": {"text": "123 Main St", "venue_name": "P.S. 123 auditorium",
                      "differs_from_listing": true, "evidence": "We meet at P.S. 123"},
  "shares_space_with": [{"name": "Iglesia Nueva Vida", "relation": "guest", "evidence": "..."}]
}
```

## Colocation rules

Each site gets one class. Match in this order and stop at the first hit: building ID, then parcel ID, then normalized address including unit, then within 25 m plus a name mention on the website.

| Class | Rule | Typical evidence |
| --- | --- | --- |
| Single-use religious building | One congregation; parcel religious or exempt; owner matches the congregation or its denomination | Parcel owner and use code |
| Shared religious building | Two or more distinct congregations on one building or lot; host is the owner, others are guests | Two listings at one BIN or BBL; "hosted by" or "worships at" text |
| Public or charter school | Site matches a district school and the congregation does not own it | School list match; "we meet at P.S. 123" |
| Own school on campus | Matched school is private, shares the congregation's tradition, and the congregation or diocese owns the lot | NCES private school record plus owner match; not a rental |
| Commercial space | Parcel use is retail, office or mixed use and not religious-owned | Use code; unit or floor in the address |
| Other institution | Hotel, theater, community center, college, YMCA, funeral home | Use code or co-located place type |
| Residence | Parcel is residential: house church, shtiebel, home prayer room | Residential class code |
| Unknown | No match or conflicting evidence | Goes to the review queue |

When a Google or directory address conflicts with the congregation's own site, trust the site and set a `listing_conflict` flag. Stale listings are common for congregations that have moved.

## Counting services

Record two numbers per congregation: main weekly services, the gatherings most members attend, and total weekly worship events. Compare congregations only within a tradition, because daily prayer cycles make raw totals incomparable.

| Tradition | Main weekly services | Also record | Watch for |
| --- | --- | --- | --- |
| Catholic | Weekend Masses, Saturday vigil included | Weekday Masses | Each language Mass counts; one parish may run several churches |
| Protestant and other Christian | Sabbath or Sunday services | Midweek services; skip classes and Bible studies | Multisite campuses; a guest's service counts for the guest |
| Orthodox Christian | Divine Liturgy | Vespers | Feast-day schedules |
| Jewish | Shabbat services, Friday evening and Saturday morning | Daily minyanim | Small shuls often have no website |
| Muslim | Jumu'ah sessions | Daily iqama times | Several Friday shifts often mean the space is too small; count sessions, not clock times |
| Hindu, Buddhist, Sikh | Main weekly gathering | Daily puja or aarti | Temples often list open hours, not services |

Where a schedule lists no end time, impute a duration by tradition. Pope's cellphone study documents that attendance duration differs across traditions and can supply the defaults ([Pope, 2024](https://bfi.uchicago.edu/working-paper/religious-worship-attendance-in-america-evidence-from-cellphone-data/)). Building-hours of worship per week then follow from services × duration.

## Quality checks and pilot gates

The agent stops at three gates for a human review before spending more. Accuracy targets below are proposals, to be tightened once the pilot shows what is achievable.

1. **Gate 1, Richmond discovery.** Report candidate counts by source and a source-overlap matrix. Hand-check 50 random candidates for false positives such as church-supply shops or closed congregations. Drop any source that adds under 2% unique, valid records.
2. **Gate 2, Richmond extraction.** Hand-label 100 random congregations from their websites. Targets: main service count within one of the label for 90%, colocation class correct for 85%. Fix prompts and rules before moving on.
3. **Gate 3, one NYC community district.** Run end to end, review, then scale borough by borough. Check the citywide total against the roughly 5,600 Bricks and Mortals estimate and Furman's 7,643 faith-owned lots ([Furman Center](https://furmancenter.org/thestoop/entry/institutional-owned-land-and-new-york-citys-housing-crisis-the-extent-of-faith-based-owned-land-ownership)).

Automated checks on every run:

- Reject any service without an evidence quote
- Flag implausible times (other than dawn prayer), more than 30 main services, or more than 8 congregations at one site
- Estimate undercount with capture–recapture across sources that find congregations independently, such as Google versus IRS versus OSM
- Report the share of congregations with no website or no schedule, by tradition and neighborhood, since that gap likely tracks renting and small size

## Rules of the road

The crawl should be polite, licensed and privacy-safe, and the agent should enforce these rules in code rather than in prompts.

- **Google terms.** Store only place IDs, never use Places coordinates for spatial joins, and get the reading confirmed before the full run ([Geocoding policies](https://developers.google.com/maps/documentation/geocoding/policies)).
- **Crawling.** Obey robots.txt and site terms. Send a user agent with a contact email, keep to about one request per second per domain, and cache pages. Never bypass logins, CAPTCHAs or paywalls.
- **Social platforms.** Record Facebook and Instagram URLs only; do not scrape them.
- **Licenses.** OSM is ODbL, so a published derived database must be shared alike. Overture carries per-record licenses. MassTimes needs written permission. IRS files are public.
- **Personal data.** Keep no clergy names, personal emails or personal phones, only the congregation's main contact.
- **Residences and security.** Publish home-based congregations only at tract level or coarser. Publish city results as aggregates, and share point-level files on request.

## Running it in Claude Code

Run this in Claude Code on your own machine. A Claude cloud session like this one blocks most data hosts by default; NYC Open Data, Overpass and the IRS were all refused here.

To hand Claude Code this plan, export the doc as Markdown and save it as `CLAUDE.md` at the repo root, which Claude Code reads at the start of every session. Re-export after editing the doc, so the two stay in step.

Repo layout for the full build; version 0 needs only CLAUDE.md, a v0 folder and a few scripts:

```
worship-census/
  CLAUDE.md              # this plan condensed: rules, schema, gates
  config/cities.yaml     # boundary, FIPS, parcel and school sources, budget caps
  src/discover/          # google_places, overture, osm, irs_bmf, parcels, directories
  src/normalize/         # address, geocode, dedupe
  src/web/               # find_site, crawl, extract
  src/match/             # colocate
  src/qa/                # checks, review samples
  data/<city>/raw|interim|final
  reports/<city>/summary.md
```

Keys needed: Google Maps Platform, one search API, Anthropic, and NYC Geoclient. Put hard spending caps per city in `cities.yaml`, and check current Places and search-API pricing before setting them. Use a small Claude model for bulk extraction, and a larger one to re-check low-confidence records.

Kickoff prompt for the first session:

> Read CLAUDE.md. Build Version 0 for Richmond only. Do step 1 and stop so I can check the category counts and sample rows. Do not use Google Places or any search API.

Later sessions each start from the last stopping point: "Step 1 looks right. Run steps 2–6 and write v0/report.md." After the 50-row check, decide what version 1 adds and update this doc first.

## Open decisions

These choices change the code or the budget, so settle them before Gate 1:

- [ ] Midwest city: Chicago (suggested), Minneapolis or Columbus
- [ ] Scope: every house of worship, or only churches, synagogues and mosques
- [ ] Budget caps per city for Places, search API and extraction
- [ ] Google Places in or out, given its storage terms; without it, discovery relies on Overture, OSM, IRS and parcels
- [ ] Colocation unit in NYC: building (BIN) or tax lot (BBL)
- [ ] Online-only congregations: drop, or keep and flag
- [ ] Release policy: aggregates only, or point-level files too

## Sources

- [Google, Places API (New) Text Search](https://developers.google.com/maps/documentation/places/web-service/text-search)
- [Google, Place types](https://developers.google.com/maps/documentation/places/web-service/place-types)
- [Google, Geocoding API policies](https://developers.google.com/maps/documentation/geocoding/policies)
- [Overture Maps, Places guide](https://docs.overturemaps.org/guides/places)
- [IRS, Exempt Organizations Business Master File](https://www.irs.gov/charities-non-profits/exempt-organizations-business-master-file-extract-eo-bmf)
- [IRS, Churches and tax-exempt recognition](https://www.irs.gov/node/6165)
- [NCES, Private School Locations](https://catalog.data.gov/dataset/private-school-locations-current)
- [City of Richmond, Assessor parcels layer](https://services1.arcgis.com/k3vhq11XkBNeeOfM/ArcGIS/rest/services/Parcels/FeatureServer/layers)
- [City of Richmond, Assessor public data sets](https://www.rva.gov/node/2210)
- [Cook County Assessor, Tax-exempt parcels](https://catalog.data.gov/dataset/assessor-property-tax-exempt-parcels)
- [Cook County Assessor, Parcel universe](https://catalog-beta.data.gov/dataset/assessor-parcel-universe)
- [San Francisco Assessor-Recorder, Secured property tax data](https://www.sf.gov/resource--secured-property-tax-data)
- [DataSF, Historical secured property tax rolls](https://catalog.data.gov/dataset/assessor-historical-secured-property-tax-rolls)
- [The Register, Bing Search APIs retired](https://www.theregister.com/2025/05/15/bing_search_apis_retired/)
- [MassTimes.org, About and data terms](https://masstimes.org/components/about/about.html)
- [Pope, Religious worship attendance from cellphone data](https://bfi.uchicago.edu/working-paper/religious-worship-attendance-in-america-evidence-from-cellphone-data/)
- [Furman Center, Faith-based land ownership in NYC](https://furmancenter.org/thestoop/entry/institutional-owned-land-and-new-york-citys-housing-crisis-the-extent-of-faith-based-owned-land-ownership)
- [Urban Omnibus, Holding on to the halo effect (Bricks and Mortals)](https://urbanomnibus.net/holding-on-to-the-halo-effect)

- [Overture Maps, Places taxonomy (2026-09-23.0)](https://github.com/OvertureMaps/docs/blob/main/static/taxonomy/2026-09-23.0/basic_categories.csv)
- [Literature review: Houses of Worship as a Signal of Space Affordability](https://claude.ai/artifact/BFEz8c6Tfh6HDpQQjnfFnp)
