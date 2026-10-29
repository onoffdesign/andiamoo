"""Eventi della redazione: trovati e verificati dalla revisione notturna di Claude su siti ufficiali.

Legge config/eventi_redazione.yaml:
  eventi:
    - title: "Concerto d'autunno"
      start: 2026-11-14T20:45          # oppure solo la data
      end: ""                          # facoltativo
      venue: Teatro Comunale
      address: Corso del Popolo 31
      town: Treviso
      category: musica                 # id da config/categories.yaml
      access: biglietto                # libero | offerta | biglietto | iscrizione | invito
      price: "da 15 EUR"
      official_url: https://...        # pagina ufficiale (obbligatoria): e' il link d'azione
      summary: "Concerto di musica da camera con quartetto d'archi."   # neutro, scritto da noi
      fonte: https://...               # dove e' stato trovato (articolo, comune...), se diversa
      trovato: 2026-10-30
"""
from __future__ import annotations

import logging
from typing import Iterator

import yaml

from .. import categories as cats
from ..models import Event
from ..textutil import strip_personal_data, to_local_iso
from . import Context

log = logging.getLogger(__name__)


def collect(src: dict, ctx: Context) -> Iterator[Event]:
    from ..editorial import CURATED
    if not CURATED.exists():
        return
    data = yaml.safe_load(CURATED.read_text(encoding="utf-8")) or {}
    for item in data.get("eventi") or []:
        if not (item.get("title") and item.get("start") and item.get("official_url")):
            continue
        start, all_day = to_local_iso(str(item["start"]))
        end, _ = to_local_iso(str(item["end"])) if item.get("end") else (None, False)
        cat, sub = cats.validate(item.get("category"), item.get("subcategory"))
        summary = strip_personal_data(str(item.get("summary") or "")).strip()
        yield Event(
            source=src["id"], source_name=src["name"],
            source_url=str(item.get("fonte") or item["official_url"]),
            title=str(item["title"]).strip(), start=start, end=end, all_day=all_day,
            summary=summary, ai_summary=bool(summary),
            category=cat, subcategory=sub,
            access=item.get("access") if item.get("access") in cats.access_ids() else "sconosciuto",
            audience=[a for a in item.get("audience") or [] if a in cats.audience_ids()],
            setting=item.get("setting") if item.get("setting") in cats.setting_ids() else "",
            price=str(item.get("price") or ""), official_url=str(item["official_url"]),
            venue=str(item.get("venue") or ""), address=str(item.get("address") or ""), town=str(item.get("town") or ""),
            lat=item.get("lat"), lon=item.get("lon"), geo_precision="address" if item.get("lat") else "",
            needs_ai=False, ai_allowed=True,
        )
