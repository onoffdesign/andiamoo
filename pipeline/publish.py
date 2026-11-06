"""Pubblicazione: commit e push dei file che scrive il PC (GitHub Pages aggiorna il sito da solo).

Il PC e la revisione notturna di Claude scrivono nello stesso repository, ma su file diversi:
  - il PC possiede il sito (docs/data/events.json), i rapporti per Claude in ops/ (elencati in PC_OPS) e l'archivio;
  - Claude possiede tutto il resto (correzioni, eventi della redazione, fonti, file di memoria).
Per non finire mai in un conflitto, il PC non unisce le modifiche: prende la versione di GitHub, ci rimette sopra
solo i propri file appena generati e pubblica. Se nel frattempo qualcuno ha pubblicato, riprova.
"""
from __future__ import annotations

import logging
import subprocess

from .config import ROOT, env, settings

log = logging.getLogger(__name__)

PC_OPS = ["rapporto.json", "revisione.json", "scoperte.csv", "segnalazioni.json", "campione.json", "saturazione.csv"]
ATTEMPTS = 3


def _git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)


def owned_files() -> list[str]:
    """I file che scrive il PC, relativi alla cartella del progetto."""
    paths = [settings()["publish"]["export_path"]] + [f"ops/{n}" for n in PC_OPS]
    archive = ROOT / "archivio"
    if archive.exists():
        paths += [f"archivio/{p.name}" for p in sorted(archive.glob("*.jsonl"))]
    return [p for p in paths if (ROOT / p).exists()]


def publish(message: str) -> bool:
    branch = settings()["publish"]["branch"]
    if _git("rev-parse", "--is-inside-work-tree").returncode != 0:
        log.warning("Cartella non collegata a git: niente pubblicazione.")
        return False
    files = owned_files()
    snapshot = {p: (ROOT / p).read_bytes() for p in files}
    for attempt in range(1, ATTEMPTS + 1):
        for state in ("rebase-merge", "rebase-apply"):
            if (ROOT / ".git" / state).exists():
                _git("rebase", "--abort")
        if (ROOT / ".git" / "MERGE_HEAD").exists():
            _git("merge", "--abort")
        f = _git("fetch", "origin", branch)
        if f.returncode != 0:
            log.warning("GitHub non raggiungibile: %s", f.stderr.strip())
            return False
        _git("reset", "--hard", f"origin/{branch}")          # versione di GitHub, con le modifiche di Claude
        for p, data in snapshot.items():                      # sopra, solo i file del PC appena generati
            (ROOT / p).parent.mkdir(parents=True, exist_ok=True)
            (ROOT / p).write_bytes(data)
        _git("add", "--", *files)
        if _git("diff", "--cached", "--quiet").returncode == 0:
            log.info("Nessuna novita' da pubblicare.")
            return True
        if not _git("config", "user.email").stdout.strip():
            # PC appena installato: identita' dei commit automatici (solo per questo progetto)
            _git("config", "user.name", "ANDIAMO? PC fisso")
            _git("config", "user.email", env("CONTACT_EMAIL", "info@onoff.zone"))
        c = _git("commit", "-m", message)
        if c.returncode != 0:
            log.warning("Commit non riuscito: %s", (c.stderr or c.stdout).strip())
            return False
        p = _git("push", "origin", f"HEAD:{branch}")
        if p.returncode == 0:
            log.info("Pubblicato su GitHub.")
            return True
        log.warning("Push non riuscito (tentativo %d di %d): %s", attempt, ATTEMPTS, p.stderr.strip())
    return False
