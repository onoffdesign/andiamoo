"""Controllo automatico delle posizioni di tutti gli eventi, a ogni giro del PC (2026-11-11).

Nasce da un errore visto da Federico: gli eventi del Parco degli Alberi Parlanti erano sparsi nel centro storico
di Treviso perche' l'indirizzo non veniva trovato, mentre altri eventi nello stesso parco avevano il punto giusto.
Il controllo non aspetta che qualcuno se ne accorga:

1. **Allinea** (correzione automatica): un evento con solo il comune che nomina un luogo (o un indirizzo) gia'
   posizionato con certezza in altri eventi dello stesso comune prende quel punto.
2. **Segnala** in `ops/posizioni.json`, raggruppato per luogo, quello che non si puo' sistemare da solo:
   - stesso luogo con punti diversi (oltre `SPREAD_KM`) in eventi diversi;
   - punti lontani dal centro del loro comune (oltre `FAR_KM`), cioe' probabilmente nel comune sbagliato;
   - luoghi con un nome ma senza punto (solo il comune), ordinati per numero di eventi: i primi della lista vanno
     cercati e scritti in `config/luoghi.yaml`;
   - luoghi che tornano in piu' eventi con un punto coerente ma non ancora in `config/luoghi.yaml` (candidati).
La revisione notturna legge il file e sistema i gruppi dal piu' grande (vedi ops/revisione-notturna.md).
"""
from __future__ import annotations

import json
import re
from collections import defaultdict
from datetime import datetime
from statistics import median
from typing import Iterable

from .config import ROOT
from .geocode import INITIALS_RE, PAREN_RE, _norm, km_between, load_known_places
from .models import Event
from .textutil import ROME

OPS = ROOT / "ops"
SPREAD_KM = 0.4          # stesso luogo: punti piu' lontani di cosi' tra loro sono sospetti
FAR_KM = 6               # come in quality.py: oltre, il punto e' probabilmente in un altro comune
ANCHORS = ("source", "address", "venue")    # precisioni che valgono come punto certo di un luogo
CANDIDATE_MIN = 3        # eventi nello stesso luogo per proporlo in config/luoghi.yaml
GENERIC = {"", "piazza", "centro", "centro storico", "municipio", "chiesa", "parrocchia", "sede", "online",
           "da definire", "varie sedi", "vari luoghi", "luogo da definire"}


def place_keys(ev: Event) -> list[str]:
    """Chiavi con cui riconoscere lo stesso luogo: nome del luogo e indirizzo, puliti, con il comune."""
    town = _norm(ev.town)
    keys = []
    venue = _norm(PAREN_RE.sub("", ev.venue or ""))
    venue = re.sub(rf"\b{re.escape(town)}\b", "", venue).strip() if town else venue
    if venue not in GENERIC and len(venue) >= 4:
        keys.append(f"v|{venue}|{town}")
    address = _norm(INITIALS_RE.sub("", ev.address or ""))
    address = re.sub(rf"\b{re.escape(town)}\b|\b\d{{5}}\b|\btv\b|\btreviso\b", "", address).strip()
    if re.search(r"\d", address) and len(address) >= 6:          # solo indirizzi con numero civico
        keys.append(f"a|{address}|{town}")
    return keys


def _label(ev: Event) -> str:
    return ", ".join(x for x in (ev.venue, ev.address, ev.town) if x)


def _center(points: list[tuple[float, float]]) -> tuple[float, float]:
    return median(p[0] for p in points), median(p[1] for p in points)


def check(events: Iterable[Event], centers: dict | None = None, apply: bool = True) -> dict:
    """Controlla (e se `apply` allinea) le posizioni. Ritorna il rapporto da scrivere in ops/posizioni.json."""
    events = [e for e in events if e.lat is not None and e.lon is not None]
    centers = centers or {}
    known = load_known_places()

    anchors: dict[str, list[Event]] = defaultdict(list)
    for ev in events:
        if ev.geo_precision in ANCHORS:
            for k in place_keys(ev):
                anchors[k].append(ev)

    # luoghi con punto coerente / con punti diversi
    good: dict[str, tuple[float, float]] = {}
    spread = []
    for k, evs in anchors.items():
        pts = [(e.lat, e.lon) for e in evs]
        c = _center(pts)
        far = [e for e in evs if km_between(c[0], c[1], e.lat, e.lon) > SPREAD_KM]
        if far and len(far) < len(evs):
            near = [e for e in evs if e not in far]
            c = _center([(e.lat, e.lon) for e in near])
        if not far or len(far) < len(evs) / 2:
            good[k] = c
        if far:
            spread.append({
                "luogo": _label(evs[0]), "eventi": len(evs),
                "punti": sorted({(round(e.lat, 4), round(e.lon, 4)) for e in evs}),
                "uid_fuori_posto": [e.uid for e in far][:10],
                "cosa_fare": "scegli il punto giusto e scrivilo in config/luoghi.yaml (vale per tutti gli eventi)",
            })

    # 1. allinea gli eventi con solo il comune
    aligned = []
    for ev in events:
        if ev.geo_precision != "town":
            continue
        for k in place_keys(ev):
            if k in good:
                lat, lon = good[k]
                if apply:
                    ev.lat, ev.lon, ev.geo_precision = lat, lon, "venue"
                aligned.append({"uid": ev.uid, "titolo": ev.title, "luogo": _label(ev),
                                "lat": round(lat, 5), "lon": round(lon, 5)})
                break

    # 2. lontani dal centro del comune
    far_town = defaultdict(list)
    for ev in events:
        c = centers.get((ev.town or "").strip().lower())
        if c and ev.geo_precision != "town":
            km = km_between(c[0], c[1], ev.lat, ev.lon)
            if km > FAR_KM:
                far_town[(_label(ev), round(km))].append(ev.uid)
    far_list = [{"luogo": lbl, "km_dal_centro": km, "eventi": len(u), "uid": u[:10],
                 "cosa_fare": "verifica il luogo: probabilmente e' in un altro comune o il comune e' sbagliato"}
                for (lbl, km), u in sorted(far_town.items(), key=lambda x: -len(x[1]))]

    # 3. luoghi con un nome ma senza punto
    missing = defaultdict(list)
    for ev in events:
        if ev.geo_precision == "town" and (ev.venue or ev.address):
            missing[_label(ev)].append(ev.uid)
    missing_list = [{"luogo": lbl, "eventi": len(u), "uid": u[:10],
                     "cosa_fare": "cerca il punto (sito del luogo, OpenStreetMap) e scrivilo in config/luoghi.yaml"}
                    for lbl, u in sorted(missing.items(), key=lambda x: -len(x[1]))]
    no_place = sum(1 for e in events if e.geo_precision == "town" and not (e.venue or e.address))

    # 4. candidati per config/luoghi.yaml
    def is_known(ev: Event) -> bool:
        text = f" {_norm(ev.venue)} {_norm(ev.address)} "
        return any(any(f" {n} " in text for n in p["names"]) for p in known)
    candidates = []
    for k, evs in anchors.items():
        if k in good and len(evs) >= CANDIDATE_MIN and k.startswith("v|") and not is_known(evs[0]):
            lat, lon = good[k]
            candidates.append({"nomi": [evs[0].venue], "comune": evs[0].town, "lat": round(lat, 5),
                               "lon": round(lon, 5), "eventi": len(evs)})
    candidates.sort(key=lambda d: -d["eventi"])

    return {
        "generato": datetime.now(ROME).isoformat(timespec="minutes"),
        "riepilogo": {
            "eventi_controllati": len(events),
            "allineati_in_automatico": len(aligned),
            "luoghi_con_punti_diversi": len(spread),
            "lontani_dal_comune": sum(d["eventi"] for d in far_list),
            "solo_comune_con_luogo": sum(d["eventi"] for d in missing_list),
            "solo_comune_senza_luogo": no_place,
            "candidati_luoghi_noti": len(candidates),
        },
        "punti_diversi": spread[:30],
        "lontani_dal_comune": far_list[:30],
        "senza_punto": missing_list[:40],
        "allineati": aligned[:60],
        "candidati_luoghi": candidates[:20],
    }


def flagged_uids(rep: dict) -> dict[str, str]:
    """uid -> motivo, per la coda di revisione."""
    out = {}
    for d in rep.get("punti_diversi", []):
        for u in d["uid_fuori_posto"]:
            out[u] = f"posizione diversa dagli altri eventi in {d['luogo']}: verifica il punto"
    return out


def write(rep: dict) -> None:
    OPS.mkdir(exist_ok=True)
    (OPS / "posizioni.json").write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
