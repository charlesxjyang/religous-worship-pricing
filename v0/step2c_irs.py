"""Version 1 addition (NYC): IRS registered religious organizations.

Source: IRS Exempt Organizations Business Master File, New York extract
(https://www.irs.gov/pub/irs-soi/eo_ny.csv), monthly, public.

Kept: NYC ZIP codes, and foundation code 10 (church, 170(b)(1)(A)(i)) or an
NTEE code in group X (religion). Each record is sorted by name into
congregation, school, support group (funds, auxiliaries, housing) or other.

IRS addresses are REGISTERED addresses: often an office, a PO box, or a
pastor's apartment, not where people gather. So they are used to tell who a
listing is (dedupe, confirmation) and to find congregations Overture missed,
never as the gathering place. The "in care of" field names people and is not
kept, only whether it was set.

Street addresses (not PO boxes) are geocoded with GeoSearch to BBL and BIN.

Run after step 2:  .venv/bin/python v0/step2c_irs.py
"""

import json
import re
import threading
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

import config
from common import assign_lots, connect, download, make_geocoder
from names import tokens

IRS_URL = f"https://www.irs.gov/pub/irs-soi/{config.IRS_FILE}"
CACHE = config.DATA / "interim" / "irs_geosearch_cache.json"
WORKERS = 4
MIN_CONFIDENCE = 0.8

PO_BOX_RE = re.compile(r"^\s*(P\.?\s*O\.?\s*BOX|POB|BOX|PMB|P\.?O\.? DRAWER)\b", re.I)
UNIT_RE = re.compile(r"\s+(APT|APARTMENT|STE|SUITE|UNIT|FL|FLR|FLOOR|RM|ROOM|PH|BSMT|#)\.?\s*[\w-]*.*$", re.I)
KIND_RULES = [  # first match wins, on the IRS name
    ("school", r"\b(YESHIVA|YESHIVAS|MESIVTA|TALMUD|TORAH VODAATH|SCHOOL|ACADEMY|KOLLEL|SEMINARY|INSTITUTE|COLLEGE|UNIVERSITY|DAY CARE|DAYCARE|PRESCHOOL|BAIS YAAKOV|BETH JACOB)\b"),
    ("support", r"\b(FUND|FOUNDATION|AUXILIARY|AUX|TRUST|HOUSING|DEVELOPMENT|CEMETERY|CHARITIES|CHARITABLE|BENEVOLENT|RELIEF|FRIENDS OF|ALUMNI|SOCIETY|ASSOCIATION|BUILDING FUND|PRESS|PUBLICATIONS|RADIO|TV|TELEVISION|BROADCAST|CAMP|SENIOR|NURSING|HOSPITAL|COUNCIL|FEDERATION|CONFERENCE|DIOCESE|ARCHDIOCESE|PRESBYTERY|SYNOD|VICARIATE|NETWORK)\b"),
    ("congregation", r"\b(CHURCH|CHURCHES|CONGREGATION|CONG|CHAPEL|TEMPLE|MASJID|MOSQUE|ISLAMIC CENTER|JAME|JAMIA|SYNAGOGUE|SHUL|MINYAN|CHABAD|GURDWARA|SIKH|MANDIR|HINDU|BUDDHIST|ZEN|SANGHA|PARISH|CATHEDRAL|TABERNACLE|ASSEMBLY|FELLOWSHIP|MINISTRIES|MINISTRY|KINGDOM HALL|MISSION|IGLESIA|MINISTERIO|BAPTIST|METHODIST|PENTECOSTAL|EPISCOPAL|LUTHERAN|PRESBYTERIAN|ADVENTIST|ORTHODOX|APOSTOLIC|EVANGELICAL|GOSPEL|KHAL|KEHILLA|BETH|BAIS|ANSHE|AHAVAS)\b"),
]


def kind_of(name: str, foundation: str) -> str:
    for kind, pat in KIND_RULES:
        if re.search(pat, name or "", re.I):
            return kind
    return "congregation" if foundation == "10" else "other"


def main():
    con = connect(config.DB_PATH)
    path = download(IRS_URL, config.RAW / "irs" / config.IRS_FILE)
    zips = ", ".join(f"'{z}'" for z in config.ZIP3)
    rows = con.execute(f"""
        SELECT EIN, NAME, ICO IS NOT NULL AS has_care_of, STREET, CITY, left(ZIP, 5) AS zip5,
               "GROUP" <> '0000' AS group_exempt, SUBSECTION, FOUNDATION, NTEE_CD,
               left(RULING, 4) AS ruling_year, ASSET_AMT, REVENUE_AMT
        FROM read_csv('{path}', all_varchar = true, header = true)
        WHERE left(ZIP, 3) IN ({zips}) AND (FOUNDATION = '10' OR NTEE_CD LIKE 'X%')
    """).fetchall()
    print(f"{len(rows):,} religious organizations registered at {config.CITY_SHORT} ZIP codes")

    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    lock = threading.Lock()
    recs, todo = [], []
    for (ein, name, care_of, street, city, zip5, grp, subsec, found, ntee, ruling,
         assets, revenue) in rows:
        street = (street or "").strip()
        po_box = bool(PO_BOX_RE.search(street))
        unit = UNIT_RE.search(street)
        base = UNIT_RE.sub("", street).strip()
        rec = dict(ein=ein, name=name, name_tokens=" ".join(tokens(name)), kind=kind_of(name, found),
                   has_care_of=care_of, street=street, street_unit=unit.group(0).strip() if unit else None,
                   po_box=po_box, city=city, zip5=zip5, group_exempt=grp, subsection=subsec,
                   foundation=found, ntee=ntee, ruling_year=ruling,
                   assets=int(assets) if assets else None, revenue=int(revenue) if revenue else None,
                   query=None, geo_label=None, geo_confidence=None, bbl=None, bin=None, lat=None, lon=None)
        if not po_box and re.match(r"^\d", base):
            rec["query"] = f"{base}, {city} {config.STATE} {zip5}"
            todo.append(rec)
        recs.append(rec)

    t0, done = time.monotonic(), [0]
    geo = make_geocoder(con)

    def work(rec):
        hit = geo(rec["query"], cache, lock)
        if hit and (hit.get("confidence") or 0) >= MIN_CONFIDENCE and (hit.get("bbl") or hit.get("lat")):
            rec.update(geo_label=hit["label"], geo_confidence=hit["confidence"],
                       bbl=int(hit["bbl"]) if hit.get("bbl") else None, bin=hit["bin"],
                       lat=hit["lat"], lon=hit["lon"])
        with lock:
            done[0] += 1
            if done[0] % 1000 == 0:
                print(f"  geocoded {done[0]:,}/{len(todo):,}, {time.monotonic() - t0:,.0f}s", flush=True)
                CACHE.parent.mkdir(parents=True, exist_ok=True)
                CACHE.write_text(json.dumps(cache))

    with ThreadPoolExecutor(WORKERS) as ex:
        list(ex.map(work, todo))
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(cache))

    cols = list(recs[0])
    con.execute(f"CREATE OR REPLACE TABLE irs_orgs ({', '.join(c + ' ' + t for c, t in zip(cols, [
        'VARCHAR', 'VARCHAR', 'VARCHAR', 'VARCHAR', 'BOOLEAN', 'VARCHAR', 'VARCHAR', 'BOOLEAN',
        'VARCHAR', 'VARCHAR', 'BOOLEAN', 'VARCHAR', 'VARCHAR', 'VARCHAR', 'VARCHAR', 'BIGINT',
        'BIGINT', 'VARCHAR', 'VARCHAR', 'DOUBLE', 'BIGINT', 'VARCHAR', 'DOUBLE', 'DOUBLE']))})")
    con.executemany(f"INSERT INTO irs_orgs VALUES ({', '.join('?' * len(cols))})",
                    [[r[c] for c in cols] for r in recs])
    assign_lots(con, "irs_orgs", "ein")   # points without a parcel (DC's Census fallback)
    print(con.execute("""
        SELECT kind, count(*) AS orgs, count(*) FILTER (WHERE po_box) AS po_box,
               count(*) FILTER (WHERE street_unit IS NOT NULL) AS with_unit,
               count(*) FILTER (WHERE bbl IS NOT NULL) AS on_a_lot
        FROM irs_orgs GROUP BY 1 ORDER BY 2 DESC
    """).df().to_string(index=False))


if __name__ == "__main__":
    main()
