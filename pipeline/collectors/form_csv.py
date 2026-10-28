"""Modulo per organizzatori: Google Form -> foglio Google pubblicato come CSV.

Gli eventi arrivano "in attesa" e il bot Telegram li manda all'amministratore per l'approvazione.
Colonne riconosciute (per parola contenuta nell'intestazione, maiuscole indifferenti):
  titolo, data, ora, fine, luogo/locale, indirizzo, comune, descrizione, link, prezzo, accesso, categoria
"""
from __future__ import annotations

import csv
import io
import logging
from typing import Iterator

from ..config import env
from ..models import Event
from ..textutil import to_local_iso
from . import Context

log = logging.getLogger(__name__)

COLUMNS = {
    "title": ("titolo", "nome evento"), "date": ("data",), "time": ("ora", "orario"), "end": ("fine",),
    "venue": ("luogo", "locale"), "address": ("indirizzo",), "town": ("comune", "citt"),
    "text": ("descrizione",), "url": ("link", "sito"), "price": ("prezzo", "costo"),
    "access": ("accesso", "ingresso"), "category": ("categoria",), "stamp": ("informazioni cronologiche", "timestamp"),
}


def _map_header(header: list[str]) -> dict[str, int]:
    idx = {}
    for i, h in enumerate(header):
        hl = h.lower()
        for key, words in COLUMNS.items():
            if key not in idx and any(w in hl for w in words):
                idx[key] = i
    return idx


def parse(text: str, src: dict) -> Iterator[Event]:
    rows = list(csv.reader(io.StringIO(text)))
    if len(rows) < 2:
        return
    idx = _map_header(rows[0])
    for row in rows[1:]:
        get = lambda k: (row[idx[k]].strip() if k in idx and idx[k] < len(row) else "")  # noqa: E731
        if not get("title") or not get("date"):
            continue
        start, all_day = to_local_iso(f"{get('date')} {get('time')}".strip())
        acc = get("access").lower()
        access = next((a for a in ("invito", "iscrizione", "libero", "biglietto") if a in acc), "sconosciuto")
        yield Event(
            source=src["id"], source_name="Segnalazione organizzatore",
            source_url=get("url") or f"modulo:{get('stamp')}:{get('title')}",
            official_url=get("url"), title=get("title"), start=start, all_day=all_day,
            venue=get("venue"), address=get("address"), town=get("town"), price=get("price"),
            access=access, raw_text=get("text"), status="pending", submitted_by="modulo",
        )


def collect(src: dict, ctx: Context) -> Iterator[Event]:
    url = env("FORM_CSV_URL")
    if not url:
        return
    try:
        # E' il nostro foglio: lettura diretta (robots.txt di Google non riguarda i propri file pubblicati)
        r = ctx.fetcher.client.get(url)
        r.raise_for_status()
        r.encoding = "utf-8"
        yield from parse(r.text, src)
    except Exception as e:  # noqa: BLE001
        log.warning("Modulo organizzatori non letto: %s", e)
