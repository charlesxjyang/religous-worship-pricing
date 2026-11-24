# Version 0 report: Houston, TX

Run 2026-11-24. 5,082 Overture places in the seven worship categories. Colocation is judged at the lot where each congregation gathers: the address its own website gives for services when we could place it, otherwise its listing. Extraction used Claude Haiku 5.5 on 1,507 sites ($1.91).

## From listing to gathering place

| stage | places | share |
| --- | --- | --- |
| Places | 5082 | 100% |
| With any website or social link | 3234 | 64% |
| With a fetchable website (not social media) | 3052 | 60% |
| Homepage fetched | 1805 | 36% |
| Website confirmed as this congregation's (yes or likely) | 1176 | 23% |
| Weekly main services found, with evidence | 887 | 17% |
| Gathering place from website, placed on a lot | 748 | 15% |
| ... on a different lot than the listing | 148 | 3% |

## Colocation by tradition

| tradition | school | shared | commercial | single-use | unknown |
| --- | --- | --- | --- | --- | --- |
| Buddhist | 0 | 3 | 6 | 15 | 6 |
| Catholic | 20 | 21 | 2 | 50 | 22 |
| Hindu | 0 | 5 | 2 | 8 | 10 |
| Jewish | 2 | 3 | 3 | 13 | 6 |
| Muslim | 2 | 12 | 9 | 22 | 20 |
| Orthodox Christian | 1 | 2 | 0 | 6 | 1 |
| Protestant and other Christian | 101 | 913 | 554 | 1294 | 1046 |
| Sikh | 0 | 0 | 0 | 0 | 1 |
| Unknown | 25 | 260 | 178 | 133 | 305 |

Colocation by where the address came from:

| address_basis | school | shared | commercial | single-use | unknown |
| --- | --- | --- | --- | --- | --- |
| listing | 109 | 1060 | 667 | 1185 | 1313 |
| website | 42 | 159 | 87 | 356 | 104 |

Of the school flags, 88 are a private school on a religious-owned lot: most likely the congregation's own school, not a rental. The full rules split these out as "own school on campus".

## Weekly main services, where found

| tradition | places_with_schedule | mean_main | median_main | pct_two_or_more | mean_all_weekly |
| --- | --- | --- | --- | --- | --- |
| Protestant and other Christian | 812 | 1.3 | 1.0 | 25.0 | 2.1 |
| Catholic | 35 | 4.3 | 4.0 | 89.0 | 9.5 |
| Jewish | 12 | 1.7 | 1.5 | 50.0 | 1.8 |
| Muslim | 10 | 1.3 | 1.0 | 30.0 | 7.2 |
| Orthodox Christian | 8 | 1.1 | 1.0 | 13.0 | 2.0 |
| Buddhist | 4 | 1.0 | 1.0 | 0.0 | 1.0 |
| Hindu | 4 | 1.0 | 1.0 | 0.0 | 22.5 |
| Unknown | 2 | 1.0 | 1.0 | 0.0 | 1.5 |

## Websites

| homepage | places |
| --- | --- |
| (no website) | 2030 |
| ok | 1805 |
| dead domain (proxy could not connect) | 415 |
| connection or TLS error | 308 |
| robots_disallowed | 236 |
| http_403 | 109 |
| http_404 | 82 |
| empty | 70 |
| http_522 | 6 |
| http_500 | 5 |
| http_503 | 4 |
| http_429 | 2 |

Website judged against the listing:

| site_match | places |
| --- | --- |
| yes | 1058 |
| no | 449 |
| likely | 118 |
| unclear | 96 |
| (not extracted) | 84 |

Evidence check (items whose quote was not found on the page are dropped):

| key | items |
| --- | --- |
| gathering_locations_dropped | 90.0 |
| gathering_locations_ok | 1012.0 |
| mailing_dropped | 12.0 |
| services_dropped | 107.0 |
| services_ok | 2370.0 |
| shares_space_with_ok | 27.0 |

## Cross-checks across sources

Four sources describe the same places independently: Overture listings, tax-lot records (building class and owner), OpenStreetMap religious buildings, and IRS registrations. IRS addresses are registered addresses (often an office, PO box or pastor's apartment), so they confirm *who* a listing is, not where it gathers.

### Duplicate listings or real sharing

Lots where two or more congregations seem to gather, as each merge rule is added:

| merge_keys | congregations | lots_with_2plus | congregations_on_those_lots |
| --- | --- | --- | --- |
| website or same name | 4828 | 684 | 2496 |
| + phone | 4630 | 597 | 2211 |
| + name match | 4279 | 562 | 1825 |
| + IRS EIN | 4277 | 562 | 1823 |

Evidence behind each "shared" flag after merging:

| shared_evidence | places | lots |
| --- | --- | --- |
| listings only | 1038 | 282 |
| two or more IRS congregations | 157 | 49 |
| website says so | 24 | 19 |

### IRS registrations

| kind | orgs | po_box | apartment_or_suite | placed_on_a_lot |
| --- | --- | --- | --- | --- |
| congregation | 3315 | 417 | 431 | 1983 |
| other | 342 | 23 | 73 | 214 |
| support | 265 | 24 | 58 | 174 |
| school | 82 | 3 | 6 | 62 |

Overture listings matched to an IRS registration (same lot, or a unique name match in the same ZIP code):

| tradition | places | matched | pct_matched | on_same_lot | matched_school_or_support |
| --- | --- | --- | --- | --- | --- |
| Protestant and other Christian | 3908 | 1009 | 26.0 | 612 | 25 |
| Unknown | 901 | 133 | 15.0 | 78 | 6 |
| Catholic | 115 | 18 | 16.0 | 14 | 6 |
| Muslim | 65 | 12 | 18.0 | 7 | 3 |
| Buddhist | 30 | 11 | 37.0 | 8 | 4 |
| Jewish | 27 | 14 | 52.0 | 12 | 2 |
| Hindu | 25 | 5 | 20.0 | 3 | 2 |
| Orthodox Christian | 10 | 5 | 50.0 | 3 | 0 |
| Sikh | 1 | 1 | 100.0 | 0 | 0 |

IRS congregations that no Overture listing matched, by the lot of their registered address (listed in `v0/houston/private/houston_irs_only.csv`). Those registered on another body's religious lot, a school or a commercial lot are candidate renters and guests. Those at a house or apartment are mostly a pastor's or treasurer's address, not where people gather. PLUTO cuts owner names at about 21 characters, so some "owned by another body" lots are the congregation's own:

| lot_type | congregations | lot_has_an_overture_listing | registered_since_2010 |
| --- | --- | --- | --- |
| address not placed | 802 | 0 | 366 |
| house or residential building | 490 | 19 | 237 |
| PO box | 417 | 0 | 187 |
| commercial lot | 176 | 63 | 94 |
| other lot | 156 | 59 | 58 |
| religious lot owned by another body | 152 | 125 | 40 |
| religious lot it owns | 89 | 58 | 29 |
| apartment | 73 | 3 | 44 |
| school lot | 21 | 13 | 4 |

### Agreement at the lot level

Lots named by each source. Worship lot = building class M1/M9, or a religious owner with institutional use (the step 3 definition).

| overture | worship_lot | osm_building | irs | lots |
| --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 0 | 1643 |
| 0 | 0 | 0 | 1 | 875 |
| 1 | 0 | 0 | 1 | 556 |
| 0 | 1 | 0 | 0 | 393 |
| 1 | 1 | 0 | 0 | 356 |
| 1 | 1 | 0 | 1 | 221 |
| 1 | 0 | 1 | 0 | 108 |
| 0 | 0 | 1 | 0 | 101 |
| 1 | 1 | 1 | 0 | 84 |
| 1 | 0 | 1 | 1 | 67 |
| 1 | 1 | 1 | 1 | 45 |
| 0 | 1 | 1 | 0 | 27 |

Capture-recapture (Chapman). The lists are not independent and IRS keeps closed churches on file, so these are rough indications, not counts:

| pair | list_1 | list_2 | in_both | estimated_total |
| --- | --- | --- | --- | --- |
| Congregations: Overture x IRS | 4277 | 3315 | 1039 | 13639 |
| Lots: Overture x OSM buildings | 3080 | 439 | 304 | 4444 |

## Recall check: worship lots with no Overture place

| why | borough | lots | likely_misses |
| --- | --- | --- | --- |
| M1/M9 building class | District A | 51 | 10 |
| M1/M9 building class | District B | 282 | 45 |
| M1/M9 building class | District C | 56 | 4 |
| M1/M9 building class | District D | 185 | 27 |
| M1/M9 building class | District E | 37 | 1 |
| M1/M9 building class | District F | 47 | 8 |
| M1/M9 building class | District G | 16 | 2 |
| M1/M9 building class | District H | 165 | 28 |
| M1/M9 building class | District I | 99 | 19 |
| M1/M9 building class | District J | 27 | 5 |
| M1/M9 building class | District K | 99 | 24 |
| religious owner, institutional use | District A | 3 | 1 |
| religious owner, institutional use | District B | 17 | 4 |
| religious owner, institutional use | District C | 11 | 10 |
| religious owner, institutional use | District D | 17 | 9 |
| religious owner, institutional use | District E | 1 | 1 |
| religious owner, institutional use | District F | 2 | 0 |
| religious owner, institutional use | District G | 5 | 3 |
| religious owner, institutional use | District H | 6 | 2 |
| religious owner, institutional use | District I | 20 | 14 |
| religious owner, institutional use | District J | 3 | 1 |
| religious owner, institutional use | District K | 7 | 6 |

The likely misses, with owner and address, are in `v0/houston/private/houston_recall_misses.csv`.

## 50 random rows for checking

Drawn with seed 20261122. They name places and addresses, so they are in `v0/houston/private/check50.md` and `v0/houston/private/houston_check50.csv` (with evidence quotes and URLs), which are not committed.

## Known gaps in this run

- The cloud session reaches websites only over HTTPS; sites with no HTTPS show as connection or TLS errors and would load from a normal network.
- Version 0 reads static HTML only: no JavaScript rendering, PDFs or social media.
- Listings on one lot count as one congregation when they share a website, a phone number, a matching name or an IRS registration. Two names for one body with none of these in common still show as "shared"; the evidence column says how strong each flag is.
- Places with no website (about a third) can only be judged at their listing lot.
