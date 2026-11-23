# Shared and multi-use worship space in NYC: first pass

Run 2026-11-23. 7,138 congregations (after merging duplicate listings), each placed on the tax lot where it gathers. Website extraction has not run yet, so every lot here is the Overture listing's, which is usually but not always where people gather. The unit is the tax lot (BBL), not the building; the single-building row below is the stricter test.

## 1. Congregations sharing a building with other congregations

| test | congregations | share |
| --- | --- | --- |
| Lot holds at least one other congregation | 1500 | 21.0% |
| ... and the IRS shows 2+ congregations registered there | 260 | 3.6% |
| ... on a lot with a single building | 1144 | 16.0% |
| ... both: single building and IRS-corroborated | 182 | 2.5% |

The first row is an upper bound: a congregation listed twice under unrelated names still looks like two. The IRS-corroborated row is closer to a lower bound, since many congregations are registered elsewhere or not at all. Lots with 2+ congregations, by how many share:

| congregations_on_lot | lots | congregations |
| --- | --- | --- |
| 2 | 574 | 1148 |
| 3 | 84 | 252 |
| 4 | 18 | 72 |
| 5 or more | 5 | 28 |

## 2. Congregations in a building also used for something else

3,480 congregations (48.8%) gather on a lot whose building is not a religious building alone. For 545 of them the IRS registration is on the same lot, which corroborates that the congregation is based there. By building type (DOF building class, plus NCES schools on the lot):

| building_use | congregations | pct | also_shared_with_other_congregations | irs_registered_on_lot |
| --- | --- | --- | --- | --- |
| religious building only | 3658 | 51.2 | 927 | 1175 |
| apartments or house with stores | 888 | 12.4 | 107 | 174 |
| residential | 818 | 11.5 | 37 | 124 |
| store or office building | 767 | 10.7 | 196 | 118 |
| school building | 270 | 3.8 | 76 | 44 |
| vacant or no lot record | 252 | 3.5 | 53 | 7 |
| industrial, garage or loft | 173 | 2.4 | 28 | 16 |
| other institution or hall | 167 | 2.3 | 32 | 23 |
| religious building with a school on the lot | 145 | 2.0 | 44 | 39 |

## Both questions together

| building | alone_on_lot | with_other_congregations | total |
| --- | --- | --- | --- |
| religious building only | 2731 | 927 | 3658 |
| other-use building | 2907 | 573 | 3480 |

The plan's price signal sits in the three cells other than "religious building only, alone": congregations that economize on space by sharing a sanctuary, renting a storefront or school, or meeting in a home.

## By tradition

| tradition | congregations | pct_sharing | pct_other_use_building | pct_either |
| --- | --- | --- | --- | --- |
| Protestant and other Christian | 5310 | 23.0 | 49.0 | 63.0 |
| Jewish | 512 | 12.0 | 42.0 | 51.0 |
| Unknown | 452 | 24.0 | 58.0 | 71.0 |
| Catholic | 423 | 14.0 | 35.0 | 43.0 |
| Muslim | 240 | 9.0 | 62.0 | 67.0 |
| Hindu | 99 | 4.0 | 65.0 | 65.0 |
| Buddhist | 87 | 11.0 | 60.0 | 61.0 |

Tradition comes from the Overture category; "Unknown" is mostly Overture's generic categories. Website extraction will fill many of these in.

## By borough

| borough | congregations | pct_sharing | pct_other_use_building | pct_either |
| --- | --- | --- | --- | --- |
| Bronx | 1248 | 24.0 | 52.0 | 64.0 |
| Brooklyn | 2344 | 16.0 | 47.0 | 58.0 |
| Manhattan | 1300 | 25.0 | 51.0 | 67.0 |
| Queens | 1947 | 23.0 | 48.0 | 63.0 |
| Staten Island | 299 | 18.0 | 42.0 | 54.0 |

## How the population changes the answer

| population | congregations | pct_sharing | pct_other_use_building |
| --- | --- | --- | --- |
| All listings, any category or confidence | 9027 | 26.8 | 54.5 |
| Headline (worship categories, confidence 0.5+) | 7138 | 21.0 | 48.8 |
| Headline, IRS-registered congregations only | 2766 | 17.0 | 42.4 |

## Caveats

- Duplicate listings under unrelated names inflate sharing. Merges use website, phone, a conservative name match and IRS EIN; the IRS-corroborated row is the safer number.
- A lot can hold several buildings (a church and its school or rectory). The single-building row removes those.
- Building class describes the main building. A church building whose basement hosts a day care, or a store building with a church upstairs, is classed by its main use.
- Places with no listing are missing. The IRS file holds about 9,600 registered congregations that no listing matched, many on commercial lots or in other bodies' buildings, so the true shares of sharing and other-use space are likely higher.
