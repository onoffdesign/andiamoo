# Andiamoo

Mappa pubblica degli eventi in provincia di Treviso: concerti, sagre, gare, mostre, mercatini, convegni.
Il PC fisso raccoglie gli eventi da fonti pubbliche, li fa leggere a un'AI locale (Ollama), li geolocalizza
con OpenStreetMap e pubblica il risultato su GitHub Pages. Costo: zero (al massimo un dominio).

```
 Fonti pubbliche ─┐
 Notizie (RSS)  ──┼─► PC fisso: raccolta ─► AI locale ─► geolocalizzazione ─► deduplica ─► events.json ─► GitHub Pages
 Bot Telegram  ───┤        (Python)        (Ollama)      (Nominatim/OSM)                   (git push)     (sito + mappa)
 Modulo Google ───┘
```

## Cosa c'e' nella cartella

| Cartella | Contenuto |
|---|---|
| `config/` | `sources.yaml` fonti, `categories.yaml` categorie e filtri, `settings.yaml` impostazioni |
| `pipeline/` | raccolta, AI, geocoding, deduplica, export, pubblicazione |
| `bot/` | bot Telegram per le segnalazioni (foto di locandine, link, testo) |
| `docs/` | il sito (pubblicato da GitHub Pages) e `docs/data/events.json` |
| `windows/` | installazione e attivita' pianificate sul PC fisso |
| `tests/` | test su campioni reali delle fonti |

## Installazione sul PC fisso (una volta)

1. Installa Git per Windows se manca, poi in PowerShell:
   ```
   cd $HOME\Documents
   git clone https://github.com/onoffdesign/andiamoo.git
   cd andiamoo
   powershell -ExecutionPolicy Bypass -File windows\setup.ps1
   ```
   Lo script installa Python, Ollama e il modello `gemma3:12b` (circa 8 GB), prepara l'ambiente
   e registra due attivita': la pipeline ogni 4 ore e il bot all'accesso.
2. Apri `.env` e compila: email di contatto, token del bot (da @BotFather), il tuo id Telegram (da @userinfobot).
3. Primo giro a mano: `windows\run_pipeline.bat`, poi guarda `logs\pipeline.log`.
   Al primo `git push` Windows chiede di accedere a GitHub: una volta sola.
4. Su GitHub: Settings > Pages > Deploy from a branch > `main` / `docs`.

Impostazioni consigliate per un PC sempre acceso: risparmio energia "mai sospendere", accesso automatico
all'avvio (cosi' parte anche il bot), aggiornamenti di Windows fuori dalle ore notturne di lavoro.

## Giro notturno: AI locale + Claude

| Ora (Italia) | Dove | Cosa |
|---|---|---|
| 01:00 | PC fisso, attivita' `Andiamoo-Pipeline` | aggiorna il codice, avvia Ollama se serve, raccoglie tutte le fonti, l'AI locale (`gemma3:12b`) estrae, classifica e riassume, cerca i luoghi, geolocalizza, deduplica, applica le correzioni della redazione, pubblica il sito e lascia in `ops/` il rapporto (`rapporto.json`), la coda di revisione (`revisione.json`) e le scoperte (`scoperte.csv`) |
| 03:37 | Claude nel cloud (attivita' pianificata, piano attuale) | legge rapporto e coda, sistema le fonti in errore, verifica sul web fino a 40 eventi dubbi, scrive correzioni e rimozioni (`config/correzioni.yaml`), cerca categoria per categoria, nei siti dei 94 comuni, negli aggregatori e nelle notizie tutti gli eventi mancanti e li aggiunge senza limite (`config/eventi_redazione.yaml`, copertura in `ops/copertura.yaml`) e nuove fonti, pubblica subito le correzioni e annota tutto in `ops/registro-redazione.md` |
| 07:30 | PC fisso, attivita' `Andiamoo-Resoconto` | si risveglia, manda su Telegram il resoconto della notte (eventi sul sito, nuovi, aggiunti / corretti / rimossi da Claude, fonti con problemi) e torna in ibernazione |
| 01:00 notte dopo | PC fisso | riprende correzioni ed eventi della redazione: geolocalizza i nuovi luoghi e indirizzi |

Le istruzioni della revisione sono in `ops/revisione-notturna.md`: per cambiare cosa fa Claude ogni notte basta
modificare quel file. Ogni correzione e' una riga in `config/correzioni.yaml`: si annulla cancellandola.

## PC fisso: si sveglia, lavora e si iberna da solo

Da PowerShell **come amministratore**, nella cartella del progetto:
```
powershell -ExecutionPolicy Bypass -File windows\reset_automazioni.ps1   # elenca, salva e toglie le vecchie automazioni
powershell -ExecutionPolicy Bypass -File windows\imposta_notte.ps1       # risveglio alle 01:00 e ibernazione a fine giro
```
- `reset_automazioni.ps1` mostra programmi all'avvio, attivita' pianificate e accesso automatico in una finestra:
  si sceglie cosa eliminare. Prima fa una copia di sicurezza in `Documenti\backup-automazioni-<data>`.
  Le attivita' di Windows e quelle di ANDIAMO? non compaiono.
- `imposta_notte.ps1` attiva ibernazione e timer di risveglio, fa ibernare il tasto di accensione e registra il giro
  delle 01:00 e il resoconto delle 07:30 in modo che partano **anche senza accesso a Windows** (schermata "Accedi"),
  senza password (modalita' S4U). Per GitHub usa una chiave dedicata al progetto (`chiave_github.ps1`), perche'
  senza accesso Windows non sblocca le credenziali salvate. Alla fine fa una prova (`prova_notte.bat`) nella stessa
  modalita' della notte. Se la prova non parte: `-ConPassword` (Windows chiede la password dell'account). A fine giro il PC
  si iberna, a meno che sia in uso.
- La sera il PC va **ibernato** (tasto di accensione o Start > Arresta > Iberna), non spento del tutto: da spento
  Windows non puo' riaccenderlo. Per l'accensione da spento serve l'opzione del BIOS "Power On by RTC", se c'e'.

## "Aggiungi evento" e "Segnala" dal sito (API sul PC)

Il sito e' statico: per leggere link e screenshot con l'AI chiama una piccola API che gira sul PC accanto
a Ollama (`windows\run_api.bat`, registrata come attivita' `Andiamoo-API`). L'API ascolta solo su
`127.0.0.1:8787`; per renderla raggiungibile dal sito si usa **Cloudflare Tunnel** (gratis, nessuna porta
da aprire sul router).

**Automatico (nessun account, nessun dominio)**: `setup.ps1` installa cloudflared e registra le attivita'
`Andiamoo-API` e `Andiamoo-Tunnel`, che partono a ogni accesso. Il tunnel ottiene da Cloudflare un indirizzo
`https://....trycloudflare.com`, lo salva in `data\api_url.txt` e ripubblica il sito: dopo un paio di minuti
"Aggiungi evento" legge link e screenshot con l'AI del PC. L'indirizzo cambia a ogni riavvio del PC, ma lo
script ripubblica da solo quello nuovo (log in `logs\tunnel.log`). Se il PC e' spento il sito torna da solo
alla compilazione a mano.

**Indirizzo fisso** (piu' affidabile, quando il dominio andiamoo.ai e' su Cloudflare):
```
cloudflared tunnel login
cloudflared tunnel create andiamo
cloudflared tunnel route dns andiamo api.andiamoo.ai
cloudflared tunnel run --url http://localhost:8787 andiamo
```
Poi in `config/settings.yaml` metti `site.api_url: "https://api.andiamoo.ai"` (il tunnel rapido si disattiva da
solo) e, se il sito gira su un dominio diverso da `site.base_url`, aggiungilo in `api.allowed_origins`.

Finche' `api_url` e' vuoto il modulo "Aggiungi evento" resta compilabile a mano e invia via email
(se `contact_email` e' impostato). L'API ha limiti per indirizzo (20 letture, 10 invii, 10 segnalazioni
all'ora), un campo trappola anti-spam, e ogni evento arriva sul bot Telegram in attesa di approvazione.

## Uso quotidiano

- **Segnalazioni**: arrivano sul bot Telegram. Tocchi ✅ per pubblicare o ❌ per scartare.
  Se manca la posizione: `/luogo <id> Via Roma 1, Treviso`.
- **Profili Instagram/Facebook**: `/profili` nel bot elenca quelli da tenere d'occhio. Non vengono letti
  in automatico; quando vedi un evento nuovo inoltri lo screenshot della locandina al bot.
- **Stato**: `/stato` nel bot mostra l'ultimo giro e le fonti con errori.
- **Scoperte**: `data/scoperte.csv` elenca i siti ufficiali trovati negli eventi dei grandi portali.
  Quelli frequenti vanno aggiunti in `config/sources.yaml` come fonti dirette: col tempo il catalogo
  si sposta dai portali ai singoli organizzatori.

## Regole che il codice applica

- **robots.txt rispettato** e una richiesta ogni 2 secondi per sito, con user agent dichiarato e contatto.
- **Niente aggiramenti**: siti con protezioni anti-bot (es. Vivaticket) o vietati (Instagram, Facebook) non si raccolgono.
- **Portali solo come scoperta**: Eventbrite, TicketOne, eventiesagre, 2night e insolitotrantran hanno un tetto
  di 40 eventi a giro. Nei doppioni vince la fonte diretta.
- **Testi**: l'AI scrive un riassunto neutro di 1-2 frasi ("L'evento prevede..."), senza aggettivi promozionali.
  Le fonti che non lo consentono (`ai_rewrite: false`, es. DICE, calendariopodismo) mostrano solo i dati e il link.
  Senza AI non si pubblica nessun riassunto: mai testo copiato.
- **Link d'azione**: ogni scheda dice "Dettagli riassunti tramite AI. Per il programma ufficiale e le iscrizioni,
  visita il sito ufficiale" e porta al sito dell'organizzatore (o alla biglietteria, o alla fonte).
- **Dati personali**: email e telefoni vengono tolti prima dell'AI; nessuna immagine viene copiata o ospitata.
- **Rimozione**: ogni scheda ha il link per chiedere correzione o rimozione.
- **Luoghi**: se un evento ha solo il comune, la pipeline cerca il luogo esatto nel testo, nella pagina
  dell'evento e nelle pagine collegate della stessa fonte (scheda del luogo, link a Google Maps), al massimo
  80 pagine in piu' a giro e sempre con le regole sopra. Un luogo trovato a piu' di 8 km dal comune viene scartato.
  Se non si trova nulla l'evento resta nel comune, spostato a caso di qualche centinaio di metri dal centro
  perche' i segnaposti non si sovrappongano ("posizione indicativa" nella scheda).

## Comandi utili

```
.venv\Scripts\python -m pipeline.run                          giro completo e pubblicazione
.venv\Scripts\python -m pipeline.run --source eventbrite --no-publish   prova una fonte
.venv\Scripts\python -m pipeline.run --llm rules             senza AI (piu' veloce, niente riassunti)
.venv\Scripts\python -m pipeline.run --export-only           rigenera il sito dall'archivio
.venv\Scripts\python -m pytest -q tests                      test
```

## Modifiche al sito

Il sito e' in `docs/` (HTML, CSS, JS senza build). Quando cambi `style.css` o `app.js`, aumenta il numero
`?v=` nei due link dentro `docs/index.html`: altrimenti i browser possono tenere in cache la versione vecchia.

## Fonti da aggiungere (da verificare una per una)

Pro Loco della Marca (UNPLI Treviso) e "Delizie d'Autunno", Musei Civici di Treviso, Teatro Comunale
Mario Del Monaco, Teatro del Pane, H-FARM, FabLab Treviso, open data turismo della Regione Veneto,
altri comuni con MyPortal (stesso raccoglitore del Comune di Treviso: cambiano indirizzo e codice IPA),
squadre (Treviso Basket, Imoco Volley, Benetton Rugby). Per ognuna: controllare robots.txt e se offre
dati strutturati (JSON-LD, RSS, iCal, API), poi aggiungerla in `config/sources.yaml`.

Non e' una consulenza legale: prima del lancio pubblico conviene una verifica con un legale su banche dati e diritto d'autore.
