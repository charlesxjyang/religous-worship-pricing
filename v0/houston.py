"""Houston loaders: council districts, HCAD parcels and the address geocoder.

Sources:
- City of Houston GIS (ArcGIS Online, cohgis_ago): Council Districts 2024
  (11 districts, A-K), Houston's subareas.
- Harris County Appraisal District (HCAD) public data, download.hcad.org:
  CAMA 2026 real_acct.txt (owner, site address, state class, land area and
  market land value) and building_other.txt (commercial building type codes,
  4620 = Religious), plus the GIS parcel geodatabase (HCAD_NUM). Accounts
  whose taxing jurisdictions include 061 (City of Houston) are the city's.
  Texas appraises at market value every year.

Religious use: building type 4620, state class X3 (religious exemption), or a
religious owner name (step 2). The parts of Houston in Fort Bend and
Montgomery counties are not in HCAD's files and are left out.

About a third of HCAD's parcel shapes are curved polygons, which DuckDB cannot
read; linear_wkb() turns them into ordinary polygons, treating arc control
points as vertices. Shapes are in Texas South Central state plane feet
(EPSG:2278) and are transformed to longitude and latitude.

The lot key is the HCAD account; bbl is a surrogate integer.
"""

import struct
import urllib.parse

import addrgeo
import config
from common import download

COH = "https://services.arcgis.com/NummVBqZSIJKUeVR/arcgis/rest/services"
DISTRICTS = f"{COH}/CouncilDistrict2024/FeatureServer/0"
HCAD = config.RAW / "hcad_x"          # unzipped CAMA text files
HCAD_GDB = config.RAW / "hcad_gis" / "Parcels.gdb"
CITY_JUR = "061"

# HCAD commercial building type (impr_tp) -> NYC DOF building class.
_TYPE = {
    "M1": [4620],
    "W8": [4612], "W5": [4613], "W9": [4369],
    "K1": [4301, 4310, 4321, 4323, 4324, 4325, 4326, 4327, 4329, 4330, 4331, 4345, 4346, 4347, 4348,
           4350, 4351, 4356, 4362, 4370, 4373, 4374, 4375, 4376, 4378],
    "K4": [4340, 4341, 4342, 4343, 4344],
    "O1": [4349, 4353, 4354, 4355, 4357, 4359, 4366],
    "H1": [4311, 4314, 4315, 4320], "H8": [4318],
    "I1": [4316, 4317, 4352, 4360, 4640],
    "P9": [4361, 4367, 4387, 4388, 4610, 4630], "P8": [4611], "P7": [4680],
    "J1": [4328, 4363, 4364, 4365, 4381, 4382, 4383, 4384, 4385, 4386, 4390, 4615],
    "Q9": [4389],
    "G0": [4338, 4339, 4372], "G5": [4332, 4333, 4334, 4335, 4336, 4337],
    "E1": [4312, 4358, 4377, 4380, 4391, 4392, 4394, 4395, 4396, 4397, 4398, 4399, 4427, 4428, 4491, 4368],
    "F1": [4401, 4402, 4403, 4405, 4410, 4411, 4412, 4413, 4414, 4415, 4416, 4417, 4418, 4419, 4420,
           4421, 4422, 4423, 4424, 4425, 4426, 4497],
    "Y9": [4614, 4660, 4670, 4685, 4690],
    "C1": [4209, 4211, 4221, 4222, 4299], "D1": [4212, 4214], "S9": [4319], "W9b": [4313],
    "Z9": [4108, 4213, 4215],
}
TYPE_CLASS = {t: (cls if cls != "W9b" else "W9") for cls, codes in _TYPE.items() for t in codes}
# State class -> building class where no commercial building record says otherwise.
STATE_CLASS = {"A1": "A1", "A2": "A2", "A3": "A1", "A4": "B1", "B1": "C1", "B2": "B1", "B3": "C0", "B4": "C0",
               "C1": "V0", "C2": "V0", "C3": "V0", "D1": "V0", "D2": "V0", "1D": "V0", "1D1": "V0",
               "E1": "A1", "F1": "Z9", "F2": "F1", "X1": "Y9", "X2": "Z9", "X3": "M9", "X4": "Z9",
               "X7": "Z9", "XJ": "W8", "XV": "Z9", "XG": "Z9", "XI": "P9",
               "Z0": "V0", "Z1": "R4", "Z2": "R4", "Z3": "R4", "Z4": "R4", "Z5": "R4"}
CLASS_TO_LANDUSE = {"A": 1, "B": 1, "C": 2, "D": 3, "R": 3, "S": 4, "K": 5, "O": 5, "H": 5, "J": 5,
                    "E": 6, "F": 6, "G": 10, "M": 8, "W": 8, "I": 8, "Y": 8, "P": 8, "Z": 8,
                    "Q": 9, "V": 11}


def linear_wkb(b: bytes) -> bytes | None:
    """Any (Multi)Polygon / CurvePolygon / MultiSurface WKB, with or without Z/M,
    as a 2D MultiPolygon WKB. Arc control points become vertices."""
    if b is None:
        return None
    b = bytes(b)
    pos = 0

    def header():
        nonlocal pos
        bo = "<" if b[pos] == 1 else ">"
        (t,) = struct.unpack_from(bo + "I", b, pos + 1)
        pos += 5
        base, dims = t % 1000, 2 + (t // 1000 in (1, 2)) + 2 * (t // 1000 == 3)
        return bo, base, dims

    def u32(bo):
        nonlocal pos
        (n,) = struct.unpack_from(bo + "I", b, pos)
        pos += 4
        return n

    def points(bo, dims):
        nonlocal pos
        n = u32(bo)
        vals = struct.unpack_from(bo + "d" * (n * dims), b, pos)
        pos += 8 * n * dims
        return [(vals[i], vals[i + 1]) for i in range(0, n * dims, dims)]

    def curve():  # a full curve geometry with its own header
        bo, base, dims = header()
        if base in (2, 8):                       # LineString, CircularString
            return points(bo, dims)
        if base == 9:                            # CompoundCurve
            out = []
            for _ in range(u32(bo)):
                seg = curve()
                out.extend(seg if not out else seg[1:])
            return out
        raise ValueError(f"curve type {base}")

    def polygon():  # returns list of rings
        bo, base, dims = header()
        if base == 3:
            return [points(bo, dims) for _ in range(u32(bo))]
        if base == 10:
            return [curve() for _ in range(u32(bo))]
        raise ValueError(f"polygon type {base}")

    bo, base, dims = (lambda: header())()
    if base in (3, 10):
        pos = 0
        polys = [polygon()]
    elif base in (6, 12):
        polys = [polygon() for _ in range(u32(bo))]
    else:
        return None
    out = [struct.pack("<BII", 1, 6, len(polys))]
    for rings in polys:
        out.append(struct.pack("<BII", 1, 3, len(rings)))
        for r in rings:
            if r and r[0] != r[-1]:
                r = r + [r[0]]
            out.append(struct.pack("<I", len(r)))
            out.append(struct.pack("<" + "d" * (2 * len(r)), *[c for p in r for c in p]))
    return b"".join(out)


def load_boundary(con):
    q = urllib.parse.urlencode({"where": "1=1", "outFields": "DISTRICT", "outSR": 4326, "f": "geojson"})
    path = download(f"{DISTRICTS}/query?{q}", config.RAW / "houston_council_districts_2024.geojson")
    con.execute(f"""
        CREATE OR REPLACE TABLE boroughs AS
        SELECT row_number() OVER (ORDER BY DISTRICT)::INT AS borocode, 'District ' || DISTRICT AS boroname,
               geom::GEOMETRY AS geom
        FROM ST_Read('{path}')
    """)
    con.execute("CREATE OR REPLACE TABLE city AS SELECT ST_Union_Agg(geom) AS geom FROM boroughs")


def load_parcels(con):
    con.execute(f"""
        CREATE OR REPLACE TABLE hcad_acct AS
        SELECT trim(acct) AS acct, trim(mailto) AS ownername, trim(site_addr_1) AS address,
               trim(site_addr_3) AS zip, trim(state_class) AS state_class,
               TRY_CAST(bld_ar AS DOUBLE) AS bldgarea, TRY_CAST(land_ar AS DOUBLE) AS lotarea,
               TRY_CAST(land_val AS DOUBLE) AS land_val, TRY_CAST(tot_mkt_val AS DOUBLE) AS tot_mkt_val,
               TRY_CAST(yr_impr AS INT) AS yearbuilt
        FROM read_csv('{HCAD / "real_acct.txt"}', delim = '\t', header = true, all_varchar = true,
                      quote = '', ignore_errors = true)
        WHERE list_contains(string_split(trim(jurs), ' '), '{CITY_JUR}')
    """)
    con.execute(f"""
        CREATE OR REPLACE TABLE hcad_bldg AS
        SELECT trim(acct) AS acct,
               first(TRY_CAST(impr_tp AS INT) ORDER BY TRY_CAST(im_sq_ft AS DOUBLE) DESC NULLS LAST) AS impr_tp,
               bool_or(TRY_CAST(impr_tp AS INT) = 4620) AS has_religious_bldg
        FROM read_csv('{HCAD / "building_other.txt"}', delim = '\t', header = true, all_varchar = true,
                      quote = '', ignore_errors = true)
        GROUP BY 1
    """)
    # Parcel shapes for the city's accounts, made linear in Python.
    rows = con.execute(f"""
        SELECT trim(HCAD_NUM_1) AS acct, Shape FROM ST_Read('{HCAD_GDB}', keep_wkb := true)
        WHERE trim(HCAD_NUM_1) IN (SELECT acct FROM hcad_acct)
    """).fetchall()
    shapes = [(a, linear_wkb(s)) for a, s in rows]
    con.execute("CREATE OR REPLACE TEMP TABLE hcad_shape (acct VARCHAR, wkb BLOB)")
    con.executemany("INSERT INTO hcad_shape VALUES (?, ?)", [(a, w) for a, w in shapes if w])
    con.execute("CREATE OR REPLACE TABLE hcad_lot AS SELECT acct, row_number() OVER (ORDER BY acct) AS bbl "
                "FROM (SELECT DISTINCT acct FROM hcad_shape)")
    con.execute("""CREATE OR REPLACE TABLE taxlots AS
        SELECT l.bbl, NULL::VARCHAR AS condo_flag,
               ST_Transform(ST_Union_Agg(ST_MakeValid(ST_GeomFromWKB(s.wkb))), 'EPSG:2278', 'EPSG:4326',
                            always_xy := true) AS geom
        FROM hcad_shape s JOIN hcad_lot l USING (acct) GROUP BY l.bbl""")
    type_case = "CASE " + " ".join(f"WHEN b.impr_tp = {k} THEN '{v}'" for k, v in TYPE_CLASS.items()) + " END"
    state_case = "CASE " + " ".join(f"WHEN a.state_class = '{k}' THEN '{v}'" for k, v in STATE_CLASS.items()) + " END"
    lu_case = ("CASE " + " ".join(f"WHEN left(bldgclass, 1) = '{k}' THEN {v}"
                                  for k, v in CLASS_TO_LANDUSE.items()) + " END")
    con.execute(f"""
        CREATE OR REPLACE TABLE pluto AS
        SELECT l.bbl, NULL::VARCHAR AS borough, NULL AS cd, NULL AS bct2020, a.address,
               CASE WHEN coalesce(b.has_religious_bldg, false) THEN 'M1'
                    ELSE coalesce({type_case}, {state_case}) END AS bldgclass,
               NULL::INT AS landuse,
               CASE WHEN left(a.state_class, 1) = 'X' THEN 'X' END AS ownertype,
               upper(a.ownername) AS ownername,
               a.lotarea, a.bldgarea, NULL::DOUBLE AS comarea, NULL::DOUBLE AS resarea, NULL::DOUBLE AS officearea,
               NULL::DOUBLE AS retailarea, NULL::DOUBLE AS numbldgs, NULL::DOUBLE AS numfloors,
               NULL::DOUBLE AS unitsres, NULL::DOUBLE AS unitstotal, a.land_val AS assessland,
               a.tot_mkt_val AS assesstot, NULL::DOUBLE AS exempttot, nullif(a.yearbuilt, 0) AS yearbuilt,
               NULL::DOUBLE AS latitude, NULL::DOUBLE AS longitude, 'HCAD 2026' AS version,
               a.acct, a.state_class, b.impr_tp, a.state_class = 'X3' AS exempt_religious,
               false AS owner_is_person
        FROM hcad_acct a JOIN hcad_lot l USING (acct) LEFT JOIN hcad_bldg b USING (acct)
    """)
    # As elsewhere: a religious exemption means religious use, unless the lot is a school.
    con.execute("ALTER TABLE pluto ADD COLUMN bldgclass_landuse VARCHAR")
    # Religious-exempt parcels with no commercial building (parking, parsonages, land) are
    # religious property but not worship sites; the recall check reads this column.
    con.execute("UPDATE pluto SET bldgclass_landuse = CASE WHEN state_class = 'X3' AND impr_tp IS NULL "
                "THEN 'Z9' ELSE bldgclass END")
    con.execute("UPDATE pluto SET bldgclass = 'M9' WHERE exempt_religious AND left(coalesce(bldgclass, ''), 1) NOT IN ('M', 'W')")
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
    rows = con.execute("""
        SELECT p.address, p.bbl, NULL, ST_Y(ST_Centroid(t.geom)), ST_X(ST_Centroid(t.geom))
        FROM pluto p JOIN taxlots t USING (bbl)
        WHERE p.address IS NOT NULL AND NOT starts_with(p.address, '0 ')
    """).fetchall()
    return addrgeo.make_geocoder(rows, _keys, "TX")
