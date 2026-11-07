# Lezioni della revisione notturna

Quello che Claude impara notte dopo notte su come trovare eventi in provincia di Treviso con meno ricerche:
query che funzionano, siti che non servono, periodi in cui certe fonti pubblicano, errori da non ripetere.
Si legge all'inizio di ogni notte; si aggiorna alla fine (aggiungi, correggi, togli cio' che non vale piu').
Tienila breve: al massimo ~80 righe, raggruppate per tema.

## Ricerche che funzionano
- Per gruppi di eventi Eventbrite nello stesso luogo (es. 6 a Santa Caterina) cercare i titoli insieme: esce il
  festival che li organizza e il suo programma verifica tutto con 2-3 letture.
- WebSearch "standard" rende poco sui siti locali (risultati USA): per comuni, rassegne e teatri usare "extended".
- WebFetch apre solo link comparsi nei risultati: i link della coda (comune.treviso.it, 2night, eventiesagre) vanno
  prima fatti uscire con una ricerca mirata (titolo + comune + anno).
- Rassegne con programma su sito WordPress (es. musincantus.it): la pagina /eventi/elenco/?tribe-bar-search=<comune>
  da' tutte le date con indirizzo in una volta.
- Mercatini ricorrenti: le schede cosedicasa.com indicano la regola (seconda/terza domenica), le sospensioni e la
  prossima data; servono per dividere in date singole. Su fleamapket i risultati di ricerca mostrano gia' gli
  indirizzi con la data (/AAAA-MM-GG/): bastano per sapere le date confermate senza aprire le pagine.
- Calendario Podismo Veneto (pagina del mese) da' anche i link ai volantini: si usano come official_url delle gare
  senza sito. Una lettura ha sistemato 7 gare e trovato una gara mancante.

- Il calendario di trevisoeventi.com rende ~25 eventi TV per lettura: ideale per scoprire e per il test di
  copertura; poi conferma sul sito dell'organizzatore (auditorium, comitato, teatro).
- I calendari di stagione dei teatri (Teatro Da Ponte) danno decine di date con ora, sala e scheda in una lettura.
- I calendari delle squadre (trevisobasket.it, benettonrugby.it) danno tutte le partite in casa in una lettura.
- Le pagine elenco dei comuni (San Biagio, Silea) danno in una lettura i link alle schede: aprire solo le schede
  degli eventi in coda, una lettura per evento con ora, luogo e ingresso.
- Le schede di un teatro amatoriale hanno orario e prezzo, l'elenco no: basta aprire una scheda per la rassegna.

- Le pagine elenco dei comuni design-comuni (San Biagio, Sernaglia, Castelfranco) mettono nei risultati i link alle
  schede: dopo una lettura dell'elenco le schede si aprono con WebFetch anche se non erano nei risultati di ricerca.
- Le schede di dettaglio di trevisoeventi (es. /colle-umberto-sagra-di-san-martino.html) si aprono e danno programma per
  giorno e sito dell'organizzatore: 8 letture il 2026-11-07 hanno dato 37 eventi. Le pagine elenco dei locali
  (mattorosso.it/eventi) danno 20 date in una lettura.
- Calendario Podismo Veneto del mese: una lettura ha dato i volantini di 7 gare (official_url) e un orario diverso dalla
  pagina ufficiale (Prosecco Ultra Trail parte da Vittorio Veneto, non da Vidor): la pagina della gara vince.
- La guida del weekend di Nordest24 ("Veneto, cosa fare dal ... al ...") esce il giovedi': una lettura, eventi TV con
  programma per giorno. Eventivenetando ha i programmi completi delle feste (Prealpi in Festa).

## Fonti da evitare o poco utili
- bibliotecatreviso.it vieta /myportal/ nei robots (WebFetch robots_disallowed): fonte del PC disattivata.
- teatro.it (pagine date) da' errore a WebFetch; imocovolley.it mostra in prima pagina solo le partite gia' giocate.
- Gli articoli di VenetoToday e Nordest24 sulle rassegne non dicono quasi mai l'ingresso: per l'accesso servono le
  schede dell'organizzatore (es. musincantus.it/evento/...), non le testate.
- cheventi.it e arteven.it/pr/treviso danno errore a WebFetch; Eventbrite non si apre senza un risultato di ricerca.
- eventivenetando ed eventiesagre per le sagre spesso mostrano l'edizione di anni passati: controllare l'anno.
- deliziedautunno.tv e cultura.gov.it vietano i robot: non aprirli, usarli solo come titolo nei risultati.
- trevisotoday.it da' errore a WebFetch; venetotoday.it invece si apre.
- microturismodellevenezie.it ha date contraddittorie nella stessa scheda: mai usarla come conferma.
- Vietano i robot o danno errore: trevisosotterranea.it, comune.pievedisoligo.tv.it, rockol.it, itinerarinelgusto.it,
  comune.cappellamaggiore.tv.it, puntoettore.it (pagina eventi vuota, eventi solo su Eventbrite e Instagram).
- WebFetch rifiuta anche gli indirizzi presi dai file del repository (coda, sito_ufficiale): solo link usciti da
  WebSearch. Le 4 aperture tentate cosi' il 2026-11-01 sono ricerche sprecate.
- Ricerche "eventi <comune> novembre <anno>" sui comuni piccoli: escono solo portali (virgilio, ilborghista,
  cheventi) e quasi mai eventi; resa ~0. Meglio cercare "Pro Loco <comune>" e il sito del comune per scoprire se
  e' MyPortal (si passa al PC).
- Ricerche per tema generiche (bambini all'aperto, presentazioni di libri) danno guide e pagine vecchie
  (edizioni di giugno o gennaio): servono parole del periodo (Natale, San Martino) e un comune.

- Coordinate esatte: WebFetch non legge le mappe (wanderlog chiede un permesso, tripaligner e zero.eu non hanno
  lat/lon) e la shell non raggiunge Nominatim: 4 letture sprecate il 2026-11-05. Meglio dare indirizzo e comune
  giusti (il PC ricalcola) o il centro certo piu' vicino.
- hellomoglianoveneto.net: nei risultati solo post di anni passati. trevisoimprese.it vieta i robot.
- Eventbrite: la pagina organizzatore di .Ettore non elenca gli eventi. L'accesso si conferma con l'elenco dei gratuiti
  (/d/italy--treviso--85685297/free--events/?page=N, ora letto dal PC); chi non vi compare va visto sulla scheda.

- WebFetch rifiuta anche i link presi dentro una pagina letta se il dominio e' nuovo (veneto.eu, comune.mottadilivenza
  dopo un redirect, wp-json di musincantus): 3 letture perse il 2026-11-06. lapiazzaweb.it vieta i robot.
- 2026-11-07: robots_disallowed per WebFetch anche comune.quintoditreviso.tv.it, comune.vedelago.tv.it e
  comune.valdobbiadene.tv.it; insolitotrantran.it da' errore (anche l'API tribe del PC: 404). Permesso negato senza
  risposta (lettura persa): pagine nuove di sernaglia, imocovolley.it/calendar, trevignanocultura.it, culturalheritageonline.
- Ricerche sui comuni piccoli (Carbonera, Castelcucco, Colle Umberto) e la newsletter UNPLI 'Weekend con le Pro Loco'
  (nessun evento veneto): resa 0. lavitadelpopolo.it a volte mostra articoli di anni passati (Vedelago 2023).
- Il calendario delle degustazioni del Consorzio Conegliano Valdobbiadene sono disponibilita' su appuntamento, non eventi.
- Le pagine del Comune di Castelfranco per "Giallo in Castello" nei risultati sono tutte di edizioni passate (2024,
  maggio 2026): le date di novembre restano senza scheda.

## Calendario (chi pubblica quando)
- Teatri comunali: le stagioni 2026/27 escono a fine ottobre con vendite da inizio novembre (Castelfranco).
- Sagre di San Martino e Madonna della Salute: tutte a novembre, quasi solo su Facebook e aggregatori.
- Mostre del radicchio rosso (Preganziol, Zero Branco, rassegna Fiori d'Inverno): a gennaio, programmi a dicembre.
- Garden center (Bardin): festival d'autunno settembre-ottobre, poi Natale.

## Errori da non ripetere
- eventiesagre a volte sbaglia il nome del comune (Badoere di Morgano scritto "Mordano", poi geocodificato a caso):
  leggere la scheda prima di rimuovere come "fuori provincia".
- Nel modificare correzioni.yaml con script, l'intestazione commentata contiene "# rimuovi:": inserire le voci
  prima della riga "rimuovi:" che inizia a capo, non della prima occorrenza.
- In correzioni.yaml le date senza ora vanno tra virgolette ("2026-11-01"): altrimenti --applica si blocca
  (TypeError nel sort) anche se --controlla le dice valide.
