# Version 0 report: Washington, DC

Run 2026-11-23. 1,300 Overture places in the seven worship categories. Colocation is judged at the lot where each congregation gathers: the address its own website gives for services when we could place it, otherwise its listing. Extraction used Claude Haiku 5.5 on 603 sites ($0.84).

## From listing to gathering place

| stage | places | share |
| --- | --- | --- |
| Places | 1300 | 100% |
| With any website or social link | 994 | 76% |
| With a fetchable website (not social media) | 961 | 74% |
| Homepage fetched | 666 | 51% |
| Website confirmed as this congregation's (yes or likely) | 418 | 32% |
| Weekly main services found, with evidence | 305 | 23% |
| Gathering place from website, placed on a lot | 327 | 25% |
| ... on a different lot than the listing | 57 | 4% |

## Colocation by tradition

| tradition | school | shared | commercial | single-use | unknown |
| --- | --- | --- | --- | --- | --- |
| Buddhist | 1 | 1 | 2 | 3 | 0 |
| Catholic | 10 | 37 | 4 | 26 | 11 |
| Hindu | 0 | 0 | 1 | 0 | 0 |
| Jewish | 0 | 5 | 0 | 11 | 3 |
| Muslim | 1 | 2 | 3 | 6 | 2 |
| Orthodox Christian | 0 | 0 | 0 | 6 | 0 |
| Protestant and other Christian | 29 | 295 | 75 | 406 | 145 |
| Sikh | 0 | 0 | 1 | 1 | 0 |
| Unknown | 13 | 74 | 34 | 41 | 51 |

Colocation by where the address came from:

| address_basis | school | shared | commercial | single-use | unknown |
| --- | --- | --- | --- | --- | --- |
| listing | 33 | 306 | 103 | 342 | 189 |
| website | 21 | 108 | 17 | 158 | 23 |

Of the school flags, 21 are a private school on a religious-owned lot: most likely the congregation's own school, not a rental. The full rules split these out as "own school on campus".

## Weekly main services, where found

| tradition | places_with_schedule | mean_main | median_main | pct_two_or_more | mean_all_weekly |
| --- | --- | --- | --- | --- | --- |
| Protestant and other Christian | 261 | 1.2 | 1.0 | 14.0 | 1.9 |
| Catholic | 25 | 3.5 | 4.0 | 76.0 | 10.9 |
| Jewish | 9 | 1.6 | 2.0 | 56.0 | 2.4 |
| Unknown | 5 | 1.2 | 1.0 | 20.0 | 2.0 |
| Orthodox Christian | 2 | 1.0 | 1.0 | 0.0 | 2.0 |
| Muslim | 2 | 1.0 | 1.0 | 0.0 | 1.0 |
| Sikh | 1 | 1.0 | 1.0 | 0.0 | 2.0 |

## Websites

| homepage | places |
| --- | --- |
| ok | 666 |
| (no website) | 339 |
| dead domain (proxy could not connect) | 110 |
| connection or TLS error | 65 |
| robots_disallowed | 56 |
| http_404 | 28 |
| http_403 | 19 |
| empty | 15 |
| http_301 | 1 |
| http_500 | 1 |

Website judged against the listing:

| site_match | places |
| --- | --- |
| yes | 376 |
| no | 207 |
| likely | 42 |
| unclear | 26 |
| (not extracted) | 15 |

Evidence check (items whose quote was not found on the page are dropped):

| key | items |
| --- | --- |
| gathering_locations_dropped | 25.0 |
| gathering_locations_ok | 354.0 |
| mailing_dropped | 8.0 |
| services_dropped | 54.0 |
| services_ok | 916.0 |
| shares_space_with_ok | 29.0 |

## Cross-checks across sources

Four sources describe the same places independently: Overture listings, tax-lot records (building class and owner), OpenStreetMap religious buildings, and IRS registrations. IRS addresses are registered addresses (often an office, PO box or pastor's apartment), so they confirm *who* a listing is, not where it gathers.

### Duplicate listings or real sharing

Lots where two or more congregations seem to gather, as each merge rule is added:

| merge_keys | congregations | lots_with_2plus | congregations_on_those_lots |
| --- | --- | --- | --- |
| website or same name | 1214 | 204 | 478 |
| + phone | 1174 | 182 | 416 |
| + name match | 1156 | 170 | 386 |
| + IRS EIN | 1156 | 170 | 386 |

Evidence behind each "shared" flag after merging:

| shared_evidence | places | lots |
| --- | --- | --- |
| listings only | 330 | 138 |
| two or more IRS congregations | 56 | 23 |
| website says so | 28 | 24 |

### IRS registrations

| kind | orgs | po_box | apartment_or_suite | placed_on_a_lot |
| --- | --- | --- | --- | --- |
| congregation | 848 | 77 | 81 | 742 |
| support | 133 | 10 | 47 | 118 |
| other | 101 | 9 | 26 | 91 |
| school | 35 | 2 | 7 | 33 |

Overture listings matched to an IRS registration (same lot, or a unique name match in the same ZIP code):

| tradition | places | matched | pct_matched | on_same_lot | matched_school_or_support |
| --- | --- | --- | --- | --- | --- |
| Protestant and other Christian | 950 | 341 | 36.0 | 244 | 9 |
| Unknown | 213 | 35 | 16.0 | 21 | 8 |
| Catholic | 88 | 25 | 28.0 | 20 | 4 |
| Jewish | 19 | 5 | 26.0 | 3 | 0 |
| Muslim | 14 | 4 | 29.0 | 4 | 0 |
| Buddhist | 7 | 4 | 57.0 | 4 | 1 |
| Orthodox Christian | 6 | 3 | 50.0 | 3 | 0 |
| Sikh | 2 | 0 | 0.0 | 0 | 0 |
| Hindu | 1 | 0 | 0.0 | 0 | 0 |

IRS congregations that no Overture listing matched, by the lot of their registered address (listed in `v0/dc/private/dc_irs_only.csv`). Those registered on another body's religious lot, a school or a commercial lot are candidate renters and guests. Those at a house or apartment are mostly a pastor's or treasurer's address, not where people gather. PLUTO cuts owner names at about 21 characters, so some "owned by another body" lots are the congregation's own:

| lot_type | congregations | lot_has_an_overture_listing | registered_since_2010 |
| --- | --- | --- | --- |
| house or residential building | 162 | 6 | 47 |
| religious lot owned by another body | 88 | 68 | 18 |
| PO box | 70 | 0 | 12 |
| commercial lot | 53 | 7 | 13 |
| other lot | 45 | 12 | 11 |
| apartment | 35 | 1 | 15 |
| religious lot it owns | 35 | 19 | 5 |
| address not placed | 20 | 0 | 4 |
| school lot | 7 | 5 | 0 |

### Agreement at the lot level

Lots named by each source. Worship lot = building class M1/M9, or a religious owner with institutional use (the step 3 definition).

| overture | worship_lot | osm_building | irs | lots |
| --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 0 | 574 |
| 1 | 0 | 0 | 0 | 306 |
| 0 | 0 | 0 | 1 | 304 |
| 1 | 1 | 0 | 0 | 190 |
| 1 | 1 | 1 | 1 | 146 |
| 1 | 1 | 1 | 0 | 126 |
| 1 | 1 | 0 | 1 | 126 |
| 1 | 0 | 0 | 1 | 67 |
| 0 | 1 | 1 | 0 | 53 |
| 0 | 1 | 0 | 1 | 30 |
| 0 | 0 | 1 | 0 | 16 |
| 1 | 0 | 1 | 0 | 11 |

Capture-recapture (Chapman). The lists are not independent and IRS keeps closed churches on file, so these are rough indications, not counts:

| pair | list_1 | list_2 | in_both | estimated_total |
| --- | --- | --- | --- | --- |
| Congregations: Overture x IRS | 1156 | 848 | 362 | 2705 |
| Lots: Overture x OSM buildings | 974 | 363 | 285 | 1240 |

## Recall check: worship lots with no Overture place

| why | borough | lots | likely_misses |
| --- | --- | --- | --- |
| M1/M9 building class | Ward 1 | 64 | 26 |
| M1/M9 building class | Ward 2 | 166 | 35 |
| M1/M9 building class | Ward 3 | 73 | 24 |
| M1/M9 building class | Ward 4 | 176 | 37 |
| M1/M9 building class | Ward 5 | 245 | 75 |
| M1/M9 building class | Ward 6 | 133 | 15 |
| M1/M9 building class | Ward 7 | 211 | 42 |
| M1/M9 building class | Ward 8 | 167 | 49 |
| religious owner, institutional use | Ward 2 | 4 | 3 |
| religious owner, institutional use | Ward 3 | 2 | 0 |
| religious owner, institutional use | Ward 5 | 3 | 2 |
| religious owner, institutional use | Ward 6 | 1 | 1 |
| religious owner, institutional use | Ward 7 | 4 | 2 |
| religious owner, institutional use | Ward 8 | 4 | 2 |

The likely misses, with owner and address, are in `v0/dc/private/dc_recall_misses.csv`.

## 50 random rows for checking

Drawn with seed 20261122. They name places and addresses, so they are in `v0/dc/private/check50.md` and `v0/dc/private/dc_check50.csv` (with evidence quotes and URLs), which are not committed.

## Known gaps in this run

- The cloud session reaches websites only over HTTPS; sites with no HTTPS show as connection or TLS errors and would load from a normal network.
- Version 0 reads static HTML only: no JavaScript rendering, PDFs or social media.
- Listings on one lot count as one congregation when they share a website, a phone number, a matching name or an IRS registration. Two names for one body with none of these in common still show as "shared"; the evidence column says how strong each flag is.
- Places with no website (about a third) can only be judged at their listing lot.
