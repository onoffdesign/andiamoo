"""Esporta gli eventi pubblicati nel file JSON letto dal sito, e il report delle "scoperte"."""
from __future__ import annotations

import copy
import csv
import hashlib
import json
import math
from collections import Counter
from datetime import datetime, timedelta
from urllib.parse import urlparse

from .config import DATA_DIR, ROOT, settings, taxonomy
from .enrich import SOCIAL, action_link
from .models import Event
from .textutil import ROME, parse_day, today_rome


def visible(ev: Event) -> bool:
    cfg = settings()["pipeline"]
    today = today_rome()
    start = parse_day(ev.start)
    end = parse_day(ev.end) or start
    if not start or ev.lat is None:
        return False
    if end < today - timedelta(days=cfg["keep_past_days"]):
        return False
    return start <= today + timedelta(days=cfg["days_ahead"])


def api_url() -> str:
    """Indirizzo dell'API: quello fisso in settings.yaml, altrimenti quello del tunnel rapido scritto da
    pipeline.tunnel in data/api_url.txt (cambia a ogni avvio del tunnel)."""
    fixed = (settings()["site"].get("api_url") or "").strip()
    if fixed:
        return fixed
    f = DATA_DIR / "api_url.txt"
    return f.read_text(encoding="utf-8").strip() if f.exists() else ""


def scatter(ev: Event) -> tuple[float, float]:
    """Eventi con solo il comune: un punto attorno al centro, diverso per ogni evento ma stabile nel tempo
    (calcolato dall'id), cosi' non finiscono tutti uno sopra l'altro."""
    lo, hi = settings()["geocoding"].get("town_scatter_meters", [150, 650])
    h = hashlib.sha1(ev.uid.encode()).digest()
    angle = int.from_bytes(h[:4], "big") / 2 ** 32 * 2 * math.pi
    dist = lo + (hi - lo) * math.sqrt(int.from_bytes(h[4:8], "big") / 2 ** 32)   # radice: densita' uniforme
    dlat = dist * math.cos(angle) / 111_320
    dlon = dist * math.sin(angle) / (111_320 * math.cos(math.radians(ev.lat)))
    return ev.lat + dlat, ev.lon + dlon


def export(events: list[Event]) -> dict:
    tax = copy.deepcopy(taxonomy())      # copia: la tassonomia in memoria serve ancora al classificatore
    items = []
    for ev in sorted(events, key=lambda e: e.start or ""):
        if not visible(ev):
            continue
        d = ev.public_dict()
        d["action_url"] = action_link(ev)
        lat, lon = scatter(ev) if ev.geo_precision == "town" else (ev.lat, ev.lon)
        d["lat"], d["lon"] = round(lat, 5), round(lon, 5)
        items.append(d)
    payload = {
        "generated": datetime.now(ROME).isoformat(timespec="minutes"),
        "site": {**settings()["site"], "days_ahead": settings()["pipeline"]["days_ahead"], "api_url": api_url()},
        "categories": tax["categories"],
        "access": tax["access"],
        "access_groups": tax.get("access_groups", {}),
        "audiences": tax.get("audiences", {}),
        "audience_filters": tax.get("audience_filters", {}),
        "settings": tax.get("settings", {}),
        "count": len(items),
        "events": items,
    }
    for c in payload["categories"]:
        c.pop("keywords", None)
    out = ROOT / settings()["publish"]["export_path"]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    return payload


def discovery_report(events: list[Event], portals: set[str]) -> int:
    """Siti ufficiali citati negli eventi dei portali: candidati a diventare fonti dirette."""
    counts: Counter[str] = Counter()
    examples: dict[str, str] = {}
    for ev in events:
        if ev.source not in portals:
            continue
        for url in (ev.official_url, ev.ticket_url):
            if not url:
                continue
            host = urlparse(url).netloc.lower().removeprefix("www.")
            if not host or any(s in host for s in ("eventbrite", "ticketone", "dice.fm", "vivaticket")):
                continue
            key = url if any(s in host for s in SOCIAL) else host
            counts[key] += 1
            examples.setdefault(key, ev.title)
    DATA_DIR.mkdir(exist_ok=True)
    with open(DATA_DIR / "scoperte.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["sito_o_profilo", "eventi_trovati", "esempio", "tipo"])
        for key, n in counts.most_common():
            kind = "social (da seguire a mano)" if any(s in key for s in SOCIAL) else "sito (fonte diretta possibile)"
            w.writerow([key, n, examples[key], kind])
    return len(counts)
