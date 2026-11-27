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
  python -m pipeline.editorial --doppioni           probabili doppioni in eventi_redazione.yaml e tra redazione e sito
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


def duplicate_keys(text: str) -> list[str]:
    """uid ripetuti nella stessa sezione di correzioni.yaml: YAML tiene solo l'ultimo e la correzione nuova si perde
    in silenzio (2026-11-24: Il canto di Orsola corretto due volte, valeva la voce vecchia)."""
    errs, section, seen = [], None, {}
    for n, line in enumerate(text.splitlines(), 1):
        if line and not line.startswith((" ", "#")) and line.rstrip().endswith(":"):
            section, seen = line.rstrip()[:-1], {}
            continue
        m = re.match(r"^  ([^\s#:][^:]*):", line)
        if section and m:
            key = m.group(1).strip().strip("'\"")
            if key in seen:
                errs.append(f"{section}.{key}: ripetuto alle righe {seen[key]} e {n}, unisci le due voci (vale solo l'ultima)")
            else:
                seen[key] = n
    return errs


def check() -> list[str]:
    errs = []
    try:
        corr = load()
    except yaml.YAMLError as e:
        return [f"correzioni.yaml non leggibile: {e}"]
    errs += duplicate_keys(CORRECTIONS.read_text(encoding="utf-8")) if CORRECTIONS.exists() else []
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
    from rapidfuzz import fuzz, utils
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
        # default_process toglie punteggiatura e maiuscole ("Casaro." = "casaro"); a parita' di punteggio
        # vince il titolo piu' simile al testo intero, cosi' una parola comune (Treviso) non copre i risultati giusti
        score = fuzz.token_set_ratio(text, hay, processor=utils.default_process)
        if score >= 55:
            tie = fuzz.partial_ratio(text, str(d.get("title") or ""), processor=utils.default_process)
            scored.append((score, tie, d))
    scored.sort(key=lambda x: (-x[0], -x[1]))
    if len(scored) > 8:
        print(f"({len(scored)} risultati, mostrati i primi 8: aggiungi parole o --data per restringere)")
    scored = [(s_, d) for s_, _t, d in scored]
    for score, d in scored[:8]:
        print(f"{score:3.0f}  {d['uid']}  {d.get('start')}  {d.get('title')}  |  {d.get('venue') or ''} {d.get('town') or ''}")
    if not scored:
        print("nessun evento simile sul sito")
    return 0


def town_overview(town: str, since: Optional[str] = None, show: int = 40) -> list:
    """Eventi futuri di un comune (sito + redazione, senza doppioni) e domini dei link: si guarda prima di spendere
    una ricerca su un comune, per sapere cosa e' gia' coperto e da quali fonti."""
    from datetime import date
    since = since or date.today().isoformat()
    path = ROOT / settings()["publish"]["export_path"]
    site = json.loads(path.read_text(encoding="utf-8")).get("events", []) if path.exists() else []
    curated = (yaml.safe_load(CURATED.read_text(encoding="utf-8")) or {}).get("eventi") if CURATED.exists() else []
    want = " ".join(sorted(_norm_words(town)))
    seen, rows = set(), []
    for d in site + [{**c, "uid": "redazione"} for c in curated or []]:
        if " ".join(sorted(_norm_words(d.get("town")))) != want:
            continue
        start, end = str(d.get("start") or ""), str(d.get("end") or d.get("start") or "")
        if end[:10] < since:
            continue
        key = (start[:10], " ".join(sorted(_norm_words(d.get("title")))))
        if key in seen:
            continue
        seen.add(key)
        url = d.get("official_url") or d.get("action_url") or d.get("source_url") or ""
        dom = re.sub(r"^https?://(www\.)?", "", str(url)).split("/")[0]
        rows.append((start, str(d.get("title") or ""), d.get("uid"), dom))
    rows.sort()
    return rows


def print_town(town: str, since: Optional[str]) -> int:
    rows = town_overview(town, since)
    doms: dict = {}
    for r in rows:
        doms[r[3]] = doms.get(r[3], 0) + 1
    print(f"{town}: {len(rows)} eventi futuri (sito + redazione)")
    for start, title, uid, dom in rows[:40]:
        print(f"  {start[:16]}  {title}  [{uid}, {dom}]")
    if len(rows) > 40:
        print(f"  ... altri {len(rows) - 40}")
    print("fonti:", ", ".join(f"{k or '-'} {v}" for k, v in sorted(doms.items(), key=lambda x: -x[1])) or "nessuna")
    return 0


def _norm_words(s) -> set:
    return set(re.sub(r"[^a-z0-9 ]", " ", str(s or "").lower()).split())


def duplicates(events: list) -> list:
    """Coppie di eventi della redazione con stesso giorno, ora e comune e titolo quasi uguale (doppioni)."""
    groups: dict = {}
    for i, e in enumerate(events):
        start = str(e.get("start") or "")
        key = (start[:10], start[11:16], " ".join(sorted(_norm_words(e.get("town")))))
        groups.setdefault(key, []).append(i)
    pairs = []
    for idx in groups.values():
        for a in range(len(idx)):
            for b in range(a + 1, len(idx)):
                ta, tb = (_norm_words(events[idx[a]].get("title")), _norm_words(events[idx[b]].get("title")))
                if ta and tb and len(ta & tb) / min(len(ta), len(tb)) >= 0.6:
                    pairs.append((idx[a], idx[b]))
    return pairs


def site_duplicates(curated: list, site: list) -> list:
    """Eventi della redazione che sono gia' sul sito da un'altra fonte (stesso giorno e comune, titolo simile, ore
    uguali o mancanti): (indice nella redazione, uid sul sito). Succede quando --cerca non li trova per un titolo
    scritto diverso (LiTLe Run / LitTLe RuN) o quando il PC li ha raccolti dopo che la redazione li aveva aggiunti."""
    from rapidfuzz import fuzz, utils
    by_key: dict = {}
    for d in site:
        if d.get("source") == "redazione":  # gli eventi della redazione pubblicati dal PC sono gli stessi
            continue
        start = str(d.get("start") or "")
        by_key.setdefault((start[:10], " ".join(sorted(_norm_words(d.get("town"))))), []).append(d)
    out = []
    for i, c in enumerate(curated):
        start = str(c.get("start") or "")
        for d in by_key.get((start[:10], " ".join(sorted(_norm_words(c.get("town"))))), []):
            h1, h2 = start[11:16], str(d.get("start") or "")[11:16]
            if h1 and h2 and h1 != h2:
                continue
            ta, tb = str(c.get("title") or ""), str(d.get("title") or "")
            score = fuzz.token_set_ratio(ta, tb, processor=utils.default_process)
            if min(len(ta), len(tb)) >= 8:  # titolo corto dentro uno lungo, scritto diverso (LitTLe RuN)
                score = max(score, fuzz.partial_ratio(ta, tb, processor=utils.default_process))
            if score >= 85:
                out.append((i, d.get("uid")))
                break
    return out


def find_duplicates() -> int:
    """Stampa i probabili doppioni in eventi_redazione.yaml (stesso giorno e comune, titolo simile).
    L'ora vuota conta come 'qualsiasi ora': confronta anche eventi senza ora con eventi con ora."""
    data = yaml.safe_load(CURATED.read_text(encoding="utf-8")) or {}
    events = data.get("eventi") or []
    loose = [dict(e, start=str(e.get("start") or "")[:10]) for e in events]
    hour = [str(e.get("start") or "")[11:16] for e in events]
    pairs = sorted(p for p in set(duplicates(loose)) if not (hour[p[0]] and hour[p[1]] and hour[p[0]] != hour[p[1]]))
    for a, b in pairs:
        ea, eb = events[a], events[b]
        print(f"{str(ea.get('start'))[:16]}  {ea.get('title')}  ||  {str(eb.get('start'))[:16]}  {eb.get('title')}"
              f"  ({ea.get('town')})")
    print(f"{len(pairs)} possibili doppioni (stesso giorno e comune; repliche a ore diverse sono legittime)")
    path = ROOT / settings()["publish"]["export_path"]
    site = json.loads(path.read_text(encoding="utf-8")).get("events", []) if path.exists() else []
    today = date.today().isoformat()
    same = [(i, uid) for i, uid in site_duplicates(events, site) if str(events[i].get("start") or "")[:10] >= today]
    for i, uid in same:
        e = events[i]
        print(f"gia' sul sito: {str(e.get('start'))[:16]}  {e.get('title')}  ({e.get('town')})  = {uid}")
    print(f"{len(same)} eventi futuri della redazione gia' sul sito da un'altra fonte (da togliere dalla redazione"
          f" se l'evento del sito e' completo)")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Correzioni della redazione")
    ap.add_argument("--doppioni", action="store_true",
                    help="elenca i probabili doppioni in eventi_redazione.yaml (stesso giorno e comune)")
    ap.add_argument("--controlla", action="store_true", help="verifica i file della redazione")
    ap.add_argument("--applica", action="store_true", help="applica correzioni e rimozioni al sito pubblicato")
    ap.add_argument("--cerca", metavar="TESTO", help="cerca un evento gia' sul sito (titolo, luogo, comune)")
    ap.add_argument("--data", metavar="AAAA-MM-GG", help="con --cerca: solo eventi attivi in quel giorno")
    ap.add_argument("--uid", help="mostra tutti i dati di un evento pubblicato")
    ap.add_argument("--comune", metavar="NOME",
                    help="eventi futuri di un comune (sito + redazione) e loro fonti: da guardare prima di cercarlo")
    args = ap.parse_args(argv)
    if args.doppioni:
        return find_duplicates()
    if args.comune:
        return print_town(args.comune, args.data)
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
