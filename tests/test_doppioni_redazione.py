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
