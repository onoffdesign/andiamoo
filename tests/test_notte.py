import yaml

from pipeline import editorial, notte


def _setup(tmp_path, monkeypatch):
    corr = tmp_path / "correzioni.yaml"
    corr.write_text("# intestazione\ncorreggi:\n  aaa:\n    price: \"5 EUR\"\n    verificato: \"2026-11-01\"\n"
                    "rimuovi:\n  bbb: \"annullato\"\nverificati:\n  ccc: \"2026-11-02\"        # nota\n", encoding="utf-8")
    cur = tmp_path / "eventi_redazione.yaml"
    cur.write_text("eventi:\n  - title: Uno\n    start: 2026-12-01\n    town: Treviso\n    official_url: https://a.it\n",
                   encoding="utf-8")
    parts = tmp_path / "notte"
    parts.mkdir()
    monkeypatch.setattr(editorial, "CORRECTIONS", corr)
    monkeypatch.setattr(editorial, "CURATED", cur)
    monkeypatch.setattr(editorial, "check", lambda: [])
    monkeypatch.setattr(notte, "PARTS", parts)
    return corr, cur, parts


def test_unisce_eventi_e_correzioni(tmp_path, monkeypatch):
    corr, cur, parts = _setup(tmp_path, monkeypatch)
    (parts / "treviso-eventi.yaml").write_text(yaml.safe_dump({"eventi": [
        {"title": "Due", "start": "2026-12-02T21:00", "town": "Oderzo", "official_url": "https://comune.oderzo.tv.it/x",
         "fonte": "https://comune.oderzo.tv.it/x", "trovato": "2026-11-29"}]}, allow_unicode=True), encoding="utf-8")
    (parts / "revisione-correzioni.yaml").write_text(yaml.safe_dump({
        "correggi": {"aaa": {"start": "2026-12-03T20:30"}, "ddd": {"town": "Asolo"}},
        "rimuovi": {"eee": "doppione"}, "verificati": {"fff": "2026-11-29"}}), encoding="utf-8")
    stats = notte.merge(["tutti"])
    assert stats == {"revisione": {"eventi": 0, "correzioni": 4}, "treviso": {"eventi": 1, "correzioni": 0}}
    c = editorial.load(corr)
    assert c["correggi"]["aaa"] == {"price": "5 EUR", "verificato": "2026-11-01", "start": "2026-12-03T20:30"}
    assert c["correggi"]["ddd"] == {"town": "Asolo"}
    assert set(c["rimuovi"]) == {"bbb", "eee"} and set(c["verificati"]) == {"ccc", "fff"}
    assert corr.read_text().startswith("# intestazione") and not editorial.duplicate_keys(corr.read_text())
    titles = [e["title"] for e in yaml.safe_load(cur.read_text())["eventi"]]
    assert titles == ["Uno", "Due"] and not list(parts.iterdir())


def test_parte_non_valida_non_si_unisce(tmp_path, monkeypatch):
    _, cur, parts = _setup(tmp_path, monkeypatch)
    (parts / "italia-eventi.yaml").write_text(yaml.safe_dump({"eventi": [
        {"title": "Tre", "start": "2026-12-02", "town": "Padova", "official_url": "https://www.eventbrite.it/e/1"}]}),
        encoding="utf-8")
    try:
        notte.merge(["italia"])
        assert False
    except SystemExit as e:
        assert "regola fonti" in str(e)
    assert (parts / "italia-eventi.yaml").exists() and "title: Tre" not in cur.read_text()
