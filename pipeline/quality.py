"""Controllo qualita' a fine giro: coda di revisione per Claude e rapporto del giro (cartella ops/, in git).

ops/rapporto.json   com'e' andato il giro sul PC (fonti, errori, AI, tempi)
ops/revisione.json  eventi da verificare stanotte, con il motivo, i piu' vicini nel tempo per primi
ops/scoperte.csv    siti ufficiali trovati nei portali: candidati a diventare fonti dirette
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timedelta

from rapidfuzz import fuzz

from .config import ROOT
from .dedupe import norm_title
from .models import Event
from .textutil import ROME, parse_day, today_rome

OPS = ROOT / "ops"
MAX_ITEMS = 60
NEWS_SOURCES = {"google-news-eventi", "qdpnews"}
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿]")


def reasons_for(ev: Event, ai_on: bool) -> list[str]:
    r = []
    if ev.geo_precision == "town":
        r.append("luogo: solo il comune, cerca locale e indirizzo")
    if ev.source in NEWS_SOURCES:
        r.append("da notizia: verifica data, ora e luogo sul sito ufficiale")
    if ev.access == "sconosciuto":
        r.append("accesso sconosciuto (libero, offerta, biglietto, iscrizione, invito?)")
    if not ev.all_day and len(ev.start or "") == 10:
        r.append("orario mancante")
    if "categoria-ripiego" in (ev.tags or []):
        r.append("categoria di ripiego: verifica")
    if ai_on and ev.ai_allowed and not ev.summary:
        r.append("riassunto mancante")
    start, end = parse_day(ev.start), parse_day(ev.end)
    if start and end and (end - start).days > 45:
        r.append("durata oltre 45 giorni: sono date singole o un periodo?")
    if len(ev.title) > 80 or EMOJI.search(ev.title) or (ev.title.isupper() and len(ev.title) > 20):
        r.append("titolo da ripulire")
    if not (ev.official_url or ev.ticket_url):
        r.append("manca il sito ufficiale: cercalo")
    return r


def possible_duplicates(events: list[Event]) -> dict[str, str]:
    """Coppie simili lo stesso giorno non unite dalla deduplica (comuni diversi o titoli un po' diversi)."""
    out = {}
    by_day: dict[str, list[Event]] = {}
    for e in events:
        by_day.setdefault((e.start or "")[:10], []).append(e)
    for day_events in by_day.values():
        for i, a in enumerate(day_events):
            for b in day_events[i + 1:]:
                if fuzz.token_set_ratio(norm_title(a.title), norm_title(b.title)) >= 70:
                    out[b.uid] = a.uid
    return out


def build_queue(events: list[Event], corrections: dict, ai_on: bool) -> list[dict]:
    today = today_rome()
    done = set(corrections["verificati"]) | set(corrections["correggi"]) | set(corrections["rimuovi"])
    dup = possible_duplicates(events)
    items = []
    for ev in events:
        if ev.uid in done:
            continue
        start = parse_day(ev.start)
        end = parse_day(ev.end) or start
        if not start or start > today + timedelta(days=60) or end < today:
            continue
        r = reasons_for(ev, ai_on)
        if ev.uid in dup:
            r.append(f"possibile doppione di {dup[ev.uid]}")
        if not r:
            continue
        items.append({
            "uid": ev.uid, "motivi": r, "titolo": ev.title, "inizio": ev.start, "fine": ev.end,
            "luogo": ev.venue, "indirizzo": ev.address, "comune": ev.town, "categoria": ev.category,
            "accesso": ev.access, "prezzo": ev.price, "fonte": ev.source_name, "pagina_fonte": ev.source_url,
            "sito_ufficiale": ev.official_url or ev.ticket_url, "riassunto": ev.summary,
        })
    # prima i piu' vicini nel tempo, a parita' quelli con piu' problemi
    items.sort(key=lambda d: ((d["inizio"] or "")[:10], -len(d["motivi"])))
    return items[:MAX_ITEMS]


def write_ops(report: dict, queue: list[dict]) -> None:
    OPS.mkdir(exist_ok=True)
    report = {**report, "finito_alle": datetime.now(ROME).isoformat(timespec="minutes")}
    (OPS / "rapporto.json").write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    (OPS / "revisione.json").write_text(json.dumps({"generato": report["finito_alle"], "eventi": queue},
                                                   ensure_ascii=False, indent=1), encoding="utf-8")
