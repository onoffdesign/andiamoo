"""Siti WordPress con The Events Calendar (API /wp-json/tribe/events/v1). Es. insolitotrantran.it"""
from __future__ import annotations

import logging
import re
from typing import Iterator

from ..fetch import Blocked
from ..models import Event
from ..textutil import html_to_text, to_local_iso, today_rome, unescape
from . import Context

log = logging.getLogger(__name__)

# Convenzione di molti siti: "Titolo – Comune" oppure "Titolo – Comune (Provincia)"
TITLE_TOWN_RE = re.compile(r"\s[–-]\s([^–\-:]{3,40}?)(?:\s*\(([^)]+)\))?\s*$")
OTHER_PROVINCES = {"venezia", "padova", "vicenza", "belluno", "verona", "rovigo", "pordenone", "udine"}


def parse(data: dict, src: dict) -> Iterator[Event]:
    for e in data.get("events", []):
        start, all_day = to_local_iso(e.get("start_date"))
        end, _ = to_local_iso(e.get("end_date"))
        if e.get("all_day"):
            start, all_day = (start or "")[:10] or None, True
            end = (end or "")[:10] or None
        if end and start and end[:10] == start[:10] and (all_day or len(end) == 10):
            end = None
        v = e.get("venue") if isinstance(e.get("venue"), dict) else {}
        lat = lon = None
        try:
            if v.get("geo_lat"):
                lat, lon = float(v["geo_lat"]), float(v["geo_lng"])
        except (TypeError, ValueError):
            pass
        venue_name = unescape(v.get("venue", ""))
        address = unescape(v.get("address", ""))
        if venue_name == address:
            venue_name = ""
        cats_src = [c.get("name", "") for c in e.get("categories", [])]
        lowered = {c.lower() for c in cats_src}
        if lowered & OTHER_PROVINCES and "treviso" not in lowered:
            continue                              # la fonte stessa lo colloca in un'altra provincia
        title = unescape(e.get("title", ""))
        town = unescape(v.get("city", ""))
        m = TITLE_TOWN_RE.search(title)
        if m:
            if (m.group(2) or "").lower() in OTHER_PROVINCES:
                continue
            cand = m.group(1).strip()
            # un nome di comune e' breve e con l'iniziale maiuscola ("Combai", "San Donà di Piave")
            if not town and cand[:1].isupper() and len(cand.split()) <= 4 and cand.lower() not in OTHER_PROVINCES:
                town = cand
        cost = unescape(e.get("cost", ""))
        yield Event(
            source=src["id"], source_name=src["name"], source_url=e.get("url", ""),
            title=title, start=start, end=end, all_day=all_day,
            venue=venue_name, address=address, town=town,
            lat=lat, lon=lon, geo_precision="source" if lat else "",
            price=cost, ticket_url="", official_url=(e.get("website") or "").strip(),
            raw_text=("Categorie fonte: " + ", ".join(cats_src) + "\n" + html_to_text(e.get("description", "")))[:8000],
            ai_allowed=src.get("ai_rewrite", True),
        )


def collect(src: dict, ctx: Context) -> Iterator[Event]:
    base = src["base_url"].rstrip("/")
    url = (f"{base}/wp-json/tribe/events/v1/events?per_page={src.get('per_page', 50)}"
           f"&start_date={today_rome().isoformat()}")
    for _ in range(int(src.get("max_pages", 5))):
        try:
            data = ctx.fetcher.get_json(url, max_age=3 * 3600)
        except Blocked as e:
            log.warning("%s: %s", src["id"], e)
            return
        yield from parse(data, src)
        url = data.get("next_rest_url")
        if not url:
            return
