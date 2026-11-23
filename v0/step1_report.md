# Version 0, step 1: New York City inputs loaded

Run 2026-11-23. Overture release 2026-11-18.0; parcels 26v2; NCES public 2024-25 and private 2023-24. Stop here for a sanity check before step 2.

## Inputs

| input | rows | note |
| --- | --- | --- |
| Overture places, kept categories | 9522 | inside the city |
| Borough boundaries | 5 | NYC Open Data wh2p-dxnf, water included |
| Parcel polygons | 858020 | DOF tax lots, NYC Open Data i38t-6if2 |
| Parcel records | 858284 | PLUTO, NYC Open Data 64uk-42ks |
| Polygons with a parcel record | 845560 | 98.5% of polygons |
| NCES public schools | 1885 | EDGE 2024-25 |
| NCES private schools | 539 | EDGE 2023-24 |

## Overture: counts by basic category

9,522 places in the kept categories; 6,277 (66%) carry a website.

| basic_category | places | pct_website | pct_phone | median_confidence |
| --- | --- | --- | --- | --- |
| christian_place_of_worship | 6445 | 67.0 | 89.0 | 0.92 |
| religious_organization | 1974 | 60.0 | 78.0 | 0.75 |
| jewish_place_of_worship | 564 | 74.0 | 91.0 | 0.92 |
| muslim_place_of_worship | 275 | 59.0 | 85.0 | 0.92 |
| hindu_place_of_worship | 115 | 54.0 | 78.0 | 0.92 |
| buddhist_place_of_worship | 99 | 63.0 | 91.0 | 0.92 |
| place_of_worship | 50 | 68.0 | 74.0 | 0.92 |

## Overture: confidence bands

Overture's confidence that the place exists. Low bands are candidates for a cutoff in step 2.

| band | places | closed |
| --- | --- | --- |
| a. under 0.50 | 885 | 1 |
| b. 0.50-0.69 | 1362 | 68 |
| c. 0.70-0.89 | 1151 | 4 |
| d. 0.90 and up | 6124 | 4 |

50 places sit inside the city but list a ZIP code outside NYC, a sign the point or the address is wrong.


## Overture: category by borough

| basic_category | Bronx | Brooklyn | Manhattan | Queens | Staten Island |
| --- | --- | --- | --- | --- | --- |
| buddhist_place_of_worship | 6 | 13 | 38 | 39 | 3 |
| christian_place_of_worship | 1217 | 2065 | 1199 | 1687 | 277 |
| hindu_place_of_worship | 9 | 8 | 7 | 90 | 1 |
| jewish_place_of_worship | 27 | 268 | 128 | 118 | 23 |
| muslim_place_of_worship | 54 | 79 | 32 | 99 | 11 |
| place_of_worship | 1 | 11 | 18 | 16 | 4 |
| religious_organization | 308 | 600 | 505 | 482 | 79 |

## Overture: detailed taxonomy within kept categories

| taxonomy_primary | basic_category | places |
| --- | --- | --- |
| christian_place_of_worship | christian_place_of_worship | 4953 |
| religious_organization | religious_organization | 1964 |
| jewish_place_of_worship | jewish_place_of_worship | 564 |
| baptist_place_of_worship | christian_place_of_worship | 491 |
| roman_catholic_place_of_worship | christian_place_of_worship | 478 |
| pentecostal_place_of_worship | christian_place_of_worship | 322 |
| muslim_place_of_worship | muslim_place_of_worship | 275 |
| hindu_place_of_worship | hindu_place_of_worship | 115 |
| buddhist_place_of_worship | buddhist_place_of_worship | 99 |
| protestant_place_of_worship | christian_place_of_worship | 96 |
| anglican_or_episcopal_place_of_worship | christian_place_of_worship | 52 |
| jehovahs_witness_place_of_worship | christian_place_of_worship | 39 |
| place_of_worship | place_of_worship | 35 |
| sikh_place_of_worship | place_of_worship | 15 |
| methodist_place_of_worship | christian_place_of_worship | 6 |
| seminary | religious_organization | 6 |
| lutheran_place_of_worship | christian_place_of_worship | 5 |
| monastery | religious_organization | 4 |
| greek_orthodox_place_of_worship | christian_place_of_worship | 1 |
| eastern_orthodox_place_of_worship | christian_place_of_worship | 1 |
| russian_orthodox_place_of_worship | christian_place_of_worship | 1 |

## Overture: operating status and source datasets

| operating_status | places |
| --- | --- |
| open | 7416 |
| (null) | 2029 |
| permanently_closed | 77 |

| source_dataset | places |
| --- | --- |
| Overture | 9522 |
| meta | 8205 |
| Overture-signals | 6948 |
| BrightQuery | 1004 |
| Foursquare | 323 |
| Microsoft | 36 |
| Birdeye | 1 |

## Overture: religious-looking places left out by the category filter

| taxonomy_primary | basic_category | places |
| --- | --- | --- |
| religious_school | place_of_learning | 177 |
| religious_and_spiritual_goods_store | specialty_store | 59 |

## Overture: 20 random places

In `v0/private/step1_samples.md` (not committed: it names places and addresses).

## Parcels: religious building classes

| bldgclass | label | lots | owner_type_x | bldg_area_sqft |
| --- | --- | --- | --- | --- |
| M1 | Church, synagogue, chapel | 3767 | 3201 | 54564122.0 |
| M2 | Mission house (non-residential) | 55 | 42 | 608832.0 |
| M3 | Parsonage, rectory | 495 | 441 | 3280047.0 |
| M4 | Convent | 122 | 105 | 1627864.0 |
| M9 | Miscellaneous religious facility | 1060 | 726 | 10860436.0 |

Land use 08 (public facilities and institutions): 12,055 lots. Owner type X (fully exempt, privately owned): 20,390 lots.

## Schools by borough

| source | Bronx | Brooklyn | Manhattan | Queens | Staten Island |
| --- | --- | --- | --- | --- | --- |
| nces_private | 52 | 229 | 117 | 118 | 23 |
| nces_public | 471 | 582 | 353 | 392 | 87 |

Five random schools of each kind:

| source | name | street | borough |
| --- | --- | --- | --- |
| nces_private | BETH RIVHAK SCHOOL | 470 LEFFERTS AVE | Brooklyn |
| nces_private | HADAR BET YAAKOV | 193 PECK AVE # 10 | Queens |
| nces_private | LITTLE ANGEL DAYCARE CENTER #3 | 12 CROWN ST | Brooklyn |
| nces_private | MARY BOBB LEARNING ACADEMY | 1187 NOSTRAND AVE | Brooklyn |
| nces_private | SMILES AROUND US ACADEMY | 351 SAND LN | Staten Island |
| nces_public | ACADEMY FOR PERSONAL LEADERSHIP AND EXCELLENCE | 120 E 184TH ST | Bronx |
| nces_public | BRONX SCHOOL FOR LAW GOVERNMENT AND JUSTICE | 244 E 163RD ST | Bronx |
| nces_public | JHS 217 ROBERT A VAN WYCK | 85-05 144TH ST | Queens |
| nces_public | PS 68 | 4011 MONTICELLO AVE | Bronx |
| nces_public | RIVERDALE AVENUE MIDDLE SCHOOL | 76 RIVERDALE AVE | Brooklyn |

## Files

- DuckDB: `data/nyc/nyc_v0.duckdb` (tables boroughs, city, overture_nyc, pluto, taxlots, parcels, schools; view places)
- Overture extract: `data/nyc/raw/overture_places_2026-11-18.0_nyc.parquet`
- Raw downloads: `data/nyc/raw/` (not committed)
