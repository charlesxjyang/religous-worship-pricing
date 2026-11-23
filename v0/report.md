# Version 0 report: New York City

Run 2026-11-23. 9,522 Overture places in the seven worship categories. Colocation is judged at the lot where each congregation gathers: the address its own website gives for services when we could place it, otherwise its listing. Extraction used Claude Haiku 5.5 on 0 sites ($0.00).

**Extraction has not run yet** (no API key in this session), so every row below uses the listing lot, and service counts are empty. Rerun steps 4b–6 once `WORSHIP_ANTHROPIC_API_KEY` is set.

## From listing to gathering place

| stage | places | share |
| --- | --- | --- |
| Places | 9522 | 100% |
| With any website or social link | 6275 | 66% |
| With a fetchable website (not social media) | 5965 | 63% |
| Homepage fetched | 3556 | 37% |
| Website confirmed as this congregation's (yes or likely) | 0 | 0% |
| Weekly main services found, with evidence | 0 | 0% |
| Gathering place from website, placed on a lot | 0 | 0% |
| ... on a different lot than the listing | 0 | 0% |

## Colocation by tradition

| tradition | school | shared | commercial | single-use | unknown |
| --- | --- | --- | --- | --- | --- |
| Buddhist | 1 | 14 | 23 | 44 | 17 |
| Catholic | 91 | 98 | 10 | 237 | 42 |
| Hindu | 0 | 12 | 24 | 39 | 40 |
| Jewish | 31 | 85 | 64 | 277 | 107 |
| Muslim | 9 | 34 | 66 | 116 | 50 |
| Orthodox Christian | 1 | 0 | 2 | 0 | 0 |
| Protestant and other Christian | 178 | 1645 | 1081 | 2094 | 966 |
| Sikh | 0 | 5 | 2 | 7 | 1 |
| Unknown | 86 | 625 | 473 | 315 | 510 |

Colocation by where the address came from:

| address_basis | school | shared | commercial | single-use | unknown |
| --- | --- | --- | --- | --- | --- |
| listing | 397 | 2518 | 1745 | 3129 | 1733 |

Of the school flags, 163 are a private school on a religious-owned lot: most likely the congregation's own school, not a rental. The full rules split these out as "own school on campus".

## Weekly main services, where found

| tradition | places_with_schedule | mean_main | median_main | pct_two_or_more | mean_all_weekly |
| --- | --- | --- | --- | --- | --- |

## Websites

| homepage | places |
| --- | --- |
| (no website) | 3557 |
| ok | 3556 |
| dead domain (proxy could not connect) | 721 |
| connection or TLS error | 631 |
| robots_disallowed | 458 |
| http_403 | 237 |
| http_404 | 141 |
| empty | 131 |
| http_429 | 32 |
| http_500 | 14 |
| http_522 | 11 |
| http_503 | 7 |

## Recall check: worship lots with no Overture place

| why | borough | lots | likely_misses |
| --- | --- | --- | --- |
| M1/M9 building class | Bronx | 717 | 53 |
| M1/M9 building class | Brooklyn | 1876 | 404 |
| M1/M9 building class | Manhattan | 699 | 56 |
| M1/M9 building class | Queens | 1301 | 138 |
| M1/M9 building class | Staten Island | 224 | 41 |
| religious owner, institutional use | Bronx | 74 | 26 |
| religious owner, institutional use | Brooklyn | 259 | 122 |
| religious owner, institutional use | Manhattan | 111 | 21 |
| religious owner, institutional use | Queens | 147 | 53 |
| religious owner, institutional use | Staten Island | 51 | 19 |

The likely misses, with owner and address, are in `v0/private/nyc_recall_misses.csv`.

## 50 random rows for checking

Drawn with seed 20261122. They name places and addresses, so they are in `v0/private/check50.md` and `v0/private/nyc_check50.csv` (with evidence quotes and URLs), which are not committed.

## Known gaps in this run

- The cloud session reaches websites only over HTTPS; sites with no HTTPS show as connection or TLS errors and would load from a normal network.
- Version 0 reads static HTML only: no JavaScript rendering, PDFs or social media.
- Listings on one lot count as one congregation only when they share a website, a phone number or an identical normalized name, so some "shared" flags are one congregation listed twice under different names.
- Places with no website (about a third) can only be judged at their listing lot.
