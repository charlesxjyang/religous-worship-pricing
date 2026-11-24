# Shared and multi-use worship space in Charlotte: first pass

Run 2026-11-24. 1,068 congregations (after merging duplicate listings), each placed on the tax lot where it gathers. For 300 the lot comes from the congregation's own website; for the rest it is the Overture listing. The unit is the tax lot (BBL); the same-building (BIN) rows below are the stricter test.

## 1. Congregations sharing a building with other congregations

| test | congregations | share |
| --- | --- | --- |
| Same tax lot as at least one other congregation | 327 | 30.6% |
| ... and the IRS shows 2+ congregations registered on the lot | 28 | 2.6% |

This city's parcel records carry no building IDs, so only the lot test is available; a lot can hold more than one building. The lot row is an upper bound: a congregation listed twice under unrelated names still looks like two. The IRS-corroborated rows are closer to lower bounds, since many congregations are registered at another address or not at all. Lots with 2+ congregations, by how many share:

| congregations_on_lot | lots | congregations |
| --- | --- | --- |
| 2 | 108 | 216 |
| 3 | 23 | 69 |
| 4 | 5 | 20 |
| 5 or more | 4 | 22 |

## 2. Congregations in a building also used for something else

417 congregations (39.0%) gather on a lot whose building is not a religious building or its own school. For 39 of them the IRS registration is on the same lot, which corroborates that the congregation is based there. 76 of the 417 are homes with no evidence either way (see the check below). 7 more are set aside as location unknown, because their home address looks like a mailing address. By building type (DOF building class, NCES schools on the lot, and the checks below):

| building_use | congregations | pct | also_shared_with_other_congregations | irs_registered_on_lot |
| --- | --- | --- | --- | --- |
| religious building only | 643 | 60.2 | 193 | 146 |
| store or office building | 149 | 14.0 | 48 | 11 |
| residential | 88 | 8.2 | 8 | 6 |
| industrial, garage or loft | 79 | 7.4 | 44 | 12 |
| religious building hosting another school | 30 | 2.8 | 19 | 8 |
| public or charter school building | 26 | 2.4 | 6 | 0 |
| other institution or hall | 19 | 1.8 | 2 | 2 |
| vacant or no lot record | 12 | 1.1 | 0 | 0 |
| school building, owner unrelated | 8 | 0.7 | 4 | 0 |
| location unknown (home looks like a mailing address) | 7 | 0.7 | 0 | 0 |
| independent private school building | 5 | 0.5 | 3 | 0 |
| college or university building | 1 | 0.1 | 0 | 0 |
| its own school (religious complex) | 1 | 0.1 | 0 | 0 |

### Checking homes: gathering place or mailing address?

Congregations on residential lots (houses, apartment buildings, and apartments over stores). Evidence from OpenStreetMap, the listing address, the IRS registration and the crawled website text; strongest first. "Suggests mailing" cases are moved to "location unknown" above.

| home_check | home_evidence | congregations | residential | with_stores |
| --- | --- | --- | --- | --- |
| unconfirmed | no evidence either way (no website text) | 67 | 67 | 0 |
| unconfirmed | no evidence either way | 9 | 9 | 0 |
| supports gathering | its website gives this street address | 9 | 9 | 0 |
| supports gathering | OSM maps a place of worship on the lot | 3 | 3 | 0 |
| suggests mailing | its website gives other addresses, not this one | 6 | 6 | 0 |
| suggests mailing | IRS registration is on a church, school or commercial lot e… | 1 | 1 | 0 |

### Checking schools: the congregation's own, or another body's?

Congregations on a lot holding an NCES school, or in a school-class building. Own school: the school carries the congregation's name; or a Catholic parish with a Catholic-named school on Catholic-owned land; or, for a school building with no NCES record, the congregation owns it or it is a parochial school (class W2) on religious land. Public, charter and independent schools (independent religious schools included) count as other use; own schools do not.

| school_check | lot_building | congregations |
| --- | --- | --- |
| college | school building | 1 |
| independent school | religious building with a school on the lot | 25 |
| independent school | school building | 5 |
| own school | religious building with a school on the lot | 9 |
| own school | school building | 1 |
| public school | school building | 26 |
| public school | religious building with a school on the lot | 5 |
| unrelated school building | school building | 8 |

## Both questions together

| building | alone_on_lot | with_other_congregations | total |
| --- | --- | --- | --- |
| religious building only | 458 | 193 | 651 |
| other-use building | 283 | 134 | 417 |

The plan's price signal sits in the three cells other than "religious building only, alone": congregations that economize on space by sharing a sanctuary, renting a storefront or school, or meeting in a home.

## By tradition

| tradition | congregations | pct_sharing | pct_other_use_building | pct_either |
| --- | --- | --- | --- | --- |
| Protestant and other Christian | 986 | 32.0 | 39.0 | 58.0 |
| Unknown | 27 | 37.0 | 67.0 | 81.0 |
| Catholic | 17 | 24.0 | 24.0 | 29.0 |
| Muslim | 15 | 13.0 | 67.0 | 67.0 |

Tradition comes from the congregation's own website where extraction read one, else from the Overture category; "Unknown" is mostly Overture's generic categories with no usable website.

## By council district

| council district | congregations | pct_sharing | pct_other_use_building | pct_either |
| --- | --- | --- | --- | --- |
| District 1 | 257 | 35.0 | 41.0 | 61.0 |
| District 2 | 241 | 26.0 | 37.0 | 54.0 |
| District 3 | 177 | 31.0 | 45.0 | 63.0 |
| District 4 | 95 | 37.0 | 49.0 | 69.0 |
| District 5 | 167 | 34.0 | 35.0 | 54.0 |
| District 6 | 79 | 22.0 | 32.0 | 44.0 |
| District 7 | 52 | 21.0 | 29.0 | 42.0 |

## How the population changes the answer

| population | congregations | pct_sharing | pct_other_use_building |
| --- | --- | --- | --- |
| All listings, any category or confidence | 1378 | 40.9 | 43.8 |
| Headline (worship categories, confidence 0.5+) | 1068 | 30.6 | 39.0 |
| Headline, IRS-registered congregations only | 284 | 24.3 | 27.5 |

## Caveats

- Duplicate listings under unrelated names inflate sharing. Merges use website, phone, a conservative name match and IRS EIN; the IRS-corroborated row is the safer number.
- A lot can hold several buildings (a church and its school or rectory). The same-building (BIN) rows remove those, but only for congregations whose address geocoded.
- Each listing sits on the lot of its geocoded street address where that agrees with its map point to within 150 m, else on the point's lot. Listing addresses are what Overture's sources publish and can be a mailing address; website extraction replaces them with the address where services are held.
- Building class describes the main building. A church building whose basement hosts a day care, or a store building with a church upstairs, is classed by its main use.
- Places with no listing are missing. The IRS file holds 631 registered congregations that no listing matched, many on commercial lots or in other bodies' buildings, so the true shares of sharing and other-use space are likely higher.
