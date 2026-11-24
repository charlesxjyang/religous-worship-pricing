# Version 0 report: New York City

Run 2026-11-24. 9,522 Overture places in the seven worship categories. Colocation is judged at the lot where each congregation gathers: the address its own website gives for services when we could place it, otherwise its listing. Extraction used Claude Haiku 5.5 on 2,944 sites ($3.96).

## From listing to gathering place

| stage | places | share |
| --- | --- | --- |
| Places | 9522 | 100% |
| With any website or social link | 6275 | 66% |
| With a fetchable website (not social media) | 5965 | 63% |
| Homepage fetched | 3556 | 37% |
| Website confirmed as this congregation's (yes or likely) | 2150 | 23% |
| Weekly main services found, with evidence | 1457 | 15% |
| Gathering place from website, placed on a lot | 1640 | 17% |
| ... on a different lot than the listing | 301 | 3% |

## Colocation by tradition

| tradition | school | shared | commercial | single-use | unknown |
| --- | --- | --- | --- | --- | --- |
| Buddhist | 1 | 8 | 27 | 50 | 18 |
| Catholic | 68 | 95 | 17 | 301 | 68 |
| Hindu | 0 | 6 | 30 | 43 | 40 |
| Jewish | 31 | 85 | 75 | 302 | 116 |
| Muslim | 12 | 31 | 73 | 135 | 40 |
| Orthodox Christian | 10 | 6 | 5 | 42 | 3 |
| Protestant and other Christian | 171 | 1148 | 1398 | 2411 | 901 |
| Sikh | 0 | 4 | 3 | 8 | 1 |
| Unknown | 59 | 317 | 588 | 339 | 436 |

Colocation by where the address came from:

| address_basis | school | shared | commercial | single-use | unknown |
| --- | --- | --- | --- | --- | --- |
| listing | 246 | 1314 | 2001 | 2847 | 1474 |
| website | 106 | 386 | 215 | 784 | 149 |

Of the school flags, 145 are a private school on a religious-owned lot: most likely the congregation's own school, not a rental. The full rules split these out as "own school on campus".

## Weekly main services, where found

| tradition | places_with_schedule | mean_main | median_main | pct_two_or_more | mean_all_weekly |
| --- | --- | --- | --- | --- | --- |
| Protestant and other Christian | 1119 | 1.3 | 1.0 | 21.0 | 2.3 |
| Catholic | 162 | 3.4 | 3.0 | 86.0 | 10.2 |
| Jewish | 92 | 1.7 | 2.0 | 51.0 | 5.6 |
| Orthodox Christian | 39 | 1.2 | 1.0 | 18.0 | 3.3 |
| Muslim | 23 | 1.3 | 1.0 | 17.0 | 7.3 |
| Hindu | 8 | 1.0 | 1.0 | 0.0 | 9.3 |
| Buddhist | 7 | 1.3 | 1.0 | 14.0 | 5.1 |
| Unknown | 7 | 1.1 | 1.0 | 14.0 | 2.1 |

## Websites

| homepage | places |
| --- | --- |
| (no website) | 3557 |
| ok | 3556 |
| dead domain (proxy could not connect) | 721 |
| connection or TLS error | 631 |
| robots_disallowed | 458 |
| http_403 | 237 |
| http_404 | 141 |
| empty | 131 |
| http_429 | 32 |
| http_500 | 14 |
| http_522 | 11 |
| http_503 | 7 |

Website judged against the listing:

| site_match | places |
| --- | --- |
| yes | 1882 |
| no | 1044 |
| likely | 268 |
| (not extracted) | 198 |
| unclear | 164 |

Evidence check (items whose quote was not found on the page are dropped):

| key | items |
| --- | --- |
| gathering_locations_dropped | 167.0 |
| gathering_locations_ok | 1848.0 |
| mailing_dropped | 24.0 |
| services_dropped | 497.0 |
| services_ok | 5716.0 |
| shares_space_with_dropped | 2.0 |
| shares_space_with_ok | 98.0 |

## Cross-checks across sources

Four sources describe the same places independently: Overture listings, tax-lot records (building class and owner), OpenStreetMap religious buildings, and IRS registrations. IRS addresses are registered addresses (often an office, PO box or pastor's apartment), so they confirm *who* a listing is, not where it gathers.

### Duplicate listings or real sharing

Lots where two or more congregations seem to gather, as each merge rule is added:

| merge_keys | congregations | lots_with_2plus | congregations_on_those_lots |
| --- | --- | --- | --- |
| website or same name | 9102 | 1327 | 3109 |
| + phone | 8793 | 1123 | 2596 |
| + name match | 8668 | 1043 | 2391 |
| + IRS EIN | 8666 | 1042 | 2388 |

Evidence behind each "shared" flag after merging:

| shared_evidence | places | lots |
| --- | --- | --- |
| listings only | 1217 | 545 |
| two or more IRS congregations | 394 | 149 |
| website says so | 89 | 72 |

### IRS registrations

| kind | orgs | po_box | apartment_or_suite | placed_on_a_lot |
| --- | --- | --- | --- | --- |
| congregation | 11100 | 560 | 1842 | 10388 |
| support | 1130 | 47 | 246 | 1052 |
| other | 1063 | 25 | 288 | 1009 |
| school | 859 | 18 | 92 | 828 |

Overture listings matched to an IRS registration (same lot, or a unique name match in the same ZIP code):

| tradition | places | matched | pct_matched | on_same_lot | matched_school_or_support |
| --- | --- | --- | --- | --- | --- |
| Protestant and other Christian | 6029 | 2148 | 36.0 | 1486 | 47 |
| Unknown | 1739 | 438 | 25.0 | 268 | 29 |
| Jewish | 609 | 283 | 46.0 | 207 | 16 |
| Catholic | 549 | 136 | 25.0 | 86 | 33 |
| Muslim | 291 | 127 | 44.0 | 112 | 12 |
| Hindu | 119 | 48 | 40.0 | 37 | 2 |
| Buddhist | 104 | 52 | 50.0 | 47 | 17 |
| Orthodox Christian | 66 | 28 | 42.0 | 27 | 3 |
| Sikh | 16 | 6 | 38.0 | 6 | 1 |

IRS congregations that no Overture listing matched, by the lot of their registered address (listed in `v0/private/nyc_irs_only.csv`). Those registered on another body's religious lot, a school or a commercial lot are candidate renters and guests. Those at a house or apartment are mostly a pastor's or treasurer's address, not where people gather. PLUTO cuts owner names at about 21 characters, so some "owned by another body" lots are the congregation's own:

| lot_type | congregations | lot_has_an_overture_listing | registered_since_2010 |
| --- | --- | --- | --- |
| house or residential building | 2783 | 75 | 1073 |
| commercial lot | 1755 | 308 | 667 |
| religious lot owned by another body | 1125 | 631 | 309 |
| other lot | 888 | 110 | 397 |
| apartment | 664 | 17 | 356 |
| PO box | 480 | 0 | 98 |
| religious lot it owns | 440 | 191 | 100 |
| school lot | 176 | 66 | 48 |
| address not placed | 125 | 0 | 49 |

### Agreement at the lot level

Lots named by each source. Worship lot = building class M1/M9, or a religious owner with institutional use (the step 3 definition).

| overture | worship_lot | osm_building | irs | lots |
| --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 1 | 5250 |
| 1 | 0 | 0 | 0 | 2823 |
| 0 | 1 | 0 | 0 | 1234 |
| 1 | 1 | 0 | 1 | 1064 |
| 1 | 0 | 0 | 1 | 1036 |
| 1 | 1 | 0 | 0 | 972 |
| 1 | 1 | 1 | 0 | 715 |
| 1 | 1 | 1 | 1 | 704 |
| 0 | 1 | 0 | 1 | 402 |
| 0 | 1 | 1 | 0 | 306 |
| 0 | 0 | 1 | 0 | 170 |
| 1 | 0 | 1 | 0 | 85 |

Capture-recapture (Chapman). The lists are not independent and IRS keeps closed churches on file, so these are rough indications, not counts:

| pair | list_1 | list_2 | in_both | estimated_total |
| --- | --- | --- | --- | --- |
| Congregations: Overture x IRS | 8666 | 11100 | 2894 | 33233 |
| Lots: Overture x OSM buildings | 7452 | 2113 | 1557 | 10112 |

## Recall check: worship lots with no Overture place

| why | borough | lots | likely_misses |
| --- | --- | --- | --- |
| M1/M9 building class | Bronx | 717 | 53 |
| M1/M9 building class | Brooklyn | 1876 | 404 |
| M1/M9 building class | Manhattan | 699 | 56 |
| M1/M9 building class | Queens | 1301 | 138 |
| M1/M9 building class | Staten Island | 224 | 41 |
| religious owner, institutional use | Bronx | 74 | 26 |
| religious owner, institutional use | Brooklyn | 259 | 122 |
| religious owner, institutional use | Manhattan | 111 | 21 |
| religious owner, institutional use | Queens | 147 | 53 |
| religious owner, institutional use | Staten Island | 51 | 19 |

The likely misses, with owner and address, are in `v0/private/nyc_recall_misses.csv`.

## 50 random rows for checking

Drawn with seed 20261122. They name places and addresses, so they are in `v0/private/check50.md` and `v0/private/nyc_check50.csv` (with evidence quotes and URLs), which are not committed.

## Known gaps in this run

- The cloud session reaches websites only over HTTPS; sites with no HTTPS show as connection or TLS errors and would load from a normal network.
- Version 0 reads static HTML only: no JavaScript rendering, PDFs or social media.
- Listings on one lot count as one congregation when they share a website, a phone number, a matching name or an IRS registration. Two names for one body with none of these in common still show as "shared"; the evidence column says how strong each flag is.
- Places with no website (about a third) can only be judged at their listing lot.
