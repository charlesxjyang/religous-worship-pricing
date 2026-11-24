"""Charlotte, NC inputs: council districts, parcels, address geocoding.

Source: Mecklenburg County GIS (meckgis.mecklenburgcountync.gov), public:
- Charlotte City Council Districts (7) play the role of NYC's boroughs;
- Parcel_Landuse: every parcel with land-use description, owner (last and
  first name, so people are easy to tell from bodies), site address and tax
  exemption (RELIGIOUS, "EDUCATIONAL OPERATED ONLY BE RELIG ORGANIZATION", ...),
  restricted to the City of Charlotte tax district;
- MasterAddressPoints: every address, with its parent parcel, used to geocode.

Land-use descriptions are mapped onto NYC's DOF building-class letters so
later steps group buildings the same way in every city. The parcel key (PID)
is kept; `bbl` is a surrogate number. The county's address points carry no
building footprint IDs, so Charlotte, like DC, has no building-level test.
"""

import json
import re

import addrgeo
import arcgis
import config
from common import download

MECK = "https://meckgis.mecklenburgcountync.gov/server/rest/services"
DISTRICTS = f"{MECK}/CharlotteCityCouncilDistricts/FeatureServer/0"
PARCELS = f"{MECK}/Parcel_Landuse/FeatureServer/0"
ADDRESSES = f"{MECK}/MasterAddressPoints/FeatureServer/0"

# Land-use description -> DOF building class; first matching rule wins.
_RULES = [
    ("M1", r"^CHURCH"),
    ("W1", r"^SCHOOL - PUBLIC|^MUNICIPAL EDUCATION"),
    ("W5", r"^COLLEGE - PUBLIC"),
    ("W8", r"^SCHOOL,COLLEGE, PRIVATE"),
    ("W9", r"^DAY CARE"),
    ("R4", r"^CONDO"),
    ("D1", r"^MULTI FAMILY HIGH RISE"),
    ("C0", r"^MULTI FAMIL|^TOWNHOUSE AFFORDABLE|^MUNICIPAL HOUSING"),
    ("A1", r"^SINGLE FAMILY|^TOWN HOUSE|^PATIO HOME|^RURAL HOMESITE|^USE VALUE HOMESITE|"
           r"^RESIDENTIAL AFFORDABLE|^MOBILE HOME"),
    ("O1", r"^OFFICE|^MEDICAL OFFICE|^MEDICAL CONDO|^BANK|^LABORATORY"),
    ("K1", r"^COMMERCIAL|^RESTAURANT|^FAST FOOD|^CONVEN|^CONVIEN|^SHOPPING CENTER|^SUPERMARKET|"
           r"^DEPARTMENT STORE|^FURNITURE STORE|^LOUNGE|^AUTO SALES|^SERVICE GARAGE|^CAR WASH|"
           r"^SERVICE STATION|^LUMBER YARD"),
    ("H1", r"^HOTEL"),
    ("F1", r"^INDUSTRIAL|MANUFACTURING|^WAREHOUS|^MINI WAREHOUSE|^TRUCK TERMINAL|^RECYCLING|"
           r"^PACKING PLANT|^BREWERY|^PETROLEUM|^MINING|^DISPOSAL"),
    ("I1", r"^NURSING HOME|^HOME FOR THE AGED|^HOSPITAL"),
    ("P2", r"^CLUB, LODGES"),
    ("J1", r"^STADIUM|^THEATRE|^BOWLING"),
    ("Z9", r"^FUNERAL"),
    ("Y1", r"^OTHER COUNTY|^OTHER MUNICIPAL|^STATE PROP|^OTHER FEDERAL|^FIRE DEPARTMENT|^JAIL|^INSTITUTIONAL"),
    ("Q1", r"^REC AREA|^GREENWAY|^GOLF COURSE|^MINIATURE GOLF"),
    ("G0", r"^PARKING|^AIRPORT|^MUNICIPAL AIRPORT|^UTILITY|^WATER PLANT|^CELL TOWER|^BILL BOARD|"
           r"^PVT OWNED RR|^RIGHT OF WAY|^ROADWAY"),
]
VACANT_RE = re.compile(r"COMMON AREA|^WASTELAND|^COS NO|FLOOD|^BUFFER|^WETLAND|^SUBMERGED|^ISLAND|"
                       r"^WATER RETENTION|^NO LAND|^AIR RIGHTS|^LEASEHOLD|^FOREST|^AGRICULTURAL|"
                       r"^CONSERVATION|^WOODLAND|^WELL LOT|^UNSUITABLE|^ENVIRONMENTAL|^R101")
CLASS_TO_LANDUSE = {"A": 1, "C": 2, "D": 3, "R": 3, "K": 5, "O": 5, "H": 5, "J": 5, "F": 6,
                    "G": 10, "M": 8, "W": 8, "I": 8, "Y": 8, "P": 8, "Z": 8, "Q": 9, "V": 11}


def class_for(desc: str | None) -> str | None:
    d = (desc or "").upper().strip()
    if not d:
        return None
    if VACANT_RE.search(d):
        return "V0"
    for cls, pat in _RULES:
        if re.search(pat, d):
            return cls
    return None


def load_boundary(con):
    path = download(f"{DISTRICTS}/query?where=1%3D1&outFields=district&outSR=4326&f=geojson",
                    config.RAW / "charlotte_council_districts.geojson")
    con.execute(f"""
        CREATE OR REPLACE TABLE boroughs AS
        SELECT CAST(district AS INT) AS borocode, 'District ' || district AS boroname,
               geom::GEOMETRY AS geom
        FROM ST_Read('{path}')
    """)
    con.execute("CREATE OR REPLACE TABLE city AS SELECT ST_Union_Agg(geom) AS geom FROM boroughs")


def load_parcels(con):
    pdir = config.RAW / "meck_parcels"
    arcgis.pages(PARCELS, "objectid,pid,lusecode,landuse_description,ownrlstnme,ownrfrstnme,address,exemption",
                 pdir, geometry=True, where="taxmundist='CHARLOTTE'", oid="objectid")
    union = " UNION ALL ".join(
        f"SELECT pid, landuse_description, ownrlstnme, ownrfrstnme, address, exemption, geom "
        f"FROM ST_Read('{p}')" for p in sorted(pdir.glob("part-*.json")))
    con.execute(f"""
        CREATE OR REPLACE TABLE clt_parcels_raw AS
        SELECT trim(pid) AS pid, upper(trim(landuse_description)) AS landuse_desc,
               trim(ownrlstnme) || CASE WHEN nullif(trim(ownrfrstnme), '') IS NOT NULL
                                        THEN ', ' || trim(ownrfrstnme) ELSE '' END AS ownername,
               nullif(trim(ownrfrstnme), '') IS NOT NULL AS owner_is_person,
               regexp_replace(trim(address), '\\s+CHARLOTTE\\s+NC\\s*$', '') AS address,
               trim(exemption) AS exemption, geom::GEOMETRY AS geom
        FROM ({union}) WHERE pid IS NOT NULL
    """)
    descs = [r[0] for r in con.execute("SELECT DISTINCT landuse_desc FROM clt_parcels_raw").fetchall()]
    con.execute("CREATE OR REPLACE TABLE clt_landuse_map (landuse_desc VARCHAR, bldgclass VARCHAR)")
    con.executemany("INSERT INTO clt_landuse_map VALUES (?, ?)", [(d, class_for(d)) for d in descs])
    con.execute("CREATE OR REPLACE TABLE clt_pid AS SELECT pid, row_number() OVER (ORDER BY pid) AS bbl "
                "FROM (SELECT DISTINCT pid FROM clt_parcels_raw)")
    con.execute("CREATE OR REPLACE TABLE taxlots AS SELECT s.bbl, NULL::VARCHAR AS condo_flag, r.geom "
                "FROM clt_parcels_raw r JOIN clt_pid s USING (pid)")
    lu_case = ("CASE " + " ".join(f"WHEN left(bldgclass, 1) = '{k}' THEN {v}"
                                  for k, v in CLASS_TO_LANDUSE.items()) + " END")
    con.execute("""
        CREATE OR REPLACE TABLE pluto AS
        WITH p AS (
          SELECT r.*, m.bldgclass FROM clt_parcels_raw r LEFT JOIN clt_landuse_map m USING (landuse_desc)
          -- a PID can carry several land-use rows; prefer a church, then any known use
          QUALIFY row_number() OVER (PARTITION BY pid ORDER BY (m.bldgclass LIKE 'M%') DESC,
                                     (m.bldgclass IS NULL), m.bldgclass) = 1
        )
        SELECT s.bbl, NULL::VARCHAR AS borough, NULL AS cd, NULL AS bct2020, p.address,
               p.bldgclass, NULL::INT AS landuse,
               CASE WHEN p.exemption IS NOT NULL AND p.exemption NOT LIKE '%HOMESTEAD%'
                         AND p.exemption NOT LIKE '%DEFERMENT%' AND p.exemption NOT LIKE '%FLAG%'
                    THEN 'X' END AS ownertype,
               upper(p.ownername) AS ownername,
               NULL::DOUBLE AS lotarea, NULL::DOUBLE AS bldgarea, NULL::DOUBLE AS comarea,
               NULL::DOUBLE AS resarea, NULL::DOUBLE AS officearea, NULL::DOUBLE AS retailarea,
               NULL::DOUBLE AS numbldgs, NULL::DOUBLE AS numfloors, NULL::DOUBLE AS unitsres,
               NULL::DOUBLE AS unitstotal, NULL::DOUBLE AS assessland, NULL::DOUBLE AS assesstot,
               NULL::DOUBLE AS exempttot, NULL::DOUBLE AS yearbuilt, NULL::DOUBLE AS latitude,
               NULL::DOUBLE AS longitude, 'Mecklenburg Parcel_Landuse' AS version,
               p.pid, p.landuse_desc, p.exemption,
               coalesce(p.exemption = 'RELIGIOUS', false) AS exempt_religious,
               coalesce(p.exemption LIKE 'EDUCATIONAL OPERATED ONLY BE RELIG%', false) AS exempt_religious_school,
               p.owner_is_person
        FROM p JOIN clt_pid s USING (pid)
    """)
    # As in DC: a religious exemption means religious use, whatever the land-use code.
    con.execute("ALTER TABLE pluto ADD COLUMN bldgclass_landuse VARCHAR")
    con.execute("UPDATE pluto SET bldgclass_landuse = bldgclass")
    con.execute("UPDATE pluto SET bldgclass = 'M9' WHERE exempt_religious AND coalesce(bldgclass, '') NOT LIKE 'M%'")
    con.execute("UPDATE pluto SET bldgclass = 'W2' WHERE exempt_religious_school AND left(coalesce(bldgclass, ''), 1) <> 'M'")
    con.execute(f"UPDATE pluto SET landuse = {lu_case}")
    con.execute("""
        CREATE OR REPLACE TABLE parcels AS
        SELECT t.bbl, t.condo_flag, p.* EXCLUDE (bbl), t.geom
        FROM taxlots t LEFT JOIN pluto p USING (bbl)
    """)


def _keys(text):
    full, loose = addrgeo.us_address_keys(text)
    return [full, loose]


def make_geocoder(con):
    adir = config.RAW / "meck_address_points"
    parts = arcgis.pages(ADDRESSES, "objectid,txt_street_number,cde_street_dir_prfx,nme_street,cde_roadway_type,"
                         "cde_street_dir_suff,num_parent_parcel,latitude,longitude",
                         adir, geometry=False, where="nme_city='CHARLOTTE'", oid="objectid")
    pid_to_bbl = dict(con.execute("SELECT pid, bbl FROM clt_pid").fetchall())
    rows = []
    for p in parts:
        for f in json.loads(p.read_text()).get("features", []):
            a = f["attributes"]
            bbl = pid_to_bbl.get((a.get("num_parent_parcel") or "").strip())
            if not bbl or a.get("txt_street_number") is None:
                continue
            num = str(int(a["txt_street_number"])) if isinstance(a["txt_street_number"], float) else str(a["txt_street_number"])
            text = " ".join(x for x in (num, a.get("cde_street_dir_prfx"), a.get("nme_street"),
                                        a.get("cde_roadway_type"), a.get("cde_street_dir_suff")) if x)
            rows.append((text, bbl, None, a.get("latitude"), a.get("longitude")))
    # Parcels' own site addresses too (a few have no address point).
    rows += con.execute("""
        SELECT p.address, p.bbl, NULL, ST_Y(ST_Centroid(t.geom)), ST_X(ST_Centroid(t.geom))
        FROM pluto p JOIN taxlots t USING (bbl) WHERE p.address IS NOT NULL
    """).fetchall()
    return addrgeo.make_geocoder(rows, _keys, "NC")
