# Services and building use in DC: first pass

Run 2026-11-24. Of 903 congregations, 318 have a website that matched their listing and 258 posted weekly main services that extraction found, with a quote on the page for each. Everything below is about those congregations; they are likely larger and better established than those without a website or schedule.

## Who has a schedule

| building_group | congregations | with_matched_site | with_schedule | pct_with_schedule |
| --- | --- | --- | --- | --- |
| single-use religious building | 439 | 172 | 140 | 32.0 |
| other-use building | 269 | 80 | 63 | 23.0 |
| shared religious building | 179 | 63 | 53 | 30.0 |

## Single-use religious buildings: services per week, within tradition

One congregation in its own religious building. Several main services, especially on the same day, means the building is used more intensively than one service a week.

| tradition | with_schedule | mean_main | median_main | pct_one | pct_two | pct_three_plus | pct_2plus_same_day | pct_2plus_languages | mean_hours_week |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Protestant and other Christian | 117 | 1.2 | 1.0 | 87.0 | 10.0 | 3.0 | 13.0 | 1.0 | 2.6 |

## The same, by kind of building

Main services per congregation, within tradition. A guest congregation in a shared building counts its own services, not its host's.

| tradition | other-use building | shared religious building | single-use religious building |
| --- | --- | --- | --- |
| Catholic | 3.0 | 4.6 | 3.2 |
| Protestant and other Christian | 1.2 | 1.2 | 1.2 |

Share holding two or more main services:

| tradition | other-use building | shared religious building | single-use religious building |
| --- | --- | --- | --- |
| Catholic | 100.0 | 80.0 | 82.0 |
| Protestant and other Christian | 14.0 | 17.0 | 13.0 |

## Per building: all congregations together

Total weekly main services and worship hours on one tax lot, adding host and guests. Only lots where every congregation on them posted a schedule, so totals are not undercounted.

| building_group | lots | congregations_per_lot | mean_main_services | median_main | mean_hours_week |
| --- | --- | --- | --- | --- | --- |
| other-use building | 52 | 1.0 | 1.2 | 1.0 | 2.6 |
| shared religious building | 8 | 2.0 | 3.4 | 2.0 | 8.4 |
| single-use religious building | 140 | 1.0 | 1.3 | 1.0 | 3.0 |

## Single-use religious buildings by ward

A rough look at place until land values are added (the plan's next phase). Within the two largest traditions; cells under 15 congregations left blank.

| tradition | ward | n | mean_main | pct_two_plus | hours |
| --- | --- | --- | --- | --- | --- |
| Protestant and other Christian | Ward 1 | 5 |  |  |  |
| Protestant and other Christian | Ward 2 | 18 | 1.4 | 33.0 | 2.7 |
| Protestant and other Christian | Ward 3 | 9 |  |  |  |
| Protestant and other Christian | Ward 4 | 12 |  |  |  |
| Protestant and other Christian | Ward 5 | 19 | 1.1 | 5.0 | 2.4 |
| Protestant and other Christian | Ward 6 | 20 | 1.3 | 20.0 | 2.8 |
| Protestant and other Christian | Ward 7 | 21 | 1.0 | 0.0 | 2.5 |
| Protestant and other Christian | Ward 8 | 13 |  |  |  |
| Catholic | Ward 2 | 1 |  |  |  |
| Catholic | Ward 3 | 2 |  |  |  |
| Catholic | Ward 4 | 1 |  |  |  |
| Catholic | Ward 5 | 3 |  |  |  |
| Catholic | Ward 6 | 2 |  |  |  |
| Catholic | Ward 7 | 2 |  |  |  |

## Caveats

- Only 10% of services posted an end time; the rest use a default duration by tradition (`DEFAULT_MIN` in v0/analysis_services.py), so building-hours are approximate.
- Schedules are as posted on the day of the crawl; summer, holiday and Ramadan schedules differ. The plan recrawls a sample in a second season.
- Congregations without a matched website or posted schedule are not in these tables, and they skew small and renting, so the single-use figures speak for established congregations.
- Compare across rows only within a tradition.
