# Services and building use in Charlotte: first pass

Run 2026-11-24. Of 1,068 congregations, 374 have a website that matched their listing and 295 posted weekly main services that extraction found, with a quote on the page for each. Everything below is about those congregations; they are likely larger and better established than those without a website or schedule.

## Who has a schedule

| building_group | congregations | with_matched_site | with_schedule | pct_with_schedule |
| --- | --- | --- | --- | --- |
| single-use religious building | 451 | 209 | 163 | 36.0 |
| other-use building | 417 | 98 | 78 | 19.0 |
| shared religious building | 193 | 63 | 50 | 26.0 |

## Single-use religious buildings: services per week, within tradition

One congregation in its own religious building. Several main services, especially on the same day, means the building is used more intensively than one service a week.

| tradition | with_schedule | mean_main | median_main | pct_one | pct_two | pct_three_plus | pct_2plus_same_day | pct_2plus_languages | mean_hours_week |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Protestant and other Christian | 154 | 1.3 | 1.0 | 75.0 | 21.0 | 5.0 | 25.0 | 1.0 | 2.7 |

## The same, by kind of building

Main services per congregation, within tradition. A guest congregation in a shared building counts its own services, not its host's.

| tradition | other-use building | shared religious building | single-use religious building |
| --- | --- | --- | --- |
| Protestant and other Christian | 1.2 | 1.2 | 1.3 |

Share holding two or more main services:

| tradition | other-use building | shared religious building | single-use religious building |
| --- | --- | --- | --- |
| Protestant and other Christian | 20.0 | 12.0 | 25.0 |

## Per building: all congregations together

Total weekly main services and worship hours on one tax lot, adding host and guests. Only lots where every congregation on them posted a schedule, so totals are not undercounted.

| building_group | lots | congregations_per_lot | mean_main_services | median_main | mean_hours_week |
| --- | --- | --- | --- | --- | --- |
| other-use building | 50 | 1.02 | 1.3 | 1.0 | 2.6 |
| shared religious building | 7 | 2.0 | 2.0 | 2.0 | 4.7 |
| single-use religious building | 163 | 1.0 | 1.4 | 1.0 | 2.8 |

## Single-use religious buildings by council district

A rough look at place until land values are added (the plan's next phase). Within the two largest traditions; cells under 15 congregations left blank.

| tradition | council district | n | mean_main | pct_two_plus | hours |
| --- | --- | --- | --- | --- | --- |
| Protestant and other Christian | District 1 | 31 | 1.1 | 6.0 | 2.2 |
| Protestant and other Christian | District 2 | 25 | 1.2 | 16.0 | 2.4 |
| Protestant and other Christian | District 3 | 23 | 1.4 | 30.0 | 2.9 |
| Protestant and other Christian | District 4 | 13 |  |  |  |
| Protestant and other Christian | District 5 | 21 | 1.3 | 19.0 | 2.9 |
| Protestant and other Christian | District 6 | 25 | 1.6 | 52.0 | 3.1 |
| Protestant and other Christian | District 7 | 16 | 1.3 | 25.0 | 2.6 |
| Catholic | District 1 | 2 |  |  |  |
| Catholic | District 3 | 1 |  |  |  |
| Catholic | District 7 | 1 |  |  |  |

## Caveats

- Only 9% of services posted an end time; the rest use a default duration by tradition (`DEFAULT_MIN` in v0/analysis_services.py), so building-hours are approximate.
- Schedules are as posted on the day of the crawl; summer, holiday and Ramadan schedules differ. The plan recrawls a sample in a second season.
- Congregations without a matched website or posted schedule are not in these tables, and they skew small and renting, so the single-use figures speak for established congregations.
- Compare across rows only within a tradition.
