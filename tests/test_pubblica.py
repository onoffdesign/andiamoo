from pipeline import pubblica
from pipeline.models import Event


def _ev(**kw):
    base = dict(title="Concerto", start="2026-12-05T21:00", town="Treviso", source="redazione",
                source_name="Redazione", source_url="https://www.comune.treviso.it/evento")
    base.update(kw)
    return Event(**base)


def test_comuni_csv_copre_la_provincia():
    towns = pubblica.load_towns()
    tv = [t for t in towns.values() if t["sigla"] == "TV"]
    assert len(tv) >= 94
    assert "pieve del grappa" in {pubblica._norm(t["nome"]) for t in tv}


def test_posizione_dal_centro_del_comune():
    towns, sigle = pubblica.load_towns(), {"TV"}
    ev = _ev(town="Oderzo")
    assert pubblica.place(ev, towns, [], sigle) == ""
    assert ev.geo_precision == "town" and 45.7 < ev.lat < 45.85


def test_coordinate_scritte_vincono():
    ev = _ev(lat=45.66, lon=12.24)
    assert pubblica.place(ev, pubblica.load_towns(), [], {"TV"}) == ""
    assert (ev.lat, ev.lon) == (45.66, 12.24)


def test_fuori_area_e_comune_sconosciuto():
    towns = pubblica.load_towns()
    assert "fuori area" in pubblica.place(_ev(town="Padova"), towns, [], {"TV"})
    assert "non riconosciuto" in pubblica.place(_ev(town="Paese Che Non Esiste"), towns, [], {"TV"})


def test_luogo_noto():
    known = [{"town": "treviso", "names": ["teatro mario del monaco"], "lat": 45.664, "lon": 12.246}]
    ev = _ev(venue="Teatro Mario Del Monaco")
    assert pubblica.place(ev, pubblica.load_towns(), known, {"TV"}) == ""
    assert ev.geo_precision == "venue" and ev.lat == 45.664


def test_pc_escluso_non_raccoglie(monkeypatch, capsys):
    from pipeline import report, run
    monkeypatch.setattr(run, "settings", lambda: {"pc": {"attivo": False}})
    monkeypatch.setattr(report, "settings", lambda: {"pc": {"attivo": False}})
    assert run.main([]) == 0 and report.main([]) == 0
    assert "PC escluso" in capsys.readouterr().out
