"""Segnalazioni dal sito: estrazione dati da link o immagine, campi mancanti, salvataggio in attesa."""
from __future__ import annotations

import logging
import re
import time
from typing import Optional

from . import categories as cats
from .collectors.jsonld import iter_jsonld, main_text, to_event
from .enrich import enrich
from .fetch import Blocked, Fetcher
from .geocode import Geocoder
from .llm import RulesLLM
from .models import Event
from .places import PlaceFinder
from .store import Store
from .textutil import to_local_iso

log = logging.getLogger(__name__)

SOCIAL_RE = re.compile(r"instagram\.com|facebook\.com|fb\.watch|fb\.me|tiktok\.com|threads\.net", re.I)

# Campi del modulo. I primi tre sono obbligatori per pubblicare.
FIELDS = ["title", "date", "time", "end_date", "venue", "address", "town", "category", "access",
          "price", "official_url", "summary"]
REQUIRED = ["title", "date", "town"]
RECOMMENDED = ["time", "venue", "category"]


class ExtractError(Exception):
    """Errore spiegabile all'utente (codice + messaggio)."""

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code, self.message = code, message


def to_fields(found: dict, url: str = "") -> dict:
    """Dati AI/JSON-LD -> campi del modulo (data e ora separate)."""
    start = (found.get("start") or "").strip()
    end = (found.get("end") or "").strip()
    out = {k: "" for k in FIELDS}
    out.update({
        "title": (found.get("title") or "").strip(),
        "date": start[:10] if re.match(r"\d{4}-\d{2}-\d{2}", start) else "",
        "time": start[11:16] if len(start) >= 16 else "",
        "end_date": end[:10] if re.match(r"\d{4}-\d{2}-\d{2}", end) and end[:10] != start[:10] else "",
        "venue": (found.get("venue") or "").strip(),
        "address": (found.get("address") or "").strip(),
        "town": (found.get("town") or "").strip(),
        "price": (found.get("price") or "").strip(),
        "summary": (found.get("summary") or "").strip(),
        "official_url": (found.get("official_url") or found.get("ticket_url") or "").strip(),
    })
    cat, _ = cats.validate(found.get("category"), found.get("subcategory"))
    if not cat:
        cat, _ = cats.classify_rules(f"{out['title']}\n{out['summary']}")
    out["category"] = cat or ""
    acc = found.get("access")
    out["access"] = acc if acc in cats.access_ids() and acc != "sconosciuto" else ""
    if url and not out["official_url"] and not SOCIAL_RE.search(url):
        out["official_url"] = url
    return out


def missing(fields: dict) -> dict:
    return {
        "required": [f for f in REQUIRED if not (fields.get(f) or "").strip()],
        "recommended": [f for f in RECOMMENDED if not (fields.get(f) or "").strip()],
    }


def extract_from_url(url: str, llm, fetcher: Fetcher) -> list[dict]:
    if not re.match(r"https?://", url or ""):
        raise ExtractError("link_non_valido", "Il link deve iniziare con http:// o https://")
    if SOCIAL_RE.search(url):
        raise ExtractError("social", "I post di Instagram, Facebook e TikTok non si possono leggere in automatico: "
                                     "carica lo screenshot della locandina.")
    try:
        html = fetcher.get(url, use_cache=False)
    except Blocked:
        raise ExtractError("bloccato", "Questo sito non consente la lettura automatica: carica uno screenshot "
                                       "o compila a mano.") from None
    except Exception:  # noqa: BLE001
        raise ExtractError("irraggiungibile", "Non riesco ad aprire il link. Controlla l'indirizzo.") from None
    found = []
    for obj in iter_jsonld(html):
        ev = to_event(obj, {"id": "web", "name": "web"})
        if ev:
            found.append({"title": ev.title, "start": ev.start or "", "end": ev.end or "", "venue": ev.venue,
                          "address": ev.address, "town": ev.town, "price": ev.price,
                          "access": ev.access, "official_url": ev.source_url or url})
    if not found and not isinstance(llm, RulesLLM):
        found = llm.extract_events(main_text(html), hint=f"Pagina: {url}")
    if not found:
        raise ExtractError("nessun_evento", "Non ho trovato un evento in questa pagina: compila i campi a mano.")
    return [to_fields(f, url) for f in found]


def extract_from_image(data: bytes, llm) -> list[dict]:
    if isinstance(llm, RulesLLM):
        raise ExtractError("ai_spenta", "L'analisi delle immagini non e' disponibile ora: compila i campi a mano.")
    found = llm.extract_from_image(data)
    if not found:
        raise ExtractError("nessun_evento", "Non riesco a leggere un evento in questa immagine: compila i campi a mano.")
    return [to_fields(f) for f in found]


def _clean(v, limit=300) -> str:
    return re.sub(r"\s+", " ", str(v or "")).strip()[:limit]


def save_submission(data: dict, store: Store, geo: Geocoder, llm, contact: str = "", fetcher: Optional[Fetcher] = None) -> Event:
    """Valida, arricchisce, geolocalizza e salva in attesa di approvazione."""
    f = {k: _clean(data.get(k), 1500 if k == "summary" else 300) for k in FIELDS}
    miss = missing(f)["required"]
    if miss:
        raise ExtractError("campi_mancanti", "Mancano: " + ", ".join(miss))
    if not re.match(r"\d{4}-\d{2}-\d{2}$", f["date"]):
        raise ExtractError("data_non_valida", "La data deve essere nel formato AAAA-MM-GG")
    start = f["date"] + (f"T{f['time']}" if re.match(r"\d{2}:\d{2}$", f["time"]) else "")
    start, all_day = to_local_iso(start)
    if f["official_url"] and not re.match(r"https?://", f["official_url"]):
        f["official_url"] = ""
    cat, _ = cats.validate(f["category"], None)
    ev = Event(
        source="segnalazioni-web", source_name="Segnalazione",
        source_url=f["official_url"] or f"web:{int(time.time())}:{f['title'][:40]}",
        title=f["title"], start=start, end=f["end_date"] or None, all_day=all_day,
        venue=f["venue"], address=f["address"], town=f["town"], price=f["price"],
        category=cat, access=f["access"] if f["access"] in cats.access_ids() else "sconosciuto",
        official_url=f["official_url"], raw_text=f["summary"], needs_ai=bool(f["summary"]),
        status="pending", submitted_by="web" + (f":{_clean(contact, 120)}" if contact else ""),
    )
    enrich(ev, llm)
    geo.locate(ev, PlaceFinder(fetcher, llm, store, max_pages=3))
    store.upsert_event(ev)
    return ev


def save_report(data: dict, store: Store) -> Optional[Event]:
    uid = _clean(data.get("uid"), 40)
    ev = store.get_event(uid)
    if not ev:
        raise ExtractError("evento_sconosciuto", "Evento non trovato.")
    kind = data.get("tipo") if data.get("tipo") in ("modifica", "rimozione") else "modifica"
    store.add_report(uid, kind, _clean(data.get("messaggio"), 1500), _clean(data.get("contatto"), 120))
    return ev
