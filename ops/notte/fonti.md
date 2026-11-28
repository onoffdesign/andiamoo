# Agente fonti, notte del 2026-11-28 (quarto giro)

## Numeri
- Fonti da verificare del piano: 12. Ammesse 0 nuove, vietate 2 nuove (dice.fm, feverup.com), restano da verificare 7
  (ticketone.it, classicalive.it, 2night.it, allevents.in, balliamoliscio.it, canzoni.it, cheventi.it); 3 erano gia'
  decise (eventbrite.it e cosedicasa.com vietate, eventivenetando.it ammessa).
- Fonti nuove valutate e salvate in ops/fonti.yaml: 43 (catalogo da 231 a 274 voci), tutte siti ufficiali
  (Comuni, enti turistici regionali e comunali, teatri, un museo) piu' una pagina dell'aggregatore gia' ammesso
  iltaccodibacco.it. Nessuna nuova voce in config/fonti-vietate.yaml oltre alle verifiche.
- Eventi aggiunti: 0 (config/notte/fonti-eventi.yaml non creato). Correzioni: 0.
- Ricerche usate: 68 su 75 (WebSearch 37, WebFetch 31). Nessuna lettura da shell.
- `python -m pipeline.notte --controlla fonti`: vedi fondo.

## Verifiche delle fonti (config/fonti-vietate.yaml)
- **ticketone.it** (15 trattenuti): robots.txt e /help/terms/ con WebFetch rispondono 503. Resta da verificare.
- **classicalive.it** (9 trattenuti): /it/privacy/ 404, ricerca dell'informativa senza risultati. Resta da verificare.
- **2night.it**: non riaperta (robots.txt blocca proprio le pagine legali). Resta da verificare.
- **allevents.in**: robots.txt letto (gruppo ClaudeBot con solo Crawl-delay 10; per * bloccati /manage/, archivi
  2013-2023 e link ?ref=, non le pagine eventi); /pages/terms e /pages/terms-of-service 404 e ricerca senza esito.
  Resta da verificare.
- **balliamoliscio.it**: robots.txt "User-agent: * / Allow: /"; /privacy-policy/ 404, nessuna pagina legale trovata.
  Resta da verificare (aggiunta in da_verificare con nota).
- **canzoni.it**: robots.txt (per * blocca solo /artisti/cerca.php); /privacy.php 404, nessuna pagina legale trovata.
  Resta da verificare (aggiunta con nota).
- **cheventi.it**: robots.txt letto (blocca wp-admin, feed e ricerche con parametri, non le pagine eventi);
  /termini-e-condizioni/ 403. Resta da verificare (aggiunta con nota).
- **dice.fm -> vietate**: robots.txt "User-agent: ClaudeBot / Disallow: /" (anche anthropic-ai e Claude-Web).
- **feverup.com -> vietate**: Terms of Use (/legal/terms_italy.html) sez. 8.1 E(vi) vieta "accessing, monitoring or
  copying any content from the Website using any robot, spider, scraper ... without our express written permission"
  e E(vii) l'aggregazione delle attivita'.
- eventbrite.it e cosedicasa.com gia' vietate, eventivenetando.it gia' ammessa: non riaperte.
- Nessuna fonte e' diventata ammessa: nessun evento di ops/da-verificare.json puo' tornare sul sito per questa via.

## Fonti nuove salvate (ops/fonti.yaml; nome, url, query, tipo)
- Teatro Nuovo Giovanni da Udine | https://www.teatroudine.it/wp-json/tribe/events/v1/events | "Teatro Nuovo Giovanni da Udine stagione calendario" | tribe_api (92 eventi)
- Teatro Fraschini Pavia | https://www.teatrofraschini.it/wp-json/tribe/events/v1/events | "Teatro Fraschini Pavia programma stagione" | tribe_api
- Teatro Comunale di Ferrara | https://www.teatrocomunaleferrara.it/spettacolo/?month=next | "Teatro Comunale Ferrara calendario spettacoli" | html (circa 115 recite)
- Fondazione Teatro Petruzzelli Bari | https://www.fondazionepetruzzelli.it/eventi/ | "Fondazione Petruzzelli eventi stagione" | html
- Teatro Comunale Pavarotti-Freni Modena | https://www.teatrocomunalemodena.it/ | "Teatro Comunale Modena stagione opera concerti" | html
- Teatro Ponchielli Cremona | https://www.teatroponchielli.it/ | "Teatro Ponchielli Cremona stagione" | html
- Centro Servizi Culturali S. Chiara Trento | https://www.centrosantachiara.it/ | "Centro Santa Chiara Trento spettacoli stagione" | html
- Teatro Marrucino Chieti | https://www.teatromarrucino.eu/ | "Teatro Marrucino Chieti stagione" | html
- Teatro Biondo Palermo | https://teatrobiondo.it/ | "Teatro Biondo Palermo stagione" | html
- AMAT Marche | https://www.amatmarche.net/ | "AMAT Marche spettacoli calendario" | html
- Turismo Cremona | https://www.turismocremona.it/it/eventi | "Turismo Cremona eventi" | html
- Comune di Cremona | https://www.comune.cremona.it/vivere-comune/eventi | "Comune di Cremona eventi" | html
- Comune di Pavia | https://www.comune.pavia.it/vivere-comune/eventi | "Comune di Pavia eventi" | html
- Comune di Sondrio | https://comune.sondrio.it/eventi/ | "Comune di Sondrio eventi" | html
- Comune di Mantova | https://www.comune.mantova.it/it/eventi | "Comune di Mantova eventi" | html (Municipium)
- Orto Botanico di Bergamo | https://ortobotanico.comune.bergamo.it/eventi/ | "Orto Botanico Bergamo prossimi eventi" | html
- Comune di Piacenza | https://www.comune.piacenza.it/it/eventi | "Comune di Piacenza eventi" | html (Municipium)
- Visit Romagna | https://visitromagna.it/eventi | "Visit Romagna eventi" | html
- ViviRovereto | https://eventi.comune.rovereto.tn.it/ | "ViviRovereto eventi" | html (OpenCity, forse API opendata)
- Comune di Merano | https://www.comune.merano.bz.it/it/Vivere_la_citta/Eventi | "Comune di Merano eventi" | html
- Comune di Siena | https://www.comune.siena.it/vivere-il-comune/eventi | "Comune di Siena eventi" | html
- Visit Arezzo | https://www.visitarezzo.com/ | "Visit Arezzo eventi" | html (gestore da verificare)
- Comune di Pistoia | https://www.comune.pistoia.it/it/eventi | "Comune di Pistoia eventi" | html (Municipium)
- Comune di Lucca | https://www.comune.lucca.it/vivere-il-comune/eventi/ | "Comune di Lucca eventi" | html
- Comune di Macerata | https://www.comune.macerata.it/vivere-il-comune/eventi/ | "Comune di Macerata eventi" | html
- Umbria Tourism | https://www.umbriatourism.it/it/eventi | "Umbria Tourism eventi" | html
- Calabria Straordinaria | https://calabriastraordinaria.it/eventi | "Calabria Straordinaria eventi" | html (JavaScript)
- Comune di Crotone | https://www.comune.crotone.it/vivere-il-comune/eventi/ | "Comune di Crotone eventi" | html
- Comune di Matera | https://comune.matera.it/vivere-il-comune/eventi/ | "Comune di Matera eventi" | html
- Salerno Cultura | https://cultura.comune.salerno.it/eventi/ | "Salerno Cultura eventi" | html
- Comune di Taranto | https://www.comune.taranto.it/it/news | "Comune di Taranto eventi Natale" | html (debole)
- Comune di Lecce, notizie | https://www.comune.lecce.it/news | "Comune di Lecce stagione Teatri Apollo Paisiello" | html
- Comune di Foggia, notizie | https://www.comune.foggia.it/it/news | "Comune di Foggia cartellone Natale eventi" | html (debole)
- Comune di Nuoro | https://www.comune.nuoro.it/it/vivere/eventi | "Comune di Nuoro eventi" | html
- Comune di Oristano | https://comune.oristano.it/it/vivere-il-comune/eventi | "Comune di Oristano eventi" | html
- Comune di Sassari | https://www.comune.sassari.it/it/vivere-il-comune/eventi | "Comune di Sassari eventi" | html
- Comune di Trapani | https://comune.trapani.it/evento/ | "Comune di Trapani eventi" | html
- Comune di Ragusa | https://comune.ragusa.it/it/eventi | "Comune di Ragusa eventi" | html
- Comune di Caltanissetta | https://www.comune.caltanissetta.it/it/eventi | "Comune di Caltanissetta eventi" | html (Municipium)
- Comune di Messina, notizie | https://www.comune.messina.it/it/news | "Comune di Messina eventi Natale biblioteca" | html (debole)
- Comune di Isernia | https://comune.isernia.it/ | "Comune di Isernia eventi" | html (debole: calendario vuoto)
- Il Tacco di Bacco Molise per giorno | https://iltaccodibacco.it/molise/events/2026-12-13/ | "iltaccodibacco molise eventi <AAAA-MM-GG>" | aggregatore ammesso
- Cagliari Turismo | https://cagliariturismo.comune.cagliari.it/it/eventi | "Cagliari Turismo eventi" | html (WebFetch 403)

## Proposte per le fonti del giro (config/sources.yaml, le aggiunge il coordinatore)
1. Teatro Nuovo Giovanni da Udine | https://www.teatroudine.it/wp-json/tribe/events/v1/events | Udine (UD) | tribe_api |
   API pubblica letta: 92 eventi dal 29/11/2026; il Friuli ha poche fonti.
2. Teatro Fraschini | https://www.teatrofraschini.it/wp-json/tribe/events/v1/events | Pavia (PV) | tribe_api | API
   pubblica letta, stagione d'opera, prosa e concerti con date e ore.
3. Teatro Comunale di Ferrara | https://www.teatrocomunaleferrara.it/spettacolo/?month=next | Ferrara (FE) | html |
   circa 115 recite fino a maggio 2027 in un solo calendario.
4. Salerno Cultura | https://cultura.comune.salerno.it/eventi/ | Salerno (SA) | html | tutto il dicembre di Salerno
   (teatri, strada, Capodanno) con luoghi e prezzi, sito del Comune.
5. Comune di Piacenza | https://www.comune.piacenza.it/it/eventi | Piacenza (PC) | html (Municipium, come Roncade) |
   molti eventi con date, ore e luoghi.
6. Comune di Mantova | https://www.comune.mantova.it/it/eventi | Mantova (MN) | html (Municipium) | biblioteche,
   teatro, Capodanno.
7. Comune di Pistoia | https://www.comune.pistoia.it/it/eventi | Pistoia (PT) | html (Municipium) | 3 pagine di eventi.
8. Comune di Caltanissetta | https://www.comune.caltanissetta.it/it/eventi | Caltanissetta (CL) | html (Municipium) |
   concerti e Natale, provincia senza fonti.
9. Comune di Crotone | https://www.comune.crotone.it/vivere-il-comune/eventi/ | Crotone (KR) | html | 10 eventi futuri
   in prima pagina, provincia senza fonti.
10. Comune di Sondrio | https://comune.sondrio.it/eventi/ | Sondrio (SO) | html | Natale 2026 con date e ore.

## Lezioni
- WebSearch con `allowed_domains` su 3-5 siti comunali e la sola query "eventi dicembre 2026" porta dritto alle
  pagine eventi dei Comuni (1-3 fonti nuove a ricerca); le ricerche libere per teatro o citta' danno quasi solo
  aggregatori (iltaccodibacco, eventiesagre vietata, mentelocale) e PDF.
- Prova dell'API tribe (/wp-json/tribe/events/v1/events) con WebFetch: 2 su 7 siti WordPress di teatri rispondono
  (Udine, Pavia); costa una lettura e dice subito se la fonte va nel giro.
- Molti capoluoghi del Sud usano Municipium (Taranto, Foggia, Messina, Caltanissetta, Pistoia, Mantova, Piacenza):
  le pagine /it/eventi vanno bene per html_llm come Roncade; dove l'elenco eventi e' vuoto le iniziative stanno in
  /it/news.
- Le verifiche delle fonti da verificare stanno girando a vuoto: per ticketone.it, classicalive.it, allevents.in,
  balliamoliscio.it, canzoni.it e cheventi.it i termini non si trovano o non si aprono. Serve una lettura manuale di
  Federico (link nel footer) o un contatto: altri giri automatici sprecano ricerche.

## Problemi
- ticketone.it (15 trattenuti) e classicalive.it (9) restano da verificare: 503 e informativa introvabile.
- WebFetch non legge le pagine JavaScript (Calabria Straordinaria) e riceve 403 da Cagliari Turismo.
- Non ho potuto controllare il JSON-LD delle pagine (WebFetch toglie gli script): il tipo jsonld resta da provare dal giro.
