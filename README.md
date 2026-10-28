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
