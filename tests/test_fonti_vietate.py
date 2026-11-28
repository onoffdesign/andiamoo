"""Regola fonti: piattaforme con divieto di scraping."""
from datetime import date

import pytest

from pipeline import fonti_vietate as fv


@pytest.fixture(autouse=True)
def lists(tmp_path, monkeypatch):
    f = tmp_path / "fonti-vietate.yaml"
    f.write_text("""
vietate:
  - {dominio: eventbrite.it, motivo: termini 13.1}
  - {dominio: instagram.com, motivo: meta}
da_verificare:
  - {dominio: eventiesagre.it}
ammesse:
  - {dominio: blogspot-ok.com}
api: []
""", encoding="utf-8")
    monkeypatch.setattr(fv, "LIST_FILE", f)
    monkeypatch.setattr(fv, "CATALOG", tmp_path / "nessuno.yaml")
    fv.reload()
    yield
    fv.reload()


def test_status_of_links():
    assert fv.status("https://www.eventbrite.it/e/123")[0] == "vietata"
    assert fv.status("https://eventiesagre.it/x")[0] == "da_verificare"
    assert fv.status("https://www.blogspot-ok.com/")[0] == "ammessa"
    assert fv.status("https://www.comune.treviso.it/eventi")[0] == "ufficiale"
    assert fv.blocked("https://eventiesagre.it/x") and not fv.blocked("https://www.comune.treviso.it/")
    assert not fv.blocked("https://noteventbrite.it/")          # solo il dominio e i suoi sottodomini


def test_banned_source_is_not_read():
    assert fv.source_blocked({"listing_urls": ["https://www.eventbrite.it/d/italy--treviso/"]})
    assert fv.source_blocked({"base_url": "https://www.comune.paese.tv.it"}) is None


def test_separate_holds_and_rewrites(tmp_path):
    events = [
        # dati presi da Eventbrite: non si pubblica
        {"uid": "a", "title": "Bike test", "start": "2026-12-01", "source_url": "https://www.eventbrite.it/e/1"},
        # fonte ammessa con iscrizioni su Eventbrite: si pubblica, Eventbrite solo come "Iscrizioni su"
        {"uid": "b", "title": "Corso", "start": "2026-12-02", "source_url": "https://www.comune.treviso.it/ev",
         "official_url": "https://www.eventbrite.it/e/2", "ticket_url": ""},
        # unico link ufficiale su Instagram, fonte ammessa: il link d'azione diventa la fonte ammessa
        {"uid": "c", "title": "Live", "start": "2026-12-03", "source_url": "https://www.teatro.example/live",
         "official_url": "https://www.instagram.com/x/", "ticket_url": "https://biglietti.example/1"},
    ]
    keep, held = fv.separate(events, today=date(2026, 11, 28))
    assert [d["uid"] for d in keep] == ["b", "c"] and held[0]["uid"] == "a" and "eventbrite.it" in held[0]["motivo"]
    b, c = keep
    assert b["official_url"] == "" and b["ticket_url"] == "https://www.eventbrite.it/e/2"
    assert b["action_url"] == "https://www.comune.treviso.it/ev"
    assert c["official_url"] == "" and c["action_url"] == "https://www.teatro.example/live"
    path = tmp_path / "da-verificare.json"
    assert fv.write_held(held, path) == 1 and fv.write_held(held, path) == 1     # niente doppioni
