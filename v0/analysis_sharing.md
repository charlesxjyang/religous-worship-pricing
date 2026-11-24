# Shared and multi-use worship space in NYC: first pass

Run 2026-11-24. 6,912 congregations (after merging duplicate listings), each placed on the tax lot where it gathers. For 1,326 the lot comes from the congregation's own website; for the rest it is the Overture listing. The unit is the tax lot (BBL); the same-building (BIN) rows below are the stricter test.

## 1. Congregations sharing worship space with other congregations

Sharing means two distinct congregations using the same worship space: another congregation in the same building, where the building is not split into units, or the congregation's own website saying it shares space or meets at another congregation. Congregations in separate units of one store, office, industrial or apartment building are co-tenants: separate places of worship, not sharing.

| test | congregations | share |
| --- | --- | --- |
| Shares worship space with another congregation | 1027 | 14.9% |
| ... and the IRS shows 2+ congregations registered there | 203 | 2.9% |
| Co-tenant: another congregation in a separate unit of the s… | 305 | 4.4% |
| For reference: same tax lot as another congregation | 1477 | 21.4% |

6,364 of 6,912 congregations are placed in a building, from building IDs (BIN) from geocoding; the rest are judged by their lot. The sharing row is an upper bound in one way (two listings for one congregation under unrelated names still look like two) and the IRS row a lower bound (many congregations are registered elsewhere or not at all). Buildings with shared worship space, by how many congregations share it:

| congregations_in_space | buildings | congregations |
| --- | --- | --- |
| 2 | 398 | 795 |
| 3 | 49 | 147 |
| 4 | 8 | 32 |
| 5 or more | 4 | 20 |

## 2. Congregations in a building also used for something else

2,810 congregations (40.7%) gather on a lot whose building is not a religious building or its own school. For 620 of them the IRS registration is on the same lot, which corroborates that the congregation is based there. 1,135 of the 2,810 are homes with no evidence either way (see the check below). 243 more are set aside as location unknown, because their home address looks like a mailing address. By building type (DOF building class, NCES schools on the lot, and the checks below):

| building_use | congregations | pct | sharing_worship_space | cotenants | irs_registered_on_lot |
| --- | --- | --- | --- | --- | --- |
| religious building only | 3796 | 54.9 | 875 | 0 | 1294 |
| store or office building | 734 | 10.6 | 3 | 164 | 140 |
| apartments or house with stores | 732 | 10.6 | 2 | 78 | 186 |
| residential | 557 | 8.1 | 0 | 26 | 140 |
| location unknown (home looks like a mailing address) | 243 | 3.5 | 3 | 16 | 39 |
| vacant or no lot record | 232 | 3.4 | 42 | 0 | 51 |
| other institution or hall | 164 | 2.4 | 23 | 0 | 27 |
| industrial, garage or loft | 119 | 1.7 | 3 | 19 | 20 |
| religious building hosting another school | 85 | 1.2 | 25 | 0 | 29 |
| public or charter school building | 84 | 1.2 | 18 | 2 | 6 |
| school building, owner unrelated | 66 | 1.0 | 22 | 0 | 12 |
| its own school (religious complex) | 63 | 0.9 | 6 | 0 | 22 |
| independent private school building | 21 | 0.3 | 3 | 0 | 8 |
| college or university building | 16 | 0.2 | 2 | 0 | 1 |

### Checking homes: gathering place or mailing address?

Congregations on residential lots (houses, apartment buildings, and apartments over stores). Evidence from OpenStreetMap, the listing address, the IRS registration and the crawled website text; strongest first. "Suggests mailing" cases are moved to "location unknown" above.

| home_check | home_evidence | congregations | residential | with_stores |
| --- | --- | --- | --- | --- |
| unconfirmed | no evidence either way (no website text) | 1009 | 433 | 576 |
| unconfirmed | no evidence either way | 126 | 51 | 75 |
| supports gathering | its website gives this street address | 105 | 44 | 61 |
| supports gathering | OSM maps a place of worship on the lot | 48 | 28 | 20 |
| supports gathering | address is a storefront, ground floor or basement | 1 | 1 | 0 |
| suggests mailing | IRS registration is on a church, school or commercial lot e… | 116 | 61 | 55 |
| suggests mailing | its website gives other addresses, not this one | 103 | 50 | 53 |
| suggests mailing | address has an apartment unit | 24 | 10 | 14 |

### Checking schools: the congregation's own, or another body's?

Congregations on a lot holding an NCES school, or in a school-class building. Own school: the school carries the congregation's name; or a Catholic parish with a Catholic-named school on Catholic-owned land; or, for a school building with no NCES record, the congregation owns it or it is a parochial school (class W2) on religious land. Public, charter and independent schools (independent religious schools included) count as other use; own schools do not.

| school_check | lot_building | congregations |
| --- | --- | --- |
| college | school building | 16 |
| independent school | religious building with a school on the lot | 59 |
| independent school | school building | 21 |
| own school | school building | 63 |
| own school | religious building with a school on the lot | 30 |
| public school | school building | 84 |
| public school | religious building with a school on the lot | 26 |
| public school | vacant or no lot record | 1 |
| unrelated school building | school building | 66 |

## Both questions together

| building | not_sharing | sharing_worship_space | total |
| --- | --- | --- | --- |
| religious building only | 3218 | 884 | 4102 |
| other-use building | 2667 | 143 | 2810 |

The plan's price signal sits in the three cells other than "religious building only, alone": congregations that economize on space by sharing a sanctuary, renting a storefront or school, or meeting in a home.

## By tradition

| tradition | congregations | pct_sharing | pct_other_use_building | pct_either |
| --- | --- | --- | --- | --- |
| Protestant and other Christian | 5161 | 16.0 | 41.0 | 55.0 |
| Jewish | 505 | 11.0 | 34.0 | 44.0 |
| Catholic | 440 | 10.0 | 24.0 | 32.0 |
| Unknown | 316 | 15.0 | 55.0 | 68.0 |
| Muslim | 242 | 8.0 | 52.0 | 58.0 |
| Hindu | 101 | 2.0 | 56.0 | 56.0 |
| Buddhist | 84 | 5.0 | 51.0 | 52.0 |
| Orthodox Christian | 49 | 10.0 | 22.0 | 27.0 |

Tradition comes from the congregation's own website where extraction read one, else from the Overture category; "Unknown" is mostly Overture's generic categories with no usable website.

## By borough

| borough | congregations | pct_sharing | pct_other_use_building | pct_either |
| --- | --- | --- | --- | --- |
| Bronx | 1215 | 13.0 | 44.0 | 56.0 |
| Brooklyn | 2287 | 10.0 | 40.0 | 49.0 |
| Manhattan | 1226 | 21.0 | 44.0 | 60.0 |
| Queens | 1891 | 17.0 | 39.0 | 54.0 |
| Staten Island | 293 | 15.0 | 35.0 | 46.0 |

## How the population changes the answer

| population | congregations | pct_sharing | pct_other_use_building |
| --- | --- | --- | --- |
| All listings, any category or confidence | 8666 | 14.3 | 46.3 |
| Headline (worship categories, confidence 0.5+) | 6912 | 14.9 | 40.7 |
| Headline, IRS-registered congregations only | 2774 | 13.1 | 33.0 |

## Caveats

- Duplicate listings under unrelated names inflate sharing. Merges use website, phone, a conservative name match and IRS EIN; the IRS-corroborated row is the safer number.
- A lot can hold several buildings (a church and its school or rectory). The same-building (BIN) rows remove those, but only for congregations whose address geocoded.
- Each listing sits on the lot of its geocoded street address where that agrees with its map point to within 150 m, else on the point's lot. Listing addresses are what Overture's sources publish and can be a mailing address; website extraction replaces them with the address where services are held.
- Building class describes the main building. A church building whose basement hosts a day care, or a store building with a church upstairs, is classed by its main use.
- Places with no listing are missing. The IRS file holds 8,436 registered congregations that no listing matched, many on commercial lots or in other bodies' buildings, so the true shares of sharing and other-use space are likely higher.
