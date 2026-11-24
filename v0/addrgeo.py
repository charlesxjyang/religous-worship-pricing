"""Address -> parcel geocoding for cities without NYC's GeoSearch.

A street address is first matched exactly to a parcel's own address list (the
city's records); failing that, the US Census geocoder gives a point and the
caller finds the parcel under it (common.assign_lots).
"""

import json
import re
import time
import urllib.parse
import urllib.request

from common import user_agent

CENSUS = "https://geocoding.geo.census.gov/geocoder/locations/onelineaddress"

SUFFIXES = {"STREET": "ST", "STR": "ST", "AVENUE": "AVE", "AV": "AVE", "ROAD": "RD", "PLACE": "PL",
            "TERRACE": "TER", "BOULEVARD": "BLVD", "DRIVE": "DR", "COURT": "CT", "CIRCLE": "CIR",
            "PARKWAY": "PKWY", "LANE": "LN", "SQUARE": "SQ", "HIGHWAY": "HWY", "ALLEY": "ALY",
            "CRESCENT": "CRES", "TRAIL": "TRL", "EXPRESSWAY": "EXPY", "FREEWAY": "FWY",
            "POINTE": "PT", "POINT": "PT", "CROSSING": "XING", "COVE": "CV", "LOOP": "LOOP",
            "RUN": "RUN", "PATH": "PATH", "PIKE": "PIKE", "WAY": "WAY", "ROW": "ROW", "BYPASS": "BYP"}
SUFFIX_SET = set(SUFFIXES.values()) | set(SUFFIXES)
DIRS = {"NORTH": "N", "SOUTH": "S", "EAST": "E", "WEST": "W", "N": "N", "S": "S", "E": "E", "W": "W",
        "NORTHEAST": "NE", "NORTHWEST": "NW", "SOUTHEAST": "SE", "SOUTHWEST": "SW",
        "NE": "NE", "NW": "NW", "SE": "SE", "SW": "SW"}
UNIT_WORDS = {"STE", "SUITE", "APT", "APARTMENT", "UNIT", "BLDG", "BUILDING", "FL", "FLOOR", "RM",
              "ROOM", "#", "LOT", "SPC", "SPACE"}


def us_address_keys(text: str) -> tuple[str | None, str | None]:
    """'615 Grandin Rd, Charlotte, NC 28208' -> ('615 GRANDIN RD', '615 GRANDIN').

    The first key is number, directions, street name and type; the second
    drops the type and directions, for listings that leave them out.
    """
    s = (text or "").upper().replace(".", " ")
    s = s.split(",")[0]
    s = re.sub(r"#", " # ", s)
    words = s.split()
    if not words or not re.match(r"^\d+[A-Z]?$", words[0]):
        return None, None
    num, rest = re.sub(r"[A-Z]$", "", words[0]), words[1:]
    out = []
    for w in rest:
        if w in UNIT_WORDS:
            break
        out.append(w)
    if out and out[0] in DIRS and len(out) > 1:
        out[0] = DIRS[out[0]]
    for i, w in enumerate(out):
        if w in SUFFIXES and i > 0:
            out[i] = SUFFIXES[w]
            out = out[: i + 1] + ([DIRS[out[i + 1]]] if i + 1 < len(out) and out[i + 1] in DIRS else [])
            break
    if not out:
        return None, None
    full = f"{num} {' '.join(out)}"
    loose_words = [w for w in out if w not in DIRS and w not in SUFFIX_SET] or out
    return full, f"{num} {' '.join(loose_words)}"


def make_geocoder(rows, key_fn, state: str):
    """rows: (address, bbl, bin, lat, lon). key_fn(text) -> list of keys, best first.

    Returns geocode(text, cache, lock) -> dict(label, confidence, bbl, bin, lat,
    lon, method) or None. Keys that point to more than one parcel are dropped.
    """
    index = {}
    for address, bbl, bin_, lat, lon in rows:
        for k in key_fn(address):
            if k:
                index.setdefault(k, {})[bbl] = (bbl, bin_, lat, lon)
    unique = {k: next(iter(v.values())) for k, v in index.items() if len(v) == 1}

    def geocode(text, cache, lock):
        for k in key_fn(text):
            if k and k in unique:
                bbl, bin_, lat, lon = unique[k]
                return {"label": k, "confidence": 1.0, "bbl": bbl, "bin": bin_, "lat": lat, "lon": lon,
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
                if matches and matches[0]["addressComponents"].get("state") == state:
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


if __name__ == "__main__":
    for t in ["615 Grandin Rd, Charlotte, NC 28208", "501 North Tryon Street", "5000 Albemarle Rd Ste 101",
              "1234 E. 7th St.", "9600 Providence Rd W", "PO Box 12"]:
        print(f"{t!r:42} -> {us_address_keys(t)}")
