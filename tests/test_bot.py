"""Flusso del bot con Telegram e AI finti: segnalazione -> attesa -> approvazione."""
from bot.telegram_bot import Bot
from pipeline.geocode import Geocoder
from pipeline.store import Store


class FakeTG:
    enabled = True

    def __init__(self):
        self.sent = []
        self.calls = []

    def send(self, chat, text, buttons=None):
        self.sent.append((str(chat), text, buttons))

    def call(self, method, **kw):
        self.calls.append((method, kw))

    def download_file(self, file_id):
        return b"fake-image"


class FakeLLM:
    name = "fake"
    calls = 0

    def extract_from_image(self, image, caption=""):
        return [{"title": "Concerto di prova", "start": "2026-12-12T21:00", "venue": "Home", "address": "Via Fonderia 73",
                 "town": "Treviso", "province": "TV", "category": "musica", "subcategory": "concerti",
                 "access": "biglietto", "summary": "Concerto dal vivo di musica jazz."}]

    def extract_events(self, text, hint=""):
        return []

    def enrich(self, known, text):
        return {}


def make_bot(tmp_path, monkeypatch):
    b = Bot.__new__(Bot)
    b.tg = FakeTG()
    b.admin = "999"
    b.store = Store(tmp_path / "b.sqlite")
    b.store.geo_put("s|home, via fonderia 73, treviso",
                    {"lat": 45.6859, "lon": 12.2494, "province": "IT-TV", "town": "Treviso", "type": "house"})
    b.llm = FakeLLM()
    b.fetcher = None
    b.geo = Geocoder(b.store, offline=True)
    from collections import defaultdict
    b.sent_today = defaultdict(list)
    monkeypatch.setattr("pipeline.run.main", lambda argv=None: 0)
    return b


def test_photo_submission_and_approval(tmp_path, monkeypatch):
    b = make_bot(tmp_path, monkeypatch)
    b.handle({"update_id": 1, "message": {"chat": {"id": 42}, "photo": [{"file_id": "x", "file_size": 10}]}})
    pending = list(b.store.events("pending"))
    assert len(pending) == 1 and pending[0].lat is not None and pending[0].ai_summary
    admin_msgs = [m for m in b.tg.sent if m[0] == "999"]
    assert admin_msgs and admin_msgs[0][2][0][0]["callback_data"].startswith("ok:")
    uid = pending[0].uid
    # un utente qualunque non puo' approvare
    b.handle({"update_id": 2, "callback_query": {"id": "c", "data": f"ok:{uid}", "message": {"chat": {"id": 42}, "message_id": 5}}})
    assert b.store.get_event(uid).status == "pending"
    b.handle({"update_id": 3, "callback_query": {"id": "c", "data": f"ok:{uid}", "message": {"chat": {"id": 999}, "message_id": 5}}})
    assert b.store.get_event(uid).status == "published"
    assert any("sulla mappa" in m[1] for m in b.tg.sent if m[0] == "42")


def test_instagram_link_asks_for_screenshot(tmp_path, monkeypatch):
    b = make_bot(tmp_path, monkeypatch)
    b.handle({"update_id": 1, "message": {"chat": {"id": 7}, "text": "guarda https://www.instagram.com/p/abc/"}})
    assert "screenshot" in b.tg.sent[-1][1]
