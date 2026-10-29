"""Bot Telegram per le segnalazioni. Gira sul PC fisso insieme a Ollama.

Chiunque puo' mandare:
  - la foto o lo screenshot di una locandina (anche di un post Instagram/Facebook)
  - il link di una pagina evento
  - un messaggio di testo che descrive un evento
L'AI estrae i dati, l'evento resta "in attesa" e l'amministratore lo approva con un tocco.

Comandi amministratore: /attesa  /profili  /stato  /luogo <id> <indirizzo, comune>

Avvio:  python -m bot.telegram_bot
"""
from __future__ import annotations

import json
import logging
import re
import time
from collections import defaultdict
from html import escape

from pipeline.collectors.jsonld import iter_jsonld, main_text, to_event
from pipeline.config import env, watchlist
from pipeline.enrich import enrich
from pipeline.fetch import Blocked, Fetcher
from pipeline.geocode import Geocoder
from pipeline.llm import make_llm
from pipeline.models import Event
from pipeline.places import PlaceFinder
from pipeline.store import Store
from pipeline.telegram import Telegram, describe, moderation_buttons

log = logging.getLogger("bot")

URL_RE = re.compile(r"https?://\S+")
SOCIAL_RE = re.compile(r"instagram\.com|facebook\.com|fb\.watch|fb\.me|tiktok\.com", re.I)
DAILY_LIMIT = 15

HELP = ("Ciao! Segnalami un evento in provincia di Treviso:\n"
        "📸 manda la <b>foto o lo screenshot della locandina</b> (va benissimo anche da Instagram o Facebook)\n"
        "🔗 oppure il <b>link</b> della pagina dell'evento\n"
        "✍️ oppure scrivimi cosa, quando e dove.\n\n"
        "Lo controllo e, se va bene, finisce sulla mappa.")


class Bot:
    def __init__(self):
        self.tg = Telegram()
        if not self.tg.enabled:
            raise SystemExit("Manca TELEGRAM_TOKEN nel file .env")
        self.admin = str(env("TELEGRAM_ADMIN_CHAT_ID"))
        self.store = Store()
        self.llm = make_llm(self.store)
        self.fetcher = Fetcher(self.store)
        self.geo = Geocoder(self.store)
        self.sent_today: dict[str, list[float]] = defaultdict(list)

    # ---------------------------------------------------------------- utilità
    def is_admin(self, chat_id) -> bool:
        return self.admin and str(chat_id) == self.admin

    def over_limit(self, chat_id) -> bool:
        now = time.time()
        times = [t for t in self.sent_today[str(chat_id)] if now - t < 86400]
        self.sent_today[str(chat_id)] = times
        return len(times) >= DAILY_LIMIT and not self.is_admin(chat_id)

    def save_pending(self, found: list[dict], chat_id, origin_url: str, origin: str) -> list[Event]:
        saved = []
        for i, f in enumerate(found):
            if not f.get("title") or not f.get("start"):
                continue
            ev = Event(
                source="segnalazioni", source_name="Segnalazione", source_url=origin_url or f"telegram:{chat_id}:{time.time():.0f}:{i}",
                title=f["title"], start=f["start"], end=f.get("end") or None, all_day=len(f["start"]) == 10,
                summary=f.get("summary", ""), ai_summary=bool(f.get("summary")),
                category=f.get("category"), subcategory=f.get("subcategory"),
                access=f.get("access") or "sconosciuto", price=f.get("price", ""),
                venue=f.get("venue", ""), address=f.get("address", ""), town=f.get("town", ""),
                ticket_url=f.get("ticket_url", ""), official_url=f.get("official_url") or (origin_url if origin == "link" else ""),
                status="pending", submitted_by=str(chat_id), needs_ai=False,
            )
            enrich(ev, self.llm)
            self.geo.locate(ev, PlaceFinder(self.fetcher, self.llm, self.store, max_pages=3))
            self.store.upsert_event(ev)
            saved.append(ev)
            self.tg.send(self.admin, f"🆕 Segnalazione ({origin}) da {chat_id}:\n\n" + describe(ev),
                         moderation_buttons(ev.uid))
        return saved

    # ---------------------------------------------------------------- gestori
    def on_photo(self, msg: dict):
        chat = msg["chat"]["id"]
        photo = max(msg["photo"], key=lambda p: p.get("file_size", 0))
        self.tg.send(chat, "📸 Ricevuta, la sto leggendo…")
        image = self.tg.download_file(photo["file_id"])
        found = self.llm.extract_from_image(image, caption=msg.get("caption", ""))
        self.reply_result(chat, self.save_pending(found, chat, "", "locandina"))

    def on_link(self, chat, url: str, text: str):
        if SOCIAL_RE.search(url):
            self.tg.send(chat, "I post di Instagram e Facebook non posso aprirli da qui. "
                               "Mandami lo <b>screenshot della locandina</b> e ci penso io 👍")
            return
        try:
            html = self.fetcher.get(url, use_cache=False)
        except Blocked:
            self.tg.send(chat, "Questo sito non consente la lettura automatica. Mandami uno screenshot.")
            return
        except Exception:  # noqa: BLE001
            self.tg.send(chat, "Non riesco ad aprire il link. Controlla l'indirizzo o mandami uno screenshot.")
            return
        found = []
        for obj in iter_jsonld(html):
            ev = to_event(obj, {"id": "segnalazioni", "name": "Segnalazione"})
            if ev:
                found.append({"title": ev.title, "start": ev.start, "end": ev.end or "", "venue": ev.venue,
                              "address": ev.address, "town": ev.town, "price": ev.price, "access": ev.access})
        if not found:
            found = self.llm.extract_events(main_text(html) + "\n" + text, hint=f"Pagina: {url}")
        self.reply_result(chat, self.save_pending(found, chat, url, "link"))

    def on_text(self, chat, text: str):
        found = self.llm.extract_events(text, hint="Messaggio inviato da un utente al bot.")
        self.reply_result(chat, self.save_pending(found, chat, "", "testo"))

    def reply_result(self, chat, saved: list[Event]):
        if not saved:
            self.tg.send(chat, "Non ho trovato un evento con titolo e data. Puoi aggiungere quando e dove?")
            return
        names = "\n".join(f"• {escape(e.title)} ({(e.start or '')[:10]})" for e in saved)
        self.tg.send(chat, f"Grazie! In revisione:\n{names}")

    def on_command(self, chat, text: str):
        cmd, *rest = text.split(maxsplit=2)
        cmd = cmd.split("@")[0].lower()
        if cmd in ("/start", "/aiuto", "/help"):
            self.tg.send(chat, HELP)
            if self.is_admin(chat):
                self.tg.send(chat, "Comandi admin: /attesa /profili /stato /luogo &lt;id&gt; &lt;indirizzo, comune&gt;")
            return
        if not self.is_admin(chat):
            self.tg.send(chat, HELP)
            return
        if cmd == "/profili":
            lines = [f"• <a href=\"{escape(w['url'])}\">{escape(w['name'])}</a>" for w in watchlist()]
            self.tg.send(chat, "Profili da controllare (inoltrami gli screenshot dei nuovi eventi):\n" + "\n".join(lines))
        elif cmd == "/attesa":
            pending = list(self.store.events("pending"))
            if not pending:
                self.tg.send(chat, "Nessuna segnalazione in attesa.")
            for ev in pending[:10]:
                self.tg.send(chat, describe(ev) + f"\n<code>{ev.uid}</code>", moderation_buttons(ev.uid))
        elif cmd == "/stato":
            row = self.store.db.execute("SELECT started, report FROM runs ORDER BY id DESC LIMIT 1").fetchone()
            if not row:
                self.tg.send(chat, "Nessun giro della pipeline registrato.")
                return
            rep = json.loads(row["report"])
            when = time.strftime("%d/%m %H:%M", time.localtime(row["started"]))
            lines = [f"Ultimo giro: {when} · sul sito: {rep.get('eventi_sul_sito')}"]
            for sid, s in rep.get("fonti", {}).items():
                flag = "⚠️ " + s["errore"][:60] if s.get("errore") else f"{s.get('in_provincia', 0)} in provincia"
                lines.append(f"• {sid}: {s.get('trovati', 0)} trovati, {flag}")
            self.tg.send(chat, escape("\n".join(lines)))
        elif cmd == "/luogo" and len(rest) == 2:
            ev = self.store.get_event(rest[0])
            if not ev:
                self.tg.send(chat, "Id non trovato.")
                return
            parts = [p.strip() for p in rest[1].rsplit(",", 1)]
            ev.address, ev.town = (parts[0], parts[1]) if len(parts) == 2 else ("", parts[0])
            ev.lat = ev.lon = None
            ok = self.geo.locate(ev)
            self.store.upsert_event(ev)
            self.tg.send(chat, ("📍 Posizione aggiornata.\n" if ok else "⚠️ Indirizzo non trovato in provincia.\n")
                         + describe(ev), moderation_buttons(ev.uid))

    def on_callback(self, cb: dict):
        chat = cb["message"]["chat"]["id"]
        if not self.is_admin(chat):
            return
        action, uid = cb["data"].split(":", 1)
        ev = self.store.get_event(uid)
        if not ev:
            self.tg.call("answerCallbackQuery", callback_query_id=cb["id"], text="Evento non trovato")
            return
        if action == "ok" and ev.lat is None:
            self.tg.call("answerCallbackQuery", callback_query_id=cb["id"],
                         text="Manca la posizione: usa /luogo prima di pubblicare", show_alert=True)
            return
        self.store.set_status(uid, "published" if action == "ok" else "rejected")
        self.tg.call("answerCallbackQuery", callback_query_id=cb["id"],
                     text="Pubblicato" if action == "ok" else "Scartato")
        self.tg.call("editMessageReplyMarkup", chat_id=chat, message_id=cb["message"]["message_id"],
                     reply_markup={"inline_keyboard": []})
        from pipeline.run import main as run_main
        run_main(["--export-only"])              # aggiorna subito il sito (pubblicazione o rimozione)
        if action == "ok":
            if ev.submitted_by and ev.submitted_by.isdigit() and ev.submitted_by != self.admin:
                self.tg.send(ev.submitted_by, f"✅ «{escape(ev.title)}» e' sulla mappa. Grazie!")

    # ---------------------------------------------------------------- ciclo
    def handle(self, upd: dict):
        if "callback_query" in upd:
            self.on_callback(upd["callback_query"])
            return
        msg = upd.get("message") or {}
        chat = (msg.get("chat") or {}).get("id")
        if not chat:
            return
        text = msg.get("text") or msg.get("caption") or ""
        if text.startswith("/"):
            self.on_command(chat, text)
            return
        if self.over_limit(chat):
            self.tg.send(chat, "Hai raggiunto il limite di segnalazioni per oggi. Grazie!")
            return
        self.sent_today[str(chat)].append(time.time())
        if msg.get("photo"):
            self.on_photo(msg)
        elif (m := URL_RE.search(text)):
            self.on_link(chat, m.group(0), text)
        elif len(text) > 25:
            self.on_text(chat, text)
        else:
            self.tg.send(chat, HELP)

    def loop(self):
        log.info("Bot avviato (AI: %s)", self.llm.name)
        offset = None
        while True:
            try:
                updates = self.tg.call("getUpdates", timeout=50, offset=offset,
                                       allowed_updates=["message", "callback_query"]) or []
            except Exception as e:  # noqa: BLE001 - rete instabile: riprova
                log.warning("getUpdates: %s", e)
                time.sleep(5)
                continue
            for upd in updates:
                offset = upd["update_id"] + 1
                try:
                    self.handle(upd)
                except Exception:  # noqa: BLE001
                    log.exception("Errore gestendo un messaggio")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    logging.getLogger("httpx").setLevel(logging.WARNING)
    Bot().loop()
