"""Checks on "other use" buildings (Charles, 2026-11-23).

Homes: is a residential lot where the congregation gathers (a house church,
a storefront under apartments) or only a pastor's or treasurer's mailing
address? Evidence, strongest first:
  supports gathering  an OSM religious building on the lot; or the
                      congregation's own website gives this street address
  suggests mailing    the listing address has an apartment unit; or the
                      IRS registration sits on a different, non-residential
                      lot; or the website gives other NYC addresses but not
                      this one
  unconfirmed         none of the above
Schools: is the school on the lot the congregation's own (St. Brendan
Church and St. Brendan School; a Catholic parish's school on diocesan land),
or a public or independent school (which may itself be religious)?
  own school          school name matches the congregation's name; or a
                      Catholic parish, a Catholic-named school and a
                      Catholic-owned lot
  public school       NCES public or charter school
  independent school  any other private school
Writes tables home_checks and school_checks.
"""

import json
import re
from collections import defaultdict

import config
from names import names_match, tokens

WEB_DIR = config.RAW / "web"
SUFFIX = (r"Street|St|Avenue|Ave|Av|Road|Rd|Boulevard|Blvd|Place|Pl|Parkway|Pkwy|Lane|Ln|"
          r"Drive|Dr|Court|Ct|Terrace|Ter|Way|Concourse|Plaza|Highway|Hwy|Turnpike|Tpke|Walk|Loop|Square|Sq")
ADDR_RE = re.compile(
    rf"\b(\d{{1,5}}(?:-\d{{1,5}})?)\s+(?:(?:N|S|E|W|North|South|East|West)\.?\s+)?"
    rf"((?:\d{{1,3}}(?:st|nd|rd|th)?|[A-Za-z]+)(?:\s+[A-Za-z]+){{0,2}}?)\s+(?:{SUFFIX})\b\.?"
    rf"|\b(\d{{1,5}}(?:-\d{{1,5}})?)\s+(Broadway)\b", re.I)
UNIT_APT_RE = re.compile(r"\b(apt|apartment|unit|ph|penthouse)\b\.?\s*[\w-]+|#\s*\d+[a-z]?\b|\b(fl|floor)\s*([2-9]|\d{2,})\b|\b\d{1,2}[a-z]\b$", re.I)
UNIT_STREET_RE = re.compile(r"\b(store|storefront|ground|grd|bsmt|basement|fl(oor)?\s*1|1st\s+fl(oor)?)\b", re.I)
CATHOLIC_SCHOOL_RE = re.compile(r"\b(ST|SAINT|OUR LADY|HOLY|SACRED|BLESSED|IMMACULATE|CHRIST THE KING|CATHOLIC|ANNUNCIATION|ASSUMPTION|RESURRECTION|NATIVITY|VISITATION|TRANSFIGURATION|PRECIOUS BLOOD|GUARDIAN ANGEL)\b")
CATHOLIC_OWNER_RE = re.compile(r"\b(ARCHDIOCESE|DIOCESE|ROMAN CATHOLIC|CATHOLIC|PARISH|ARCHBISHOP|BISHOP OF)\b"
                               r"|\bR\.?\s?C(\b|\d|CH)")
FILLER = {"the", "of", "inc", "ny", "nyc", "new", "york", "and", "de", "la", "el", "corp", "incorporated"}


def named_for(cong_name: str, school_name: str) -> bool:
    """School name carries the congregation's name: 'Muslim Center of New York'
    and 'Muslim Center Junior High School'; 'St Brigid Church' and 'St Brigid School'."""
    if names_match(cong_name, school_name):
        return True
    words = [t for t in tokens(cong_name) if t not in FILLER]
    words = [t for t in words if t not in ("church", "congregation", "masjid", "temple")] or words
    school = set(tokens(school_name))
    return len(words) >= 2 and all(t in school for t in words[:3])


def addr_keys(text: str) -> set[tuple[str, str]]:
    """(house number, first word of street) pairs found in text."""
    keys = set()
    for m in ADDR_RE.finditer(text or ""):
        num = m.group(1) or m.group(3)
        street = m.group(2) or m.group(4) or ""
        if not num or not street:
            continue
        first = re.sub(r"^(\d+)(st|nd|rd|th)$", r"\1", street.split()[0].lower())  # 141st -> 141
        keys.add((num, first))
    return keys


def site_text(site_key: str | None) -> str:
    if not site_key:
        return ""
    p = WEB_DIR / f"{site_key}.json"
    if not p.exists():
        return ""
    return "\n".join(pg.get("text") or "" for pg in json.loads(p.read_text())["pages"])


def home_checks(con):
    rows = con.execute("""
        SELECT s.cong_id, s.bbl, s.building_use,
               list(DISTINCT g.address) FILTER (WHERE g.address IS NOT NULL) AS addresses,
               list(DISTINCT g.site_key) FILTER (WHERE g.site_key IS NOT NULL) AS site_keys,
               list(DISTINCT i.ein) FILTER (WHERE i.ein IS NOT NULL) AS eins,
               coalesce(any_value(o.osm_buildings), 0) AS osm_buildings
        FROM cong_sites s
        JOIN place_cong c USING (cong_id) JOIN place_gathering g USING (id)
        LEFT JOIN place_irs i USING (id)
        LEFT JOIN osm_lot_flags o ON o.bbl = s.bbl
        WHERE s.building_use IN ('residential', 'apartments or house with stores')
        GROUP BY ALL
    """).fetchall()
    irs_lot = dict(con.execute("""
        SELECT o.ein, CASE WHEN f.religious_owned OR f.commercial_use OR left(f.bldgclass, 1) IN ('M', 'W', 'K', 'O')
                           THEN o.bbl END
        FROM irs_orgs o LEFT JOIN lot_flags f ON f.bbl = o.bbl
    """).fetchall())
    out = []
    for cong_id, bbl, use, addresses, site_keys, eins, osm in rows:
        addresses, site_keys, eins = addresses or [], site_keys or [], eins or []
        listing_keys = set().union(*(addr_keys(a) for a in addresses)) if addresses else set()
        text = "\n".join(site_text(k) for k in site_keys)
        site_keys_found = addr_keys(text) if text else set()
        site_has_listing = bool(listing_keys & site_keys_found)
        site_other = bool(site_keys_found - listing_keys) and not site_has_listing
        apt_unit = any(UNIT_APT_RE.search(a or "") for a in addresses)
        street_unit = any(UNIT_STREET_RE.search(a or "") for a in addresses)
        irs_elsewhere = any(irs_lot.get(e) and irs_lot.get(e) != bbl for e in eins)
        if osm:
            check, why = "supports gathering", "OSM maps a place of worship on the lot"
        elif site_has_listing:
            check, why = "supports gathering", "its website gives this street address"
        elif street_unit and not apt_unit:
            check, why = "supports gathering", "address is a storefront, ground floor or basement"
        elif apt_unit:
            check, why = "suggests mailing", "address has an apartment unit"
        elif irs_elsewhere:
            check, why = "suggests mailing", "IRS registration is on a church, school or commercial lot elsewhere"
        elif site_other:
            check, why = "suggests mailing", "its website gives other addresses, not this one"
        else:
            check, why = "unconfirmed", "no evidence either way" + ("" if text else " (no website text)")
        out.append((cong_id, check, why, bool(text)))
    con.execute("CREATE OR REPLACE TABLE home_checks (cong_id VARCHAR, home_check VARCHAR, home_evidence VARCHAR, has_site_text BOOLEAN)")
    if out:
        con.executemany("INSERT INTO home_checks VALUES (?, ?, ?, ?)", out)


def school_checks(con):
    rows = con.execute("""
        SELECT s.cong_id, s.names, s.tradition, f.ownername, f.ownertype,
               list({'name': sc.name, 'source': sc.source}) AS schools
        FROM cong_sites s
        JOIN lot_flags f ON f.bbl = s.bbl
        JOIN school_lot sl ON sl.bbl = s.bbl
        JOIN schools sc ON sc.school_id = sl.id
        GROUP BY ALL
    """).fetchall()
    out = []
    for cong_id, names, tradition, owner, ownertype, schools in rows:
        cong_names = (names or "").split(" | ")
        kinds = []
        for sc in schools:
            sname, src = sc["name"], sc["source"]
            if src == "nces_public":
                kinds.append(("public school", sname))
            elif any(named_for(n, sname) for n in cong_names):
                kinds.append(("own school", sname))
            elif (tradition == "Catholic" and CATHOLIC_SCHOOL_RE.search(sname.upper())
                  and CATHOLIC_OWNER_RE.search((owner or "").upper())):
                kinds.append(("own school", sname))
            else:
                kinds.append(("independent school", sname))
        labels = {k for k, _ in kinds}
        # One label per congregation: another body's school wins over its own.
        check = ("public school" if "public school" in labels else
                 "independent school" if "independent school" in labels else "own school")
        out.append((cong_id, check, "; ".join(f"{n} ({k})" for k, n in kinds)))
    # School-class buildings (DOF class W) with no NCES school on the lot:
    # judge by owner and class instead.
    rows = con.execute("""
        SELECT s.cong_id, s.names, s.tradition, s.bldgclass, f.ownername, f.religious_owned
        FROM cong_sites s JOIN lot_flags f ON f.bbl = s.bbl
        WHERE left(s.bldgclass, 1) = 'W'
    """).fetchall()
    have = {r[0] for r in out}
    for cong_id, names, tradition, cls, owner, rel_owned in rows:
        if cong_id in have:
            continue
        cong_names = (names or "").split(" | ")
        if any(names_match(n, owner or "") or named_for(n, owner or "") for n in cong_names) \
                or (cls == "W2" and rel_owned) \
                or (tradition == "Catholic" and CATHOLIC_OWNER_RE.search((owner or "").upper())):
            out.append((cong_id, "own school", f"{cls} school building owned by {owner} (own)"))
        elif cls in ("W5", "W6") or re.search(r"\b(COLLEGE|UNIVERSITY|SEMINARY)\b", (owner or "").upper()):
            out.append((cong_id, "college", f"{cls} college building owned by {owner}"))
        else:
            out.append((cong_id, "unrelated school building", f"{cls} school building owned by {owner}"))
    con.execute("CREATE OR REPLACE TABLE school_checks (cong_id VARCHAR, school_check VARCHAR, schools_on_lot VARCHAR)")
    if out:
        con.executemany("INSERT INTO school_checks VALUES (?, ?, ?)", out)


if __name__ == "__main__":
    tests = ["Join us Sunday at 1234 Grand Concourse, Bronx", "455 West 141st Street", "2200 Broadway",
             "Located at 85-05 144th St, Jamaica", "PO Box 12"]
    for t in tests:
        print(t, "->", addr_keys(t))
    for a in ["1057 E 227th St Apt 3B", "214 Utica Ave Store 1", "35 W 125th St Fl 2", "88 Lee Ave"]:
        print(a, "apt" if UNIT_APT_RE.search(a) else "", "street-level" if UNIT_STREET_RE.search(a) else "")
