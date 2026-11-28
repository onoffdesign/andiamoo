# Agente giro, notte del 2026-11-28 (seconda sessione, quinto giro)

Le mie parti sono in config/notte/n2giro-eventi.yaml e config/notte/n2giro-correzioni.yaml (i file giro-*.yaml
sono stati sovrascritti dall'altra sessione; il coordinatore ha copiato le mie parti nei file n2giro). Copia di
riserva anche nella scratchpad della sessione.

## Numeri
- Eventi in n2giro-eventi.yaml: 32 (tutti nei prossimi 30 giorni tranne la mostra di Maenza, che arriva al 6/1).
  `python -m pipeline.notte --controlla n2giro`: parti valide. Ne ho scritti 42; 10 li ho tolti perche' l'altra sessione
  li aveva gia' uniti in eventi_redazione (Emisferi Ciampino, Riano, Manziana, Nerola, Contigliano, Priverno, Rocca
  Massima, Mosciarella, Sonnino, Giovanna dei disoccupati a Oderzo).
  - VisitLazio: 12 (Polentazza di Civitella d'Agliano 27-29/11 e 4-6/12, Bassano in Teverina 6/12 e 8/12, Sagra della
    polenta di Proceno 28-29/11, Allumiere 28/11 e 29/11, Scampanata di Sant'Andrea a Latera 30/11, mostra Lipperi a
    Carbognano fino al 30/11, Incanto di Natale a Montalto di Castro 5/12, Echi di Valle Santa a Poggio Bustone 28/11 e
    a Greccio 20/12) piu' Il Natale delle Favole al Castello di Maenza (6/12-6/1, date dal sito ufficiale amaenza.com).
  - Calendario Podismo Veneto: 19 gare del 29/11 e del 6/12 fuori dalla provincia di Treviso (PD, VE, VI, VR, RO), che il
    collettore teneva solo per TV. I volantini sono immagini: niente ritrovo, punto sul centro del comune o della frazione
    (OSM), scritto nella nota. Fossò 29/11 non aggiunta: la scheda dice 28/11, l'elenco 29/11.
- Correzioni in n2giro-correzioni.yaml: 6 spettacoli del Teatro Cristallo di Oderzo (ora 21 al posto di "tutto il giorno",
  prezzi 15 o 20 euro dalle schede; Buena Vista Social Club e Velvet Dress passati a musica > concerti).
- Fonti del giro lette: visit-lazio, podismoveneto, qdpnews, mattorosso, teatro-cristallo-oderzo, teatro-del-pane,
  libreria-san-leonardo (7 su 40). Le altre trevigiane erano gia' state lette quattro volte oggi e le tre riaperte erano
  sature (Mattorosso 32 eventi tutti sul sito, Teatro del Pane tutto sul sito, Qdpnews solo la Magia del Natale di
  Conegliano gia' sul sito): non ho speso altro. Le date in ops/copertura.yaml sezione giro erano gia' 2026-11-28.
- Fonti note da riaprire in ops/fonti.yaml: nessuna in scadenza secondo frequenza.
- Ricerche usate: 77 su 100 (3 WebSearch, 74 WebFetch, di cui 30 a Nominatim e 2 a Overpass falliti).

## Da fare per il coordinatore
- Teatro Cristallo, Casanova Grand Tour (uid 28021fe1411fe6df): sul sito il 15/1; l'elenco del teatro dice venerdi' 15
  gennaio, la scheda dice giovedi' 28 gennaio ore 21. Non corretto: da verificare.
- Non aggiunti per date in conflitto sulla stessa pagina VisitLazio: Favole di Luce a Gaeta (27-29/11 nel riquadro,
  8/11-11/1 nel testo, 10/1 secondo un articolo), Sagra della Polenta a Capranica (4-8 o 4-13/12; l'altra sessione l'ha
  gia' messa dal 4/12), Riano convegno "venerdi' 6 dicembre" (il 6/12 e' domenica).
- config/sources.yaml: aggiunta alla nota di visit-lazio (calendario leggibile solo fino al 6/12, date delle schede da
  controllare). libreria-san-leonardo: WebFetch di /notes da' ancora solo il catalogo del negozio (vedi nota gia' presente).
- podismoveneto: la pagina "Anno 2027" non ha ancora le pagine di gennaio-marzo; da riaprire tra qualche settimana.

## Luoghi nuovi (nome | comune | indirizzo | lat, lon | fonti)
Coordinate di OpenStreetMap (Nominatim letto con WebFetch), indirizzi da VisitLazio o dal sito ufficiale.
- Castello Baronale di Maenza | Maenza | Piazza Fernando Lepri | 41.5236242, 13.1810885 | amaenza.com + OSM way 198798863
- Santuario di Poggio Bustone | Poggio Bustone | Via Francescana 9 | 42.5044977, 12.8925546 | visitlazio.com + OSM node 7704423453
- Santuario di Greccio | Greccio | Via Limiti Nord 17, Limiti di Greccio | 42.4617193, 12.7513267 | visitlazio.com + OSM way 66106620
- Piazza della Liberta' | Proceno | Piazza della Liberta' 1 | 42.7572366, 11.8303932 | visitlazio.com + OSM way 416935323
- Piazza della Repubblica (Municipio e Palazzo della Camera Apostolica) | Allumiere | Piazza della Repubblica 39 | 42.1564178, 11.9021206 | visitlazio.com + OSM way 385819733
- Piazza della Rocca | Latera | Piazza della Rocca 2 | 42.6262502, 11.8285186 | visitlazio.com + OSM way 1072028105
- Piazza Giacomo Matteotti | Montalto di Castro | Piazza Giacomo Matteotti 11 | 42.3534062, 11.6041015 | visitlazio.com + OSM way 842605046
- Piazza Piombino | Riano | Piazza Piombino | 42.0913249, 12.5224818 | visitlazio.com + OSM way 209542060
- Piazza Tommaso Tittoni | Manziana | Piazza Tommaso Tittoni | 42.129176, 12.1329804 | visitlazio.com + OSM way 77951783
- Il Piccolissimo | Ciampino | Largo Felice Armati 1 | 41.8028104, 12.6019279 | visitlazio.com + OSM node 3357430995
- Parco di Villa Franceschini | Contigliano | Via Ettore Franceschini 7 | 42.4094752, 12.7727376 | OSM way 371346706
- Abbazia di Fossanova (Infermeria dei Conversi) | Priverno | Piazza Giovanni XXIII, Fossanova | 41.4383229, 13.195651 | OSM relation 2854335
- Piazza Giuseppe Garibaldi | Sonnino | Piazza Garibaldi 1 | 41.4141931, 13.2419263 | OSM way 392466441
Punti approssimati (non per luoghi.yaml): Civitella d'Agliano Piazza Cardinale Dolci, Carbognano Scuderie Farnese,
Rocca Massima Via del Municipio, Capranica Prenestina Piazza Frezza al centro del comune (Nominatim non li trova);
Bassano in Teverina sulla fermata "Piazza Liberta'" (OSM node 2267108546); le gare venete sul centro di comune o frazione.

## Fonti nuove da catalogare (per l'agente fonti)
- Associazione Maenza (Il Natale delle Favole) | https://amaenza.com/eventi/ | query "amaenza eventi Maenza" | associazione, ammessa; calendario caricato da script
- Santuari della Valle Santa | https://www.santuarivallesanta.com/2026/11/05/echi-di-valle-santa/ | query "Echi di Valle Santa santuari" | ente religioso, rassegna concerti (non aperta)

## Lezioni
- Overpass (overpass-api.de e kumi) non risponde a WebFetch (503 e timeout): per le coordinate resta Nominatim, un luogo per chiamata.
- VisitLazio: il calendario si legge solo fino a una settimana avanti; le schede hanno spesso due date diverse
  (riquadro e testo): prendere solo quelle confermate dal sito ufficiale.
- Calendario Podismo Veneto: con l'area tutta Italia rende di nuovo (19 gare in una lettura fuori TV), ma i volantini
  sono immagini senza testo: il ritrovo non si legge.
- Due sessioni sullo stesso percorso di file si sovrascrivono: controllare con --cerca anche gli eventi appena uniti.

## Problemi
- Le parti giro-*.yaml sono state sovrascritte dall'altra sessione a meta' lavoro (risolto dal coordinatore con n2giro).
