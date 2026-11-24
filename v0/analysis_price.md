# Sharing and the local price of commercial space, NYC and DC

Congregations placed at the Overture listing address (website extraction was not run in this database). Price: assessed market value of land per square foot for retail and office lots, median within 1,000 m of each congregation (2,000 m where fewer than 10 lots lie within 1,000 m). NYC: PLUTO land assessment / 0.45; DC: OTR land value. Assessed values are the assessor's estimate of market value, not observed rents.

## The price measure

| city | retail and office lots | land $/sq ft, median (IQR) | congregations priced | using 2 km |
| --- | --- | --- | --- | --- |
| New York City | 25,832 | $50 ($35–$100) | 7,100 of 7,104 | 43 |
| Washington, DC | 4,892 | $289 ($129–$479) | 944 of 944 | 27 |

## Pooled by local price quintile, within each city

Quintiles of congregations by the land price around them. 95% Wilson intervals treat congregations as independent, so they are somewhat too narrow.

| city | quintile | land $/sq ft | congregations | Sharing worship space | Sharing, same property | Multi-use (2+ uses) | In a store, office or loft unit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| New York City | 1 | $16–$35 | 1,420 | 11.8% (10.2–13.5) | 13.7% (12.0–15.5) | 16.8% (14.9–18.9) | 26.4% (24.2–28.8) |
|  | 2 | $35–$40 | 1,420 | 12.5% (10.9–14.4) | 14.0% (12.3–15.9) | 16.6% (14.7–18.7) | 27.1% (24.9–29.5) |
|  | 3 | $40–$50 | 1,483 | 12.7% (11.1–14.5) | 14.1% (12.4–16.0) | 17.3% (15.4–19.3) | 27.1% (24.9–29.4) |
|  | 4 | $50–$80 | 1,357 | 17.4% (15.5–19.5) | 19.5% (17.5–21.7) | 23.9% (21.6–26.2) | 22.0% (19.9–24.3) |
|  | 5 | $80–$1,003 | 1,420 | 20.5% (18.5–22.7) | 22.5% (20.4–24.8) | 29.6% (27.2–32.0) | 20.3% (18.3–22.5) |
| Washington, DC | 1 | $18–$60 | 190 | 17.9% (13.1–24.0) | 19.5% (14.5–25.7) | 22.3% (17.0–28.8) | 7.4% (4.4–12.0) |
|  | 2 | $60–$90 | 188 | 14.4% (10.1–20.1) | 15.4% (11.0–21.3) | 21.7% (16.4–28.2) | 12.2% (8.3–17.7) |
|  | 3 | $90–$180 | 189 | 21.2% (15.9–27.5) | 27.0% (21.2–33.7) | 26.5% (20.7–33.3) | 6.3% (3.7–10.8) |
|  | 4 | $180–$320 | 189 | 21.7% (16.4–28.1) | 25.9% (20.2–32.6) | 28.5% (22.5–35.4) | 9.0% (5.7–13.9) |
|  | 5 | $320–$1,644 | 188 | 21.3% (16.0–27.7) | 24.5% (18.9–31.1) | 33.5% (27.1–40.6) | 12.8% (8.7–18.3) |

## Regression: percentage points per doubling of local land price

Linear probability models at the congregation level, standard errors clustered by community district (NYC) or neighborhood cluster (DC). Nearby congregations = log(1 + congregations within 1 km).

| outcome | sample | model | pp per doubling (SE) | p | n |
| --- | --- | --- | --- | --- | --- |
| Sharing worship space | Both cities | City only | +2.88 (0.90) | 0.001 | 8,043 |
| Sharing worship space | Both cities | + tradition | +3.11 (0.92) | <0.001 | 8,043 |
| Sharing worship space | Both cities | + tradition, nearby congregations | +3.32 (0.94) | <0.001 | 8,043 |
| Sharing worship space | NYC | City only | +3.10 (1.07) | 0.004 | 7,099 |
| Sharing worship space | NYC | + tradition | +3.36 (1.10) | 0.002 | 7,099 |
| Sharing worship space | NYC | + tradition, nearby congregations | +3.62 (1.11) | 0.001 | 7,099 |
| Sharing worship space | DC | City only | +1.76 (0.94) | 0.061 | 944 |
| Sharing worship space | DC | + tradition | +1.82 (0.93) | 0.052 | 944 |
| Sharing worship space | DC | + tradition, nearby congregations | +1.69 (0.98) | 0.087 | 944 |
| Sharing worship space | Both cities, religious buildings only | City only | +3.63 (1.11) | 0.001 | 4,615 |
| Sharing worship space | Both cities, religious buildings only | + tradition | +4.18 (1.10) | <0.001 | 4,615 |
| Sharing worship space | Both cities, religious buildings only | + tradition, nearby congregations | +4.46 (1.12) | <0.001 | 4,615 |
| Sharing worship space | NYC, religious buildings only | + tradition, nearby congregations | +4.87 (1.34) | <0.001 | 3,967 |
| Sharing worship space | NYC, religious buildings only | + building floor area, built before 1930 | +3.72 (1.32) | 0.005 | 3,967 |
| Sharing, same property | Both cities | City only | +3.05 (0.92) | <0.001 | 8,043 |
| Sharing, same property | Both cities | + tradition | +3.28 (0.94) | <0.001 | 8,043 |
| Sharing, same property | Both cities | + tradition, nearby congregations | +3.46 (0.95) | <0.001 | 8,043 |
| Sharing, same property | NYC | City only | +3.23 (1.07) | 0.003 | 7,099 |
| Sharing, same property | NYC | + tradition | +3.49 (1.11) | 0.002 | 7,099 |
| Sharing, same property | NYC | + tradition, nearby congregations | +3.71 (1.12) | <0.001 | 7,099 |
| Sharing, same property | DC | City only | +2.15 (1.17) | 0.067 | 944 |
| Sharing, same property | DC | + tradition | +2.18 (1.17) | 0.063 | 944 |
| Sharing, same property | DC | + tradition, nearby congregations | +2.10 (1.22) | 0.086 | 944 |
| Multi-use (2+ uses) | Both cities | City only | +4.37 (1.03) | <0.001 | 7,770 |
| Multi-use (2+ uses) | Both cities | + tradition | +4.53 (1.04) | <0.001 | 7,770 |
| Multi-use (2+ uses) | Both cities | + tradition, nearby congregations | +5.03 (1.03) | <0.001 | 7,770 |
| Multi-use (2+ uses) | NYC | City only | +4.58 (1.22) | <0.001 | 6,842 |
| Multi-use (2+ uses) | NYC | + tradition | +4.79 (1.25) | <0.001 | 6,842 |
| Multi-use (2+ uses) | NYC | + tradition, nearby congregations | +5.34 (1.23) | <0.001 | 6,842 |
| Multi-use (2+ uses) | DC | City only | +3.28 (1.07) | 0.002 | 928 |
| Multi-use (2+ uses) | DC | + tradition | +3.24 (1.09) | 0.003 | 928 |
| Multi-use (2+ uses) | DC | + tradition, nearby congregations | +3.45 (1.15) | 0.003 | 928 |
| In a store, office or loft unit | Both cities | City only | -1.38 (1.43) | 0.334 | 8,043 |
| In a store, office or loft unit | Both cities | + tradition | -1.03 (1.38) | 0.453 | 8,043 |
| In a store, office or loft unit | Both cities | + tradition, nearby congregations | -1.38 (1.34) | 0.304 | 8,043 |
| In a store, office or loft unit | NYC | City only | -1.90 (1.70) | 0.264 | 7,099 |
| In a store, office or loft unit | NYC | + tradition | -1.52 (1.64) | 0.352 | 7,099 |
| In a store, office or loft unit | NYC | + tradition, nearby congregations | -1.93 (1.59) | 0.225 | 7,099 |
| In a store, office or loft unit | DC | City only | +1.29 (1.49) | 0.386 | 944 |
| In a store, office or loft unit | DC | + tradition | +1.31 (1.45) | 0.368 | 944 |
| In a store, office or loft unit | DC | + tradition, nearby congregations | +1.39 (1.44) | 0.336 | 944 |

## Caveats

- Assessed land values are model estimates; NYC's class 4 land values in particular are an allocation of an income-based total. They rank places by price well, less well as levels.
- Sharing in NYC is likely understated where pairs are split across neighbouring lots (the near-miss check in the map page), and that happens more in dense, expensive areas.
- Prices and congregation density rise together; the third model holds nearby congregations fixed.
- Charlotte is not included: its parcel pull has no value fields yet.
