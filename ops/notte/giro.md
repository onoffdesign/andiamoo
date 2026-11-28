# Agente giro, notte del 2026-11-28

(Riscritto da capo: il tentativo precedente di stanotte era fallito perche' WebFetch era bloccato.)

## Numeri
- Eventi aggiunti in config/notte/giro-eventi.yaml: 61 (`python -m pipeline.notte --controlla giro`: parti valide).
- Correzioni: 0 (config/notte/giro-correzioni.yaml non creato).
- Fonti del giro lette: 39 su 39 elencate dal piano (il piano ne elenca 39, non 40); data 2026-11-28 scritta in
  ops/copertura.yaml, sezione `giro`.
- Verifiche fonti: 2 ammesse (happyticket.com, itinerarinellarte.it), 2 vietate (calendariopodismo.it, trovasagre.com),
  8 restano da verificare.
- Ricerche usate: 108 su 125 (12 WebSearch, 96 WebFetch).

## Verifiche delle fonti (config/fonti-vietate.yaml)
- **happyticket.com -> ammesse**: robots.txt (blocca solo /backend/) e /assistenza.htm (Condizioni Generali, agg.
  10/06/2026): nessun divieto di scraping o estrazione automatica; nel footer solo "vietata la riproduzione".
- **itinerarinellarte.it -> ammesse**: robots.txt (blocca solo /script/ e le pagine di ricerca) e /it/privacy: nessun
  divieto; termini d'uso non presenti. Nota: secondo WebSearch le pagine del magazine riservano la riproduzione dei
  testi (niente testi copiati, che vale comunque).
- **calendariopodismo.it -> vietate**: robots.txt con gruppi ClaudeBot e anthropic-ai `Disallow: /` (e
  Content-Signal ai-train=no).
- **trovasagre.com -> vietate**: robots.txt `User-agent: ClaudeBot` `Disallow: /` (anche anthropic-ai, GPTBot, CCBot).
- Restano in `da_verificare` (pagine dei termini non trovate o non leggibili):
  - trevisoeventi.com: robots.txt 404 (nessun blocco), /privacy-policy/ e /privacy 404, WebSearch non trova pagine legali.
  - ticketone.it: robots.txt e /help/terms/ rispondono 503 (protezione o sito sovraccarico): da riprovare.
  - umbriaecultura.it: robots.txt libero (solo /wp-admin/), /privacy-policy/ 404.
  - classicalive.it: robots.txt `Allow: /`, /privacy-policy/ 404.
  - running.life: robots.txt blocca solo /map/; pagina dei termini non trovata.
  - tviweb.it: robots.txt libero; nessuna pagina legale trovata (solo footer con copyright Tviweb S.R.L.).
  - eventiesagre.it: robots.txt `Allow: /` per tutti; la pagina "Condizioni di Utilizzo" esiste (link nel footer secondo
    WebSearch) ma non ne conosco l'indirizzo; WebSearch riporta anche "riproduzione anche parziale vietata".
  - insolitotrantran.it (anche in domini-illeggibili): robots.txt consente tutto, ClaudeBot compreso; termini non trovati.
  Lezione: indovinare /privacy-policy/ costa una lettura a vuoto quasi sempre; meglio WebSearch con
  `allowed_domains` sul dominio per trovare l'URL della pagina legale e poi una sola WebFetch.

## Eventi trattenuti in ops/da-verificare.json (non toccato a mano)
- Da itinerarinellarte.it: Renato Casaro. Horror; L'Ultima Rinascita; Andar per fiere; Klimt a Villa Freya; Ritratti di
  donna tra Hayez, Boldini e Carra'. Sono gia' in config/eventi_redazione.yaml: con la fonte ammessa dovrebbero tornare
  pubblicabili da soli alla prossima pubblicazione (`--controlla` non li segnala piu').
- Da happyticket.com: Angelo Branduardi - Il Cantico (11/12, Conegliano) e Il mago di Oz (21/03/2027, Castelfranco) sono
  gia' in eventi_redazione: stesso discorso. Rimessi da me dopo la lettura della scheda Happy Ticket (fonte ora
  ammessa): "Affinita' elettive (Harmonia Ruris Festival)" 06/12 19:00 Teatro Accademico Castelfranco e "Capodanno da
  Oscar" 01/01/2027 18:30 Teatro Accademia Conegliano. Le righe vecchie in ops/da-verificare.json vanno tolte alla
  prossima `pipeline.pubblica` / `--sposta-vietati` (non le ho modificate a mano).
- Gli eventi trattenuti da calendariopodismo.it (11) e trovasagre.com (10) restano fuori: ora la fonte e' vietata,
  servono conferme da organizzatori o comuni.

## Fonti del giro: esito
- Con eventi nuovi: gli-alcuni (Gospel 17/12), comune-castelfranco (Bianco Natale), podismoveneto (Trail delle Terre
  Rosse, dati da sportdolomiti.it), comune-roncade (concerto d'arpa, torneo di dama), comune-povegliano, comune-chiarano,
  comune-sernaglia, qdpnews (Natale a Susegana), mattorosso (14 serate fino al 27/12 non presenti), scopri-oderzo (8),
  comune-giavera, comune-maser (2), comune-nervesa (3), comune-quinto (2), comune-silea (6, con 4 date del Salotto
  musicale), comune-san-vendemiano (Fiammetta Borsellino 9/12), teatro-da-ponte (13 date mancanti: Voice, A Christmas
  Story, Michael Jackson Tribute, Queen Mania, repliche a Cison e le date di marzo).
- Gia' coperte, niente di nuovo: virtuosi-italiani-treviso (tutte le date gia' sul sito), museo-canova, teatro-del-pane,
  teatro-cristallo-oderzo, nautilus-teatro (le altre due date non hanno comune: Auditorium Manzoni, Chez les Grottes),
  comune-san-biagio, comune-gaiarine (solo concorsi e una gita a Lubiana).
- Vuote (nessun evento in programma): comune-loria, comune-resana, comune-cornuda, comune-san-polo, comune-fonte,
  comune-monastier (rassegne gia' in corso), visit-fregona (home ferma al 1/11; pagina eventi /news-eventi/).
- Non leggibili con WebFetch (pagina caricata da script, testo "MyPortal" ripetuto): comune-mogliano, comune-treviso,
  comune-spresiano, comune-paese, comune-trevignano (anche /home/vivere/eventi.html). Sono fonti `myportal` con
  `base_url`: il PC le legge via API, quindi non le ho disattivate.
- fondazione-benetton: /agenda-home/ e /agenda/ vuote a WebFetch; WebSearch mostra schede 2026 (presentazione
  "Venezia dopo la caduta" il 1/12 a Palazzo Bomben, non aggiunta: letta solo nel riassunto di ricerca). Nota aggiunta
  in config/sources.yaml, fonte non disattivata.
- libreria-san-leonardo: /notes a WebFetch mostra il catalogo del negozio; l'indirizzo e' giusto (WebSearch lo titola
  "Attivita' ed eventi in libreria", ultimi incontri al 13/11). Nota aggiunta, non disattivata.
- ubik-treviso: tre presentazioni del 28-29/11 con link solo a post Instagram (vietato): non aggiunte.

## Eventi visti ma non pubblicati
- Corsa dei Babbi Natale, Ponzano Veneto, 29/11/2026 ore 10 (home di calendariopodismoveneto): la scheda del blog dice
  invece 2/11/2026 e rimanda a cisonoancheio.it; date in conflitto, non aggiunta.
- "Aperitivo in musica" della Toti Dal Monte, 29/11 19:30 (Qdpnews): l'articolo e' sotto Conegliano ma il luogo letto
  e' "Gran Caffe' Tiziano, Pieve di Cadore": luogo incerto, non aggiunto.
- Festa e accensione dell'albero a Santa Lucia di Piave (Qdpnews 28/11): il giorno non e' scritto, non aggiunta.
- Rassegna Gospel: Black Gold (14/12) e Pastor Ron (27/12) gia' sul sito.

## Fonti nuove da catalogare
- sportdolomiti.it, schede gara `ds_event/<codice>` (es. https://sportdolomiti.it/ds_event/ttr_27): tipo cronometraggio
  e iscrizioni gare (trail e corsa in Veneto), dati con data, ora e organizzatore; query: "sportdolomiti ds_event
  <nome gara> 2027". Sito ufficiale del servizio di iscrizione, ammesso dal controllo fonti.
- Gli Alcuni, pagine di rassegna (https://live.alcuni.it/rassegna-gospel-gli-alcuni-treviso/): prezzi e date di piu'
  concerti in una pagina.

## Lezioni
- WebFetch funziona: il giro di 39 fonti costa circa 39 letture piu' 1 lettura per ogni evento che ha bisogno di orario
  e luogo (le pagine elenco dei comuni MyPortal e di scoprioderzo non riportano orari).
- I comuni MyPortal che hanno solo `base_url` non si leggono con WebFetch (testo del framework); quelli con l'URL
  /home/vivere/eventi.html si' (Povegliano, Chiarano, Silea, Maser, Gaiarine, San Vendemiano).
- Il calendario del Teatro Da Ponte ha date che il PC non ha preso (concerti fuori rassegna e date di marzo): vale la
  pena confrontarlo per intero con `--comune "Vittorio Veneto"`.
- Il Mattorosso pubblica circa 30 date in un elenco senza orari: il PC ne aveva solo 4 sul sito.
