"""Ricerca approfondita del luogo: quando un evento ha solo il comune, si cerca il posto esatto.

Ordine (dal piu' economico):
  1. testo gia' raccolto: "Indirizzo: ...", "Via Roma 5, Treviso", "al Museo Salce – Treviso", nomi di luoghi;
  2. pagina dell'evento sulla fonte: dati schema.org, link a Google Maps, testo (con l'AI se attiva);
  3. pagine collegate dalla stessa fonte (scheda del luogo / "come arrivare") e sito ufficiale dell'evento.
Ogni candidato viene poi verificato dal geocoder: deve cadere vicino al comune dell'evento.
I risultati delle pagine restano in cache, cosi' i giri successivi non riscaricano nulla.
"""
from __future__ import annotations

import logging
import re
from typing import Iterator, Optional
from urllib.parse import parse_qs, unquote, urljoin, urlparse

from bs4 import BeautifulSoup

from .collectors.jsonld import _address, iter_jsonld, main_text
from .fetch import Fetcher
from .llm import RulesLLM
from .models import Event
from .store import Store
from .textutil import html_to_text

log = logging.getLogger(__name__)

STREET = r"(?:Via|V\.le|Viale|Piazza|P\.zza|Piazzale|Piazzetta|Borgo|Vicolo|Corso|C\.so|Strada|Largo|Riviera|Contrada|Calle|Località|Loc\.|Lungosile|Lungargine|Galleria|Salita)"
NAME_WORD = r"(?:di|del|della|dello|dei|delle|degli|de|d['’]|S\.|San|Santa|Santo|[IVXL]+|[A-ZÀ-Ý0-9][\w'’-]*)"
STREET_RE = re.compile(
    rf"(?:(?P<venue>[A-Z0-9](?:[^,\n:;–—|().]|\.(?!\s)){{1,60}}?),\s*)?"
    rf"(?P<street>{STREET}\s+{NAME_WORD}(?:\s+{NAME_WORD}){{0,5}}(?:,?\s*\d{{1,4}}(?:\s?[a-zA-Z]\b|/[0-9a-zA-Z]+|-\d+)?)?)"
    rf"(?:\s*[,–-]\s*(?:\d{{5}}\s+)?(?P<town>[A-Z][A-Za-zÀ-ÿ'’ ]{{2,40}}?))?(?=\W|$)"
)
INDIRIZZO_RE = re.compile(r"(?:Indirizzo|Dove|Luogo|Location|Sede|Ritrovo|Partenza)\s*:\s*([^\n]{3,140})", re.I)
VENUE_WORDS = (r"Teatro|Cinema|Museo|Musei|Auditorium|Villa|Palazzo|Palazzetto|Chiesa|Ex Chiesa|Duomo|Abbazia|Santuario|"
               r"Libreria|Biblioteca|Parco|Castello|Sala|Centro|Casa|Osteria|Trattoria|Ristorante|Hotel|Agriturismo|"
               r"Cantina|Birreria|Pub|Bar|Caff[eè]|Circolo|Stadio|Palestra|Oratorio|Spazio|Galleria|Fondazione|Loggia|"
               r"Barchessa|Grotte|Mulino|Cso|Centro sociale|Arena|Piscina|Bocciodromo|Golf|Tenuta|Distilleria|Club")
VENUE_RE = re.compile(rf"\b((?:{VENUE_WORDS})\s+(?:[A-Z][\w'’&-]*|«[^»]+»|\"[^\"]+\")"
                      rf"(?:\s+(?:di|del|della|dello|dei|delle|de|d['’]|San|Santa|Santo|[A-Z0-9][\w'’&-]*)){{0,4}})")
TITLE_VENUE_RE = re.compile(r"\b(?:al|alla|allo|ai|agli|alle|all['’]|presso|nel|nella|nell['’]|a|ad|da|in)\s*"
                            r"([A-Z][^–—|:]{2,60}?)\s*(?:[–—|-]\s*[A-Z][^–—|]*)?$")
MAPS_RE = re.compile(r"(?:google\.[a-z.]+/maps|maps\.google\.|goo\.gl/maps|maps\.app\.goo\.gl|openstreetmap\.org)", re.I)
LINK_HINT_RE = re.compile(r"/(?:venue|venues|luogo|luoghi|location|locations|sede|sedi|dove|place|places|struttura|organizer|organizzatore)/", re.I)
LINK_TEXT_RE = re.compile(r"^(?:come arrivare|dove(?: siamo)?|mappa|indicazioni|luogo|location|sede)\b", re.I)
GENERIC = {"centro", "piazza", "sala", "casa", "parco", "chiesa", "villa", "teatro", "cinema", "bar", "club", "spazio",
           "centro storico", "il centro", "la piazza"}


def _clean(s: str) -> str:
    s = re.sub(r"\s+", " ", (s or "").replace("’", "'")).strip(" ,.;:–—-\"«»")
    return s[:120]


def _cand(venue="", address="", town="", lat=None, lon=None, how="") -> Optional[dict]:
    venue, address, town = _clean(venue), _clean(address), _clean(re.sub(r"\s*\(.*?\)", "", town or ""))
    venue = re.sub(r"\s+(?:di|del|della|dello|dei|delle|degli|de|d'|a|al|alla|in)$", "", venue, flags=re.I)
    address = re.sub(r"\s+(?:di|del|della|dello|dei|delle|degli|de|d')$", "", address, flags=re.I)
    if re.fullmatch(rf"{STREET}", address, flags=re.I):
        address = ""
    if venue and town and venue.lower() == town.lower():
        venue = ""
    if re.match(r"^(?:dal|dalla|dalle|dai|ore|il|la|le|lo|gli|un|una|e|ed|con|per|tra|fra)\b", venue):
        venue = ""
    if venue.lower() in GENERIC or len(venue) < 3:
        venue = ""
    if venue and re.match(rf"^{STREET}\b", venue):          # "Via Roma" non e' un nome di luogo
        address, venue = address or venue, ""
    if not (venue or address or lat is not None):
        return None
    return {"venue": venue, "address": address, "town": town, "lat": lat, "lon": lon, "how": how}


def from_text(title: str, text: str, town: str = "") -> list[dict]:
    """Candidati dal testo, in ordine di affidabilita'."""
    text = html_to_text(text or "") if "<" in (text or "") else (text or "")
    town = re.sub(r"\s*\(.*?\)", "", town or "").strip()
    out: list[dict] = []
    for m in INDIRIZZO_RE.finditer(text):
        parts = [p.strip() for p in re.split(r",|–|—", m.group(1)) if p.strip()]
        street = next((p for p in parts if re.match(rf"^{STREET}\b", p)), "")
        venue = next((p for p in parts if p != street and not re.match(r"^\d{5}", p)), "")
        tw = next((p for p in parts[parts.index(street) + 1:] if not re.match(r"^\d", p)), "") if street else ""
        out.append(_cand(venue if venue.lower() != (town or "").lower() else "", street, tw, how="indirizzo"))
    for m in STREET_RE.finditer(text):
        out.append(_cand(m.group("venue") or "", m.group("street"), m.group("town") or "", how="via"))
    if town:
        for m in re.finditer(rf"[–—-]\s*([A-Z][^,–—\n]{{2,60}}?),\s*{re.escape(town)}\b", text):
            out.append(_cand(m.group(1), "", town, how="luogo, comune"))
    m = TITLE_VENUE_RE.search(title or "")
    if m:
        v = m.group(1).strip()
        if not town or v.lower() != town.lower():
            out.append(_cand(v, how="titolo"))
    seen_v = 0
    for m in VENUE_RE.finditer(f"{title}\n{text}"):
        if re.search(rf"{STREET}\s*$", f"{title}\n{text}"[:m.start()]):     # "Via Palazzo 41": e' una via
            continue
        out.append(_cand(m.group(1), how="nome luogo"))
        seen_v += 1
        if seen_v >= 3:
            break
    uniq, keys = [], set()
    for c in out:
        if not c:
            continue
        k = (c["venue"].lower(), c["address"].lower())
        if k not in keys:
            keys.add(k)
            uniq.append(c)
    return uniq


def maps_coords(url: str) -> Optional[tuple[float, float]]:
    """Coordinate da un link di Google Maps / OpenStreetMap, se presenti."""
    u = unquote(url)
    for pat in (r"@(-?\d+\.\d+),(-?\d+\.\d+)", r"[?&](?:q|query|ll|destination|daddr)=(-?\d+\.\d+),\s*(-?\d+\.\d+)",
                r"[?&]mlat=(-?\d+\.\d+)&mlon=(-?\d+\.\d+)", r"!3d(-?\d+\.\d+)!4d(-?\d+\.\d+)"):
        m = re.search(pat, u)
        if m:
            return float(m.group(1)), float(m.group(2))
    return None


def maps_query(url: str) -> str:
    q = parse_qs(urlparse(url).query)
    for k in ("q", "query", "destination", "daddr"):
        if q.get(k) and not re.match(r"^-?\d+\.\d+,", q[k][0]):
            return q[k][0]
    m = re.search(r"/maps/(?:place|search)/([^/@?]+)", unquote(url))
    return m.group(1).replace("+", " ") if m else ""


class PlaceFinder:
    """Trova candidati per il luogo di un evento. Le pagine si scaricano solo se il testo non basta."""

    def __init__(self, fetcher: Optional[Fetcher], llm, store: Store, max_pages: int = 80):
        self.fetcher, self.llm, self.store = fetcher, llm, store
        self.max_pages = max_pages
        self.pages = 0
        self.shared_urls: set[str] = set()      # pagine-elenco con piu' eventi: non dicono il luogo del singolo
        self.found = 0

    def begin_batch(self, events: list[Event]) -> None:
        seen: dict[str, int] = {}
        for e in events:
            seen[e.source_url] = seen.get(e.source_url, 0) + 1
        self.shared_urls = {u for u, n in seen.items() if n > 1}

    def candidates(self, ev: Event) -> Iterator[dict]:
        yield from from_text(ev.title, ev.raw_text, ev.town)
        urls = [ev.source_url]
        if ev.official_url and urlparse(ev.official_url).netloc != urlparse(ev.source_url).netloc:
            urls.append(ev.official_url)
        for url in urls:
            if not url.startswith("http") or url in self.shared_urls:
                continue
            yield from self.from_page(url, ev, follow=True)

    # ---------------------------------------------------------------- pagine
    def _cached(self, url: str) -> Optional[list[dict]]:
        v = self.store.ai_get("place|" + url)
        return v.get("c", []) if isinstance(v, dict) else None

    def from_page(self, url: str, ev: Event, follow: bool) -> list[dict]:
        cached = self._cached(url)
        if cached is not None:
            return cached
        if self.fetcher is None or self.pages >= self.max_pages:
            return []
        self.pages += 1
        try:
            html = self.fetcher.get(url)
        except Exception as e:  # noqa: BLE001 - pagina irraggiungibile o vietata da robots.txt
            log.debug("Luogo: pagina non letta %s (%s)", url, e)
            self.store.ai_put("place|" + url, {"c": []})
            return []
        found = self.parse_page(html, url, ev)
        if follow and not any(c.get("lat") is not None or c.get("address") for c in found):
            for link in self.related_links(html, url)[:2]:
                found += self.from_page(link, ev, follow=False)
        self.store.ai_put("place|" + url, {"c": found})
        return found

    def parse_page(self, html: str, url: str, ev: Event) -> list[dict]:
        out: list[dict] = []
        for obj in iter_jsonld(html):
            loc = obj.get("location") if isinstance(obj, dict) else None
            if isinstance(obj, dict) and obj.get("@type") in ("Place", "LocalBusiness", "EventVenue") and obj.get("address"):
                loc = obj
            if not loc:
                continue
            for item in loc if isinstance(loc, list) else [loc]:
                venue, street, town = _address(item)
                geo = item.get("geo") if isinstance(item, dict) else None
                lat = lon = None
                if isinstance(geo, dict):
                    try:
                        lat, lon = float(geo["latitude"]), float(geo["longitude"])
                    except (KeyError, TypeError, ValueError):
                        pass
                out.append(_cand(venue, street, town, lat, lon, how="schema.org"))
        soup = BeautifulSoup(html, "lxml")
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if not MAPS_RE.search(href):
                continue
            co = maps_coords(href)
            if co:
                out.append(_cand(lat=co[0], lon=co[1], how="mappa"))
            elif maps_query(href):
                q = maps_query(href)
                parts = [p.strip() for p in q.split(",")]
                street = next((p for p in parts if re.match(rf"^{STREET}\b", p)), "")
                out.append(_cand(parts[0] if parts[0] != street else "", street, "", how="mappa"))
        for frame in soup.find_all("iframe", src=True):
            if MAPS_RE.search(frame["src"]) and (co := maps_coords(frame["src"])):
                out.append(_cand(lat=co[0], lon=co[1], how="mappa"))
        text = main_text(html)
        out += from_text("", text, ev.town)
        if not any(c and (c["address"] or c["lat"] is not None) for c in out) and not isinstance(self.llm, RulesLLM) \
                and hasattr(self.llm, "extract_place"):
            try:
                p = self.llm.extract_place(ev.title, text)
                out.append(_cand(p.get("venue", ""), p.get("address", ""), p.get("town", ""), how="ai"))
            except Exception as e:  # noqa: BLE001
                log.debug("AI luogo non riuscita: %s", e)
        return [c for c in out if c]

    @staticmethod
    def related_links(html: str, url: str) -> list[str]:
        """Link interni alla scheda del luogo o a "come arrivare"."""
        host = urlparse(url).netloc
        soup = BeautifulSoup(html, "lxml")
        links = []
        for a in soup.find_all("a", href=True):
            href = urljoin(url, a["href"]).split("#")[0]
            if urlparse(href).netloc != host or href == url:
                continue
            if LINK_HINT_RE.search(urlparse(href).path) or LINK_TEXT_RE.match(a.get_text(" ", strip=True)):
                links.append(href)
        return list(dict.fromkeys(links))
