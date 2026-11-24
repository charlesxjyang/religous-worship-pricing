# Version 0 report: New York City

Run 2026-11-24. 9,522 Overture places in the seven worship categories. Colocation is judged at the lot where each congregation gathers: the address its own website gives for services when we could place it, otherwise its listing. Extraction used Claude Haiku 5.5 on 3,076 sites ($4.13).

## From listing to gathering place

| stage | places | share |
| --- | --- | --- |
| Places | 9522 | 100% |
| With any website or social link | 6275 | 66% |
| With a fetchable website (not social media) | 5965 | 63% |
| Homepage fetched | 3652 | 38% |
| Website confirmed as this congregation's (yes or likely) | 2243 | 24% |
| Weekly main services found, with evidence | 1529 | 16% |
| Gathering place from website, placed on a lot | 1736 | 18% |
| ... on a different lot than the listing | 338 | 4% |

## Colocation by tradition

| tradition | school | shared | commercial | single-use | unknown |
| --- | --- | --- | --- | --- | --- |
| Buddhist | 0 | 8 | 26 | 49 | 19 |
| Catholic | 67 | 99 | 17 | 304 | 60 |
| Hindu | 0 | 6 | 28 | 44 | 40 |
| Jewish | 33 | 88 | 75 | 302 | 114 |
| Muslim | 12 | 31 | 72 | 134 | 42 |
| Orthodox Christian | 12 | 9 | 4 | 42 | 3 |
| Protestant and other Christian | 177 | 1161 | 1399 | 2411 | 895 |
| Sikh | 0 | 4 | 3 | 8 | 1 |
| Unknown | 59 | 316 | 580 | 335 | 433 |

Colocation by where the address came from:

| address_basis | school | shared | commercial | single-use | unknown |
| --- | --- | --- | --- | --- | --- |
| listing | 246 | 1307 | 1986 | 2788 | 1459 |
| website | 114 | 415 | 218 | 841 | 148 |

Of the school flags, 147 are a private school on a religious-owned lot: most likely the congregation's own school, not a rental. The full rules split these out as "own school on campus".

## Weekly main services, where found

| tradition | places_with_schedule | mean_main | median_main | pct_two_or_more | mean_all_weekly |
| --- | --- | --- | --- | --- | --- |
| Protestant and other Christian | 1172 | 1.3 | 1.0 | 22.0 | 2.2 |
| Catholic | 165 | 3.4 | 4.0 | 87.0 | 9.9 |
| Jewish | 113 | 1.7 | 2.0 | 51.0 | 5.2 |
| Orthodox Christian | 40 | 1.2 | 1.0 | 15.0 | 3.6 |
| Muslim | 23 | 1.3 | 1.0 | 17.0 | 11.5 |
| Hindu | 7 | 1.0 | 1.0 | 0.0 | 4.6 |
| Buddhist | 4 | 1.0 | 1.0 | 0.0 | 3.5 |
| Unknown | 4 | 1.0 | 1.0 | 0.0 | 1.5 |
| Sikh | 1 | 1.0 | 1.0 | 0.0 | 15.0 |

## Websites

| homepage | places |
| --- | --- |
| ok | 3652 |
| (no website) | 3557 |
| dead domain (proxy could not connect) | 717 |
| connection or TLS error | 506 |
| robots_disallowed | 460 |
| http_403 | 238 |
| http_404 | 160 |
| empty | 127 |
| http_429 | 37 |
| http_500 | 16 |
| http_522 | 8 |
| RemoteDisconnected: Remote end closed connection without re… | 7 |

Website judged against the listing:

| site_match | places |
| --- | --- |
| yes | 1948 |
| no | 1093 |
| likely | 295 |
| unclear | 166 |
| (not extracted) | 150 |

Evidence check (items whose quote was not found on the page are dropped):

| key | items |
| --- | --- |
| gathering_locations_dropped | 164.0 |
| gathering_locations_ok | 1942.0 |
| mailing_dropped | 45.0 |
| services_dropped | 434.0 |
| services_ok | 6064.0 |
| shares_space_with_ok | 110.0 |

## Cross-checks across sources

Four sources describe the same places independently: Overture listings, tax-lot records (building class and owner), OpenStreetMap religious buildings, and IRS registrations. IRS addresses are registered addresses (often an office, PO box or pastor's apartment), so they confirm *who* a listing is, not where it gathers.

### Duplicate listings or real sharing

Lots where two or more congregations seem to gather, as each merge rule is added:

| merge_keys | congregations | lots_with_2plus | congregations_on_those_lots |
| --- | --- | --- | --- |
| website or same name | 9084 | 1326 | 3105 |
| + phone | 8777 | 1126 | 2598 |
| + name match | 8647 | 1041 | 2383 |
| + IRS EIN | 8645 | 1040 | 2380 |

Evidence behind each "shared" flag after merging:

| shared_evidence | places | lots |
| --- | --- | --- |
| listings only | 1224 | 551 |
| two or more IRS congregations | 399 | 150 |
| website says so | 99 | 83 |

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
| Protestant and other Christian | 6043 | 2155 | 36.0 | 1495 | 48 |
| Unknown | 1723 | 430 | 25.0 | 264 | 27 |
| Jewish | 612 | 287 | 47.0 | 212 | 17 |
| Catholic | 547 | 136 | 25.0 | 87 | 33 |
| Muslim | 291 | 128 | 44.0 | 113 | 12 |
| Hindu | 118 | 49 | 42.0 | 38 | 2 |
| Buddhist | 102 | 51 | 50.0 | 46 | 17 |
| Orthodox Christian | 70 | 30 | 43.0 | 29 | 4 |
| Sikh | 16 | 6 | 38.0 | 6 | 1 |

IRS congregations that no Overture listing matched, by the lot of their registered address (listed in `v0/private/nyc_irs_only.csv`). Those registered on another body's religious lot, a school or a commercial lot are candidate renters and guests. Those at a house or apartment are mostly a pastor's or treasurer's address, not where people gather. PLUTO cuts owner names at about 21 characters, so some "owned by another body" lots are the congregation's own:

| lot_type | congregations | lot_has_an_overture_listing | registered_since_2010 |
| --- | --- | --- | --- |
| house or residential building | 2783 | 79 | 1073 |
| commercial lot | 1755 | 308 | 667 |
| religious lot owned by another body | 1124 | 629 | 308 |
| other lot | 888 | 111 | 397 |
| apartment | 664 | 17 | 356 |
| PO box | 480 | 0 | 98 |
| religious lot it owns | 440 | 191 | 101 |
| school lot | 176 | 66 | 48 |
| address not placed | 125 | 0 | 49 |

### Agreement at the lot level

Lots named by each source. Worship lot = building class M1/M9, or a religious owner with institutional use (the step 3 definition).

| overture | worship_lot | osm_building | irs | lots |
| --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 1 | 5251 |
| 1 | 0 | 0 | 0 | 2817 |
| 0 | 1 | 0 | 0 | 1245 |
| 1 | 1 | 0 | 1 | 1064 |
| 1 | 0 | 0 | 1 | 1031 |
| 1 | 1 | 0 | 0 | 971 |
| 1 | 1 | 1 | 0 | 713 |
| 1 | 1 | 1 | 1 | 706 |
| 0 | 1 | 0 | 1 | 406 |
| 0 | 1 | 1 | 0 | 310 |
| 0 | 0 | 1 | 0 | 168 |
| 1 | 0 | 1 | 0 | 85 |

Capture-recapture (Chapman). The lists are not independent and IRS keeps closed churches on file, so these are rough indications, not counts:

| pair | list_1 | list_2 | in_both | estimated_total |
| --- | --- | --- | --- | --- |
| Congregations: Overture x IRS | 8645 | 11100 | 2894 | 33152 |
| Lots: Overture x OSM buildings | 7441 | 2113 | 1558 | 10090 |

## Recall check: worship lots with no Overture place

| why | borough | lots | likely_misses |
| --- | --- | --- | --- |
| M1/M9 building class | Bronx | 717 | 53 |
| M1/M9 building class | Brooklyn | 1876 | 404 |
| M1/M9 building class | Manhattan | 699 | 56 |
| M1/M9 building class | Queens | 1301 | 138 |
| M1/M9 building class | Staten Island | 224 | 41 |
| religious owner, institutional use | Bronx | 77 | 27 |
| religious owner, institutional use | Brooklyn | 261 | 123 |
| religious owner, institutional use | Manhattan | 116 | 23 |
| religious owner, institutional use | Queens | 151 | 56 |
| religious owner, institutional use | Staten Island | 53 | 20 |

The likely misses, with owner and address, are in `v0/private/nyc_recall_misses.csv`.

## 50 random rows for checking

Drawn with seed 20261122. They name places and addresses, so they are in `v0/private/check50.md` and `v0/private/nyc_check50.csv` (with evidence quotes and URLs), which are not committed.

## Known gaps in this run

- The cloud session reaches websites only over HTTPS; sites with no HTTPS show as connection or TLS errors and would load from a normal network.
- Version 0 reads static HTML only: no JavaScript rendering, PDFs or social media.
- Listings on one lot count as one congregation when they share a website, a phone number, a matching name or an IRS registration. Two names for one body with none of these in common still show as "shared"; the evidence column says how strong each flag is.
- Places with no website (about a third) can only be judged at their listing lot.
