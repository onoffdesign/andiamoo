"""Pagine con dati strutturati schema.org (JSON-LD): Eventbrite, TicketOne, DICE, 2night, eventiesagre, running.life."""
from __future__ import annotations

import json
import logging
import re
from typing import Iterator
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from ..fetch import Blocked
from ..models import Event
from ..textutil import html_to_text, to_local_iso, today_rome, unescape
from . import Context

log = logging.getLogger(__name__)


def iter_jsonld(html: str) -> Iterator[dict]:
    """Tutti gli oggetti JSON-LD della pagina, appiattiti (array, @graph, ItemList, Place.event)."""
    soup = BeautifulSoup(html, "lxml")
    for tag in soup.find_all("script", type="application/ld+json"):
        raw = tag.string or tag.get_text() or ""
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            # alcuni siti mettono a capo dentro le stringhe: riproviamo in modo tollerante
            try:
                data = json.loads(raw, strict=False)
            except json.JSONDecodeError:
                continue
        yield from _flatten(data)


def _flatten(obj) -> Iterator[dict]:
    if isinstance(obj, list):
        for o in obj:
            yield from _flatten(o)
        return
    if not isinstance(obj, dict):
        return
    if "@graph" in obj:
        yield from _flatten(obj["@graph"])
    if obj.get("@type") == "ItemList" or "itemListElement" in obj:
        for el in obj.get("itemListElement", []):
            yield from _flatten(el.get("item", el) if isinstance(el, dict) else el)
    if isinstance(obj.get("event"), (list, dict)):        # Place con eventi (DICE)
        place = {k: v for k, v in obj.items() if k != "event"}
        for ev in obj["event"] if isinstance(obj["event"], list) else [obj["event"]]:
            if isinstance(ev, dict):
                ev = dict(ev)
                ev.setdefault("location", place)
                yield ev
    yield obj


def is_event(obj: dict) -> bool:
    t = obj.get("@type", "")
    t = " ".join(t) if isinstance(t, list) else str(t)
    return "Event" in t and obj.get("name")


def _address(loc: dict) -> tuple[str, str, str]:
    """(venue, via, comune) da un Place schema.org."""
    if not isinstance(loc, dict):
        return (str(loc or ""), "", "")
    venue = unescape(loc.get("name", ""))
    addr = loc.get("address", "")
    street = town = ""
    if isinstance(addr, dict):
        street = unescape(addr.get("streetAddress", ""))
        town = unescape(addr.get("addressLocality", ""))
    elif isinstance(addr, str):
        street = unescape(addr)
    if town:
        town = town.title() if town.isupper() or town.islower() else town
    if venue and town and venue.lower() == town.lower():
        venue = ""
    return venue, street, town


def to_event(obj: dict, src: dict, page_text: str = "") -> Event | None:
    if not is_event(obj):
        return None
    start, all_day = to_local_iso(obj.get("startDate"))
    end, _ = to_local_iso(obj.get("endDate"))
    if not start:
        return None
    if end == start or (end and start and end[:10] == start[:10] and len(end) == 10):
        end = None if end == start else end
    offers = obj.get("offers") or {}
    if isinstance(offers, list):
        offers = offers[0] if offers else {}
    price = ""
    if isinstance(offers, dict):
        p = offers.get("lowPrice") or offers.get("price")
        if p not in (None, "", "0", "0.0", 0):
            try:
                price = f"da {float(p):.0f} €" if offers.get("lowPrice") else f"{float(p):.0f} €"
            except (TypeError, ValueError):
                price = str(p)
    url = obj.get("url") or ""
    ticket = offers.get("url", "") if isinstance(offers, dict) else ""
    if "/artist/" in url and ticket:          # TicketOne: l'url principale e' l'artista
        url, ticket = ticket, ""
    venue, street, town = _address(obj.get("location", {}))
    geo = (obj.get("location") or {}).get("geo") if isinstance(obj.get("location"), dict) else None
    lat = lon = None
    if isinstance(geo, dict):
        try:
            lat, lon = float(geo.get("latitude")), float(geo.get("longitude"))
        except (TypeError, ValueError):
            pass
    desc = html_to_text(obj.get("description", "") or "")
    free = obj.get("isAccessibleForFree")
    ev = Event(
        source=src["id"], source_name=src["name"], source_url=url,
        title=unescape(obj["name"]), start=start, end=end, all_day=all_day,
        venue=venue, address=street, town=town, lat=lat, lon=lon,
        geo_precision="source" if lat else "",
        price=price, ticket_url=ticket if ticket != url else "",
        access="libero" if free is True else ("biglietto" if price else "sconosciuto"),
        raw_text=(desc + "\n\n" + page_text).strip()[:8000],
        ai_allowed=src.get("ai_rewrite", True),
        category=src.get("default_category"), subcategory=src.get("default_subcategory"),
    )
    # Piattaforme dove la pagina dell'evento e' la pagina di iscrizione/biglietti dell'organizzatore
    # (es. Eventbrite): diventa il link d'azione, cosi' l'evento non finisce in coda per "manca il sito ufficiale".
    if src.get("pagina_iscrizione") and url and not ev.ticket_url:
        ev.ticket_url = url
    return ev


def main_text(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    node = soup.find("article") or soup.find("main") or soup.body
    return html_to_text(str(node)) if node else ""


MESI_CAP = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto",
            "Settembre", "Ottobre", "Novembre", "Dicembre"]


def expand_months(url: str) -> str:
    """{Mese} -> mese corrente, {Mese+1} -> mese successivo (nomi italiani con iniziale maiuscola)."""
    m = today_rome().month - 1
    return url.replace("{Mese}", MESI_CAP[m]).replace("{Mese+1}", MESI_CAP[(m + 1) % 12])


def collect(src: dict, ctx: Context) -> Iterator[Event]:
    seen: set[str] = set()
    pattern = re.compile(src["detail_link_regex"]) if src.get("detail_link_regex") else None
    pages: list[str] = []
    for base in map(expand_months, src.get("listing_urls", [])):
        pages.append(base)
        for n in range(2, int(src.get("max_pages", 1)) + 1):
            if src.get("pagination"):
                pages.append(src["pagination"].format(n=n, base=base))
            elif src.get("page_param"):
                pages.append(f"{base}{'&' if '?' in base else '?'}{src['page_param']}={n}")
    pages = list(dict.fromkeys(pages))

    detail_links: list[str] = []
    for url in pages:
        if ctx.fetcher.requests >= ctx.max_requests:
            break
        try:
            html = ctx.fetcher.get(url, max_age=3 * 3600)       # gli elenchi cambiano spesso
        except Blocked as e:
            log.warning("%s: %s", src["id"], e)
            break
        except Exception as e:  # noqa: BLE001 - una pagina rotta non deve fermare la fonte
            log.warning("%s: errore su %s: %s", src["id"], url, e)
            continue
        for obj in iter_jsonld(html):
            ev = to_event(obj, src)
            if ev and ev.source_url not in seen:
                seen.add(ev.source_url)
                yield ev
        if pattern and src.get("fetch_details"):
            soup = BeautifulSoup(html, "lxml")
            for a in soup.find_all("a", href=True):
                href = urljoin(url, a["href"])
                if pattern.search(href) and href not in detail_links:
                    detail_links.append(href)

    for link in detail_links:
        if link in seen:
            continue
        if ctx.fetcher.requests >= ctx.max_requests:
            log.info("%s: raggiunto il limite di richieste, riprendo al prossimo giro", src["id"])
            break
        try:
            html = ctx.fetcher.get(link)          # cache di qualche giorno: le schede cambiano poco
        except Blocked as e:
            log.warning("%s: %s", src["id"], e)
            break
        except Exception as e:  # noqa: BLE001
            log.warning("%s: errore su %s: %s", src["id"], link, e)
            continue
        text = main_text(html)
        for obj in iter_jsonld(html):
            ev = to_event(obj, src, page_text=text)
            if ev:
                ev.source_url = ev.source_url or link
                if ev.source_url not in seen:
                    seen.add(ev.source_url)
                    yield ev
