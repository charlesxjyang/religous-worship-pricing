# Shared and multi-use worship space in NYC: first pass

Run 2026-11-23. 7,104 congregations (after merging duplicate listings), each placed on the tax lot where it gathers. Website extraction has not run yet, so every lot here is the Overture listing's, which is usually but not always where people gather. The unit is the tax lot (BBL); the same-building (BIN) rows below are the stricter test.

## 1. Congregations sharing a building with other congregations

| test | congregations | share |
| --- | --- | --- |
| Same tax lot as at least one other congregation | 1571 | 22.1% |
| ... and the IRS shows 2+ congregations registered on the lot | 304 | 4.3% |
| Same building (BIN) as at least one other congregation | 1330 | 18.7% |
| ... and the IRS shows 2+ registered in the building | 263 | 3.7% |

Building IDs (BIN) come from geocoding the listing's street address; 6,463 of 7,104 congregations have one, so the building rows are a floor. The lot row is an upper bound: a congregation listed twice under unrelated names still looks like two. The IRS-corroborated rows are closer to lower bounds, since many congregations are registered at another address or not at all. Lots with 2+ congregations, by how many share:

| congregations_on_lot | lots | congregations |
| --- | --- | --- |
| 2 | 590 | 1180 |
| 3 | 99 | 297 |
| 4 | 14 | 56 |
| 5 or more | 7 | 38 |

## 2. Congregations in a building also used for something else

2,900 congregations (40.8%) gather on a lot whose building is not a religious building or its own school. For 618 of them the IRS registration is on the same lot, which corroborates that the congregation is based there. 1,141 of the 2,900 are homes with no evidence either way (see the check below). 257 more are set aside as location unknown, because their home address looks like a mailing address. By building type (DOF building class, NCES schools on the lot, and the checks below):

| building_use | congregations | pct | also_shared_with_other_congregations | irs_registered_on_lot |
| --- | --- | --- | --- | --- |
| religious building only | 3882 | 54.6 | 1007 | 1305 |
| store or office building | 758 | 10.7 | 213 | 133 |
| apartments or house with stores | 738 | 10.4 | 88 | 187 |
| residential | 566 | 8.0 | 36 | 147 |
| vacant or no lot record | 261 | 3.7 | 54 | 51 |
| location unknown (home looks like a mailing address) | 257 | 3.6 | 18 | 39 |
| other institution or hall | 168 | 2.4 | 34 | 27 |
| industrial, garage or loft | 124 | 1.7 | 22 | 19 |
| public or charter school building | 90 | 1.3 | 31 | 3 |
| religious building hosting another school | 85 | 1.2 | 28 | 29 |
| school building, owner unrelated | 71 | 1.0 | 21 | 14 |
| its own school (religious complex) | 65 | 0.9 | 7 | 23 |
| independent private school building | 25 | 0.4 | 10 | 7 |
| college or university building | 14 | 0.2 | 2 | 1 |

### Checking homes: gathering place or mailing address?

Congregations on residential lots (houses, apartment buildings, and apartments over stores). Evidence from OpenStreetMap, the listing address, the IRS registration and the crawled website text; strongest first. "Suggests mailing" cases are moved to "location unknown" above.

| home_check | home_evidence | congregations | residential | with_stores |
| --- | --- | --- | --- | --- |
| unconfirmed | no evidence either way (no website text) | 1009 | 433 | 576 |
| unconfirmed | no evidence either way | 132 | 55 | 77 |
| supports gathering | its website gives this street address | 112 | 48 | 64 |
| supports gathering | OSM maps a place of worship on the lot | 50 | 29 | 21 |
| supports gathering | address is a storefront, ground floor or basement | 1 | 1 | 0 |
| suggests mailing | IRS registration is on a church, school or commercial lot e… | 119 | 63 | 56 |
| suggests mailing | its website gives other addresses, not this one | 112 | 54 | 58 |
| suggests mailing | address has an apartment unit | 26 | 10 | 16 |

### Checking schools: the congregation's own, or another body's?

Congregations on a lot holding an NCES school, or in a school-class building. Own school: the school carries the congregation's name; or a Catholic parish with a Catholic-named school on Catholic-owned land; or, for a school building with no NCES record, the congregation owns it or it is a parochial school (class W2) on religious land. Public, charter and independent schools (independent religious schools included) count as other use; own schools do not.

| school_check | lot_building | congregations |
| --- | --- | --- |
| college | school building | 14 |
| independent school | religious building with a school on the lot | 61 |
| independent school | school building | 25 |
| own school | school building | 65 |
| own school | religious building with a school on the lot | 29 |
| public school | school building | 90 |
| public school | religious building with a school on the lot | 24 |
| public school | vacant or no lot record | 1 |
| unrelated school building | school building | 71 |

## Both questions together

| building | alone_on_lot | with_other_congregations | total |
| --- | --- | --- | --- |
| religious building only | 3172 | 1032 | 4204 |
| other-use building | 2361 | 539 | 2900 |

The plan's price signal sits in the three cells other than "religious building only, alone": congregations that economize on space by sharing a sanctuary, renting a storefront or school, or meeting in a home.

## By tradition

| tradition | congregations | pct_sharing | pct_other_use_building | pct_either |
| --- | --- | --- | --- | --- |
| Protestant and other Christian | 5292 | 24.0 | 41.0 | 57.0 |
| Jewish | 512 | 14.0 | 35.0 | 45.0 |
| Unknown | 449 | 25.0 | 49.0 | 65.0 |
| Catholic | 414 | 12.0 | 22.0 | 31.0 |
| Muslim | 235 | 11.0 | 53.0 | 60.0 |
| Hindu | 101 | 5.0 | 59.0 | 59.0 |
| Buddhist | 86 | 14.0 | 52.0 | 56.0 |

Tradition comes from the Overture category; "Unknown" is mostly Overture's generic categories. Website extraction will fill many of these in.

## By borough

| borough | congregations | pct_sharing | pct_other_use_building | pct_either |
| --- | --- | --- | --- | --- |
| Bronx | 1241 | 26.0 | 43.0 | 58.0 |
| Brooklyn | 2337 | 16.0 | 39.0 | 51.0 |
| Manhattan | 1289 | 28.0 | 45.0 | 62.0 |
| Queens | 1936 | 23.0 | 39.0 | 56.0 |
| Staten Island | 301 | 19.0 | 35.0 | 47.0 |

## How the population changes the answer

| population | congregations | pct_sharing | pct_other_use_building |
| --- | --- | --- | --- |
| All listings, any category or confidence | 8959 | 28.6 | 46.6 |
| Headline (worship categories, confidence 0.5+) | 7104 | 22.1 | 40.8 |
| Headline, IRS-registered congregations only | 2819 | 18.7 | 33.1 |

## Caveats

- Duplicate listings under unrelated names inflate sharing. Merges use website, phone, a conservative name match and IRS EIN; the IRS-corroborated row is the safer number.
- A lot can hold several buildings (a church and its school or rectory). The same-building (BIN) rows remove those, but only for congregations whose address geocoded.
- Each listing sits on the lot of its geocoded street address where that agrees with its map point to within 150 m, else on the point's lot. Listing addresses are what Overture's sources publish and can be a mailing address; website extraction replaces them with the address where services are held.
- Building class describes the main building. A church building whose basement hosts a day care, or a store building with a church upstairs, is classed by its main use.
- Places with no listing are missing. The IRS file holds about 9,600 registered congregations that no listing matched, many on commercial lots or in other bodies' buildings, so the true shares of sharing and other-use space are likely higher.
