# Agente fonti, notte del 2026-11-28 (sesto giro)

## Numeri
- Fonti da verificare del piano: 12. Nessuna nuova decisione su quelle del piano: 8 erano gia' decise (eventbrite.it,
  cosedicasa.com, fleamapket.com, canzoni.it, finishers.com vietate; balliamoliscio.it, eventivenetando.it,
  happyticket.com ammesse) e non le ho riaperte. Restano da verificare 4: ticketone.it, classicalive.it, 2night.it, cheventi.it.
- Altre fonti verificate cercando fonti nuove: marathons.com ammessa (caso limite), napolike.it e ahotu.com da verificare.
- Fonti nuove valutate e salvate in ops/fonti.yaml: 48 (da 320 a 368 voci): 45 siti ufficiali (Comuni, enti turistici
  regionali, circuiti teatrali, teatri, musei, biblioteche, un'associazione) e 3 aggregatori. 32 attive, 16 deboli.
  Per regione: Campania 9, Puglia 5, Basilicata 1, Calabria 3, Sicilia 6, Sardegna 4, Abruzzo 3, Molise 2,
  Emilia-Romagna 9, Piemonte 5, nazionali 2.
- Eventi aggiunti: 22 (config/notte/fonti-eventi.yaml). Correzioni: 0.
- Ricerche usate: 49 su 75 (WebSearch 23, WebFetch 26). Coordinate da Nominatim con la shell, fuori quota.
- `python -m pipeline.notte --controlla fonti`: "Parti valide". config/fonti-vietate.yaml e ops/fonti.yaml: YAML validi.

## Verifiche delle fonti (config/fonti-vietate.yaml)
- **ticketone.it** (15 trattenuti): robots.txt ancora 503 (sesto giro). Resta da verificare.
- **classicalive.it** (9 trattenuti): un'altra ricerca, nessuna pagina legale. Resta da verificare: serve che Federico
  copi a mano il link del footer.
- **2night.it**: non riaperta (il suo robots.txt blocca proprio le pagine legali). Resta da verificare.
- **cheventi.it**: non riaperta (in ops/domini-illeggibili.yaml; i termini davano 403). Resta da verificare.
- Gia' decise, non riaperte: eventbrite.it (vietata per decisione di Federico), cosedicasa.com, fleamapket.com,
  canzoni.it, finishers.com (vietate), balliamoliscio.it, eventivenetando.it, happyticket.com (ammesse).
- **marathons.com -> ammesse** (caso limite): robots.txt ("User-agent: * / Allow: /") e mentions legales letti
  (/fr/mentions-legales, che rimanda a legal.finishers.com/marathons/mentions-legales; editore Finish Line Media).
  Nessun divieto di scraping, estrazione automatica o TDM, ma vietate riproduzione e adattamento senza permesso
  scritto. Il gruppo e' lo stesso di finishers.com, che e' vietata: usarla solo per scoprire le gare e confermarle
  sul sito dell'organizzatore. Se Federico preferisce la prudenza basta spostarla in vietate.
- **napolike.it -> da_verificare**: robots.txt letto (blocca solo cartelle tecniche e /turismo/search/), pagina dei
  termini non trovata (/termini-e-condizioni 404, ricerca senza risultati).
- **ahotu.com -> da_verificare**: robots.txt 403 con WebFetch.
- Eventi di ops/da-verificare.json che possono tornare: **0**. Ticketone e classicalive restano da verificare; le
  altre fonti che trattengono eventi sono vietate.

## Fonti nuove salvate (ops/fonti.yaml; nome | url | tipo | provincia)
Campania
- Teatro Trianon Viviani | https://www.teatrotrianon.org/programmazione-stagione-20262027/ | teatro | NA (robots Allow /)
- Teatro Augusteo | https://www.teatroaugusteo.it/1/cartellone_2026_27_1365226.html | teatro | NA
- Teatro Diana | https://teatrodiana.it/category/eventi/ | teatro | NA
- Teatro Pubblico Campano | https://www.teatropubblicocampano.com/teatri/programma-teatro-verdi-salerno/ | ente (circuito) | Campania
- Museo Madre | https://www.madrenapoli.it/mostre/ | museo | NA
- Comune di Amalfi, notizie | https://comune.amalfi.sa.it/Novita/Notizie | comune | SA
- Comune di Ercolano (debole) | https://www.comune.ercolano.na.it/sito/ | comune | NA
- Napolike (da verificare) | https://www.napolike.it/ | aggregatore | NA
Puglia
- Viaggiare in Puglia | https://www.viaggiareinpuglia.it/it/eventi-attivita | ente regionale | Puglia (nessun robots.txt)
- Teatro Umberto Giordano | https://www.teatrogiordano.it/stagione/2026-2027.html | teatro | FG
- Comune di Monopoli, eventi | https://www.comune.monopoli.ba.it/Vivere-il-comune/Eventi | comune | BA
- Comune di Andria (debole) | https://www.comune.andria.bt.it/it/news | comune | BT
- Comune di Altamura (debole) | https://www.comune.altamura.ba.it/it | comune | BA
Basilicata
- Basilicata Turistica | https://www.basilicataturistica.it/eventi/ | ente regionale | PZ, MT (robots 503)
Calabria
- Fondazione Politeama Catanzaro | https://www.politeamacatanzaro.net/stagione-artistica-2026-2027/ | teatro | CZ (robots letto)
- Comune di Lamezia Terme, eventi | https://www.comune.lamezia-terme.cz.it/it/eventi | comune | CZ
- AMA Calabria (debole) | https://www.amacalabria.org/ | ente (circuito) | Calabria
Sicilia
- Teatro Stabile di Catania | https://www.teatrostabilecatania.it/stagione/stagione-2026-2027/ | teatro | CT (robots letto)
- Comune di Catania, avvisi (debole) | https://www.comune.catania.it/novita/avvisi/ | comune | CT
- Comune di Caltagirone, eventi | https://www.comune.caltagirone.ct.it/it/eventi | comune | CT
- Comune di Erice, notizie | https://www.comune.erice.tp.it/it/news | comune | TP
- Comune di Gela, eventi (debole) | https://www.comune.gela.cl.it/it/eventi | comune | CL
- Comune di Alcamo, eventi (debole) | https://comune.alcamo.tp.it/it/eventi | comune | TP
Sardegna
- Comune di Cagliari, portale | https://www.comune.cagliari.it/portale/ | comune | CA
- Comune di Quartu Sant'Elena, notizie | https://www.comune.quartu.ca.it/novita/news | comune | CA
- Comune di Sanluri (debole) | https://www.comune.sanluri.su.it/ | comune | SU
- Ente Concerti Marialisa de Carolis | https://www.marialisadecarolis.it/ | associazione | SS
Abruzzo
- Comune di Vasto (debole) | https://www.comune.vasto.ch.it/index.php/it | comune | CH
- Comune di Chieti, novita (debole) | https://comune.chieti.it/novita/ | comune | CH
- Biblioteca di Giulianova | https://biblioteca.comune.giulianova.te.it/ | biblioteca | TE
Molise
- Visit Molise | https://www.visitmolise.eu/ | ente regionale | CB, IS (robots letto, Disallow vuoto)
- Comune di Agnone (debole) | https://www.comune.agnone.is.it/ | comune | IS
Emilia-Romagna
- ATER Fondazione | https://www.ater.emr.it/it/teatri-e-stagioni | ente (circuito regionale) | Emilia-Romagna (robots letto)
- ERT Emilia Romagna Teatro | https://bologna.emiliaromagnateatro.com/la-stagione-2026-2027/ | teatro | BO, MO (robots letto)
- Rimini Turismo, calendario | https://riminiturismo.it/eventi/calendario | ente | RN (robots 503)
- Teatro Galli | https://teatrogalli.it/ | teatro | RN
- I Teatri di Reggio Emilia | https://www.iteatri.re.it/ | teatro | RE
- Teatro Stignani | https://www.teatrostignani.it/spettacoli/ | teatro | BO
- Biblioteche e Archivi di Ferrara | https://archibiblio.comune.ferrara.it/ | biblioteca | FE
- Comune di Imola, comunicati | https://www.comune.imola.bo.it/novita/comunicati/ | comune | BO
- Comune di Ravenna (debole) | https://comune.ravenna.it/ | comune | RA
Piemonte
- Comune di Asti, eventi | https://www.comune.asti.it/vivere-comune/eventi | comune | AT
- Comune di Biella, eventi | https://comune.biella.it/eventi/ | comune | BI
- Comune di Casale Monferrato, eventi | https://comune.casale-monferrato.al.it/eventi/ | comune | AL
- Comune di Pinerolo, eventi | https://www.comune.pinerolo.to.it/vivere-comune/eventi | comune | TO
- Comune di Ivrea, eventi (debole: 403 a WebFetch) | https://www.comune.ivrea.to.it/it/argomenti/eventi | comune | TO
Nazionali
- Marathons.com | https://www.marathons.com/it/ | aggregatore (ammessa, caso limite) | Italia
- Ahotu (da verificare) | https://www.ahotu.com/it/calendario | aggregatore | Italia

## Proposte per le fonti del giro (config/sources.yaml, le aggiunge il coordinatore)
1. Comune di Lamezia Terme | https://www.comune.lamezia-terme.cz.it/it/eventi | Lamezia Terme (CZ) | html (Design
   Comuni, schede con data, ora e indirizzo; JSON-LD da controllare) | stagione del Teatro Grandinetti.
2. Teatro Umberto Giordano | https://www.teatrogiordano.it/calendario.html | Foggia (FG) | html | data e ora in elenco.
3. Fondazione Politeama | https://www.politeamacatanzaro.net/stagione-artistica-2026-2027/ | Catanzaro (CZ) |
   WordPress: tribe_api da provare, altrimenti html | robots letto.
4. Teatro Stabile di Catania | https://www.teatrostabilecatania.it/stagione/stagione-2026-2027/ | Catania (CT) |
   WordPress (Yoast): tribe_api da provare, altrimenti html | robots letto.
5. Teatro Trianon Viviani | https://www.teatrotrianon.org/programmazione-stagione-20262027/ | Napoli (NA) | html
   (date senza orari) | robots Allow /.
6. Teatro Augusteo | https://www.teatroaugusteo.it/1/cartellone_2026_27_1365226.html | Napoli (NA) | html.
7. Viaggiare in Puglia | https://www.viaggiareinpuglia.it/it/eventi-attivita | Puglia | html (schede /dettaglio-evento/).
8. Basilicata Turistica | https://www.basilicataturistica.it/eventi/ | Basilicata | html (WordPress: tribe_api da provare).
9. Visit Molise | https://www.visitmolise.eu/ (schede /evento/-/d/dms/...) | Molise | html (Liferay).
10. ATER Fondazione | https://www.ater.emr.it/it/teatri-e-stagioni | Emilia-Romagna | html (una pagina per teatro).
11. ERT Emilia Romagna Teatro | https://bologna.emiliaromagnateatro.com/la-stagione-2026-2027/ | Bologna e Modena |
    WordPress: tribe_api da provare, altrimenti html.
12. Rimini Turismo | https://riminiturismo.it/eventi/calendario | Rimini (RN) | html (Drupal, senza parametri).
13. Comune di Pinerolo | https://www.comune.pinerolo.to.it/vivere-comune/eventi | Pinerolo (TO) | html (Design Comuni).
14. Comune di Asti | https://www.comune.asti.it/vivere-comune/eventi | Asti (AT) | html (Design Comuni).
15. Comune di Casale Monferrato | https://comune.casale-monferrato.al.it/eventi/ | Casale Monferrato (AL) | html.
16. Comune di Biella | https://comune.biella.it/eventi/ | Biella (BI) | html.

## Eventi aggiunti (config/notte/fonti-eventi.yaml, 22)
- Lamezia Terme, Teatro Grandinetti: Lo schiaccianoci (9/12), Nemici come prima (18/12), La notte del Gospel (27/12).
- Napoli, Museo Madre: inaugurazione della mostra Isabella Ducrot (3/12 ore 19, ingresso libero).
- Catania, Ridotto del Teatro Verga: tre letture animate "C'era due volte" (6, 13 e 20/12 ore 10, 5 e 2 EUR).
- Catanzaro, Teatro Politeama: Natale in casa Cupiello (6/12), Pinocchio (8/12), Circus Ronaldo Swing (19 e 20/12),
  Sergio Rubini (3/1), Concerto di Capodanno della Filarmonica della Calabria (5/1).
- Foggia, Teatro Giordano: Macy Gray (9/12), Falstaff (11 e 12/12), Rebecca Ferguson (22/12), InfernoItalia (27/12),
  Tombolata con Valerio Lundini (5/1), Lisistrata con Lella Costa (16/1).
- Amalfi, Piazza Duomo: Natale in Gospel (23/12 ore 19; accesso non indicato, lasciato "sconosciuto").
Coordinate da OpenStreetMap (Nominatim) per tutti. Nessuno era gia' sul sito.
Luoghi nuovi per config/luoghi.yaml (per revisione o coordinatore): Teatro Grandinetti, Via Colonnello Cassoli 45,
Lamezia Terme, 38.9730251, 16.3181544; Museo Madre, Via Luigi Settembrini 79, Napoli, 40.8551228, 14.2585862; Teatro
Verga, Via Giuseppe Fava 35, Catania, 37.5123857, 15.0716147; Teatro Politeama, Via G. Jannoni (indirizzo dal sito
ufficiale; OSM lo mette su Via Italia), Catanzaro, 38.9059508, 16.5944671; Teatro Umberto Giordano, Piazza Cesare
Battisti, Foggia, 41.4640308, 15.5462317.

## Lezioni
- WebSearch con allowed_domains su 7-10 siti di teatri dello stesso territorio rende piu' dei Comuni: 3-5 fonti buone a
  ricerca (Napoli, Emilia-Romagna). I circuiti regionali (ATER, Teatro Pubblico Campano, AMA Calabria, ERT) coprono
  molti teatri con una fonte sola.
- Al Sud molti Comuni mostrano ancora il programma di Natale 2025-26 (Caltagirone, Erice, Gela, Ercolano, Andria):
  catalogati come deboli, da riaprire a meta' dicembre.
- Le pagine eventi dei Comuni con Design Comuni (Lamezia Terme, Pinerolo, Asti) danno indirizzo completo e ora: le
  migliori per il giro.
- Aggregatori sportivi: marathons.com appartiene allo stesso gruppo di finishers.com (vietata), ma le sue note legali
  non hanno il divieto; prudenza.

## Problemi
- ticketone.it (15 trattenuti) e classicalive.it (9 trattenuti): sesto giro a vuoto. Altri tentativi automatici
  sprecano ricerche: serve un controllo manuale di Federico (pagina dei termini di Ticketone, link legale nel footer di classicalive).
- robots.txt in 503: basilicataturistica.it, riminiturismo.it (siti ufficiali, ammessi per categoria). comune.ivrea.to.it
  risponde 403 a WebFetch.
- Il Teatro Politeama di Catanzaro ha due date diverse per l'Harlem Gospel Choir (8/12 in un risultato di ricerca, 12/12
  ore 21 sulla pagina della stagione): non l'ho aggiunto.
