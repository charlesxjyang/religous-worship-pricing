# Version 0 report: Houston, TX

Run 2026-11-24. 5,082 Overture places in the seven worship categories. Colocation is judged at the lot where each congregation gathers: the address its own website gives for services when we could place it, otherwise its listing. Extraction used Claude Haiku 5.5 on 0 sites ($0.00).

**Extraction has not run yet** (no API key in this session), so every row below uses the listing lot, and service counts are empty. Rerun steps 4b–6 once `WORSHIP_ANTHROPIC_API_KEY` is set.

## From listing to gathering place

| stage | places | share |
| --- | --- | --- |
| Places | 5082 | 100% |
| With any website or social link | 3234 | 64% |
| With a fetchable website (not social media) | 3052 | 60% |
| Homepage fetched | 1805 | 36% |
| Website confirmed as this congregation's (yes or likely) | 0 | 0% |
| Weekly main services found, with evidence | 0 | 0% |
| Gathering place from website, placed on a lot | 0 | 0% |
| ... on a different lot than the listing | 0 | 0% |

## Colocation by tradition

| tradition | school | shared | commercial | single-use | unknown |
| --- | --- | --- | --- | --- | --- |
| Buddhist | 0 | 3 | 7 | 13 | 7 |
| Catholic | 16 | 20 | 2 | 45 | 18 |
| Hindu | 0 | 5 | 2 | 7 | 9 |
| Jewish | 2 | 2 | 3 | 12 | 5 |
| Muslim | 2 | 10 | 8 | 20 | 22 |
| Protestant and other Christian | 87 | 879 | 499 | 1274 | 1040 |
| Sikh | 0 | 0 | 0 | 0 | 1 |
| Unknown | 34 | 316 | 208 | 164 | 340 |

Colocation by where the address came from:

| address_basis | school | shared | commercial | single-use | unknown |
| --- | --- | --- | --- | --- | --- |
| listing | 141 | 1235 | 729 | 1535 | 1442 |

Of the school flags, 84 are a private school on a religious-owned lot: most likely the congregation's own school, not a rental. The full rules split these out as "own school on campus".

## Weekly main services, where found

| tradition | places_with_schedule | mean_main | median_main | pct_two_or_more | mean_all_weekly |
| --- | --- | --- | --- | --- | --- |

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
| http_410 | 2 |

## Cross-checks across sources

Four sources describe the same places independently: Overture listings, tax-lot records (building class and owner), OpenStreetMap religious buildings, and IRS registrations. IRS addresses are registered addresses (often an office, PO box or pastor's apartment), so they confirm *who* a listing is, not where it gathers.

### Duplicate listings or real sharing

Lots where two or more congregations seem to gather, as each merge rule is added:

| merge_keys | congregations | lots_with_2plus | congregations_on_those_lots |
| --- | --- | --- | --- |
| website or same name | 4973 | 718 | 2605 |
| + phone | 4766 | 625 | 2305 |
| + name match | 4408 | 593 | 1915 |
| + IRS EIN | 4404 | 593 | 1911 |

Evidence behind each "shared" flag after merging:

| shared_evidence | places | lots |
| --- | --- | --- |
| listings only | 1070 | 300 |
| two or more IRS congregations | 165 | 51 |

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
| Protestant and other Christian | 3779 | 985 | 26.0 | 587 | 25 |
| Unknown | 1062 | 153 | 14.0 | 84 | 8 |
| Catholic | 101 | 13 | 13.0 | 9 | 5 |
| Muslim | 62 | 12 | 19.0 | 7 | 3 |
| Buddhist | 30 | 11 | 37.0 | 8 | 4 |
| Jewish | 24 | 14 | 58.0 | 12 | 2 |
| Hindu | 23 | 4 | 17.0 | 2 | 1 |
| Sikh | 1 | 1 | 100.0 | 0 | 0 |

IRS congregations that no Overture listing matched, by the lot of their registered address (listed in `v0/houston/private/houston_irs_only.csv`). Those registered on another body's religious lot, a school or a commercial lot are candidate renters and guests. Those at a house or apartment are mostly a pastor's or treasurer's address, not where people gather. PLUTO cuts owner names at about 21 characters, so some "owned by another body" lots are the congregation's own:

| lot_type | congregations | lot_has_an_overture_listing | registered_since_2010 |
| --- | --- | --- | --- |
| address not placed | 801 | 0 | 366 |
| house or residential building | 491 | 19 | 237 |
| PO box | 417 | 0 | 187 |
| commercial lot | 177 | 63 | 95 |
| other lot | 157 | 54 | 58 |
| religious lot owned by another body | 151 | 123 | 40 |
| religious lot it owns | 92 | 57 | 30 |
| apartment | 73 | 3 | 44 |
| school lot | 21 | 13 | 4 |

### Agreement at the lot level

Lots named by each source. Worship lot = building class M1/M9, or a religious owner with institutional use (the step 3 definition).

| overture | worship_lot | osm_building | irs | lots |
| --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 0 | 1660 |
| 0 | 0 | 0 | 1 | 881 |
| 1 | 0 | 0 | 1 | 550 |
| 0 | 1 | 0 | 0 | 383 |
| 1 | 1 | 0 | 0 | 366 |
| 1 | 1 | 0 | 1 | 227 |
| 1 | 0 | 1 | 0 | 116 |
| 0 | 0 | 1 | 0 | 93 |
| 1 | 1 | 1 | 0 | 84 |
| 1 | 0 | 1 | 1 | 66 |
| 1 | 1 | 1 | 1 | 46 |
| 0 | 1 | 1 | 0 | 27 |

Capture-recapture (Chapman). The lists are not independent and IRS keeps closed churches on file, so these are rough indications, not counts:

| pair | list_1 | list_2 | in_both | estimated_total |
| --- | --- | --- | --- | --- |
| Congregations: Overture x IRS | 4404 | 3315 | 1051 | 13884 |
| Lots: Overture x OSM buildings | 3115 | 439 | 312 | 4379 |

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
