# Shared and multi-use worship space in SF: first pass

Run 2026-11-24. 645 congregations (after merging duplicate listings), each placed on the tax lot where it gathers. Website extraction has not run yet, so every lot here is the Overture listing's, which is usually but not always where people gather. The unit is the tax lot (BBL); the same-building (BIN) rows below are the stricter test.

## 1. Congregations sharing worship space with other congregations

Sharing means two distinct congregations using the same worship space: another congregation in the same building, where the building is not split into units, or the congregation's own website saying it shares space or meets at another congregation. Congregations in separate units of one store, office, industrial or apartment building are co-tenants: separate places of worship, not sharing.

| test | congregations | share |
| --- | --- | --- |
| Shares worship space with another congregation | 114 | 17.7% |
| ... and the IRS shows 2+ congregations registered there | 29 | 4.5% |
| Co-tenant: another congregation in a separate unit of the s… | 18 | 2.8% |
| For reference: same tax lot as another congregation | 137 | 21.2% |

644 of 645 congregations are placed in a building, from building footprints (Overture); the rest are judged by their lot. The sharing row is an upper bound in one way (two listings for one congregation under unrelated names still look like two) and the IRS row a lower bound (many congregations are registered elsewhere or not at all). Buildings with shared worship space, by how many congregations share it:

| congregations_in_space | buildings | congregations |
| --- | --- | --- |
| 2 | 39 | 78 |
| 3 | 11 | 32 |
| 4 | 1 | 4 |

## 2. Congregations in a building also used for something else

214 congregations (33.2%) gather on a lot whose building is not a religious building or its own school. For 40 of them the IRS registration is on the same lot, which corroborates that the congregation is based there. 62 of the 214 are homes with no evidence either way (see the check below). 18 more are set aside as location unknown, because their home address looks like a mailing address. By building type (DOF building class, NCES schools on the lot, and the checks below):

| building_use | congregations | pct | sharing_worship_space | cotenants | irs_registered_on_lot |
| --- | --- | --- | --- | --- | --- |
| religious building only | 411 | 63.7 | 102 | 0 | 137 |
| residential | 59 | 9.1 | 0 | 3 | 18 |
| store or office building | 53 | 8.2 | 0 | 7 | 9 |
| other institution or hall | 27 | 4.2 | 4 | 2 | 2 |
| apartments or house with stores | 18 | 2.8 | 0 | 2 | 5 |
| location unknown (home looks like a mailing address) | 18 | 2.8 | 0 | 1 | 1 |
| vacant or no lot record | 16 | 2.5 | 3 | 0 | 0 |
| religious building hosting another school | 12 | 1.9 | 5 | 0 | 2 |
| industrial, garage or loft | 12 | 1.9 | 0 | 3 | 1 |
| school building, owner unrelated | 8 | 1.2 | 0 | 0 | 3 |
| independent private school building | 5 | 0.8 | 0 | 0 | 0 |
| public or charter school building | 4 | 0.6 | 0 | 0 | 0 |
| its own school (religious complex) | 2 | 0.3 | 0 | 0 | 1 |

### Checking homes: gathering place or mailing address?

Congregations on residential lots (houses, apartment buildings, and apartments over stores). Evidence from OpenStreetMap, the listing address, the IRS registration and the crawled website text; strongest first. "Suggests mailing" cases are moved to "location unknown" above.

| home_check | home_evidence | congregations | residential | with_stores |
| --- | --- | --- | --- | --- |
| unconfirmed | no evidence either way (no website text) | 49 | 35 | 14 |
| unconfirmed | no evidence either way | 13 | 10 | 3 |
| supports gathering | its website gives this street address | 10 | 10 | 0 |
| supports gathering | OSM maps a place of worship on the lot | 5 | 4 | 1 |
| suggests mailing | IRS registration is on a church, school or commercial lot e… | 10 | 6 | 4 |
| suggests mailing | its website gives other addresses, not this one | 8 | 7 | 1 |

### Checking schools: the congregation's own, or another body's?

Congregations on a lot holding an NCES school, or in a school-class building. Own school: the school carries the congregation's name; or a Catholic parish with a Catholic-named school on Catholic-owned land; or, for a school building with no NCES record, the congregation owns it or it is a parochial school (class W2) on religious land. Public, charter and independent schools (independent religious schools included) count as other use; own schools do not.

| school_check | lot_building | congregations |
| --- | --- | --- |
| independent school | religious building with a school on the lot | 12 |
| independent school | school building | 5 |
| own school | school building | 2 |
| own school | religious building with a school on the lot | 1 |
| public school | school building | 4 |
| public school | vacant or no lot record | 2 |
| unrelated school building | school building | 8 |

## Both questions together

| building | not_sharing | sharing_worship_space | total |
| --- | --- | --- | --- |
| religious building only | 329 | 102 | 431 |
| other-use building | 202 | 12 | 214 |

The plan's price signal sits in the three cells other than "religious building only, alone": congregations that economize on space by sharing a sanctuary, renting a storefront or school, or meeting in a home.

## By tradition

| tradition | congregations | pct_sharing | pct_other_use_building | pct_either |
| --- | --- | --- | --- | --- |
| Protestant and other Christian | 495 | 20.0 | 33.0 | 50.0 |
| Catholic | 55 | 4.0 | 25.0 | 29.0 |
| Buddhist | 36 | 8.0 | 44.0 | 53.0 |
| Unknown | 24 | 17.0 | 38.0 | 54.0 |
| Jewish | 21 | 14.0 | 43.0 | 57.0 |

Tradition comes from the congregation's own website where extraction read one, else from the Overture category; "Unknown" is mostly Overture's generic categories with no usable website.

## By supervisor district

| supervisor district | congregations | pct_sharing | pct_other_use_building | pct_either |
| --- | --- | --- | --- | --- |
| District 1 | 49 | 10.0 | 31.0 | 41.0 |
| District 10 | 88 | 17.0 | 28.0 | 43.0 |
| District 11 | 62 | 16.0 | 29.0 | 45.0 |
| District 2 | 50 | 24.0 | 28.0 | 48.0 |
| District 3 | 63 | 6.0 | 49.0 | 56.0 |
| District 4 | 52 | 17.0 | 21.0 | 38.0 |
| District 5 | 74 | 14.0 | 32.0 | 46.0 |
| District 6 | 27 | 30.0 | 74.0 | 93.0 |
| District 7 | 59 | 34.0 | 20.0 | 51.0 |
| District 8 | 45 | 13.0 | 38.0 | 51.0 |
| District 9 | 76 | 20.0 | 36.0 | 51.0 |

## How the population changes the answer

| population | congregations | pct_sharing | pct_other_use_building |
| --- | --- | --- | --- |
| All listings, any category or confidence | 804 | 16.8 | 39.4 |
| Headline (worship categories, confidence 0.5+) | 645 | 17.7 | 33.2 |
| Headline, IRS-registered congregations only | 238 | 16.0 | 23.5 |

## Caveats

- Duplicate listings under unrelated names inflate sharing. Merges use website, phone, a conservative name match and IRS EIN; the IRS-corroborated row is the safer number.
- A lot can hold several buildings (a church and its school or rectory). The same-building (BIN) rows remove those, but only for congregations whose address geocoded.
- Each listing sits on the lot of its geocoded street address where that agrees with its map point to within 150 m, else on the point's lot. Listing addresses are what Overture's sources publish and can be a mailing address; website extraction replaces them with the address where services are held.
- Building class describes the main building. A church building whose basement hosts a day care, or a store building with a church upstairs, is classed by its main use.
- Places with no listing are missing. The IRS file holds 409 registered congregations that no listing matched, many on commercial lots or in other bodies' buildings, so the true shares of sharing and other-use space are likely higher.
