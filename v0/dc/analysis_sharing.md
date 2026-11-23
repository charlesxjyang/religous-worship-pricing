# Shared and multi-use worship space in DC: first pass

Run 2026-11-23. 944 congregations (after merging duplicate listings), each placed on the tax lot where it gathers. Website extraction has not run yet, so every lot here is the Overture listing's, which is usually but not always where people gather. The unit is the tax lot (BBL); the same-building (BIN) rows below are the stricter test.

## 1. Congregations sharing a building with other congregations

| test | congregations | share |
| --- | --- | --- |
| Same tax lot as at least one other congregation | 248 | 26.3% |
| ... and the IRS shows 2+ congregations registered on the lot | 20 | 2.1% |

This city's parcel records carry no building IDs, so only the lot test is available; a lot can hold more than one building. The lot row is an upper bound: a congregation listed twice under unrelated names still looks like two. The IRS-corroborated rows are closer to lower bounds, since many congregations are registered at another address or not at all. Lots with 2+ congregations, by how many share:

| congregations_on_lot | lots | congregations |
| --- | --- | --- |
| 2 | 91 | 182 |
| 3 | 19 | 57 |
| 4 | 1 | 4 |
| 5 or more | 1 | 5 |

## 2. Congregations in a building also used for something else

290 congregations (30.7%) gather on a lot whose building is not a religious building or its own school. For 43 of them the IRS registration is on the same lot, which corroborates that the congregation is based there. 72 of the 290 are homes with no evidence either way (see the check below). 16 more are set aside as location unknown, because their home address looks like a mailing address. By building type (DOF building class, NCES schools on the lot, and the checks below):

| building_use | congregations | pct | also_shared_with_other_congregations | irs_registered_on_lot |
| --- | --- | --- | --- | --- |
| religious building only | 635 | 67.3 | 185 | 210 |
| residential | 85 | 9.0 | 9 | 15 |
| store or office building | 83 | 8.8 | 16 | 12 |
| vacant or no lot record | 38 | 4.0 | 6 | 5 |
| other institution or hall | 38 | 4.0 | 11 | 3 |
| location unknown (home looks like a mailing address) | 16 | 1.7 | 2 | 1 |
| public or charter school building | 13 | 1.4 | 2 | 1 |
| religious building hosting another school | 13 | 1.4 | 4 | 4 |
| independent private school building | 7 | 0.7 | 6 | 1 |
| industrial, garage or loft | 7 | 0.7 | 2 | 2 |
| college or university building | 5 | 0.5 | 3 | 0 |
| its own school (religious complex) | 3 | 0.3 | 2 | 0 |
| school building, owner unrelated | 1 | 0.1 | 0 | 0 |

### Checking homes: gathering place or mailing address?

Congregations on residential lots (houses, apartment buildings, and apartments over stores). Evidence from OpenStreetMap, the listing address, the IRS registration and the crawled website text; strongest first. "Suggests mailing" cases are moved to "location unknown" above.

| home_check | home_evidence | congregations | residential | with_stores |
| --- | --- | --- | --- | --- |
| unconfirmed | no evidence either way (no website text) | 64 | 64 | 0 |
| unconfirmed | no evidence either way | 8 | 8 | 0 |
| supports gathering | its website gives this street address | 12 | 12 | 0 |
| supports gathering | OSM maps a place of worship on the lot | 1 | 1 | 0 |
| suggests mailing | IRS registration is on a church, school or commercial lot e… | 8 | 8 | 0 |
| suggests mailing | its website gives other addresses, not this one | 8 | 8 | 0 |

### Checking schools: the congregation's own, or another body's?

Congregations on a lot holding an NCES school, or in a school-class building. Own school: the school carries the congregation's name; or a Catholic parish with a Catholic-named school on Catholic-owned land; or, for a school building with no NCES record, the congregation owns it or it is a parochial school (class W2) on religious land. Public, charter and independent schools (independent religious schools included) count as other use; own schools do not.

| school_check | lot_building | congregations |
| --- | --- | --- |
| college | school building | 5 |
| independent school | school building | 7 |
| independent school | religious building with a school on the lot | 5 |
| own school | religious building with a school on the lot | 5 |
| own school | school building | 3 |
| public school | school building | 13 |
| public school | religious building with a school on the lot | 8 |
| public school | vacant or no lot record | 2 |
| unrelated school building | school building | 1 |

## Both questions together

| building | alone_on_lot | with_other_congregations | total |
| --- | --- | --- | --- |
| religious building only | 465 | 189 | 654 |
| other-use building | 231 | 59 | 290 |

The plan's price signal sits in the three cells other than "religious building only, alone": congregations that economize on space by sharing a sanctuary, renting a storefront or school, or meeting in a home.

## By tradition

| tradition | congregations | pct_sharing | pct_other_use_building | pct_either |
| --- | --- | --- | --- | --- |
| Protestant and other Christian | 823 | 26.0 | 29.0 | 50.0 |
| Catholic | 61 | 28.0 | 46.0 | 57.0 |
| Unknown | 27 | 33.0 | 48.0 | 70.0 |
| Jewish | 15 | 20.0 | 20.0 | 40.0 |

Tradition comes from the Overture category; "Unknown" is mostly Overture's generic categories. Website extraction will fill many of these in.

## By ward

| ward | congregations | pct_sharing | pct_other_use_building | pct_either |
| --- | --- | --- | --- | --- |
| Ward 1 | 54 | 15.0 | 43.0 | 54.0 |
| Ward 2 | 138 | 27.0 | 35.0 | 57.0 |
| Ward 3 | 62 | 50.0 | 23.0 | 65.0 |
| Ward 4 | 143 | 36.0 | 24.0 | 50.0 |
| Ward 5 | 152 | 18.0 | 40.0 | 51.0 |
| Ward 6 | 132 | 28.0 | 29.0 | 52.0 |
| Ward 7 | 167 | 23.0 | 29.0 | 44.0 |
| Ward 8 | 96 | 20.0 | 25.0 | 41.0 |

## How the population changes the answer

| population | congregations | pct_sharing | pct_other_use_building |
| --- | --- | --- | --- |
| All listings, any category or confidence | 1221 | 34.4 | 36.8 |
| Headline (worship categories, confidence 0.5+) | 944 | 26.3 | 30.7 |
| Headline, IRS-registered congregations only | 353 | 20.4 | 21.0 |

## Caveats

- Duplicate listings under unrelated names inflate sharing. Merges use website, phone, a conservative name match and IRS EIN; the IRS-corroborated row is the safer number.
- A lot can hold several buildings (a church and its school or rectory). The same-building (BIN) rows remove those, but only for congregations whose address geocoded.
- Each listing sits on the lot of its geocoded street address where that agrees with its map point to within 150 m, else on the point's lot. Listing addresses are what Overture's sources publish and can be a mailing address; website extraction replaces them with the address where services are held.
- Building class describes the main building. A church building whose basement hosts a day care, or a store building with a church upstairs, is classed by its main use.
- Places with no listing are missing. The IRS file holds 517 registered congregations that no listing matched, many on commercial lots or in other bodies' buildings, so the true shares of sharing and other-use space are likely higher.
