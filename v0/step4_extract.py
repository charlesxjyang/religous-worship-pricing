"""Version 0, step 4b (NYC): extract services and gathering places with Claude.

For each crawled site, Claude (a small model, per the plan) reads the pages and
returns, with a verbatim evidence quote for each item:
- where the congregation physically gathers for worship, as distinct from a
  mailing, office or business address (the research cares about the former);
- its regular weekly services;
- whether the site is really this congregation's (it is often a namesake's);
- any congregation it shares space with.

Quotes are checked against the page text in code. Services or places whose
quote is not found are dropped and counted.

Needs WORSHIP_ANTHROPIC_API_KEY (a name chosen so it does not interfere with
Claude Code's own credentials).

Run:  .venv/bin/python v0/step4_extract.py --estimate     # no API calls
      .venv/bin/python v0/step4_extract.py --limit 50     # pilot
      .venv/bin/python v0/step4_extract.py                # all sites
"""

import argparse
import json
import os
import re
import threading
import time
import unicodedata
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed

import config
from common import connect

MODEL = "claude-haiku-5-5"      # plan: small model for bulk extraction
PRICE_IN, PRICE_OUT = 0.10, 0.50  # USD per million tokens, prompts under 100K
MAX_SPEND_USD = 25.0            # hard cap for one run; raise deliberately
MAX_SITE_CHARS = 40_000         # about 10K tokens of page text per site
WORKERS = 8
PROMPT_VERSION = "v0.1"
WEB_DIR = config.RAW / "web"
OUT_DIR = config.DATA / "interim" / "extract"

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
TRADITIONS = ["Catholic", "Protestant and other Christian", "Orthodox Christian", "Jewish",
              "Muslim", "Hindu", "Buddhist", "Sikh", "Other", "Unknown"]
VENUE_KINDS = ["own_building", "another_congregation", "public_school", "private_school",
               "commercial_space", "community_or_other_institution", "home", "online_only",
               "unknown"]

NULLABLE_STR = {"type": ["string", "null"]}
SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["site_match", "site_match_evidence", "is_worshipping_congregation", "tradition",
                 "denomination", "gathering_locations", "mailing_or_office_address",
                 "mailing_evidence", "schedule_found", "services", "shares_space_with",
                 "online_only"],
    "properties": {
        "site_match": {"type": "string", "enum": ["yes", "likely", "no", "unclear"]},
        "site_match_evidence": NULLABLE_STR,
        "is_worshipping_congregation": {"type": "boolean"},
        "tradition": {"type": "string", "enum": TRADITIONS},
        "denomination": NULLABLE_STR,
        "gathering_locations": {"type": "array", "items": {
            "type": "object", "additionalProperties": False,
            "required": ["location_id", "address", "venue_name", "venue_kind", "is_primary", "evidence"],
            "properties": {
                "location_id": {"type": "integer"},
                "address": NULLABLE_STR,
                "venue_name": NULLABLE_STR,
                "venue_kind": {"type": "string", "enum": VENUE_KINDS},
                "is_primary": {"type": "boolean"},
                "evidence": {"type": "string"},
            }}},
        "mailing_or_office_address": NULLABLE_STR,
        "mailing_evidence": NULLABLE_STR,
        "schedule_found": {"type": "boolean"},
        "services": {"type": "array", "items": {
            "type": "object", "additionalProperties": False,
            "required": ["day", "start", "end", "type", "language", "recurrence", "location_id", "evidence"],
            "properties": {
                "day": {"type": "string", "enum": DAYS},
                "start": {"type": "string", "description": "24-hour HH:MM"},
                "end": NULLABLE_STR,
                "type": {"type": "string", "enum": ["main_worship", "weekday_worship", "daily_prayer", "other"]},
                "language": NULLABLE_STR,
                "recurrence": {"type": "string", "enum": ["weekly", "monthly", "seasonal"]},
                "location_id": {"type": ["integer", "null"]},
                "evidence": {"type": "string"},
            }}},
        "shares_space_with": {"type": "array", "items": {
            "type": "object", "additionalProperties": False,
            "required": ["name", "relation", "evidence"],
            "properties": {
                "name": {"type": "string"},
                "relation": {"type": "string", "enum": ["we_host_them", "they_host_us", "unclear"]},
                "evidence": {"type": "string"},
            }}},
        "online_only": {"type": "boolean"},
    },
}

SYSTEM = """You extract facts about one house of worship in New York City from its own website, for a study of how congregations use physical space.

The study cares about WHERE PEOPLE PHYSICALLY GATHER for worship, not where the organization receives mail or keeps an office. Keep these apart:
- gathering_locations: places where services are held in person. Signals: "we meet at", "services are held at", "worship location", "join us at", "our sanctuary", a map or directions to services, an address given with service times. A church that meets in a school, another church, a storefront, a hotel or a home names that venue here.
- mailing_or_office_address: a P.O. box, "mailing address", "office", "administrative office", a pastor's or registered address. Do not list it as a gathering location unless the site also says services are held there.
- If the site gives one street address as the congregation's location with no sign it is only for mail, treat it as a gathering location with venue_kind "own_building" if the site suggests the congregation has its own building, else "unknown".

venue_kind: own_building (its own church, mosque, synagogue or temple); another_congregation (a different congregation's building, e.g. "we worship at St. Mark's", "hosted by"); public_school (P.S., I.S., J.H.S., M.S., H.S., a named public or charter school); private_school; commercial_space (storefront, office floor or suite, retail or industrial building); community_or_other_institution (hotel, theater, community center, college, YMCA, library, funeral home); home; online_only; unknown.

site_match: compare the website with the listing given (name, address, phone). "yes" if the site shows the listing's address or phone; "likely" if the name matches and the site places the congregation in New York City but shows neither; "no" if the site belongs to a different congregation or city (namesakes are common), or is a directory, denomination office, school or business rather than the congregation; "unclear" otherwise. If "no", leave gathering_locations, services and shares_space_with empty.

services: regular services only, each with a stated day and start time. Do not infer times. Skip one-off events, holidays, classes, Bible studies, choir practice and meetings. Use type "main_worship" for the gatherings most members attend: Catholic weekend Masses including the Saturday vigil; Protestant Sabbath or Sunday services; Orthodox Divine Liturgy; Jewish Shabbat services on Friday evening and Saturday morning; Muslim Jumu'ah sessions, one entry per session; for Hindu, Buddhist and Sikh temples the main weekly gathering. Use "weekday_worship" for weekday Masses, midweek services or Vespers, "daily_prayer" for daily minyanim or daily iqama times (one entry per day and time only if listed), "other" for anything else. Each language Mass or service is its own entry. location_id links a service to a gathering location when the site says where it happens.

shares_space_with: other congregations the site says use the same building, either hosted by this one or hosting it.

Every evidence field must be a short quote, under 30 words, copied exactly from the page text, that shows the fact. Choose quotes that do not name clergy or other individuals where the page allows, and never put a person's name or a personal email or phone in any other field. If nothing on the pages shows a fact, leave it out (or null) rather than guess."""


def load_site_text(site: dict) -> tuple[str, bool]:
    """Join a site's pages, dropping lines (menus, footers) already seen."""
    seen, parts, total, cut = set(), [], 0, False
    for i, p in enumerate(site["pages"]):
        text = p.get("text")
        if not text:
            continue
        keep = []
        for line in text.splitlines():
            k = line.strip().lower()
            if k in seen and len(k) < 200:
                continue
            seen.add(k)
            keep.append(line)
        body = "\n".join(keep)
        ld = "\n".join(p.get("jsonld") or [])
        block = f"=== PAGE {i + 1} ({p.get('role')}): {p.get('final_url') or p.get('url')} ===\n{body}"
        if ld:
            block += f"\n[structured data]\n{ld[:3000]}"
        if total + len(block) > MAX_SITE_CHARS:
            block = block[: max(0, MAX_SITE_CHARS - total)]
            cut = True
        parts.append(block)
        total += len(block)
        if total >= MAX_SITE_CHARS:
            break
    return "\n\n".join(parts), cut


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", s or "").lower()
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = re.sub(r"[–—]", "-", s)
    return re.sub(r"\s+", " ", s).strip()


def quote_ok(quote: str | None, haystack_norm: str) -> bool:
    q = norm(quote or "").strip(" .\"'")
    if len(q) < 4:
        return False
    if q in haystack_norm:
        return True
    # Allow a quote that skips a line break or an ellipsis: every piece present.
    pieces = [x.strip() for x in re.split(r"\.\.\.|…", q) if x.strip()]
    return len(pieces) > 1 and all(x in haystack_norm for x in pieces)


def verify(result: dict, text: str) -> dict:
    hay = norm(text)
    stats = Counter()
    for key in ("services", "gathering_locations", "shares_space_with"):
        kept = []
        for item in result.get(key, []):
            ok = quote_ok(item.get("evidence"), hay)
            stats[f"{key}_{'ok' if ok else 'dropped'}"] += 1
            if ok:
                kept.append(item)
        result[key] = kept
    if result.get("mailing_or_office_address") and not quote_ok(result.get("mailing_evidence"), hay):
        stats["mailing_dropped"] += 1
        result["mailing_or_office_address"] = None
    result["schedule_found"] = bool(result.get("services"))
    return {"result": result, "verification": dict(stats)}


def listing_block(rows) -> str:
    lines = []
    for name, address, boro, phones in rows[:5]:
        lines.append(f"- {name} | {address or 'no address'} | {boro} | phone: {', '.join(phones or []) or 'none'}")
    return "Listings that point to this website:\n" + "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int)
    ap.add_argument("--estimate", action="store_true", help="estimate tokens and cost; no API calls")
    args = ap.parse_args()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    con = connect(config.DB_PATH)

    rows = con.execute("""
        SELECT s.site_key, p.name, p.address, p.boroname, p.phones
        FROM place_site s JOIN places p USING (id)
        WHERE s.site_key IS NOT NULL ORDER BY s.site_key, p.confidence DESC
    """).fetchall()
    listings = {}
    for key, *rest in rows:
        listings.setdefault(key, []).append(rest)

    jobs = []
    for key in sorted(listings):
        path = WEB_DIR / f"{key}.json"
        if not path.exists():
            continue
        site = json.loads(path.read_text())
        text, cut = load_site_text(site)
        if len(text) < 200:
            continue  # nothing fetched worth reading
        jobs.append((key, site["start_url"], text, cut))
    if args.limit:
        jobs = jobs[: args.limit]

    sys_chars = len(SYSTEM) + len(json.dumps(SCHEMA))
    est_in = sum((len(t) + sys_chars + 400) / 3.5 for _, _, t, _ in jobs)
    est_out = len(jobs) * 1500  # JSON plus thinking, rough
    est_cost = est_in / 1e6 * PRICE_IN + est_out / 1e6 * PRICE_OUT
    print(f"{len(jobs):,} sites with text; about {est_in / 1e6:.1f}M input tokens; "
          f"estimated cost ${est_cost:.2f} (cap ${MAX_SPEND_USD:.0f})")
    if args.estimate:
        return

    key = os.environ.get("WORSHIP_ANTHROPIC_API_KEY")
    if not key:
        raise SystemExit("Set WORSHIP_ANTHROPIC_API_KEY to run extraction.")
    import anthropic
    client = anthropic.Anthropic(api_key=key, base_url="https://api.anthropic.com", max_retries=4)

    spent, lock, counts = 0.0, threading.Lock(), Counter()

    def run(job):
        nonlocal spent
        skey, url, text, cut = job
        out = OUT_DIR / f"{skey}.json"
        if out.exists():
            counts["cached"] += 1
            return
        with lock:
            if spent >= MAX_SPEND_USD:
                counts["skipped_cap"] += 1
                return
        user = (f"{listing_block(listings[skey])}\n\nWebsite: {url}\n\n"
                f"Pages{' (cut to fit)' if cut else ''}:\n\n{text}")
        try:
            resp = client.messages.create(
                model=MODEL, max_tokens=8000, system=SYSTEM,
                messages=[{"role": "user", "content": user}],
                output_config={"effort": "medium",
                               "format": {"type": "json_schema", "schema": SCHEMA}},
            )
        except anthropic.BadRequestError as e:
            counts["bad_request"] += 1
            print(f"  {skey}: 400 {e.message[:200]}")
            return
        except anthropic.APIStatusError as e:
            counts[f"api_{e.status_code}"] += 1
            return
        except anthropic.APIConnectionError:
            counts["connection"] += 1
            return
        u = resp.usage
        cost = u.input_tokens / 1e6 * PRICE_IN + u.output_tokens / 1e6 * PRICE_OUT
        with lock:
            spent += cost
        rec = {"site_key": skey, "url": url, "model": MODEL, "prompt_version": PROMPT_VERSION,
               "fetched_pages_cut": cut, "stop_reason": resp.stop_reason,
               "usage": {"input": u.input_tokens, "output": u.output_tokens}, "cost_usd": cost,
               "request_id": resp._request_id}
        if resp.stop_reason != "end_turn":
            counts[f"stop_{resp.stop_reason}"] += 1
            rec["result"] = None
        else:
            raw = next(b.text for b in resp.content if b.type == "text")
            rec |= verify(json.loads(raw), text)
            counts["ok"] += 1
        out.write_text(json.dumps(rec))

    t0 = time.monotonic()
    with ThreadPoolExecutor(WORKERS) as ex:
        futs = [ex.submit(run, j) for j in jobs]
        for i, f in enumerate(as_completed(futs), 1):
            f.result()
            if i % 200 == 0:
                print(f"  {i:,}/{len(jobs):,} sites, ${spent:.2f}, {time.monotonic() - t0:,.0f}s", flush=True)
    print(dict(counts), f"spent ${spent:.2f} this run")


if __name__ == "__main__":
    main()
