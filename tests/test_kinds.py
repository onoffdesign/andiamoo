"""Solo eventi specifici: calendari scartati, ricorrenze divise in date singole."""
from datetime import date

from pipeline.kinds import looks_like_listing, occurrences, split
from pipeline.models import Event


def ev(title, start, end=None, **kw):
    return Event("eventiesagre", "eventiesagre.it", "https://x/1", title, start=start, end=end, **kw)


def test_listing_detection():
    # caso reale del 29/10/2026 su eventiesagre
    assert looks_like_listing(ev("Calendario Mensile Eventi E Sagre Per Regioni Italiane", "2026-01-01", "2026-12-31",
                                 venue="Italia"))
    assert looks_like_listing(ev("Mercatino", "2026-01-01", "2026-12-31", town="Treviso"))      # quasi un anno
    assert looks_like_listing(ev("Eventi del weekend a Treviso", "2026-11-07"))
    assert not looks_like_listing(ev("Mostra di Canova", "2026-10-01", "2027-02-28", town="Possagno"))
    assert not looks_like_listing(ev("Sagra del radicchio", "2026-11-06", "2026-11-09", town="Treviso"))


def test_monthly_third_sunday():
    e = ev("Mercatino dell'antiquariato", "2026-05-30T08:00", "2026-12-20", town="Godega di Sant'Urbano",
           kind="ricorrente", recurrence={"frequenza": "mensile", "giorno_settimana": "domenica", "settimana_del_mese": 3})
    d = occurrences(e, 120, today=date(2026, 10, 29))
    assert d == ["2026-11-15", "2026-12-20"]
    parts = split(e, d)
    assert [p.start for p in parts] == ["2026-11-15T08:00", "2026-12-20T08:00"] and len({p.uid for p in parts}) == 2
    assert all(p.end is None and p.kind == "evento" for p in parts)


def test_last_weekday_weekly_and_listed():
    last = ev("Mercato", "2026-06-01", "2026-12-31", kind="ricorrente",
              recurrence={"frequenza": "mensile", "giorno_settimana": "sabato", "settimana_del_mese": -1})
    assert occurrences(last, 120, today=date(2026, 10, 29)) == ["2026-10-31", "2026-11-28", "2026-12-26"]
    weekly = ev("Mercato contadino", "2026-10-01", "2026-11-20", kind="ricorrente",
                recurrence={"frequenza": "settimanale", "giorno_settimana": "giovedi"})
    assert occurrences(weekly, 120, today=date(2026, 10, 29)) == ["2026-10-29", "2026-11-05", "2026-11-12", "2026-11-19"]
    listed = ev("Visite guidate", "2026-10-01", "2026-12-31", kind="ricorrente",
                recurrence={"frequenza": "date_elencate", "date_elencate": ["2026-10-10", "2026-11-08", "2027-05-01"]})
    assert occurrences(listed, 120, today=date(2026, 10, 29)) == ["2026-11-08"]


def test_merged_categories():
    from pipeline import categories as cats
    assert cats.category_ids() == ["sport", "arte-cultura", "musica", "sagre-feste", "teatro-spettacoli",
                                   "famiglie-bambini", "mercatini-fiere", "business", "natura-outdoor"]
    assert cats.validate("nightlife", "club") == ("musica", "club")
    assert cats.validate("cinema", "proiezioni") == ("teatro-spettacoli", "proiezioni")
    assert cats.validate("cibo-vino", "degustazioni") == ("sagre-feste", "degustazioni")
    assert cats.validate("benessere", "yoga")[0] == "natura-outdoor" and cats.validate("comunita", None)[0] == "arte-cultura"
