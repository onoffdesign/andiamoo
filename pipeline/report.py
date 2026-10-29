"""Resoconto del mattino su Telegram: cosa e' cambiato sul sito stanotte (giro del PC + revisione di Claude).

Legge ops/rapporto.json (giro del PC), ops/riepilogo-notte.json (revisione di Claude) e docs/data/events.json,
e manda un messaggio all'amministratore (TELEGRAM_ADMIN_CHAT_ID nel file .env).

Uso:  python -m pipeline.report            (invia)
      python -m pipeline.report --prova    (stampa il messaggio senza inviarlo)
"""
from __future__ import annotations

import argparse
import json
import sys
from html import escape

from . import categories as cats
from .config import DATA_DIR, ROOT, env, settings
from .telegram import Telegram
from .textutil import today_rome

OPS = ROOT / "ops"
SILENT_SOURCES = {"redazione", "modulo-organizzatori"}     # a zero e' normale


def _load(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def build_message() -> str:
    today = today_rome().isoformat()
    site = _load(ROOT / settings()["publish"]["export_path"]) or {"count": 0, "events": []}
    pc = _load(OPS / "rapporto.json") or {}
    claude = _load(OPS / "riepilogo-notte.json") or {}
    state_file = DATA_DIR / "resoconto.json"
    prev = (_load(state_file) or {}).get("eventi_sul_sito")
    labels = {c["id"]: c["label"] for c in cats.categories()}

    count = site.get("count", 0)
    diff = f" ({count - prev:+d} rispetto a ieri)" if isinstance(prev, int) else ""
    lines = [f"🗺️ <b>ANDIAMO? · resoconto del {today[8:10]}/{today[5:7]}</b>",
             f"Sul sito ora: <b>{count} eventi</b>{diff}", ""]

    # giro del PC
    if pc.get("giro_pc") and (pc.get("finito_alle") or "")[:10] == today:
        fonti = pc.get("fonti", {})
        nuovi = sum(int(s.get("nuovi") or 0) for s in fonti.values())
        lines.append(f"🖥️ <b>Giro del PC</b> (finito alle {pc['finito_alle'][11:16]}, {pc.get('minuti', '?')} min, "
                     f"AI locale {escape(pc.get('modello') or pc.get('motore_ai') or '?')})")
        lines.append(f"• eventi nuovi dalle fonti: {nuovi}")
        lines.append(f"• da verificare per Claude: {pc.get('in_revisione', 0)}")
        problemi = [f"{k} ({escape(s['errore'][:60])})" if s.get("errore") else f"{k} (0 eventi)"
                    for k, s in fonti.items() if k not in SILENT_SOURCES and (s.get("errore") or not s.get("trovati"))]
        if problemi:
            lines.append("• fonti con problemi: " + ", ".join(problemi))
    else:
        lines.append("🖥️ <b>Giro del PC: non fatto stanotte.</b> Il PC era spento, non ibernato, o senza rete?")
    lines.append("")

    # revisione di Claude
    if claude.get("data") == today:
        lines.append("🤖 <b>Revisione di Claude</b>")
        lines.append(f"• aggiunti {claude.get('aggiunti', 0)} · corretti {claude.get('corretti', 0)} · "
                     f"rimossi {claude.get('rimossi', 0)} · verificati {claude.get('verificati', 0)}")
        per_cat = claude.get("aggiunti_per_categoria") or {}
        if per_cat:
            lines.append("• aggiunti per categoria: " + ", ".join(
                f"{escape(labels.get(k, k))} {v}" for k, v in sorted(per_cat.items(), key=lambda x: -x[1])))
        lines.append(f"• fonti nuove nel catalogo: {claude.get('fonti_nuove', 0)} · passate al PC: "
                     f"{claude.get('fonti_spostate', 0)} · sistemate: {claude.get('fonti_sistemate', 0)}")
        for p in (claude.get("problemi") or [])[:5]:
            lines.append(f"⚠️ {escape(str(p))[:200]}")
        if claude.get("aggiunti"):
            lines.append("<i>Gli eventi aggiunti da Claude compaiono sulla mappa dopo il giro del PC della notte prossima.</i>")
    else:
        lines.append("🤖 <b>Revisione di Claude: non ancora conclusa</b> (o non partita). Il riepilogo arriva nella notifica di Claude.")
    lines += ["", settings()["site"]["base_url"]]
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Resoconto del mattino su Telegram")
    ap.add_argument("--prova", action="store_true", help="stampa il messaggio senza inviarlo")
    args = ap.parse_args(argv)
    text = build_message()
    if args.prova:
        print(text)
        return 0
    tg, chat = Telegram(), env("TELEGRAM_ADMIN_CHAT_ID")
    if not (tg.enabled and chat):
        print("Telegram non configurato (TELEGRAM_TOKEN e TELEGRAM_ADMIN_CHAT_ID nel file .env). Messaggio:\n" + text)
        return 1
    tg.send(chat, text)
    site = _load(ROOT / settings()["publish"]["export_path"]) or {}
    DATA_DIR.mkdir(exist_ok=True)
    (DATA_DIR / "resoconto.json").write_text(json.dumps({"eventi_sul_sito": site.get("count", 0)}), encoding="utf-8")
    print("Resoconto inviato su Telegram.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
