# Services and building use in NYC: first pass

Run 2026-11-24. Of 6,897 congregations, 1,702 have a website that matched their listing and 1,280 posted weekly main services that extraction found, with a quote on the page for each. Everything below is about those congregations; they are likely larger and better established than those without a website or schedule.

## City summary

All traditions. Multi-use and sharing cover every congregation except homes that look like a mailing address; the service columns cover those that posted a schedule.

| congregations | avg_multi_use | pct_multi_use | pct_sharing_worship_space | pct_cotenants_separate_units | with_schedule | avg_main_services | pct_2plus_services | hours_per_week |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 6650 | 1.26 | 21.0 | 15.5 | 4.2 | 1239 | 1.55 | 31.0 | 3.9 |

## Multi-use and services, by tradition

Multi-use counts the distinct bodies using a congregation's worship space: 1 for the congregation, +1 for each other congregation sharing that space (same building, not a building split into units, or its website says so), +1 for a school that is not its own (public, charter, independent, college), +1 for a rented hall (community center, hotel, theater). A church alone is 1.0; with a nesting congregation, a charter school in its building, or meeting in a public school, 2.0. Congregations in separate units of one strip mall, office, flex or apartment building are separate places, each 1.0. The service columns cover congregations that posted a schedule.

| tradition | congregations | mean_uses | pct_one_use | pct_two_uses | pct_three_plus | with_schedule | mean_main_services | pct_2plus_services | mean_hours_week |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Protestant and other Christian | 4967 | 1.27 | 78.0 | 17.0 | 4.0 | 950 | 1.3 | 22.0 | 3.1 |
| Jewish | 487 | 1.24 | 80.0 | 17.0 | 3.0 | 93 | 1.7 | 55.0 | 5.2 |
| Catholic | 438 | 1.22 | 81.0 | 17.0 | 3.0 | 135 | 3.4 | 87.0 | 8.2 |
| Unknown | 286 | 1.26 | 79.0 | 16.0 | 5.0 | 2 | 1.0 | 0.0 | 1.8 |
| Muslim | 233 | 1.13 | 88.0 | 10.0 | 2.0 | 19 | 1.3 | 21.0 | 5.1 |
| Hindu | 96 | 1.1 | 94.0 | 4.0 | 2.0 | 5 | 1.0 | 0.0 | 7.8 |
| Buddhist | 77 | 1.1 | 94.0 | 4.0 | 3.0 | 4 | 1.0 | 0.0 | 6.5 |
| Orthodox Christian | 52 | 1.31 | 75.0 | 19.0 | 6.0 | 30 | 1.2 | 17.0 | 4.7 |

By borough, all traditions (service columns as above):

| borough | congregations | mean_uses | pct_multi_use | with_schedule | mean_main_services | pct_2plus_services |
| --- | --- | --- | --- | --- | --- | --- |
| Bronx | 1181 | 1.21 | 18.0 | 141 | 1.3 | 17.0 |
| Brooklyn | 2200 | 1.18 | 16.0 | 366 | 1.5 | 29.0 |
| Manhattan | 1187 | 1.41 | 30.0 | 307 | 1.5 | 32.0 |
| Queens | 1799 | 1.29 | 22.0 | 353 | 1.8 | 38.0 |
| Staten Island | 283 | 1.26 | 21.0 | 72 | 1.5 | 32.0 |

Multi-use within each kind of building:

| building_group | congregations | mean_uses | max_uses |
| --- | --- | --- | --- |
| single-use religious building | 2968 | 1.0 | 1 |
| other-use building | 2793 | 1.21 | 4 |
| shared religious building | 889 | 2.26 | 5 |

## Who has a schedule

| building_group | congregations | with_matched_site | with_schedule | pct_with_schedule |
| --- | --- | --- | --- | --- |
| single-use religious building | 2968 | 883 | 678 | 23.0 |
| other-use building | 2793 | 493 | 345 | 12.0 |
| shared religious building | 889 | 269 | 216 | 24.0 |

## Single-use religious buildings: services per week, within tradition

One congregation in its own religious building. Several main services, especially on the same day, means the building is used more intensively than one service a week.

| tradition | with_schedule | mean_main | median_main | pct_one | pct_two | pct_three_plus | pct_2plus_same_day | pct_2plus_languages | mean_hours_week |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Protestant and other Christian | 479 | 1.3 | 1.0 | 78.0 | 16.0 | 5.0 | 22.0 | 6.0 | 3.2 |
| Catholic | 104 | 3.4 | 3.0 | 12.0 | 20.0 | 68.0 | 77.0 | 40.0 | 8.1 |
| Jewish | 56 | 1.8 | 2.0 | 48.0 | 39.0 | 13.0 | 20.0 | 0.0 | 5.4 |
| Orthodox Christian | 21 | 1.1 | 1.0 | 90.0 | 10.0 | 0.0 | 5.0 | 0.0 | 4.3 |

## The same, by kind of building

Main services per congregation, within tradition. A guest congregation in a shared building counts its own services, not its host's.

| tradition | other-use building | shared religious building | single-use religious building |
| --- | --- | --- | --- |
| Catholic | 2.9 | 4.3 | 3.4 |
| Jewish | 1.6 | 1.8 | 1.8 |
| Muslim | 1.3 | 1.0 | 1.4 |
| Orthodox Christian | 1.4 | 1.0 | 1.1 |
| Protestant and other Christian | 1.3 | 1.3 | 1.3 |

Share holding two or more main services:

| tradition | other-use building | shared religious building | single-use religious building |
| --- | --- | --- | --- |
| Catholic | 72.0 | 100.0 | 88.0 |
| Jewish | 54.0 | 69.0 | 52.0 |
| Muslim | 14.0 | 0.0 | 27.0 |
| Orthodox Christian | 38.0 | 0.0 | 10.0 |
| Protestant and other Christian | 23.0 | 21.0 | 22.0 |

## Per place of worship: all congregations together

A place of worship is one worship space: a congregation on its own, or several sharing one space (co-tenants in separate units are separate places). Total weekly main services and worship hours per place, adding host and guests. Only places where every congregation posted a schedule, so totals are not undercounted.

| building_group | places | congregations_per_place | mean_uses | mean_main_services | median_main | mean_hours_week |
| --- | --- | --- | --- | --- | --- | --- |
| other-use building | 321 | 1.01 | 1.32 | 1.4 | 1.0 | 3.7 |
| shared religious building | 44 | 1.75 | 2.02 | 2.8 | 2.0 | 6.5 |
| single-use religious building | 678 | 1.0 | 1.0 | 1.6 | 1.0 | 4.3 |

## Single-use religious buildings by borough

A rough look at place until land values are added (the plan's next phase). Within the two largest traditions; cells under 15 congregations left blank.

| tradition | borough | n | mean_main | pct_two_plus | hours |
| --- | --- | --- | --- | --- | --- |
| Protestant and other Christian | Bronx | 60 | 1.2 | 12.0 | 3.2 |
| Protestant and other Christian | Brooklyn | 163 | 1.1 | 12.0 | 2.8 |
| Protestant and other Christian | Manhattan | 89 | 1.4 | 31.0 | 3.3 |
| Protestant and other Christian | Queens | 124 | 1.5 | 30.0 | 3.5 |
| Protestant and other Christian | Staten Island | 43 | 1.4 | 28.0 | 3.1 |
| Catholic | Bronx | 3 |  |  |  |
| Catholic | Brooklyn | 41 | 3.0 | 90.0 | 7.0 |
| Catholic | Manhattan | 12 |  |  |  |
| Catholic | Queens | 45 | 3.7 | 91.0 | 8.6 |
| Catholic | Staten Island | 3 |  |  |  |

## Caveats

- Only 15% of services posted an end time; the rest use a default duration by tradition (`DEFAULT_MIN` in v0/analysis_services.py), so building-hours are approximate.
- Schedules are as posted on the day of the crawl; summer, holiday and Ramadan schedules differ. The plan recrawls a sample in a second season.
- Congregations without a matched website or posted schedule are not in these tables, and they skew small and renting, so the single-use figures speak for established congregations.
- Compare across rows only within a tradition.
