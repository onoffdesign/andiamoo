"""Redazione notturna: correzioni, rimozioni, eventi aggiunti e coda di revisione."""
import json

import pytest
import yaml

from pipeline import editorial, quality
from pipeline.collectors import Context
from pipeline.collectors import redazione
from pipeline.models import Event


@pytest.fixture()
def files(tmp_path, monkeypatch):
    corr, cur = tmp_path / "correzioni.yaml", tmp_path / "eventi_redazione.yaml"
    monkeypatch.setattr(editorial, "CORRECTIONS", corr)
    monkeypatch.setattr(editorial, "CURATED", cur)
    return corr, cur


def ev(title="Concerto", start="2026-11-14", town="Treviso", **kw):
    kw.setdefault("geo_precision", "address")
    return Event("t", "Fonte", f"https://fonte.it/{title}", title, start=start, town=town, lat=45.66, lon=12.24, **kw)


def test_apply_events_keeps_uid_and_removes(files):
    corr, _ = files
    a, b = ev("Concerto"), ev("Sagra")
    corr.write_text(yaml.safe_dump({"correggi": {a.uid: {"start": "2026-11-14T20:45", "title": "Concerto d'autunno",
                                                         "nota": "dal sito del teatro"}},
                                    "rimuovi": {b.uid: "annullato"}}), encoding="utf-8")
    out = editorial.apply_events([a, b], geo=None, corr=editorial.load(corr))
    assert len(out) == 1 and out[0].uid == a.uid and out[0].start == "2026-11-14T20:45"
    assert out[0].title == "Concerto d'autunno" and a.title == "Concerto"      # l'originale non cambia


class FakeGeo:
    def locate(self, e):
        e.lat, e.lon, e.geo_precision = 45.7, 12.3, "venue"
        return True


def test_place_correction_regeocodes(files):
    corr, _ = files
    a = ev(geo_precision="town")
    corr.write_text(yaml.safe_dump({"correggi": {a.uid: {"venue": "Teatro Comunale"}}}), encoding="utf-8")
    out = editorial.apply_events([a], geo=FakeGeo(), corr=editorial.load(corr))
    assert (out[0].lat, out[0].geo_precision, out[0].venue) == (45.7, "venue", "Teatro Comunale")


def test_apply_payload_in_cloud(files):
    corr, _ = files
    payload = {"count": 2, "events": [{"uid": "a1", "title": "X", "start": "2026-11-02", "source_url": "https://s",
                                       "official_url": ""}, {"uid": "b2", "title": "Y", "start": "2026-11-01"}]}
    corr.write_text(yaml.safe_dump({"correggi": {"a1": {"official_url": "https://ufficiale.it", "lat": 45.7, "lon": 12.1}},
                                    "rimuovi": {"b2": "doppione"}}), encoding="utf-8")
    out = editorial.apply_payload(payload, editorial.load(corr))
    assert out["count"] == 1 and out["events"][0]["action_url"] == "https://ufficiale.it"
    assert out["events"][0]["geo_precision"] == "address" and out["redazione"] == {"rimossi": 1, "corretti": 1}


def test_check_reports_bad_values(files):
    corr, cur = files
    corr.write_text(yaml.safe_dump({"correggi": {"a1": {"start": "14/11/2026", "category": "boh", "lat": 45}}}), encoding="utf-8")
    cur.write_text(yaml.safe_dump({"eventi": [{"title": "Senza link", "start": "2026-11-20", "town": "Treviso"}]}), encoding="utf-8")
    errs = " | ".join(editorial.check())
    assert "start deve essere" in errs and "categoria sconosciuta" in errs and "lat e lon" in errs and "official_url" in errs


def test_curated_collector(files):
    _, cur = files
    cur.write_text(yaml.safe_dump({"eventi": [{
        "title": "Concerto d'autunno", "start": "2026-11-14T20:45", "town": "Treviso", "venue": "Teatro Comunale",
        "category": "musica", "access": "biglietto", "official_url": "https://teatro.it/concerto",
        "summary": "Concerto di musica da camera. Info: 333 1234567"}]}), encoding="utf-8")
    out = list(redazione.collect({"id": "redazione", "name": "Redazione"}, Context(None, None, None)))
    assert len(out) == 1 and out[0].start == "2026-11-14T20:45" and out[0].category == "musica"
    assert "333" not in out[0].summary and not out[0].needs_ai and out[0].official_url.startswith("https://teatro")


def test_review_queue_priorities():
    corr = {"correggi": {}, "rimuovi": {}, "verificati": {}}
    from datetime import timedelta
    from pipeline.textutil import today_rome
    d1, d2 = (today_rome() + timedelta(days=2)).isoformat(), (today_rome() + timedelta(days=9)).isoformat()
    ok = ev("Mostra", start=d1 + "T10:00", access="libero", official_url="https://x", summary="Mostra di pittura.",
            category="arte-cultura")
    late = ev("Sagra lontana", start=d2, geo_precision="town")
    soon = ev("Festa vicina", start=d1, geo_precision="town")
    q = quality.build_queue([ok, late, soon], corr, ai_on=True)
    assert [i["titolo"] for i in q] == ["Festa vicina", "Sagra lontana"]
    assert any("solo il comune" in m for m in q[0]["motivi"])
    corr["verificati"][soon.uid] = "2026-10-30"
    assert [i["titolo"] for i in quality.build_queue([ok, late, soon], corr, ai_on=True)] == ["Sagra lontana"]


def test_morning_report(tmp_path, monkeypatch):
    import json as _json
    from pipeline import report
    from pipeline.textutil import today_rome
    today = today_rome().isoformat()
    ops = tmp_path / "ops"; ops.mkdir()
    (ops / "rapporto.json").write_text(_json.dumps({"giro_pc": True, "finito_alle": today + "T01:08+01:00", "minuti": 7,
        "modello": "gemma3:12b", "in_revisione": 12, "fonti": {"insolitotrantran": {"trovati": 50, "nuovi": 4, "errore": ""},
        "ticketone": {"trovati": 0, "nuovi": 0, "errore": "timeout"}, "redazione": {"trovati": 0}}}), encoding="utf-8")
    (ops / "riepilogo-notte.json").write_text(_json.dumps({"data": today, "aggiunti": 9, "corretti": 3, "rimossi": 1,
        "verificati": 20, "aggiunti_per_categoria": {"musica": 6, "sport": 3}, "fonti_nuove": 11, "problemi": ["DICE vuoto"]}),
        encoding="utf-8")
    monkeypatch.setattr(report, "OPS", ops)
    monkeypatch.setattr(report, "DATA_DIR", tmp_path)
    (tmp_path / "resoconto.json").write_text('{"eventi_sul_sito": 120}', encoding="utf-8")
    msg = report.build_message()
    assert "eventi nuovi dalle fonti: 4" in msg and "ticketone (timeout)" in msg and "redazione" not in msg
    assert "aggiunti 9" in msg and "Musica e party 6" in msg and "DICE vuoto" in msg and "rispetto a ieri" in msg


def test_site_reports_never_export_contacts(tmp_path):
    from pipeline import quality
    from pipeline.models import Event
    from pipeline.store import Store
    store = Store(tmp_path / "r.sqlite")
    ev = Event("t", "T", "https://fonte/1", "Sagra", start="2026-11-08", town="Treviso")
    store.add_report(ev.uid, "errore", "Orario sbagliato, scrivetemi a mario.rossi@example.com o 347 1234567",
                     "mario.rossi@example.com")
    out = quality.site_reports(store, [ev])
    text = str(out)
    assert out[0]["evento"] == "Sagra" and "contatto" not in out[0]
    assert "mario.rossi" not in text and "347" not in text


def test_quality_sample_is_stable_per_day():
    from datetime import date
    from pipeline import quality
    from pipeline.models import Event
    evs = [Event("t", "T", f"u{i}", f"Evento {i}", start=f"2026-11-{i + 1:02d}", town="Treviso", lat=45.6, lon=12.2)
           for i in range(28)]
    a = quality.quality_sample(evs, 10, today=date(2026, 11, 1))
    b = quality.quality_sample(list(reversed(evs)), 10, today=date(2026, 11, 1))
    c = quality.quality_sample(evs, 10, today=date(2026, 11, 2))
    assert len(a) == 10 and a == b and a != c
