"""Settings, per city. Pick the city with the CITY environment variable:

    .venv/bin/python v0/step1_load.py              # New York City (default)
    CITY=dc .venv/bin/python v0/step1_load.py      # Washington, DC

The plan (docs/plan.md) writes Version 0 for Richmond. Inputs per city:

  Plan's input                    NYC                                  Washington, DC
  ------------------------------  -----------------------------------  ------------------------------------
  City boundary, subareas         DCP borough boundaries               DC wards (2022), DCGIS
  Parcels: owner, use, exemption  PLUTO 26v2 + DOF tax-lot polygons    OTR owner polygons (ITSPE), use codes,
                                                                       tax-exempt property (RPTA)
  Address geocoder                NYC Planning Labs GeoSearch (BBL,    US Census geocoder, then the parcel
                                  BIN)                                 under the point
  Schools, IRS, Overture, OSM     same sources, clipped to the city    same sources, clipped to the city

Downstream steps read city-neutral columns: `bbl` is the parcel key (NYC's
BBL; a surrogate number in DC, with the real SSL kept alongside) and
`bldgclass` is NYC's DOF building class, or DC's use code mapped onto it
(v0/dc.py), so the same building-type groups apply in both cities.
"""

import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CITY = os.environ.get("CITY", "nyc").lower()

CITIES = {
    "nyc": dict(
        name="New York City", short="NYC", state="NY", area_label="borough",
        bbox=dict(xmin=-74.2591, xmax=-73.7004, ymin=40.4774, ymax=40.9176),
        zip3=("100", "101", "102", "103", "104", "110", "111", "112", "113", "114", "116"),
        place_re=r"\b(new york|nyc|manhattan|brooklyn|bronx|queens|staten island|flushing|"
                 r"jamaica|astoria|harlem|ny)\b",
        geocoder="geosearch", irs_file="eo_ny.csv",
        report_dir=ROOT / "v0", db_name="nyc_v0.duckdb",
    ),
    "dc": dict(
        name="Washington, DC", short="DC", state="DC", area_label="ward",
        bbox=dict(xmin=-77.1199, xmax=-76.9094, ymin=38.7916, ymax=38.9955),
        zip3=("200", "202", "203", "204", "205"),
        place_re=r"\b(washington|d\.?c\.?|district of columbia)\b",
        geocoder="census", irs_file="eo_dc.csv",
        report_dir=ROOT / "v0" / "dc", db_name="dc_v0.duckdb",
    ),
}
if CITY not in CITIES:
    raise SystemExit(f"unknown CITY={CITY!r}; choose from {sorted(CITIES)}")
C = CITIES[CITY]
CITY_NAME, CITY_SHORT, STATE, AREA_LABEL = C["name"], C["short"], C["state"], C["area_label"]
BBOX = C["bbox"]
NYC_BBOX = BBOX  # older name, kept for scripts that still use it
ZIP3 = C["zip3"]
PLACE_RE = re.compile(C["place_re"], re.I)
GEOCODER = C["geocoder"]
IRS_FILE = C["irs_file"]

DATA = ROOT / "data" / CITY
RAW = DATA / "raw"
DB_PATH = DATA / C["db_name"]
REPORT_DIR = C["report_dir"]
# Point-level outputs (names, addresses, lots). The repo is public and the plan
# publishes aggregates only, so these folders are gitignored.
PRIVATE_DIR = REPORT_DIR / "private"

# --- Overture Maps places -------------------------------------------------
OVERTURE_BUCKET = "overturemaps-us-west-2"
OVERTURE_REGION = "us-west-2"
# None = use the newest release listed in the bucket; pin a string to freeze it.
OVERTURE_RELEASE = None

# Basic categories kept, from the plan (Overture taxonomy 2026-09-23.0).
KEEP_CATEGORIES = [
    "place_of_worship",
    "christian_place_of_worship",
    "jewish_place_of_worship",
    "muslim_place_of_worship",
    "hindu_place_of_worship",
    "buddhist_place_of_worship",
    "religious_organization",
]

# --- NYC Open Data (Socrata) ---------------------------------------------
SOCRATA = "https://data.cityofnewyork.us"
BOROUGHS_DATASET = "wh2p-dxnf"   # Borough Boundaries (water areas included), DCP
PLUTO_DATASET = "64uk-42ks"      # PLUTO, DCP; geometry column is empty here
TAXLOT_DATASET = "i38t-6if2"     # DOF Digital Tax Map tax lot polygons

PLUTO_COLUMNS = [
    "bbl", "borough", "block", "lot", "cd", "bct2020", "address", "zipcode",
    "bldgclass", "landuse", "ownertype", "ownername",
    "lotarea", "bldgarea", "comarea", "resarea", "officearea", "retailarea",
    "numbldgs", "numfloors", "unitsres", "unitstotal",
    "assessland", "assesstot", "exempttot", "yearbuilt",
    "latitude", "longitude", "version",
]
TAXLOT_COLUMNS = ["bbl", "boro", "block", "lot", "condo_flag", "the_geom"]
SOCRATA_PAGE = 100_000

# --- DC GIS (ArcGIS REST) ----------------------------------------------------
DCGIS = "https://maps2.dcgis.dc.gov/dcgis/rest/services/DCGIS_DATA"
DC_OWNER_POLYGONS = f"{DCGIS}/Property_and_Land_WebMercator/MapServer/40"
DC_TAX_EXEMPT = f"{DCGIS}/Property_and_Land_WebMercator/MapServer/70"
DC_USECODES = f"{DCGIS}/Property_and_Land_WebMercator/MapServer/54"

# --- NCES EDGE school locations ------------------------------------------
NCES_BASE = "https://nces.ed.gov/programs/edge/data"
NCES_PUBLIC_ZIP = "EDGE_GEOCODE_PUBLICSCH_2425.zip"    # 2024-25; 2025-26 not posted yet
NCES_PUBLIC_TXT = "EDGE_GEOCODE_PUBLICSCH_2425.TXT"
NCES_PRIVATE_ZIP = "EDGE_GEOCODE_PRIVATESCH_2324.zip"  # PSS 2023-24, latest
NCES_PRIVATE_SHP = "EDGE_GEOCODE_PRIVATESCH_2324.shp"
# The public TXT file has no header row; these are its 23 fields in order.
NCES_PUBLIC_FIELDS = [
    "NCESSCH", "LEAID", "NAME", "OPSTFIPS", "STREET", "CITY", "STATE", "ZIP",
    "STFIP", "CNTY", "NMCNTY", "LOCALE", "LAT", "LON", "CBSA", "NMCBSA",
    "CBSATYPE", "CSA", "NMCSA", "CD", "SLDL", "SLDU", "SCHOOLYEAR",
]

# --- HTTP etiquette --------------------------------------------------------
# Identify the project; set CONTACT_EMAIL in the environment to add a contact.
USER_AGENT = "worship-census-v0/0.1 (academic research)"
REQUEST_PAUSE_S = 1.0
SAMPLE_SEED = 20261122
