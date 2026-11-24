# Shared and multi-use worship space in Charlotte: first pass

Run 2026-11-24. 1,069 congregations (after merging duplicate listings), each placed on the tax lot where it gathers. For 293 the lot comes from the congregation's own website; for the rest it is the Overture listing. The unit is the tax lot (BBL); the same-building (BIN) rows below are the stricter test.

## 1. Congregations sharing worship space with other congregations

Sharing means two distinct congregations using the same worship space: another congregation in the same building, where the building is not split into units, or the congregation's own website saying it shares space or meets at another congregation. Congregations in separate units of one store, office, industrial or apartment building are co-tenants: separate places of worship, not sharing.

| test | congregations | share |
| --- | --- | --- |
| Shares worship space with another congregation | 183 | 17.1% |
| ... and the IRS shows 2+ congregations registered there | 18 | 1.7% |
| Co-tenant: another congregation in a separate unit of the s… | 104 | 9.7% |
| For reference: same tax lot as another congregation | 331 | 31.0% |

1,016 of 1,069 congregations are placed in a building, from building footprints (Overture); the rest are judged by their lot. The sharing row is an upper bound in one way (two listings for one congregation under unrelated names still look like two) and the IRS row a lower bound (many congregations are registered elsewhere or not at all). Buildings with shared worship space, by how many congregations share it:

| congregations_in_space | buildings | congregations |
| --- | --- | --- |
| 2 | 60 | 120 |
| 3 | 12 | 36 |
| 4 | 3 | 12 |
| 5 or more | 1 | 5 |

## 2. Congregations in a building also used for something else

414 congregations (38.7%) gather on a lot whose building is not a religious building or its own school. For 39 of them the IRS registration is on the same lot, which corroborates that the congregation is based there. 75 of the 414 are homes with no evidence either way (see the check below). 8 more are set aside as location unknown, because their home address looks like a mailing address. By building type (DOF building class, NCES schools on the lot, and the checks below):

| building_use | congregations | pct | sharing_worship_space | cotenants | irs_registered_on_lot |
| --- | --- | --- | --- | --- | --- |
| religious building only | 646 | 60.4 | 165 | 0 | 146 |
| store or office building | 151 | 14.1 | 0 | 47 | 12 |
| residential | 86 | 8.0 | 0 | 9 | 6 |
| industrial, garage or loft | 79 | 7.4 | 0 | 40 | 11 |
| public or charter school building | 26 | 2.4 | 6 | 0 | 0 |
| religious building hosting another school | 25 | 2.3 | 10 | 0 | 8 |
| other institution or hall | 19 | 1.8 | 0 | 2 | 2 |
| vacant or no lot record | 12 | 1.1 | 0 | 0 | 0 |
| location unknown (home looks like a mailing address) | 8 | 0.7 | 0 | 1 | 0 |
| independent private school building | 8 | 0.7 | 0 | 5 | 0 |
| school building, owner unrelated | 7 | 0.7 | 2 | 0 | 0 |
| its own school (religious complex) | 1 | 0.1 | 0 | 0 | 0 |
| college or university building | 1 | 0.1 | 0 | 0 | 0 |

### Checking homes: gathering place or mailing address?

Congregations on residential lots (houses, apartment buildings, and apartments over stores). Evidence from OpenStreetMap, the listing address, the IRS registration and the crawled website text; strongest first. "Suggests mailing" cases are moved to "location unknown" above.

| home_check | home_evidence | congregations | residential | with_stores |
| --- | --- | --- | --- | --- |
| unconfirmed | no evidence either way (no website text) | 67 | 67 | 0 |
| unconfirmed | no evidence either way | 8 | 8 | 0 |
| supports gathering | its website gives this street address | 8 | 8 | 0 |
| supports gathering | OSM maps a place of worship on the lot | 3 | 3 | 0 |
| suggests mailing | its website gives other addresses, not this one | 7 | 7 | 0 |
| suggests mailing | IRS registration is on a church, school or commercial lot e… | 1 | 1 | 0 |

### Checking schools: the congregation's own, or another body's?

Congregations on a lot holding an NCES school, or in a school-class building. Own school: the school carries the congregation's name; or a Catholic parish with a Catholic-named school on Catholic-owned land; or, for a school building with no NCES record, the congregation owns it or it is a parochial school (class W2) on religious land. Public, charter and independent schools (independent religious schools included) count as other use; own schools do not.

| school_check | lot_building | congregations |
| --- | --- | --- |
| college | school building | 1 |
| independent school | religious building with a school on the lot | 20 |
| independent school | school building | 8 |
| own school | religious building with a school on the lot | 9 |
| own school | school building | 1 |
| public school | school building | 26 |
| public school | religious building with a school on the lot | 5 |
| unrelated school building | school building | 7 |

## Both questions together

| building | not_sharing | sharing_worship_space | total |
| --- | --- | --- | --- |
| religious building only | 490 | 165 | 655 |
| other-use building | 396 | 18 | 414 |

The plan's price signal sits in the three cells other than "religious building only, alone": congregations that economize on space by sharing a sanctuary, renting a storefront or school, or meeting in a home.

## By tradition

| tradition | congregations | pct_sharing | pct_other_use_building | pct_either |
| --- | --- | --- | --- | --- |
| Protestant and other Christian | 986 | 18.0 | 38.0 | 55.0 |
| Unknown | 27 | 15.0 | 67.0 | 81.0 |
| Catholic | 17 | 12.0 | 18.0 | 24.0 |
| Muslim | 15 | 13.0 | 67.0 | 67.0 |

Tradition comes from the congregation's own website where extraction read one, else from the Overture category; "Unknown" is mostly Overture's generic categories with no usable website.

## By council district

| council district | congregations | pct_sharing | pct_other_use_building | pct_either |
| --- | --- | --- | --- | --- |
| District 1 | 259 | 19.0 | 41.0 | 59.0 |
| District 2 | 240 | 15.0 | 37.0 | 52.0 |
| District 3 | 174 | 17.0 | 44.0 | 59.0 |
| District 4 | 95 | 22.0 | 49.0 | 66.0 |
| District 5 | 168 | 14.0 | 34.0 | 46.0 |
| District 6 | 82 | 17.0 | 30.0 | 45.0 |
| District 7 | 51 | 20.0 | 27.0 | 45.0 |

## How the population changes the answer

| population | congregations | pct_sharing | pct_other_use_building |
| --- | --- | --- | --- |
| All listings, any category or confidence | 1379 | 16.8 | 43.4 |
| Headline (worship categories, confidence 0.5+) | 1069 | 17.1 | 38.7 |
| Headline, IRS-registered congregations only | 288 | 19.4 | 27.8 |

## Caveats

- Duplicate listings under unrelated names inflate sharing. Merges use website, phone, a conservative name match and IRS EIN; the IRS-corroborated row is the safer number.
- A lot can hold several buildings (a church and its school or rectory). The same-building (BIN) rows remove those, but only for congregations whose address geocoded.
- Each listing sits on the lot of its geocoded street address where that agrees with its map point to within 150 m, else on the point's lot. Listing addresses are what Overture's sources publish and can be a mailing address; website extraction replaces them with the address where services are held.
- Building class describes the main building. A church building whose basement hosts a day care, or a store building with a church upstairs, is classed by its main use.
- Places with no listing are missing. The IRS file holds 631 registered congregations that no listing matched, many on commercial lots or in other bodies' buildings, so the true shares of sharing and other-use space are likely higher.
