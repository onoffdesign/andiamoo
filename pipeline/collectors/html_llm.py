"""Pagina web qualsiasi: il testo va all'AI, che estrae gli eventi. Per siti senza dati strutturati."""
from __future__ import annotations

import logging
from typing import Iterator

from ..fetch import Blocked
from ..llm import RulesLLM
from ..models import Event
from . import Context
from .jsonld import main_text

log = logging.getLogger(__name__)


def collect(src: dict, ctx: Context) -> Iterator[Event]:
    if isinstance(ctx.llm, RulesLLM):
        return
    for url in src.get("listing_urls", []):
        try:
            text = main_text(ctx.fetcher.get(url, max_age=6 * 3600))
        except Blocked as e:
            log.warning("%s: %s", src["id"], e)
            continue
        for f in ctx.llm.extract_events(text, hint=src.get("hint", "")):
            if (f.get("province") or "TV").upper() not in ("TV", "TREVISO"):
                continue
            yield Event(
                source=src["id"], source_name=src["name"], source_url=url,
                title=f.get("title", ""), start=f.get("start") or None, end=f.get("end") or None,
                all_day=len(f.get("start") or "") == 10, summary=f.get("summary", ""),
                category=f.get("category"), subcategory=f.get("subcategory"),
                access=f.get("access") or "sconosciuto", price=f.get("price", ""),
                venue=f.get("venue", ""), address=f.get("address", ""), town=f.get("town", ""),
                ticket_url=f.get("ticket_url", ""), official_url=f.get("official_url", ""),
                ai_summary=bool(f.get("summary")), needs_ai=False,
            )
