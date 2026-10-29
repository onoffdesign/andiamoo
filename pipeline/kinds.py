"""Solo eventi specifici: scarta calendari ed elenchi, divide gli eventi ricorrenti in date singole."""
from __future__ import annotations

import calendar
import copy
import re
from datetime import date, timedelta
from typing import Optional

from .models import Event
from .textutil import parse_day, today_rome

LISTING_RE = re.compile(
    r"\b(calendari[oa]|agenda|programma (mensile|settimanale|degli eventi|eventi)|tutti gli eventi|elenco (degli )?eventi|"
    r"eventi (e sagre|del mese|della settimana|del weekend|in (veneto|italia|provincia))|sagre (in|del) (veneto|italia)|"
    r"guida (agli|ai) eventi|cosa fare (a|in|questo))\b", re.I)
AREA_NAMES = {"italia", "italy", "veneto", "nord italia", "provincia di treviso", "marca trevigiana"}
WEEKDAYS = ["lunedi", "martedi", "mercoledi", "giovedi", "venerdi", "sabato", "domenica"]


def looks_like_listing(ev: Event) -> bool:
    """Regole sicure anche senza AI: titoli da calendario, luogo = una regione intera, durata di quasi un anno."""
    if LISTING_RE.search(ev.title or ""):
        return True
    if (ev.town or ev.venue or "").strip().lower() in AREA_NAMES and not ev.address:
        return True
    start, end = parse_day(ev.start), parse_day(ev.end)
    return bool(start and end and (end - start).days >= 300)


def _nth_weekdays(year: int, month: int, weekday: int, nth: int) -> list[date]:
    days = [date(year, month, d) for d in range(1, calendar.monthrange(year, month)[1] + 1)
            if date(year, month, d).weekday() == weekday]
    if nth == 0:
        return days
    if nth == -1:
        return days[-1:]
    return days[nth - 1:nth] if 1 <= nth <= len(days) else []


def occurrences(ev: Event, days_ahead: int, today: Optional[date] = None) -> list[str]:
    """Date singole di un evento ricorrente, nel periodo dell'evento e nella finestra del sito."""
    rule = ev.recurrence or {}
    today = today or today_rome()
    start = max(parse_day(ev.start) or today, today)
    last = min(parse_day(ev.end) or (today + timedelta(days=days_ahead)), today + timedelta(days=days_ahead))
    if last < start:
        return []
    freq = rule.get("frequenza") or ""
    if freq == "date_elencate" or (rule.get("date_elencate") and freq in ("", "sconosciuta")):
        out = []
        for d in rule.get("date_elencate") or []:
            day = parse_day(str(d))
            if day and start <= day <= last:
                out.append(day.isoformat())
        return sorted(set(out))
    wd = rule.get("giorno_settimana") or ""
    if wd not in WEEKDAYS:
        return []
    weekday = WEEKDAYS.index(wd)
    if freq == "settimanale":
        first = start + timedelta(days=(weekday - start.weekday()) % 7)
        return [(first + timedelta(weeks=i)).isoformat() for i in range(0, 60) if first + timedelta(weeks=i) <= last]
    if freq == "mensile":
        nth = int(rule.get("settimana_del_mese") or 0)
        out, y, m = [], start.year, start.month
        while date(y, m, 1) <= last:
            out += [d.isoformat() for d in _nth_weekdays(y, m, weekday, nth) if start <= d <= last]
            y, m = (y + 1, 1) if m == 12 else (y, m + 1)
        return out
    return []


def split(ev: Event, dates: list[str]) -> list[Event]:
    """Un evento per data, con l'orario dell'originale."""
    time = ev.start[10:] if ev.start and len(ev.start) > 10 else ""
    out = []
    for d in dates:
        e = copy.deepcopy(ev)
        e.start, e.end, e.kind, e.recurrence = d + time, None, "evento", {}
        e.all_day = not time
        out.append(e)
    return out
