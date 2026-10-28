"""Test sui campioni reali raccolti il 28/10/2026 (tests/fixtures)."""
import json
from pathlib import Path

import pytest

from pipeline.collectors import calendariopodismo, jsonld, myportal, podismoveneto, rss_news, tribe
from pipeline.collectors.form_csv import parse as parse_form
from pipeline.dedupe import dedupe
from pipeline.enrich import action_link, enrich
from pipeline.geocode import Geocoder
from pipeline.llm import RulesLLM
from pipeline.models import Event
from pipeline.store import Store
from pipeline.textutil import strip_personal_data, to_local_iso

FX = Path(__file__).parent / "fixtures"
SRC = {"id": "test", "name": "Test", "ai_rewrite": True}


def fx(name):
    return (FX / name).read_text(encoding="utf-8")


# ---------- date ----------
@pytest.mark.parametrize("raw,expected", [
    ("2026-10-03T00:00:00+0100", ("2026-10-03", True)),          # eventiesagre: mezzanotte = tutto il giorno
    ("2026-11-18T23:59:59+0100", ("2026-11-18", True)),
    ("2026-10-31T23:01:00.000Z", ("2026-11-01", True)),          # MyPortal: 00:01 ora italiana
    ("2026-10-29T07:30:00.000Z", ("2026-10-29T08:30", False)),   # UTC -> ora solare
    ("2027-04-21T21:00:00.000+02:00", ("2027-04-21T21:00", False)),
    ("2026-10-30 16:30:00", ("2026-10-30T16:30", False)),
    ("2026-12-02", ("2026-12-02", True)),
    ("28/10/2026 20:30", ("2026-10-28T20:30", False)),
])
def test_dates(raw, expected):
    assert to_local_iso(raw) == expected


def test_personal_data_removed():
    t = strip_personal_data("Info 347 950 9961 – lastanzettatreviso@gmail.com, tel. 0422 123456")
    assert "347" not in t and "@" not in t and "0422" not in t


# ---------- raccoglitori ----------
def test_tribe():
    evs = list(tribe.parse(json.loads(fx("tribe_events.json")), SRC))
    assert len(evs) == 3                                   # l'evento in categoria "Venezia" e' scartato
    jazz = evs[0]
    assert jazz.all_day and jazz.start == "2026-10-29"
    assert jazz.town == "Treviso"                          # dal titolo "… – Treviso"
    assert jazz.official_url.startswith("https://www.instagram.com/")
    assert "Via Fonderia 73" in jazz.raw_text
    assert evs[1].start == "2026-10-30T16:30" and evs[1].end == "2026-10-30T18:30"
    assert evs[2].address.startswith("Via Reggimento")


def test_jsonld_detail_eventiesagre():
    evs = [jsonld.to_event(o, SRC) for o in jsonld.iter_jsonld(fx("eventiesagre_detail.html"))]
    evs = [e for e in evs if e]
    assert len(evs) == 1
    e = evs[0]
    assert e.title.startswith("Mostra Dei Funghi") and e.start == "2026-10-03" and e.end == "2026-11-18"
    assert e.town == "Altivole" and e.venue == ""


def test_jsonld_2night():
    e = [x for x in (jsonld.to_event(o, SRC) for o in jsonld.iter_jsonld(fx("2night_detail.html"))) if x][0]
    assert e.venue == "Enoteca Vettoretti" and e.address == "via crevada" and e.town == "San Pietro Di Feletto"


def test_jsonld_eventbrite_itemlist_with_geo():
    e = [x for x in (jsonld.to_event(o, SRC) for o in jsonld.iter_jsonld(fx("eventbrite_listing.html"))) if x][0]
    assert e.venue == "Palaverde" and e.town == "Lancenigo"
    assert e.lat == pytest.approx(45.724118) and e.geo_precision == "source"


def test_jsonld_ticketone_uses_event_url_and_price():
    e = [x for x in (jsonld.to_event(o, SRC) for o in jsonld.iter_jsonld(fx("ticketone_listing.html"))) if x][0]
    assert "/event/" in e.source_url and e.price == "da 30 €" and e.access == "biglietto"
    assert e.town == "Treviso" and e.start == "2027-04-21T21:00"


def test_jsonld_dice_place_events():
    evs = [x for x in (jsonld.to_event(o, SRC) for o in jsonld.iter_jsonld(fx("dice_venue.html"))) if x]
    assert len(evs) == 1 and evs[0].venue == "Treviso Opendream" and evs[0].lat == pytest.approx(45.651301)


def test_jsonld_running_life_default_category():
    src = dict(SRC, default_category="sport", default_subcategory="corsa")
    evs = [x for x in (jsonld.to_event(o, src) for o in jsonld.iter_jsonld(fx("running_life.html"))) if x]
    assert len(evs) == 2 and all(e.category == "sport" for e in evs)


def test_myportal():
    places = {"6709350184843e008d8720bc": json.loads(fx("myportal_place.json"))["entity"]}
    src = dict(SRC, base_url="https://www.comune.treviso.it")
    evs = list(myportal.parse(json.loads(fx("myportal_list.json")), src, places))
    eco = evs[0]
    assert eco.start == "2026-11-01" and eco.all_day
    assert eco.address == "" and eco.venue == ""                     # luogo generico scartato
    assert "Piazza Indipendenza" in eco.raw_text
    assert eco.source_url == "https://www.comune.treviso.it/home/dettaglio/eventi/giornata-ecologica-1-11-2026"
    assert evs[1].start == "2026-10-29T08:30"


def test_calendariopodismo():
    e = calendariopodismo.parse_detail(fx("calendariopodismo_detail.html"), "https://x/gara/1/", SRC)
    assert e.title == "43° Corsa della Salute" and e.start == "2026-11-08T09:00"
    assert e.town == "Giavera del Montello" and e.lat == pytest.approx(45.7967913202)
    assert "5,5km" in e.summary and "info@" not in e.summary and "349" not in e.summary
    assert e.category == "sport" and e.subcategory == "corsa"


def test_podismoveneto_only_tv_not_cancelled():
    evs = list(podismoveneto.parse(fx("podismoveneto_month.html"), {"id": "p", "name": "P"}, "u", 11, 2026))
    titles = [e.title for e in evs]
    assert titles == ["Vertikal Pizzoc", "Corsa della Salute"]
    assert evs[0].start == "2026-11-01T10:00" and evs[0].town == "Fregona" and evs[0].venue == "Sonego"
    assert evs[1].start == "2026-11-08T09:00" and "FIASP" in evs[1].tags


def test_news_feed_entries():
    items = rss_news.entries(fx("gnews.xml"))
    assert items[0]["source"] == "RaiNews"
    assert rss_news._clean_title(items[0]["title"], items[0]["source"]).endswith('"CartaCarbone Festival"')
    assert rss_news.EVENTISH.search(items[0]["title"])


def test_form_csv():
    csv_text = ("Informazioni cronologiche,Titolo evento,Data,Ora,Luogo,Comune,Descrizione,Link,Accesso\n"
                "28/10/2026 10:00,Cena aziendale Rossi,05/12/2026,20:00,Villa X,Treviso,Cena per clienti,https://rossi.it,Su invito\n")
    e = list(parse_form(csv_text, {"id": "modulo"}))[0]
    assert e.status == "pending" and e.access == "invito" and e.start == "2026-12-05T20:00"
    assert e.official_url == "https://rossi.it"


# ---------- arricchimento, geolocalizzazione, deduplica ----------
def test_enrich_rules_fills_address_category_access():
    ev = list(tribe.parse(json.loads(fx("tribe_events.json")), SRC))[1]
    enrich(ev, RulesLLM())
    assert ev.address.startswith("Via San Nicolò 16") and ev.town == "Treviso"
    assert ev.category == "famiglie-bambini" or ev.category == "arte-cultura"
    assert ev.access in ("biglietto", "iscrizione")
    assert ev.summary == "" and not ev.ai_summary                      # senza AI niente riassunto copiato
    assert action_link(ev).startswith("https://www.instagram.com/")


def _seeded_geocoder(tmp_path):
    store = Store(tmp_path / "t.sqlite")
    seed = {
        "s|via fonderia 73, treviso": {"lat": 45.6859, "lon": 12.2494, "province": "IT-TV", "town": "Treviso", "type": "house"},
        "s|giavera del montello, veneto": {"lat": 45.8031, "lon": 12.1646, "province": "IT-TV", "town": "Giavera del Montello", "type": "city"},
        "s|venezia, veneto": {"lat": 45.43, "lon": 12.33, "province": "IT-VE", "town": "Venezia", "type": "city"},
        "r|45.724,12.263": {"lat": 45.7241, "lon": 12.2626, "province": "IT-TV", "town": "Lancenigo", "type": "village"},
    }
    for k, v in seed.items():
        store.geo_put(k, v)
    return store, Geocoder(store, offline=True)


def test_geocode_province_filter(tmp_path):
    _, geo = _seeded_geocoder(tmp_path)
    tv = Event("t", "T", "u1", "Jazz", start="2026-10-29", address="Via Fonderia 73", town="Treviso")
    ve = Event("t", "T", "u2", "Cinema", start="2026-10-29", town="Venezia")
    src_geo = Event("t", "T", "u3", "Show", start="2026-12-02", lat=45.724118, lon=12.2626219)
    lagoon = Event("t", "T", "u4", "Lagoon", start="2026-11-01", lat=45.4536, lon=12.4577)
    assert geo.locate(tv) and tv.geo_precision == "address"
    assert not geo.locate(ve)
    assert geo.locate(src_geo) and src_geo.town == "Lancenigo"
    assert not geo.locate(lagoon)                                       # fuori dal riquadro della provincia


def test_dedupe_prefers_direct_source():
    a = Event("eventbrite", "Eventbrite", "https://eb/1", "FUORI COPIONE Nessun Limite show serale",
              start="2026-12-02", town="Lancenigo", lat=45.72, lon=12.26, geo_precision="source")
    b = Event("comune-x", "Comune", "https://comune/1", "Fuori Copione - Nessun limite!",
              start="2026-12-02T21:00", town="Lancenigo", lat=45.72, lon=12.26, geo_precision="address",
              official_url="https://fuoricopione.it")
    c = Event("eventbrite", "Eventbrite", "https://eb/2", "Altro evento", start="2026-12-02", town="Lancenigo")
    out = dedupe([a, b, c])
    assert len(out) == 2
    main = next(e for e in out if e.also_on)
    assert main.source == "comune-x" and main.also_on[0]["source"] == "Eventbrite"


def test_store_keeps_moderation(tmp_path):
    store = Store(tmp_path / "s.sqlite")
    ev = Event("modulo", "M", "u", "Evento", start="2026-12-01", status="pending")
    assert store.upsert_event(ev)
    store.set_status(ev.uid, "rejected")
    ev2 = Event("modulo", "M", "u", "Evento aggiornato", start="2026-12-01", status="pending")
    store.upsert_event(ev2)
    assert store.get_event(ev.uid).status == "rejected"
