"""calendariopodismo.it: elenco gare per localita' + scheda gara (data, comune, distanze, partenza, coordinate).

Lettore a regole, senza AI (il sito chiede use=reference). Email e telefoni non vengono letti.
"""
from __future__ import annotations

import logging
import re
from typing import Iterator
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from ..fetch import Blocked
from ..models import Event
from ..textutil import unescape
from . import Context

log = logging.getLogger(__name__)

LINK_RE = re.compile(r"/gara/\d+/[^/]+/?$")
COORD_RE = re.compile(r"setView\(\[\s*([\d.]+)\s*,\s*([\d.]+)\s*\]")
TIME_RE = re.compile(r"(?:partenza|ritrovo|ore)\D{0,12}(\d{1,2})[:.](\d{2})", re.I)


def parse_detail(html: str, url: str, src: dict) -> Event | None:
    soup = BeautifulSoup(html, "lxml")
    h2 = soup.find("h2")
    date_el = soup.find(class_="data-gara")
    town_el = soup.find(class_="localita-gara")
    if not (h2 and date_el):
        return None
    m = re.search(r"(\d{2})/(\d{2})/(\d{4})", date_el.get_text())
    if not m:
        return None
    day = f"{m.group(3)}-{m.group(2)}-{m.group(1)}"
    text = soup.get_text(" ")
    tm = TIME_RE.search(text)
    start = f"{day}T{int(tm.group(1)):02d}:{tm.group(2)}" if tm else day
    distances = ""
    for row in soup.find_all(class_="info-riga"):
        if "Distanz" in row.get_text():
            val = row.find(class_="info-valore")
            distances = val.get_text(" ", strip=True) if val else ""
    town_raw = unescape(town_el.get_text()) if town_el else ""
    prov = re.search(r"\((\w{2})\)", town_raw)
    town = re.sub(r"\s*\(\w{2}\)", "", town_raw).split(" - ")[-1].strip()
    lat = lon = None
    c = COORD_RE.search(html)
    if c:
        lat, lon = float(c.group(1)), float(c.group(2))
    competitive = bool(soup.find(class_="competitiva-gara"))
    summary = "Gara podistica" + (" competitiva" if competitive else "")
    if distances:
        summary += f": {distances}"
    if tm:
        summary += f", partenza ore {int(tm.group(1))}:{tm.group(2)}"
    return Event(
        source=src["id"], source_name=src["name"], source_url=url,
        title=unescape(h2.get_text()), start=start, all_day=not tm,
        town=town, lat=lat, lon=lon, geo_precision="source" if lat else "",
        summary=summary + ".", category="sport", subcategory="corsa",
        tags=["competitiva"] if competitive else ["non competitiva"],
        access="iscrizione", needs_ai=False, ai_allowed=False,
        raw_text=f"provincia: {prov.group(1) if prov else ''}",
    )


def collect(src: dict, ctx: Context) -> Iterator[Event]:
    skip = re.compile(src["skip_link_regex"]) if src.get("skip_link_regex") else None
    links: list[str] = []
    for listing in src.get("listing_urls", []):
        try:
            html = ctx.fetcher.get(listing, max_age=6 * 3600)
        except Blocked as e:
            log.warning("%s: %s", src["id"], e)
            return
        for a in BeautifulSoup(html, "lxml").find_all("a", href=True):
            href = urljoin(listing, a["href"])
            if LINK_RE.search(href) and href not in links and not (skip and skip.search(href)):
                links.append(href)
    for link in links:
        if ctx.fetcher.requests >= ctx.max_requests:
            break
        try:
            ev = parse_detail(ctx.fetcher.get(link), link, src)
        except Blocked:
            break
        except Exception as e:  # noqa: BLE001
            log.info("%s: scheda non letta %s: %s", src["id"], link, e)
            continue
        if ev:
            yield ev
