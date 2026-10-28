"""Notizie (Google News, testate locali, magazine): l'AI decide se un articolo annuncia un evento futuro."""
from __future__ import annotations

import logging
import re
import time
from calendar import timegm
from typing import Iterator

import feedparser

from ..fetch import Blocked
from ..llm import RulesLLM
from ..models import Event
from ..textutil import html_to_text, unescape
from . import Context

log = logging.getLogger(__name__)

# Pre-filtro economico: solo i titoli che sembrano parlare di un evento vanno all'AI.
EVENTISH = re.compile(
    r"festival|concert|sagra|festa|mostra|spettacol|teatro|rassegna|maratona|corsa|gara|torneo|partita|"
    r"fiera|mercatin|convegno|incontro|presentazion|inaugura|open day|serata|evento|edizione|"
    r"appuntament|weekend|cosa fare|in programma|tour|live|danza|cinema|degustazion|camminata|marcia",
    re.I,
)
MAX_AGE_DAYS = 10


def entries(feed_text: str) -> list[dict]:
    parsed = feedparser.parse(feed_text)
    out = []
    for e in parsed.entries:
        published = e.get("published_parsed") or e.get("updated_parsed")
        ts = timegm(published) if published else time.time()
        src = e.get("source", {}) or {}
        content = ""
        if e.get("content"):
            content = e["content"][0].get("value", "")
        out.append({
            "title": unescape(e.get("title", "")),
            "link": e.get("link", ""),
            "summary": html_to_text(content or e.get("summary", "")),
            "source": src.get("title", "") if isinstance(src, dict) else "",
            "ts": ts,
        })
    return out


def _clean_title(title: str, source: str) -> str:
    if source and title.endswith(" - " + source):
        return title[: -len(source) - 3]
    return title


def collect(src: dict, ctx: Context) -> Iterator[Event]:
    if isinstance(ctx.llm, RulesLLM):
        log.info("%s: senza AI non si estraggono eventi dalle notizie, salto.", src["id"])
        return
    browser = None
    for feed_url in src.get("feeds", []):
        try:
            text = ctx.fetcher.get(feed_url, max_age=3600, accept="application/rss+xml,application/xml,text/xml")
        except Blocked as e:
            log.warning("%s: %s", src["id"], e)
            continue
        for item in entries(text):
            if time.time() - item["ts"] > MAX_AGE_DAYS * 86400:
                continue
            title = _clean_title(item["title"], item["source"])
            if not EVENTISH.search(title + " " + item["summary"][:300]):
                continue
            url, body = item["link"], item["summary"]
            if src.get("resolve_with_browser") and "news.google.com" in url:
                if browser is None:
                    from ..browser import Browser
                    browser = Browser.maybe()
                if browser:
                    final_url, page_text = browser.read(url)
                    if final_url and ctx.fetcher.allowed(final_url):
                        url, body = final_url, page_text or body
            article = f"TITOLO: {title}\nTESTATA: {item['source'] or src['name']}\n\n{body}"
            try:
                found = ctx.llm.extract_events(article, hint="Fonte: articolo di giornale locale.")
            except Exception as e:  # noqa: BLE001
                log.warning("AI non riuscita su %s: %s", url, e)
                continue
            for f in found:
                if (f.get("province") or "TV").upper() not in ("TV", "TREVISO"):
                    continue
                yield Event(
                    source=src["id"], source_name=item["source"] or src["name"], source_url=url,
                    title=f.get("title") or title, start=f.get("start") or None, end=f.get("end") or None,
                    all_day=len(f.get("start") or "") == 10,
                    summary=f.get("summary", ""), category=f.get("category"), subcategory=f.get("subcategory"),
                    access=f.get("access") or "sconosciuto", price=f.get("price", ""),
                    venue=f.get("venue", ""), address=f.get("address", ""), town=f.get("town", ""),
                    ticket_url=f.get("ticket_url", ""), official_url=f.get("official_url", ""),
                    ai_summary=bool(f.get("summary")), needs_ai=False, ai_allowed=True,
                )
    if browser:
        browser.close()
