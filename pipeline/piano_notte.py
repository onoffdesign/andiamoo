"""Piano della notte per la revisione di Claude: cosa fare stanotte, dentro il budget del piano in uso.

Legge i file di memoria e stampa solo le voci da lavorare, cosi' Claude non deve leggere per intero file che
crescono ogni notte (copertura, catalogo delle fonti, albero delle categorie): meno testo letto, meno crediti.

Uso:  python -m pipeline.piano_notte
      python -m pipeline.piano_notte --url <link>   (dice se il dominio e' tra quelli che WebFetch non legge)
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import date, timedelta

import yaml

from .config import ROOT, settings
from .textutil import today_rome

OPS = ROOT / "ops"
FREQ_DAYS = {"giornaliera": 1, "settimanale": 7, "mensile": 30, "trimestrale": 90, "annuale": 365}
NEVER = ("mai",)  # fonti da non riaprire da sole (solo su richiesta)
PC_STALE_DAYS = 2  # oltre questo il rapporto del PC e' vecchio: coda, campione e posizioni non sono rinnovati


def budget() -> dict:
    path = OPS / "budget.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8")) if path.exists() else {}
    defaults = {"piano": "pro", "ricerche_max": 70, "coda_max": 30, "campione": 10, "test_copertura": 10,
                "fonti_note": 8, "comuni": 6, "ambiti_categorie": 4, "categorie_nuove": 10, "fonti_nuove": 5,
                "posizioni": 10, "giro": 12, "verifiche_fonti": 2, "province_italia": 0, "comuni_per_provincia": 3}
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
        if str(f.get("stato", "attiva")) in ("spostata", "ferma") or str(f.get("frequenza")) in NEVER:
            continue
        last = _day(f.get("ultimo_controllo"))
        every = FREQ_DAYS.get(str(f.get("frequenza", "settimanale")), 7)
        if last and today < last + timedelta(days=every):
            continue
        due.append(f)
    due.sort(key=lambda f: (-int(f.get("qualita") or 0), str(f.get("ultimo_controllo") or "")))
    return due[:n]


def giro_sources(cov: dict, n: int) -> list[tuple[dict, str, str]]:
    """Fonti del giro (config/sources.yaml) che Claude legge al posto del PC: attive, non vietate, a rotazione
    (le mai lette o lette da piu' tempo prima). La data va in copertura.yaml, sezione giro: {id: AAAA-MM-GG}."""
    from . import fonti_vietate
    from .config import sources
    pool = {}
    for src in sources():
        if not src.get("enabled", True) or src.get("type") == "redazione" or fonti_vietate.source_blocked(src):
            continue
        urls = [u for u in fonti_vietate.source_urls(src) if u.startswith("http")]
        if urls:
            pool[src["id"]] = (src, urls[0])
    done = cov.get("giro") or {}
    order = oldest({k: done.get(k) for k in pool}, n)
    return [(pool[k][0], pool[k][1], when) for k, when in order]


def italy_provinces(cov: dict, n: int, skip: str) -> list[tuple[dict, str]]:
    """Province d'Italia a rotazione (area tutta Italia): prima le mai cercate, nell'ordine di pipeline/italia.py
    (Veneto, regioni vicine, Nord, Centro, Sud e isole), poi quelle cercate da piu' tempo. Data in copertura.yaml,
    sezione province: {SIGLA: AAAA-MM-GG}."""
    from .italia import PROVINCE
    done = cov.get("province") or {}
    rows = []
    for i, (sigla, info) in enumerate(PROVINCE.items()):
        if sigla == skip:
            continue
        d = _day(done.get(sigla))
        rows.append((d or date.min, i, info, d.isoformat() if d else "mai"))
    rows.sort(key=lambda r: (r[0], r[1]))
    return [(info, when) for _, _, info, when in rows[:n]]


def province_towns(sigla: str, cov: dict, n: int) -> list[tuple[str, str]]:
    """I comuni della provincia (config/comuni.csv) controllati da piu' tempo o mai, per la ricerca per comune."""
    import csv
    path = ROOT / "config" / "comuni.csv"
    lines = [l for l in path.read_text(encoding="utf-8").splitlines() if l and not l.startswith("#")]
    from .italia import PROVINCE
    capo = PROVINCE.get(sigla, {}).get("capoluogo", "")
    names = [r["comune"] for r in csv.DictReader(lines) if r["sigla"] == sigla and r["comune"] != capo]
    done = cov.get(f"comuni_{sigla}") or {}
    return oldest({t: done.get(t) for t in names}, n)


def sources_to_verify(n: int) -> list[tuple[str, int]]:
    """Domini da verificare (elenco, catalogo e link degli eventi trattenuti), prima quelli che trattengono piu' eventi."""
    from collections import Counter
    from . import fonti_vietate
    held = Counter()
    try:
        for i in json.loads((OPS / "da-verificare.json").read_text(encoding="utf-8")).get("eventi") or []:
            link = i.get("link") or ""
            if fonti_vietate.status(link)[0] == "da_verificare":
                held[fonti_vietate._host(link)] += 1
    except (OSError, ValueError):
        pass
    lists = fonti_vietate._lists()
    doms = {e["dominio"] for e in lists["da_verificare"] + lists["catalogo"]} | set(held)
    return sorted(((d, held.get(d, 0)) for d in doms), key=lambda x: (-x[1], x[0]))[:n]


def pc_status(today: date | None = None) -> tuple[str, int | None]:
    """(data dell'ultimo giro del PC, giorni passati) da ops/rapporto.json; giorni None se il rapporto manca."""
    try:
        r = json.loads((OPS / "rapporto.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return "mai", None
    d = _day(r.get("finito_alle"))
    if d is None:
        return "mai", None
    return d.isoformat(), ((today or today_rome()) - d).days


def blocked_domains() -> list[dict]:
    path = OPS / "domini-illeggibili.yaml"
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except OSError:
        return []
    return [d for d in data.get("domini") or [] if d.get("dominio")]


def blocked(url: str) -> dict | None:
    """La voce di domini-illeggibili.yaml che copre il link (dominio o sottodominio, percorso se indicato)."""
    m = re.match(r"^(?:[a-z]+://)?([^/?#]+)([^?#]*)", url.strip().lower())
    if not m:
        return None
    host, path = m.group(1).split(":")[0], m.group(2) or "/"
    if host.startswith("www."):
        host = host[4:]
    for d in blocked_domains():
        dom = d["dominio"].lower()
        if (host == dom or host.endswith("." + dom)) and path.startswith((d.get("percorso") or "/").lower()):
            return d
    return None


def _count(name: str, key: str) -> int:
    try:
        return len(json.loads((OPS / name).read_text(encoding="utf-8")).get(key) or [])
    except (OSError, ValueError):
        return 0


def main(argv=None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if args[:1] == ["--url"] and len(args) > 1:
        from . import fonti_vietate
        st, entry = fonti_vietate.status(args[1])
        if st == "da_verificare":
            print(f"DA VERIFICARE: di {fonti_vietate.label(args[1])} puoi aprire solo robots.txt e termini e condizioni; "
                  f"nessun divieto di scraping o simili = scrivila in ammesse, divieto = vietate")
            return 1
        if st in fonti_vietate.BLOCKED:
            print(f"VIETATA (regola fonti, config/fonti-vietate.yaml): {fonti_vietate.label(args[1])} e' "
                  f"{st.replace('_', ' ')}: non aprirla ne' leggerla"
                  + (f" ({entry.get('motivo') or entry.get('nota')})" if entry else ""))
            return 1
        d = blocked(args[1])
        if d:
            print(f"DA EVITARE: {d['dominio']}{d.get('percorso') or ''} non si legge con WebFetch"
                  + (f" ({d['nota']})" if d.get("nota") else ""))
            return 1
        print("ok: dominio non segnato come illeggibile")
        return 0
    b = budget()
    name, sigla = active_province()
    cov = yaml.safe_load((OPS / "copertura.yaml").read_text(encoding="utf-8")) or {}
    print(f"PIANO DELLA NOTTE {today_rome().isoformat()} · piano Claude: {b['piano']} · "
          f"al massimo {b['ricerche_max']} ricerche (WebSearch + WebFetch) in tutta la notte")
    print(f"Provincia attiva: {name} ({sigla})")
    last, days = pc_status()
    pc_on = (settings().get("pc") or {}).get("attivo", True)
    if not pc_on:
        print("Senza PC: raccolta, revisione e pubblicazione le fa Claude. Pubblica con `python -m pipeline.pubblica` "
              "(scrive anche coda, campione e saturazione).")
    elif days is None or days > PC_STALE_DAYS:
        print(f"ATTENZIONE: il PC non gira dal {last} ({days if days is not None else '?'} giorni). Coda, campione e "
              f"posizioni sono vecchi: non spendere ricerche su di loro, riporta i numeri gia' noti e usa il budget "
              f"per la ricerca. Segnalalo nel messaggio finale.")
    else:
        print(f"Giro del PC: ultimo il {last}")
    from . import fonti_vietate
    lists = fonti_vietate._lists()
    print("REGOLA FONTI: mai aprire, leggere o cercare con site: le piattaforme vietate o da verificare di "
          "config/fonti-vietate.yaml (" + ", ".join(sorted(e["dominio"] for e in lists["vietate"])[:12]) + ", ...). "
          "Delle da verificare si aprono solo robots.txt e termini (vedi sotto). "
          "Controllo di un link: python -m pipeline.fonti_vietate --url <link>")
    todo = sources_to_verify(b["verifiche_fonti"])
    if todo:
        print(f"Fonti da verificare stanotte ({len(todo)}; leggi SOLO robots.txt e termini e condizioni: nessun divieto "
              f"di scraping o simili = ammessa, divieto = vietata, pagine illeggibili = resta da verificare): "
              + ", ".join(f"{d} ({n} eventi trattenuti)" if n else d for d, n in todo))
    doms = [d["dominio"] + (d.get("percorso") or "") for d in blocked_domains()]
    if doms:
        print(f"Non aprire con WebFetch (ops/domini-illeggibili.yaml): {', '.join(doms)}")
    print()

    print("1. Manutenzione")
    print(f"   - segnalazioni dal sito: {_count('segnalazioni.json', 'segnalazioni')} negli ultimi 30 giorni "
          f"(gestisci quelle non ancora registrate)")
    print(f"   - coda di revisione: {_count('revisione.json', 'eventi')} in coda, lavorane al massimo {b['coda_max']} "
          f"(nell'ordine del file)")
    print(f"   - controllo a campione: {_count('campione.json', 'eventi')} eventi in ops/campione.json")
    pos_path = ROOT / "ops" / "posizioni.json"
    if pos_path.exists():
        r = json.loads(pos_path.read_text(encoding="utf-8")).get("riepilogo", {})
        print(f"   - posizioni (ops/posizioni.json): {r.get('luoghi_con_punti_diversi', 0)} luoghi con punti diversi, "
              f"{r.get('lontani_dal_comune', 0)} eventi lontani dal comune, {r.get('solo_comune_con_luogo', 0)} con luogo "
              f"ma senza punto, {r.get('candidati_luoghi_noti', 0)} candidati per config/luoghi.yaml "
              f"(allineati in automatico: {r.get('allineati_in_automatico', 0)}); sistemane almeno {b.get('posizioni', 10)}")
    else:
        print("   - posizioni: ops/posizioni.json non ancora scritto dal PC")
    print(f"   - fonti note da riaprire ({b['fonti_note']}):")
    for f in due_sources(b["fonti_note"]):
        print(f"       · {f.get('nome')} | {f.get('query') or f.get('url')} | ultimo controllo {f.get('ultimo_controllo') or 'mai'}")

    if not pc_on:
        print(f"   - fonti del giro da leggere al posto del PC ({b['giro']}), data in copertura.yaml sezione giro:")
        for src, url, when in giro_sources(cov, b["giro"]):
            print(f"       · {src['id']} | {src.get('name')} | {url} | ultima lettura {when}")

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

    from .italia import all_italy
    if all_italy(settings()["area"]["provinces"]) and b["province_italia"]:
        print(f"\n2b. Resto d'Italia (area: tutta Italia): {b['province_italia']} province a rotazione; per ognuna "
              f"capoluogo (Comune, ufficio turistico, teatri, musei), un ambito delle categorie e i comuni indicati. "
              f"Date in copertura.yaml: province.<SIGLA> e comuni_<SIGLA>.<Comune>")
        for info, when in italy_provinces(cov, b["province_italia"], sigla):
            towns = ", ".join(t for t, _ in province_towns(info["sigla"], cov, b["comuni_per_provincia"]))
            print(f"       · {info['provincia']} ({info['sigla']}, {info['regione']}) | capoluogo {info['capoluogo']} | "
                  f"comuni: {towns} | ultima ricerca {when}")

    print("\n3. Misura e memoria")
    print(f"   - test di copertura: {b['test_copertura']} eventi (ops/espansione.md)")
    print(f"   - voci nuove nell'albero delle categorie: {b['categorie_nuove']}")
    print("   - una miglioria del metodo (ops/metodo-ricerca.md)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
