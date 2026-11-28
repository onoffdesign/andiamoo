# Agente giro, notte del 2026-11-28 (quinto giro)

(Riscritto da capo. Le 40 fonti del giro erano gia' state lette oggi: questo giro le ha rilette tutte con i raccoglitori
del progetto dalla shell (pipeline.fetch, che rispetta robots.txt e la regola fonti), senza spendere ricerche, e ha
confrontato in automatico gli eventi con il sito, la redazione e le parti degli altri agenti.)

## Numeri
- Eventi aggiunti in config/notte/giro-eventi.yaml: 48 (26 nei prossimi 30 giorni). `python -m pipeline.notte --controlla giro`: parti valide.
  Nessuna correzione (config/notte/giro-correzioni.yaml non creato).
  - Marche (Ancona), API di marche-teatro: 20 fuori cartellone non ancora sul sito (Teatro delle Muse, Ridotto, Teatro
    Sperimentale, Auditorium della Mole): Cognini 5/12, Ma tu sei la pianta 9/12, Genesis 14/12, Gospel Night 23/12,
    Una notte per Faber 9/1, Trio NefEsh 24/1, Michela Giraud 30/1, Ruggero de I Timidi 4/2, Novara 5/2, Shen Yun 6-9/2,
    Lindo Ferretti 22/2, Legend 24/2, 1886 Anima romantica 27/2 (solo data: API 17.30, testo 18.00), La sera dei miracoli
    2/3, Tiziano La Bella 5/3, Mezzanotte 6/3, Carofiglio 9/3, Imperatore 19/3, Crepet 20/3, Gio Evan 21/3.
    Non aggiunti: Massimo Ranieri (titolo "rinviato"), Shamzy (API 6/3, testo 17/4).
  - Lazio (VisitLazio, JSON-LD): 10: Emisferi CineFest a Ciampino 27-29/11, Novembre in Festa a Contigliano 28-29/11,
    Premio Camilla a Priverno 28/11, Street Food alla Sonninese 29/11, Sagra della Polenta a Rocca Massima 29/11 e a
    Capranica 4-13/12, Mosciarella a Capranica Prenestina 6/12, Pangiallo a Riano 6-8/12, Polentando a Manziana 6/12,
    Via dell'Olio a Nerola 6/12. Gli orari del JSON-LD di VisitLazio sono sfasati di un'ora rispetto al testo: usato il testo.
  - Veneto, Treviso: 13: Silea (mostra 80 anni di donne al voto 13/11-30/12 in Municipio, inaugurazione dello Stradon di
    Villa Tiepolo Passi 28/11, Biblio-filo' 15 e 22/12), San Biagio (Accendiamo il Natale 28/11), Sernaglia (5 laboratori
    STEM 2/12, 16/12, 20/1, 17/2, 24/3), Oderzo (Giovanna dei disoccupati al Cristallo 16/3), Roncade (Sile Classica,
    Sulle note dell'avventura 28/11), Altivole (visita FAI straordinaria al Memoriale Brion 28/11 ore 11).
  - Veneto, Belluno (Dolomiti Prealpi): 5: (S)parliamo di psicologia 20/12 e 24/1 a Santa Giustina, Mulino di Santa
    Libera 29/11, Cena Potteriana al Castello di Zumelle 7/12 (solo data), Katia Follesa al Teatro Buzzati 5/3.
- Fonti del giro lette: 40 su 40 (tutte con il fetcher dalla shell; 403 su teatro-bellini-napoli e gli-alcuni, gia'
  coperte sul sito fino a fine marzo). Date in ops/copertura.yaml sezione giro: gia' tutte al 2026-11-28, nessuna modifica.
- Fonti note riaperte (ops/fonti.yaml, ultimo_controllo 2026-11-28 da aggiornare): Sile Classica resa 1, FAI Memoriale
  Brion resa 1, Musei Civici Treviso 0, Visit Museum Treviso 0 (dicembre non ancora pubblicato; 403 al fetcher, letta
  con WebFetch), Auditorium Maserada 0, Malipiero Salotto Musicale 0 (finito il 21/11), Pro Loco Mogliano 0, Antica Fiera
  Santa Lucia 0 ("nessun evento programmato"), Il Mosaico Montebelluna 0, MyArteven 0, Biblioteca di Casale 0.
  Conservatorio Steffani e Bardin Garden Store: 403 al fetcher.
- Ricerche usate: 7 su 100 (5 WebSearch, 2 WebFetch). Le letture dalla shell
  (circa 90 pagine e API, piu' circa 40 richieste a Nominatim con pausa) non contano nella quota.

## config/sources.yaml
- Note aggiunte a comune-spresiano (l'API MyPortal da' solo 5 progetti annuali per giovani, nessun evento datato),
  dolomiti-prealpi (una cinquantina di eventi non sul sito ma importati da Feratel senza ora ne' luogo) e
  teatro-bellini-napoli (403 al fetcher). Nessuna fonte spenta.

## Da fare per il coordinatore
- Ancona e' nel piano di italia-b stanotte: prima di unire, guardare `--comune Ancona` per doppioni con i 20 di Marche Teatro.
- Sile Classica 28/11: la scheda ha data e ora strutturate "28 novembre 2026 ore 17:00" e il menu dice 28 novembre, ma il
  testo dice "Domenica 8 novembre": tenuto il 28/11. Iscrizioni su Eventbrite solo come ticket_url.
- Punti approssimati (da non mettere in luoghi.yaml senza verifica): Municipio di Silea (Via Don Minzoni 12, non in OSM)
  sul punto della biblioteca accanto (Via Don Minzoni 14); Stradon a Lanzago sul centro di Lanzago (OSM node 1482122473;
  Villa Tiepolo Passi e' in comune di Carbonera); Polo educativo di Sernaglia sul punto di Piazza Martiri della Liberta'
  (OSM way 887989433); Auditorium dell'Istituto Comprensivo di Roncade sul punto di Via Vivaldi (OSM way 72490073);
  Piazza Tobagi di San Biagio sul municipio (Via Postumia Centro 71, 45.68505, 12.37724, da una ricerca); Rocca Massima e
  Capranica Prenestina al centro del comune di config/comuni.csv; Ciampino Il Piccolissimo senza civico.

## Luoghi nuovi (nome | comune | indirizzo | lat, lon | fonti)
- Mulino di Santa Libera | Santa Giustina | Via del Mulino 4, Salzan | 46.0784837, 12.0496905 | dolomitiprealpi.it + OSM node 6169429754
- Centro culturale di Santa Giustina | Santa Giustina | Via Cal de Formiga 31 | 46.0805572, 12.0383704 | dolomitiprealpi.it + OSM way 212902968 (in OSM su Via Pulliere)
- Castello di Zumelle | Borgo Valbelluna | Via San Dona' 4, Mel | 46.0363063, 12.0814015 | dolomitiprealpi.it + OSM way 161233967
- Auditorium Orfeo Tamburi, Mole Vanvitelliana | Ancona | Banchina Nazario Sauro 28 | 43.61437, 13.50442 | marcheteatro.it + OSM relation 11877 (stesso punto degli eventi gia' sul sito)
- Ridotto del Teatro delle Muse | Ancona | Piazza della Repubblica | 43.6195966, 13.5101245 | stesso edificio del Teatro delle Muse
- Abbazia di Fossanova (Infermeria dei Conversi) | Priverno | Via San Tommaso d'Aquino | 41.4383229, 13.195651 | visitlazio.com + OSM relation 2854335
- Cineteatro Il Piccolissimo | Ciampino | Via Ludovico Ariosto | 41.8038696, 12.6041789 | OSM node 4257289831 (VisitLazio scrive Largo Felice Armati 1, il Comune)
- Parco di Villa Franceschini | Contigliano | Via Ettore Franceschini | 42.4094752, 12.7727376 | visitlazio.com + OSM way 371346706
- Piazza Garibaldi | Sonnino | Piazza Giuseppe Garibaldi | 41.4141931, 13.2419263 | visitlazio.com + OSM way 392466441
- Piazza Piombino | Riano | Piazza Piombino | 42.0913249, 12.5224818 | visitlazio.com + OSM way 209542060
- Piazza Tommaso Tittoni | Manziana | Piazza Tommaso Tittoni | 42.129379, 12.1328486 | visitlazio.com + OSM relation 18267858
- Corso Francesco Petrarca | Capranica | Corso Francesco Petrarca 40 | 42.256669, 12.1780278 | visitlazio.com + OSM way 454009835
- Corso Umberto I | Nerola | Corso Umberto I 15 | 42.161662, 12.7869036 | visitlazio.com + OSM way 391606445 (punto della via)

## Fonti nuove da catalogare (per l'agente fonti)
- Nessuna fonte nuova usata. Da guardare: amicimusica.an.it (Societa' Amici della Musica di Ancona, pagine evento con
  programma), query "Amici della Musica Ancona stagione", tipo associazione; teatroverdimontecatini.it compare come
  produttore, non aperto.

## Lezioni
- I raccoglitori del progetto (pipeline.collectors tribe, jsonld, myportal, podismoveneto) si possono eseguire dalla shell
  con uno Store nello scratchpad e llm=None: danno gli eventi strutturati senza spendere ricerche, e il confronto
  automatico titolo+data con docs/data/events.json trova i mancanti. Le pagine html_llm si leggono con
  Fetcher.get + html_to_text. Stanotte 40 fonti lette con 0 ricerche.
- Marche Teatro: la pagina della stagione copre prosa e danza, l'API ha anche i fuori cartellone (concerti, comici,
  conferenze): l'API va letta per intero.
- Dolomiti Prealpi: il giro precedente aveva detto "gia' tutto sul sito" guardando la prima pagina; il confronto completo
  mostra una cinquantina di eventi mancanti, quasi tutti pero' senza luogo ne' ora (import Feratel).
- Nominatim risponde con liste vuote (non errori) a raffica di richieste: tenere almeno 3 secondi tra una e l'altra.
  Overpass dal proxy cade a meta'.
- Silea: robots.txt ora non vieta nulla (Disallow vuoto), le schede /eventi/<nome>.html si leggono.

## Problemi
- Nessuno bloccante. Il curl dalla shell oggi funziona (al giro precedente era negato dai permessi).
