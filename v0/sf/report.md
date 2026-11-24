# Version 0 report: San Francisco, CA

Run 2026-11-24. 867 Overture places in the seven worship categories. Colocation is judged at the lot where each congregation gathers: the address its own website gives for services when we could place it, otherwise its listing. Extraction used Claude Haiku 5.5 on 0 sites ($0.00).

**Extraction has not run yet** (no API key in this session), so every row below uses the listing lot, and service counts are empty. Rerun steps 4b–6 once `WORSHIP_ANTHROPIC_API_KEY` is set.

## From listing to gathering place

| stage | places | share |
| --- | --- | --- |
| Places | 867 | 100% |
| With any website or social link | 630 | 73% |
| With a fetchable website (not social media) | 609 | 70% |
| Homepage fetched | 399 | 46% |
| Website confirmed as this congregation's (yes or likely) | 0 | 0% |
| Weekly main services found, with evidence | 0 | 0% |
| Gathering place from website, placed on a lot | 0 | 0% |
| ... on a different lot than the listing | 0 | 0% |

## Colocation by tradition

| tradition | school | shared | commercial | single-use | unknown |
| --- | --- | --- | --- | --- | --- |
| Buddhist | 0 | 4 | 9 | 16 | 9 |
| Catholic | 2 | 6 | 4 | 34 | 12 |
| Hindu | 0 | 1 | 2 | 1 | 0 |
| Jewish | 0 | 4 | 7 | 8 | 4 |
| Muslim | 0 | 4 | 1 | 4 | 1 |
| Orthodox Christian | 0 | 1 | 0 | 0 | 0 |
| Protestant and other Christian | 29 | 130 | 82 | 224 | 98 |
| Sikh | 0 | 0 | 1 | 0 | 0 |
| Unknown | 6 | 36 | 38 | 36 | 53 |

Colocation by where the address came from:

| address_basis | school | shared | commercial | single-use | unknown |
| --- | --- | --- | --- | --- | --- |
| listing | 37 | 186 | 144 | 323 | 177 |

Of the school flags, 16 are a private school on a religious-owned lot: most likely the congregation's own school, not a rental. The full rules split these out as "own school on campus".

## Weekly main services, where found

| tradition | places_with_schedule | mean_main | median_main | pct_two_or_more | mean_all_weekly |
| --- | --- | --- | --- | --- | --- |

## Websites

| homepage | places |
| --- | --- |
| ok | 399 |
| (no website) | 258 |
| dead domain (proxy could not connect) | 61 |
| connection or TLS error | 53 |
| robots_disallowed | 32 |
| http_403 | 23 |
| http_404 | 18 |
| empty | 16 |
| http_429 | 3 |
| http_522 | 1 |
| http_409 | 1 |
| http_526 | 1 |

## Cross-checks across sources

Four sources describe the same places independently: Overture listings, tax-lot records (building class and owner), OpenStreetMap religious buildings, and IRS registrations. IRS addresses are registered addresses (often an office, PO box or pastor's apartment), so they confirm *who* a listing is, not where it gathers.

### Duplicate listings or real sharing

Lots where two or more congregations seem to gather, as each merge rule is added:

| merge_keys | congregations | lots_with_2plus | congregations_on_those_lots |
| --- | --- | --- | --- |
| website or same name | 846 | 139 | 318 |
| + phone | 807 | 113 | 253 |
| + name match | 804 | 111 | 248 |
| + IRS EIN | 804 | 111 | 248 |

Evidence behind each "shared" flag after merging:

| shared_evidence | places | lots |
| --- | --- | --- |
| listings only | 143 | 62 |
| two or more IRS congregations | 43 | 17 |

### IRS registrations

| kind | orgs | po_box | apartment_or_suite | placed_on_a_lot |
| --- | --- | --- | --- | --- |
| congregation | 629 | 44 | 58 | 570 |
| support | 107 | 6 | 22 | 96 |
| other | 63 | 8 | 15 | 53 |
| school | 15 | 0 | 5 | 15 |

Overture listings matched to an IRS registration (same lot, or a unique name match in the same ZIP code):

| tradition | places | matched | pct_matched | on_same_lot | matched_school_or_support |
| --- | --- | --- | --- | --- | --- |
| Protestant and other Christian | 563 | 181 | 32.0 | 131 | 12 |
| Unknown | 169 | 35 | 21.0 | 23 | 5 |
| Catholic | 58 | 35 | 60.0 | 26 | 4 |
| Buddhist | 38 | 19 | 50.0 | 15 | 2 |
| Jewish | 23 | 11 | 48.0 | 9 | 0 |
| Muslim | 10 | 3 | 30.0 | 2 | 1 |
| Hindu | 4 | 1 | 25.0 | 1 | 1 |
| Orthodox Christian | 1 | 1 | 100.0 | 1 | 0 |
| Sikh | 1 | 0 | 0.0 | 0 | 0 |

IRS congregations that no Overture listing matched, by the lot of their registered address (listed in `v0/sf/private/sf_irs_only.csv`). Those registered on another body's religious lot, a school or a commercial lot are candidate renters and guests. Those at a house or apartment are mostly a pastor's or treasurer's address, not where people gather. PLUTO cuts owner names at about 21 characters, so some "owned by another body" lots are the congregation's own:

| lot_type | congregations | lot_has_an_overture_listing | registered_since_2010 |
| --- | --- | --- | --- |
| house or residential building | 152 | 8 | 40 |
| religious lot owned by another body | 98 | 73 | 15 |
| commercial lot | 60 | 15 | 23 |
| PO box | 39 | 0 | 8 |
| apartment | 26 | 0 | 12 |
| other lot | 17 | 4 | 3 |
| address not placed | 9 | 0 | 3 |
| school lot | 8 | 5 | 2 |

### Agreement at the lot level

Lots named by each source. Worship lot = building class M1/M9, or a religious owner with institutional use (the step 3 definition).

| overture | worship_lot | osm_building | irs | lots |
| --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 1 | 255 |
| 1 | 0 | 0 | 0 | 241 |
| 0 | 1 | 0 | 0 | 136 |
| 1 | 1 | 1 | 1 | 86 |
| 1 | 0 | 0 | 1 | 82 |
| 1 | 1 | 0 | 0 | 79 |
| 1 | 1 | 1 | 0 | 79 |
| 1 | 1 | 0 | 1 | 72 |
| 0 | 1 | 1 | 0 | 46 |
| 0 | 0 | 1 | 0 | 35 |
| 1 | 0 | 1 | 0 | 20 |
| 1 | 0 | 1 | 1 | 12 |

Capture-recapture (Chapman). The lists are not independent and IRS keeps closed churches on file, so these are rough indications, not counts:

| pair | list_1 | list_2 | in_both | estimated_total |
| --- | --- | --- | --- | --- |
| Congregations: Overture x IRS | 804 | 629 | 246 | 2052 |
| Lots: Overture x OSM buildings | 671 | 286 | 197 | 973 |

## Recall check: worship lots with no Overture place

| why | borough | lots | likely_misses |
| --- | --- | --- | --- |
| M1/M9 building class | District 1 | 39 | 6 |
| M1/M9 building class | District 10 | 72 | 18 |
| M1/M9 building class | District 11 | 47 | 5 |
| M1/M9 building class | District 2 | 43 | 3 |
| M1/M9 building class | District 3 | 35 | 2 |
| M1/M9 building class | District 4 | 45 | 7 |
| M1/M9 building class | District 5 | 60 | 6 |
| M1/M9 building class | District 6 | 9 | 4 |
| M1/M9 building class | District 7 | 56 | 9 |
| M1/M9 building class | District 8 | 46 | 11 |
| M1/M9 building class | District 9 | 59 | 9 |

The likely misses, with owner and address, are in `v0/sf/private/sf_recall_misses.csv`.

## 50 random rows for checking

Drawn with seed 20261122. They name places and addresses, so they are in `v0/sf/private/check50.md` and `v0/sf/private/sf_check50.csv` (with evidence quotes and URLs), which are not committed.

## Known gaps in this run

- The cloud session reaches websites only over HTTPS; sites with no HTTPS show as connection or TLS errors and would load from a normal network.
- Version 0 reads static HTML only: no JavaScript rendering, PDFs or social media.
- Listings on one lot count as one congregation when they share a website, a phone number, a matching name or an IRS registration. Two names for one body with none of these in common still show as "shared"; the evidence column says how strong each flag is.
- Places with no website (about a third) can only be judged at their listing lot.
