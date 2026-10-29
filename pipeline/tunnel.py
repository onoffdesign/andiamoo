"""Tunnel Cloudflare per l'API del sito, senza account ne' dominio ("quick tunnel").

Avvia `cloudflared tunnel --url http://localhost:8787`, legge l'indirizzo https://....trycloudflare.com
che Cloudflare assegna, lo salva in data/api_url.txt e ripubblica il sito, cosi' "Aggiungi evento" e
"Segnala" usano subito l'API del PC. L'indirizzo cambia a ogni avvio: ci pensa questo script.
Se in config/settings.yaml c'e' gia' site.api_url (tunnel con nome su api.andiamoo.ai) non fa nulla.

Avvio:  python -m pipeline.tunnel      (su Windows: windows\\run_tunnel.bat, attivita' Andiamoo-Tunnel)
"""
from __future__ import annotations

import logging
import os
import re
import shutil
import subprocess
import sys
import threading
from pathlib import Path

from .config import DATA_DIR, settings

log = logging.getLogger("tunnel")
URL_RE = re.compile(r"https://[a-z0-9-]+\.trycloudflare\.com")
WINDOWS_PATHS = [r"C:\Program Files (x86)\cloudflared\cloudflared.exe", r"C:\Program Files\cloudflared\cloudflared.exe",
                 os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Links\cloudflared.exe")]


def find_cloudflared() -> str | None:
    return shutil.which("cloudflared") or next((p for p in WINDOWS_PATHS if Path(p).exists()), None)


def tunnel_url(line: str) -> str | None:
    m = URL_RE.search(line)
    return m.group(0) if m and "api.trycloudflare.com" not in m.group(0) else None


def publish_url(url: str) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "api_url.txt").write_text(url + "\n", encoding="utf-8")
    from .run import main as run_main
    run_main(["--export-only"])          # rigenera events.json con il nuovo indirizzo e lo pubblica


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    if (settings()["site"].get("api_url") or "").strip():
        log.info("site.api_url e' impostato (%s): tunnel rapido non necessario.", settings()["site"]["api_url"])
        return 0
    exe = find_cloudflared()
    if not exe:
        log.error("cloudflared non trovato. Installa con: winget install Cloudflare.cloudflared")
        return 1
    port = int(settings().get("api", {}).get("port", 8787))
    proc = subprocess.Popen([exe, "tunnel", "--no-autoupdate", "--url", f"http://localhost:{port}"],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1,
                            encoding="utf-8", errors="replace")
    published = False
    for line in proc.stdout:              # cloudflared scrive l'indirizzo nel suo log
        sys.stdout.write(line)
        url = tunnel_url(line)
        if url and not published:
            published = True
            log.info("Tunnel attivo: %s", url)
            threading.Thread(target=publish_url, args=(url,), daemon=True).start()
    code = proc.wait()
    log.warning("cloudflared terminato (codice %s)", code)
    return code or 1                      # l'attivita' di Windows lo riavvia


if __name__ == "__main__":
    sys.exit(main())
