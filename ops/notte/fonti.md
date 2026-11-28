# Agente fonti, notte del 2026-11-28 (quinto giro)

## Numeri
- Fonti da verificare del piano: 12. Nuove decisioni: ammessa 1 (balliamoliscio.it), vietate 2 (allevents.in,
  canzoni.it). Restano da verificare 4 (ticketone.it, classicalive.it, 2night.it, cheventi.it). 5 erano gia' decise
  (eventbrite.it, cosedicasa.com e fleamapket.com vietate; eventivenetando.it e happyticket.com ammesse), non riaperte.
- Altre due fonti verificate mentre cercavo fonti nuove: hdsports.org ammessa, finishers.com vietata.
- Fonti nuove nel catalogo ops/fonti.yaml: 46 (da 274 a 320 voci). 39 attive, 6 deboli, 1 ferma (finishers, vietata).
  Quasi tutte sono siti ufficiali (Comuni, enti turistici regionali e comunali, teatri, musei), piu' 2 aggregatori.
- Eventi aggiunti: 3 (config/notte/fonti-eventi.yaml). Correzioni: 0.
- Ricerche usate: 58 su 75 (WebSearch 29, WebFetch 29). Coordinate prese da Nominatim con la shell, fuori quota.
- `python -m pipeline.notte --controlla fonti`: "Parti valide". `pipeline.fonti_vietate` legge ancora il file.

## Verifiche delle fonti (config/fonti-vietate.yaml)
- **ticketone.it** (15 trattenuti): robots.txt e /help/terms/ rispondono ancora 503. Resta da verificare.
- **classicalive.it** (9 trattenuti): due ricerche, nessuna pagina legale trovata. Resta da verificare: serve che
  Federico copi a mano il link del footer.
- **allevents.in -> vietate**: Terms of Use (/conditions), Acceptable Use e): vietato '"crawl," "scrape," or "spider"
  any page, data, or portion of or relating to the Platform (through use of manual or automated means)'; f): vietato
  "use unauthorized automated agents to harvest data".
- **canzoni.it -> vietate** (caso limite): Termini d'uso (/info/termini_uso.html): dati, informazioni e contenuti
  "per uso esclusivamente personale obbligandosi a non procedere alla loro distribuzione con qualsiasi mezzo, anche
  telematico ... pubblicazione, cessione a terzi". Trattata come eventiesagre.it. La voce del catalogo e' ora ferma.
- **balliamoliscio.it -> ammesse**: robots.txt ("User-agent: * / Allow: /") e /privacy/ letti, nessun divieto;
  termini e note legali non ci sono. Nessun evento di ops/da-verificare.json viene da li': nessun evento torna.
- **2night.it**: non riaperta, perche' il suo robots.txt blocca proprio le pagine legali. Resta da verificare.
- **cheventi.it**: non riaperta (/termini-e-condizioni/ dava 403 e non si fanno altri tentativi). Resta da verificare.
- **hdsports.org -> ammesse**: robots.txt (blocca ricerche, /kalender, /de/ e cartelle tecniche, non le pagine
  /running/), /nutzungsbedingungen e /impressum letti: nessun divieto di scraping o TDM; vietato riprodurre testi e grafiche.
- **finishers.com -> vietate**: CGU del 27/10/2026, art. 13.4: vietato raccogliere dati con robot, crawler o scraper
  e "creare o gestire banche dati, calendari o servizi" da quei dati; c'e' anche l'opt-out TDM (art. 13.3).
- Eventi di ops/da-verificare.json che possono tornare: **0**. Le fonti che trattengono eventi (ticketone 15,
  classicalive 9) restano da verificare; le altre (umbriaecultura, calendariopodismo, trovasagre, eventbrite,
  eventiesagre, fleamapket, cosedicasa) sono vietate.

## Fonti nuove salvate (ops/fonti.yaml; nome | url | query | tipo)
- Comune di Livorno, eventi | https://www.comune.livorno.it/it/categorie-eventi/74150 | "Comune di Livorno eventi dicembre" | comune
- Comune di Prato, Cartellone Eventi | https://tempolibero.comune.prato.it/ | "Cartellone Eventi Prato tempolibero comune" | comune
- Comune di Pesaro, prossimi eventi | https://www.comune.pesaro.pu.it/novita-in-comune/eventi/prossimi-eventi/ | "Comune di Pesaro prossimi eventi" | comune
- Perugia Comunica | https://perugiacomunica.comune.perugia.it/ | "Perugia Comunica evento" | comune
- Turismo Terni | https://turismo.comune.terni.it/eventi | "Turismo Terni eventi" | comune
- BCT Terni | https://bct.comune.terni.it/ | "BCT Terni presentazione libro dicembre" | biblioteca
- Comune di Viterbo e Teatro dell'Unione | https://comune.viterbo.it/vivere-il-comune/eventi/ | "Comune di Viterbo stagione teatrale Teatro dell'Unione" | comune
- Comune di Rieti (debole) | https://lnx.comune.rieti.it/ | "Comune di Rieti programma eventi festivita' natalizie" | comune
- Teatro di San Carlo (debole: anti-bot) | https://www.teatrosancarlo.it/ | "Teatro di San Carlo spettacoli stagione 2026 2027" | teatro
- Teatro Carlo Felice | https://www.carlofelice.it/ | "Teatro Carlo Felice Genova calendario" | teatro
- Fondazione Pergolesi Spontini | https://www.fondazionepergolesispontini.com/ | "Fondazione Pergolesi Spontini stagione Jesi 2026-2027" | teatro
- Teatro di Napoli | https://www.teatrodinapoli.it/ | "Teatro di Napoli stagione Mercadante San Ferdinando" | teatro
- Comune di Cuneo, eventi | https://www.comune.cuneo.it/vivere-il-comune/eventi/ | "Comune di Cuneo eventi dicembre" | comune
- Comune di Savona, eventi | https://www.comune.savona.it/index.php/it/eventi | "Comune di Savona eventi" | comune
- Visit Genoa | https://www.visitgenoa.it/it/eventi | "Visit Genoa eventi" | ente
- Comune di Palermo, eventi | https://www.comune.palermo.it/vivere-il-comune/eventi/ | "Comune di Palermo eventi" | comune
- Turismo Palermo | https://turismo.comune.palermo.it/ | "Portale del Turismo Comune di Palermo eventi" | comune
- Comune di Reggio Calabria (debole) | https://comune.reggio-calabria.it/Notizie | "Comune di Reggio Calabria notizie evento dicembre 2026" | comune
- Comune di Napoli, eventi | https://www.comune.napoli.it/vivere-il-comune/eventi/ | "Comune di Napoli eventi" | comune
- Comune di Olbia, eventi | https://www.comune.olbia.ot.it/it/eventi | "Comune di Olbia eventi" | comune
- Visit Tuscany | https://www.visittuscany.com/it/eventi/ | "Visit Tuscany eventi dicembre 2026" | ente
- Abruzzo Turismo | https://www.abruzzoturismo.it/it/eventi | "Abruzzo Turismo eventi" | ente
- Visit Piemonte | https://www.visitpiemonte.com/eventi | "Visit Piemonte eventi" | ente
- Comune di Senigallia | https://www.comune.senigallia.an.it/vivere-il-comune/eventi/ | "Comune di Senigallia eventi" | comune
- Teatro dell'Opera di Roma | https://www.operaroma.it/ | "Teatro dell'Opera di Roma stagione 2026 2027" | teatro
- Auditorium Parco della Musica | https://www.auditorium.com/it/ | "Auditorium Parco della Musica Natale 2026 evento" | teatro
- Teatro Vittorio Emanuele di Messina | https://www.teatrovittorioemanuele.it/stagione-vittorio-emanuele-2026-2027-sala-grande/ | "Stagione Vittorio Emanuele 2026/2027" | teatro
- Comune di Spoleto | https://www.comune.spoleto.pg.it/it | "Comune di Spoleto Accade a Natale 2026" | comune
- Comune di Foligno, eventi | https://comune.foligno.pg.it/vivere-il-comune/eventi/ | "Comune di Foligno eventi" | comune
- Comune di Empoli, eventi | https://www.comune.empoli.fi.it/Vivere-il-comune/Eventi | "Comune di Empoli eventi" | comune
- Natale a Termoli 2026 | https://www.comune.termoli.cb.it/novita/natale-a-termoli-2026-tutti-gli-eventi/ | "Natale a Termoli 2026 tutti gli eventi" | comune
- Comune di Marsala, eventi | https://www.comune.marsala.tp.it/it/eventi | "Comune di Marsala eventi" | comune
- Citta' di Noto (debole) | https://comune.noto.sr.it/index.php/it | "Comune di Noto concerto stagione concertistica" | comune
- Turismo Torino e Provincia | https://turismotorino.org/it/visita/eventi | "Turismo Torino eventi" | ente
- Comune di Sanremo (debole) | https://comune.sanremo.im.it/it | "Comune di Sanremo eventi dicembre" | comune
- Teatro Pubblico Pugliese | https://www.teatropubblicopugliese.it/news/ | "Teatro Pubblico Pugliese aperture debutti stagioni" | ente
- Comune di Avezzano | https://comune.avezzano.aq.it/ | "Comune di Avezzano notizie concerto Natale" | comune
- HDsports, corse in Puglia | https://www.hdsports.org/running/puglia-correre-calendario-corse | "hdsports Puglia calendario corse" | aggregatore (ammesso)
- Finishers (vietata, ferma) | https://www.finishers.com/it/d/europa/italia | (non usare) | aggregatore
- Turismo Roma | https://www.turismoroma.it/it/romalive | "Turismo Roma Romalive eventi" | ente
- Musei in Comune Roma | https://www.museiincomuneroma.it/it/mostre_ed_eventi/mostre | "Musei in Comune Roma mostre" | museo
- Roma Culture | https://culture.roma.it/arte/ | "Roma Culture arte eventi" | ente
- Comune di Pisa, eventi | https://www.comune.pisa.it/Vivere-il-Comune/Eventi | "Comune di Pisa eventi Natale" | comune
- Comune di Massa | https://www.comune.massa.ms.it/novita | "Comune di Massa novita evento dicembre" | comune
- Comune di Grosseto | https://www.comune.grosseto.it/notizia/ | "Comune di Grosseto notizia concerto teatro" | comune
- Comune di Bitonto (debole) | https://comune.bitonto.ba.it/it/news | "Comune di Bitonto news mercato Natale" | comune

## Proposte per le fonti del giro (config/sources.yaml, le aggiunge il coordinatore)
1. Comune di Cuneo | https://www.comune.cuneo.it/vivere-il-comune/eventi/ | Cuneo (CN) | html (Design Comuni) | molti
   eventi al mese con schede complete.
2. Comune di Marsala | https://www.comune.marsala.tp.it/it/eventi | Marsala (TP) | html | stagione concertistica e
   teatro con ora, luogo e prezzo.
3. Teatro Vittorio Emanuele | https://www.teatrovittorioemanuele.it/stagione-vittorio-emanuele-2026-2027-sala-grande/ |
   Messina (ME) | tribe_api da provare (/wp-json/tribe/events/v1/events), altrimenti html | schede /evento/.
4. Turismo Torino | https://turismotorino.org/it/visita/eventi | Torino (TO) e provincia | html | ente ufficiale,
   robots.txt letto.
5. Visit Tuscany | https://www.visittuscany.com/it/eventi/ | Toscana | html (schede senza parametri) | portale regionale.
6. Comune di Napoli | https://www.comune.napoli.it/vivere-il-comune/eventi/ | Napoli (NA) | html (Design Comuni).
7. Comune di Palermo | https://www.comune.palermo.it/vivere-il-comune/eventi/ | Palermo (PA) | html (Design Comuni).
8. Auditorium Parco della Musica | https://www.auditorium.com/it/ | Roma (RM) | html (WordPress, /it/event/<slug>/).
9. Comune di Livorno | https://www.comune.livorno.it/it/categorie-eventi/74150 | Livorno (LI) | html.
10. Comune di Foligno | https://comune.foligno.pg.it/vivere-il-comune/eventi/ | Foligno (PG) | html (Design Comuni).
11. Teatro Carlo Felice | https://www.carlofelice.it/ | Genova (GE) | tribe_api da provare, altrimenti html.
12. Visit Genoa | https://www.visitgenoa.it/it/eventi | Genova (GE) | html (Drupal).

## Eventi aggiunti (config/notte/fonti-eventi.yaml)
- Noemi in concerto, Auditorium Parco della Musica, Roma, 22/12 ore 21 (da 39 EUR).
- Mauro Carpi Quartet, Teatro Sollima, Marsala, 6/12 ore 18 (10 o 6 EUR).
- Municipio a porte aperte, Palazzo Municipale di Cuneo, 18/12, visite alle 15:30, 16:30 e 17:30 (gratuite, su prenotazione).
Coordinate da OpenStreetMap (Nominatim) per tutti e tre. Nessuno dei tre era gia' sul sito.

## Lezioni
- Con WebSearch e allowed_domains su 5-6 Comuni capoluogo, con la sola query "eventi dicembre 2026", escono 1-3 fonti
  nuove a ricerca. I capoluoghi con Design Comuni (/vivere-il-comune/eventi/) sono i migliori: Cuneo, Napoli,
  Palermo, Foligno, Pisa. Rendono zero Latina, Frosinone, Campobasso, Benevento, Caserta, Potenza e Bari, dove
  escono solo atti e notizie vecchie.
- I portali turistici regionali e comunali (Visit Tuscany, Turismo Torino, Visit Piemonte, Visit Genoa) hanno robots.txt
  aperti: sono la via piu' rapida per coprire una regione.
- La shell raggiunge Nominatim (non i siti): le coordinate dei luoghi non costano ricerche.
- Gli aggregatori sportivi stranieri hanno spesso clausole anti-scraping e anti-TDM molto esplicite (finishers.com):
  conviene leggere subito i termini.

## Problemi
- ticketone.it (15 trattenuti) e classicalive.it (9 trattenuti): quinto giro a vuoto (503 e pagina legale
  introvabile). Altri tentativi automatici sprecano ricerche: serve un controllo manuale di Federico.
- teatrosancarlo.it risponde a WebFetch con una pagina anti-bot; abruzzoturismo.it (503) e teatropubblicopugliese.it
  (500) non danno il robots.txt: da rileggere.
- Le API tribe non le ho provate: WebFetch apre solo link usciti dalle ricerche. Le provera' il giro.
