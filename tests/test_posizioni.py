"""Controllo automatico delle posizioni (pipeline/posizioni.py)."""
from pipeline import posizioni
from pipeline.models import Event


def _ev(uid, venue, address, town, lat, lon, prec):
    ev = Event(title=f"Evento {uid}", start="2026-11-20", source="t", source_name="t",
               source_url="https://example.org", venue=venue, address=address, town=town,
               lat=lat, lon=lon, geo_precision=prec)
    ev.__dict__["uid_override"] = uid
    return ev


def test_allinea_luogo_gia_posizionato():
    evs = [_ev("a", "Parco degli Alberi Parlanti", "", "Treviso", 45.6904, 12.2586, "venue"),
           _ev("b", "Parco degli Alberi Parlanti (Villa Margherita)", "Viale G. G. Felissent 56", "Treviso",
               45.6669, 12.2430, "town")]
    rep = posizioni.check(evs)
    assert (evs[1].lat, evs[1].lon, evs[1].geo_precision) == (45.6904, 12.2586, "venue")
    assert rep["riepilogo"]["allineati_in_automatico"] == 1


def test_segnala_punti_diversi_e_lontani():
    evs = [_ev("a", "Teatro Comunale", "Via Roma 1", "Paese", 45.67, 12.17, "address"),
           _ev("b", "Teatro Comunale", "Via Roma 1", "Paese", 45.67, 12.17, "address"),
           _ev("c", "Teatro Comunale", "Via Roma 1", "Paese", 45.95, 12.30, "venue")]
    rep = posizioni.check(evs, centers={"paese": (45.67, 12.17)})
    assert rep["riepilogo"]["luoghi_con_punti_diversi"] >= 1
    assert "c" in posizioni.flagged_uids(rep)
    assert rep["riepilogo"]["lontani_dal_comune"] == 1


def test_luogo_senza_punto_in_elenco():
    evs = [_ev("a", "Sala polifunzionale del Municipio", "Piazza G. Marconi 2", "San Fior", 45.92, 12.36, "town")]
    rep = posizioni.check(evs)
    assert rep["senza_punto"][0]["eventi"] == 1
