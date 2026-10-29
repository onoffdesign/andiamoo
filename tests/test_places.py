"""Ricerca approfondita del luogo e punti sparsi per gli eventi con solo il comune."""
from pipeline.export import scatter
from pipeline.geocode import Geocoder, km_between
from pipeline.llm import RulesLLM
from pipeline.models import Event
from pipeline.places import PlaceFinder, from_text, maps_coords
from pipeline.store import Store

TV = {"lat": 45.6669, "lon": 12.2430, "province": "IT-TV", "town": "Treviso", "type": "city"}


def test_text_candidates_real_descriptions():
    # testi reali di insolitotrantran (28/10/2026)
    c = from_text("La casa coi merli: presentazione del libro su Aldo Piccoli a Casa Robegan – Treviso",
                  "Venerdì 30 ottobre, ore 18:30. Casa Robegan, Via Antonio Canova 38, Treviso Info su: https://x", "Treviso")
    assert (c[0]["venue"], c[0]["address"], c[0]["town"]) == ("Casa Robegan", "Via Antonio Canova 38", "Treviso")
    c = from_text("The Rocky Horror Picture Show Night: sing-along di Halloween al Cinema Edera – Treviso",
                  "Sabato 31 ottobre – Cinema Edera, Treviso – 22:00 arrivo dei partecipanti", "Treviso")
    assert c[0]["venue"] == "Cinema Edera"
    c = from_text("Diavolopizza alle Colonne – Mestre (Venezia)", "Indirizzo: Colonne, Via Palazzo 41, Mestre (VE)", "Mestre (Venezia)")
    assert c[0]["address"] == "Via Palazzo 41" and not any(x["venue"] == "Palazzo 41" for x in c)
    assert from_text("Cose Ritrovate – Montebelluna", "Corso Mazzini si trasforma in una vetrina", "Montebelluna")[0]["address"] == "Corso Mazzini"


def test_maps_link_coordinates():
    assert maps_coords("https://www.google.com/maps/place/Teatro/@45.6661,12.2441,17z") == (45.6661, 12.2441)
    assert maps_coords("https://maps.google.com/?q=45.70,12.30") == (45.70, 12.30)
    assert maps_coords("https://www.google.com/maps/search/teatro") is None


def _geo(tmp_path, extra):
    store = Store(tmp_path / "g.sqlite")
    store.geo_put("s|treviso, veneto", TV)
    for k, v in extra.items():
        store.geo_put(k, v)
    return store, Geocoder(store, offline=True)


def test_deep_search_from_text(tmp_path):
    store, geo = _geo(tmp_path, {
        "s|cinema edera, treviso": {"lat": 45.6700, "lon": 12.2330, "province": "IT-TV", "town": "Treviso", "type": "cinema"}})
    ev = Event("t", "T", "https://fonte/1", "Rocky Horror al Cinema Edera – Treviso", start="2026-10-31", town="Treviso",
               raw_text="Sabato 31 ottobre – Cinema Edera, Treviso")
    assert geo.locate(ev, PlaceFinder(None, RulesLLM(), store))
    assert ev.geo_precision == "venue" and ev.venue == "Cinema Edera" and ev.lat == 45.67


def test_deep_search_rejects_far_or_area_hits(tmp_path):
    store, geo = _geo(tmp_path, {
        "s|museo lontano, treviso": {"lat": 45.95, "lon": 12.60, "province": "IT-TV", "town": "Altrove", "type": "museum"},
        "s|teatro sant'artemio, treviso": {"lat": 45.6669, "lon": 12.2430, "province": "IT-TV", "town": "Treviso", "type": "city"}})
    ev = Event("t", "T", "https://fonte/2", "Mostra al Museo Lontano – Treviso", start="2026-10-31", town="Treviso",
               raw_text="Teatro Sant'Artemio")
    assert geo.locate(ev, PlaceFinder(None, RulesLLM(), store))
    assert ev.geo_precision == "town" and not ev.venue            # niente di affidabile: centro del comune


class FakeFetcher:
    def __init__(self, pages):
        self.pages, self.calls = pages, []

    def get(self, url, **kw):
        self.calls.append(url)
        return self.pages[url]


def test_deep_search_follows_venue_link(tmp_path):
    store, geo = _geo(tmp_path, {})
    pages = {
        "https://fonte.it/evento/1": '<html><body><article><h1>Concerto</h1><p>Info sul concerto.</p>'
                                     '<a href="/luoghi/auditorium-x/">Auditorium X</a></article></body></html>',
        "https://fonte.it/luoghi/auditorium-x/": '<html><body><main>Auditorium X'
                                                 '<a href="https://www.google.com/maps/place/X/@45.6702,12.2401,17z">Mappa</a>'
                                                 '</main></body></html>',
    }
    fetcher = FakeFetcher(pages)
    finder = PlaceFinder(fetcher, RulesLLM(), store)
    ev = Event("t", "T", "https://fonte.it/evento/1", "Concerto", start="2026-11-05", town="Treviso", raw_text="")
    assert geo.locate(ev, finder) and ev.geo_precision == "address" and (ev.lat, ev.lon) == (45.6702, 12.2401)
    # seconda volta: tutto dalla cache, nessuna pagina riscaricata
    ev2 = Event("t", "T", "https://fonte.it/evento/1", "Concerto", start="2026-11-05", town="Treviso", raw_text="")
    n = len(fetcher.calls)
    assert geo.locate(ev2, PlaceFinder(fetcher, RulesLLM(), store)) and len(fetcher.calls) == n


def test_shared_list_pages_are_not_fetched(tmp_path):
    store, geo = _geo(tmp_path, {})
    fetcher = FakeFetcher({})
    finder = PlaceFinder(fetcher, RulesLLM(), store)
    evs = [Event("p", "P", "https://blog/novembre.html", f"Corsa {i}", start="2026-11-08", town="Treviso") for i in range(3)]
    finder.begin_batch(evs)
    assert geo.locate(evs[0], finder) and evs[0].geo_precision == "town" and not fetcher.calls


def test_scatter_is_stable_and_bounded():
    a = Event("t", "T", "u1", "A", start="2026-11-01", town="Treviso", lat=TV["lat"], lon=TV["lon"], geo_precision="town")
    b = Event("t", "T", "u2", "B", start="2026-11-01", town="Treviso", lat=TV["lat"], lon=TV["lon"], geo_precision="town")
    pa, pb = scatter(a), scatter(b)
    assert pa == scatter(a) and pa != pb
    for p in (pa, pb):
        assert 0.14 <= km_between(TV["lat"], TV["lon"], *p) <= 0.66


def test_town_is_never_the_province(tmp_path):
    """"Treviso" non deve finire al centro della provincia (15 km a nord della citta')."""
    store = Store(tmp_path / "p.sqlite")
    store.geo_put("s|treviso, veneto", {"lat": 45.807, "lon": 12.205, "province": "IT-TV", "town": "", "type": "county"})
    store.geo_put("c|treviso", {"lat": 45.6667, "lon": 12.2431, "province": "IT-TV", "town": "Treviso", "type": "city"})
    store.geo_put("s|porta san tomaso, treviso", {"lat": 45.6699, "lon": 12.2509, "province": "IT-TV", "town": "Treviso",
                                                  "type": "attraction"})
    geo = Geocoder(store, offline=True)
    only_town = Event("t", "T", "u1", "Memory Cafe", start="2026-11-02", town="Treviso")
    assert geo.locate(only_town) and only_town.geo_precision == "town" and only_town.lat == 45.6667
    walls = Event("t", "T", "u2", "Treviso Sotterranea", start="2026-11-15", town="Treviso",
                  venue="Mura di Treviso, Porta San Tomaso, Treviso", address="Mura di Treviso, Porta San Tomaso, Treviso")
    assert geo.locate(walls) and walls.geo_precision != "town" and (walls.lat, walls.lon) == (45.6699, 12.2509)


def test_far_namesake_is_rejected(tmp_path):
    store, geo = _geo(tmp_path, {
        "s|bar centrale, treviso": {"lat": 45.95, "lon": 12.60, "province": "IT-TV", "town": "Altrove", "type": "bar"}})
    ev = Event("t", "T", "u3", "Aperitivo", start="2026-11-02", town="Treviso", venue="Bar Centrale")
    assert geo.locate(ev) and ev.geo_precision == "town"


def test_stored_town_events_are_relocated(tmp_path):
    from pipeline.run import relocate_town_level
    store = Store(tmp_path / "r.sqlite")
    store.geo_put("c|treviso", {"lat": 45.6667, "lon": 12.2431, "province": "IT-TV", "town": "Treviso", "type": "city"})
    store.geo_put("s|porta san tomaso, treviso", {"lat": 45.6699, "lon": 12.2509, "province": "IT-TV", "town": "Treviso",
                                                  "type": "attraction"})
    old = Event("t", "T", "u9", "Treviso Sotterranea", start="2026-11-15", town="Treviso",
                venue="Mura di Treviso, Porta San Tomaso", lat=45.807, lon=12.205, geo_precision="town")
    old.status = "published"
    store.upsert_event(old)
    assert relocate_town_level(store, Geocoder(store, offline=True), None, set()) == 1
    ev = store.get_event(old.uid)
    assert (ev.lat, ev.lon, ev.geo_precision) == (45.6699, 12.2509, "venue")
