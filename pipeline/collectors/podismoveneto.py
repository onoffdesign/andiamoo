"""calendariopodismoveneto.blogspot.com: pagine mensili, una riga per gara.

Formato riga:  Comune (PR) [frazione] "Nome gara" km 6 12 18 - ore 9:00 - ...
Tiene solo le province indicate in "provinces" (default TV). Salta le gare ANNULLATE.
"""
from __future__ import annotations

import logging
import re
from datetime import date, timedelta
from typing import Iterator

from bs4 import BeautifulSoup

from ..fetch import Blocked
from ..models import Event
from ..textutil import GIORNI, MESI, today_rome
from . import Context

log = logging.getLogger(__name__)

DAY_RE = re.compile(r"^(?:%s)\s+(\d{1,2})(?:\s+([A-Za-z]+))?" % "|".join(GIORNI), re.I)
ROW_RE = re.compile(r'^(?P<town>[^"()]+?)\s*\((?P<prov>[A-Z]{2})\)\s*(?P<frazione>[^"]*?)\s*"(?P<name>[^"]+)"(?P<rest>.*)$')
KM_RE = re.compile(r"km\s+([\d,.\s]+?)(?=\s*(?:d\+|-|ore|$))", re.I)
ORE_RE = re.compile(r"ore\s+(\d{1,2})[:.](\d{2})", re.I)
MONTH_URL_RE = re.compile(r"/(%s)-(\d{4})\.html" % "|".join(MESI), re.I)


def page_lines(html: str) -> list[str]:
    soup = BeautifulSoup(html, "lxml")
    body = soup.find(class_="post-body") or soup.body
    for br in body.find_all("br"):
        br.replace_with("\n")
    for div in body.find_all("div"):
        div.insert_before("\n")
    text = body.get_text("")
    return [" ".join(ln.replace(" ", " ").split()) for ln in text.splitlines() if ln.strip()]


def parse(html: str, src: dict, url: str, month: int | None, year: int | None) -> Iterator[Event]:
    provinces = {p.upper() for p in src.get("provinces", ["TV"])}
    today = today_rome()
    current: date | None = None
    for line in page_lines(html):
        d = DAY_RE.match(line)
        if d and '"' not in line:
            day = int(d.group(1))
            m = MESI.get((d.group(2) or "").lower()) or month
            y = year or today.year
            if m is None:
                # pagina "nei prossimi giorni": il primo giorno futuro con quel numero
                cand = today
                for _ in range(40):
                    if cand.day == day:
                        break
                    cand += timedelta(days=1)
                current = cand
            else:
                try:
                    current = date(y, m, day)
                except ValueError:
                    current = None
            continue
        r = ROW_RE.match(line)
        if not (r and current):
            continue
        if r.group("prov").upper() not in provinces or "ANNULLAT" in line.upper():
            continue
        rest = r.group("rest")
        km = KM_RE.search(rest)
        ore = ORE_RE.search(rest)
        start = current.isoformat() + (f"T{int(ore.group(1)):02d}:{ore.group(2)}" if ore else "")
        town = r.group("town").strip()
        frazione = r.group("frazione").strip(" -")
        summary = "Corsa/marcia podistica"
        if km:
            summary += " km " + " - ".join(km.group(1).split())
        if ore:
            summary += f", partenza ore {int(ore.group(1))}:{ore.group(2)}"
        fiasp = "FIASP" in rest.upper()
        yield Event(
            source=src["id"], source_name=src["name"], source_url=url,
            title=r.group("name").strip(), start=start, all_day=not ore,
            town=town, venue=frazione, summary=summary + ".",
            category="sport", subcategory="corsa", tags=["FIASP"] if fiasp else [],
            access="iscrizione", needs_ai=False, ai_allowed=False,
        )


def collect(src: dict, ctx: Context) -> Iterator[Event]:
    home = src["base_url"].rstrip("/") + "/"
    try:
        html = ctx.fetcher.get(home, max_age=6 * 3600)
    except Blocked as e:
        log.warning("%s: %s", src["id"], e)
        return
    pages = {home: (None, None)}
    for a in BeautifulSoup(html, "lxml").find_all("a", href=True):
        m = MONTH_URL_RE.search(a["href"])
        if m:
            pages[a["href"]] = (MESI[m.group(1).lower()], int(m.group(2)))
    today = today_rome()
    for url, (month, year) in pages.items():
        if month and (year, month) < (today.year, today.month):
            continue
        if month and (year - today.year) * 12 + month - today.month > 3:
            continue
        try:
            page = html if url == home else ctx.fetcher.get(url, max_age=12 * 3600)
        except Blocked:
            break
        except Exception as e:  # noqa: BLE001
            log.info("pagina %s non letta: %s", url, e)
            continue
        yield from parse(page, src, url, month, year)
