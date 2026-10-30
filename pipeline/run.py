"""Giro completo: raccolta -> AI -> geolocalizzazione -> archivio -> deduplica -> export -> pubblicazione.

Uso:
    python -m pipeline.run                    # tutte le fonti attive, pubblica su GitHub
    python -m pipeline.run --source eventbrite --no-publish
    python -m pipeline.run --llm rules        # senza AI (test)
    python -m pipeline.run --export-only      # rigenera il JSON dall'archivio
"""
from __future__ import annotations

import argparse
import logging
import shutil
import sys
import time
from datetime import timedelta

from . import editorial, quality
from .collectors import Context, registry
from .config import DATA_DIR, settings, sources
from .dedupe import dedupe
from .enrich import enrich
from .export import discovery_report, export
from .fetch import Fetcher
from .geocode import Geocoder
from .kinds import occurrences, split
from .places import PlaceFinder
from .llm import make_llm
from .models import Event
from .publish import publish
from .store import Store
from .telegram import Telegram, describe, moderation_buttons
from .textutil import parse_day, today_rome

log = logging.getLogger("pipeline")


def in_window(ev: Event) -> bool:
    cfg = settings()["pipeline"]
    today = today_rome()
    start = parse_day(ev.start)
    end = parse_day(ev.end) or start
    if not start or not ev.title:
        return False
    if end < today:
        return False
    return start <= today + timedelta(days=cfg["days_ahead"])


def run_source(src: dict, ctx: Context, geo: Geocoder, store: Store, tg: Telegram, finder=None) -> dict:
    collect = registry().get(src["type"])
    stats = {"trovati": 0, "nel_periodo": 0, "in_provincia": 0, "nuovi": 0, "errore": ""}
    if not collect:
        stats["errore"] = f"tipo sconosciuto {src['type']}"
        return stats
    t0 = time.time()
    try:
        raw = [e for e in collect(src, ctx)]
    except Exception as e:  # noqa: BLE001 - una fonte rotta non ferma le altre
        log.exception("Fonte %s fallita", src["id"])
        stats["errore"] = str(e)[:200]
        return stats
    stats["trovati"] = len(raw)
    events = [e for e in raw if in_window(e)]
    # coordinate gia' note e fuori dal riquadro della provincia: scartate prima del tetto per fonte
    events = [e for e in events if e.lat is None or geo.in_bbox(e.lat, e.lon)]
    if src.get("max_events"):
        events = sorted(events, key=lambda e: e.start or "")[: int(src["max_events"])]
    stats["nel_periodo"] = len(events)
    if finder is not None:
        finder.begin_batch(events)
    days_ahead = settings()["pipeline"]["days_ahead"]
    for ev in events:
        enrich(ev, ctx.llm)
        # solo eventi specifici: calendari ed elenchi fuori, ricorrenti divisi in date singole
        if ev.kind == "non_evento":
            store.set_status(ev.uid, "rejected")          # se era gia' in archivio esce dal sito
            stats["non_eventi"] = stats.get("non_eventi", 0) + 1
            continue
        if ev.kind == "ricorrente":
            dates = occurrences(ev, days_ahead)
            store.set_status(ev.uid, "rejected")          # al suo posto le date singole
            stats["ricorrenti"] = stats.get("ricorrenti", 0) + 1
            if not dates:
                start, end = parse_day(ev.start), parse_day(ev.end)
                if start and end and (end - start).days > 14:
                    continue                                  # periodo lungo senza date precise: non e' specifico
                ev.kind, dates = "evento", None              # pochi giorni: resta un evento unico
        else:
            dates = None
        if not geo.locate(ev, finder):
            continue
        for item in split(ev, dates) if dates else [ev]:
            ctx.located.add(item.uid)
            if item.geo_precision == "town":
                stats["solo_comune"] = stats.get("solo_comune", 0) + 1
            stats["in_provincia"] += 1
            is_new = store.upsert_event(item)
            stats["nuovi"] += int(is_new)
            if is_new and item.status == "pending" and tg.enabled:
                from .config import env
                tg.send(env("TELEGRAM_ADMIN_CHAT_ID"), "🆕 Segnalazione dal modulo:\n\n" + describe(item),
                        moderation_buttons(item.uid))
    stats["secondi"] = round(time.time() - t0)
    return stats


def relocate_town_level(store: Store, geo: Geocoder, finder, done: set) -> int:
    """Eventi in archivio posizionati solo sul comune e non riletti stanotte: si riprova a trovare il luogo
    (con le regole di geocodifica aggiornate). La cache rende il ripasso quasi gratis."""
    fixed = 0
    for ev in list(store.events("published")):
        if ev.geo_precision != "town" or ev.uid in done or ev.lat is None:
            continue
        old = (ev.lat, ev.lon)
        ev.lat = ev.lon = None
        if geo.locate(ev, finder) and (ev.lat, ev.lon) != old:
            store.update_data(ev)
            fixed += 1
    return fixed


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Pipeline Andiamoo")
    ap.add_argument("--source", action="append", help="solo queste fonti (id)")
    ap.add_argument("--llm", choices=["ollama", "rules"], help="forza il motore AI")
    ap.add_argument("--no-publish", action="store_true")
    ap.add_argument("--export-only", action="store_true")
    ap.add_argument("--offline-geo", action="store_true", help="usa solo la cache di geocoding (test)")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args(argv)

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s", datefmt="%H:%M:%S")
    for noisy in ("httpx", "httpcore"):
        logging.getLogger(noisy).setLevel(logging.WARNING)

    started = time.time()
    store = Store()
    report: dict = {"fonti": {}}
    if not args.export_only:
        llm = make_llm(store, args.llm)
        log.info("Motore AI: %s", llm.name)
        fetcher = Fetcher(store)
        geo = Geocoder(store, offline=args.offline_geo)
        tg = Telegram()
        deep = settings()["geocoding"].get("deep_search", {})
        finder = PlaceFinder(fetcher, llm, store, int(deep.get("max_pages_per_run", 80))) if deep.get("enabled", True) else None
        max_req = settings()["pipeline"]["max_requests_per_source"]
        located: set = set()
        for src in sources():
            if not src.get("enabled", True) or (args.source and src["id"] not in args.source):
                continue
            ctx = Context(fetcher=fetcher, store=store, llm=llm, max_requests=fetcher.requests + max_req, located=located)
            log.info("→ %s", src["name"])
            stats = run_source(src, ctx, geo, store, tg, finder)
            report["fonti"][src["id"]] = stats
            log.info("  %s", stats)
        report["luoghi_ricalcolati"] = relocate_town_level(store, geo, finder, located)
        report["chiamate_ai"] = getattr(llm, "calls", 0)
        report["richieste_web"] = fetcher.requests
        report["richieste_geocoding"] = geo.requests
        if finder is not None:
            report["luoghi_trovati_con_ricerca"] = finder.found
            report["pagine_luogo_lette"] = finder.pages

    published = list(store.events("published"))
    unique = dedupe(published)
    corrections = editorial.load()
    # correzioni e rimozioni della redazione (revisione notturna di Claude), con nuova geocodifica se serve
    unique = editorial.apply_events(unique, None if args.offline_geo else (geo if not args.export_only else Geocoder(store)),
                                    corrections)
    payload = export(unique)
    portals = {s["id"] for s in sources() if s.get("portal")}
    report["scoperte"] = discovery_report(published, portals)
    report["eventi_sul_sito"] = payload["count"]
    report["correzioni_attive"] = len(corrections["correggi"])
    report["rimossi_dalla_redazione"] = len(corrections["rimuovi"])
    log.info("Eventi sul sito: %d (da %d record, deduplicati)", payload["count"], len(published))
    store.log_run(started, report)
    if not args.export_only:
        # coda di revisione per Claude e rapporto del giro, pubblicati in ops/
        ai_on = getattr(llm, "name", "") == "ollama"
        located_events = [e for e in unique if e.lat is not None]
        centers, town_province = {}, {}
        for town in {(e.town or "").strip() for e in located_events if e.town}:
            area = geo.town_area(town)
            if area:
                centers[town.lower()] = (area["lat"], area["lon"])
                if area.get("province"):
                    town_province[town.lower()] = area["province"].replace("IT-", "")
        queue = quality.build_queue(located_events, corrections, ai_on, centers)
        report.update({"giro_pc": True, "motore_ai": getattr(llm, "name", ""), "modello": settings()["llm"]["text_model"] if ai_on else "",
                       "minuti": round((time.time() - started) / 60, 1), "in_revisione": len(queue)})
        quality.write_ops(report, queue, quality.site_reports(store, unique), quality.quality_sample(located_events))
        shutil.copy(DATA_DIR / "scoperte.csv", quality.OPS / "scoperte.csv")
        day_start = time.mktime(today_rome().timetuple())
        quality.append_saturation(quality.saturation_rows(located_events, town_province, store.first_seen_since(day_start)))
        log.info("Coda di revisione: %d eventi", len(queue))

    if not args.no_publish and settings()["publish"]["git_push"]:
        publish(f"Aggiornamento eventi: {payload['count']} eventi")
    return 0


if __name__ == "__main__":
    sys.exit(main())
