# Version 0 report: San Francisco, CA

Run 2026-11-24. 867 Overture places in the seven worship categories. Colocation is judged at the lot where each congregation gathers: the address its own website gives for services when we could place it, otherwise its listing. Extraction used Claude Haiku 5.5 on 344 sites ($0.49).

## From listing to gathering place

| stage | places | share |
| --- | --- | --- |
| Places | 867 | 100% |
| With any website or social link | 630 | 73% |
| With a fetchable website (not social media) | 609 | 70% |
| Homepage fetched | 399 | 46% |
| Website confirmed as this congregation's (yes or likely) | 275 | 32% |
| Weekly main services found, with evidence | 211 | 24% |
| Gathering place from website, placed on a lot | 218 | 25% |
| ... on a different lot than the listing | 36 | 4% |

## Colocation by tradition

| tradition | school | shared | commercial | single-use | unknown |
| --- | --- | --- | --- | --- | --- |
| Buddhist | 0 | 5 | 11 | 18 | 9 |
| Catholic | 2 | 11 | 3 | 34 | 13 |
| Hindu | 0 | 1 | 2 | 1 | 0 |
| Jewish | 0 | 5 | 7 | 8 | 4 |
| Muslim | 0 | 4 | 1 | 4 | 1 |
| Orthodox Christian | 4 | 4 | 0 | 7 | 0 |
| Protestant and other Christian | 26 | 140 | 82 | 222 | 94 |
| Sikh | 0 | 0 | 1 | 0 | 0 |
| Unknown | 6 | 26 | 35 | 29 | 47 |

Colocation by where the address came from:

| address_basis | school | shared | commercial | single-use | unknown |
| --- | --- | --- | --- | --- | --- |
| listing | 22 | 132 | 125 | 224 | 146 |
| website | 16 | 64 | 17 | 99 | 22 |

Of the school flags, 15 are a private school on a religious-owned lot: most likely the congregation's own school, not a rental. The full rules split these out as "own school on campus".

## Weekly main services, where found

| tradition | places_with_schedule | mean_main | median_main | pct_two_or_more | mean_all_weekly |
| --- | --- | --- | --- | --- | --- |
| Protestant and other Christian | 162 | 1.5 | 1.0 | 35.0 | 2.4 |
| Catholic | 29 | 3.5 | 4.0 | 83.0 | 8.6 |
| Jewish | 7 | 1.6 | 2.0 | 57.0 | 2.9 |
| Orthodox Christian | 6 | 1.0 | 1.0 | 0.0 | 2.0 |
| Buddhist | 4 | 1.0 | 1.0 | 0.0 | 3.3 |
| Unknown | 2 | 1.0 | 1.0 | 0.0 | 4.5 |
| Muslim | 1 | 1.0 | 1.0 | 0.0 | 1.0 |

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
| http_526 | 1 |
| http_409 | 1 |
| http_522 | 1 |

Website judged against the listing:

| site_match | places |
| --- | --- |
| yes | 245 |
| no | 98 |
| likely | 30 |
| unclear | 14 |
| (not extracted) | 12 |

Evidence check (items whose quote was not found on the page are dropped):

| key | items |
| --- | --- |
| gathering_locations_dropped | 24.0 |
| gathering_locations_ok | 231.0 |
| mailing_dropped | 4.0 |
| services_dropped | 47.0 |
| services_ok | 674.0 |
| shares_space_with_ok | 17.0 |

## Cross-checks across sources

Four sources describe the same places independently: Overture listings, tax-lot records (building class and owner), OpenStreetMap religious buildings, and IRS registrations. IRS addresses are registered addresses (often an office, PO box or pastor's apartment), so they confirm *who* a listing is, not where it gathers.

### Duplicate listings or real sharing

Lots where two or more congregations seem to gather, as each merge rule is added:

| merge_keys | congregations | lots_with_2plus | congregations_on_those_lots |
| --- | --- | --- | --- |
| website or same name | 809 | 140 | 312 |
| + phone | 771 | 113 | 247 |
| + name match | 767 | 109 | 239 |
| + IRS EIN | 767 | 109 | 239 |

Evidence behind each "shared" flag after merging:

| shared_evidence | places | lots |
| --- | --- | --- |
| listings only | 140 | 65 |
| two or more IRS congregations | 37 | 15 |
| website says so | 19 | 16 |

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
| Protestant and other Christian | 564 | 183 | 32.0 | 135 | 12 |
| Unknown | 143 | 29 | 20.0 | 18 | 4 |
| Catholic | 63 | 35 | 56.0 | 26 | 4 |
| Buddhist | 43 | 20 | 47.0 | 16 | 3 |
| Jewish | 24 | 12 | 50.0 | 10 | 0 |
| Orthodox Christian | 15 | 8 | 53.0 | 8 | 1 |
| Muslim | 10 | 3 | 30.0 | 2 | 1 |
| Hindu | 4 | 1 | 25.0 | 1 | 1 |
| Sikh | 1 | 0 | 0.0 | 0 | 0 |

IRS congregations that no Overture listing matched, by the lot of their registered address (listed in `v0/sf/private/sf_irs_only.csv`). Those registered on another body's religious lot, a school or a commercial lot are candidate renters and guests. Those at a house or apartment are mostly a pastor's or treasurer's address, not where people gather. PLUTO cuts owner names at about 21 characters, so some "owned by another body" lots are the congregation's own:

| lot_type | congregations | lot_has_an_overture_listing | registered_since_2010 |
| --- | --- | --- | --- |
| house or residential building | 152 | 8 | 40 |
| religious lot owned by another body | 97 | 72 | 15 |
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
| 1 | 0 | 0 | 0 | 223 |
| 0 | 1 | 0 | 0 | 137 |
| 1 | 1 | 1 | 1 | 86 |
| 1 | 0 | 0 | 1 | 82 |
| 1 | 1 | 0 | 0 | 78 |
| 1 | 1 | 1 | 0 | 76 |
| 1 | 1 | 0 | 1 | 72 |
| 0 | 1 | 1 | 0 | 49 |
| 0 | 0 | 1 | 0 | 37 |
| 1 | 0 | 1 | 0 | 18 |
| 1 | 0 | 1 | 1 | 12 |

Capture-recapture (Chapman). The lists are not independent and IRS keeps closed churches on file, so these are rough indications, not counts:

| pair | list_1 | list_2 | in_both | estimated_total |
| --- | --- | --- | --- | --- |
| Congregations: Overture x IRS | 767 | 629 | 240 | 2007 |
| Lots: Overture x OSM buildings | 647 | 286 | 192 | 963 |

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
