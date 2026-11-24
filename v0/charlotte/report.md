# Version 0 report: Charlotte, NC

Run 2026-11-24. 1,556 Overture places in the seven worship categories. Colocation is judged at the lot where each congregation gathers: the address its own website gives for services when we could place it, otherwise its listing. Extraction used Claude Haiku 5.5 on 615 sites ($0.77).

## From listing to gathering place

| stage | places | share |
| --- | --- | --- |
| Places | 1556 | 100% |
| With any website or social link | 1114 | 72% |
| With a fetchable website (not social media) | 1044 | 67% |
| Homepage fetched | 690 | 44% |
| Website confirmed as this congregation's (yes or likely) | 504 | 32% |
| Weekly main services found, with evidence | 380 | 24% |
| Gathering place from website, placed on a lot | 390 | 25% |
| ... on a different lot than the listing | 82 | 5% |

## Colocation by tradition

| tradition | school | shared | commercial | single-use | unknown |
| --- | --- | --- | --- | --- | --- |
| Buddhist | 0 | 2 | 1 | 9 | 0 |
| Catholic | 9 | 4 | 0 | 7 | 0 |
| Hindu | 0 | 1 | 1 | 0 | 0 |
| Jewish | 1 | 0 | 0 | 7 | 1 |
| Muslim | 4 | 0 | 4 | 6 | 4 |
| Orthodox Christian | 0 | 1 | 0 | 6 | 0 |
| Protestant and other Christian | 78 | 453 | 103 | 413 | 156 |
| Sikh | 0 | 0 | 0 | 1 | 0 |
| Unknown | 13 | 131 | 47 | 34 | 59 |

Colocation by where the address came from:

| address_basis | school | shared | commercial | single-use | unknown |
| --- | --- | --- | --- | --- | --- |
| listing | 62 | 460 | 133 | 316 | 195 |
| website | 43 | 132 | 23 | 167 | 25 |

Of the school flags, 49 are a private school on a religious-owned lot: most likely the congregation's own school, not a rental. The full rules split these out as "own school on campus".

## Weekly main services, where found

| tradition | places_with_schedule | mean_main | median_main | pct_two_or_more | mean_all_weekly |
| --- | --- | --- | --- | --- | --- |
| Protestant and other Christian | 362 | 1.3 | 1.0 | 22.0 | 1.8 |
| Catholic | 7 | 3.4 | 4.0 | 71.0 | 6.7 |
| Jewish | 4 | 1.8 | 2.0 | 75.0 | 1.8 |
| Muslim | 2 | 1.5 | 1.5 | 50.0 | 1.5 |
| Buddhist | 2 | 1.0 | 1.0 | 0.0 | 2.0 |
| Unknown | 1 | 1.0 | 1.0 | 0.0 | 1.0 |
| Orthodox Christian | 1 | 1.0 | 1.0 | 0.0 | 2.0 |
| Sikh | 1 | 2.0 | 2.0 | 100.0 | 5.0 |

## Websites

| homepage | places |
| --- | --- |
| ok | 690 |
| (no website) | 512 |
| dead domain (proxy could not connect) | 136 |
| robots_disallowed | 67 |
| connection or TLS error | 60 |
| http_404 | 34 |
| http_403 | 26 |
| empty | 21 |
| http_429 | 2 |
| http_503 | 2 |
| http_500 | 2 |
| http_522 | 1 |

Website judged against the listing:

| site_match | places |
| --- | --- |
| yes | 464 |
| no | 142 |
| likely | 40 |
| unclear | 29 |
| (not extracted) | 15 |

Evidence check (items whose quote was not found on the page are dropped):

| key | items |
| --- | --- |
| gathering_locations_dropped | 44.0 |
| gathering_locations_ok | 453.0 |
| mailing_dropped | 5.0 |
| services_dropped | 30.0 |
| services_ok | 781.0 |
| shares_space_with_ok | 30.0 |

## Cross-checks across sources

Four sources describe the same places independently: Overture listings, tax-lot records (building class and owner), OpenStreetMap religious buildings, and IRS registrations. IRS addresses are registered addresses (often an office, PO box or pastor's apartment), so they confirm *who* a listing is, not where it gathers.

### Duplicate listings or real sharing

Lots where two or more congregations seem to gather, as each merge rule is added:

| merge_keys | congregations | lots_with_2plus | congregations_on_those_lots |
| --- | --- | --- | --- |
| website or same name | 1470 | 279 | 703 |
| + phone | 1399 | 243 | 596 |
| + name match | 1379 | 232 | 565 |
| + IRS EIN | 1378 | 232 | 564 |

Evidence behind each "shared" flag after merging:

| shared_evidence | places | lots |
| --- | --- | --- |
| listings only | 484 | 186 |
| two or more IRS congregations | 77 | 25 |
| website says so | 31 | 25 |

### IRS registrations

| kind | orgs | po_box | apartment_or_suite | placed_on_a_lot |
| --- | --- | --- | --- | --- |
| congregation | 895 | 122 | 91 | 688 |
| other | 119 | 8 | 27 | 95 |
| support | 81 | 11 | 8 | 60 |
| school | 16 | 1 | 3 | 13 |

Overture listings matched to an IRS registration (same lot, or a unique name match in the same ZIP code):

| tradition | places | matched | pct_matched | on_same_lot | matched_school_or_support |
| --- | --- | --- | --- | --- | --- |
| Protestant and other Christian | 1203 | 276 | 23.0 | 179 | 6 |
| Unknown | 284 | 44 | 15.0 | 23 | 2 |
| Catholic | 20 | 7 | 35.0 | 6 | 2 |
| Muslim | 18 | 7 | 39.0 | 7 | 2 |
| Buddhist | 12 | 4 | 33.0 | 4 | 3 |
| Jewish | 9 | 2 | 22.0 | 2 | 0 |
| Orthodox Christian | 7 | 3 | 43.0 | 3 | 0 |
| Hindu | 2 | 1 | 50.0 | 1 | 0 |
| Sikh | 1 | 0 | 0.0 | 0 | 0 |

IRS congregations that no Overture listing matched, by the lot of their registered address (listed in `v0/charlotte/private/charlotte_irs_only.csv`). Those registered on another body's religious lot, a school or a commercial lot are candidate renters and guests. Those at a house or apartment are mostly a pastor's or treasurer's address, not where people gather. PLUTO cuts owner names at about 21 characters, so some "owned by another body" lots are the congregation's own:

| lot_type | congregations | lot_has_an_overture_listing | registered_since_2010 |
| --- | --- | --- | --- |
| house or residential building | 250 | 2 | 131 |
| PO box | 112 | 0 | 33 |
| address not placed | 73 | 0 | 39 |
| commercial lot | 64 | 22 | 26 |
| religious lot owned by another body | 52 | 50 | 18 |
| religious lot it owns | 31 | 26 | 11 |
| other lot | 26 | 4 | 11 |
| apartment | 23 | 0 | 10 |

### Agreement at the lot level

Lots named by each source. Worship lot = building class M1/M9, or a religious owner with institutional use (the step 3 definition).

| overture | worship_lot | osm_building | irs | lots |
| --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 0 | 464 |
| 0 | 0 | 0 | 1 | 376 |
| 0 | 1 | 0 | 0 | 205 |
| 1 | 1 | 1 | 0 | 156 |
| 1 | 1 | 1 | 1 | 110 |
| 1 | 1 | 0 | 0 | 102 |
| 1 | 0 | 0 | 1 | 77 |
| 1 | 1 | 0 | 1 | 60 |
| 1 | 0 | 1 | 0 | 56 |
| 1 | 0 | 1 | 1 | 29 |
| 0 | 0 | 1 | 0 | 27 |
| 0 | 1 | 1 | 0 | 25 |

Capture-recapture (Chapman). The lists are not independent and IRS keeps closed churches on file, so these are rough indications, not counts:

| pair | list_1 | list_2 | in_both | estimated_total |
| --- | --- | --- | --- | --- |
| Congregations: Overture x IRS | 1378 | 895 | 296 | 4159 |
| Lots: Overture x OSM buildings | 1054 | 404 | 351 | 1213 |

## Recall check: worship lots with no Overture place

| why | borough | lots | likely_misses |
| --- | --- | --- | --- |
| M1/M9 building class | District 1 | 161 | 34 |
| M1/M9 building class | District 2 | 123 | 24 |
| M1/M9 building class | District 3 | 109 | 22 |
| M1/M9 building class | District 4 | 41 | 7 |
| M1/M9 building class | District 5 | 93 | 13 |
| M1/M9 building class | District 6 | 80 | 29 |
| M1/M9 building class | District 7 | 38 | 5 |
| religious owner, institutional use | District 1 | 3 | 3 |
| religious owner, institutional use | District 2 | 4 | 1 |
| religious owner, institutional use | District 3 | 1 | 0 |
| religious owner, institutional use | District 4 | 1 | 0 |
| religious owner, institutional use | District 5 | 1 | 1 |
| religious owner, institutional use | District 6 | 3 | 2 |
| religious owner, institutional use | District 7 | 2 | 1 |

The likely misses, with owner and address, are in `v0/charlotte/private/charlotte_recall_misses.csv`.

## 50 random rows for checking

Drawn with seed 20261122. They name places and addresses, so they are in `v0/charlotte/private/check50.md` and `v0/charlotte/private/charlotte_check50.csv` (with evidence quotes and URLs), which are not committed.

## Known gaps in this run

- The cloud session reaches websites only over HTTPS; sites with no HTTPS show as connection or TLS errors and would load from a normal network.
- Version 0 reads static HTML only: no JavaScript rendering, PDFs or social media.
- Listings on one lot count as one congregation when they share a website, a phone number, a matching name or an IRS registration. Two names for one body with none of these in common still show as "shared"; the evidence column says how strong each flag is.
- Places with no website (about a third) can only be judged at their listing lot.
