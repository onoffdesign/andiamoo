"""API del sito con AI e Telegram finti, server reale su porta locale."""
import base64
import threading
from http.server import ThreadingHTTPServer

import httpx
import pytest

from pipeline import api
from pipeline.fetch import Fetcher
from pipeline.geocode import Geocoder
from pipeline.models import Event
from pipeline.store import Store
from pipeline.submissions import missing, to_fields


class FakeLLM:
    name = "fake"
    calls = 0

    def extract_from_image(self, image, caption=""):
        return [{"title": "Concerto in villa", "start": "2026-12-12T21:00", "venue": "", "town": "Treviso",
                 "category": "musica", "access": "biglietto", "summary": "Concerto di musica da camera."}]

    def extract_events(self, text, hint=""):
        return []

    def enrich(self, known, text):
        return {"summary": "L'evento prevede musica dal vivo.", "category": "musica", "access": "biglietto"}


class FakeTG:
    enabled = True
    sent = []

    def send(self, chat, text, buttons=None):
        FakeTG.sent.append((text, buttons))


@pytest.fixture()
def server(tmp_path, monkeypatch):
    db = tmp_path / "api.sqlite"
    seed = Store(db)
    seed.geo_put("s|treviso, veneto", {"lat": 45.666, "lon": 12.243, "province": "IT-TV", "town": "Treviso", "type": "city"})
    seed.upsert_event(Event("x", "Fonte X", "https://x/1", "Mercatino di Natale", start="2026-12-06", town="Treviso",
                            lat=45.66, lon=12.24))

    def ctx(backend=None):
        st = Store(db)
        return st, Fetcher(st), Geocoder(st, offline=True), FakeLLM()

    monkeypatch.setattr(api.Handler, "context_factory", staticmethod(ctx))
    monkeypatch.setattr(api.Handler, "telegram_factory", staticmethod(FakeTG))
    monkeypatch.setattr(api, "ai_available", lambda: True)
    api._hits.clear()
    FakeTG.sent = []
    srv = ThreadingHTTPServer(("127.0.0.1", 0), api.Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{srv.server_address[1]}", db
    srv.shutdown()


def test_fields_and_missing():
    f = to_fields({"title": "Sagra", "start": "2026-11-08T12:00", "town": "", "category": "sagre-feste"}, "https://proloco.it/sagra")
    assert f["date"] == "2026-11-08" and f["time"] == "12:00" and f["official_url"] == "https://proloco.it/sagra"
    m = missing(f)
    assert m["required"] == ["town"] and "venue" in m["recommended"]


def test_health_and_cors(server):
    url, _ = server
    r = httpx.get(url + "/api/salute", headers={"Origin": "https://onoffdesign.github.io"})
    assert r.json() == {"ok": True, "ai": True}
    assert r.headers["access-control-allow-origin"] == "https://onoffdesign.github.io"
    r2 = httpx.get(url + "/api/salute", headers={"Origin": "https://sito-estraneo.example"})
    assert "access-control-allow-origin" not in r2.headers


def test_extract_image_reports_missing_venue(server):
    url, _ = server
    img = "data:image/png;base64," + base64.b64encode(b"\x89PNG fake").decode()
    r = httpx.post(url + "/api/estrai", json={"immagine": img}).json()
    assert r["ok"] and r["eventi"][0]["title"] == "Concerto in villa" and r["eventi"][0]["time"] == "21:00"
    assert r["mancanti"]["required"] == [] and "venue" in r["mancanti"]["recommended"]


def test_extract_social_link_asks_screenshot(server):
    url, _ = server
    r = httpx.post(url + "/api/estrai", json={"url": "https://www.instagram.com/p/abc/"})
    assert r.status_code == 422 and r.json()["errore"] == "social"


def test_submit_saves_pending_and_notifies(server):
    url, db = server
    r = httpx.post(url + "/api/invia", json={"title": "Concerto in villa", "date": "2026-12-12", "time": "21:00",
                                             "town": "Treviso", "summary": "Una serata imperdibile!!!"}).json()
    assert r["ok"] and r["geolocalizzato"]
    ev = Store(db).get_event(r["id"])
    assert ev.status == "pending" and ev.start == "2026-12-12T21:00"
    assert ev.summary == "L'evento prevede musica dal vivo."          # riscritto, neutro
    assert FakeTG.sent and FakeTG.sent[0][1][0][0]["callback_data"] == f"ok:{r['id']}"


def test_submit_missing_required(server):
    url, _ = server
    r = httpx.post(url + "/api/invia", json={"title": "Senza data", "town": "Treviso"})
    assert r.status_code == 422 and "date" in r.json()["messaggio"]


def test_honeypot_ignored(server):
    url, db = server
    r = httpx.post(url + "/api/invia", json={"title": "Spam", "date": "2026-12-12", "town": "Treviso", "website": "x"})
    assert r.json() == {"ok": True}
    assert not list(Store(db).events("pending"))


def test_report_removal(server):
    url, db = server
    uid = next(Store(db).events("published")).uid
    r = httpx.post(url + "/api/segnala", json={"uid": uid, "tipo": "rimozione", "messaggio": "Annullato"})
    assert r.json()["ok"]
    text, buttons = FakeTG.sent[-1]
    assert "RIMOZIONE" in text and buttons[0][0]["callback_data"] == f"no:{uid}"
    assert Store(db).db.execute("SELECT kind FROM reports").fetchone()[0] == "rimozione"


def test_rate_limit(server):
    url, _ = server
    codes = [httpx.post(url + "/api/segnala", json={"uid": "nope"}).status_code for _ in range(11)]
    assert codes[-1] == 429


def test_tunnel_publishes_quick_url(tmp_path, monkeypatch):
    import sys
    from pipeline import export, tunnel
    fake = tmp_path / "cloudflared.py"
    fake.write_text("print('INF Requesting new quick Tunnel on trycloudflare.com...')\n"
                    "print('INF |  https://lucky-owl-ace.trycloudflare.com  |')\n")
    monkeypatch.setattr(tunnel, "find_cloudflared", lambda: sys.executable)
    real_popen = tunnel.subprocess.Popen
    monkeypatch.setattr(tunnel.subprocess, "Popen", lambda args, **kw: real_popen([sys.executable, str(fake)], **kw))
    monkeypatch.setattr(tunnel, "DATA_DIR", tmp_path)
    monkeypatch.setattr(export, "DATA_DIR", tmp_path)
    got = []
    monkeypatch.setattr(tunnel, "publish_url", lambda url: (got.append(url), (tmp_path / "api_url.txt").write_text(url)))
    assert tunnel.main() == 1                       # cloudflared finto termina: l'attivita' lo riavviera'
    import time
    time.sleep(0.2)
    assert got == ["https://lucky-owl-ace.trycloudflare.com"]
    assert export.api_url() == "https://lucky-owl-ace.trycloudflare.com"
    assert tunnel.tunnel_url("https://api.trycloudflare.com/tunnel") is None
