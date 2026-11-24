# Services and building use in NYC: first pass

Run 2026-11-24. Of 6,912 congregations, 1,643 have a website that matched their listing and 1,229 posted weekly main services that extraction found, with a quote on the page for each. Everything below is about those congregations; they are likely larger and better established than those without a website or schedule.

## City summary

All traditions. Multi-use and sharing cover every congregation except homes that look like a mailing address; the service columns cover those that posted a schedule.

| congregations | avg_multi_use | pct_multi_use | pct_sharing_worship_space | pct_cotenants_separate_units | with_schedule | avg_main_services | pct_2plus_services | hours_per_week |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 6669 | 1.26 | 21.0 | 15.4 | 4.3 | 1187 | 1.53 | 30.0 | 3.9 |

## Multi-use and services, by tradition

Multi-use counts the distinct bodies using a congregation's worship space: 1 for the congregation, +1 for each other congregation sharing that space (same building, not a building split into units, or its website says so), +1 for a school that is not its own (public, charter, independent, college), +1 for a rented hall (community center, hotel, theater). A church alone is 1.0; with a nesting congregation, a charter school in its building, or meeting in a public school, 2.0. Congregations in separate units of one strip mall, office, flex or apartment building are separate places, each 1.0. The service columns cover congregations that posted a schedule.

| tradition | congregations | mean_uses | pct_one_use | pct_two_uses | pct_three_plus | with_schedule | mean_main_services | pct_2plus_services | mean_hours_week |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Protestant and other Christian | 4980 | 1.28 | 78.0 | 17.0 | 5.0 | 913 | 1.3 | 21.0 | 3.1 |
| Jewish | 491 | 1.23 | 80.0 | 17.0 | 3.0 | 79 | 1.7 | 56.0 | 5.4 |
| Catholic | 437 | 1.22 | 80.0 | 17.0 | 3.0 | 131 | 3.4 | 86.0 | 8.3 |
| Unknown | 293 | 1.26 | 80.0 | 16.0 | 4.0 | 4 | 1.0 | 0.0 | 2.7 |
| Muslim | 231 | 1.15 | 88.0 | 10.0 | 3.0 | 20 | 1.4 | 20.0 | 3.3 |
| Hindu | 95 | 1.09 | 95.0 | 3.0 | 2.0 | 6 | 1.0 | 0.0 | 9.3 |
| Buddhist | 80 | 1.11 | 93.0 | 5.0 | 3.0 | 5 | 1.0 | 0.0 | 5.7 |
| Orthodox Christian | 48 | 1.27 | 79.0 | 15.0 | 6.0 | 29 | 1.2 | 17.0 | 4.9 |

By borough, all traditions (service columns as above):

| borough | congregations | mean_uses | pct_multi_use | with_schedule | mean_main_services | pct_2plus_services |
| --- | --- | --- | --- | --- | --- | --- |
| Bronx | 1176 | 1.2 | 17.0 | 129 | 1.3 | 18.0 |
| Brooklyn | 2204 | 1.18 | 15.0 | 349 | 1.4 | 26.0 |
| Manhattan | 1198 | 1.42 | 31.0 | 296 | 1.5 | 31.0 |
| Queens | 1806 | 1.29 | 22.0 | 347 | 1.7 | 36.0 |
| Staten Island | 285 | 1.27 | 22.0 | 66 | 1.5 | 35.0 |

Multi-use within each kind of building:

| building_group | congregations | mean_uses | max_uses |
| --- | --- | --- | --- |
| single-use religious building | 2978 | 1.0 | 1 |
| other-use building | 2810 | 1.21 | 4 |
| shared religious building | 881 | 2.28 | 5 |

## Who has a schedule

| building_group | congregations | with_matched_site | with_schedule | pct_with_schedule |
| --- | --- | --- | --- | --- |
| single-use religious building | 2978 | 857 | 661 | 22.0 |
| other-use building | 2810 | 475 | 321 | 11.0 |
| shared religious building | 881 | 252 | 205 | 23.0 |

## Single-use religious buildings: services per week, within tradition

One congregation in its own religious building. Several main services, especially on the same day, means the building is used more intensively than one service a week.

| tradition | with_schedule | mean_main | median_main | pct_one | pct_two | pct_three_plus | pct_2plus_same_day | pct_2plus_languages | mean_hours_week |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Protestant and other Christian | 468 | 1.3 | 1.0 | 80.0 | 15.0 | 4.0 | 20.0 | 5.0 | 3.1 |
| Catholic | 100 | 3.4 | 3.0 | 12.0 | 19.0 | 69.0 | 79.0 | 44.0 | 8.3 |
| Jewish | 48 | 1.8 | 2.0 | 48.0 | 40.0 | 13.0 | 17.0 | 0.0 | 5.6 |
| Orthodox Christian | 23 | 1.1 | 1.0 | 87.0 | 13.0 | 0.0 | 9.0 | 0.0 | 4.1 |

## The same, by kind of building

Main services per congregation, within tradition. A guest congregation in a shared building counts its own services, not its host's.

| tradition | other-use building | shared religious building | single-use religious building |
| --- | --- | --- | --- |
| Catholic | 2.5 | 4.5 | 3.4 |
| Jewish | 1.6 | 1.7 | 1.8 |
| Muslim | 1.6 | 1.0 | 1.3 |
| Orthodox Christian | 1.6 | 1.0 | 1.1 |
| Protestant and other Christian | 1.3 | 1.3 | 1.3 |

Share holding two or more main services:

| tradition | other-use building | shared religious building | single-use religious building |
| --- | --- | --- | --- |
| Catholic | 68.0 | 100.0 | 88.0 |
| Jewish | 55.0 | 73.0 | 52.0 |
| Muslim | 29.0 | 0.0 | 17.0 |
| Orthodox Christian | 40.0 | 0.0 | 13.0 |
| Protestant and other Christian | 23.0 | 19.0 | 20.0 |

## Per place of worship: all congregations together

A place of worship is one worship space: a congregation on its own, or several sharing one space (co-tenants in separate units are separate places). Total weekly main services and worship hours per place, adding host and guests. Only places where every congregation posted a schedule, so totals are not undercounted.

| building_group | places | congregations_per_place | mean_uses | mean_main_services | median_main | mean_hours_week |
| --- | --- | --- | --- | --- | --- | --- |
| other-use building | 300 | 1.01 | 1.31 | 1.4 | 1.0 | 3.7 |
| shared religious building | 41 | 1.73 | 2.02 | 3.0 | 2.0 | 7.0 |
| single-use religious building | 661 | 1.0 | 1.0 | 1.6 | 1.0 | 4.2 |

## Single-use religious buildings by borough

A rough look at place until land values are added (the plan's next phase). Within the two largest traditions; cells under 15 congregations left blank.

| tradition | borough | n | mean_main | pct_two_plus | hours |
| --- | --- | --- | --- | --- | --- |
| Protestant and other Christian | Bronx | 57 | 1.2 | 12.0 | 3.4 |
| Protestant and other Christian | Brooklyn | 164 | 1.1 | 11.0 | 2.8 |
| Protestant and other Christian | Manhattan | 87 | 1.3 | 26.0 | 3.4 |
| Protestant and other Christian | Queens | 122 | 1.4 | 26.0 | 3.3 |
| Protestant and other Christian | Staten Island | 38 | 1.4 | 32.0 | 3.0 |
| Catholic | Bronx | 2 |  |  |  |
| Catholic | Brooklyn | 36 | 2.8 | 89.0 | 6.8 |
| Catholic | Manhattan | 13 |  |  |  |
| Catholic | Queens | 46 | 3.7 | 89.0 | 8.7 |
| Catholic | Staten Island | 3 |  |  |  |

## Caveats

- Only 15% of services posted an end time; the rest use a default duration by tradition (`DEFAULT_MIN` in v0/analysis_services.py), so building-hours are approximate.
- Schedules are as posted on the day of the crawl; summer, holiday and Ramadan schedules differ. The plan recrawls a sample in a second season.
- Congregations without a matched website or posted schedule are not in these tables, and they skew small and renting, so the single-use figures speak for established congregations.
- Compare across rows only within a tradition.
