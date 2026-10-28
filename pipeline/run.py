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
import sys
import time
from datetime import timedelta

from .collectors import Context, registry
from .config import settings, sources
from .dedupe import dedupe
from .enrich import enrich
from .export import discovery_report, export
from .fetch import Fetcher
from .geocode import Geocoder
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


def run_source(src: dict, ctx: Context, geo: Geocoder, store: Store, tg: Telegram) -> dict:
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
    for ev in events:
        enrich(ev, ctx.llm)
        if not geo.locate(ev):
            continue
        stats["in_provincia"] += 1
        is_new = store.upsert_event(ev)
        stats["nuovi"] += int(is_new)
        if is_new and ev.status == "pending" and tg.enabled:
            from .config import env
            tg.send(env("TELEGRAM_ADMIN_CHAT_ID"), "🆕 Segnalazione dal modulo:\n\n" + describe(ev),
                    moderation_buttons(ev.uid))
    stats["secondi"] = round(time.time() - t0)
    return stats


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
        max_req = settings()["pipeline"]["max_requests_per_source"]
        for src in sources():
            if not src.get("enabled", True) or (args.source and src["id"] not in args.source):
                continue
            ctx = Context(fetcher=fetcher, store=store, llm=llm, max_requests=fetcher.requests + max_req)
            log.info("→ %s", src["name"])
            stats = run_source(src, ctx, geo, store, tg)
            report["fonti"][src["id"]] = stats
            log.info("  %s", stats)
        report["chiamate_ai"] = getattr(llm, "calls", 0)
        report["richieste_web"] = fetcher.requests
        report["richieste_geocoding"] = geo.requests

    published = list(store.events("published"))
    unique = dedupe(published)
    payload = export(unique)
    portals = {s["id"] for s in sources() if s.get("portal")}
    report["scoperte"] = discovery_report(published, portals)
    report["eventi_sul_sito"] = payload["count"]
    log.info("Eventi sul sito: %d (da %d record, deduplicati)", payload["count"], len(published))
    store.log_run(started, report)

    if not args.no_publish and settings()["publish"]["git_push"]:
        publish(f"Aggiornamento eventi: {payload['count']} eventi")
    return 0


if __name__ == "__main__":
    sys.exit(main())
