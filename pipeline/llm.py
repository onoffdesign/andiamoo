"""AI locale con Ollama (output JSON vincolato da schema) + alternativa a regole.

Tre compiti:
  enrich()          completa un evento gia' strutturato: riassunto, categoria, accesso, indirizzo
  extract_events()  trova eventi dentro un testo libero (articolo, post, messaggio)
  extract_from_image()  legge una locandina
"""
from __future__ import annotations

import base64
import hashlib
import json
import logging
import re
from typing import Optional

import httpx

from . import categories as cats
from .config import settings
from .store import Store
from .textutil import strip_personal_data, today_rome

log = logging.getLogger(__name__)

# ---------------------------------------------------------------- schemi JSON

def _event_props() -> dict:
    return {
        "title": {"type": "string"},
        "start": {"type": "string", "description": "YYYY-MM-DD oppure YYYY-MM-DDTHH:MM, ora locale"},
        "end": {"type": "string", "description": "come start, vuoto se non indicato"},
        "summary": {"type": "string", "description": "max 2 frasi, scritte da te, niente contatti personali"},
        "category": {"type": "string", "enum": cats.category_ids()},
        "subcategory": {"type": "string"},
        "access": {"type": "string", "enum": cats.access_ids()},
        "price": {"type": "string"},
        "venue": {"type": "string", "description": "nome del luogo/locale"},
        "address": {"type": "string", "description": "via e numero, se presenti nel testo"},
        "town": {"type": "string", "description": "comune"},
        "province": {"type": "string", "description": "sigla provincia, es. TV, VE"},
        "ticket_url": {"type": "string"},
        "official_url": {"type": "string", "description": "sito ufficiale dell'evento o dell'organizzatore, se nel testo"},
        "audience": {"type": "array", "items": {"type": "string", "enum": cats.audience_ids()},
                     "description": "solo se il testo indica esplicitamente il pubblico"},
        "setting": {"type": "string", "enum": cats.setting_ids() + [""], "description": "al chiuso / all'aperto, vuoto se non detto"},
    }


KIND_PROPS = {
    "tipo": {"type": "string", "enum": ["evento", "ricorrente", "non_evento"],
             "description": "evento = una singola iniziativa con data e luogo precisi (anche su piu' giorni, es. una mostra "
                            "o una sagra di un weekend); ricorrente = la stessa iniziativa si ripete in date diverse "
                            "(es. mercatino ogni terza domenica del mese); non_evento = calendario, elenco o raccolta di "
                            "tanti eventi, pagina di un portale, guida, notizia generica senza un evento preciso"},
    "ricorrenza": {
        "type": "object",
        "description": "solo se tipo = ricorrente, ricavata dal testo; altrimenti valori vuoti",
        "properties": {
            "frequenza": {"type": "string", "enum": ["settimanale", "mensile", "date_elencate", "sconosciuta"]},
            "giorno_settimana": {"type": "string", "enum": ["lunedi", "martedi", "mercoledi", "giovedi", "venerdi",
                                                           "sabato", "domenica", ""]},
            "settimana_del_mese": {"type": "integer", "description": "1-4 = prima..quarta, -1 = ultima, 0 = tutte"},
            "date_elencate": {"type": "array", "items": {"type": "string"}, "description": "AAAA-MM-GG, se il testo le elenca"},
        },
    },
}

ENRICH_SCHEMA = {
    "type": "object",
    "properties": {**{k: v for k, v in _event_props().items() if k not in ("title", "start", "end")}, **KIND_PROPS},
    "required": ["summary", "category", "subcategory", "access", "venue", "address", "town", "province", "tipo"],
}

EXTRACT_SCHEMA = {
    "type": "object",
    "properties": {
        "events": {
            "type": "array",
            "items": {"type": "object", "properties": _event_props(),
                      "required": ["title", "start", "category", "town", "province", "summary", "access"]},
        }
    },
    "required": ["events"],
}

PLACE_SCHEMA = {
    "type": "object",
    "properties": {"venue": {"type": "string"}, "address": {"type": "string"}, "town": {"type": "string"}},
    "required": ["venue", "address", "town"],
}

SYSTEM = """Estrai e schematizzi dati di eventi in provincia di Treviso per una mappa pubblica.
Regole:
- Usa solo informazioni presenti nel testo. Se un dato manca lascia la stringa vuota. Non dedurre, non inventare.
- Il riassunto e' neutro, schematico e puramente informativo: massimo 2 frasi brevi, che dicono COSA prevede l'evento.
  Stile: "L'evento prevede una degustazione di vini locali e musica dal vivo." / "Gara podistica non competitiva su 6 e 12 km."
  Vietati aggettivi promozionali o emotivi (imperdibile, magico, spumeggiante, unico...), metafore, battute, inviti all'azione.
  Non copiare frasi dal testo: riformula in modo asciutto.
- Non riportare mai numeri di telefono, email o nomi di persone private. Nomi di artisti, relatori, squadre e organizzazioni vanno bene.
- Categorie ammesse (id = nome: sottocategorie):
{catalog}
- access: libero (ingresso gratuito), offerta (offerta libera), biglietto (a pagamento), iscrizione (prenotazione/registrazione richiesta), invito (evento privato o aziendale su invito), sconosciuto.
- Oggi e' {today}. Le date relative ("sabato prossimo") vanno convertite in date assolute."""


def _system() -> str:
    return SYSTEM.format(catalog=cats.prompt_catalog(), today=today_rome().isoformat())


# ---------------------------------------------------------------- backend

class OllamaLLM:
    name = "ollama"

    def __init__(self, store: Store):
        cfg = settings()["llm"]
        self.store = store
        self.host = cfg["host"].rstrip("/")
        self.text_model = cfg["text_model"]
        self.vision_model = cfg["vision_model"]
        self.temperature = cfg["temperature"]
        self.client = httpx.Client(timeout=cfg["timeout_seconds"])
        self.calls = 0

    def available(self) -> bool:
        try:
            r = self.client.get(self.host + "/api/tags", timeout=5)
            names = {m["name"] for m in r.json().get("models", [])}
            return self.text_model in names or self.text_model + ":latest" in names
        except (httpx.HTTPError, ValueError):
            return False

    def _chat(self, user: str, schema: dict, images: Optional[list[bytes]] = None, model: Optional[str] = None) -> dict:
        model = model or self.text_model
        key = hashlib.sha1(json.dumps([model, user, schema, [hashlib.sha1(i).hexdigest() for i in images or []]],
                                      sort_keys=True).encode()).hexdigest()
        cached = self.store.ai_get(key)
        if cached is not None:
            return cached
        msg = {"role": "user", "content": user}
        if images:
            msg["images"] = [base64.b64encode(i).decode() for i in images]
        payload = {
            "model": model,
            "messages": [{"role": "system", "content": _system()}, msg],
            "format": schema,
            "stream": False,
            # tetto alla risposta: senza, su alcuni testi il modello ripete all'infinito e va in timeout
            "options": {"temperature": self.temperature, "num_predict": 1500 if schema is EXTRACT_SCHEMA else 600,
                        "num_ctx": 8192, "repeat_penalty": 1.15},
            "keep_alive": "30m",          # il modello resta caricato sulla GPU per tutto il giro
        }
        self.calls += 1
        r = self.client.post(self.host + "/api/chat", json=payload)
        r.raise_for_status()
        content = r.json()["message"]["content"]
        try:
            result = json.loads(content)
        except json.JSONDecodeError:
            m = re.search(r"\{.*\}", content, re.S)
            result = json.loads(m.group(0)) if m else {}
        self.store.ai_put(key, result)
        return result

    def warm_up(self) -> None:
        """Carica il modello sulla GPU prima del giro: il primo caricamento puo' richiedere minuti."""
        try:
            self.client.post(self.host + "/api/generate", json={"model": self.text_model, "prompt": "", "keep_alive": "30m"},
                             timeout=600)
        except httpx.HTTPError as e:
            log.warning("Caricamento del modello non riuscito: %s", e)

    def enrich(self, known: dict, text: str) -> dict:
        user = ("Completa i dati di questo evento. Dati gia' noti (affidabili):\n"
                + json.dumps(known, ensure_ascii=False)
                + "\n\nTesto della pagina:\n" + strip_personal_data(text)[:6000])
        return self._chat(user, ENRICH_SCHEMA)

    def extract_events(self, text: str, hint: str = "") -> list[dict]:
        user = ("Trova gli eventi pubblici FUTURI descritti in questo testo (concerti, sagre, gare, mostre, convegni, "
                "eventi aziendali...). Se il testo e' cronaca, polemica o un evento gia' concluso, restituisci events vuoto.\n"
                f"{hint}\n\nTESTO:\n" + strip_personal_data(text)[:8000])
        return self._chat(user, EXTRACT_SCHEMA).get("events", [])

    def extract_place(self, title: str, text: str) -> dict:
        user = (f"Dove si svolge l'evento \"{title}\"? Riporta nome del luogo, via con numero civico e comune "
                "solo se scritti nel testo. Se non ci sono, stringhe vuote.\n\nTESTO:\n" + strip_personal_data(text)[:6000])
        return self._chat(user, PLACE_SCHEMA)

    def extract_from_image(self, image: bytes, caption: str = "") -> list[dict]:
        user = ("Questa e' la locandina o lo screenshot di un evento. Leggi titolo, data, orario, luogo, prezzo. "
                + (f"Didascalia del messaggio: {caption}" if caption else ""))
        return self._chat(user, EXTRACT_SCHEMA, images=[image], model=self.vision_model).get("events", [])


ADDRESS_RE = re.compile(
    r"((?:Via|Viale|Piazza|Piazzale|Borgo|Vicolo|Corso|Strada|Largo|Riviera|Contrada|Calle)\s+[^,\n]{2,60}?,?\s*\d{0,4}[a-zA-Z]?)\s*,\s*([A-Z][\w' àèéìòù]+?)(?:\s*\(|\n|$|,|<)",
)


class RulesLLM:
    """Nessuna AI: classificazione a parole chiave e indirizzi con espressioni regolari.
    Serve per i test e come riserva se Ollama non risponde. Non estrae eventi da testo libero."""
    name = "rules"
    calls = 0

    def __init__(self, store: Store | None = None):
        pass

    def available(self) -> bool:
        return True

    def enrich(self, known: dict, text: str) -> dict:
        blob = f"{known.get('title', '')}\n{text}"
        cat, sub = cats.classify_rules(blob)
        out = {"category": cat or "", "subcategory": sub or "", "access": cats.access_rules(blob),
               "summary": "", "venue": "", "address": "", "town": "", "province": "", "price": ""}
        m = ADDRESS_RE.search(text)
        if m:
            out["address"], out["town"] = m.group(1).strip(" ,"), m.group(2).strip()
        # Senza AI non scriviamo riassunti (copiare il testo della fonte non e' ammesso): resta il link.
        return out

    def extract_events(self, text: str, hint: str = "") -> list[dict]:
        return []

    def extract_from_image(self, image: bytes, caption: str = "") -> list[dict]:
        return []


def make_llm(store: Store, backend: Optional[str] = None):
    backend = backend or settings()["llm"]["backend"]
    if backend == "ollama":
        llm = OllamaLLM(store)
        if llm.available():
            llm.warm_up()
            return llm
        log.warning("Ollama non raggiungibile o modello %s non scaricato: uso le regole.", llm.text_model)
    return RulesLLM(store)
