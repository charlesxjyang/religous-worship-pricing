# Shared and multi-use worship space in Houston: first pass

Run 2026-11-24. 3,453 congregations (after merging duplicate listings), each placed on the tax lot where it gathers. Website extraction has not run yet, so every lot here is the Overture listing's, which is usually but not always where people gather. The unit is the tax lot (BBL); the same-building (BIN) rows below are the stricter test.

## 1. Congregations sharing worship space with other congregations

Sharing means two distinct congregations using the same worship space: another congregation in the same building, where the building is not split into units, or the congregation's own website saying it shares space or meets at another congregation. Congregations in separate units of one store, office, industrial or apartment building are co-tenants: separate places of worship, not sharing.

| test | congregations | share |
| --- | --- | --- |
| Shares worship space with another congregation | 635 | 18.4% |
| ... and the IRS shows 2+ congregations registered there | 62 | 1.8% |
| Co-tenant: another congregation in a separate unit of the s… | 285 | 8.3% |
| For reference: same tax lot as another congregation | 1219 | 35.3% |

3,107 of 3,453 congregations are placed in a building, from building footprints (Overture); the rest are judged by their lot. The sharing row is an upper bound in one way (two listings for one congregation under unrelated names still look like two) and the IRS row a lower bound (many congregations are registered elsewhere or not at all). Buildings with shared worship space, by how many congregations share it:

| congregations_in_space | buildings | congregations |
| --- | --- | --- |
| 2 | 216 | 430 |
| 3 | 41 | 121 |
| 4 | 9 | 36 |
| 5 or more | 5 | 48 |

## 2. Congregations in a building also used for something else

1,591 congregations (46.1%) gather on a lot whose building is not a religious building or its own school. For 150 of them the IRS registration is on the same lot, which corroborates that the congregation is based there. 204 of the 1,591 are homes with no evidence either way (see the check below). 42 more are set aside as location unknown, because their home address looks like a mailing address. By building type (DOF building class, NCES schools on the lot, and the checks below):

| building_use | congregations | pct | sharing_worship_space | cotenants | irs_registered_on_lot |
| --- | --- | --- | --- | --- | --- |
| religious building only | 1814 | 52.5 | 407 | 0 | 475 |
| store or office building | 438 | 12.7 | 0 | 163 | 37 |
| vacant or no lot record | 427 | 12.4 | 152 | 0 | 17 |
| industrial, garage or loft | 262 | 7.6 | 0 | 96 | 36 |
| residential | 229 | 6.6 | 0 | 19 | 37 |
| other institution or hall | 137 | 4.0 | 34 | 4 | 10 |
| religious building hosting another school | 46 | 1.3 | 22 | 0 | 6 |
| location unknown (home looks like a mailing address) | 42 | 1.2 | 0 | 1 | 2 |
| school building, owner unrelated | 23 | 0.7 | 10 | 0 | 4 |
| public or charter school building | 16 | 0.5 | 6 | 0 | 2 |
| its own school (religious complex) | 6 | 0.2 | 0 | 0 | 1 |
| college or university building | 6 | 0.2 | 2 | 0 | 0 |
| independent private school building | 4 | 0.1 | 2 | 2 | 0 |
| apartments or house with stores | 3 | 0.1 | 0 | 0 | 1 |

### Checking homes: gathering place or mailing address?

Congregations on residential lots (houses, apartment buildings, and apartments over stores). Evidence from OpenStreetMap, the listing address, the IRS registration and the crawled website text; strongest first. "Suggests mailing" cases are moved to "location unknown" above.

| home_check | home_evidence | congregations | residential | with_stores |
| --- | --- | --- | --- | --- |
| unconfirmed | no evidence either way (no website text) | 177 | 176 | 1 |
| unconfirmed | no evidence either way | 27 | 27 | 0 |
| supports gathering | its website gives this street address | 27 | 26 | 1 |
| supports gathering | OSM maps a place of worship on the lot | 1 | 0 | 1 |
| suggests mailing | IRS registration is on a church, school or commercial lot e… | 23 | 23 | 0 |
| suggests mailing | its website gives other addresses, not this one | 16 | 16 | 0 |
| suggests mailing | address has an apartment unit | 3 | 3 | 0 |

### Checking schools: the congregation's own, or another body's?

Congregations on a lot holding an NCES school, or in a school-class building. Own school: the school carries the congregation's name; or a Catholic parish with a Catholic-named school on Catholic-owned land; or, for a school building with no NCES record, the congregation owns it or it is a parochial school (class W2) on religious land. Public, charter and independent schools (independent religious schools included) count as other use; own schools do not.

| school_check | lot_building | congregations |
| --- | --- | --- |
| college | school building | 6 |
| independent school | religious building with a school on the lot | 31 |
| independent school | school building | 4 |
| own school | religious building with a school on the lot | 26 |
| own school | school building | 6 |
| public school | school building | 16 |
| public school | religious building with a school on the lot | 15 |
| unrelated school building | school building | 23 |

## Both questions together

| building | not_sharing | sharing_worship_space | total |
| --- | --- | --- | --- |
| religious building only | 1455 | 407 | 1862 |
| other-use building | 1363 | 228 | 1591 |

The plan's price signal sits in the three cells other than "religious building only, alone": congregations that economize on space by sharing a sanctuary, renting a storefront or school, or meeting in a home.

## By tradition

| tradition | congregations | pct_sharing | pct_other_use_building | pct_either |
| --- | --- | --- | --- | --- |
| Protestant and other Christian | 3118 | 19.0 | 46.0 | 58.0 |
| Unknown | 112 | 21.0 | 51.0 | 68.0 |
| Catholic | 94 | 9.0 | 19.0 | 28.0 |
| Muslim | 56 | 14.0 | 61.0 | 70.0 |
| Buddhist | 27 | 11.0 | 41.0 | 48.0 |
| Jewish | 23 | 4.0 | 30.0 | 35.0 |
| Hindu | 22 | 23.0 | 64.0 | 68.0 |

Tradition comes from the congregation's own website where extraction read one, else from the Overture category; "Unknown" is mostly Overture's generic categories with no usable website.

## By council district

| council district | congregations | pct_sharing | pct_other_use_building | pct_either |
| --- | --- | --- | --- | --- |
| District A | 304 | 20.0 | 64.0 | 72.0 |
| District B | 786 | 19.0 | 40.0 | 51.0 |
| District C | 198 | 11.0 | 43.0 | 52.0 |
| District D | 449 | 15.0 | 29.0 | 42.0 |
| District E | 173 | 18.0 | 60.0 | 66.0 |
| District F | 314 | 24.0 | 68.0 | 79.0 |
| District G | 119 | 15.0 | 55.0 | 68.0 |
| District H | 381 | 17.0 | 30.0 | 45.0 |
| District I | 267 | 21.0 | 34.0 | 55.0 |
| District J | 198 | 12.0 | 76.0 | 81.0 |
| District K | 264 | 23.0 | 45.0 | 63.0 |

## How the population changes the answer

| population | congregations | pct_sharing | pct_other_use_building |
| --- | --- | --- | --- |
| All listings, any category or confidence | 4404 | 17.9 | 51.8 |
| Headline (worship categories, confidence 0.5+) | 3453 | 18.4 | 46.1 |
| Headline, IRS-registered congregations only | 1012 | 15.3 | 31.1 |

## Caveats

- Duplicate listings under unrelated names inflate sharing. Merges use website, phone, a conservative name match and IRS EIN; the IRS-corroborated row is the safer number.
- A lot can hold several buildings (a church and its school or rectory). The same-building (BIN) rows remove those, but only for congregations whose address geocoded.
- Each listing sits on the lot of its geocoded street address where that agrees with its map point to within 150 m, else on the point's lot. Listing addresses are what Overture's sources publish and can be a mailing address; website extraction replaces them with the address where services are held.
- Building class describes the main building. A church building whose basement hosts a day care, or a store building with a church upstairs, is classed by its main use.
- Places with no listing are missing. The IRS file holds 2,380 registered congregations that no listing matched, many on commercial lots or in other bodies' buildings, so the true shares of sharing and other-use space are likely higher.
