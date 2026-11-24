# Services and building use in NYC: first pass

Run 2026-11-24. Of 6,897 congregations, 1,702 have a website that matched their listing and 1,280 posted weekly main services that extraction found, with a quote on the page for each. Everything below is about those congregations; they are likely larger and better established than those without a website or schedule.

## Multi-use and services, by tradition

Multi-use counts the uses sharing the building a congregation gathers in: 1 per congregation on the lot, +1 for a school that is not its own (public, charter, independent, college), +1 when the building's main use is not religious (store, office, home, apartments over stores, industrial, hall). A church alone in its own building is 1.0; with a guest congregation or a charter school, or as a storefront church, 2.0. The service columns cover congregations that posted a schedule.

| tradition | congregations | mean_uses | pct_one_use | pct_two_uses | pct_three_plus | with_schedule | mean_main_services | pct_2plus_services | mean_hours_week |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Protestant and other Christian | 4967 | 1.71 | 44.0 | 45.0 | 11.0 | 950 | 1.3 | 22.0 | 3.1 |
| Jewish | 487 | 1.48 | 60.0 | 35.0 | 5.0 | 93 | 1.7 | 55.0 | 5.2 |
| Catholic | 438 | 1.34 | 69.0 | 28.0 | 3.0 | 135 | 3.4 | 87.0 | 8.2 |
| Unknown | 286 | 1.91 | 28.0 | 59.0 | 13.0 | 2 | 1.0 | 0.0 | 1.8 |
| Muslim | 233 | 1.62 | 42.0 | 53.0 | 5.0 | 19 | 1.3 | 21.0 | 5.1 |
| Hindu | 96 | 1.66 | 42.0 | 53.0 | 5.0 | 5 | 1.0 | 0.0 | 7.8 |
| Buddhist | 77 | 1.64 | 48.0 | 42.0 | 10.0 | 4 | 1.0 | 0.0 | 6.5 |
| Orthodox Christian | 52 | 1.37 | 69.0 | 25.0 | 6.0 | 30 | 1.2 | 17.0 | 4.7 |

By borough, all traditions (service columns as above):

| borough | congregations | mean_uses | pct_multi_use | with_schedule | mean_main_services | pct_2plus_services |
| --- | --- | --- | --- | --- | --- | --- |
| Bronx | 1181 | 1.76 | 58.0 | 141 | 1.3 | 17.0 |
| Brooklyn | 2200 | 1.59 | 50.0 | 366 | 1.5 | 29.0 |
| Manhattan | 1185 | 1.71 | 54.0 | 305 | 1.5 | 32.0 |
| Queens | 1800 | 1.7 | 56.0 | 354 | 1.8 | 38.0 |
| Staten Island | 284 | 1.54 | 46.0 | 73 | 1.5 | 33.0 |

Multi-use within each kind of building:

| building_group | congregations | mean_uses | max_uses |
| --- | --- | --- | --- |
| single-use religious building | 2896 | 1.0 | 1 |
| other-use building | 2793 | 2.15 | 7 |
| shared religious building | 961 | 2.29 | 5 |

## Who has a schedule

| building_group | congregations | with_matched_site | with_schedule | pct_with_schedule |
| --- | --- | --- | --- | --- |
| single-use religious building | 2896 | 879 | 679 | 23.0 |
| other-use building | 2793 | 493 | 345 | 12.0 |
| shared religious building | 961 | 273 | 215 | 22.0 |

## Single-use religious buildings: services per week, within tradition

One congregation in its own religious building. Several main services, especially on the same day, means the building is used more intensively than one service a week.

| tradition | with_schedule | mean_main | median_main | pct_one | pct_two | pct_three_plus | pct_2plus_same_day | pct_2plus_languages | mean_hours_week |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Protestant and other Christian | 479 | 1.3 | 1.0 | 77.0 | 17.0 | 5.0 | 22.0 | 6.0 | 3.2 |
| Catholic | 103 | 3.4 | 3.0 | 12.0 | 20.0 | 68.0 | 77.0 | 41.0 | 8.0 |
| Jewish | 58 | 1.8 | 2.0 | 48.0 | 40.0 | 12.0 | 19.0 | 0.0 | 5.4 |
| Orthodox Christian | 21 | 1.1 | 1.0 | 90.0 | 10.0 | 0.0 | 5.0 | 0.0 | 4.3 |

## The same, by kind of building

Main services per congregation, within tradition. A guest congregation in a shared building counts its own services, not its host's.

| tradition | other-use building | shared religious building | single-use religious building |
| --- | --- | --- | --- |
| Catholic | 2.9 | 4.4 | 3.4 |
| Jewish | 1.6 | 1.8 | 1.8 |
| Muslim | 1.3 | 1.0 | 1.4 |
| Orthodox Christian | 1.4 | 1.0 | 1.1 |
| Protestant and other Christian | 1.3 | 1.2 | 1.3 |

Share holding two or more main services:

| tradition | other-use building | shared religious building | single-use religious building |
| --- | --- | --- | --- |
| Catholic | 72.0 | 100.0 | 88.0 |
| Jewish | 54.0 | 73.0 | 52.0 |
| Muslim | 14.0 | 0.0 | 27.0 |
| Orthodox Christian | 38.0 | 0.0 | 10.0 |
| Protestant and other Christian | 23.0 | 19.0 | 23.0 |

## Per building: all congregations together

Total weekly main services and worship hours on one tax lot, adding host and guests. Only lots where every congregation on them posted a schedule, so totals are not undercounted.

| building_group | lots | congregations_per_lot | mean_uses | mean_main_services | median_main | mean_hours_week |
| --- | --- | --- | --- | --- | --- | --- |
| other-use building | 286 | 1.02 | 1.92 | 1.5 | 1.0 | 3.8 |
| shared religious building | 30 | 2.03 | 2.03 | 3.2 | 3.0 | 7.3 |
| single-use religious building | 679 | 1.0 | 1.0 | 1.7 | 1.0 | 4.3 |

## Single-use religious buildings by borough

A rough look at place until land values are added (the plan's next phase). Within the two largest traditions; cells under 15 congregations left blank.

| tradition | borough | n | mean_main | pct_two_plus | hours |
| --- | --- | --- | --- | --- | --- |
| Protestant and other Christian | Bronx | 60 | 1.2 | 13.0 | 3.3 |
| Protestant and other Christian | Brooklyn | 165 | 1.1 | 12.0 | 2.8 |
| Protestant and other Christian | Manhattan | 88 | 1.4 | 33.0 | 3.3 |
| Protestant and other Christian | Queens | 123 | 1.5 | 32.0 | 3.6 |
| Protestant and other Christian | Staten Island | 43 | 1.4 | 28.0 | 3.1 |
| Catholic | Bronx | 3 |  |  |  |
| Catholic | Brooklyn | 41 | 3.0 | 90.0 | 7.0 |
| Catholic | Manhattan | 11 |  |  |  |
| Catholic | Queens | 45 | 3.7 | 91.0 | 8.6 |
| Catholic | Staten Island | 3 |  |  |  |

## Caveats

- Only 15% of services posted an end time; the rest use a default duration by tradition (`DEFAULT_MIN` in v0/analysis_services.py), so building-hours are approximate.
- Schedules are as posted on the day of the crawl; summer, holiday and Ramadan schedules differ. The plan recrawls a sample in a second season.
- Congregations without a matched website or posted schedule are not in these tables, and they skew small and renting, so the single-use figures speak for established congregations.
- Compare across rows only within a tradition.
