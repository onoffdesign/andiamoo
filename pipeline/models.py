"""Modello dati di un evento."""
from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass, field
from typing import Optional


@dataclass
class Event:
    # Provenienza
    source: str                      # id della fonte (config/sources.yaml)
    source_name: str
    source_url: str                  # pagina dell'evento sulla fonte
    # Contenuto
    title: str
    start: Optional[str] = None      # ISO locale Europe/Rome, "2026-10-29" o "2026-10-29T20:30"
    end: Optional[str] = None
    all_day: bool = False
    summary: str = ""                # testo breve riscritto (mai copiato integralmente)
    category: Optional[str] = None
    subcategory: Optional[str] = None
    tags: list[str] = field(default_factory=list)
    access: str = "sconosciuto"      # libero | offerta | biglietto | iscrizione | invito | sconosciuto
    audience: list[str] = field(default_factory=list)   # famiglie | giovani | senior | animali
    setting: str = ""                # al-chiuso | all-aperto | "" (non detto)
    price: str = ""
    ticket_url: str = ""             # link per biglietti/iscrizione, se diverso dalla fonte
    official_url: str = ""           # sito ufficiale dell'evento/organizzatore: e' il link d'azione
    ai_summary: bool = False         # True se il riassunto e' stato scritto dall'AI (mostra la nota)
    # Luogo
    venue: str = ""
    address: str = ""
    town: str = ""
    lat: Optional[float] = None
    lon: Optional[float] = None
    geo_precision: str = ""          # source | address | venue | town
    # Gestione
    status: str = "published"        # published | pending | rejected
    also_on: list[dict] = field(default_factory=list)   # altre fonti dello stesso evento
    raw_text: str = ""               # testo grezzo per l'AI; non viene esportato
    ai_allowed: bool = True          # la fonte consente riscrittura AI?
    needs_ai: bool = True            # mancano dati che solo l'AI puo' ricavare?
    submitted_by: str = ""           # per segnalazioni: id chat Telegram o "modulo"

    @property
    def uid(self) -> str:
        """Identificativo stabile: fonte + URL + data + titolo (piu' eventi possono stare sulla stessa pagina)."""
        override = self.__dict__.get("uid_override")      # correzioni della redazione: l'uid pubblicato non cambia
        if override:
            return override
        title = " ".join(self.title.lower().split())
        key = f"{self.source}|{self.source_url}|{(self.start or '')[:10]}|{title}"
        return hashlib.sha1(key.encode("utf-8")).hexdigest()[:16]

    def to_dict(self) -> dict:
        d = asdict(self)
        d["uid"] = self.uid
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "Event":
        allowed = {k for k in cls.__dataclass_fields__}
        return cls(**{k: v for k, v in d.items() if k in allowed})

    def public_dict(self) -> dict:
        """Campi esportati sul sito (niente testo grezzo, niente dati interni)."""
        d = self.to_dict()
        for k in ("raw_text", "ai_allowed", "needs_ai", "submitted_by", "status"):
            d.pop(k, None)
        return d
