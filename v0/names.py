"""Congregation name normalization and matching, shared by IRS and dedupe steps.

Matching is deliberately conservative. After expanding abbreviations, a name
splits into:
- kind words ("church", "congregation", "ministries", articles, borough names),
  ignored;
- denomination words ("baptist", "roman catholic", "seventh day adventist");
  two names with different denominations never match;
- proper words, the rest ("zion", "mel", "moishe"). Common ones ("first",
  "mount", "holy", "beth", "faith") count only weakly.

Two names match when they share a distinctive proper word and their proper
words mostly overlap, or one's distinctive words are a subset of the other's.
Names with no distinctive word ("First Baptist Church") match only when their
proper and denomination words are identical. Use it only within one lot or
ZIP code, never citywide.
"""

import re
import unicodedata

import config

ABBREV = {
    "st": "saint", "sts": "saints", "ste": "sainte", "san": "saint", "santa": "saint",
    "rc": "roman catholic", "ch": "church", "chr": "church", "chs": "church",
    "cong": "congregation", "congreg": "congregation", "congregacion": "congregation",
    "bapt": "baptist", "bap": "baptist", "bautista": "baptist", "meth": "methodist",
    "metodista": "methodist", "pres": "presbyterian", "presb": "presbyterian",
    "presbiteriana": "presbyterian", "episc": "episcopal", "episcopalian": "episcopal",
    "evang": "evangelical", "evangelica": "evangelical", "evangelico": "evangelical",
    "pent": "pentecostal", "pentecostes": "pentecostal", "pentecostals": "pentecostal",
    "luterana": "lutheran", "catolica": "catholic", "catolico": "catholic",
    "adventista": "adventist", "sda": "seventh day adventist", "sdb": "seventh day baptist",
    "7th": "seventh", "septimo": "seventh", "dia": "day", "ame": "african methodist episcopal", "amez": "african methodist episcopal zion",
    "umc": "united methodist church", "cogic": "church god christ",
    "intl": "international", "int": "international", "min": "ministries",
    "mins": "ministries", "ministry": "ministries", "ministerio": "ministries",
    "ministerios": "ministries", "assem": "assembly", "asamblea": "assembly",
    "tab": "tabernacle", "ctr": "center", "cntr": "center", "centro": "center",
    "cmty": "community", "comm": "community", "mt": "mount", "monte": "mount",
    "ft": "fort", "1st": "first", "2nd": "second", "3rd": "third", "primera": "first",
    "bais": "beth", "beis": "beth", "bet": "beth", "bnai": "bnei", "ahavas": "ahavat",
    "ahavath": "ahavat", "kehal": "khal", "kahal": "khal", "anshei": "anshe",
    "jame": "jamia", "jamaat": "jamia", "mosque": "masjid", "igl": "iglesia",
    "iglesias": "iglesia",
}
KIND = set("""
the of and a an in at for to de la el los las del y al el en du des le
church churches congregation ministries temple masjid center centre international
fellowship assembly worship house god inc incorporated corp corporation co ltd
ny nyc new york city brooklyn bronx queens manhattan staten island usa america
iglesia parish chapel community society association shul synagogue minyan
cathedral tabernacle mission missionary sanctuary
""".split())
if config.CITY == "dc":
    KIND |= {"washington", "dc", "district", "columbia", "nw", "ne", "sw", "se"}
if config.CITY == "charlotte":
    KIND |= {"charlotte", "nc", "carolina"}
if config.CITY == "sf":
    KIND |= {"san", "francisco", "sf", "ca", "california"}
if config.CITY == "houston":
    KIND |= {"houston", "tx", "texas"}
DENOM = set("""
baptist methodist presbyterian lutheran episcopal anglican pentecostal catholic
roman orthodox greek russian ukrainian coptic armenian adventist seventh day
apostolic evangelical reformed nazarene wesleyan african zion christian
jewish islamic muslim buddhist hindu sikh unitarian congregational moravian
""".split())
WEAK = set("""
first second third fourth fifth new true greater mount saint saints sainte holy
faith life gospel family full united world global beth bnei anshe khal kehilat
blessed divine good great living new our
""".split())


def tokens(name: str) -> list[str]:
    s = unicodedata.normalize("NFKD", name or "").encode("ascii", "ignore").decode().lower()
    s = s.replace("’", "'").replace("&", " and ")
    s = re.sub(r"'s\b", "", s).replace("'", "")          # St Mel's -> st mel
    s = re.sub(r"\br\.?\s*c\.?\b", " rc ", s)          # R.C., R C
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    out = []
    for t in s.split():
        out.extend(ABBREV.get(t, t).split())
    return [t for t in out if len(t) > 1 or t.isdigit()]


def parts(name: str) -> tuple[set, set, set]:
    toks = set(tokens(name))
    denom = toks & DENOM
    proper = toks - KIND - DENOM
    return proper, proper - WEAK, denom


def names_match(a: str, b: str) -> bool:
    """Same body, judged from names alone (use only within one lot or ZIP)."""
    pa, sa, da = parts(a)
    pb, sb, db = parts(b)
    if da and db and not (da <= db or db <= da):
        return False                                    # Baptist vs Presbyterian
    if sa and sb:
        if not sa & sb:
            return False
        jacc = len(pa & pb) / len(pa | pb)
        return jacc >= 0.5 or sa <= sb or sb <= sa
    if not sa and not sb:
        return bool(pa or da) and pa == pb and da == db
    return False


if __name__ == "__main__":
    tests = [
        ("Faith SDB Church", "Faith Seventh Day Baptist Church of the Bronx", True),
        ("St Mel's R C Church", "Saint Mel Roman Catholic Church", True),
        ("Greenpoint Shul", "Congregation Ahavas Israel", False),
        ("Congregation Bais Moishe", "CONG BETH MOISHE INC", True),
        ("Little Rock Baptist Church", "St Lydia's Episcopal Church", False),
        ("First Baptist Church", "First Baptist Church of Brooklyn", True),
        ("First Baptist Church", "First Presbyterian Church", False),
        ("Mount Zion Baptist Church", "Mount Olive Baptist Church", False),
        ("Beth Israel", "Beth El Synagogue", False),
        ("Iglesia Pentecostal La Vid Verdadera", "Iglesia C- Eben Ezer Pentecostes INC", False),
        ("Masjid Al-Iman", "Al Iman Mosque", True),
        ("St John's Episcopal Church", "St. John's Church", True),
        ("Iglesia Adventista Del Septimo Dia", "Bethany Lutheran Church", False),
    ]
    bad = 0
    for a, b, want in tests:
        got = names_match(a, b)
        bad += got != want
        print(f"{'ok ' if got == want else 'BAD'} {got!s:5} {a!r} ~ {b!r}")
    print("all pass" if not bad else f"{bad} failing")
