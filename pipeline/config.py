"""Caricamento configurazione (YAML) e segreti (.env)."""
from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = ROOT / "config"
DATA_DIR = ROOT / "data"          # database e cache locali, non pubblicati
DOCS_DIR = ROOT / "docs"          # sito pubblicato su GitHub Pages


def _load_env() -> None:
    """Legge .env (KEY=VALUE) senza dipendenze esterne. Non sovrascrive variabili gia' impostate."""
    env_file = ROOT / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_env()


def env(key: str, default: str = "") -> str:
    return os.environ.get(key, default)


@lru_cache(maxsize=None)
def load_yaml(name: str) -> dict:
    with open(CONFIG_DIR / name, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def settings() -> dict:
    return load_yaml("settings.yaml")


def sources() -> list[dict]:
    return load_yaml("sources.yaml").get("sources", [])


def watchlist() -> list[dict]:
    return load_yaml("sources.yaml").get("watchlist", [])


def taxonomy() -> dict:
    return load_yaml("categories.yaml")


def user_agent() -> str:
    ua = settings()["pipeline"]["user_agent"]
    return ua.format(contact_email=env("CONTACT_EMAIL", "info@example.com"))
