"""Raccoglitori: ognuno trasforma una fonte in oggetti Event (ancora da arricchire e geolocalizzare)."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterator

from ..fetch import Fetcher
from ..models import Event
from ..store import Store


@dataclass
class Context:
    fetcher: Fetcher
    store: Store
    llm: object
    max_requests: int = 80


def registry() -> dict[str, Callable[[dict, Context], Iterator[Event]]]:
    from . import calendariopodismo, form_csv, html_llm, jsonld, myportal, podismoveneto, rss_news, tribe
    return {
        "form_csv": form_csv.collect,
        "tribe_api": tribe.collect,
        "jsonld": jsonld.collect,
        "myportal": myportal.collect,
        "rss_news": rss_news.collect,
        "calendariopodismo": calendariopodismo.collect,
        "podismoveneto": podismoveneto.collect,
        "html_llm": html_llm.collect,
    }
