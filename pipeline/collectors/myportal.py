"""Portali comunali MyPortal (Regione Veneto). Stessa API per tutti i comuni che lo usano."""
from __future__ import annotations

import logging
from typing import Iterator

from ..fetch import Blocked
from ..models import Event
from ..textutil import html_to_text, to_local_iso, unescape
from . import Context

log = logging.getLogger(__name__)

GENERIC_PLACES = {"centro storico", "territorio comunale", "varie sedi", "online", "luoghi vari"}


def parse(data: dict, src: dict, places: dict[str, dict]) -> Iterator[Event]:
    base = src["base_url"].rstrip("/")
    for ent in (data.get("page") or {}).get("entities", []):
        a = ent.get("attributes", {})
        start, all_day = to_local_iso(a.get("sys_start_date"))
        end, _ = to_local_iso(a.get("sys_end_date"))
        if end and start and end[:10] == start[:10] and len(end) == 10:
            end = None
        place = places.get(a.get("pnrr_event_place") or "", {})
        pa = place.get("attributes", {})
        # "Centro Storico" e simili sono luoghi generici con indirizzo di comodo: meglio il testo (AI)
        generic = (pa.get("sys_title") or "").lower() in GENERIC_PLACES
        place_title = "" if generic else unescape(pa.get("sys_title", ""))
        place_addr = "" if generic else unescape((pa.get("place_address") or "").split(" - ")[0])
        money = html_to_text(a.get("pnrr_event_money") or "")
        types = a.get("sys_pnrr_type") or {}
        text = "\n".join(filter(None, [
            a.get("sys_sottotitolo", ""), html_to_text(a.get("sys_description") or ""),
            "Costo: " + money if money else "",
            "Tipo (fonte): " + " / ".join(v for v in types.values() if v),
            ("Luogo indicato dal Comune: " + place_title + " " + place_addr) if place_title else "",
        ]))
        yield Event(
            source=src["id"], source_name=src["name"],
            source_url=base + "/home/dettaglio" + (a.get("sys_canonical_url") or "/eventi/" + ent.get("slug", "")),
            title=unescape(a.get("sys_title") or ent.get("name", "")),
            start=start, end=end, all_day=all_day,
            venue=place_title,
            address=place_addr,
            town=src.get("town", "Treviso"),
            price=money[:80],
            raw_text=text[:8000],
            ai_allowed=src.get("ai_rewrite", True),
        )


def collect(src: dict, ctx: Context) -> Iterator[Event]:
    base = src["base_url"].rstrip("/")
    ipa = src["ipa"]
    url = (f"{base}/myportal/{ipa}/api/content?type=pnrr_event&pageIndex=1&onlyNotHidden=true"
           f"&parent=/Eventi&includeSubFolders=true&sortBy=modifiedAt&desc=true&pageSize={src.get('page_size', 40)}")
    try:
        data = ctx.fetcher.get_json(url, max_age=3 * 3600)
    except Blocked as e:
        log.warning("%s: %s", src["id"], e)
        return
    places: dict[str, dict] = {}
    for ent in (data.get("page") or {}).get("entities", []):
        pid = ent.get("attributes", {}).get("pnrr_event_place")
        if pid and pid not in places:
            try:
                places[pid] = ctx.fetcher.get_json(f"{base}/myportal/{ipa}/api/content/{pid}").get("entity", {})
            except Exception as e:  # noqa: BLE001
                log.info("luogo %s non risolto: %s", pid, e)
                places[pid] = {}
    yield from parse(data, src, places)
