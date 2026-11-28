"""Lavoro in parallelo della sessione notturna: ogni agente scrive solo i suoi file "parte", poi il coordinatore li
unisce ai file della redazione.

Ogni agente (giro, revisione, treviso, italia...) scrive in config/notte/:
  <agente>-eventi.yaml       eventi nuovi, stesso formato di config/eventi_redazione.yaml (chiave "eventi")
  <agente>-correzioni.yaml   correzioni, stesso formato di config/correzioni.yaml (correggi, rimuovi, verificati)
e il suo resoconto in ops/notte/<agente>.md. Nessun agente tocca eventi_redazione.yaml o correzioni.yaml, ne'
pubblica, ne' fa commit: lo fa solo il coordinatore, quando un agente ha finito:

  python -m pipeline.notte --controlla [agente]   controlla le parti (senza unire)
  python -m pipeline.notte --unisci agente [...]  unisce le parti di quegli agenti e le cancella
  python -m pipeline.notte --unisci tutti         unisce tutte le parti presenti
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

from . import editorial, fonti_vietate
from .config import ROOT

PARTS = ROOT / "config" / "notte"
SECTIONS = ("correggi", "rimuovi", "verificati")


def part_files(agents: list[str] | None = None) -> dict[str, dict[str, Path]]:
    out: dict[str, dict[str, Path]] = {}
    if not PARTS.exists():
        return out
    for p in sorted(PARTS.glob("*.yaml")):
        m = re.match(r"(.+)-(eventi|correzioni)\.yaml$", p.name)
        if m and (not agents or "tutti" in agents or m.group(1) in agents):
            out.setdefault(m.group(1), {})[m.group(2)] = p
    return out


def _load(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def check_events(events: list, label: str) -> list[str]:
    errs = []
    for i, ev in enumerate(events):
        where = f"{label}[{i}] {ev.get('title', '')!r}"
        for req in ("title", "start", "town", "official_url"):
            if not ev.get(req):
                errs.append(f"{where}: manca '{req}'")
        errs += editorial.validate_fields({k: v for k, v in ev.items() if k not in ("fonte", "trovato")}, where)
        for key in ("official_url", "fonte"):
            url = str(ev.get(key) or "")
            if url.startswith("http") and fonti_vietate.blocked(url):
                errs.append(f"{where}: {key} su fonte {fonti_vietate.status(url)[0].replace('_', ' ')} "
                            f"({fonti_vietate.label(url)}): regola fonti")
    return errs


def check(agents: list[str] | None = None) -> list[str]:
    errs = []
    for agent, files in part_files(agents).items():
        try:
            if "eventi" in files:
                errs += check_events(_load(files["eventi"]).get("eventi") or [], f"{agent}-eventi")
            if "correzioni" in files:
                data = _load(files["correzioni"])
                errs += editorial.duplicate_keys(files["correzioni"].read_text(encoding="utf-8"))
                for uid, fields in (data.get("correggi") or {}).items():
                    if not isinstance(fields, dict):
                        errs.append(f"{agent}-correzioni correggi.{uid}: deve contenere i campi da cambiare")
                    else:
                        errs += editorial.validate_fields(fields, f"{agent}-correzioni correggi.{uid}")
        except yaml.YAMLError as e:
            errs.append(f"{agent}: file non leggibile: {e}")
    return errs


def _dump(obj) -> str:
    return yaml.safe_dump(obj, allow_unicode=True, sort_keys=False, width=1000, default_flow_style=False)


def _indent(text: str, n: int) -> str:
    return "".join((" " * n + line if line.strip() else line) for line in text.splitlines(keepends=True))


def _section_bounds(lines: list[str], name: str) -> tuple[int, int]:
    """(riga dell'intestazione, riga dove finisce la sezione) in correzioni.yaml; -1 se la sezione manca."""
    start = next((i for i, l in enumerate(lines) if l.rstrip() == f"{name}:" or l.startswith(f"{name}: ")), -1)
    if start < 0:
        return -1, -1
    end = start + 1
    while end < len(lines) and (not lines[end].strip() or lines[end].startswith((" ", "#"))):
        end += 1
    while end > start + 1 and not lines[end - 1].strip():
        end -= 1
    return start, end


def merge_corrections(part: dict, path: Path | None = None) -> int:
    """Unisce una parte in correzioni.yaml: una voce gia' presente viene sostituita (per correggi i campi si sommano,
    quelli nuovi vincono)."""
    path = path or editorial.CORRECTIONS
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    current = editorial.load(path) if path.exists() else {s: {} for s in SECTIONS}
    n = 0
    for name in SECTIONS:
        items = part.get(name) or {}
        if not items:
            continue
        lines = text.splitlines(keepends=True)
        start, end = _section_bounds(lines, name)
        if start < 0:
            text = text.rstrip("\n") + f"\n{name}:\n"
            lines = text.splitlines(keepends=True)
            start, end = _section_bounds(lines, name)
        body = lines[start + 1:end]
        for uid in items:
            key = re.compile(rf"^  ['\"]?{re.escape(str(uid))}['\"]?:")
            out, skip = [], False
            for line in body:
                if key.match(line):
                    skip = True
                    continue
                if skip and (line.startswith("    ") or not line.strip()):
                    continue
                skip = False
                out.append(line)
            body = out
        merged = {}
        for uid, val in items.items():
            if name == "correggi" and isinstance(current["correggi"].get(uid), dict) and isinstance(val, dict):
                val = {**current["correggi"][uid], **val}
            merged[str(uid)] = val
            n += 1
        block = _indent(_dump(merged), 2)
        lines = lines[:start + 1] + body + [block] + lines[end:]
        text = "".join(lines)
    path.write_text(text, encoding="utf-8")
    return n


def merge_events(events: list, path: Path | None = None) -> int:
    path = path or editorial.CURATED
    if not events:
        return 0
    text = path.read_text(encoding="utf-8") if path.exists() else "eventi:\n"
    text = text.rstrip("\n") + "\n" + _indent(_dump(events), 2)
    path.write_text(text, encoding="utf-8")
    return len(events)


def merge(agents: list[str]) -> dict:
    errs = check(agents)
    if errs:
        raise SystemExit("Parti non valide, correggile prima di unire:\n  " + "\n  ".join(errs))
    stats = {}
    for agent, files in part_files(agents).items():
        ev = merge_events(_load(files["eventi"]).get("eventi") or []) if "eventi" in files else 0
        co = merge_corrections(_load(files["correzioni"])) if "correzioni" in files else 0
        for p in files.values():
            p.unlink()
        stats[agent] = {"eventi": ev, "correzioni": co}
    bad = editorial.check()
    if bad:
        print("ATTENZIONE: dopo l'unione editorial --controlla segnala:\n  " + "\n  ".join(bad[:20]))
    return stats


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Parti degli agenti della notte")
    ap.add_argument("--controlla", nargs="*", metavar="AGENTE")
    ap.add_argument("--unisci", nargs="+", metavar="AGENTE")
    args = ap.parse_args(argv)
    if args.unisci:
        print(merge(args.unisci))
        return 0
    errs = check(args.controlla or None)
    print("Parti valide." if not errs else "\n".join(errs))
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
