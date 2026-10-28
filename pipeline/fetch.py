"""Scaricamento educato: rispetta robots.txt, pausa tra richieste, cache, user agent dichiarato."""
from __future__ import annotations

import logging
import time
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import httpx

from .config import settings, user_agent
from .store import Store

log = logging.getLogger(__name__)


class Blocked(Exception):
    """La pagina non si puo' raccogliere (robots.txt o protezione anti-bot)."""


class Fetcher:
    def __init__(self, store: Store, *, offline_dir=None):
        cfg = settings()["pipeline"]
        self.store = store
        self.delay = float(cfg["request_delay_seconds"])
        self.cache_age = float(cfg["cache_days"]) * 86400
        self.ua = user_agent()
        self._robots: dict[str, RobotFileParser | None] = {}
        self._last: dict[str, float] = {}
        self.client = httpx.Client(
            headers={"User-Agent": self.ua, "Accept-Language": "it-IT,it;q=0.9"},
            timeout=30, follow_redirects=True,
        )
        self.requests = 0

    # ---------- robots.txt ----------
    def allowed(self, url: str) -> bool:
        p = urlparse(url)
        host = f"{p.scheme}://{p.netloc}"
        if host not in self._robots:
            rp = RobotFileParser()
            try:
                r = self.client.get(host + "/robots.txt")
                if r.status_code >= 400:
                    rp = None          # niente robots.txt = nessun divieto
                else:
                    rp.parse(r.text.splitlines())
            except httpx.HTTPError:
                rp = None
            self._robots[host] = rp
        rp = self._robots[host]
        if rp is None:
            return True
        # Valutiamo sia il nostro user agent sia "*"
        return rp.can_fetch(self.ua.split("/")[0], url) and rp.can_fetch("*", url)

    def _wait(self, url: str) -> None:
        host = urlparse(url).netloc
        last = self._last.get(host, 0)
        pause = self.delay - (time.time() - last)
        if pause > 0:
            time.sleep(pause)
        self._last[host] = time.time()

    # ---------- GET ----------
    def get(self, url: str, *, use_cache: bool = True, max_age: float | None = None,
            accept: str = "text/html,application/json;q=0.9,*/*;q=0.8") -> str:
        max_age = self.cache_age if max_age is None else max_age
        if use_cache:
            cached = self.store.http_get(url, max_age)
            if cached is not None:
                return cached
        if not self.allowed(url):
            raise Blocked(f"robots.txt non consente: {url}")
        self._wait(url)
        self.requests += 1
        r = self.client.get(url, headers={"Accept": accept})
        if r.status_code in (403, 429) or "_Incapsula_Resource" in r.text[:3000]:
            raise Blocked(f"Accesso negato ({r.status_code}): {url}")
        r.raise_for_status()
        body = r.text
        if use_cache:
            self.store.http_put(url, body)
        return body

    def get_json(self, url: str, **kw):
        import json
        return json.loads(self.get(url, accept="application/json", **kw))

    def get_bytes(self, url: str) -> bytes:
        if not self.allowed(url):
            raise Blocked(url)
        self._wait(url)
        r = self.client.get(url)
        r.raise_for_status()
        return r.content
