"""Tassonomia: elenco categorie, classificazione a regole, validazione dell'output AI."""
from __future__ import annotations

import re
from functools import lru_cache

from .config import taxonomy


@lru_cache(maxsize=1)
def categories() -> list[dict]:
    return taxonomy()["categories"]


@lru_cache(maxsize=1)
def category_ids() -> list[str]:
    return [c["id"] for c in categories()]


@lru_cache(maxsize=1)
def alias_map() -> dict[str, str]:
    """Vecchie categorie -> categoria in cui sono confluite."""
    return {old: c["id"] for c in categories() for old in c.get("aliases", [])}


def canonical(cat: str | None) -> str | None:
    return alias_map().get(cat, cat) if cat else cat


def subcategory_ids(cat: str) -> list[str]:
    for c in categories():
        if c["id"] == cat:
            return list(c.get("sub", {}).keys())
    return []


def access_ids() -> list[str]:
    return list(taxonomy()["access"].keys())


def audience_ids() -> list[str]:
    return list(taxonomy().get("audiences", {}).keys())


def setting_ids() -> list[str]:
    return list(taxonomy().get("settings", {}).keys())


AUDIENCE_RULES = {
    "famiglie": r"bambin|bimb|famigli|kids|ragazzi",
    "giovani": r"student|universit|under ?(25|30)|giovani",
    "senior": r"over ?(60|65)|terza et|anzian|senior",
    "animali": r"cani ammessi|pet.?friendly|amici a quattro zampe|con il tuo cane",
}
OUTDOOR = {"corsa", "ciclismo", "outdoor", "escursioni", "green", "mercati-contadini"}


def audience_rules(text: str, category: str | None) -> list[str]:
    t = text.lower()
    out = [a for a, p in AUDIENCE_RULES.items() if re.search(p, t)]
    if category == "famiglie-bambini" and "famiglie" not in out:
        out.append("famiglie")
    return out


def setting_rules(text: str, sub: str | None) -> str:
    t = text.lower()
    if sub in OUTDOOR or re.search(r"all.aperto|nel parco|in piazza|outdoor|sotto le stelle", t):
        return "all-aperto"
    if re.search(r"al chiuso|teatro|auditorium|sala |cinema|museo|palazzetto|palasport", t):
        return "al-chiuso"
    return ""


def prompt_catalog() -> str:
    """Elenco compatto per il prompt dell'AI: id categoria: sottocategorie."""
    lines = []
    for c in categories():
        subs = ", ".join(f"{k} ({v})" for k, v in c.get("sub", {}).items())
        lines.append(f"- {c['id']} = {c['label']}: {subs}")
    return "\n".join(lines)


def validate(cat: str | None, sub: str | None) -> tuple[str | None, str | None]:
    cat = canonical(cat)
    if cat not in category_ids():
        return None, None
    if sub not in subcategory_ids(cat):
        sub = None
    return cat, sub


def classify_rules(text: str) -> tuple[str | None, str | None]:
    """Classificatore di riserva: conta le parole chiave per categoria e sottocategoria.

    Le righe "Categorie fonte: ..." (categorie dichiarate dal sito) pesano il triplo.
    """
    t = text.lower()
    hints = " ".join(ln for ln in t.splitlines() if ln.startswith("categorie fonte:"))
    best, best_score = None, 0
    for c in categories():
        kws = c.get("keywords", [])
        score = sum(len(re.findall(r"\b" + re.escape(k), t)) for k in kws)
        score += 2 * sum(len(re.findall(r"\b" + re.escape(k), hints)) for k in kws)
        if score > best_score:
            best, best_score = c, score
    if not best:
        return None, None
    sub = None
    sub_score = 0
    for sid, label in best.get("sub", {}).items():
        words = [w for w in re.split(r"[\s,e]+", label.lower()) if len(w) > 3] + [sid.replace("-", " ")]
        s = sum(t.count(w) for w in words)
        if s > sub_score:
            sub, sub_score = sid, s
    return best["id"], sub


ACCESS_RULES = [
    ("invito", r"su invito|solo invitati|riservato agli? invitat|evento privato"),
    ("iscrizione", r"iscrizion|prenotazione obbligatoria|preiscrizione|registrazione obbligatoria|posti limitati|prenota"),
    ("offerta", r"offerta libera|ad offerta|a offerta"),
    ("libero", r"ingresso (libero|gratuito)|accesso libero|gratuit|free entry|entrata libera"),
    ("biglietto", r"bigliett|€\s?\d|\d+\s?€|euro|ticket|prevendita"),
]


def access_rules(text: str) -> str:
    t = text.lower()
    for acc, pattern in ACCESS_RULES:
        if re.search(pattern, t):
            return acc
    return "sconosciuto"
