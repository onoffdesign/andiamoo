"""Geolocalizzazione: luoghi noti, indirizzi con iniziali e frazioni (2026-11-11)."""
from pipeline.geocode import Geocoder
from pipeline.models import Event
from pipeline.store import Store


def _ev(**kw):
    base = dict(title="Prova", start="2026-11-15", source="t", source_name="t", source_url="https://example.org")
    base.update(kw)
    return Event(**base)


def _geo(tmp_path, cache):
    st = Store(tmp_path / "g.sqlite")
    for k, v in cache.items():
        st.geo_put(k, v)
    return Geocoder(st, offline=True)


TREVISO = {"lat": 45.6669, "lon": 12.2430, "province": "IT-TV", "town": "Treviso", "type": "city"}
CASIER = {"lat": 45.6417, "lon": 12.2953, "province": "IT-TV", "town": "Casier", "type": "village"}


def test_luogo_noto_prima_di_nominatim(tmp_path):
    g = _geo(tmp_path, {"c|treviso": TREVISO})
    ev = _ev(venue="Parco degli Alberi Parlanti (Villa Margherita)", address="Viale G. G. Felissent 56", town="Treviso")
    assert g.locate(ev)
    assert (ev.lat, ev.lon, ev.geo_precision) == (45.69036, 12.25858, "venue")


def test_indirizzo_senza_iniziali_e_parentesi(tmp_path):
    g = _geo(tmp_path, {})
    queries = [q for q, _ in g.place_queries(_ev(venue="Sala (primo piano)", address="Piazza G. Marconi 2",
                                                  town="San Fior"), "San Fior")]
    assert "Piazza Marconi 2, San Fior" in queries
    assert "Sala, San Fior" in queries


def test_frazione_al_posto_del_centro_del_comune(tmp_path):
    dosson = {"lat": 45.6236, "lon": 12.2633, "province": "IT-TV", "town": "Casier", "type": "village"}
    g = _geo(tmp_path, {"c|casier": CASIER, "s|dosson, casier": dosson})
    ev = _ev(venue="Dosson", town="Casier")
    assert g.locate(ev)
    assert (ev.lat, ev.lon, ev.geo_precision) == (45.6236, 12.2633, "frazione")


def test_luogo_noto_solo_nel_suo_comune(tmp_path):
    other = {"lat": 45.70, "lon": 12.10, "province": "IT-TV", "town": "Montebelluna", "type": "town"}
    g = _geo(tmp_path, {"c|montebelluna": other})
    ev = _ev(venue="Parco degli Alberi Parlanti", town="Montebelluna")
    assert g.locate(ev)
    assert ev.geo_precision == "town"
