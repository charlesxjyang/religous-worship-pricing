# Version 0, step 1: San Francisco, CA inputs loaded

Run 2026-11-24. Overture release 2026-11-18.0; parcels SF secured roll 2025; NCES public 2024-25 and private 2023-24. Stop here for a sanity check before step 2.

## Inputs

| input | rows | note |
| --- | --- | --- |
| Overture places, kept categories | 867 | inside the city |
| Supervisor district boundaries | 11 | DataSF Supervisor Districts (2022) |
| Parcel polygons | 155029 | DataSF active parcels |
| Parcel records | 155029 | Assessor secured roll 2025 (no owner names) |
| Polygons with a parcel record | 154051 | 99.4% of polygons |
| NCES public schools | 132 | EDGE 2024-25 |
| NCES private schools | 89 | EDGE 2023-24 |

## Overture: counts by basic category

867 places in the kept categories; 630 (73%) carry a website.

| basic_category | places | pct_website | pct_phone | median_confidence |
| --- | --- | --- | --- | --- |
| christian_place_of_worship | 622 | 75.0 | 91.0 | 0.92 |
| religious_organization | 166 | 59.0 | 75.0 | 0.72 |
| buddhist_place_of_worship | 38 | 74.0 | 92.0 | 0.92 |
| jewish_place_of_worship | 23 | 100.0 | 96.0 | 0.92 |
| muslim_place_of_worship | 10 | 60.0 | 70.0 | 0.92 |
| hindu_place_of_worship | 4 | 100.0 | 75.0 | 0.93 |
| place_of_worship | 4 | 50.0 | 50.0 | 0.71 |

## Overture: confidence bands

Overture's confidence that the place exists. Low bands are candidates for a cutoff in step 2.

| band | places | closed |
| --- | --- | --- |
| a. under 0.50 | 88 | 1 |
| b. 0.50-0.69 | 117 | 5 |
| c. 0.70-0.89 | 85 | 0 |
| d. 0.90 and up | 577 | 1 |

5 places sit inside the city but list a ZIP code outside SF, a sign the point or the address is wrong.


## Overture: category by supervisor district

| basic_category | District 1 | District 10 | District 11 | District 2 | District 3 | District 4 | District 5 | District 6 | District 7 | District 8 | District 9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| buddhist_place_of_worship | 3 | 1 | 2 | 1 | 10 | 6 | 8 | 1 | 0 | 2 | 4 |
| christian_place_of_worship | 43 | 89 | 64 | 52 | 53 | 44 | 61 | 35 | 56 | 48 | 77 |
| hindu_place_of_worship | 0 | 1 | 0 | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| jewish_place_of_worship | 7 | 0 | 0 | 1 | 4 | 3 | 0 | 1 | 3 | 2 | 2 |
| muslim_place_of_worship | 0 | 1 | 1 | 0 | 1 | 0 | 5 | 0 | 1 | 0 | 1 |
| place_of_worship | 0 | 1 | 0 | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| religious_organization | 10 | 17 | 22 | 17 | 17 | 10 | 14 | 11 | 17 | 13 | 18 |

## Overture: detailed taxonomy within kept categories

| taxonomy_primary | basic_category | places |
| --- | --- | --- |
| christian_place_of_worship | christian_place_of_worship | 458 |
| religious_organization | religious_organization | 166 |
| baptist_place_of_worship | christian_place_of_worship | 70 |
| roman_catholic_place_of_worship | christian_place_of_worship | 58 |
| buddhist_place_of_worship | buddhist_place_of_worship | 38 |
| jewish_place_of_worship | jewish_place_of_worship | 23 |
| pentecostal_place_of_worship | christian_place_of_worship | 15 |
| muslim_place_of_worship | muslim_place_of_worship | 10 |
| protestant_place_of_worship | christian_place_of_worship | 7 |
| anglican_or_episcopal_place_of_worship | christian_place_of_worship | 7 |
| hindu_place_of_worship | hindu_place_of_worship | 4 |
| lutheran_place_of_worship | christian_place_of_worship | 3 |
| place_of_worship | place_of_worship | 3 |
| jehovahs_witness_place_of_worship | christian_place_of_worship | 2 |
| sikh_place_of_worship | place_of_worship | 1 |
| methodist_place_of_worship | christian_place_of_worship | 1 |
| eastern_orthodox_place_of_worship | christian_place_of_worship | 1 |

## Overture: operating status and source datasets

| operating_status | places |
| --- | --- |
| open | 679 |
| (null) | 181 |
| permanently_closed | 7 |

| source_dataset | places |
| --- | --- |
| Overture | 867 |
| meta | 726 |
| Overture-signals | 629 |
| BrightQuery | 107 |
| Foursquare | 35 |
| Microsoft | 2 |

## Overture: religious-looking places left out by the category filter

| taxonomy_primary | basic_category | places |
| --- | --- | --- |
| religious_school | place_of_learning | 8 |
| religious_and_spiritual_goods_store | specialty_store | 2 |

## Overture: 20 random places

In `v0/sf/private/step1_samples.md` (not committed: it names places and addresses).


## Parcels: religious building classes

| bldgclass | label | lots | owner_type_x | bldg_area_sqft |
| --- | --- | --- | --- | --- |
| M1 | Church, synagogue, chapel | 511 | 446 | 3476370.0 |
| M9 | Miscellaneous religious facility | 164 | 163 | 607194.0 |

Land use 08 (public facilities and institutions): 1,541 lots. Owner type X (fully exempt, privately owned): 1,695 lots.

## Schools by supervisor district

| source | District 1 | District 10 | District 11 | District 2 | District 3 | District 4 | District 5 | District 6 | District 7 | District 8 | District 9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nces_private | 9 | 5 | 5 | 15 | 5 | 6 | 8 | 4 | 10 | 11 | 11 |
| nces_public | 9 | 18 | 12 | 10 | 12 | 12 | 12 | 4 | 11 | 16 | 16 |

Five random schools of each kind:

| source | name | street | borough |
| --- | --- | --- | --- |
| nces_private | HILLWOOD ACADEMIC DAY SCHOOL | 2521 SCOTT ST | District 2 |
| nces_private | KAHLON FAMILY SERVICES SCHOOL | 3140 BALBOA ST | District 1 |
| nces_private | ST IGNATIUS COLLEGE PREPARATORY | 2001 37TH AVE | District 4 |
| nces_private | STS PETER & PAUL SCHOOL | 660 FILBERT ST | District 3 |
| nces_private | THE BAY SCHOOL OF SAN FRANCISCO | 35 KEYES AVE | District 2 |
| nces_public | Clarendon Alternative Elementary | 500 Clarendon Ave. | District 7 |
| nces_public | O'Connell (John) High | 2355 Folsom St. | District 9 |
| nces_public | San Miguel Children Center | 300 Seneca Ave. | District 11 |
| nces_public | Stockton (Commodore) Children Center | 1 Trenton St. | District 3 |
| nces_public | Sunset Elementary | 1920 41st Ave. | District 4 |

## Files

- DuckDB: `data/sf/sf_v0.duckdb` (tables boroughs, city, overture_nyc, pluto, taxlots, parcels, schools; view places)
- Overture extract: `data/sf/raw/overture_places_2026-11-18.0_sf.parquet`
- Raw downloads: `data/sf/raw/` (not committed)
