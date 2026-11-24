# Version 0, step 1: Charlotte, NC inputs loaded

Run 2026-11-24. Overture release 2026-11-18.0; parcels Mecklenburg Parcel_Landuse; NCES public 2024-25 and private 2023-24. Stop here for a sanity check before step 2.

## Inputs

| input | rows | note |
| --- | --- | --- |
| Overture places, kept categories | 1556 | inside the city |
| Council district boundaries | 7 | Mecklenburg GIS, Charlotte City Council Districts |
| Parcel polygons | 333995 | Mecklenburg Parcel_Landuse polygons |
| Parcel records | 290634 | land use, owner, exemption |
| Polygons with a parcel record | 333995 | 100.0% of polygons |
| NCES public schools | 175 | EDGE 2024-25 |
| NCES private schools | 50 | EDGE 2023-24 |

## Overture: counts by basic category

1,556 places in the kept categories; 1,114 (72%) carry a website.

| basic_category | places | pct_website | pct_phone | median_confidence |
| --- | --- | --- | --- | --- |
| christian_place_of_worship | 1152 | 73.0 | 91.0 | 0.92 |
| religious_organization | 361 | 68.0 | 75.0 | 0.74 |
| muslim_place_of_worship | 15 | 67.0 | 93.0 | 0.92 |
| buddhist_place_of_worship | 11 | 36.0 | 91.0 | 0.92 |
| place_of_worship | 8 | 75.0 | 88.0 | 0.7 |
| jewish_place_of_worship | 7 | 86.0 | 100.0 | 0.92 |
| hindu_place_of_worship | 2 | 50.0 | 100.0 | 0.68 |

## Overture: confidence bands

Overture's confidence that the place exists. Low bands are candidates for a cutoff in step 2.

| band | places | closed |
| --- | --- | --- |
| a. under 0.50 | 139 | 0 |
| b. 0.50-0.69 | 259 | 20 |
| c. 0.70-0.89 | 216 | 2 |
| d. 0.90 and up | 942 | 1 |

30 places sit inside the city but list a ZIP code outside Charlotte, a sign the point or the address is wrong.


## Overture: category by council district

| basic_category | District 1 | District 2 | District 3 | District 4 | District 5 | District 6 | District 7 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| buddhist_place_of_worship | 0 | 5 | 2 | 2 | 2 | 0 | 0 |
| christian_place_of_worship | 278 | 240 | 197 | 107 | 178 | 90 | 62 |
| hindu_place_of_worship | 0 | 0 | 1 | 0 | 1 | 0 | 0 |
| jewish_place_of_worship | 0 | 0 | 0 | 0 | 0 | 6 | 1 |
| muslim_place_of_worship | 5 | 3 | 0 | 2 | 5 | 0 | 0 |
| place_of_worship | 4 | 2 | 0 | 1 | 0 | 1 | 0 |
| religious_organization | 82 | 66 | 59 | 30 | 69 | 32 | 23 |

## Overture: detailed taxonomy within kept categories

| taxonomy_primary | basic_category | places |
| --- | --- | --- |
| christian_place_of_worship | christian_place_of_worship | 937 |
| religious_organization | religious_organization | 360 |
| baptist_place_of_worship | christian_place_of_worship | 120 |
| pentecostal_place_of_worship | christian_place_of_worship | 32 |
| anglican_or_episcopal_place_of_worship | christian_place_of_worship | 23 |
| roman_catholic_place_of_worship | christian_place_of_worship | 17 |
| muslim_place_of_worship | muslim_place_of_worship | 15 |
| protestant_place_of_worship | christian_place_of_worship | 14 |
| buddhist_place_of_worship | buddhist_place_of_worship | 11 |
| place_of_worship | place_of_worship | 7 |
| jewish_place_of_worship | jewish_place_of_worship | 7 |
| methodist_place_of_worship | christian_place_of_worship | 4 |
| hindu_place_of_worship | hindu_place_of_worship | 2 |
| lutheran_place_of_worship | christian_place_of_worship | 2 |
| jehovahs_witness_place_of_worship | christian_place_of_worship | 2 |
| russian_orthodox_place_of_worship | christian_place_of_worship | 1 |
| seminary | religious_organization | 1 |
| sikh_place_of_worship | place_of_worship | 1 |

## Overture: operating status and source datasets

| operating_status | places |
| --- | --- |
| open | 1178 |
| (null) | 355 |
| permanently_closed | 23 |

| source_dataset | places |
| --- | --- |
| Overture | 1556 |
| meta | 1335 |
| Overture-signals | 1107 |
| BrightQuery | 162 |
| Foursquare | 62 |
| Microsoft | 2 |
| Uberall | 1 |

## Overture: religious-looking places left out by the category filter

| taxonomy_primary | basic_category | places |
| --- | --- | --- |
| religious_school | place_of_learning | 11 |
| religious_and_spiritual_goods_store | specialty_store | 3 |

## Overture: 20 random places

In `v0/charlotte/private/step1_samples.md` (not committed: it names places and addresses).


## Parcels: religious building classes

| bldgclass | label | lots | owner_type_x | bldg_area_sqft |
| --- | --- | --- | --- | --- |
| M1 | Church, synagogue, chapel | 645 | 612 |  |
| M9 | Miscellaneous religious facility | 660 | 660 |  |

Land use 08 (public facilities and institutions): 2,965 lots. Owner type X (fully exempt, privately owned): 13,504 lots.

## Schools by council district

| source | District 1 | District 2 | District 3 | District 4 | District 5 | District 6 | District 7 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| nces_private | 12 | 4 | 3 | 2 | 8 | 12 | 9 |
| nces_public | 32 | 26 | 32 | 22 | 24 | 20 | 19 |

Five random schools of each kind:

| source | name | street | borough |
| --- | --- | --- | --- |
| nces_private | BRTISH INTERNATIONAL SCHOOL OF CHARLOTTE | 7000 ENDHAVEN LN | District 7 |
| nces_private | CHARLOTTE PREPARATORY SCHOOL | 212 BOYCE RD | District 6 |
| nces_private | EMERALD SCHOOL OF EXCELLENCE | 4012 CENTRAL AVE | District 5 |
| nces_private | INTELLICOR INTERNATIONAL ACADEMY | 4301 SHAMROCK DR | District 1 |
| nces_private | OUR LADY OF THE ASSUMPTION SCHOOL | 4225 SHAMROCK DR | District 1 |
| nces_public | Albemarle Road Elementary | 7800 Riding Trail Rd | District 5 |
| nces_public | Endhaven Elementary | 6815 Endhaven Ln | District 7 |
| nces_public | Mallard Creek High School | 3825 Johnston Oehler Rd | District 4 |
| nces_public | Oakdale Elementary | 1825 Oakdale Rd | District 2 |
| nces_public | Providence High School | 1800 Pineville-Matthews Rd | District 7 |

## Files

- DuckDB: `data/charlotte/charlotte_v0.duckdb` (tables boroughs, city, overture_nyc, pluto, taxlots, parcels, schools; view places)
- Overture extract: `data/charlotte/raw/overture_places_2026-11-18.0_charlotte.parquet`
- Raw downloads: `data/charlotte/raw/` (not committed)
