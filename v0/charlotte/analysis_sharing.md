# Shared and multi-use worship space in Charlotte: first pass

Run 2026-11-24. 1,112 congregations (after merging duplicate listings), each placed on the tax lot where it gathers. Website extraction has not run yet, so every lot here is the Overture listing's, which is usually but not always where people gather. The unit is the tax lot (BBL); the same-building (BIN) rows below are the stricter test.

## 1. Congregations sharing a building with other congregations

| test | congregations | share |
| --- | --- | --- |
| Same tax lot as at least one other congregation | 376 | 33.8% |
| ... and the IRS shows 2+ congregations registered on the lot | 29 | 2.6% |

This city's parcel records carry no building IDs, so only the lot test is available; a lot can hold more than one building. The lot row is an upper bound: a congregation listed twice under unrelated names still looks like two. The IRS-corroborated rows are closer to lower bounds, since many congregations are registered at another address or not at all. Lots with 2+ congregations, by how many share:

| congregations_on_lot | lots | congregations |
| --- | --- | --- |
| 2 | 118 | 236 |
| 3 | 31 | 93 |
| 4 | 5 | 20 |
| 5 or more | 5 | 27 |

## 2. Congregations in a building also used for something else

433 congregations (38.9%) gather on a lot whose building is not a religious building or its own school. For 35 of them the IRS registration is on the same lot, which corroborates that the congregation is based there. 76 of the 433 are homes with no evidence either way (see the check below). 7 more are set aside as location unknown, because their home address looks like a mailing address. By building type (DOF building class, NCES schools on the lot, and the checks below):

| building_use | congregations | pct | also_shared_with_other_congregations | irs_registered_on_lot |
| --- | --- | --- | --- | --- |
| religious building only | 671 | 60.3 | 221 | 149 |
| store or office building | 160 | 14.4 | 54 | 10 |
| residential | 86 | 7.7 | 9 | 5 |
| industrial, garage or loft | 82 | 7.4 | 48 | 10 |
| religious building hosting another school | 28 | 2.5 | 16 | 8 |
| public or charter school building | 28 | 2.5 | 9 | 0 |
| other institution or hall | 21 | 1.9 | 4 | 2 |
| vacant or no lot record | 11 | 1.0 | 0 | 0 |
| independent private school building | 8 | 0.7 | 6 | 0 |
| school building, owner unrelated | 7 | 0.6 | 4 | 0 |
| location unknown (home looks like a mailing address) | 7 | 0.6 | 3 | 0 |
| college or university building | 2 | 0.2 | 2 | 0 |
| its own school (religious complex) | 1 | 0.1 | 0 | 0 |

### Checking homes: gathering place or mailing address?

Congregations on residential lots (houses, apartment buildings, and apartments over stores). Evidence from OpenStreetMap, the listing address, the IRS registration and the crawled website text; strongest first. "Suggests mailing" cases are moved to "location unknown" above.

| home_check | home_evidence | congregations | residential | with_stores |
| --- | --- | --- | --- | --- |
| unconfirmed | no evidence either way (no website text) | 67 | 67 | 0 |
| unconfirmed | no evidence either way | 9 | 9 | 0 |
| supports gathering | its website gives this street address | 7 | 7 | 0 |
| supports gathering | OSM maps a place of worship on the lot | 3 | 3 | 0 |
| suggests mailing | its website gives other addresses, not this one | 6 | 6 | 0 |
| suggests mailing | IRS registration is on a church, school or commercial lot e… | 1 | 1 | 0 |

### Checking schools: the congregation's own, or another body's?

Congregations on a lot holding an NCES school, or in a school-class building. Own school: the school carries the congregation's name; or a Catholic parish with a Catholic-named school on Catholic-owned land; or, for a school building with no NCES record, the congregation owns it or it is a parochial school (class W2) on religious land. Public, charter and independent schools (independent religious schools included) count as other use; own schools do not.

| school_check | lot_building | congregations |
| --- | --- | --- |
| college | school building | 2 |
| independent school | religious building with a school on the lot | 22 |
| independent school | school building | 8 |
| own school | religious building with a school on the lot | 8 |
| own school | school building | 1 |
| public school | school building | 28 |
| public school | religious building with a school on the lot | 6 |
| unrelated school building | school building | 7 |

## Both questions together

| building | alone_on_lot | with_other_congregations | total |
| --- | --- | --- | --- |
| religious building only | 455 | 224 | 679 |
| other-use building | 281 | 152 | 433 |

The plan's price signal sits in the three cells other than "religious building only, alone": congregations that economize on space by sharing a sanctuary, renting a storefront or school, or meeting in a home.

## By tradition

| tradition | congregations | pct_sharing | pct_other_use_building | pct_either |
| --- | --- | --- | --- | --- |
| Protestant and other Christian | 1026 | 35.0 | 39.0 | 59.0 |
| Unknown | 38 | 42.0 | 55.0 | 79.0 |
| Catholic | 16 | 25.0 | 19.0 | 25.0 |

Tradition comes from the congregation's own website where extraction read one, else from the Overture category; "Unknown" is mostly Overture's generic categories with no usable website.

## By council district

| council district | congregations | pct_sharing | pct_other_use_building | pct_either |
| --- | --- | --- | --- | --- |
| District 1 | 265 | 37.0 | 42.0 | 63.0 |
| District 2 | 247 | 32.0 | 35.0 | 57.0 |
| District 3 | 186 | 38.0 | 44.0 | 66.0 |
| District 4 | 99 | 37.0 | 51.0 | 68.0 |
| District 5 | 173 | 34.0 | 34.0 | 54.0 |
| District 6 | 85 | 25.0 | 35.0 | 47.0 |
| District 7 | 57 | 23.0 | 32.0 | 47.0 |

## How the population changes the answer

| population | congregations | pct_sharing | pct_other_use_building |
| --- | --- | --- | --- |
| All listings, any category or confidence | 1438 | 43.9 | 43.5 |
| Headline (worship categories, confidence 0.5+) | 1112 | 33.8 | 38.9 |
| Headline, IRS-registered congregations only | 291 | 25.8 | 26.5 |

## Caveats

- Duplicate listings under unrelated names inflate sharing. Merges use website, phone, a conservative name match and IRS EIN; the IRS-corroborated row is the safer number.
- A lot can hold several buildings (a church and its school or rectory). The same-building (BIN) rows remove those, but only for congregations whose address geocoded.
- Each listing sits on the lot of its geocoded street address where that agrees with its map point to within 150 m, else on the point's lot. Listing addresses are what Overture's sources publish and can be a mailing address; website extraction replaces them with the address where services are held.
- Building class describes the main building. A church building whose basement hosts a day care, or a store building with a church upstairs, is classed by its main use.
- Places with no listing are missing. The IRS file holds 633 registered congregations that no listing matched, many on commercial lots or in other bodies' buildings, so the true shares of sharing and other-use space are likely higher.
