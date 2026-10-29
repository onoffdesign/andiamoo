"""Arricchimento: l'AI completa i dati mancanti e scrive il riassunto neutro; le regole fanno da riserva."""
from __future__ import annotations

import logging
import re

from . import categories as cats
from .llm import RulesLLM
from .models import Event
from .textutil import shorten, strip_personal_data

log = logging.getLogger(__name__)

SOCIAL = ("instagram.com", "facebook.com", "fb.me", "tiktok.com")


def enrich(ev: Event, llm) -> Event:
    use_ai = ev.needs_ai and ev.ai_allowed and not isinstance(llm, RulesLLM)
    if ev.needs_ai:
        known = {k: v for k, v in {
            "title": ev.title, "start": ev.start, "end": ev.end, "venue": ev.venue, "address": ev.address,
            "town": ev.town, "price": ev.price, "category": ev.category, "subcategory": ev.subcategory,
        }.items() if v}
        engine = llm if use_ai else RulesLLM()
        try:
            out = engine.enrich(known, ev.raw_text)
        except Exception as e:  # noqa: BLE001 - se l'AI fallisce si va avanti con le regole
            log.warning("AI non riuscita su '%s': %s", ev.title, e)
            out, use_ai = RulesLLM().enrich(known, ev.raw_text), False
        if use_ai and out.get("summary"):
            ev.summary = shorten(strip_personal_data(out["summary"]), 280)
            ev.ai_summary = True
        for field in ("venue", "address", "town", "price"):
            if not getattr(ev, field) and out.get(field):
                setattr(ev, field, out[field].strip())
        if not ev.category:
            ev.category, ev.subcategory = cats.validate(out.get("category"), out.get("subcategory"))
        elif not ev.subcategory and out.get("category") == ev.category:
            _, ev.subcategory = cats.validate(ev.category, out.get("subcategory"))
        if ev.access == "sconosciuto" and out.get("access") in cats.access_ids():
            ev.access = out["access"]
        if not ev.official_url and out.get("official_url", "").startswith("http"):
            ev.official_url = out["official_url"]
        if not ev.audience and isinstance(out.get("audience"), list):
            ev.audience = [a for a in out["audience"] if a in cats.audience_ids()]
        if not ev.setting and out.get("setting") in cats.setting_ids():
            ev.setting = out["setting"]
        ev.needs_ai = False
    if re.match(r"(?i)^\s*(sconosciut|non (indicat|specificat|disponibil)|n/?d\b|-+$|\?)", ev.price or ""):
        ev.price = ""                     # l'AI a volte scrive "sconosciuto" invece di lasciare vuoto
    if not ev.category:
        ev.category, ev.subcategory = cats.classify_rules(f"{ev.title}\n{ev.summary}\n{ev.raw_text}")
    if not ev.category:
        ev.category = "comunita"
    if ev.access == "sconosciuto":
        ev.access = cats.access_rules(f"{ev.price} {ev.raw_text}")
    blob = f"{ev.title}\n{ev.summary}\n{ev.venue}\n{ev.raw_text}"
    if not ev.audience:
        ev.audience = cats.audience_rules(blob, ev.category)
    if not ev.setting:
        ev.setting = cats.setting_rules(blob, ev.subcategory)
    return ev


def action_link(ev: Event) -> str:
    """Il link "decisivo" (programma ufficiale e iscrizioni): sito ufficiale > biglietteria > pagina fonte."""
    return ev.official_url or ev.ticket_url or ev.source_url
