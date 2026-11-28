"""Pubblicazione dal cloud, senza PC: costruisce docs/data/events.json con quello che c'e' nel repository.

La usa la sessione notturna di Claude, che non ha accesso libero al web dalla riga di comando (niente siti delle
fonti, niente servizio di mappe). Per questo non scarica nulla:
  - eventi gia' sul sito (finche' non sono passati) + tutti gli eventi della redazione (config/eventi_redazione.yaml);
  - correzioni e rimozioni (config/correzioni.yaml), regola fonti (config/fonti-vietate.yaml);
  - posizione: coordinate scritte nell'evento > luogo noto (config/luoghi.yaml) > centro del comune
    (config/comuni.csv, con i punti sparsi attorno al centro come sempre);
  - archivio storico (archivio/AAAA-MM.jsonl) aggiornato con gli eventi pubblicati.
Gli eventi della redazione senza posizione possibile (comune sconosciuto o fuori area) finiscono in
ops/senza-posizione.json: vanno sistemati (comune giusto, oppure lat e lon).

Uso:  python -m pipeline.pubblica            pubblica (scrive i file, il commit lo fa la sessione)
      python -m pipeline.pubblica --prova    mostra i numeri senza scrivere nulla
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import tempfile
from datetime import datetime
from pathlib import Path

from . import archive, editorial
from .collectors import redazione
from .config import ROOT, settings
from .dedupe import dedupe
from .geocode import PROVINCE_CODES, _norm, clean_town, load_known_places
from .models import Event
from .textutil import ROME

COMUNI = ROOT / "config" / "comuni.csv"
NO_PLACE = ROOT / "ops" / "senza-posizione.json"


PREFER = ("TV", "PD", "VE", "VI", "VR", "BL", "RO")    # nomi doppi (Calliano, Samone...): prima il Veneto


def load_towns() -> dict[str, dict]:
    """Comune normalizzato -> {nome, sigla, lat, lon}; anche "comune|SIGLA" per i nomi che esistono in due province."""
    out = {}
    if not COMUNI.exists():
        return out
    lines = [l for l in COMUNI.read_text(encoding="utf-8").splitlines() if l and not l.startswith("#")]
    for r in csv.DictReader(lines):
        info = {"nome": r["comune"], "sigla": r["sigla"], "lat": float(r["lat"]), "lon": float(r["lon"])}
        key = _norm(r["comune"])
        out[f"{key}|{r['sigla']}"] = info
        old = out.get(key)
        if old is None or (r["sigla"] in PREFER and old["sigla"] not in PREFER):
            out[key] = info
    return out


SIGLA_RE = re.compile(r"[\s(,-]+([A-Z]{2})\)?\s*$")


def town_info(town: str, towns: dict, sigla: str = "") -> dict | None:
    """Il comune dal nome; "Calliano (TN)" o la sigla dell'evento scelgono tra i nomi doppi."""
    m = SIGLA_RE.search(town or "")
    sigla = (sigla or (m.group(1) if m else "")).upper()
    key = _norm(clean_town(town or ""))
    return towns.get(f"{key}|{sigla}") or towns.get(key)


def allowed_sigle() -> set[str]:
    from .italia import PROVINCE, all_italy
    if all_italy(settings()["area"]["provinces"]):
        return set(PROVINCE)
    out = set()
    for p in settings()["area"]["provinces"]:
        code = PROVINCE_CODES.get(str(p).lower(), str(p))
        out.add(code.replace("IT-", "").upper())
    return out


def place(ev: Event, towns: dict, known: list, sigle: set) -> str:
    """Mette lat e lon all'evento. Ritorna '' se fatto, altrimenti il motivo."""
    town = clean_town(ev.town)
    info = town_info(ev.town, towns, ev.__dict__.get("provincia", ""))
    if info and info["sigla"] not in sigle:
        return f"comune fuori area ({info['nome']}, {info['sigla']})"
    if ev.lat is not None and ev.lon is not None:
        ev.geo_precision = ev.geo_precision or "address"
        return ""
    text = f" {_norm(ev.venue)} {_norm(ev.address)} "
    for p in known:
        if (not p["town"] or p["town"] == _norm(town)) and any(f" {n} " in text for n in p["names"]):
            ev.lat, ev.lon, ev.geo_precision = p["lat"], p["lon"], "venue"
            return ""
    if not info:
        return f"comune non riconosciuto: {ev.town!r} (scrivi il comune, non la frazione, oppure lat e lon)"
    ev.lat, ev.lon, ev.geo_precision = info["lat"], info["lon"], "town"
    return ""


def site_events(path: Path, towns: dict) -> list[Event]:
    """Eventi gia' pubblicati, rimessi come Event. Quelli con solo il comune tornano al centro del comune
    (export li sparpaglia di nuovo nello stesso modo: niente spostamenti a ogni pubblicazione)."""
    if not path.exists():
        return []
    out = []
    for d in json.loads(path.read_text(encoding="utf-8")).get("events") or []:
        ev = Event.from_dict(d)
        ev.uid_override = d.get("uid")              # l'uid pubblicato resta quello (le correzioni lo usano)
        if ev.geo_precision == "town":
            info = town_info(ev.town, towns)
            if info:
                ev.lat, ev.lon = info["lat"], info["lon"]
        out.append(ev)
    return out


def quality_ops(events: list[Event], towns: dict, old_uids: set, no_place: int) -> dict:
    """Quello che prima scriveva il PC a fine giro: coda di revisione, controllo a campione, posizioni,
    saturazione e rapporto (ops/). Centri dei comuni da config/comuni.csv; "nuovi" = non c'erano sul sito."""
    from . import posizioni, quality
    from .piano_notte import budget
    centers, town_province = {}, {}
    for e in events:
        info = town_info(e.town or "", towns)
        if info:
            centers[(e.town or "").strip().lower()] = (info["lat"], info["lon"])
            town_province[(e.town or "").strip().lower()] = info["sigla"]
    corr = editorial.load()
    pos = posizioni.check(events, centers)
    located = [e for e in events if e.lat is not None]
    queue = quality.build_queue(located, corr, False, centers, posizioni.flagged_uids(pos))
    posizioni.write(pos)
    report = {"giro_pc": False, "giro_cloud": True, "motore_ai": "claude", "eventi_sul_sito": len(located),
              "in_revisione": len(queue), "posizioni": pos["riepilogo"], "senza_posizione": no_place,
              "correzioni_attive": len(corr["correggi"]), "rimossi_dalla_redazione": len(corr["rimuovi"])}
    quality.write_ops(report, queue, None, quality.quality_sample(located, int(budget().get("campione", 10))))
    rows = quality.saturation_rows(located, town_province, {e.uid for e in located} - old_uids)
    quality.append_saturation(rows)
    return {"in_revisione": len(queue), "saturazione": {r["provincia"]: r["nuovi_oggi"] for r in rows}}


def build(write: bool = True) -> dict:
    from .export import export
    towns, known, sigle = load_towns(), load_known_places(), allowed_sigle()
    export_path = ROOT / settings()["publish"]["export_path"]
    site = site_events(export_path, towns)
    src = {"id": "redazione", "name": "Redazione ANDIAMO?"}
    curated, no_place = [], []
    for ev in redazione.collect(src, None):
        why = place(ev, towns, known, sigle)
        if why:
            no_place.append({"titolo": ev.title, "inizio": ev.start, "comune": ev.town, "motivo": why})
            continue
        curated.append(ev)
    cur_uids = {e.uid for e in curated}
    # gli eventi della redazione gia' sul sito si rimpiazzano con la versione aggiornata
    base = [e for e in site if e.source != "redazione" and e.uid not in cur_uids]
    events = dedupe(base + curated)
    corr = editorial.load()
    events = editorial.apply_events(events, geo=None, corr=corr)
    stats = {"sul_sito_prima": len(site), "redazione": len(curated), "senza_posizione": len(no_place)}
    if not write:
        stats["dopo_dedupe"] = len(events)
        return stats
    payload = export(events)
    stats["pubblicati"] = payload["count"]
    shown = {d["uid"] for d in payload["events"]}          # solo cio' che e' davvero sul sito (non i trattenuti)
    stats.update(quality_ops([e for e in events if e.uid in shown], towns, {e.uid for e in site}, len(no_place)))
    NO_PLACE.write_text(json.dumps({"generato": datetime.now(ROME).isoformat(timespec="minutes"),
                                    "eventi": no_place}, ensure_ascii=False, indent=1), encoding="utf-8")
    with tempfile.TemporaryDirectory() as tmp:          # archivio: database temporaneo ricostruito dai file
        from .store import Store
        store = Store(Path(tmp) / "archivio.sqlite")
        archive.seed_from_store(store)
        stats["archivio"] = archive.update(store, payload["events"], corr)
        archive.write_files(store)
        store.db.close()
    return stats


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Pubblicazione dal cloud (senza PC)")
    ap.add_argument("--prova", action="store_true", help="mostra i numeri senza scrivere nulla")
    args = ap.parse_args(argv)
    stats = build(write=not args.prova)
    print(json.dumps(stats, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
