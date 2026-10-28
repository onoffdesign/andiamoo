"""Chiamate minime alla Bot API di Telegram (senza librerie esterne)."""
from __future__ import annotations

import json
import logging
from typing import Optional

import httpx

from .config import env

log = logging.getLogger(__name__)
API = "https://api.telegram.org"


class Telegram:
    def __init__(self, token: Optional[str] = None):
        self.token = token or env("TELEGRAM_TOKEN")
        self.client = httpx.Client(timeout=70)

    @property
    def enabled(self) -> bool:
        return bool(self.token)

    def call(self, method: str, **params):
        if not self.enabled:
            return None
        files = params.pop("_files", None)
        data = {k: (json.dumps(v) if isinstance(v, (dict, list)) else v) for k, v in params.items() if v is not None}
        r = self.client.post(f"{API}/bot{self.token}/{method}", data=data, files=files)
        body = r.json()
        if not body.get("ok"):
            log.warning("Telegram %s: %s", method, body.get("description"))
        return body.get("result")

    def send(self, chat_id, text: str, buttons: Optional[list[list[dict]]] = None):
        markup = {"inline_keyboard": buttons} if buttons else None
        return self.call("sendMessage", chat_id=chat_id, text=text, parse_mode="HTML",
                         disable_web_page_preview=True, reply_markup=markup)

    def download_file(self, file_id: str) -> bytes:
        info = self.call("getFile", file_id=file_id)
        r = self.client.get(f"{API}/file/bot{self.token}/{info['file_path']}")
        r.raise_for_status()
        return r.content


def moderation_buttons(uid: str) -> list[list[dict]]:
    return [[{"text": "✅ Pubblica", "callback_data": f"ok:{uid}"},
             {"text": "❌ Scarta", "callback_data": f"no:{uid}"}]]


def describe(ev) -> str:
    from html import escape
    when = (ev.start or "?").replace("T", " ore ")
    where = ", ".join(x for x in (ev.venue, ev.address, ev.town) if x) or "luogo da verificare"
    lines = [f"<b>{escape(ev.title)}</b>", f"📅 {escape(when)}", f"📍 {escape(where)}",
             f"🏷️ {escape(ev.category or '?')}/{escape(ev.subcategory or '-')} · accesso: {escape(ev.access)}"]
    if ev.summary:
        lines.append(escape(ev.summary))
    if ev.lat is None:
        lines.append("⚠️ non geolocalizzato")
    return "\n".join(lines)
