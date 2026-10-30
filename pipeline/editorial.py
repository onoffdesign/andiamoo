"""Redazione: correzioni e rimozioni decise dalla revisione notturna di Claude (o a mano).

File (in git, cosi' PC e revisione cloud vedono gli stessi dati):
  config/correzioni.yaml
    correggi:   { <uid>: { campo: valore, ..., nota: "perche'", verificato: AAAA-MM-GG } }
    rimuovi:    { <uid>: "motivo" }
    verificati: { <uid>: AAAA-MM-GG }        # controllati e gia' corretti: escono dalla coda di revisione

Le correzioni valgono per l'uid pubblicato sul sito (dopo la deduplica). Si applicano:
  - sul PC a ogni export, ricalcolando le coordinate se cambiano luogo o indirizzo;
  - nel cloud con `python -m pipeline.editorial --applica`, direttamente su docs/data/events.json
    (senza geocodifica: le coordinate cambiano solo se la correzione le indica).

Comandi:
  python -m pipeline.editorial --controlla          verifica che i file della redazione siano validi
  python -m pipeline.editorial --applica            applica correzioni e rimozioni al sito pubblicato
"""
from __future__ import annotations

import argparse
import copy
import json
import logging
import re
import sys
from datetime import date
from typing import Optional

import yaml

from . import categories as cats
from .config import ROOT, settings
from .models import Event

log = logging.getLogger(__name__)

CORRECTIONS = ROOT / "config" / "correzioni.yaml"
CURATED = ROOT / "config" / "eventi_redazione.yaml"

EDITABLE = {"title", "start", "end", "all_day", "summary", "category", "subcategory", "access", "price", "venue",
            "address", "town", "official_url", "ticket_url", "audience", "setting", "lat", "lon"}
PLACE_FIELDS = {"venue", "address", "town"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2})?$")


def load(path=None) -> dict:
    path = path or CORRECTIONS
    data = yaml.safe_load(path.read_text(encoding="utf-8")) if path.exists() else None
    data = data or {}
    return {k: dict(data.get(k) or {}) for k in ("correggi", "rimuovi", "verificati")}


# ---------------------------------------------------------------- validazione
def validate_fields(fields: dict, where: str) -> list[str]:
    errs = []
    for k, v in fields.items():
        if k in ("nota", "verificato"):
            continue
        if k not in EDITABLE:
            errs.append(f"{where}: campo non modificabile '{k}'")
        elif k in ("start", "end") and v and not DATE_RE.match(str(v)):
            errs.append(f"{where}: {k} deve essere AAAA-MM-GG o AAAA-MM-GGTHH:MM, non '{v}'")
        elif k == "category" and cats.canonical(v) not in cats.category_ids():
            errs.append(f"{where}: categoria sconosciuta '{v}'")
        elif k == "access" and v not in cats.access_ids():
            errs.append(f"{where}: accesso sconosciuto '{v}'")
        elif k == "audience" and (not isinstance(v, list) or any(a not in cats.audience_ids() for a in v)):
            errs.append(f"{where}: audience deve essere una lista tra {cats.audience_ids()}")
        elif k in ("official_url", "ticket_url") and v and not str(v).startswith("http"):
            errs.append(f"{where}: {k} deve essere un link http(s)")
        elif k in ("lat", "lon"):
            try:
                float(v)
            except (TypeError, ValueError):
                errs.append(f"{where}: {k} deve essere un numero")
    if ("lat" in fields) != ("lon" in fields):
        errs.append(f"{where}: lat e lon vanno indicati insieme")
    return errs


def check() -> list[str]:
    errs = []
    try:
        corr = load()
    except yaml.YAMLError as e:
        return [f"correzioni.yaml non leggibile: {e}"]
    for uid, fields in corr["correggi"].items():
        if not isinstance(fields, dict):
            errs.append(f"correggi.{uid}: deve contenere i campi da cambiare")
            continue
        errs += validate_fields(fields, f"correggi.{uid}")
    catalog = ROOT / "ops" / "fonti.yaml"
    try:
        fonti = (yaml.safe_load(catalog.read_text(encoding="utf-8")) or {}).get("fonti") or [] if catalog.exists() else []
        for i, f in enumerate(fonti):
            for req in ("nome", "url", "tipo"):
                if not f.get(req):
                    errs.append(f"ops/fonti.yaml[{i}] {f.get('nome', '')!r}: manca '{req}'")
    except yaml.YAMLError as e:
        errs.append(f"ops/fonti.yaml non leggibile: {e}")
    cov = ROOT / "ops" / "copertura.yaml"
    try:
        data = (yaml.safe_load(cov.read_text(encoding="utf-8")) or {}) if cov.exists() else {}
        if cov.exists() and not any(k.startswith("comuni_") for k in data):
            errs.append("ops/copertura.yaml: mancano le sezioni comuni_<SIGLA> (es. comuni_TV)")
    except yaml.YAMLError as e:
        errs.append(f"ops/copertura.yaml non leggibile (controlla righe unite o rientri): {e}")
    for name in ("segnalazioni-e-controllo.md", "metodo-ricerca.md", "espansione.md", "categorie-ricerca.md"):
        if not (ROOT / "ops" / name).exists():
            errs.append(f"ops/{name} mancante: e' un file di memoria della revisione notturna")
    try:
        cur = yaml.safe_load(CURATED.read_text(encoding="utf-8")) if CURATED.exists() else {}
    except yaml.YAMLError as e:
        return errs + [f"eventi_redazione.yaml non leggibile: {e}"]
    for i, ev in enumerate((cur or {}).get("eventi") or []):
        where = f"eventi_redazione[{i}] {ev.get('title', '')!r}"
        for req in ("title", "start", "town", "official_url"):
            if not ev.get(req):
                errs.append(f"{where}: manca '{req}'")
        errs += validate_fields({k: v for k, v in ev.items() if k not in ("fonte", "trovato")}, where)
    return errs


# ---------------------------------------------------------------- applicazione
def _clean(fields: dict) -> dict:
    return {k: v for k, v in fields.items() if k in EDITABLE}


def apply_events(events: list[Event], geo=None, corr: Optional[dict] = None) -> list[Event]:
    """Sul PC: applica rimozioni e correzioni agli eventi deduplicati (copie), geolocalizzando se serve."""
    corr = corr or load()
    out = []
    for ev in events:
        uid = ev.uid
        if uid in corr["rimuovi"]:
            continue
        fields = corr["correggi"].get(uid)
        if fields:
            ev = copy.deepcopy(ev)
            fields = _clean(fields)
            for k, v in fields.items():
                setattr(ev, k, v)
            if "lat" in fields:
                ev.geo_precision = "address"
            elif PLACE_FIELDS & fields.keys() and geo is not None:
                old = (ev.lat, ev.lon, ev.geo_precision)
                ev.lat = ev.lon = None
                if not geo.locate(ev):
                    ev.lat, ev.lon, ev.geo_precision = old
            ev.uid_override = uid           # l'uid pubblicato resta quello originale anche se cambiano titolo o data
        out.append(ev)
    return out


def apply_payload(payload: dict, corr: Optional[dict] = None) -> dict:
    """Nel cloud: applica rimozioni e correzioni al JSON gia' pubblicato."""
    corr = corr or load()
    stats = {"rimossi": 0, "corretti": 0}
    events = []
    for d in payload["events"]:
        uid = d.get("uid")
        if uid in corr["rimuovi"]:
            stats["rimossi"] += 1
            continue
        fields = corr["correggi"].get(uid)
        if fields:
            fields = _clean(fields)
            if "category" in fields:
                fields["category"] = cats.canonical(fields["category"])
            d = {**d, **fields}
            if "lat" in fields:
                d["lat"], d["lon"] = round(float(fields["lat"]), 5), round(float(fields["lon"]), 5)
                d["geo_precision"] = "address"
            if "category" in fields and "subcategory" not in fields:
                d["subcategory"] = None
            d["action_url"] = d.get("official_url") or d.get("ticket_url") or d.get("source_url")
            stats["corretti"] += 1
        events.append(d)
    events.sort(key=lambda d: d.get("start") or "")
    payload = {**payload, "events": events, "count": len(events)}
    payload["redazione"] = stats
    return payload


def find(text: Optional[str], day: Optional[str], uid: Optional[str]) -> int:
    """Per la revisione: evita di leggere tutto events.json, cerca solo cio' che serve."""
    from rapidfuzz import fuzz
    payload = json.loads((ROOT / settings()["publish"]["export_path"]).read_text(encoding="utf-8"))
    if uid:
        hit = next((d for d in payload["events"] if d.get("uid") == uid), None)
        print(json.dumps(hit, ensure_ascii=False, indent=1) if hit else "uid non trovato")
        return 0
    scored = []
    curated = (yaml.safe_load(CURATED.read_text(encoding="utf-8")) or {}).get("eventi") if CURATED.exists() else []
    candidates = payload["events"] + [{**c, "uid": "redazione", "start": str(c.get("start") or ""),
                                       "end": str(c.get("end") or "")} for c in curated or []]
    for d in candidates:
        if day and not ((d.get("start") or "")[:10] <= day <= (d.get("end") or d.get("start") or "")[:10]):
            continue
        hay = " ".join(str(d.get(k) or "") for k in ("title", "venue", "town"))
        score = fuzz.token_set_ratio(text.lower(), hay.lower())
        if score >= 55:
            scored.append((score, d))
    for score, d in sorted(scored, key=lambda x: -x[0])[:8]:
        print(f"{score:3.0f}  {d['uid']}  {d.get('start')}  {d.get('title')}  |  {d.get('venue') or ''} {d.get('town') or ''}")
    if not scored:
        print("nessun evento simile sul sito")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Correzioni della redazione")
    ap.add_argument("--controlla", action="store_true", help="verifica i file della redazione")
    ap.add_argument("--applica", action="store_true", help="applica correzioni e rimozioni al sito pubblicato")
    ap.add_argument("--cerca", metavar="TESTO", help="cerca un evento gia' sul sito (titolo, luogo, comune)")
    ap.add_argument("--data", metavar="AAAA-MM-GG", help="con --cerca: solo eventi attivi in quel giorno")
    ap.add_argument("--uid", help="mostra tutti i dati di un evento pubblicato")
    args = ap.parse_args(argv)
    if args.cerca or args.uid:
        return find(args.cerca, args.data, args.uid)
    errs = check()
    for e in errs:
        print("ERRORE:", e)
    if errs:
        return 1
    if args.applica:
        path = ROOT / settings()["publish"]["export_path"]
        payload = json.loads(path.read_text(encoding="utf-8"))
        before = payload["count"]
        payload = apply_payload(payload)
        path.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        print(f"Sito: {before} -> {payload['count']} eventi; {payload['redazione']}")
    elif args.controlla:
        print("File della redazione validi.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
