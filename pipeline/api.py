"""API per il sito, gira sul PC fisso accanto a Ollama ed e' esposta con Cloudflare Tunnel.

  GET  /api/salute     stato del servizio e dell'AI
  POST /api/estrai     {"url": "..."} oppure {"immagine": "data:image/...;base64,..."}
                       -> {"eventi": [campi...], "mancanti": {"required": [...], "recommended": [...]}}
  POST /api/invia      campi del modulo -> salva l'evento "in attesa" e avvisa l'amministratore su Telegram
  POST /api/segnala    {"uid", "tipo": "modifica"|"rimozione", "messaggio", "contatto"} -> avvisa l'amministratore

Avvio:  python -m pipeline.api        (ascolta su 127.0.0.1:8787, vedi config/settings.yaml)
"""
from __future__ import annotations

import base64
import binascii
import json
import logging
import threading
import time
from collections import defaultdict
from html import escape
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

from .config import env, settings
from .fetch import Fetcher
from .geocode import Geocoder
from .llm import OllamaLLM, RulesLLM
from .store import Store
from .submissions import ExtractError, extract_from_image, extract_from_url, missing, save_report, save_submission
from .telegram import Telegram, describe, moderation_buttons

log = logging.getLogger("api")

MAX_BODY = 8 * 1024 * 1024          # immagini fino a ~6 MB (base64)
LIMITS = {"estrai": (20, 3600), "invia": (10, 3600), "segnala": (10, 3600)}   # richieste per ora per IP
_hits: dict[tuple[str, str], list[float]] = defaultdict(list)
_ai_lock = threading.Lock()           # una sola elaborazione AI alla volta (una GPU)
_ai_status = {"ok": None, "checked": 0.0}


def ai_available() -> bool:
    if time.time() - _ai_status["checked"] > 60:
        _ai_status["ok"] = settings()["llm"]["backend"] == "ollama" and OllamaLLM(Store()).available()
        _ai_status["checked"] = time.time()
    return bool(_ai_status["ok"])


def make_context(backend: str | None = None):
    """Oggetti per singola richiesta (SQLite non si condivide tra thread)."""
    store = Store()
    use_ai = (backend or settings()["llm"]["backend"]) == "ollama" and ai_available()
    llm = OllamaLLM(store) if use_ai else RulesLLM(store)
    return store, Fetcher(store), Geocoder(store), llm


def allowed_origins() -> set[str]:
    cfg = settings()
    base = cfg["site"].get("base_url") or ""
    origins = {f"{urlparse(base).scheme}://{urlparse(base).netloc}"} if base else set()
    origins |= set(cfg.get("api", {}).get("allowed_origins", []))
    return origins


class Handler(BaseHTTPRequestHandler):
    server_version = "AndiamoAPI/1.0"
    context_factory = staticmethod(make_context)
    telegram_factory = staticmethod(Telegram)

    # ---------------------------------------------------------------- risposta
    def _cors(self):
        origin = self.headers.get("Origin", "")
        if origin in allowed_origins():
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Vary", "Origin")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.send_header("Access-Control-Max-Age", "600")

    def _send(self, status: int, payload: dict):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self._cors()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _error(self, status: int, code: str, message: str):
        self._send(status, {"ok": False, "errore": code, "messaggio": message})

    def log_message(self, fmt, *args):  # log sintetico, senza dati personali
        log.info("%s %s", self.command, self.path)

    def _ip(self) -> str:
        return self.headers.get("CF-Connecting-IP") or self.client_address[0]

    def _limited(self, action: str) -> bool:
        n, window = LIMITS[action]
        key = (self._ip(), action)
        now = time.time()
        _hits[key] = [t for t in _hits[key] if now - t < window]
        if len(_hits[key]) >= n:
            return True
        _hits[key].append(now)
        return False

    def _json(self) -> dict | None:
        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0 or length > MAX_BODY:
            self._error(413 if length > MAX_BODY else 400, "richiesta_non_valida", "Richiesta vuota o troppo grande.")
            return None
        try:
            data = json.loads(self.rfile.read(length).decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            self._error(400, "richiesta_non_valida", "Formato non valido.")
            return None
        if data.get("website"):                     # campo trappola per i bot di spam
            self._send(200, {"ok": True})
            return None
        return data

    # ---------------------------------------------------------------- metodi
    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        if self.path.split("?")[0] == "/api/salute":
            self._send(200, {"ok": True, "ai": ai_available()})
        else:
            self._error(404, "non_trovato", "Indirizzo sconosciuto.")

    def do_POST(self):
        route = self.path.split("?")[0]
        action = {"/api/estrai": "estrai", "/api/invia": "invia", "/api/segnala": "segnala"}.get(route)
        if not action:
            self._error(404, "non_trovato", "Indirizzo sconosciuto.")
            return
        if self._limited(action):
            self._error(429, "troppe_richieste", "Troppe richieste: riprova tra un po'.")
            return
        data = self._json()
        if data is None:
            return
        try:
            getattr(self, "_" + action)(data)
        except ExtractError as e:
            self._error(422, e.code, e.message)
        except Exception:  # noqa: BLE001
            log.exception("Errore su %s", route)
            self._error(500, "errore_interno", "Qualcosa non ha funzionato. Riprova o compila a mano.")

    # ---------------------------------------------------------------- azioni
    def _estrai(self, data: dict):
        store, fetcher, _, llm = self.context_factory()
        with _ai_lock:
            if data.get("immagine"):
                raw = str(data["immagine"])
                b64 = raw.split(",", 1)[1] if raw.startswith("data:") else raw
                try:
                    image = base64.b64decode(b64, validate=True)
                except (binascii.Error, ValueError):
                    raise ExtractError("immagine_non_valida", "Immagine non leggibile.") from None
                events = extract_from_image(image, llm)
            else:
                events = extract_from_url(str(data.get("url", "")).strip(), llm, fetcher)
        self._send(200, {"ok": True, "eventi": events, "mancanti": missing(events[0]), "ai": not isinstance(llm, RulesLLM)})

    def _invia(self, data: dict):
        store, fetcher, geo, llm = self.context_factory()
        with _ai_lock:
            ev = save_submission(data, store, geo, llm, contact=str(data.get("contatto", "")), fetcher=fetcher)
        tg = self.telegram_factory()
        if tg.enabled:
            tg.send(env("TELEGRAM_ADMIN_CHAT_ID"), "🆕 Evento aggiunto dal sito:\n\n" + describe(ev), moderation_buttons(ev.uid))
        self._send(200, {"ok": True, "id": ev.uid, "geolocalizzato": ev.lat is not None})

    def _segnala(self, data: dict):
        store, *_ = self.context_factory()
        ev = save_report(data, store)
        tg = self.telegram_factory()
        if tg.enabled:
            kind = "🗑️ Richiesta di RIMOZIONE" if data.get("tipo") == "rimozione" else "✏️ Richiesta di MODIFICA"
            text = (f"{kind}\n\n<b>{escape(ev.title)}</b> ({escape(ev.source_name)})\n"
                    f"<code>{ev.uid}</code>\n\n{escape(str(data.get('messaggio', ''))[:1500])}")
            if data.get("contatto"):
                text += f"\n\nContatto: {escape(str(data['contatto'])[:120])}"
            buttons = [[{"text": "❌ Togli dalla mappa", "callback_data": f"no:{ev.uid}"}]]
            tg.send(env("TELEGRAM_ADMIN_CHAT_ID"), text, buttons)
        self._send(200, {"ok": True})


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    logging.getLogger("httpx").setLevel(logging.WARNING)
    cfg = settings().get("api", {})
    host, port = cfg.get("host", "127.0.0.1"), int(cfg.get("port", 8787))
    log.info("API in ascolto su http://%s:%d (AI: %s, origini: %s)", host, port,
             "attiva" if ai_available() else "non disponibile", ", ".join(sorted(allowed_origins())) or "nessuna")
    ThreadingHTTPServer((host, port), Handler).serve_forever()


if __name__ == "__main__":
    main()
