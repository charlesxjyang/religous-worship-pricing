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

## Overture: 20 random places (seed 20261122)

| name | category | borough | address | website | conf | status |
| --- | --- | --- | --- | --- | --- | --- |
| Casa De Restauracion | christian_place_of_worship | Bronx | 814 E 182nd St | http://casaderestauracionnyc.com | 0.92 | open |
| GAN ATID | religious_organization | Bronx | 1969 Haight Ave | http://Ganatid.org/ | 0.93 | open |
| Life Church Assembly | christian_place_of_worship | Bronx | 1595 E 174th St |  | 0.95 | open |
| Praying Partners International Ministry | christian_place_of_worship | Bronx | 1057 E 227th St | http://prayingpartnersintl.org/ | 0.92 | open |
| The United House of Prayer for All People | religious_organization | Bronx | 1326 Boston Rd |  | 0.99 | open |
| Church Avenue Merchants Block Association | christian_place_of_worship | Brooklyn | 2402 Atlantic Ave | http://www.camba.org/ | 0.53 |  |
| Cypress Hills Hispanic SDA Church | christian_place_of_worship | Brooklyn | 3427 Fulton St |  | 0.21 |  |
| Family & Friends Worship Ctr | religious_organization | Brooklyn | 836 Quincy St |  | 0.91 |  |
| Ocean Avenue Jewish Center | jewish_place_of_worship | Brooklyn | 2592 Ocean Ave | http://oajc.org | 0.99 | open |
| The New Creation Church Of God | christian_place_of_worship | Brooklyn | 1228 Brooklyn Ave |  | 0.92 | open |
| Victory Shiloh Apostolic Inc | pentecostal_place_of_worship | Brooklyn | 9617 Avenue L |  | 0.99 | open |
| Exilic Church | christian_place_of_worship | Manhattan | 240 W 37th St Fl 2 | http://www.exilic.com/ | 0.99 | open |
| Holy Spirit Ukrainian Catholic Cemetery | roman_catholic_place_of_worship | Manhattan | 141 Sarah Wells Trl | http://holyspirit-saintandrew.org | 0.86 | open |
| SAJ-Judaism that Stands for All | jewish_place_of_worship | Manhattan | 15 W 86th St | https://saj.nyc/ | 1.0 | open |
| Bridge Fellowship International | christian_place_of_worship | Queens | 45-04 48th Ave | https://www.facebook.com/BRIDGEFELLOWSHIPNY/ | 0.92 | open |
| Harvest Revival Christian Fellowship | christian_place_of_worship | Queens | 119-33 Springfield Blvd | http://www.harvestrevival.org | 0.99 | open |
| Immaculate Conception of Jamaica | christian_place_of_worship | Queens | 86-16 Midland Pkwy | http://www.icsalumni.org | 0.54 |  |
| Masjid Omar Ben Abdel-Aziz | muslim_place_of_worship | Queens | 88-29 161st St | http://www.mobaatif.com/ | 0.97 | open |
| QTEC Community Center | religious_organization | Queens | 40-32 166th St | http://www.qtecny.org/#!connect/czpl | 0.91 | open |
| Tabernacle Of Grace Int. | christian_place_of_worship | Queens | 220-07 Merrick Blvd |  | 0.92 | open |

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
