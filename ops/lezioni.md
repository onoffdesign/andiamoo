# Lezioni della revisione notturna

Quello che Claude impara notte dopo notte su come trovare eventi in provincia di Treviso con meno ricerche:
query che funzionano, siti che non servono, periodi in cui certe fonti pubblicano, errori da non ripetere.
Si legge all'inizio di ogni notte; si aggiorna alla fine (aggiungi, correggi, togli cio' che non vale piu').
Tienila breve: al massimo ~80 righe, raggruppate per tema.

## Ricerche che funzionano
(trevisoeventi, teatri, squadre, trovasagre, PDF dei comuni ed Eventbrite: ora nel metodo, sezione Treviso)
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

- Le schede di un teatro amatoriale hanno orario e prezzo, l'elenco no: basta aprire una scheda per la rassegna.

- Le pagine elenco dei comuni design-comuni (San Biagio, Sernaglia, Castelfranco) mettono nei risultati i link alle
  schede: dopo una lettura dell'elenco le schede si aprono con WebFetch anche se non erano nei risultati di ricerca.
- La guida del weekend di Nordest24 ("Veneto, cosa fare dal ... al ...") esce il giovedi': una lettura, eventi TV con
  programma per giorno. Eventivenetando ha i programmi completi delle feste (Prealpi in Festa).

- 2026-11-10: le schede dei comuni con elenco vietato (Quinto) si aprono se escono da una ricerca con il titolo
  esatto; il PDF del calendario stagionale allegato alla notizia del Comune (San Fior) si apre e vale un mese.
  collaltodisusegana.it: home con link a festival, mercatini e Natale, tutte apribili.

- 2026-11-11: la guida del weekend di TViWeb ("Sagre, feste, fiere, marce e mostre in Veneto: 40 appuntamenti per il
  weekend del ...") esce a meta' settimana con 14 eventi TV e il sito citato: vale per test di copertura e scoperta.
  Comuni con sito Municipium (Roncade, Breda di Piave): elenco eventi apribile, passabile al PC come html_llm.
- 2026-11-12: le schede del Mattorosso hanno ora e ingresso (l'elenco no): una lettura per scheda. La pagina eventi
  di mestre.ubiklibri.it elenca anche le presentazioni della Ubik di Treviso con data e ora. Anteprima Sagre ha date
  e luogo esatto delle sagre (Frico: salone dietro la chiesa di Lorenzaga) senza l'ingresso.

- 2026-11-13: Mapcarta (WebSearch con allowed_domains mapcarta.com) da' le coordinate OSM di castelli, chiese e
  ville con nome; le pagine Wikipedia lette da WebFetch perdono le coordinate. Qdpnews si apre e ha programmi
  orari completi delle feste dei comuni (Giavera) e dei festival (4passi): buona come official_url.

- 2026-11-14: Eventi Venetando (Consorzio Pro Loco Quartier del Piave) apre le schede anche dai link letti nella home,
  con ora, prezzo e numeri della mappa; Spettacoli di Mistero (UNPLI) ha schede apribili con prezzo e prenotazione.
  I calendari mensili dei comuni piccoli escono come articoli Qdpnews ("Novembre pievese").

## Fonti da evitare o poco utili
- Vietano i robot o danno errore a WebFetch (usarli solo come titolo nei risultati): bibliotecatreviso.it /myportal/,
  teatro.it, cheventi.it, arteven.it/pr/treviso, trevisotoday.it, oggitreviso.it, deliziedautunno.tv, cultura.gov.it,
  museiveneto.cultura.gov.it, trevisosotterranea.it, trevisoimprese.it, rockol.it, itinerarinelgusto.it, lapiazzaweb.it,
  insolitotrantran.it, beescover.com, prolococamalo.it, cinemaedera.it/rassegne.html; siti dei comuni di Pieve di
  Soligo, Cappella Maggiore, Quinto, Vedelago, Valdobbiadene, Cessalto, Sernaglia, Montebelluna. venetotoday.it si apre.
- Vuoti o vecchi: puntoettore.it (eventi solo su Eventbrite), hellomoglianoveneto, prolocofollina.it, home MyPortal di
  Trevignano, trevisoinfo.it (2011), Pro Loco di Cimadolmo (2017), lavitadelpopolo.it a volte (Vedelago 2023).
- Gli articoli di VenetoToday e Nordest24 sulle rassegne non dicono quasi mai l'ingresso: servono le schede
  dell'organizzatore (es. musincantus.it/evento/...).
- eventivenetando ed eventiesagre per le sagre spesso mostrano l'edizione di anni passati: controllare l'anno.
- microturismodellevenezie.it ha date contraddittorie nella stessa scheda: mai usarla come conferma.
- WebFetch rifiuta gli indirizzi presi dai file del repository e spesso i link dentro una pagina letta (domini nuovi,
  redirect, wp-json, pagine /page/2/, schede di itinerarinellarte: 8 rifiutate il 2026-11-09). Provare un link solo
  prima di lanciarne altri in parallelo; i link usciti da WebSearch si aprono.
- Ricerche "eventi <comune> <mese>" e "Pro Loco <comune>" sui comuni piccoli (Carbonera, Castelcucco, Cimadolmo,
  Cavaso, Tarzo): resa ~0, escono portali. Meglio scoprire se il sito del comune e' MyPortal (si passa al PC).
- Ricerche per tema o ambito generiche (bambini all'aperto, open mic, padel, cineforum, jam, nuoto e canoa in autunno)
  danno guide e pagine vecchie: servono parole del periodo (Natale, San Martino) e un comune.
- Coordinate esatte: WebFetch non legge le mappe e la shell non raggiunge Nominatim. Meglio dare indirizzo e comune
  giusti (il PC ricalcola) o il centro certo piu' vicino.
- Newsletter UNPLI 'Weekend con le Pro Loco': nessun evento veneto.
- 2026-11-10: rifiutati o vietati anche ilgazzettino.it, italiaeventinews.altervista.org, fondazionezavrel.it, i volantini
  del blog Calendario Podismo Veneto e la scheda del Comune di Codogne'. Musincantus non pubblica l'ingresso dei concerti
  di Autunno Musicale (solo il Lobgesang "libero con offerta"): verificati senza accesso, inutile ricercarlo.
- Ricerche di sport tradizionali (palio, tiro alla fune) a novembre: resa 0, sono eventi estivi o dentro le sagre.

- 2026-11-11: resa 0 o pagine vecchie: Comune e Pro Loco di Salgareda, Meduna di Livenza, Villa Lattes di Istrana,
  teatrocristallo.it (e' Bolzano), notizie di Natale 2024 di Montebelluna, asolomusica.com, montegrappa.org,
  faitango.it; ambiti "Animali" e "Musical" in provincia.
- 2026-11-12: palestre di arrampicata (Gioco Verticale, Orizzonti Verticali) senza eventi datati sul sito; schede
  delle uscite CAI Treviso "in aggiornamento" fino a pochi giorni prima; Comune di Mareno di Piave: home MyPortal senza
  link agli eventi; ricerche "tiro con l'arco" e "boulder" in provincia: solo calendari nazionali, resa 0.

- 2026-11-13: robots vietato anche per il sito del Comune di Silea (le schede) e di Caerano di San Marco; il sito
  della Pro Loco di Segusino non esce, i mercatini di Segusino solo su portali senza dati 2026. Le guide del weekend
  (TViWeb) sbagliano a volte le date (4passiFestival): confermare. I link letti dentro una pagina (TViWeb ->
  piazzainfesta, comune di Vedelago) vengono rifiutati: 6 letture perse; prima una ricerca col titolo.
  Ricerca "visite guidate Treviso" e "accensione albero Natale": solo pagine generiche o del 2025.

- 2026-11-14: Mapcarta non trova piazze, municipi e ville poco note (Piazza Marconi di San Martino, municipio di San
  Fior, Villa Freya): escono solo i paesi, 4 ricerche a vuoto. Sito della Biblioteca di Castelfranco sospeso;
  provincia.treviso.it (calendario Pari Opportunita') da' errore a WebFetch; Comune di Crocetta senza eventi.
  Ricerche per ambito "serata club", "saggio ginnastica", "cena comunitaria": solo portali e guide nazionali.

## Calendario (chi pubblica quando)
- Programmi di Natale dei comuni (accensione dell'albero, villaggi): a meta' novembre in cima ci sono ancora gli
  articoli del 2025; quelli nuovi escono dopo il 15-20 novembre.
- Mostre di presepi: le date della stagione escono a fine novembre (a inizio novembre ci sono solo quelle dell'anno prima).
- Teatri comunali: le stagioni 2026/27 escono a fine ottobre con vendite da inizio novembre (Castelfranco).
- Sagre di San Martino e Madonna della Salute: tutte a novembre, quasi solo su Facebook e aggregatori.
- Feste del radicchio (rassegna Fiori d'Inverno di UNPLI): da fine novembre a marzo; calendario a inizio novembre,
  programmi delle singole feste di solito una o due settimane prima.
- Piste di ghiaccio di Natale: a meta' novembre escono solo articoli degli anni passati; cercarle da fine novembre.

## Errori da non ripetere
- eventiesagre a volte sbaglia il nome del comune (Badoere di Morgano scritto "Mordano", poi geocodificato a caso):
  leggere la scheda prima di rimuovere come "fuori provincia".
- Nel modificare correzioni.yaml con script, l'intestazione commentata contiene "# rimuovi:": inserire le voci
  prima della riga "rimuovi:" che inizia a capo, non della prima occorrenza.
- In correzioni.yaml le date senza ora vanno tra virgolette ("2026-11-01"): altrimenti --applica si blocca
  (TypeError nel sort) anche se --controlla le dice valide.
- --controlla non verifica le sottocategorie: usare solo quelle di config/categories.yaml (teatro, non prosa;
  sagre, non radicchio). Corrette 41 voci il 2026-11-09.
