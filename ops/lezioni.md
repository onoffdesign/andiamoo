# Lezioni della revisione notturna

Quello che Claude impara notte dopo notte su come trovare eventi in provincia di Treviso con meno ricerche:
query che funzionano, siti che non servono, periodi in cui certe fonti pubblicano, errori da non ripetere.
Si legge all'inizio di ogni notte; si aggiorna alla fine (aggiungi, correggi, togli cio' che non vale piu').
Tienila breve: al massimo ~80 righe, raggruppate per tema.

## Ricerche che funzionano
(trevisoeventi, teatri, squadre, trovasagre, PDF dei comuni, Eventbrite, ricerca extended, link da far uscire con una
ricerca e mercatini ricorrenti con cosedicasa: ora nel metodo)
- Per gruppi di eventi Eventbrite nello stesso luogo (es. 6 a Santa Caterina) cercare i titoli insieme: esce il
  festival che li organizza e il suo programma verifica tutto con 2-3 letture.
- Rassegne con programma su sito WordPress (es. musincantus.it): la pagina /eventi/elenco/?tribe-bar-search=<comune>
  da' tutte le date con indirizzo in una volta.
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

- 2026-11-16: la pagina /cityd/<comune>/concerti-55/ di TicketOne si apre e da' 13 concerti con ora e link (Conegliano);
  il sito ufficiale fioridinverno.tv ha le schede di ogni festa del radicchio; le pagine comune di trevisoeventi
  (cordignano.html, ormelle.html) danno programma, orari e ingresso. Il calendario della Federciclismo del Trofeo
  Triveneto CX elenca le gare TV della stagione (senza ora ne' luogo esatto).
- 2026-11-17: le pagine IAT con My Calendar (scoprioderzo.it/my-calendar/) e le agende delle fondazioni (fbsr.it/agenda-home/)
  si aprono e danno eventi che nessun aggregatore ha; i programmi di rassegna escono in /edizioni/<nome>/. Gli orari
  ufficiali delle partite di Serie C per blocchi di giornate escono su Trivenetogoal (4 orari sistemati in una lettura).

- 2026-11-18: gli avvisi dei Comuni per le casette dei mercatini (Castelfranco) danno le date ufficiali del Natale prima
  del programma; qdpnews ha il programma del Natale di Conegliano (5/12-3/1). scoppiospettacoli.it ha le schede dei
  balletti in tournee con prezzi. La pagina della stagione de I Virtuosi Italiani apre anche le schede (ora e prezzi).

- 2026-11-19: il calendario di trevisoeventi e' lungo 130 mila caratteri: la seconda lettura con offset 100000 da' febbraio-aprile
  (6 date di Trevignano Cultura mancanti). WebSearch con allowed_domains (trevisoeventi.com, oderzocultura.it, trovasagre.com,
  caitreviso.it, newageclub.it) fa uscire subito la pagina giusta: 5 ricerche, 5 pagine utili. Le pagine comune di
  Il Tacco di Bacco elencano concerti e spettacoli in biglietteria di tutta l'area: buone per scoprire e per il test.

- 2026-11-20: la guida delle mostre del weekend di TViWeb (esce il martedi') ha le mostre TV con orari e sito: ottima per il test.
  Villa di Maser pubblica le attivita' dell'anno in /visite-ed-eventi/eventi?year=AAAA. Prima di aprire un link guardare la
  lista qui sotto: stanotte 4 letture perse su domini gia' noti come vietati (cultura.gov.it, museiveneto, trevisotoday, teatro.it).
  Gli articoli Qdpnews e La Vita del Popolo sul Natale senza anno nell'indirizzo erano del 2025: guardare la data nei risultati.

- 2026-11-21: mentelocale.it/treviso/ (120 spettacoli in una lettura) e le pagine sala di Happy Ticket (/it/locations/treviso/<comune>/<sala>.htm)
  danno gli spettacoli in vendita; il libretto PDF della stagione del Teatro Stabile (risorse.teatrostabileveneto.it/hubfs/...) ha date e ore.
  Le pagine eventi di eventiesagre per comune (Silea, Altivole, Orsago) e per Presepi danno solo edizioni passate: non riaprirle.

- 2026-11-22: per corse e camminate il calendario running.life di un comune (raggio 30 km) e' il test di copertura dello
  sport in una lettura; i mancanti si confermano sul calendario PDF Trevisando dell'anno (ora, km, gruppo) e sulle schede
  trevisando.it/marcia/<nome>/ (indirizzo di partenza), apribili dopo una ricerca con allowed_domains trevisando.it.
  Le pagine comune di Il Tacco di Bacco piccole (Riese, Motta) mostrano solo 2-3 eventi "in evidenza": non valgono una lettura.

- 2026-11-23: il programma del Natale del capoluogo esce su Qdpnews (articolo del 20/11 con l'anno nei metadati): 36 eventi
  nuovi in una lettura. La ricerca "<comune> eventi dicembre 2026" per i comuni piccoli (Codogne', Carbonera, Castelcucco,
  Colle Umberto, Valdobbiadene, Vedelago) da' solo portali generici a fine novembre: meglio cercare il programma del Natale
  del comune a fine mese. Il libretto PDF della stagione lirica e concertistica del Teatro Stabile ha anche gli orari.

- 2026-11-24: la pagina di una singola rassegna dei Musei Civici (/mostre-ed-eventi/<rassegna>/) ha ora, luogo e link di
  prenotazione di ogni appuntamento; il programma UNPLI di Boschi a Natale elenca le escursioni delle Pro Loco di tutte
  le province venete con una scheda ciascuna (ora e ritrovo). Le schede TicketOne del New Age si aprono 1 su 3.

- 2026-11-25: il calendario /events/ del New Age, uscito da WebSearch con allowed_domains newageclub.it, si apre (il 19/11 no):
  26 date fino ad aprile senza anno, che si ricava dal giorno della settimana. Le ricerche generiche "standard" su ricorrenze
  (Santa Lucia, San Nicolo') e ballo escono quasi solo dal Trentino: per la provincia servono allowed_domains (qdpnews,
  trevisoeventi) o il nome del comune. Gli agenti di lettura che provano i link interni (Il Tacco di Bacco, veneto.eu) li
  vedono rifiutati: chiedere una sola pagina. I programmi del Natale 2026 di Montebelluna non sono ancora usciti (solo 2025/26).

## Fonti da evitare o poco utili
- Elenco dei domini che WebFetch non legge: ora in `ops/domini-illeggibili.yaml` (lo stampa il piano della notte).
- Vietano i robot o danno errore a WebFetch (usarli solo come titolo nei risultati): bibliotecatreviso.it /myportal/,
  teatro.it, cheventi.it, arteven.it/pr/treviso, trevisotoday.it, oggitreviso.it, deliziedautunno.tv, cultura.gov.it,
  museiveneto.cultura.gov.it, trevisosotterranea.it, trevisoimprese.it, rockol.it, itinerarinelgusto.it, lapiazzaweb.it,
  insolitotrantran.it, beescover.com, schede eventiesagre uscite da ricerca per comune (5 su 5 di edizioni 2019-2023 il 22/11), rockol.it anche per le pagine locale, schede Mapcarta /de/ e /W... (2 su 3 in errore il 21/11), eventivenetando.it per Natale (pagine 2023), prolococamalo.it, cinemaedera.it/rassegne.html, liceoartisticotreviso.edu.it; siti dei comuni di Pieve di
  Soligo, Cappella Maggiore, Quinto, Vedelago, Valdobbiadene, Cessalto, Sernaglia, Montebelluna. scoprioderzo.it/my-calendar/ se non esce da una ricerca della notte (rifiutato il 23/11), articoli Qdpnews senza anno nell'indirizzo per il Natale (3 su 3 di anni passati il 23/11). venetotoday.it si apre.
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

- 2026-11-15: resa 0 i comuni di Asolo (OpenCity, pagina eventi non aperta), Preganziol, Riese Pio X, San Pietro di
  Feletto e Ormelle (design-comuni "Nessun evento"); Pro Loco di San Pietro di Feletto ferma a settembre; yogaday.it e
  balyogandotreviso.it fermi al 2023-2025; CCIAA Treviso-Belluno solo corsi e-learning; mercatinodinatale.it e
  2d2web.com vietati; mercatinidinatale.it e magicoveneto senza date 2026; "Novembre rosa, filo rosso" di Silea:
  in rete solo le edizioni 2023 e 2024. Sagratour ha schede apribili con programma e coordinate ma non e' fonte
  ufficiale. Link presi dentro ClassicaLive (teatrostabileveneto, filarmoniaveneta, musincantus) rifiutati: farli
  uscire con una ricerca (la pagina stagione di risorse.teatrostabileveneto esce cercando il nome della stagione).

- 2026-11-16: Mapcarta con id numerico (es. /18700670, Dosson) da' errore a WebFetch: per le frazioni non serve, il
  geocoder le posiziona dal giro dell'11/11. A vuoto: vivertempo.it (fermo al 2018), loveitalia.fun (3 eventi senza
  fonte), trevisoperte.it (elenco in errore), elenco di prolocovenete.it (caricato via JavaScript), articoli Qdpnews sul
  Natale di Pederobba (2024), trevisomtb.it (calendario 2026 fermo ad aprile), trevignanocultura.it (EventON, schede
  della stagione passata), Comune di Conegliano (OpenCms, nessun elenco).

- 2026-11-17: astrofilitrevigiani.it solo http (WebFetch va in loop di redirect); associazioniponzanoveneto.it senza eventi
  2026 in provincia; occhi.it ha ancora le schede 2025 dei mercatini di Natale; plasticfreeonlus.it elenca le raccolte
  solo dopo registrazione; le schede fbsr.it/evento/ lette dall'agenda vengono rifiutate (4 letture perse).
  Programmi di Natale 2026 di Treviso, Oderzo, Vittorio Veneto, Godega e Ponzano al 17/11 non ancora usciti
  (in cima solo articoli 2025).

- 2026-11-18: vivaticket.com (pagine venue) vieta i robot; le schede TicketOne /event/ uscite da una ricerca danno
  errore (3 letture perse, New Age Club); prolocofregona.it e prolococastelfrancoveneto.it vietano i robot; Comune di
  Vidor (Municipium) e Pro Loco ASC Mansue' senza eventi futuri; Spazio Paraggi chiuso (ora 'La Stanza'); Mapcarta per
  le frazioni (Castello Roganzuolo) e i municipi: ancora a vuoto. Ricerche per ambito 'fiere' e 'bambini all'aperto' a
  vuoto anche con il nome del santo.

- 2026-11-19: resa 0 le ricerche per comune di Villorba, Borso del Grappa, Cappella Maggiore e Pieve di Soligo (solo
  eventiesagre, virgilio e il Tacco di Bacco), gli ambiti laboratori di Natale, arti marziali ed equitazione (solo
  calendari federali e pagine di altre regioni); virgilio.it da' errore a WebFetch; newageclub.it/events/ in errore;
  le schede CAI a 6 giorni dall'uscita sono ancora 'in aggiornamento'. Programmi di Natale di Treviso, Villorba e Pieve
  al 19/11 non ancora usciti.

- 2026-11-24: ricerche "eventi <comune> dicembre" e "<comune> Natale" senza dominio (Trevignano, Follina, Cessalto,
  Vazzola) danno solo eventiesagre di anni passati e omonimi (Trevignano Romano): saltarle. Qdpnews Natale di Montebelluna
  e della Marca, eventiesagre Mogliano e concerti di Natale: tutti 2016-2025.

## Calendario (chi pubblica quando)
- Programmi di Natale dei comuni (accensione dell'albero, villaggi): a meta' novembre in cima ci sono ancora gli
  articoli del 2025; quelli nuovi escono dopo il 15-20 novembre.
- Mostre di presepi: le date della stagione escono a fine novembre (a inizio novembre ci sono solo quelle dell'anno prima).
- Teatri comunali: le stagioni 2026/27 escono a fine ottobre con vendite da inizio novembre (Castelfranco).
- Sagre di San Martino e Madonna della Salute: tutte a novembre, quasi solo su Facebook e aggregatori.
- Feste del radicchio (rassegna Fiori d'Inverno di UNPLI): da fine novembre a marzo; calendario a inizio novembre,
  programmi delle singole feste di solito una o due settimane prima.
- Mercatini di Natale: al 16 novembre le guide nazionali (thewom) dicono che i programmi di Treviso non sono ancora usciti;
  al 18/11 escono i programmi di Conegliano (qdpnews) e le date di Castelfranco (avviso del Comune), non ancora Treviso;
  al 19/11 trevisoeventi ha le schede di Valdobbiadene e Breda, ma Treviso città non c'e' ancora.
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
