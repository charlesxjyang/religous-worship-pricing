# How the NYC dataset is built

The question: do congregations in expensive places economize on space by sharing
buildings, or by meeting in buildings built for something else? This page says
where the data comes from, how a congregation is placed in a building, and how
duplicates are merged. Results are in `analysis_sharing.md`.

## Data sources

| Source | What it gives | Used for | Caveat |
| --- | --- | --- | --- |
| Overture Maps places (Nov 2026) | 9,522 listings in worship categories: name, address, map point, phone, website. Overture pools Meta, Microsoft, Foursquare and others | The list of congregations | Duplicates, closed places, wrong websites, some non-congregations |
| PLUTO (NYC Planning) + DOF tax-lot map | Every tax lot: building class (M1 = church, synagogue or chapel), land use, owner name, floor areas | What kind of building each congregation is in, and who owns it | Describes the main building only; owner names cut at about 21 characters |
| NYC GeoSearch (NYC Planning) | Street address to tax lot (BBL) and building (BIN) | Placing listings and IRS records in buildings | Some addresses fail to match |
| IRS Exempt Organizations file (Nov 2026) | 14,152 religious organizations registered at NYC ZIP codes: name, EIN, registered address | Telling who a listing is; finding congregations Overture missed | Registered address is often an office, PO box or pastor's apartment, not where people gather; churches stay on file after they close |
| OpenStreetMap (via Overture buildings) | 2,181 buildings volunteers tagged as church, synagogue, mosque, temple | Independent check that a lot holds a house of worship | Mostly larger, purpose-built buildings |
| NCES school locations | 1,885 public and 539 private schools | Finding congregations that meet in, or host, a school | Private-school list does not say who owns the school |
| Congregation websites (crawled) | Pages from 3,122 websites | Checking addresses now; service times and meeting places once extraction runs | Extraction needs an API key; not run yet |

## Placing each congregation in a building

1. Start from the listing's street address, geocoded to a lot and building. If the
   address fails, or lands more than 150 m from the listing's map point, use the lot
   under the map point instead. (Map points often sit on the street or the lot next
   door.)
2. Once website extraction runs, replace that with the address where the
   congregation's own website says services are held. The listing is a fallback,
   because it can be a business or mailing address.
3. Read the building's use from its tax-lot record: a religious building (class M),
   a store or office, apartments with stores, a house, a school, a factory or loft,
   or a hall.

## Merging duplicates

Overture often lists one congregation several times. Two listings on the same lot
are treated as one congregation when they share any of:

1. a website, or an identical name after tidying
2. a phone number
3. a matching name: abbreviations expanded (St = Saint, R.C. = Roman Catholic,
   SDB = Seventh Day Baptist, Bais = Beth) and the distinctive words agree. Names of
   different denominations never match, and common words (First, Mount, Holy) do
   not count as distinctive
4. the same IRS registration (EIN)

Listings on the same lot with none of these in common stay separate: two
congregations in one building is exactly what the study measures. Matching is never
done across the whole city, only within one lot (or, for IRS records, one ZIP code),
so two different "First Baptist" churches are never merged.

## The two measures

- **Sharing**: two distinct congregations use the same worship space: another
  congregation in the same building (NYC: building ID; DC and Charlotte: building
  footprint), when the building is not split into units, or the congregation's own
  website says it shares space. Congregations in separate units of one strip mall,
  office, flex or apartment building are co-tenants and count as separate places of
  worship. Reported with and without IRS corroboration.
- **Multi-use**: the number of distinct bodies using a congregation's worship space:
  1, plus each other congregation sharing it, plus a school that is not its own, plus
  a rented hall (community center, hotel). A church alone is 1; with a nesting
  congregation or a charter school in its building, 2.
- **Other use**: the building is not a religious building or the congregation's own
  school. Two checks keep this honest:
  - *Homes.* A house or apartment counts as a gathering place only if nothing
    suggests it is just a mailing address. An apartment unit in the address, an IRS
    registration on a church or commercial lot elsewhere, or a website giving other
    addresses moves it to "location unknown". An OSM-mapped place of worship, the
    website giving this address, or a storefront or ground-floor unit supports it.
  - *Schools.* A public or charter school, or an independent private school
    (including an independent religious school), counts as other use. A school whose
    name matches the congregation's, or a Catholic parish school on diocesan land,
    counts as the congregation's own and not as other use.

## What is not done yet

- Website extraction (service times, and the address where services are held):
  needs an Anthropic API key, about $3.50 for NYC.
- Other cities.
- A hand check of 50 random rows against websites.
