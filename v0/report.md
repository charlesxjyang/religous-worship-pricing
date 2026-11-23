# Version 0 report: New York City

Run 2026-11-23. 9,522 Overture places in the seven worship categories. Colocation is judged at the lot where each congregation gathers: the address its own website gives for services when we could place it, otherwise its listing. Extraction used Claude Haiku 5.5 on 0 sites ($0.00).

**Extraction has not run yet** (no API key in this session), so every row below uses the listing lot, and service counts are empty. Rerun steps 4b–6 once `WORSHIP_ANTHROPIC_API_KEY` is set.

## From listing to gathering place

| stage | places | share |
| --- | --- | --- |
| Places | 9522 | 100% |
| With any website or social link | 6275 | 66% |
| With a fetchable website (not social media) | 5965 | 63% |
| Homepage fetched | 3556 | 37% |
| Website confirmed as this congregation's (yes or likely) | 0 | 0% |
| Weekly main services found, with evidence | 0 | 0% |
| Gathering place from website, placed on a lot | 0 | 0% |
| ... on a different lot than the listing | 0 | 0% |

## Colocation by tradition

| tradition | school | shared | commercial | single-use | unknown |
| --- | --- | --- | --- | --- | --- |
| Buddhist | 1 | 14 | 23 | 44 | 17 |
| Catholic | 91 | 82 | 10 | 252 | 43 |
| Hindu | 0 | 11 | 24 | 40 | 40 |
| Jewish | 31 | 80 | 66 | 280 | 107 |
| Muslim | 9 | 33 | 66 | 117 | 50 |
| Orthodox Christian | 1 | 0 | 2 | 0 | 0 |
| Protestant and other Christian | 178 | 1582 | 1088 | 2144 | 972 |
| Sikh | 0 | 5 | 2 | 7 | 1 |
| Unknown | 86 | 600 | 476 | 335 | 512 |

Colocation by where the address came from:

| address_basis | school | shared | commercial | single-use | unknown |
| --- | --- | --- | --- | --- | --- |
| listing | 397 | 2407 | 1757 | 3219 | 1742 |

Of the school flags, 163 are a private school on a religious-owned lot: most likely the congregation's own school, not a rental. The full rules split these out as "own school on campus".

## Weekly main services, where found

| tradition | places_with_schedule | mean_main | median_main | pct_two_or_more | mean_all_weekly |
| --- | --- | --- | --- | --- | --- |

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

## Cross-checks across sources

Four sources describe the same places independently: Overture listings, tax-lot records (building class and owner), OpenStreetMap religious buildings, and IRS registrations. IRS addresses are registered addresses (often an office, PO box or pastor's apartment), so they confirm *who* a listing is, not where it gathers.

### Duplicate listings or real sharing

Lots where two or more congregations seem to gather, as each merge rule is added:

| merge_keys | congregations | lots_with_2plus | congregations_on_those_lots |
| --- | --- | --- | --- |
| website or same name | 9397 | 1282 | 3024 |
| + phone | 9130 | 1113 | 2588 |
| + name match | 9029 | 1047 | 2421 |
| + IRS EIN | 9027 | 1046 | 2418 |

Evidence behind each "shared" flag after merging:

| shared_evidence | places | lots |
| --- | --- | --- |
| listings only | 1876 | 796 |
| two or more IRS congregations | 531 | 193 |

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
| Protestant and other Christian | 5964 | 2068 | 35.0 | 1269 | 50 |
| Unknown | 2009 | 502 | 25.0 | 258 | 36 |
| Jewish | 564 | 261 | 46.0 | 178 | 14 |
| Catholic | 478 | 122 | 26.0 | 64 | 32 |
| Muslim | 275 | 118 | 43.0 | 88 | 11 |
| Hindu | 115 | 46 | 40.0 | 31 | 1 |
| Buddhist | 99 | 47 | 47.0 | 36 | 16 |
| Sikh | 15 | 5 | 33.0 | 5 | 1 |
| Orthodox Christian | 3 | 2 | 67.0 | 2 | 0 |

IRS congregations that no Overture listing matched, by the lot of their registered address (listed in `v0/private/nyc_irs_only.csv`). Those registered on another body's religious lot, a school or a commercial lot are candidate renters and guests. Those at a house or apartment are mostly a pastor's or treasurer's address, not where people gather. PLUTO cuts owner names at about 21 characters, so some "owned by another body" lots are the congregation's own:

| lot_type | congregations | lot_has_an_overture_listing | registered_since_2010 |
| --- | --- | --- | --- |
| house or residential building | 2790 | 59 | 1074 |
| commercial lot | 1770 | 284 | 671 |
| religious lot owned by another body | 1131 | 574 | 309 |
| other lot | 899 | 51 | 398 |
| apartment | 664 | 16 | 355 |
| PO box | 480 | 0 | 98 |
| religious lot it owns | 468 | 183 | 103 |
| school lot | 177 | 64 | 48 |
| address not placed | 125 | 0 | 49 |

### Agreement at the lot level

Lots named by each source. Worship lot = building class M1/M9, or a religious owner with institutional use (the step 3 definition).

| overture | worship_lot | osm_building | irs | lots |
| --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 1 | 5448 |
| 1 | 0 | 0 | 0 | 3323 |
| 0 | 1 | 0 | 0 | 1265 |
| 1 | 1 | 0 | 1 | 955 |
| 1 | 1 | 0 | 0 | 941 |
| 1 | 0 | 0 | 1 | 838 |
| 1 | 1 | 1 | 0 | 814 |
| 1 | 1 | 1 | 1 | 691 |
| 0 | 1 | 0 | 1 | 511 |
| 0 | 1 | 1 | 0 | 207 |
| 0 | 0 | 1 | 0 | 168 |
| 1 | 0 | 1 | 0 | 87 |

Capture-recapture (Chapman). The lists are not independent and IRS keeps closed churches on file, so these are rough indications, not counts:

| pair | list_1 | list_2 | in_both | estimated_total |
| --- | --- | --- | --- | --- |
| Congregations: Overture x IRS | 9027 | 11100 | 2883 | 34749 |
| Lots: Overture x OSM buildings | 7697 | 2113 | 1640 | 9916 |

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
