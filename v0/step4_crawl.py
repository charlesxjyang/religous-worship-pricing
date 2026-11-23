"""Version 0, step 4a (NYC): fetch congregation websites.

For each place with a website: the homepage, up to 3 linked pages whose link
text or URL mentions worship times, and 1 page about location or directions
(where congregations say where they actually gather). Pages are cached as JSON
under data/nyc/raw/web/, so reruns only fetch what is missing.

Rules enforced here, not in prompts:
- robots.txt is obeyed for our user agent;
- one request at a time per host, REQUEST_PAUSE_S apart;
- social platforms and MassTimes are recorded, never fetched;
- no login, CAPTCHA or paywall handling: a failed page is just recorded.

Run after step 3:  .venv/bin/python v0/step4_crawl.py [--limit N]
"""

import argparse
import datetime as dt
import hashlib
import json
import re
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

import warnings

from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning, XMLParsedAsHTMLWarning

import config
from common import connect, user_agent

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)
warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)

WEB_DIR = config.RAW / "web"
UA_TOKEN = "worship-census-v0"
TIMEOUT_S = 20
MAX_BYTES = 3_000_000
MAX_PAGE_CHARS = 12_000      # per page: first 9,000 and last 3,000 (footers hold addresses)
WORKERS = 24
SCHEDULE_PAGES = 3
LOCATION_PAGES = 1

NO_FETCH_DOMAINS = {  # recorded only
    "facebook.com", "fb.com", "m.facebook.com", "instagram.com", "twitter.com", "x.com",
    "youtube.com", "youtu.be", "tiktok.com", "linkedin.com", "linktr.ee", "wa.me",
    "whatsapp.com", "yelp.com", "google.com", "goo.gl", "g.page", "maps.app.goo.gl",
    "masstimes.org", "yellowpages.com", "mapquest.com", "nextdoor.com", "foursquare.com",
}
SCHEDULE_RE = re.compile(
    r"worship|service|mass|liturg|times|schedule|visit|prayer|jum|salah|salat|iqama|"
    r"shabbat|shabbos|minyan|davening|sunday|sabbath|horario|misa|culto|servicio",
    re.I)
LOCATION_RE = re.compile(
    r"location|direction|contact|find[-_ ]?us|where|campus|address|about|visit|"
    r"ubicaci|contacto|donde", re.I)
SKIP_EXT_RE = re.compile(r"\.(pdf|jpe?g|png|gif|webp|svg|docx?|xlsx?|pptx?|mp3|mp4|mov|zip)$", re.I)


def host_of(url: str) -> str:
    h = (urllib.parse.urlsplit(url).hostname or "").lower()
    return h[4:] if h.startswith("www.") else h


def normalize_url(u: str) -> str | None:
    u = (u or "").strip()
    if not u:
        return None
    if not re.match(r"^https?://", u, re.I):
        u = "http://" + u
    parts = urllib.parse.urlsplit(u)
    if not parts.hostname:
        return None
    return urllib.parse.urlunsplit((parts.scheme.lower(), parts.netloc.lower(),
                                    parts.path or "/", parts.query, ""))


def to_https(url: str) -> str:
    return "https://" + url[len("http://"):] if url.startswith("http://") else url


def is_no_fetch(url: str) -> bool:
    h = host_of(url)
    return any(h == d or h.endswith("." + d) for d in NO_FETCH_DOMAINS)


def site_key(url: str) -> str:
    return hashlib.sha1(url.encode()).hexdigest()[:16]


class HostClient:
    """Sequential, paced fetching for one host, with robots.txt."""

    def __init__(self, host: str):
        self.host = host
        self.last = 0.0
        self.robots = {}

    def _pace(self):
        wait = self.last + config.REQUEST_PAUSE_S - time.monotonic()
        if wait > 0:
            time.sleep(wait)
        self.last = time.monotonic()

    def _raw_get(self, url: str):
        self._pace()
        req = urllib.request.Request(url, headers={
            "User-Agent": user_agent(), "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.5",
        })
        with urllib.request.urlopen(req, timeout=TIMEOUT_S) as r:
            return r.status, r.geturl(), r.headers.get("Content-Type", ""), r.read(MAX_BYTES)

    def allowed(self, url: str) -> bool:
        parts = urllib.parse.urlsplit(to_https(url))
        base = f"{parts.scheme}://{parts.netloc}"
        if base not in self.robots:
            rp = urllib.robotparser.RobotFileParser()
            try:
                status, _, _, body = self._raw_get(base + "/robots.txt")
                rp.parse(body.decode("utf-8", "replace").splitlines())
            except urllib.error.HTTPError as e:
                if e.code in (401, 403):
                    rp.disallow_all = True
                else:
                    rp.allow_all = True
            except Exception:
                rp.allow_all = True
            self.robots[base] = rp
        return self.robots[base].can_fetch(UA_TOKEN, url)

    def get(self, url: str) -> dict:
        rec = {"url": url, "fetched_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")}
        if not self.allowed(url):
            return rec | {"status": None, "error": "robots_disallowed"}
        # The cloud session's proxy carries only HTTPS, so http:// links are
        # fetched as https://. Sites with no HTTPS are recorded as
        # "no_https" and would need a run from a normal network.
        was_http = url.startswith("http://")
        u = to_https(url)
        try:
            status, final, ctype, body = self._raw_get(u)
            rec |= {"status": status, "final_url": final, "content_type": ctype,
                    "sha256": hashlib.sha256(body).hexdigest()}
            if "html" not in ctype.lower() and not body.lstrip()[:15].lower().startswith((b"<!doctype", b"<html")):
                return rec | {"error": "not_html"}
            return rec | parse_html(body, final)
        except urllib.error.HTTPError as e:
            return rec | {"status": e.code, "error": f"http_{e.code}"}
        except Exception as e:  # DNS, TLS, timeout, reset
            err = type(e).__name__ + ": " + str(e)[:150]
            if was_http and ("CERTIFICATE" in err.upper() or "SSL" in err.upper()
                             or "Connection refused" in err or "timed out" in err):
                err = "no_https: " + err
            return rec | {"status": None, "error": err}


def parse_html(body: bytes, base_url: str) -> dict:
    soup = BeautifulSoup(body, "html.parser")
    jsonld = [s.get_text(" ", strip=True)[:4000]
              for s in soup.find_all("script", attrs={"type": "application/ld+json"})]
    links = []
    for a in soup.find_all("a", href=True):
        href = urllib.parse.urljoin(base_url, a["href"].strip())
        if href.startswith(("http://", "https://")):
            links.append((href.split("#")[0], a.get_text(" ", strip=True)[:80]))
    title = soup.title.get_text(strip=True)[:200] if soup.title else ""
    for t in soup(["script", "style", "noscript", "svg", "iframe", "template"]):
        t.decompose()
    lines, prev = [], None
    for line in soup.get_text("\n").splitlines():
        line = " ".join(line.split())
        if line and line != prev:
            lines.append(line)
            prev = line
    text = "\n".join(lines)
    truncated = len(text) > MAX_PAGE_CHARS
    if truncated:
        text = text[:9_000] + "\n[...]\n" + text[-3_000:]
    return {"title": title, "text": text, "jsonld": jsonld, "links": links,
            "n_chars": len(text), "truncated": truncated}


def pick_links(home: dict, start_url: str) -> list[tuple[str, str]]:
    """Pick schedule pages, then a location page, from the homepage's links."""
    host = host_of(home.get("final_url") or start_url)
    seen = {start_url.rstrip("/"), (home.get("final_url") or "").rstrip("/")}
    sched, loc = [], []
    for href, text in home.get("links", []):
        key = href.rstrip("/")
        if key in seen or host_of(href) != host or SKIP_EXT_RE.search(urllib.parse.urlsplit(href).path):
            continue
        hay = text + " " + urllib.parse.urlsplit(href).path
        if SCHEDULE_RE.search(hay):
            sched.append((href, "schedule"))
            seen.add(key)
        elif LOCATION_RE.search(hay):
            loc.append((href, "location"))
            seen.add(key)
    return sched[:SCHEDULE_PAGES] + loc[:LOCATION_PAGES]


def crawl_site(client: HostClient, start_url: str) -> dict:
    out_path = WEB_DIR / f"{site_key(start_url)}.json"
    if out_path.exists():
        return json.loads(out_path.read_text())
    home = client.get(start_url) | {"role": "home"}
    pages = [home]
    if home.get("text") is not None:
        for href, role in pick_links(home, start_url):
            pages.append(client.get(href) | {"role": role})
    for p in pages:
        p.pop("links", None)
    site = {"site_key": site_key(start_url), "start_url": start_url, "pages": pages}
    tmp = out_path.with_suffix(".tmp")
    tmp.write_text(json.dumps(site))
    tmp.rename(out_path)
    return site


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, help="crawl only the first N sites (by key)")
    args = ap.parse_args()
    WEB_DIR.mkdir(parents=True, exist_ok=True)
    con = connect(config.DB_PATH)

    rows = con.execute("SELECT id, websites FROM places").fetchall()
    place_site, sites = [], {}
    for pid, webs in rows:
        urls = [normalize_url(u) for u in (webs or [])]
        urls = [u for u in urls if u]
        fetchable = [u for u in urls if not is_no_fetch(u)]
        social = [u for u in urls if is_no_fetch(u)]
        start = fetchable[0] if fetchable else None
        place_site.append((pid, start, site_key(start) if start else None, social))
        if start:
            sites[site_key(start)] = start
    con.execute("CREATE OR REPLACE TABLE place_site (id VARCHAR, start_url VARCHAR, site_key VARCHAR, social_urls VARCHAR[])")
    con.executemany("INSERT INTO place_site VALUES (?, ?, ?, ?)", place_site)

    todo = sorted(sites.items())
    if args.limit:
        todo = todo[: args.limit]
    by_host = defaultdict(list)
    for key, url in todo:
        by_host[host_of(url)].append(url)
    print(f"{len(todo):,} sites on {len(by_host):,} hosts "
          f"({sum(1 for _, s, _, _ in place_site if s is None):,} places have no fetchable site)")

    done, lock, t0 = 0, threading.Lock(), time.monotonic()

    def run_host(host, urls):
        nonlocal done
        client = HostClient(host)
        for u in urls:
            try:
                crawl_site(client, u)
            except Exception as e:  # never let one site stop the crawl
                print(f"  {u}: {type(e).__name__}: {e}")
            with lock:
                done += 1
                if done % 250 == 0:
                    print(f"  {done:,}/{len(todo):,} sites, {time.monotonic() - t0:,.0f}s", flush=True)

    with ThreadPoolExecutor(WORKERS) as ex:
        for f in as_completed([ex.submit(run_host, h, us) for h, us in by_host.items()]):
            f.result()

    # Index what was fetched.
    page_rows = []
    for key, _ in todo:
        p = WEB_DIR / f"{key}.json"
        if not p.exists():
            continue
        site = json.loads(p.read_text())
        for pg in site["pages"]:
            page_rows.append((key, pg.get("role"), pg.get("url"), pg.get("final_url"),
                              pg.get("status"), pg.get("error"), pg.get("n_chars"),
                              pg.get("fetched_at")))
    con.execute("""CREATE OR REPLACE TABLE crawl_pages (site_key VARCHAR, role VARCHAR, url VARCHAR,
                   final_url VARCHAR, status INT, error VARCHAR, n_chars INT, fetched_at VARCHAR)""")
    con.executemany("INSERT INTO crawl_pages VALUES (?, ?, ?, ?, ?, ?, ?, ?)", page_rows)
    print(con.execute("""
        SELECT role, count(*) AS pages, count(*) FILTER (WHERE n_chars > 0) AS with_text,
               count(*) FILTER (WHERE error = 'robots_disallowed') AS robots_blocked,
               count(*) FILTER (WHERE error IS NOT NULL AND error <> 'robots_disallowed') AS failed
        FROM crawl_pages GROUP BY 1 ORDER BY 1
    """).df().to_string(index=False))
    print(f"done in {time.monotonic() - t0:,.0f}s")


if __name__ == "__main__":
    main()
