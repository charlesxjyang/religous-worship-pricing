# Shared and multi-use worship space in Houston: first pass

Run 2026-11-24. 3,366 congregations (after merging duplicate listings), each placed on the tax lot where it gathers. For 575 the lot comes from the congregation's own website; for the rest it is the Overture listing. The unit is the tax lot (BBL); the same-building (BIN) rows below are the stricter test.

## 1. Congregations sharing worship space with other congregations

Sharing means two distinct congregations using the same worship space: another congregation in the same building, where the building is not split into units, or the congregation's own website saying it shares space or meets at another congregation. Congregations in separate units of one store, office, industrial or apartment building are co-tenants: separate places of worship, not sharing.

| test | congregations | share |
| --- | --- | --- |
| Shares worship space with another congregation | 615 | 18.3% |
| ... and the IRS shows 2+ congregations registered there | 65 | 1.9% |
| Co-tenant: another congregation in a separate unit of the s… | 264 | 7.8% |
| For reference: same tax lot as another congregation | 1164 | 34.6% |

2,998 of 3,366 congregations are placed in a building, from building footprints (Overture); the rest are judged by their lot. The sharing row is an upper bound in one way (two listings for one congregation under unrelated names still look like two) and the IRS row a lower bound (many congregations are registered elsewhere or not at all). Buildings with shared worship space, by how many congregations share it:

| congregations_in_space | buildings | congregations |
| --- | --- | --- |
| 2 | 211 | 420 |
| 3 | 37 | 109 |
| 4 | 7 | 28 |
| 5 or more | 5 | 47 |

## 2. Congregations in a building also used for something else

1,568 congregations (46.6%) gather on a lot whose building is not a religious building or its own school. For 157 of them the IRS registration is on the same lot, which corroborates that the congregation is based there. 203 of the 1,568 are homes with no evidence either way (see the check below). 42 more are set aside as location unknown, because their home address looks like a mailing address. By building type (DOF building class, NCES schools on the lot, and the checks below):

| building_use | congregations | pct | sharing_worship_space | cotenants | irs_registered_on_lot |
| --- | --- | --- | --- | --- | --- |
| religious building only | 1750 | 52.0 | 382 | 0 | 470 |
| vacant or no lot record | 430 | 12.8 | 153 | 0 | 18 |
| store or office building | 424 | 12.6 | 1 | 155 | 36 |
| industrial, garage or loft | 250 | 7.4 | 1 | 83 | 38 |
| residential | 227 | 6.7 | 0 | 19 | 38 |
| other institution or hall | 139 | 4.1 | 38 | 4 | 13 |
| religious building hosting another school | 44 | 1.3 | 22 | 0 | 6 |
| location unknown (home looks like a mailing address) | 42 | 1.2 | 0 | 1 | 3 |
| school building, owner unrelated | 24 | 0.7 | 10 | 0 | 5 |
| public or charter school building | 17 | 0.5 | 6 | 0 | 2 |
| its own school (religious complex) | 6 | 0.2 | 0 | 0 | 1 |
| college or university building | 6 | 0.2 | 2 | 0 | 0 |
| independent private school building | 4 | 0.1 | 0 | 2 | 0 |
| apartments or house with stores | 3 | 0.1 | 0 | 0 | 1 |

### Checking homes: gathering place or mailing address?

Congregations on residential lots (houses, apartment buildings, and apartments over stores). Evidence from OpenStreetMap, the listing address, the IRS registration and the crawled website text; strongest first. "Suggests mailing" cases are moved to "location unknown" above.

| home_check | home_evidence | congregations | residential | with_stores |
| --- | --- | --- | --- | --- |
| unconfirmed | no evidence either way (no website text) | 177 | 176 | 1 |
| unconfirmed | no evidence either way | 26 | 26 | 0 |
| supports gathering | its website gives this street address | 26 | 25 | 1 |
| supports gathering | OSM maps a place of worship on the lot | 1 | 0 | 1 |
| suggests mailing | IRS registration is on a church, school or commercial lot e… | 25 | 25 | 0 |
| suggests mailing | its website gives other addresses, not this one | 13 | 13 | 0 |
| suggests mailing | address has an apartment unit | 4 | 4 | 0 |

### Checking schools: the congregation's own, or another body's?

Congregations on a lot holding an NCES school, or in a school-class building. Own school: the school carries the congregation's name; or a Catholic parish with a Catholic-named school on Catholic-owned land; or, for a school building with no NCES record, the congregation owns it or it is a parochial school (class W2) on religious land. Public, charter and independent schools (independent religious schools included) count as other use; own schools do not.

| school_check | lot_building | congregations |
| --- | --- | --- |
| college | school building | 6 |
| independent school | religious building with a school on the lot | 30 |
| independent school | school building | 4 |
| own school | religious building with a school on the lot | 27 |
| own school | school building | 6 |
| public school | school building | 17 |
| public school | religious building with a school on the lot | 14 |
| unrelated school building | school building | 24 |

## Both questions together

| building | not_sharing | sharing_worship_space | total |
| --- | --- | --- | --- |
| religious building only | 1416 | 382 | 1798 |
| other-use building | 1335 | 233 | 1568 |

The plan's price signal sits in the three cells other than "religious building only, alone": congregations that economize on space by sharing a sanctuary, renting a storefront or school, or meeting in a home.

## By tradition

| tradition | congregations | pct_sharing | pct_other_use_building | pct_either |
| --- | --- | --- | --- | --- |
| Protestant and other Christian | 3042 | 19.0 | 47.0 | 59.0 |
| Unknown | 96 | 23.0 | 50.0 | 71.0 |
| Catholic | 94 | 6.0 | 20.0 | 27.0 |
| Muslim | 55 | 16.0 | 58.0 | 69.0 |
| Buddhist | 26 | 8.0 | 38.0 | 42.0 |
| Jewish | 23 | 4.0 | 30.0 | 35.0 |
| Hindu | 21 | 24.0 | 67.0 | 71.0 |

Tradition comes from the congregation's own website where extraction read one, else from the Overture category; "Unknown" is mostly Overture's generic categories with no usable website.

## By council district

| council district | congregations | pct_sharing | pct_other_use_building | pct_either |
| --- | --- | --- | --- | --- |
| District A | 297 | 21.0 | 67.0 | 74.0 |
| District B | 773 | 19.0 | 41.0 | 51.0 |
| District C | 183 | 11.0 | 43.0 | 51.0 |
| District D | 435 | 14.0 | 30.0 | 41.0 |
| District E | 171 | 18.0 | 61.0 | 66.0 |
| District F | 307 | 25.0 | 68.0 | 78.0 |
| District G | 119 | 18.0 | 57.0 | 72.0 |
| District H | 372 | 17.0 | 30.0 | 45.0 |
| District I | 261 | 21.0 | 34.0 | 54.0 |
| District J | 194 | 12.0 | 76.0 | 82.0 |
| District K | 254 | 22.0 | 45.0 | 61.0 |

## How the population changes the answer

| population | congregations | pct_sharing | pct_other_use_building |
| --- | --- | --- | --- |
| All listings, any category or confidence | 4277 | 17.9 | 52.2 |
| Headline (worship categories, confidence 0.5+) | 3366 | 18.3 | 46.6 |
| Headline, IRS-registered congregations only | 1000 | 14.8 | 32.2 |

## Caveats

- Duplicate listings under unrelated names inflate sharing. Merges use website, phone, a conservative name match and IRS EIN; the IRS-corroborated row is the safer number.
- A lot can hold several buildings (a church and its school or rectory). The same-building (BIN) rows remove those, but only for congregations whose address geocoded.
- Each listing sits on the lot of its geocoded street address where that agrees with its map point to within 150 m, else on the point's lot. Listing addresses are what Overture's sources publish and can be a mailing address; website extraction replaces them with the address where services are held.
- Building class describes the main building. A church building whose basement hosts a day care, or a store building with a church upstairs, is classed by its main use.
- Places with no listing are missing. The IRS file holds 2,376 registered congregations that no listing matched, many on commercial lots or in other bodies' buildings, so the true shares of sharing and other-use space are likely higher.
