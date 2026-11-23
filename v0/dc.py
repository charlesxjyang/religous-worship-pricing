"""Washington, DC inputs: boundary, parcels, address geocoding.

Parcels come from the Office of Tax and Revenue's owner polygons (the public
ITSPE extract with geometry): owner, premise address, DC use code. Religious
tax exemptions (E1) come from the RPTA tax-exempt property table. DC use codes
are mapped onto NYC's DOF building-class letters so later steps can group
buildings the same way in both cities (081 Religious -> M1, 041 Store -> K1,
...). The real parcel key (SSL) is kept; `bbl` is a surrogate number.

Geocoding: a congregation's street address is first matched exactly to a
parcel's premise address (DC addresses carry a quadrant, so this is precise);
failing that, the US Census geocoder gives a point and the parcel under or
nearest it is used.
"""

import json
import re
import time
import urllib.parse
import urllib.request

import config
from common import download, user_agent

PAGE = 2000
WARDS = f"{config.DCGIS}/Administrative_Other_Boundaries_WebMercator/MapServer/53"
CENSUS = "https://geocoding.geo.census.gov/geocoder/locations/onelineaddress"

# DC use code -> NYC DOF building class (first letter is what later steps read).
_USE = {
    "M1": ["081"],
    "W9": ["083"],
    "A1": ["001", "011", "012", "013", "019"],
    "C0": ["002", "021", "023", "024", "025", "029"],
    "D1": ["022"],
    "D4": ["026", "027", "028"],
    "R4": ["016", "017", "116", "117", "216", "217", "316", "516", "995"],
    "S9": ["015", "126", "127"],
    "G0": ["014", "018", "214", "416", "417", "062", "063", "065", "165", "265", "365", "465"],
    "G7": ["064"],
    "H1": ["003", "031", "032", "033", "035", "037", "039"],
    "H8": ["036", "038"],
    "P2": ["034"],
    "K1": ["004", "041", "042", "043", "044", "045", "046", "047", "048", "049", "067", "068"],
    "K9": ["006", "069"],
    "O1": ["005", "051", "052", "053", "056", "057", "058", "059", "061"],
    "J1": ["066"],
    "F1": ["007", "071", "072", "073", "079"],
    "E1": ["074", "075", "076", "078"],
    "I1": ["082", "088"],
    "Y1": ["084"],
    "P7": ["086"],
    "Q1": ["087"],
    "Z9": ["008", "085", "089", "189"],
    "V0": ["091", "092", "093", "094", "095", "096", "097", "191", "192", "193", "194", "195", "196", "197"],
}
USE_TO_CLASS = {code: cls for cls, codes in _USE.items() for code in codes}
# NYC PLUTO land-use codes, by building-class letter.
CLASS_TO_LANDUSE = {"A": 1, "C": 2, "D": 3, "R": 3, "S": 4, "K": 5, "O": 5, "H": 5, "J": 5,
                    "E": 6, "F": 6, "G": 10, "M": 8, "W": 8, "I": 8, "Y": 8, "P": 8, "Z": 8,
                    "Q": 9, "V": 11}


def arcgis_pages(layer: str, fields: str, dest_dir, geometry: bool) -> list:
    """Download a whole ArcGIS layer as JSON pages, one request at a time."""
    q = urllib.parse.urlencode({"where": "1=1", "returnCountOnly": "true", "f": "json"})
    with urllib.request.urlopen(urllib.request.Request(f"{layer}/query?{q}",
                                headers={"User-Agent": user_agent()}), timeout=120) as r:
        total = json.load(r)["count"]
    parts = []
    for i, offset in enumerate(range(0, total, PAGE)):
        params = {"where": "1=1", "outFields": fields, "orderByFields": "OBJECTID",
                  "resultOffset": offset, "resultRecordCount": PAGE,
                  "returnGeometry": "true" if geometry else "false",
                  "outSR": 4326, "f": "geojson" if geometry else "json"}
        part = dest_dir / f"part-{i:04d}.json"
        if not part.exists():
            print(f"  {layer.rsplit('/', 3)[-3]}/{layer.rsplit('/', 1)[-1]}: {offset:,} of {total:,}")
        parts.append(download(f"{layer}/query?{urllib.parse.urlencode(params)}", part))
    return parts


def load_boundary(con):
    """DC's 8 wards play the role of NYC's boroughs."""
    path = download(f"{WARDS}/query?where=1%3D1&outFields=WARD,NAME&outSR=4326&f=geojson",
                    config.RAW / "dc_wards_2022.geojson")
    con.execute(f"""
        CREATE OR REPLACE TABLE boroughs AS
        SELECT CAST(WARD AS INT) AS borocode, 'Ward ' || WARD AS boroname, geom::GEOMETRY AS geom
        FROM ST_Read('{path}')
    """)
    con.execute("CREATE OR REPLACE TABLE city AS SELECT ST_Union_Agg(geom) AS geom FROM boroughs")


def load_parcels(con):
    poly_dir = config.RAW / "dc_owner_polygons"
    poly_dir.mkdir(parents=True, exist_ok=True)
    arcgis_pages(config.DC_OWNER_POLYGONS,
                 "OBJECTID,SSL,USECODE,OWNERNAME,PREMISEADD,MIXEDUSE,CLASSTYPE,LANDAREA,"
                 "NEWTOTAL,PROPTYPE,UNDERLIES_CONDO,EXTRACTDAT", poly_dir, geometry=True)
    ex_dir = config.RAW / "dc_tax_exempt"
    ex_dir.mkdir(parents=True, exist_ok=True)
    ex_parts = arcgis_pages(config.DC_TAX_EXEMPT, "OBJECTID,SSL,EXEMPTION_TYPE,EXPIRED_DATE,ENDING_DATE",
                            ex_dir, geometry=False)

    # Open exemptions carry EXPIRED_DATE = year 9999 (epoch ms), not a blank.
    now_ms = time.time() * 1000
    ex_rows = []
    for p in ex_parts:
        for f in json.loads(p.read_text()).get("features", []):
            a = f["attributes"]
            live = all(a.get(k) is None or a[k] > now_ms for k in ("EXPIRED_DATE", "ENDING_DATE"))
            if live and a.get("SSL"):
                ex_rows.append((a["SSL"].strip(), a.get("EXEMPTION_TYPE")))
    con.execute("CREATE OR REPLACE TABLE dc_exempt (ssl VARCHAR, exemption_type VARCHAR)")
    con.executemany("INSERT INTO dc_exempt VALUES (?, ?)", ex_rows)

    cls_case = ("CASE " + " ".join(f"WHEN p.u = '{k}' THEN '{v}'" for k, v in USE_TO_CLASS.items())
                + " END")
    lu_case = ("CASE " + " ".join(f"WHEN left(bldgclass, 1) = '{k}' THEN {v}"
                                  for k, v in CLASS_TO_LANDUSE.items()) + " END")
    # ST_Read takes one file at a time; read each page and union them.
    pages = sorted(poly_dir.glob("part-*.json"))
    union = " UNION ALL ".join(
        f"SELECT SSL, USECODE, OWNERNAME, PREMISEADD, MIXEDUSE, CLASSTYPE, LANDAREA, NEWTOTAL, "
        f"PROPTYPE, EXTRACTDAT, geom FROM ST_Read('{p}')" for p in pages)
    con.execute(f"""
        CREATE OR REPLACE TABLE dc_parcels_raw AS
        SELECT trim(SSL) AS ssl, lpad(CAST(USECODE AS VARCHAR), 3, '0') AS u, OWNERNAME AS ownername,
               PREMISEADD AS address, MIXEDUSE AS mixeduse, CLASSTYPE AS classtype,
               TRY_CAST(LANDAREA AS DOUBLE) AS lotarea, TRY_CAST(NEWTOTAL AS DOUBLE) AS assesstot,
               PROPTYPE AS proptype, EXTRACTDAT AS extract_date, geom::GEOMETRY AS geom
        FROM ({union}) WHERE SSL IS NOT NULL
    """)
    con.execute(f"""
        CREATE OR REPLACE TABLE dc_ssl AS
        SELECT ssl, row_number() OVER (ORDER BY ssl) AS bbl FROM (SELECT DISTINCT ssl FROM dc_parcels_raw)
    """)
    con.execute("CREATE OR REPLACE TABLE taxlots AS SELECT s.bbl, NULL::VARCHAR AS condo_flag, r.geom "
                "FROM dc_parcels_raw r JOIN dc_ssl s USING (ssl)")
    con.execute(f"""
        CREATE OR REPLACE TABLE pluto AS
        WITH ex AS (SELECT ssl, string_agg(DISTINCT exemption_type, '; ') AS exemption_type
                    FROM dc_exempt GROUP BY 1),
        p AS (SELECT * FROM dc_parcels_raw QUALIFY row_number() OVER (PARTITION BY ssl ORDER BY u) = 1)
        SELECT s.bbl, NULL::VARCHAR AS borough, NULL AS cd, NULL AS bct2020, p.address,
               {cls_case} AS bldgclass,
               NULL::INT AS landuse,
               CASE WHEN ex.exemption_type IS NOT NULL THEN 'X' END AS ownertype,
               p.ownername, p.lotarea, NULL::DOUBLE AS bldgarea, NULL::DOUBLE AS comarea,
               NULL::DOUBLE AS resarea, NULL::DOUBLE AS officearea, NULL::DOUBLE AS retailarea,
               NULL::DOUBLE AS numbldgs, NULL::DOUBLE AS numfloors, NULL::DOUBLE AS unitsres,
               NULL::DOUBLE AS unitstotal, NULL::DOUBLE AS assessland, p.assesstot,
               CASE WHEN ex.exemption_type IS NOT NULL THEN p.assesstot END AS exempttot,
               NULL::DOUBLE AS yearbuilt, NULL::DOUBLE AS latitude, NULL::DOUBLE AS longitude,
               'ITSPE ' || coalesce(any_value(p.extract_date) OVER (), '') AS version,
               p.ssl, p.u AS usecode, ex.exemption_type,
               coalesce(ex.exemption_type LIKE '%E1%', false) AS exempt_religious,
               p.mixeduse
        FROM p JOIN dc_ssl s USING (ssl) LEFT JOIN ex USING (ssl)
    """)
    con.execute(f"UPDATE pluto SET landuse = {lu_case}")
    con.execute("""
        CREATE OR REPLACE TABLE parcels AS
        SELECT t.bbl, t.condo_flag, p.* EXCLUDE (bbl), t.geom
        FROM taxlots t LEFT JOIN pluto p USING (bbl)
    """)


# ---------------------------------------------------------------- geocoding --

SUFFIXES = {"STREET": "ST", "AVENUE": "AVE", "AV": "AVE", "ROAD": "RD", "PLACE": "PL",
            "TERRACE": "TER", "BOULEVARD": "BLVD", "DRIVE": "DR", "COURT": "CT", "CIRCLE": "CIR",
            "PARKWAY": "PKWY", "LANE": "LN", "SQUARE": "SQ", "HIGHWAY": "HWY", "WAY": "WAY",
            "ALLEY": "ALY", "CRESCENT": "CRES"}
QUADS = {"NORTHWEST": "NW", "NORTHEAST": "NE", "SOUTHWEST": "SW", "SOUTHEAST": "SE",
         "N.W.": "NW", "N.E.": "NE", "S.W.": "SW", "S.E.": "SE"}


def address_key(text: str) -> str | None:
    """'1518 M Street, N.W., Washington DC 20005' -> '1518 M ST NW'."""
    s = (text or "").upper()
    for long, short in QUADS.items():
        s = s.replace(long, short)
    s = re.sub(r"[.,#]", " ", s)
    m = re.match(r"\s*(\d+)(?:-\d+)?\s+(.*?)\s+\b(NW|NE|SW|SE)\b", s)
    if not m:
        return None
    words = [SUFFIXES.get(w, w) for w in m.group(2).split()]
    return f"{m.group(1)} {' '.join(words)} {m.group(3)}"


def make_geocoder(con):
    """geocode(text, cache, lock) -> dict(label, confidence, bbl, bin, lat, lon) or None."""
    index = {}
    for bbl, address, lat, lon in con.execute("""
            SELECT p.bbl, p.address, ST_Y(ST_Centroid(t.geom)), ST_X(ST_Centroid(t.geom))
            FROM pluto p JOIN taxlots t USING (bbl) WHERE p.address IS NOT NULL""").fetchall():
        k = address_key(address)
        if k:
            index.setdefault(k, set()).add((bbl, lat, lon))
    unique = {k: next(iter(v)) for k, v in index.items() if len(v) == 1}

    def geocode(text, cache, lock):
        k = address_key(text)
        if k and k in unique:
            bbl, lat, lon = unique[k]
            return {"label": k, "confidence": 1.0, "bbl": bbl, "bin": None, "lat": lat, "lon": lon,
                    "method": "parcel address"}
        with lock:
            if text in cache:
                return cache[text]
        url = CENSUS + "?" + urllib.parse.urlencode({"address": text, "benchmark": "Public_AR_Current",
                                                     "format": "json"})
        hit = None
        for attempt in range(3):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": user_agent()})
                with urllib.request.urlopen(req, timeout=30) as r:
                    matches = json.load(r)["result"]["addressMatches"]
                if matches and matches[0]["addressComponents"].get("state") == "DC":
                    m = matches[0]
                    hit = {"label": m["matchedAddress"], "confidence": 0.9, "bbl": None, "bin": None,
                           "lat": m["coordinates"]["y"], "lon": m["coordinates"]["x"], "method": "census"}
                break
            except Exception:
                time.sleep(2 ** attempt)
        time.sleep(0.2)
        with lock:
            cache[text] = hit
        return hit

    return geocode
