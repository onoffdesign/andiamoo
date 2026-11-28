# Agente giro, notte del 2026-11-28 (secondo giro)

(Riscritto da capo. Il primo giro di stanotte aveva letto le 39 fonti allora in elenco e aggiunto 61 eventi, gia'
uniti dal coordinatore; questo giro ha letto le due fonti mai lette, rifatto le 12 verifiche e riaperto via API le
fonti che WebFetch non leggeva.)

## Numeri
- Eventi aggiunti in config/notte/giro-eventi.yaml: 98 (`python -m pipeline.notte --controlla giro`: parti valide).
  - Dolomiti Prealpi (BL): 31 dall'API piu' 6 spettacoli della stagione La Sena Viva di Feltre (titoli dalla notizia
    del Teatro Stabile del Veneto, date dall'API; orario non pubblicato, evento solo con la data).
  - Gli Alcuni: 23 (percorsi al Parco degli Alberi Parlanti fino al 28/12 e spettacoli a Sacile, Padova, San Lorenzo
    Isontino, Desenzano, Milano; escluse le repliche per le scuole e Social Paradiso, per le secondarie).
  - Museo Canova (Possagno): 14 visite guidate speciali nei prossimi 30 giorni (LIS, famiglie, Domenica in mostra,
    Natale al Museo, Napoleone). Non messe le visite "spontanee" e quelle in inglese.
  - Sala Luttazzi (Trieste): 7 (le altre 20 c'erano gia').
  - Nautilus Cantiere Teatrale: 7 date in tournee (Creazzo, Longare, Dueville, Montichiari, San Giorgio Bigarello,
    Vicenza, Sovizzo), prima tralasciate perche' fuori area.
  - Fondazione Benetton: 2 (1/12 Palazzo Bomben, 3/12 a Trento). Fiori d'Inverno: 2 (PrimaVera in Festa a Roncade,
    14 e 21/3).
- Correzioni: 0 (config/notte/giro-correzioni.yaml non creato; vedi sotto le richieste per eventi_redazione).
- Fonti del giro lette: 2 nuove (dolomiti-prealpi, sala-luttazzi-trieste, data in copertura.yaml) piu' 11 riaperte
  via API o curl (comune-treviso, comune-mogliano, comune-paese, comune-spresiano, comune-trevignano, fondazione-benetton,
  gli-alcuni, museo-canova, nautilus-teatro, visit-fregona, qdpnews). Le altre erano gia' state lette oggi.
- Verifiche fonti: 2 ammesse, 3 vietate, 7 restano da verificare.
- Ricerche usate: 90 su 125 (17 WebSearch, 10 WebFetch, 63 letture con curl di API e pagine ufficiali, robots.txt
  e Nominatim, contate una per chiamata).

## Verifiche delle fonti (config/fonti-vietate.yaml)
- **trevisoeventi.com -> ammesse** (26 eventi trattenuti): robots.txt assente (404), /newsletter-informativa-privacy.htm
  letta: nessun divieto; termini d'uso non esistono; nel footer "riproduzione vietata senza autorizzazione".
- **iltaccodibacco.it -> ammesse** (2): robots.txt senza Disallow, /condizioni/ letta: nessun divieto di raccolta
  automatica (solo "uso personale e non commerciale"); il sito offre una OpenAPI.
- **umbriaecultura.it -> vietate** (13): /termini-e-condizioni/ sez. 7 vieta "qualsiasi attivita' di raccolta dati
  sistematica o automatizzata".
- **fleamapket.com -> vietate** (2): /terms-of-service/ vieta "page-scrape, spider, robot, crawl ... or other automatic devices".
- **cosedicasa.com -> vietate** (1): /condizioni-uso vieta "l'estrazione e il reimpiego ... del contenuto" e l'accesso
  "con mezzi diversi dalla normale connessione".
- Restano da verificare: ticketone.it (robots.txt irraggiungibile, termini 503; secondo il riassunto di WebSearch i
  termini di aprile 2026 vietano gli strumenti automatizzati, da confermare), classicalive.it (informativa non trovata),
  insolitotrantran.it, running.life, tviweb.it (nessuna pagina legale trovata), eventiesagre.it (indirizzo delle
  Condizioni di Utilizzo sconosciuto), trevisando.it (robots.txt e privacy dietro controllo anti-bot).

## Da fare per il coordinatore (file che non posso toccare)
- I 13 eventi di eventi_redazione.yaml con fonte umbriaecultura.it (feste del radicchio) hanno gia' official_url su
  fioridinverno.tv, sito ufficiale UNPLI (robots.txt libero, letto stanotte). Confermati dalla home di fioridinverno.tv
  del 2026-11-28 e da ripubblicare cambiando solo `fonte` in "https://www.fioridinverno.tv/ (letta il 2026-11-28)":
  Paderno 20-29/11, Spresiano 27-29/11, Quinto 3-8/12, Preganziol 8-10/1, Zero Branco 15-24/1 (tutte e due le voci),
  Treviso 16-17/1, Mogliano 13-14/2, Vedelago 20-21/2. **Castelfranco**: il sito ufficiale dice 10-13/12, non 6-13/12:
  correggere start in 2026-12-10. **Dosson (Casier)**, tre fine settimana: non c'e' nell'elenco di fioridinverno.tv,
  restano trattenuti finche' non si trova la Pro Loco.
- ops/fonti.yaml: la voce di umbriaecultura (riga circa 1000) va segnata vietata; la voce di trevisoeventi ora e' ammessa.
- Gli eventi trattenuti da trevisoeventi.com e iltaccodibacco.it dovrebbero tornare pubblicabili da soli con la
  prossima `pipeline.pubblica`.

## Fonti del giro: esito
- dolomiti-prealpi: API tribe ok (148 eventi in 120 giorni, 3 pagine). 34 c'erano gia' (Belluno e Ponte nelle Alpi);
  le schede non hanno luogo ne' orario nei campi, solo nel testo. Saltati per dati incompleti o in conflitto: Natale nel
  Borgo a Mel (date a blocchi), Rassegna Rasai (titoli assenti), Mondovisioni (luogo assente), Lo Schiaccianoci 28/12,
  Trio Mythos, Raices al viento, Concerto di Natale con il Banco del Mutuo Soccorso, Katia Follesa (testo: 5 marzo,
  API: 5-27 febbraio), Attenti al libro (testo: ottobre, API: gennaio-marzo), Eventi Pro Loco di Fonzaso (nessun dettaglio).
- sala-luttazzi-trieste: API ok, 27 eventi, 7 nuovi.
- comune-treviso (MyPortal via API con curl): 11 eventi futuri, tutti gia' sul sito tranne la giostra (attrazione,
  non evento) e un webinar online. comune-spresiano: solo la Festa del Radicchio (gia' presente) e progetti annuali.
  comune-mogliano e comune-trevignano: 0 eventi futuri nell'API. comune-paese: l'API risponde con 0 contenuti anche
  senza filtro: nota in config/sources.yaml (codice IPA forse sbagliato o eventi non su MyPortal).
- fondazione-benetton: /agenda-home/ reindirizza a https://fbsr.it/eventi/, leggibile con curl: indirizzo corretto in
  config/sources.yaml.
- gli-alcuni: la prima pagina dell'API va; la seconda e la terza ricevono una pagina anti-bot ("One moment, please"):
  date dal 7 gennaio in poi da leggere un'altra notte. Nota in config/sources.yaml.
- museo-canova: API ok dal cloud, descrizioni vuote. Nota in config/sources.yaml.
- visit-fregona: API con 0 eventi futuri. qdpnews: il feed di oggi ha solo cronaca.

## Fonti nuove da catalogare
- **Fiori d'Inverno** | https://www.fioridinverno.tv/ | elenco di tutte le feste del radicchio con le date in home e
  schede /eventi/<slug>/ | rassegna UNPLI Treviso (pro loco) | query: nessuna, leggere la home | robots.txt libero.
- **Teatro Stabile del Veneto, notizie** | https://www.teatrostabileveneto.it/news-tsv/ | programmi delle stagioni dei
  teatri del circuito (es. La Sena Viva di Feltre) | teatro | query: "Teatro Stabile del Veneto <teatro> <mese> 2026"
  con allowed_domains [teatrostabileveneto.it].
- **Visit Dolomiti Bellunesi** | https://www.visitdolomitibellunesi.com/ | eventi del Bellunese (ufficio turistico,
  uscito in una ricerca, non aperto) | da provare come fonte BL.

## Lezioni
- Per le fonti con API (The Events Calendar, MyPortal) curl e' molto meglio di WebFetch: JSON completo in una
  chiamata, i comuni MyPortal che a WebFetch mostrano solo "MyPortal" si leggono cosi'. Gli orari MyPortal sono in UTC:
  convertire con `pipeline.textutil.to_local_iso`.
- Con il controllo dei doppioni conviene un confronto automatico (stessa data e meta' delle parole del titolo) tra
  l'API e docs/data/events.json + eventi_redazione.yaml: ha trovato 50 date mancanti di Gli Alcuni, Canova e Nautilus.
- Comuni nati da fusioni (Borgo Valbelluna) non sono in config/comuni.csv: servono lat e lon in ogni evento.
- Per i termini: WebSearch con allowed_domains trova l'URL giusto in 4 casi su 12; quando non lo trova, indovinare
  l'indirizzo fallisce quasi sempre.

## Problemi
- Anti-bot su live.alcuni.it e trevisando.it dopo poche richieste; ticketone.it irraggiungibile (503).
- Sala Guarnieri (Pedavena), Museo Secco (Seren del Grappa), Centro Sociale di Tambre e TSM di Trento non sono su
  OpenStreetMap: eventi lasciati sul centro del comune (paesi piccoli) o su Trento.
