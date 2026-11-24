# Shared and multi-use worship space in NYC: first pass

Run 2026-11-24. 6,897 congregations (after merging duplicate listings), each placed on the tax lot where it gathers. For 1,399 the lot comes from the congregation's own website; for the rest it is the Overture listing. The unit is the tax lot (BBL); the same-building (BIN) rows below are the stricter test.

## 1. Congregations sharing worship space with other congregations

Sharing means two distinct congregations using the same worship space: another congregation in the same building, where the building is not split into units, or the congregation's own website saying it shares space or meets at another congregation. Congregations in separate units of one store, office, industrial or apartment building are co-tenants: separate places of worship, not sharing.

| test | congregations | share |
| --- | --- | --- |
| Shares worship space with another congregation | 1038 | 15.1% |
| ... and the IRS shows 2+ congregations registered there | 201 | 2.9% |
| Co-tenant: another congregation in a separate unit of the s… | 297 | 4.3% |
| For reference: same tax lot as another congregation | 1476 | 21.4% |

6,353 of 6,897 congregations are placed in a building, from building IDs (BIN) from geocoding; the rest are judged by their lot. The sharing row is an upper bound in one way (two listings for one congregation under unrelated names still look like two) and the IRS row a lower bound (many congregations are registered elsewhere or not at all). Buildings with shared worship space, by how many congregations share it:

| congregations_in_space | buildings | congregations |
| --- | --- | --- |
| 2 | 410 | 817 |
| 3 | 45 | 135 |
| 4 | 9 | 36 |
| 5 or more | 3 | 15 |

## 2. Congregations in a building also used for something else

2,793 congregations (40.5%) gather on a lot whose building is not a religious building or its own school. For 619 of them the IRS registration is on the same lot, which corroborates that the congregation is based there. 1,120 of the 2,793 are homes with no evidence either way (see the check below). 247 more are set aside as location unknown, because their home address looks like a mailing address. By building type (DOF building class, NCES schools on the lot, and the checks below):

| building_use | congregations | pct | sharing_worship_space | cotenants | irs_registered_on_lot |
| --- | --- | --- | --- | --- | --- |
| religious building only | 3794 | 55.0 | 883 | 0 | 1299 |
| apartments or house with stores | 726 | 10.5 | 2 | 76 | 185 |
| store or office building | 724 | 10.5 | 3 | 157 | 138 |
| residential | 557 | 8.1 | 1 | 26 | 140 |
| location unknown (home looks like a mailing address) | 247 | 3.6 | 4 | 18 | 39 |
| vacant or no lot record | 234 | 3.4 | 43 | 0 | 54 |
| other institution or hall | 162 | 2.3 | 23 | 0 | 28 |
| industrial, garage or loft | 118 | 1.7 | 3 | 19 | 19 |
| religious building hosting another school | 84 | 1.2 | 23 | 0 | 29 |
| public or charter school building | 83 | 1.2 | 19 | 1 | 4 |
| school building, owner unrelated | 67 | 1.0 | 22 | 0 | 13 |
| its own school (religious complex) | 63 | 0.9 | 6 | 0 | 22 |
| independent private school building | 21 | 0.3 | 4 | 0 | 8 |
| college or university building | 17 | 0.2 | 2 | 0 | 1 |

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

| building | not_sharing | sharing_worship_space | total |
| --- | --- | --- | --- |
| religious building only | 3211 | 893 | 4104 |
| other-use building | 2648 | 145 | 2793 |

The plan's price signal sits in the three cells other than "religious building only, alone": congregations that economize on space by sharing a sanctuary, renting a storefront or school, or meeting in a home.

## By tradition

| tradition | congregations | pct_sharing | pct_other_use_building | pct_either |
| --- | --- | --- | --- | --- |
| Protestant and other Christian | 5153 | 16.0 | 41.0 | 55.0 |
| Jewish | 500 | 12.0 | 34.0 | 44.0 |
| Catholic | 441 | 11.0 | 23.0 | 31.0 |
| Unknown | 309 | 16.0 | 56.0 | 70.0 |
| Muslim | 244 | 7.0 | 52.0 | 57.0 |
| Hindu | 101 | 2.0 | 57.0 | 57.0 |
| Buddhist | 81 | 5.0 | 51.0 | 52.0 |
| Orthodox Christian | 54 | 11.0 | 24.0 | 30.0 |

Tradition comes from the congregation's own website where extraction read one, else from the Overture category; "Unknown" is mostly Overture's generic categories with no usable website.

## By borough

| borough | congregations | pct_sharing | pct_other_use_building | pct_either |
| --- | --- | --- | --- | --- |
| Bronx | 1218 | 14.0 | 43.0 | 56.0 |
| Brooklyn | 2285 | 11.0 | 39.0 | 49.0 |
| Manhattan | 1216 | 21.0 | 43.0 | 59.0 |
| Queens | 1887 | 17.0 | 39.0 | 54.0 |
| Staten Island | 291 | 14.0 | 35.0 | 46.0 |

## How the population changes the answer

| population | congregations | pct_sharing | pct_other_use_building |
| --- | --- | --- | --- |
| All listings, any category or confidence | 8645 | 14.4 | 46.2 |
| Headline (worship categories, confidence 0.5+) | 6897 | 15.1 | 40.5 |
| Headline, IRS-registered congregations only | 2772 | 13.1 | 32.7 |

## Caveats

- Duplicate listings under unrelated names inflate sharing. Merges use website, phone, a conservative name match and IRS EIN; the IRS-corroborated row is the safer number.
- A lot can hold several buildings (a church and its school or rectory). The same-building (BIN) rows remove those, but only for congregations whose address geocoded.
- Each listing sits on the lot of its geocoded street address where that agrees with its map point to within 150 m, else on the point's lot. Listing addresses are what Overture's sources publish and can be a mailing address; website extraction replaces them with the address where services are held.
- Building class describes the main building. A church building whose basement hosts a day care, or a store building with a church upstairs, is classed by its main use.
- Places with no listing are missing. The IRS file holds 8,435 registered congregations that no listing matched, many on commercial lots or in other bodies' buildings, so the true shares of sharing and other-use space are likely higher.
