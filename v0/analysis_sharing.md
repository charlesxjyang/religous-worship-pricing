# Shared and multi-use worship space in NYC: first pass

Run 2026-11-23. 6,897 congregations (after merging duplicate listings), each placed on the tax lot where it gathers. For 1,399 the lot comes from the congregation's own website; for the rest it is the Overture listing. The unit is the tax lot (BBL); the same-building (BIN) rows below are the stricter test.

## 1. Congregations sharing a building with other congregations

| test | congregations | share |
| --- | --- | --- |
| Same tax lot as at least one other congregation | 1476 | 21.4% |
| ... and the IRS shows 2+ congregations registered on the lot | 275 | 4.0% |
| Same building (BIN) as at least one other congregation | 1268 | 18.4% |
| ... and the IRS shows 2+ registered in the building | 244 | 3.5% |

Building IDs (BIN) come from geocoding the listing's street address; 6,353 of 6,897 congregations have one, so the building rows are a floor. The lot row is an upper bound: a congregation listed twice under unrelated names still looks like two. The IRS-corroborated rows are closer to lower bounds, since many congregations are registered at another address or not at all. Lots with 2+ congregations, by how many share:

| congregations_on_lot | lots | congregations |
| --- | --- | --- |
| 2 | 581 | 1162 |
| 3 | 77 | 231 |
| 4 | 13 | 52 |
| 5 or more | 6 | 31 |

## 2. Congregations in a building also used for something else

2,793 congregations (40.5%) gather on a lot whose building is not a religious building or its own school. For 619 of them the IRS registration is on the same lot, which corroborates that the congregation is based there. 1,120 of the 2,793 are homes with no evidence either way (see the check below). 247 more are set aside as location unknown, because their home address looks like a mailing address. By building type (DOF building class, NCES schools on the lot, and the checks below):

| building_use | congregations | pct | also_shared_with_other_congregations | irs_registered_on_lot |
| --- | --- | --- | --- | --- |
| religious building only | 3794 | 55.0 | 954 | 1299 |
| apartments or house with stores | 726 | 10.5 | 87 | 185 |
| store or office building | 724 | 10.5 | 201 | 138 |
| residential | 557 | 8.1 | 34 | 140 |
| location unknown (home looks like a mailing address) | 247 | 3.6 | 22 | 39 |
| vacant or no lot record | 234 | 3.4 | 45 | 54 |
| other institution or hall | 162 | 2.3 | 22 | 28 |
| industrial, garage or loft | 118 | 1.7 | 21 | 19 |
| religious building hosting another school | 84 | 1.2 | 28 | 29 |
| public or charter school building | 83 | 1.2 | 23 | 4 |
| school building, owner unrelated | 67 | 1.0 | 20 | 13 |
| its own school (religious complex) | 63 | 0.9 | 7 | 22 |
| independent private school building | 21 | 0.3 | 8 | 8 |
| college or university building | 17 | 0.2 | 4 | 1 |

### Checking homes: gathering place or mailing address?

Congregations on residential lots (houses, apartment buildings, and apartments over stores). Evidence from OpenStreetMap, the listing address, the IRS registration and the crawled website text; strongest first. "Suggests mailing" cases are moved to "location unknown" above.

| home_check | home_evidence | congregations | residential | with_stores |
| --- | --- | --- | --- | --- |
| unconfirmed | no evidence either way (no website text) | 1001 | 431 | 570 |
| unconfirmed | no evidence either way | 119 | 48 | 71 |
| supports gathering | its website gives this street address | 114 | 49 | 65 |
| supports gathering | OSM maps a place of worship on the lot | 48 | 28 | 20 |
| supports gathering | address is a storefront, ground floor or basement | 1 | 1 | 0 |
| suggests mailing | IRS registration is on a church, school or commercial lot e… | 116 | 60 | 56 |
| suggests mailing | its website gives other addresses, not this one | 106 | 51 | 55 |
| suggests mailing | address has an apartment unit | 25 | 10 | 15 |

### Checking schools: the congregation's own, or another body's?

Congregations on a lot holding an NCES school, or in a school-class building. Own school: the school carries the congregation's name; or a Catholic parish with a Catholic-named school on Catholic-owned land; or, for a school building with no NCES record, the congregation owns it or it is a parochial school (class W2) on religious land. Public, charter and independent schools (independent religious schools included) count as other use; own schools do not.

| school_check | lot_building | congregations |
| --- | --- | --- |
| college | school building | 17 |
| independent school | religious building with a school on the lot | 58 |
| independent school | school building | 21 |
| own school | school building | 63 |
| own school | religious building with a school on the lot | 30 |
| public school | school building | 83 |
| public school | religious building with a school on the lot | 26 |
| public school | vacant or no lot record | 1 |
| unrelated school building | school building | 67 |

## Both questions together

| building | alone_on_lot | with_other_congregations | total |
| --- | --- | --- | --- |
| religious building only | 3121 | 983 | 4104 |
| other-use building | 2300 | 493 | 2793 |

The plan's price signal sits in the three cells other than "religious building only, alone": congregations that economize on space by sharing a sanctuary, renting a storefront or school, or meeting in a home.

## By tradition

| tradition | congregations | pct_sharing | pct_other_use_building | pct_either |
| --- | --- | --- | --- | --- |
| Protestant and other Christian | 5153 | 24.0 | 41.0 | 57.0 |
| Jewish | 500 | 13.0 | 34.0 | 44.0 |
| Catholic | 441 | 12.0 | 23.0 | 32.0 |
| Unknown | 309 | 25.0 | 56.0 | 72.0 |
| Muslim | 244 | 10.0 | 52.0 | 58.0 |
| Hindu | 101 | 5.0 | 57.0 | 57.0 |
| Buddhist | 81 | 11.0 | 51.0 | 52.0 |
| Orthodox Christian | 54 | 11.0 | 24.0 | 30.0 |

Tradition comes from the congregation's own website where extraction read one, else from the Overture category; "Unknown" is mostly Overture's generic categories with no usable website.

## By borough

| borough | congregations | pct_sharing | pct_other_use_building | pct_either |
| --- | --- | --- | --- | --- |
| Bronx | 1218 | 26.0 | 43.0 | 58.0 |
| Brooklyn | 2285 | 16.0 | 39.0 | 51.0 |
| Manhattan | 1214 | 26.0 | 43.0 | 61.0 |
| Queens | 1888 | 23.0 | 39.0 | 55.0 |
| Staten Island | 292 | 17.0 | 35.0 | 46.0 |

## How the population changes the answer

| population | congregations | pct_sharing | pct_other_use_building |
| --- | --- | --- | --- |
| All listings, any category or confidence | 8645 | 27.5 | 46.2 |
| Headline (worship categories, confidence 0.5+) | 6897 | 21.4 | 40.5 |
| Headline, IRS-registered congregations only | 2772 | 17.9 | 32.7 |

## Caveats

- Duplicate listings under unrelated names inflate sharing. Merges use website, phone, a conservative name match and IRS EIN; the IRS-corroborated row is the safer number.
- A lot can hold several buildings (a church and its school or rectory). The same-building (BIN) rows remove those, but only for congregations whose address geocoded.
- Each listing sits on the lot of its geocoded street address where that agrees with its map point to within 150 m, else on the point's lot. Listing addresses are what Overture's sources publish and can be a mailing address; website extraction replaces them with the address where services are held.
- Building class describes the main building. A church building whose basement hosts a day care, or a store building with a church upstairs, is classed by its main use.
- Places with no listing are missing. The IRS file holds 8,435 registered congregations that no listing matched, many on commercial lots or in other bodies' buildings, so the true shares of sharing and other-use space are likely higher.
