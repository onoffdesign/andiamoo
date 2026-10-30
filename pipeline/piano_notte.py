"""Piano della notte per la revisione di Claude: cosa fare stanotte, dentro il budget del piano in uso.

Legge i file di memoria e stampa solo le voci da lavorare, cosi' Claude non deve leggere per intero file che
crescono ogni notte (copertura, catalogo delle fonti, albero delle categorie): meno testo letto, meno crediti.

Uso:  python -m pipeline.piano_notte
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import date, timedelta

import yaml

from .config import ROOT
from .textutil import today_rome

OPS = ROOT / "ops"
FREQ_DAYS = {"giornaliera": 1, "settimanale": 7, "mensile": 30}


def budget() -> dict:
    path = OPS / "budget.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8")) if path.exists() else {}
    defaults = {"piano": "pro", "ricerche_max": 70, "coda_max": 30, "campione": 10, "test_copertura": 10,
                "fonti_note": 8, "comuni": 6, "ambiti_categorie": 4, "categorie_nuove": 10, "fonti_nuove": 5}
    return {**defaults, **(data or {})}


def active_province() -> tuple[str, str]:
    """(Nome, SIGLA) della riga 'attiva' nella tabella di ops/espansione.md."""
    text = (OPS / "espansione.md").read_text(encoding="utf-8")
    for line in text.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 6 and cells[-1].lower() == "attiva":
            m = re.match(r"(.+?)\s*\((\w+)\)", cells[1])
            if m:
                return m.group(1), m.group(2).upper()
    return "Treviso", "TV"


def _day(v) -> date | None:
    if isinstance(v, date):
        return v
    try:
        return date.fromisoformat(str(v)[:10])
    except ValueError:
        return None


def oldest(mapping: dict | None, n: int) -> list[tuple[str, str]]:
    """Le n voci mai controllate (null) o controllate da piu' tempo; le 'rare' solo se ferme da un mese."""
    today = today_rome()
    items = []
    for name, v in (mapping or {}).items():
        if str(v).strip().lower().startswith("rara"):
            d = _day(str(v).split()[-1]) if " " in str(v) else None
            if d and (today - d).days < 30:
                continue
        d = _day(v)
        # a parita' di data l'ordine cambia ogni notte (stabile nella stessa notte): si girano tutte le voci
        mix = hashlib.sha1(f"{today.isoformat()}|{name}".encode()).hexdigest()
        items.append((d or date.min, mix, name, "mai" if d is None else d.isoformat()))
    items.sort()
    return [(name, when) for _, _, name, when in items[:n]]


def category_scopes() -> list[str]:
    """Ambiti dell'albero delle categorie: 'Macro > Ambito' per ogni riga '- **Ambito**' sotto un titolo '## Macro'."""
    out, macro = [], None
    for line in (OPS / "categorie-ricerca.md").read_text(encoding="utf-8").splitlines():
        h = re.match(r"^## (.+?)(?:\s*\(`[\w-]+`\))?\s*$", line)
        if h:
            macro = h.group(1) if "`" in line else None
            continue
        b = re.match(r"^- \*\*(.+?)\*\*", line)
        if macro and b:
            out.append(f"{macro} > {b.group(1)}")
    return out


def due_sources(n: int) -> list[dict]:
    data = yaml.safe_load((OPS / "fonti.yaml").read_text(encoding="utf-8")) or {}
    today, due = today_rome(), []
    for f in data.get("fonti") or []:
        if str(f.get("stato", "attiva")) in ("spostata", "ferma"):
            continue
        last = _day(f.get("ultimo_controllo"))
        every = FREQ_DAYS.get(str(f.get("frequenza", "settimanale")), 7)
        if last and today < last + timedelta(days=every):
            continue
        due.append(f)
    due.sort(key=lambda f: (-int(f.get("qualita") or 0), str(f.get("ultimo_controllo") or "")))
    return due[:n]


def _count(name: str, key: str) -> int:
    try:
        return len(json.loads((OPS / name).read_text(encoding="utf-8")).get(key) or [])
    except (OSError, ValueError):
        return 0


def main(argv=None) -> int:
    b = budget()
    name, sigla = active_province()
    cov = yaml.safe_load((OPS / "copertura.yaml").read_text(encoding="utf-8")) or {}
    print(f"PIANO DELLA NOTTE {today_rome().isoformat()} · piano Claude: {b['piano']} · "
          f"al massimo {b['ricerche_max']} ricerche (WebSearch + WebFetch) in tutta la notte")
    print(f"Provincia attiva: {name} ({sigla})\n")

    print("1. Manutenzione")
    print(f"   - segnalazioni dal sito: {_count('segnalazioni.json', 'segnalazioni')} negli ultimi 30 giorni "
          f"(gestisci quelle non ancora registrate)")
    print(f"   - coda di revisione: {_count('revisione.json', 'eventi')} in coda, lavorane al massimo {b['coda_max']} "
          f"(nell'ordine del file)")
    print(f"   - controllo a campione: {_count('campione.json', 'eventi')} eventi in ops/campione.json")
    print(f"   - fonti note da riaprire ({b['fonti_note']}):")
    for f in due_sources(b["fonti_note"]):
        print(f"       · {f.get('nome')} | {f.get('query') or f.get('url')} | ultimo controllo {f.get('ultimo_controllo') or 'mai'}")

    print(f"\n2. Ricerca nella provincia attiva ({sigla})")
    print(f"   - comuni da controllare ({b['comuni']}):")
    for town, when in oldest(cov.get(f"comuni_{sigla}"), b["comuni"]):
        print(f"       · {town} (ultimo controllo: {when})")
    done = cov.get(f"categorie_{sigla}") or {}
    scopes = {s: done.get(s) for s in category_scopes()}
    print(f"   - ambiti delle categorie da cercare ({b['ambiti_categorie']}); data in categorie_{sigla}:")
    for scope, when in oldest(scopes, b["ambiti_categorie"]):
        print(f"       · {scope} (ultima ricerca: {when})")
    print(f"   - fonti nuove da cercare e valutare: {b['fonti_nuove']}")

    print("\n3. Misura e memoria")
    print(f"   - test di copertura: {b['test_copertura']} eventi (ops/espansione.md)")
    print(f"   - voci nuove nell'albero delle categorie: {b['categorie_nuove']}")
    print("   - una miglioria del metodo (ops/metodo-ricerca.md)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
