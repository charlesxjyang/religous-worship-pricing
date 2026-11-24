# Version 0, step 1: Houston, TX inputs loaded

Run 2026-11-24. Overture release 2026-11-18.0; parcels HCAD 2026; NCES public 2024-25 and private 2023-24. Stop here for a sanity check before step 2.

## Inputs

| input | rows | note |
| --- | --- | --- |
| Overture places, kept categories | 5082 | inside the city |
| Council district boundaries | 11 | City of Houston council districts |
| Parcel polygons | 655407 | HCAD parcels in the city limits |
| Parcel records | 655407 | HCAD 2026 appraisal roll |
| Polygons with a parcel record | 655407 | 100.0% of polygons |
| NCES public schools | 640 | EDGE 2024-25 |
| NCES private schools | 166 | EDGE 2023-24 |

## Overture: counts by basic category

5,082 places in the kept categories; 3,234 (64%) carry a website.

| basic_category | places | pct_website | pct_phone | median_confidence |
| --- | --- | --- | --- | --- |
| christian_place_of_worship | 3880 | 65.0 | 89.0 | 0.92 |
| religious_organization | 1042 | 59.0 | 78.0 | 0.73 |
| muslim_place_of_worship | 62 | 66.0 | 82.0 | 0.92 |
| buddhist_place_of_worship | 30 | 67.0 | 87.0 | 0.92 |
| jewish_place_of_worship | 24 | 92.0 | 92.0 | 0.96 |
| hindu_place_of_worship | 23 | 83.0 | 100.0 | 0.98 |
| place_of_worship | 21 | 67.0 | 71.0 | 0.92 |

## Overture: confidence bands

Overture's confidence that the place exists. Low bands are candidates for a cutoff in step 2.

| band | places | closed |
| --- | --- | --- |
| a. under 0.50 | 513 | 2 |
| b. 0.50-0.69 | 778 | 54 |
| c. 0.70-0.89 | 648 | 4 |
| d. 0.90 and up | 3143 | 1 |

423 places sit inside the city but list a ZIP code outside Houston, a sign the point or the address is wrong.


## Overture: category by council district

| basic_category | District A | District B | District C | District D | District E | District F | District G | District H | District I | District J | District K |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| buddhist_place_of_worship | 3 | 2 | 1 | 3 | 1 | 13 | 1 | 1 | 2 | 2 | 1 |
| christian_place_of_worship | 396 | 932 | 196 | 470 | 230 | 362 | 134 | 389 | 283 | 210 | 278 |
| hindu_place_of_worship | 4 | 1 | 1 | 1 | 0 | 7 | 2 | 0 | 0 | 3 | 4 |
| jewish_place_of_worship | 0 | 2 | 11 | 1 | 1 | 1 | 3 | 0 | 0 | 0 | 5 |
| muslim_place_of_worship | 4 | 7 | 1 | 6 | 6 | 16 | 2 | 2 | 3 | 12 | 3 |
| place_of_worship | 1 | 3 | 4 | 3 | 1 | 4 | 0 | 4 | 0 | 0 | 1 |
| religious_organization | 125 | 188 | 73 | 100 | 58 | 107 | 38 | 99 | 87 | 81 | 86 |

## Overture: detailed taxonomy within kept categories

| taxonomy_primary | basic_category | places |
| --- | --- | --- |
| christian_place_of_worship | christian_place_of_worship | 2894 |
| religious_organization | religious_organization | 1040 |
| baptist_place_of_worship | christian_place_of_worship | 650 |
| pentecostal_place_of_worship | christian_place_of_worship | 125 |
| roman_catholic_place_of_worship | christian_place_of_worship | 101 |
| muslim_place_of_worship | muslim_place_of_worship | 62 |
| protestant_place_of_worship | christian_place_of_worship | 52 |
| buddhist_place_of_worship | buddhist_place_of_worship | 30 |
| jewish_place_of_worship | jewish_place_of_worship | 24 |
| anglican_or_episcopal_place_of_worship | christian_place_of_worship | 23 |
| hindu_place_of_worship | hindu_place_of_worship | 23 |
| jehovahs_witness_place_of_worship | christian_place_of_worship | 20 |
| place_of_worship | place_of_worship | 20 |
| methodist_place_of_worship | christian_place_of_worship | 12 |
| lutheran_place_of_worship | christian_place_of_worship | 3 |
| seminary | religious_organization | 2 |
| sikh_place_of_worship | place_of_worship | 1 |

## Overture: operating status and source datasets

| operating_status | places |
| --- | --- |
| open | 3920 |
| (null) | 1101 |
| permanently_closed | 61 |

| source_dataset | places |
| --- | --- |
| Overture | 5082 |
| meta | 4343 |
| Overture-signals | 3656 |
| BrightQuery | 578 |
| Foursquare | 158 |
| Microsoft | 13 |

## Overture: religious-looking places left out by the category filter

| taxonomy_primary | basic_category | places |
| --- | --- | --- |
| religious_school | place_of_learning | 42 |
| religious_and_spiritual_goods_store | specialty_store | 10 |

## Overture: 20 random places

In `v0/houston/private/step1_samples.md` (not committed: it names places and addresses).


## Parcels: religious building classes

| bldgclass | label | lots | owner_type_x | bldg_area_sqft |
| --- | --- | --- | --- | --- |
| M1 | Church, synagogue, chapel | 1057 | 883 | 12745848.0 |
| M9 | Miscellaneous religious facility | 4564 | 4564 | 4173952.0 |

Land use 08 (public facilities and institutions): 27,253 lots. Owner type X (fully exempt, privately owned): 21,466 lots.

## Schools by council district

| source | District A | District B | District C | District D | District E | District F | District G | District H | District I | District J | District K |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nces_private | 26 | 9 | 23 | 7 | 15 | 22 | 29 | 8 | 4 | 13 | 10 |
| nces_public | 46 | 90 | 40 | 61 | 60 | 51 | 27 | 73 | 74 | 60 | 58 |

Five random schools of each kind:

| source | name | street | borough |
| --- | --- | --- | --- |
| nces_private | CREATIVE CORNER | 335 AUDRY LN | District E |
| nces_private | CROSS POINT PRESCHOOL KATY | 700 WESTGREEN BLVD | District F |
| nces_private | DUCHESNE ACADEMY OF THE SACRED HEART | 10202 MEMORIAL DR | District A |
| nces_private | LA MATERNELLE FRENCH ACADEMY | 2301 S DAIRY ASHFORD RD STE A | District G |
| nces_private | ST AUGUSTINE CATHOLIC SCHOOL | 5500 LAUREL CREEK WAY | District E |
| nces_public | CLIFTON MIDDLE | 6001 GOLDEN FOREST DR | District A |
| nces_public | RICHARD MILBURN ACADEMY HOUSTON (SUBURBAN) | 500 CENTURY PLAZA DR STE 180 | District B |
| nces_public | SHARPSTOWN H S | 7504 BISSONNET ST | District J |
| nces_public | TINSLEY EL | 11035 BOB WHITE | District K |
| nces_public | YES PREP - BRAYS OAKS | 9000 W BELLFORT ST | District J |

## Files

- DuckDB: `data/houston/houston_v0.duckdb` (tables boroughs, city, overture_nyc, pluto, taxlots, parcels, schools; view places)
- Overture extract: `data/houston/raw/overture_places_2026-11-18.0_houston.parquet`
- Raw downloads: `data/houston/raw/` (not committed)
