# Version 0, step 1: Washington, DC inputs loaded

Run 2026-11-23. Overture release 2026-11-18.0; parcels ITSPE 2026-08-03; NCES public 2024-25 and private 2023-24. Stop here for a sanity check before step 2.

## Inputs

| input | rows | note |
| --- | --- | --- |
| Overture places, kept categories | 1300 | inside the city |
| Ward boundaries | 8 | DCGIS Ward - 2022 |
| Parcel polygons | 137394 | DC OTR owner polygons |
| Parcel records | 137383 | ITSPE, with RPTA tax exemptions |
| Polygons with a parcel record | 132995 | 96.8% of polygons |
| NCES public schools | 246 | EDGE 2024-25 |
| NCES private schools | 50 | EDGE 2023-24 |

## Overture: counts by basic category

1,300 places in the kept categories; 994 (76%) carry a website.

| basic_category | places | pct_website | pct_phone | median_confidence |
| --- | --- | --- | --- | --- |
| christian_place_of_worship | 995 | 77.0 | 93.0 | 0.92 |
| religious_organization | 261 | 73.0 | 85.0 | 0.77 |
| jewish_place_of_worship | 16 | 94.0 | 88.0 | 0.95 |
| muslim_place_of_worship | 14 | 79.0 | 79.0 | 0.93 |
| buddhist_place_of_worship | 7 | 71.0 | 86.0 | 0.87 |
| place_of_worship | 6 | 100.0 | 100.0 | 0.92 |
| hindu_place_of_worship | 1 | 0.0 | 100.0 | 0.39 |

## Overture: confidence bands

Overture's confidence that the place exists. Low bands are candidates for a cutoff in step 2.

| band | places | closed |
| --- | --- | --- |
| a. under 0.50 | 134 | 1 |
| b. 0.50-0.69 | 177 | 18 |
| c. 0.70-0.89 | 142 | 1 |
| d. 0.90 and up | 847 | 1 |

10 places sit inside the city but list a ZIP code outside DC, a sign the point or the address is wrong.


## Overture: category by ward

| basic_category | Ward 1 | Ward 2 | Ward 3 | Ward 4 | Ward 5 | Ward 6 | Ward 7 | Ward 8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| buddhist_place_of_worship | 0 | 2 | 0 | 4 | 1 | 0 | 0 | 0 |
| christian_place_of_worship | 62 | 145 | 64 | 148 | 161 | 141 | 172 | 102 |
| hindu_place_of_worship | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| jewish_place_of_worship | 0 | 5 | 4 | 4 | 0 | 1 | 2 | 0 |
| muslim_place_of_worship | 1 | 3 | 0 | 1 | 3 | 1 | 5 | 0 |
| place_of_worship | 0 | 2 | 1 | 1 | 0 | 1 | 0 | 1 |
| religious_organization | 16 | 52 | 20 | 32 | 64 | 35 | 23 | 19 |

## Overture: detailed taxonomy within kept categories

| taxonomy_primary | basic_category | places |
| --- | --- | --- |
| christian_place_of_worship | christian_place_of_worship | 664 |
| religious_organization | religious_organization | 256 |
| baptist_place_of_worship | christian_place_of_worship | 208 |
| roman_catholic_place_of_worship | christian_place_of_worship | 67 |
| anglican_or_episcopal_place_of_worship | christian_place_of_worship | 22 |
| pentecostal_place_of_worship | christian_place_of_worship | 19 |
| jewish_place_of_worship | jewish_place_of_worship | 16 |
| muslim_place_of_worship | muslim_place_of_worship | 14 |
| buddhist_place_of_worship | buddhist_place_of_worship | 7 |
| methodist_place_of_worship | christian_place_of_worship | 6 |
| protestant_place_of_worship | christian_place_of_worship | 6 |
| place_of_worship | place_of_worship | 4 |
| seminary | religious_organization | 3 |
| sikh_place_of_worship | place_of_worship | 2 |
| monastery | religious_organization | 2 |
| lutheran_place_of_worship | christian_place_of_worship | 1 |
| jehovahs_witness_place_of_worship | christian_place_of_worship | 1 |
| hindu_place_of_worship | hindu_place_of_worship | 1 |
| eastern_orthodox_place_of_worship | christian_place_of_worship | 1 |

## Overture: operating status and source datasets

| operating_status | places |
| --- | --- |
| open | 1056 |
| (null) | 223 |
| permanently_closed | 21 |

| source_dataset | places |
| --- | --- |
| Overture | 1300 |
| meta | 1022 |
| Overture-signals | 963 |
| BrightQuery | 235 |
| Foursquare | 51 |

## Overture: religious-looking places left out by the category filter

| taxonomy_primary | basic_category | places |
| --- | --- | --- |
| religious_school | place_of_learning | 12 |

## Overture: 20 random places

In `v0/dc/private/step1_samples.md` (not committed: it names places and addresses).

## Parcels: religious building classes

| bldgclass | label | lots | owner_type_x | bldg_area_sqft |
| --- | --- | --- | --- | --- |
| M1 | Church, synagogue, chapel | 675 | 609 |  |
| M9 | Miscellaneous religious facility | 560 | 560 |  |

Land use 08 (public facilities and institutions): 2,545 lots. Owner type X (fully exempt, privately owned): 9,582 lots.

## Schools by ward

| source | Ward 1 | Ward 2 | Ward 3 | Ward 4 | Ward 5 | Ward 6 | Ward 7 | Ward 8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nces_private | 3 | 6 | 18 | 6 | 8 | 3 | 4 | 2 |
| nces_public | 13 | 18 | 12 | 36 | 49 | 24 | 47 | 47 |

Five random schools of each kind:

| source | name | street | borough |
| --- | --- | --- | --- |
| nces_private | ARCHBISHOP CARROLL HIGH SCHOOL | 4300 HAREWOOD RD | Ward 5 |
| nces_private | RIVER SCHOOL | 4880 MACARTHUR BLVD NW | Ward 3 |
| nces_private | SAN MIGUEL SCHOOL | 7705 GEORGIA AVE NW | Ward 4 |
| nces_private | SIDWELL FRIENDS SCHOOL | 3825 WISCONSIN AVE NW | Ward 3 |
| nces_private | ST ANTHONY CATHOLIC SCHOOL | 3400 12TH ST NE | Ward 5 |
| nces_public | Hope Community PCS - Tolson | 2917 8TH STREET NE | Ward 5 |
| nces_public | Seaton ES | 1503 10th St. NW | Ward 2 |
| nces_public | The Sojourner Truth School PCS | 1800 PERRY STREET NE | Ward 5 |
| nces_public | Washington Global PCS | 525 SCHOOL STREET SW | Ward 6 |
| nces_public | Whittier ES | 6201 5th St. NW | Ward 4 |

## Files

- DuckDB: `data/dc/dc_v0.duckdb` (tables boroughs, city, overture_nyc, pluto, taxlots, parcels, schools; view places)
- Overture extract: `data/dc/raw/overture_places_2026-11-18.0_dc.parquet`
- Raw downloads: `data/dc/raw/` (not committed)
