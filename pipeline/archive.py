"""Archivio storico: tutti gli eventi mai pubblicati sul sito, anche quelli passati o tolti, nella versione finale
(con le correzioni della redazione). Il sito mostra solo gli eventi da oggi in avanti; l'archivio non perde nulla.

Dove sta:
  - nel database del PC (data/eventi.sqlite, tabella "archive"), aggiornato a ogni giro;
  - in copia nel repository, in archivio/AAAA-MM.jsonl (un file per mese di inizio dell'evento, un evento per riga),
    cosi' resta al sicuro anche se il PC si guasta e la revisione notturna di Claude lo puo' consultare.

Stato di ogni evento:
  pubblicato        e' sul sito adesso
  concluso          e' finito: era sul sito fino al giorno indicato in "ultima_pubblicazione"
  rimosso           tolto dalla redazione (annullato, doppione, non era un evento...), con il motivo
  non_piu_presente  sparito dalle fonti prima della fine (spesso annullato o spostato): da verificare

Uso:  python -m pipeline.archive --cerca "testo" [--anno 2026]   cerca nell'archivio (anche eventi passati)
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Optional

from .config import ROOT
from .textutil import parse_day, today_rome

ARCHIVE_DIR = ROOT / "archivio"

SCHEMA = """
CREATE TABLE IF NOT EXISTS archive (
    uid TEXT PRIMARY KEY,
    data TEXT NOT NULL,
    start_day TEXT,
    status TEXT NOT NULL,
    reason TEXT,
    first_published TEXT,
    last_published TEXT
);
CREATE INDEX IF NOT EXISTS archive_day ON archive(start_day);
"""


def _ensure(store) -> None:
    store.db.executescript(SCHEMA)


def _load_files(store, folder: Path) -> int:
    n = 0
    for path in sorted(folder.glob("*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            rec = json.loads(line)
            meta = {k: rec.pop(k, None) for k in ("stato", "motivo", "prima_pubblicazione", "ultima_pubblicazione")}
            store.db.execute(
                "INSERT OR IGNORE INTO archive(uid, data, start_day, status, reason, first_published, last_published) "
                "VALUES (?,?,?,?,?,?,?)",
                (rec["uid"], json.dumps(rec, ensure_ascii=False), (rec.get("start") or "")[:10], meta["stato"] or "concluso",
                 meta["motivo"], meta["prima_pubblicazione"], meta["ultima_pubblicazione"]))
            n += 1
    store.db.commit()
    return n


def seed_from_store(store, folder: Optional[Path] = None) -> int:
    """Prima volta: riprende l'archivio gia' presente nel repository (archivio/*.jsonl); poi aggiunge gli eventi
    passati che il PC aveva raccolto e che non ci sono (dati del raccoglitore, senza correzioni)."""
    _ensure(store)
    if store.db.execute("SELECT 1 FROM archive LIMIT 1").fetchone():
        return 0
    folder = folder or ARCHIVE_DIR
    if folder.exists():
        _load_files(store, folder)
    today = today_rome()
    n = 0
    for ev in store.events("published"):
        end = parse_day(ev.end) or parse_day(ev.start)
        if not end or end >= today or ev.kind != "evento" or ev.lat is None:
            continue
        d = ev.public_dict()
        store.db.execute(
            "INSERT OR IGNORE INTO archive(uid, data, start_day, status, reason, first_published, last_published) "
            "VALUES (?,?,?,?,?,?,?)",
            (ev.uid, json.dumps(d, ensure_ascii=False), (ev.start or "")[:10], "concluso",
             "dati del raccoglitore, senza correzioni (archiviato al primo avvio)", None, None))
        n += 1
    store.db.commit()
    return n


def update(store, published: list[dict], corrections: dict, today=None) -> dict:
    """Aggiorna l'archivio con gli eventi appena pubblicati e lo stato di quelli che non sono piu' sul sito."""
    _ensure(store)
    today = today or today_rome()
    day = today.isoformat()
    seen = set()
    stats = {"pubblicati": 0, "conclusi": 0, "rimossi": 0, "non_piu_presenti": 0}
    for d in published:
        uid = d.get("uid")
        if not uid:
            continue
        seen.add(uid)
        row = store.db.execute("SELECT first_published FROM archive WHERE uid=?", (uid,)).fetchone()
        first = (row["first_published"] if row and row["first_published"] else day)
        end = parse_day(d.get("end")) or parse_day(d.get("start"))
        status = "concluso" if end and end < today else "pubblicato"     # gia' finito: il sito lo nasconde
        store.db.execute(
            "INSERT OR REPLACE INTO archive(uid, data, start_day, status, reason, first_published, last_published) "
            "VALUES (?,?,?,?,?,?,?)",
            (uid, json.dumps(d, ensure_ascii=False), (d.get("start") or "")[:10], status, None, first, day))
        stats["pubblicati" if status == "pubblicato" else "conclusi"] += 1
    removed = corrections.get("rimuovi") or {}
    for row in store.db.execute("SELECT uid, data FROM archive WHERE status='pubblicato'").fetchall():
        uid = row["uid"]
        if uid in seen:
            continue
        d = json.loads(row["data"])
        end = parse_day(d.get("end")) or parse_day(d.get("start"))
        if uid in removed:
            status, reason, key = "rimosso", str(removed[uid]), "rimossi"
        elif end and end < today:
            status, reason, key = "concluso", None, "conclusi"
        else:
            status, reason, key = "non_piu_presente", "non piu' nelle fonti prima della fine: da verificare", "non_piu_presenti"
        store.db.execute("UPDATE archive SET status=?, reason=? WHERE uid=?", (status, reason, uid))
        stats[key] += 1
    store.db.commit()
    return stats


def write_files(store, folder: Optional[Path] = None) -> int:
    """Copia l'archivio in archivio/AAAA-MM.jsonl (scrive solo i file cambiati). Ritorna i file aggiornati."""
    _ensure(store)
    folder = folder or ARCHIVE_DIR
    folder.mkdir(parents=True, exist_ok=True)
    months: dict[str, list[str]] = defaultdict(list)
    for row in store.db.execute("SELECT * FROM archive ORDER BY start_day, uid"):
        rec = {"uid": row["uid"], "stato": row["status"], "motivo": row["reason"],
               "prima_pubblicazione": row["first_published"], "ultima_pubblicazione": row["last_published"],
               **json.loads(row["data"])}
        month = (row["start_day"] or "senza-data")[:7]
        months[month].append(json.dumps(rec, ensure_ascii=False, sort_keys=True))
    changed = 0
    for month, lines in months.items():
        path = folder / f"{month}.jsonl"
        text = "\n".join(lines) + "\n"
        if not path.exists() or path.read_text(encoding="utf-8") != text:
            path.write_text(text, encoding="utf-8")
            changed += 1
    return changed


def search(text: str, year: Optional[str] = None, folder: Optional[Path] = None) -> list[dict]:
    from rapidfuzz import fuzz
    folder = folder or ARCHIVE_DIR
    hits = []
    for path in sorted(folder.glob(f"{year or ''}*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            d = json.loads(line)
            hay = " ".join(str(d.get(k) or "") for k in ("title", "venue", "town"))
            score = fuzz.token_set_ratio(text.lower(), hay.lower())
            if score >= 60:
                hits.append((score, d))
    return [d for _, d in sorted(hits, key=lambda x: -x[0])[:15]]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Archivio storico degli eventi")
    ap.add_argument("--cerca", metavar="TESTO", required=True, help="titolo, luogo o comune")
    ap.add_argument("--anno", metavar="AAAA", help="solo eventi iniziati in quell'anno")
    args = ap.parse_args(argv)
    hits = search(args.cerca, args.anno)
    for d in hits:
        print(f"{d.get('start')}  {d.get('stato'):<16} {d.get('title')}  |  {d.get('venue') or ''} {d.get('town') or ''}"
              f"  |  {d.get('official_url') or d.get('action_url') or ''}")
    if not hits:
        print("nessun evento simile nell'archivio")
    return 0


if __name__ == "__main__":
    sys.exit(main())
