"""REGOLA FONTI: piattaforme con divieto di scraping (config/fonti-vietate.yaml).

Stato di un link:
  vietata        termini d'uso o robots.txt vietano l'accesso automatico
  da_verificare  aggregatore o piattaforma non ancora verificato: nel dubbio vale come vietato
  ammessa        aggregatore verificato
  ufficiale      sito di organizzatore, sede, comune, pro loco... (ammesso; il PC rispetta il suo robots.txt)

Il codice non legge mai (ne' dalla cache) una pagina vietata o da verificare, non raccoglie da fonti vietate, e non
pubblica eventi i cui dati vengono da li': finiscono in ops/da-verificare.json per una valutazione manuale.
Il link di una piattaforma vietata resta solo come "Iscrizioni su ..." (ticket_url), se l'evento ha una fonte ammessa.

Uso:  python -m pipeline.fonti_vietate --url <link>     stato del link (da guardare prima di aprirlo)
      python -m pipeline.fonti_vietate --elenco         elenco delle piattaforme vietate e da verificare
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from functools import lru_cache
from typing import Optional
from urllib.parse import urlparse

import yaml

from .config import ROOT
from .textutil import ROME, parse_day, today_rome

LIST_FILE = ROOT / "config" / "fonti-vietate.yaml"
CATALOG = ROOT / "ops" / "fonti.yaml"
HOLD_FILE = ROOT / "ops" / "da-verificare.json"
# tipi del catalogo delle fonti che sono aggregatori o piattaforme: senza verifica valgono come "da verificare"
PLATFORM_TYPES = {"aggregatore", "biglietteria", "testata", "community", "piattaforma", "portale", "news"}
BLOCKED = {"vietata", "da_verificare"}


@lru_cache(maxsize=1)
def _lists() -> dict:
    data = yaml.safe_load(LIST_FILE.read_text(encoding="utf-8")) if LIST_FILE.exists() else {}
    data = data or {}
    out = {k: list(data.get(k) or []) for k in ("vietate", "da_verificare", "ammesse", "api")}
    catalog = []
    if CATALOG.exists():
        try:
            for f in (yaml.safe_load(CATALOG.read_text(encoding="utf-8")) or {}).get("fonti") or []:
                if str(f.get("tipo", "")).lower() in PLATFORM_TYPES and f.get("url"):
                    host = _host(f["url"])
                    if host:
                        catalog.append({"dominio": host, "nota": f"{f.get('tipo')} del catalogo ({f.get('nome')}): "
                                                                 "termini d'uso da leggere"})
        except yaml.YAMLError:
            pass
    out["catalogo"] = catalog
    return out


def reload() -> None:
    _lists.cache_clear()


def _host(url: str) -> str:
    try:
        h = (urlparse(str(url)).hostname or "").lower()
    except ValueError:
        return ""
    return h[4:] if h.startswith("www.") else h


def _match(entry: dict, host: str, path: str) -> bool:
    dom = str(entry.get("dominio", "")).lower().removeprefix("www.")
    if not dom or not (host == dom or host.endswith("." + dom)):
        return False
    pref = entry.get("percorso")
    return not pref or path.startswith(str(pref))


def status(url: Optional[str]) -> tuple[str, Optional[dict]]:
    """Stato del link e voce dell'elenco che lo decide."""
    if not url or not str(url).startswith("http"):
        return "ufficiale", None
    host, path = _host(url), urlparse(str(url)).path or "/"
    lists = _lists()
    for key, label in (("vietate", "vietata"), ("ammesse", "ammessa"), ("da_verificare", "da_verificare"),
                       ("catalogo", "da_verificare")):
        for entry in lists[key]:
            if _match(entry, host, path):
                return label, entry
    return "ufficiale", None


def blocked(url: Optional[str]) -> bool:
    return status(url)[0] in BLOCKED


def api_allowed(url: str) -> bool:
    """Unica eccezione: API ufficiale con chiave valida, elencata in 'api'."""
    host, path = _host(url), urlparse(url).path or "/"
    return any(_match(e, host, path) for e in _lists()["api"])


def label(url: str) -> str:
    """Nome breve della piattaforma per "Iscrizioni su ...": il dominio senza www."""
    return _host(url)


def source_urls(src: dict) -> list[str]:
    urls = [src.get("base_url"), src.get("url"), src.get("api_url")]
    for key in ("listing_urls", "feeds", "urls", "pages"):
        urls += list(src.get(key) or [])
    return [str(u) for u in urls if u and "{" not in str(u)[:8]]


def source_blocked(src: dict) -> Optional[str]:
    """Motivo per cui una fonte del giro non va letta (None se si puo' leggere)."""
    for u in source_urls(src):
        st, entry = status(u)
        if st in BLOCKED and not api_allowed(u):
            why = (entry or {}).get("motivo") or (entry or {}).get("nota") or ""
            return f"fonte {st.replace('_', ' ')}: {_host(u)} {('(' + why + ')') if why else ''}".strip()
    return None


# ---------------------------------------------------------------- eventi pubblicati
def separate(events: list[dict], today=None) -> tuple[list[dict], list[dict]]:
    """Divide gli eventi in pubblicabili e da verificare, applicando la regola delle fonti.

    - dati presi da una fonte vietata o da verificare (source_url) -> non si pubblica: va in da-verificare;
    - sito "ufficiale" su piattaforma vietata -> diventa solo il link "Iscrizioni su ..." (ticket_url);
    - il link d'azione e la fonte indicata nella scheda sono sempre di una fonte ammessa.
    """
    today = today or today_rome()
    keep, held = [], []
    for d in events:
        d = dict(d)
        src = d.get("source_url") or ""
        if src and blocked(src):
            held.append(_hold_item(d, f"dati presi da {status(src)[0].replace('_', ' ')}: {_host(src)}"))
            continue
        off, tic = d.get("official_url") or "", d.get("ticket_url") or ""
        if off and blocked(off):
            if not tic:
                tic = off
            off = ""
        d["official_url"], d["ticket_url"] = off, tic
        action = off or (src if src.startswith("http") else "")
        if not action:
            held.append(_hold_item(d, "nessuna fonte ammessa da indicare come link ufficiale"))
            continue
        d["action_url"] = action
        if d.get("source") == "redazione" and str(d.get("source_name", "")).startswith("Redazione") and src.startswith("http"):
            d["source_name"] = _host(src)          # "Fonte: ..." con il nome della fonte usata davvero
        d["also_on"] = [a for a in d.get("also_on") or [] if not blocked(a.get("url"))]
        keep.append(d)
    return keep, held


def _hold_item(d: dict, reason: str) -> dict:
    return {"uid": d.get("uid"), "titolo": d.get("title"), "inizio": d.get("start"), "fine": d.get("end"),
            "comune": d.get("town"), "fonte": d.get("source_name"),
            "motivo": reason, "link": d.get("source_url") or d.get("official_url"),
            "registrato": datetime.now(ROME).isoformat(timespec="minutes")}


def write_held(items: list[dict], path=None) -> int:
    """Aggiorna ops/da-verificare.json: aggiunge i nuovi, tiene i vecchi finche' l'evento non e' passato."""
    path = path or HOLD_FILE
    if not items and not path.exists():
        return 0
    old = []
    if path.exists():
        try:
            old = json.loads(path.read_text(encoding="utf-8")).get("eventi") or []
        except ValueError:
            old = []
    today = today_rome()
    # le voci vecchie restano solo se il loro link e' ancora vietato o da verificare: le altre (fonte ammessa nel
    # frattempo) le ricalcola ogni pubblicazione, e se tornano pubblicabili escono da qui
    old = [i for i in old if blocked(i.get("link"))]
    by_uid = {i.get("uid") or f"{i.get('titolo')}|{i.get('inizio')}": i for i in old}
    for i in items:
        key = i.get("uid") or f"{i.get('titolo')}|{i.get('inizio')}"
        by_uid.setdefault(key, i)
    rows = [i for i in by_uid.values() if (parse_day(i.get("fine")) or parse_day(i.get("inizio")) or today) >= today]
    rows.sort(key=lambda i: (i.get("inizio") or "", i.get("titolo") or ""))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"nota": "Eventi non pubblicati: i dati vengono da piattaforme vietate o da verificare "
                                        "(config/fonti-vietate.yaml) e non c'e' una fonte ammessa. Valutazione manuale: "
                                        "contatto con l'organizzatore o API ufficiale.", "eventi": rows},
                               ensure_ascii=False, indent=1), encoding="utf-8")
    return len(rows)


TRACE_FILE = ROOT / "ops" / "prelievi.csv"


def write_trace(events: list[dict], path=None) -> None:
    """Tracciabilita' (regola punto 5): per ogni evento pubblicato fonte usata, URL e data e ora del prelievo."""
    import csv
    import io
    path = path or TRACE_FILE
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["uid", "titolo", "inizio", "fonte", "url_fonte", "prelevato_il", "link_ufficiale", "iscrizioni"])
    for d in sorted(events, key=lambda d: (d.get("start") or "", d.get("uid") or "")):
        w.writerow([d.get("uid"), d.get("title"), d.get("start"), d.get("source_name"), d.get("source_url"),
                    d.get("fetched_at") or "non registrato (prima del 2026-11-28)", d.get("official_url"),
                    d.get("ticket_url")])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(buf.getvalue(), encoding="utf-8")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Regola fonti: piattaforme con divieto di scraping")
    ap.add_argument("--url", help="stato di un link")
    ap.add_argument("--elenco", action="store_true", help="piattaforme vietate e da verificare")
    args = ap.parse_args(argv)
    if args.url:
        st, entry = status(args.url)
        msg = {"vietata": "VIETATA: non aprirla, non leggerla, non copiarla. Cerca l'evento su una fonte ammessa.",
               "da_verificare": "DA VERIFICARE: apri solo robots.txt e termini e condizioni. Nessun divieto di scraping "
                                "o simili = scrivila in ammesse; divieto = vietate; illeggibili = resta qui.",
               "ammessa": "ammessa (verificata).",
               "ufficiale": "ammessa (sito ufficiale: rispetta robots.txt)."}[st]
        print(f"{_host(args.url)}: {msg}")
        if entry:
            print("  ", entry.get("motivo") or entry.get("nota") or "")
        return 0
    lists = _lists()
    for key in ("vietate", "da_verificare", "catalogo"):
        print(f"{key}: " + ", ".join(sorted({e['dominio'] for e in lists[key]})))
    return 0


if __name__ == "__main__":
    sys.exit(main())
