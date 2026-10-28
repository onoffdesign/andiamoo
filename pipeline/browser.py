"""Browser headless (Playwright) per aprire i link di Google News, che reindirizzano via JavaScript.

Facoltativo: se Playwright non e' installato la pipeline usa solo titolo e sommario del feed.
"""
from __future__ import annotations

import logging

from .config import user_agent
from .textutil import html_to_text

log = logging.getLogger(__name__)


class Browser:
    def __init__(self, pw, browser):
        self._pw, self._browser = pw, browser
        self._ctx = browser.new_context(user_agent=user_agent(), locale="it-IT")

    @classmethod
    def maybe(cls) -> "Browser | None":
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            log.info("Playwright non installato: uso solo i titoli delle notizie.")
            return None
        try:
            pw = sync_playwright().start()
            return cls(pw, pw.chromium.launch(headless=True))
        except Exception as e:  # noqa: BLE001
            log.warning("Browser non avviabile: %s", e)
            return None

    def read(self, url: str, timeout_ms: int = 20000) -> tuple[str, str]:
        """Apre l'URL, attende l'eventuale redirect, ritorna (url finale, testo principale)."""
        page = self._ctx.new_page()
        try:
            page.goto(url, timeout=timeout_ms, wait_until="domcontentloaded")
            try:
                page.wait_for_url(lambda u: "news.google.com" not in u, timeout=10000)
            except Exception:  # noqa: BLE001
                pass
            page.wait_for_timeout(1500)
            final = page.url
            if "news.google.com" in final or "consent." in final:
                return "", ""
            html = page.evaluate(
                "() => (document.querySelector('article') || document.querySelector('main') || document.body).innerHTML")
            return final, html_to_text(html)[:8000]
        except Exception as e:  # noqa: BLE001
            log.info("Articolo non aperto (%s): %s", url, e)
            return "", ""
        finally:
            page.close()

    def close(self):
        try:
            self._browser.close()
            self._pw.stop()
        except Exception:  # noqa: BLE001
            pass
