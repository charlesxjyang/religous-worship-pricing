"""Version 0 settings for New York City.

The plan (docs/plan.md) writes Version 0 for Richmond. This repo runs it in NYC,
with NYC equivalents for each Richmond input:

  Richmond input                   NYC input used here
  -------------------------------  ---------------------------------------------
  Census place boundary (51760)    DCP borough boundaries, water included
  Assessor parcels (owner, use,    PLUTO 26v2 attributes (owner, building class,
    exemption code)                  land use, exempt value) joined by BBL to
                                     DOF Digital Tax Map lot polygons
  NCES public + private schools    the same NCES EDGE files, clipped to NYC
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CITY = "nyc"
DATA = ROOT / "data" / CITY
RAW = DATA / "raw"
DB_PATH = DATA / "nyc_v0.duckdb"
REPORT_DIR = ROOT / "v0"

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

# Rough NYC bounding box, used only to prune the S3 scan before the exact
# boundary test.
NYC_BBOX = dict(xmin=-74.2591, xmax=-73.7004, ymin=40.4774, ymax=40.9176)

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
