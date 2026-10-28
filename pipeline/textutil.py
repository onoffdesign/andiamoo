"""Pulizia testo, date e dati personali."""
from __future__ import annotations

import html
import re
from datetime import date, datetime
from typing import Optional
from zoneinfo import ZoneInfo

from bs4 import BeautifulSoup
from dateutil import parser as dtparser

ROME = ZoneInfo("Europe/Rome")

_WS = re.compile(r"[ \t ]+")
_MANY_NL = re.compile(r"\n{3,}")
EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE_RE = re.compile(r"(?<!\d)(?:\+39[\s.]?)?(?:3\d{2}|0\d{1,3})[\s./-]?\d{3,4}[\s./-]?\d{3,4}(?!\d)")
URL_RE = re.compile(r"https?://\S+")


def html_to_text(raw: str) -> str:
    """HTML -> testo leggibile, a capo sui blocchi."""
    if not raw:
        return ""
    if "<" not in raw:
        return clean_ws(html.unescape(raw))
    soup = BeautifulSoup(raw, "lxml")
    for t in soup(["script", "style", "noscript", "iframe", "svg"]):
        t.decompose()
    for br in soup.find_all("br"):
        br.replace_with("\n")
    text = soup.get_text("\n")
    return clean_ws(html.unescape(text))


def clean_ws(text: str) -> str:
    lines = [_WS.sub(" ", ln).strip() for ln in text.splitlines()]
    text = "\n".join(ln for ln in lines)
    return _MANY_NL.sub("\n\n", text).strip()


def strip_personal_data(text: str) -> str:
    """Toglie email e numeri di telefono (minimizzazione GDPR)."""
    text = EMAIL_RE.sub("[email]", text)
    text = PHONE_RE.sub("[tel]", text)
    return text


def unescape(s: str) -> str:
    return clean_ws(html.unescape(s or "")).replace("\n", " ")


def shorten(text: str, limit: int = 240) -> str:
    text = " ".join(text.split())
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(" ", 1)[0]
    return cut.rstrip(",;:.-") + "…"


def to_local_iso(value: str | None, *, keep_time: bool = True) -> tuple[Optional[str], bool]:
    """Converte una data (ISO, con o senza fuso) in ISO locale Europe/Rome.

    Ritorna (iso, all_day). Se la data non ha orario (o e' 00:00 senza fuso), all_day=True.
    """
    if not value:
        return None, False
    value = value.strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return value, True
    try:
        dt = dtparser.isoparse(value) if "T" in value or "-" in value[:5] else dtparser.parse(value, dayfirst=True)
    except (ValueError, OverflowError):
        try:
            dt = dtparser.parse(value, dayfirst=True)
        except (ValueError, OverflowError):
            return None, False
    # Molte fonti scrivono 00:00 / 23:59 con un fuso approssimativo per dire "tutto il giorno":
    # decidiamo prima di convertire, sull'orario scritto dalla fonte.
    if not keep_time or (dt.hour == 0 and dt.minute == 0) or (dt.hour == 23 and dt.minute >= 59):
        return dt.date().isoformat(), True
    if dt.tzinfo is not None:
        dt = dt.astimezone(ROME)
        if (dt.hour == 0 and dt.minute <= 1) or (dt.hour == 23 and dt.minute >= 59):
            return dt.date().isoformat(), True
    return dt.strftime("%Y-%m-%dT%H:%M"), False


def parse_day(iso: Optional[str]) -> Optional[date]:
    if not iso:
        return None
    try:
        return date.fromisoformat(iso[:10])
    except ValueError:
        return None


def today_rome() -> date:
    return datetime.now(ROME).date()


MESI = {
    "gennaio": 1, "febbraio": 2, "marzo": 3, "aprile": 4, "maggio": 5, "giugno": 6,
    "luglio": 7, "agosto": 8, "settembre": 9, "ottobre": 10, "novembre": 11, "dicembre": 12,
}
GIORNI = ("lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato", "domenica",
          "lunedi", "martedi", "mercoledi", "giovedi", "venerdi")
