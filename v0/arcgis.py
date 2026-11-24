"""Download whole ArcGIS REST layers, one polite request at a time."""

import json
import urllib.parse
import urllib.request

from common import download, user_agent

PAGE = 2000


def count(layer: str, where: str = "1=1") -> int:
    q = urllib.parse.urlencode({"where": where, "returnCountOnly": "true", "f": "json"})
    req = urllib.request.Request(f"{layer}/query?{q}", headers={"User-Agent": user_agent()})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)["count"]


def pages(layer: str, fields: str, dest_dir, geometry: bool, where: str = "1=1",
          oid: str = "OBJECTID") -> list:
    """Save every row of a layer as JSON pages (GeoJSON when geometry is wanted)."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    total = count(layer, where)
    parts = []
    for i, offset in enumerate(range(0, total, PAGE)):
        params = {"where": where, "outFields": fields, "orderByFields": oid,
                  "resultOffset": offset, "resultRecordCount": PAGE,
                  "returnGeometry": "true" if geometry else "false",
                  "outSR": 4326, "f": "geojson" if geometry else "json"}
        part = dest_dir / f"part-{i:04d}.json"
        if not part.exists():
            print(f"  {layer.split('/rest/services/')[-1]}: {offset:,} of {total:,}", flush=True)
        parts.append(download(f"{layer}/query?{urllib.parse.urlencode(params)}", part))
    return parts
