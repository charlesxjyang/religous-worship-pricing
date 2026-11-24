# Shared and multi-use worship space in DC: first pass

Run 2026-11-24. 903 congregations (after merging duplicate listings), each placed on the tax lot where it gathers. For 265 the lot comes from the congregation's own website; for the rest it is the Overture listing. The unit is the tax lot (BBL); the same-building (BIN) rows below are the stricter test.

## 1. Congregations sharing worship space with other congregations

Sharing means two distinct congregations using the same worship space: another congregation in the same building, where the building is not split into units, or the congregation's own website saying it shares space or meets at another congregation. Congregations in separate units of one store, office, industrial or apartment building are co-tenants: separate places of worship, not sharing.

| test | congregations | share |
| --- | --- | --- |
| Shares worship space with another congregation | 179 | 19.8% |
| ... and the IRS shows 2+ congregations registered there | 22 | 2.4% |
| Co-tenant: another congregation in a separate unit of the s… | 30 | 3.3% |
| For reference: same tax lot as another congregation | 232 | 25.7% |

888 of 903 congregations are placed in a building, from building footprints (Overture); the rest are judged by their lot. The sharing row is an upper bound in one way (two listings for one congregation under unrelated names still look like two) and the IRS row a lower bound (many congregations are registered elsewhere or not at all). Buildings with shared worship space, by how many congregations share it:

| congregations_in_space | buildings | congregations |
| --- | --- | --- |
| 2 | 64 | 128 |
| 3 | 12 | 36 |
| 5 or more | 1 | 5 |

## 2. Congregations in a building also used for something else

269 congregations (29.8%) gather on a lot whose building is not a religious building or its own school. For 42 of them the IRS registration is on the same lot, which corroborates that the congregation is based there. 69 of the 269 are homes with no evidence either way (see the check below). 16 more are set aside as location unknown, because their home address looks like a mailing address. By building type (DOF building class, NCES schools on the lot, and the checks below):

| building_use | congregations | pct | sharing_worship_space | cotenants | irs_registered_on_lot |
| --- | --- | --- | --- | --- | --- |
| religious building only | 615 | 68.1 | 161 | 0 | 209 |
| residential | 82 | 9.1 | 0 | 6 | 15 |
| store or office building | 76 | 8.4 | 3 | 12 | 11 |
| vacant or no lot record | 35 | 3.9 | 5 | 0 | 6 |
| other institution or hall | 34 | 3.8 | 3 | 7 | 3 |
| location unknown (home looks like a mailing address) | 16 | 1.8 | 0 | 3 | 1 |
| religious building hosting another school | 11 | 1.2 | 2 | 0 | 3 |
| public or charter school building | 11 | 1.2 | 0 | 0 | 1 |
| independent private school building | 8 | 0.9 | 3 | 0 | 1 |
| industrial, garage or loft | 7 | 0.8 | 0 | 2 | 2 |
| college or university building | 4 | 0.4 | 2 | 0 | 0 |
| its own school (religious complex) | 3 | 0.3 | 0 | 0 | 0 |
| school building, owner unrelated | 1 | 0.1 | 0 | 0 | 0 |

### Checking homes: gathering place or mailing address?

Congregations on residential lots (houses, apartment buildings, and apartments over stores). Evidence from OpenStreetMap, the listing address, the IRS registration and the crawled website text; strongest first. "Suggests mailing" cases are moved to "location unknown" above.

| home_check | home_evidence | congregations | residential | with_stores |
| --- | --- | --- | --- | --- |
| unconfirmed | no evidence either way (no website text) | 62 | 62 | 0 |
| unconfirmed | no evidence either way | 7 | 7 | 0 |
| supports gathering | its website gives this street address | 12 | 12 | 0 |
| supports gathering | OSM maps a place of worship on the lot | 1 | 1 | 0 |
| suggests mailing | IRS registration is on a church, school or commercial lot e… | 8 | 8 | 0 |
| suggests mailing | its website gives other addresses, not this one | 8 | 8 | 0 |

### Checking schools: the congregation's own, or another body's?

Congregations on a lot holding an NCES school, or in a school-class building. Own school: the school carries the congregation's name; or a Catholic parish with a Catholic-named school on Catholic-owned land; or, for a school building with no NCES record, the congregation owns it or it is a parochial school (class W2) on religious land. Public, charter and independent schools (independent religious schools included) count as other use; own schools do not.

| school_check | lot_building | congregations |
| --- | --- | --- |
| college | school building | 4 |
| independent school | school building | 8 |
| independent school | religious building with a school on the lot | 5 |
| own school | religious building with a school on the lot | 5 |
| own school | school building | 3 |
| public school | school building | 11 |
| public school | religious building with a school on the lot | 6 |
| public school | vacant or no lot record | 1 |
| unrelated school building | school building | 1 |

## Both questions together

| building | not_sharing | sharing_worship_space | total |
| --- | --- | --- | --- |
| religious building only | 473 | 161 | 634 |
| other-use building | 251 | 18 | 269 |

The plan's price signal sits in the three cells other than "religious building only, alone": congregations that economize on space by sharing a sanctuary, renting a storefront or school, or meeting in a home.

## By tradition

| tradition | congregations | pct_sharing | pct_other_use_building | pct_either |
| --- | --- | --- | --- | --- |
| Protestant and other Christian | 783 | 20.0 | 28.0 | 47.0 |
| Catholic | 62 | 21.0 | 42.0 | 55.0 |
| Unknown | 20 | 25.0 | 45.0 | 65.0 |
| Jewish | 15 | 27.0 | 20.0 | 47.0 |

Tradition comes from the congregation's own website where extraction read one, else from the Overture category; "Unknown" is mostly Overture's generic categories with no usable website.

## By ward

| ward | congregations | pct_sharing | pct_other_use_building | pct_either |
| --- | --- | --- | --- | --- |
| Ward 1 | 51 | 12.0 | 43.0 | 51.0 |
| Ward 2 | 128 | 26.0 | 32.0 | 55.0 |
| Ward 3 | 60 | 35.0 | 23.0 | 58.0 |
| Ward 4 | 143 | 29.0 | 23.0 | 48.0 |
| Ward 5 | 145 | 8.0 | 41.0 | 49.0 |
| Ward 6 | 123 | 23.0 | 31.0 | 50.0 |
| Ward 7 | 159 | 17.0 | 25.0 | 40.0 |
| Ward 8 | 94 | 13.0 | 23.0 | 36.0 |

## How the population changes the answer

| population | congregations | pct_sharing | pct_other_use_building |
| --- | --- | --- | --- |
| All listings, any category or confidence | 1156 | 19.1 | 35.8 |
| Headline (worship categories, confidence 0.5+) | 903 | 19.8 | 29.8 |
| Headline, IRS-registered congregations only | 348 | 18.7 | 21.0 |

## Caveats

- Duplicate listings under unrelated names inflate sharing. Merges use website, phone, a conservative name match and IRS EIN; the IRS-corroborated row is the safer number.
- A lot can hold several buildings (a church and its school or rectory). The same-building (BIN) rows remove those, but only for congregations whose address geocoded.
- Each listing sits on the lot of its geocoded street address where that agrees with its map point to within 150 m, else on the point's lot. Listing addresses are what Overture's sources publish and can be a mailing address; website extraction replaces them with the address where services are held.
- Building class describes the main building. A church building whose basement hosts a day care, or a store building with a church upstairs, is classed by its main use.
- Places with no listing are missing. The IRS file holds 515 registered congregations that no listing matched, many on commercial lots or in other bodies' buildings, so the true shares of sharing and other-use space are likely higher.
