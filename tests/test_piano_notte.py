from datetime import date, timedelta

from pipeline import piano_notte


def test_annual_and_quarterly_sources_not_due_every_week(tmp_path, monkeypatch):
    today = date(2026, 11, 23)
    (tmp_path / "fonti.yaml").write_text(
        "fonti:\n"
        f"  - {{nome: annuale, frequenza: annuale, ultimo_controllo: '{today - timedelta(days=10)}'}}\n"
        f"  - {{nome: trimestrale, frequenza: trimestrale, ultimo_controllo: '{today - timedelta(days=10)}'}}\n"
        f"  - {{nome: settimanale, frequenza: settimanale, ultimo_controllo: '{today - timedelta(days=10)}'}}\n"
        "  - {nome: mai, frequenza: mai}\n",
        encoding="utf-8")
    monkeypatch.setattr(piano_notte, "OPS", tmp_path)
    monkeypatch.setattr(piano_notte, "today_rome", lambda: today)
    assert [f["nome"] for f in piano_notte.due_sources(10)] == ["settimanale"]


def test_pc_status_reports_stale_report(tmp_path, monkeypatch):
    (tmp_path / "rapporto.json").write_text('{"finito_alle": "2026-11-11T09:19+01:00"}', encoding="utf-8")
    monkeypatch.setattr(piano_notte, "OPS", tmp_path)
    assert piano_notte.pc_status(date(2026, 11, 23)) == ("2026-11-11", 12)


def test_pc_status_without_report(tmp_path, monkeypatch):
    monkeypatch.setattr(piano_notte, "OPS", tmp_path)
    assert piano_notte.pc_status(date(2026, 11, 23)) == ("mai", None)
