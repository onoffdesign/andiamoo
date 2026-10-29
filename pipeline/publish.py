"""Pubblicazione: commit e push del file eventi su GitHub (GitHub Pages aggiorna il sito da solo)."""
from __future__ import annotations

import logging
import subprocess

from .config import ROOT, settings

log = logging.getLogger(__name__)


def _git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)


def publish(message: str) -> bool:
    cfg = settings()["publish"]
    path = cfg["export_path"]
    if _git("rev-parse", "--is-inside-work-tree").returncode != 0:
        log.warning("Cartella non collegata a git: niente pubblicazione.")
        return False
    _git("pull", "--rebase", "--autostash", "origin", cfg["branch"])
    _git("add", path)
    if (ROOT / "ops").exists():
        _git("add", "ops")                 # rapporto del giro e coda di revisione per Claude
    if _git("diff", "--cached", "--quiet").returncode == 0:
        log.info("Nessuna novita' da pubblicare.")
        return True
    c = _git("commit", "-m", message)
    if c.returncode != 0:
        log.warning("Commit non riuscito: %s", c.stderr.strip())
        return False
    p = _git("push", "origin", cfg["branch"])
    if p.returncode != 0:
        log.warning("Push non riuscito: %s", p.stderr.strip())
        return False
    log.info("Pubblicato su GitHub.")
    return True
