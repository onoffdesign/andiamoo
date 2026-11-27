from pipeline.editorial import duplicates


def test_stesso_giorno_comune_titolo_simile():
    ev = [
        {"title": "Anna Castiglia: La paura in tasca tour al New Age Club", "start": "2026-12-18", "town": "Roncade"},
        {"title": "Anna Castiglia: La paura in tasca Tour 2026", "start": "2026-12-18", "town": "Roncade"},
        {"title": "Altro concerto", "start": "2026-12-18", "town": "Roncade"},
    ]
    assert duplicates(ev) == [(0, 1)]


def test_repliche_a_ore_diverse_non_sono_doppioni():
    ev = [
        {"title": "Eleazaro Rossi - Kamikaze", "start": "2026-12-13T17:30", "town": "Conegliano"},
        {"title": "Eleazaro Rossi - Kamikaze", "start": "2026-12-13T21:00", "town": "Conegliano"},
    ]
    assert duplicates(ev) == []


def test_site_duplicates_finds_curated_already_on_site():
    from pipeline.editorial import site_duplicates
    cur = [{"title": "LiTLe Run per il Piccolo Rifugio", "start": "2026-12-26T09:30", "town": "Vittorio Veneto"},
           {"title": "Canto di Natale", "start": "2026-12-24T10:00", "town": "Vittorio Veneto"},
           {"title": "Concerto di Natale", "start": "2026-12-24T21:00", "town": "Vittorio Veneto"}]
    site = [{"uid": "a", "title": "LitTLe RuN", "start": "2026-12-26T09:30", "town": "Vittorio Veneto"},
            {"uid": "b", "title": "Canto di Natale", "start": "2026-12-24T10:00", "town": "Vittorio Veneto"},
            {"uid": "c", "title": "Concerto di Natale", "start": "2026-12-24T17:00", "town": "Vittorio Veneto"}]
    assert site_duplicates(cur, site) == [(0, "a"), (1, "b")]
    site[1]["source"] = "redazione"
    assert site_duplicates(cur, site) == [(0, "a")]
