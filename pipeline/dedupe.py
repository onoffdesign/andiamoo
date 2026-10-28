"""Deduplica: lo stesso evento pubblicato su piu' fonti diventa un solo punto sulla mappa."""
from __future__ import annotations

import math
import re
import unicodedata

from rapidfuzz import fuzz

from .config import sources
from .models import Event

STOP = {"il", "lo", "la", "i", "gli", "le", "di", "a", "da", "in", "con", "su", "per", "tra", "fra", "e", "al",
        "alla", "allo", "ai", "agli", "alle", "del", "della", "dei", "delle", "nel", "nella", "un", "una", "the"}


def norm_title(t: str) -> str:
    t = unicodedata.normalize("NFKD", t.lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = re.sub(r"[^a-z0-9 ]+", " ", t)
    return " ".join(w for w in t.split() if w not in STOP)


def km(a: Event, b: Event) -> float:
    if None in (a.lat, a.lon, b.lat, b.lon):
        return math.inf
    dlat = math.radians(b.lat - a.lat)
    dlon = math.radians(b.lon - a.lon)
    h = math.sin(dlat / 2) ** 2 + math.cos(math.radians(a.lat)) * math.cos(math.radians(b.lat)) * math.sin(dlon / 2) ** 2
    return 6371 * 2 * math.asin(math.sqrt(h))


def same_event(a: Event, b: Event) -> bool:
    if not a.start or not b.start or a.start[:10] != b.start[:10]:
        return False
    place_ok = (a.town and b.town and norm_title(a.town) == norm_title(b.town)) or km(a, b) < 2.0
    if not place_ok:
        return False
    return fuzz.token_set_ratio(norm_title(a.title), norm_title(b.title)) >= 78


def _portal_ids() -> set[str]:
    return {s["id"] for s in sources() if s.get("portal")}


def richness(e: Event, portals: set[str]) -> tuple:
    """Quale versione tenere come principale: fonti dirette prima dei portali, poi la piu' completa."""
    return (
        e.source not in portals,
        e.geo_precision in ("source", "address"),
        "T" in (e.start or ""),
        bool(e.summary),
        bool(e.official_url),
    )


def dedupe(events: list[Event]) -> list[Event]:
    portals = _portal_ids()
    events = sorted(events, key=lambda e: richness(e, portals), reverse=True)
    kept: list[Event] = []
    for ev in events:
        for k in kept:
            if same_event(k, ev):
                if ev.source_name != k.source_name and all(a["source"] != ev.source_name for a in k.also_on):
                    k.also_on.append({"source": ev.source_name, "url": ev.source_url})
                k.official_url = k.official_url or ev.official_url
                k.ticket_url = k.ticket_url or ev.ticket_url
                k.price = k.price or ev.price
                if k.access == "sconosciuto":
                    k.access = ev.access
                break
        else:
            kept.append(ev)
    return kept
