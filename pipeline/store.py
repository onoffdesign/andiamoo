"""Archivio locale SQLite: eventi, cache HTTP, cache geocoding, cache AI."""
from __future__ import annotations

import json
import sqlite3
import time
from pathlib import Path
from typing import Iterable, Optional

from .config import DATA_DIR
from .models import Event

SCHEMA = """
CREATE TABLE IF NOT EXISTS events (
    uid TEXT PRIMARY KEY,
    source TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'published',
    start_day TEXT,
    data TEXT NOT NULL,
    first_seen REAL NOT NULL,
    last_seen REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS events_day ON events(start_day);
CREATE TABLE IF NOT EXISTS http_cache (url TEXT PRIMARY KEY, body TEXT, fetched REAL);
CREATE TABLE IF NOT EXISTS geocode_cache (query TEXT PRIMARY KEY, result TEXT, fetched REAL);
CREATE TABLE IF NOT EXISTS ai_cache (key TEXT PRIMARY KEY, result TEXT, created REAL);
CREATE TABLE IF NOT EXISTS runs (id INTEGER PRIMARY KEY AUTOINCREMENT, started REAL, finished REAL, report TEXT);
CREATE TABLE IF NOT EXISTS reports (id INTEGER PRIMARY KEY AUTOINCREMENT, uid TEXT, kind TEXT, message TEXT,
                                    contact TEXT, created REAL, handled INTEGER DEFAULT 0);
"""


class Store:
    def __init__(self, path: Optional[Path] = None):
        path = path or DATA_DIR / "eventi.sqlite"
        path.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(path)
        self.db.row_factory = sqlite3.Row
        self.db.executescript(SCHEMA)

    # ---------- eventi ----------
    def upsert_event(self, ev: Event) -> bool:
        """Inserisce o aggiorna. Ritorna True se l'evento e' nuovo.

        Lo stato di moderazione (pending/rejected) gia' presente non viene sovrascritto da una nuova raccolta.
        """
        now = time.time()
        row = self.db.execute("SELECT status, first_seen FROM events WHERE uid=?", (ev.uid,)).fetchone()
        if row:
            # Le decisioni di moderazione restano: si cambiano solo con set_status (bot admin).
            if row["status"] in ("rejected", "pending"):
                ev.status = row["status"]
            self.db.execute(
                "UPDATE events SET data=?, status=?, start_day=?, last_seen=? WHERE uid=?",
                (json.dumps(ev.to_dict(), ensure_ascii=False), ev.status, (ev.start or "")[:10], now, ev.uid),
            )
            self.db.commit()
            return False
        self.db.execute(
            "INSERT INTO events(uid, source, status, start_day, data, first_seen, last_seen) VALUES (?,?,?,?,?,?,?)",
            (ev.uid, ev.source, ev.status, (ev.start or "")[:10], json.dumps(ev.to_dict(), ensure_ascii=False), now, now),
        )
        self.db.commit()
        return True

    def update_data(self, ev: Event) -> None:
        """Aggiorna solo i dati (es. coordinate), senza toccare stato e date di raccolta."""
        self.db.execute("UPDATE events SET data=? WHERE uid=?", (json.dumps(ev.to_dict(), ensure_ascii=False), ev.uid))
        self.db.commit()

    def get_event(self, uid: str) -> Optional[Event]:
        row = self.db.execute("SELECT data FROM events WHERE uid=?", (uid,)).fetchone()
        return Event.from_dict(json.loads(row["data"])) if row else None

    def set_status(self, uid: str, status: str) -> None:
        ev = self.get_event(uid)
        if not ev:
            return
        ev.status = status
        self.db.execute("UPDATE events SET status=?, data=? WHERE uid=?",
                        (status, json.dumps(ev.to_dict(), ensure_ascii=False), uid))
        self.db.commit()

    def events(self, status: Optional[str] = "published") -> Iterable[Event]:
        q, args = "SELECT data FROM events WHERE 1=1", []
        if status:
            q += " AND status=?"
            args.append(status)
        for row in self.db.execute(q, args):
            yield Event.from_dict(json.loads(row["data"]))

    def known_urls(self, source: str) -> set[str]:
        out = set()
        for row in self.db.execute("SELECT data FROM events WHERE source=?", (source,)):
            out.add(json.loads(row["data"]).get("source_url", ""))
        return out

    # ---------- cache generiche ----------
    def _cache_get(self, table: str, keycol: str, key: str, max_age: Optional[float]) -> Optional[str]:
        valcol, tcol = {"http_cache": ("body", "fetched"), "geocode_cache": ("result", "fetched"),
                        "ai_cache": ("result", "created")}[table]
        row = self.db.execute(f"SELECT {valcol} AS v, {tcol} AS t FROM {table} WHERE {keycol}=?", (key,)).fetchone()
        if not row:
            return None
        if max_age is not None and time.time() - row["t"] > max_age:
            return None
        return row["v"]

    def http_get(self, url: str, max_age: float) -> Optional[str]:
        return self._cache_get("http_cache", "url", url, max_age)

    def http_put(self, url: str, body: str) -> None:
        self.db.execute("INSERT OR REPLACE INTO http_cache(url, body, fetched) VALUES (?,?,?)", (url, body, time.time()))
        self.db.commit()

    def geo_get(self, query: str) -> Optional[dict]:
        v = self._cache_get("geocode_cache", "query", query, None)
        return json.loads(v) if v is not None else None

    def geo_put(self, query: str, result: dict | None) -> None:
        self.db.execute("INSERT OR REPLACE INTO geocode_cache(query, result, fetched) VALUES (?,?,?)",
                        (query, json.dumps(result), time.time()))
        self.db.commit()

    def ai_get(self, key: str) -> Optional[dict]:
        v = self._cache_get("ai_cache", "key", key, None)
        return json.loads(v) if v is not None else None

    def ai_put(self, key: str, result: dict) -> None:
        self.db.execute("INSERT OR REPLACE INTO ai_cache(key, result, created) VALUES (?,?,?)",
                        (key, json.dumps(result, ensure_ascii=False), time.time()))
        self.db.commit()

    def add_report(self, uid: str, kind: str, message: str, contact: str) -> None:
        self.db.execute("INSERT INTO reports(uid, kind, message, contact, created) VALUES (?,?,?,?,?)",
                        (uid, kind, message, contact, time.time()))
        self.db.commit()

    def first_seen_since(self, since: float) -> set[str]:
        return {r["uid"] for r in self.db.execute("SELECT uid FROM events WHERE first_seen>=?", (since,))}

    def reports_since(self, since: float) -> list[dict]:
        rows = self.db.execute("SELECT id, uid, kind, message, created, handled FROM reports WHERE created>=? ORDER BY created",
                               (since,))
        return [dict(r) for r in rows]

    def log_run(self, started: float, report: dict) -> None:
        self.db.execute("INSERT INTO runs(started, finished, report) VALUES (?,?,?)",
                        (started, time.time(), json.dumps(report, ensure_ascii=False)))
        self.db.commit()
