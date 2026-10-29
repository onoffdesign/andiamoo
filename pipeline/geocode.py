"""Geolocalizzazione con OpenStreetMap Nominatim (gratis) + verifica della provincia.

Regole d'uso Nominatim: massimo 1 richiesta al secondo, user agent con contatto, cache dei risultati.
La provincia si verifica con il codice ISO3166-2-lvl6 (es. IT-TV).
"""
from __future__ import annotations

import logging
import math
import re
import time
from typing import Optional

import httpx

from .config import settings, user_agent
from .models import Event
from .store import Store

log = logging.getLogger(__name__)

# tipi Nominatim che indicano un'area intera (comune, frazione, quartiere), non un luogo preciso
AREA_TYPES = {"city", "town", "village", "hamlet", "municipality", "suburb", "quarter", "neighbourhood",
              "isolated_dwelling", "locality", "administrative", "county", "state", "region", "province"}
# aree piu' grandi di un comune: "Treviso" puo' essere anche la provincia, il cui centro e' a 15 km dalla citta'
WIDE_TYPES = {"county", "state", "region", "province", "country"}
NOT_PLACES = {"italia", "italy", "tv", "veneto", "provincia di treviso"}


def km_between(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = math.pi / 180
    h = math.sin((lat2 - lat1) * r / 2) ** 2 + math.cos(lat1 * r) * math.cos(lat2 * r) * math.sin((lon2 - lon1) * r / 2) ** 2
    return 2 * 6371 * math.asin(math.sqrt(h))


PROVINCE_CODES = {"treviso": "IT-TV", "venezia": "IT-VE", "padova": "IT-PD", "belluno": "IT-BL",
                  "vicenza": "IT-VI", "verona": "IT-VR", "rovigo": "IT-RO", "pordenone": "IT-PN"}


class Geocoder:
    def __init__(self, store: Store, offline: bool = False):
        cfg = settings()
        self.store = store
        self.offline = offline
        self.url = cfg["geocoding"]["url"]
        self.delay = float(cfg["geocoding"]["min_delay_seconds"])
        b = cfg["area"]["bbox"]
        self.bbox = b
        self.viewbox = f"{b['west']},{b['north']},{b['east']},{b['south']}"
        self.allowed = {PROVINCE_CODES.get(p.lower(), p) for p in cfg["area"]["provinces"]}
        self.client = httpx.Client(headers={"User-Agent": user_agent()}, timeout=20)
        self._last = 0.0
        self.requests = 0
        self.missing: set[str] = set()     # ricerche non in cache (modalita' offline)
        deep = cfg["geocoding"].get("deep_search", {})
        self.max_km = float(deep.get("max_km_from_town", 8))
        self.max_candidates = int(deep.get("max_candidates", 5))

    def _call(self, url: str, params: dict) -> Optional[dict | list]:
        if self.offline:
            return None
        pause = self.delay - (time.time() - self._last)
        if pause > 0:
            time.sleep(pause)
        self._last = time.time()
        self.requests += 1
        try:
            r = self.client.get(url, params=params)
            r.raise_for_status()
            return r.json()
        except (httpx.HTTPError, ValueError) as e:
            log.warning("Nominatim: %s", e)
            return None

    @staticmethod
    def _summarize(hit: dict) -> dict:
        a = hit.get("address", {})
        return {
            "lat": float(hit["lat"]), "lon": float(hit["lon"]),
            "province": a.get("ISO3166-2-lvl6", ""),
            "town": a.get("city") or a.get("town") or a.get("village") or a.get("municipality") or "",
            "type": hit.get("addresstype") or hit.get("type", ""),
        }

    def search(self, query: str) -> Optional[dict]:
        return self._lookup("s|" + query.lower().strip(), {"q": query})

    def _lookup(self, key: str, params: dict) -> Optional[dict]:
        cached = self.store.geo_get(key)
        if cached is not None or self.store.db.execute(
                "SELECT 1 FROM geocode_cache WHERE query=?", (key,)).fetchone():
            return cached
        if self.offline:
            self.missing.add(key)
            return None
        res = self._call(self.url, {**params, "format": "jsonv2", "addressdetails": 1, "limit": 1,
                                    "countrycodes": "it", "viewbox": self.viewbox})
        out = self._summarize(res[0]) if res else None
        self.store.geo_put(key, out)
        return out

    def town_area(self, town: str) -> Optional[dict]:
        """Il comune (o la frazione) come area, mai la provincia omonima.

        Prima la ricerca strutturata per citta', poi quella libera; si scartano province e regioni."""
        tries = [("c|" + town.lower(), {"city": town, "state": "Veneto", "country": "Italia"}),
                 ("s|" + f"{town}, veneto".lower(), {"q": f"{town}, Veneto"}),
                 ("s|" + f"comune di {town}".lower(), {"q": f"Comune di {town}"})]
        for key, params in tries:
            info = self._lookup(key, params)
            if info and info.get("type", "") not in WIDE_TYPES:
                return info
        return None

    @staticmethod
    def place_queries(ev: Event, town: str) -> list[tuple[str, str]]:
        """Luogo e indirizzo interi, poi ogni loro parte separata da virgole ("Mura di Treviso, Porta San Tomaso")."""
        out = []
        if ev.address and town:
            out.append((f"{ev.venue + ', ' if ev.venue else ''}{ev.address}, {town}", "address"))
            out.append((f"{ev.address}, {town}", "address"))
        if ev.venue and town:
            out.append((f"{ev.venue}, {town}", "venue"))
        if town:
            seen = {town.lower()}
            for field, precision in ((ev.address, "address"), (ev.venue, "venue")):
                for part in (field or "").split(","):
                    part = re.sub(r"\b\d{5}\b|\b(TV|Italia|Italy)\b", "", part).strip(" -")
                    if len(part) < 4 or part.lower() in seen or part.lower() in NOT_PLACES:
                        continue
                    seen.add(part.lower())
                    out.append((f"{part}, {town}", precision))
        return list(dict.fromkeys(out))

    def reverse(self, lat: float, lon: float) -> Optional[dict]:
        key = f"r|{lat:.3f},{lon:.3f}"
        cached = self.store.geo_get(key)
        if cached is not None:
            return cached
        if self.offline:
            self.missing.add(key)
            return None
        res = self._call(self.url.replace("/search", "/reverse"),
                         {"lat": lat, "lon": lon, "format": "jsonv2", "zoom": 14, "addressdetails": 1})
        if not res or "lat" not in res:
            return None
        out = self._summarize(res)
        self.store.geo_put(key, out)
        return out

    def in_bbox(self, lat: float, lon: float) -> bool:
        b = self.bbox
        return b["south"] <= lat <= b["north"] and b["west"] <= lon <= b["east"]

    @staticmethod
    def is_area(info: dict) -> bool:
        """Il risultato e' un comune/frazione intero, non un luogo preciso."""
        return info.get("type", "") in AREA_TYPES

    def _apply(self, ev: Event, info: dict, precision: str) -> None:
        ev.lat, ev.lon = info["lat"], info["lon"]
        ev.geo_precision = precision
        if not ev.town:
            ev.town = info["town"]

    def locate(self, ev: Event, finder=None) -> bool:
        """Imposta lat/lon/town/geo_precision. Ritorna True se l'evento e' nella provincia ammessa.

        Se si conosce solo il comune e c'e' un PlaceFinder, cerca il luogo esatto (testo, pagina dell'evento,
        pagine collegate) e accetta solo risultati vicini al comune."""
        if ev.lat is not None and ev.lon is not None:
            if not self.in_bbox(ev.lat, ev.lon):
                return False
            info = self.reverse(ev.lat, ev.lon)
            if info:
                ev.town = ev.town or info["town"]
                return info["province"] in self.allowed
            return True    # nel riquadro ma senza conferma: lo teniamo
        town = ev.town.strip()
        area = None
        if town:
            area = self.town_area(town)
            if area and area["province"] not in self.allowed:
                return False            # il comune e' fuori provincia: scartato
        attempts = self.place_queries(ev, town)
        if not town and ev.venue:
            attempts.append((ev.venue + ", provincia di Treviso", "venue"))
        for query, precision in attempts:
            info = self.search(query)
            if not info or info["province"] not in self.allowed:
                continue
            if self.is_area(info):
                if not town:
                    area = area or info     # senza comune: l'area trovata fa da ripiego
                continue
            if area and km_between(area["lat"], area["lon"], info["lat"], info["lon"]) > self.max_km:
                continue                # omonimo lontano dal comune dell'evento
            self._apply(ev, info, precision)
            return True
        if finder is not None and (town or area):
            if self.deep_search(ev, finder, area):
                return True
        if area:
            self._apply(ev, area, "town")
            return True
        return False

    # ---------------------------------------------------------------- ricerca approfondita
    def deep_search(self, ev: Event, finder, area: Optional[dict]) -> bool:
        tried = 0
        for cand in finder.candidates(ev):
            if tried >= self.max_candidates:
                break
            tried += 1
            hit, precision = self._check_candidate(cand, ev.town or cand.get("town", ""), area)
            if hit:
                self._apply(ev, hit, precision)
                if not ev.venue and cand.get("venue"):
                    ev.venue = cand["venue"]
                if not ev.address and cand.get("address"):
                    ev.address = cand["address"]
                finder.found += 1
                log.debug("Luogo trovato per '%s' (%s): %s", ev.title, cand.get("how"), cand)
                return True
        return False

    def _near(self, area: Optional[dict], lat: float, lon: float) -> bool:
        if not self.in_bbox(lat, lon):
            return False
        return area is None or km_between(area["lat"], area["lon"], lat, lon) <= self.max_km

    def _check_candidate(self, cand: dict, town: str, area: Optional[dict]) -> tuple[Optional[dict], str]:
        if cand.get("lat") is not None:
            if self._near(area, cand["lat"], cand["lon"]):
                return {"lat": cand["lat"], "lon": cand["lon"], "town": town}, "address"
            return None, ""
        town = cand.get("town") or town
        venue, address = cand.get("venue", ""), cand.get("address", "")
        queries = []
        if address and town:
            queries.append((f"{address}, {town}", "address"))
            if venue:
                queries.insert(0, (f"{venue}, {address}, {town}", "address"))
        if venue and town:
            queries.append((f"{venue}, {town}", "venue"))
        for query, precision in queries:
            info = self.search(query)
            if not info or info["province"] not in self.allowed or self.is_area(info):
                continue
            if self._near(area, info["lat"], info["lon"]):
                return info, precision
        return None, ""
