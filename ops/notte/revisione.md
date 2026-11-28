# Revisione, notte del 2026-11-28 (terza prova)

Riscritto da capo. Lavoro fatto sulla coda, sul campione e sulle posizioni generati alle 12:31 (60 eventi in coda, 20
di campione), come da piano. Durante il lavoro il coordinatore ha ripubblicato (16:24): `ops/revisione.json` ha gli
stessi primi eventi, `ops/campione.json` e' un campione nuovo di 20 eventi diversi (non controllato), `ops/posizioni.json`
e' cambiato e ho lavorato anche quello nuovo (candidati e nuovi luoghi in cima).

## Numeri
- Quota: 71 su 125. 4 WebSearch e 67 letture di pagine ufficiali o di fonti ammesse fatte dalla shell (curl, contate
  come WebFetch, una per pagina; tra queste un PDF del Comune di San Fior letto con pdftotext). Nessun WebFetch.
  Fuori quota, come l'altra volta: circa 130 interrogazioni a Nominatim (OpenStreetMap) dalla shell, con 3 secondi di pausa.
- Coda di revisione: 60 lavorati su 60. Corretti 39, rimossi 0, verificati 13. Ne restano in coda 8 (dati letti ma
  luogo senza punto trovabile o fonte non leggibile, vedi "Cosa resta").
- Campione: 3 correzioni, 15 verificati (2 eventi del campione erano anche in coda).
- Posizioni: un falso allarme "lontano dal comune" verificato (Nevegal), 49 luoghi nuovi in config/luoghi.yaml.
- Eventi aggiunti: 0.
- File: config/notte/revisione-correzioni.yaml (42 correggi, 28 verificati, 0 rimuovi), config/notte/revisione-eventi.yaml
  (vuoto), config/luoghi.yaml (+49 luoghi, ora 165). `python -m pipeline.notte --controlla revisione`: parti valide.

### Correzioni principali della coda
- Pordenone (11 schede del Comune lette una per una): accesso libero per Vibrazioni, Gala' della Magia, Balconi de Nadal,
  Sinfonie di luce, Concerto dell'Avvento in ospedale, Ugo di noi; la Mostra di presepi apre il 6/12, non il 5/12;
  Sinfonie di luce e' nella Chiesa dei Santi Ilario e Taziano; Craig David al Palazzetto dello Sport (biglietto);
  punto vero per Piazza XX Settembre (12 eventi, in OSM "Piazzale Venti Settembre"), biblioteca, Castello di Torre.
- Mattorosso: Top Hits 22-3 a ingresso gratuito (era tutto il giorno, accesso sconosciuto); contest dei tatuaggi dalle 18.
- Musei: Lipparini al Bailo e Italia Germania in Basilica a biglietto; Pensieri Preziosi (Padova) e Photography Changes
  Everything (Verona) gratuiti; Donne protagoniste al Bailo: visita 7 euro piu' l'ingresso ridotto.
- Punti nuovi per eventi con solo il comune: Teatro Verdi di Padova (10 eventi), Campostrini e Museo di Storia Naturale
  a Verona, Gallerie d'Italia e Santi Felice e Fortunato a Vicenza, Duomo e Piazza Grande di Oderzo, Piavon, Giardini di
  Sant'Andrea e Casa Robegan a Treviso, Altromercato (Dutch Nazari), Biblioteca di Ramon, Col San Martino, Soligo,
  Piazza Flaminio, Piazza Aldo Moro di Villorba, Montecchio Maggiore, Adria, Mussolente.
- Nessun doppione vero tra i 9 "possibili doppioni" della coda (Santa Lucia/Susegana, Ramon/Giavera/Farra, Villorba/
  Montebelluna, Piavon/Silea, Bailo/Canova, Eremitani/Vittorio Veneto: eventi diversi).

## Controllo a campione (20 eventi delle 12:31)
Corretti 15/20: Carlo Scarpa al Canova, Trasparente all'Ubik, Falstaff, Mercatini di Corso Mazzini 29/11 e 13/12,
Memoriale Brion, Nel cuore dei bambini, Aperitivo del New Age, concerto di San Fior (orario 17:30 dal PDF del Comune),
Tina Merlin e Camminata dei Babbi Natale (punto sul centro di Farra capoluogo, a 20 m dal municipio: luogo esatto non in
OSM, giudicati giusti), Notte al Museo di Udine, Gabriele Strata, Cantanatale, La Regina delle Nevi.
Errori (corretti tutti tranne il link morto):
- luogo 2: Speciale Natale a Casa Robegan e Quinzano 1 al Museo di Storia Naturale di Verona avevano il punto sul centro
  del comune (Verona a 700 m dal museo): ora punto da OpenStreetMap.
- accesso 2: Maurizio Solieri Gang (ingresso 18 euro con consumazione, era sconosciuto); La mia vera storia di Natale
  (biglietto 7 euro non riportato).
- link 2: La mia vera storia di Natale portava alla pagina della rassegna, che non elenca la data (ora la scheda
  dell'evento su live.alcuni.it); Danzando con il cuore (Belluno, 6/12): la scheda di Dolomiti Prealpi da' "pagina non
  trovata" e una ricerca non trova altre fonti. Non corretto: resta in coda, da ricontrollare (annullato?).
- Criterio usato: accesso "sconosciuto" non e' un errore quando la fonte ufficiale non lo pubblica (Ubik, San Fior,
  Cantanatale); e' un errore quando la fonte lo dice.

Riga per la parte 3 (la scrive il coordinatore):
`- 2026-11-28 (notte, terza prova) · corretti 15/20 · errori: data 0, orario 0, luogo 2, accesso 2, categoria 0, link 2 · lezione: dopo i luoghi nuovi della seconda prova il punto sul comune scende da 6 a 2 errori; restano l'accesso pubblicato dal locale ma non trascritto (Mattorosso, Gli Alcuni) e il link alla pagina della rassegna invece che alla scheda dell'evento; una scheda di Dolomiti Prealpi e' sparita (404), evento da ricontrollare`

## Posizioni
- Prima (ops/posizioni.json delle 12:31, 786 eventi): luoghi con punti diversi 0, lontani dal comune 1, solo comune con
  luogo 203, solo comune senza luogo 20, candidati 0. Alle 16:24 (917 eventi, con le parti degli altri agenti): 0 / 2 /
  242 / 30 / 4.
- Sistemati 49 luoghi in config/luoghi.yaml (coordinate di OpenStreetMap, oggetto citato nella nota), i piu' frequenti
  per primi: Piazza XX Settembre di Pordenone (12), Teatro Verdi di Padova (10), Teatro comunale di Falze' di Trevignano
  (9, punto della via), Giardini di Sant'Andrea (3), i 4 candidati (Teatro de la Sena di Feltre 6, Museo di Mel 4,
  Cinema Esperia di Padova 3, Sala consiliare di San Lorenzo Isontino 3), Museo di Storia Naturale e Santa Maria in
  Stelle (Verona), Piazza dei Signori di Vicenza, Villa Onigo, Musano, Centro sociale di Tambre, Centro polivalente di
  Monastier, Via Gazzari di Cordignano, biblioteca, Castello di Torre, ospedale e palazzetto di Pordenone, Duomo, San
  Francesco, Santa Maria Maggiore, Santa Caterina, Sant'Agnese, Casa Robegan, San Pelagio e altri luoghi di Treviso,
  Oderzo (Duomo, Piazza Grande, Museo Eno Bellis), Castello Roganzuolo, area fiera di Santa Lucia, ecc. In piu' 8
  punti singoli in lat/lon nelle correzioni (Col San Martino, Soligo, Piavon, Mussolente, Ramon...).
- Lontani dal comune: b33cc7b9cff4550c (Babbo Natale al Nevegal, 7 km) e' giusto, il Nevegal e' nel comune di Belluno
  (verificato); b665ec02e9b8accd (H-FARM, Ca' Tron) resta il falso allarme gia' noto.
- Dopo (stima, sugli eventi di docs/data/events.json): dei 244 eventi con luogo ma punto sul comune, 87 sono ora coperti
  da un luogo di config/luoghi.yaml; alla prossima pubblicazione: punti diversi 0, lontani 2 (entrambi falsi allarmi),
  solo comune con luogo circa 155, candidati 0.

## Test di copertura (provincia di Treviso)
20 eventi presi in modo indipendente dal calendario di Treviso Eventi (trevisoeventi.com, ammessa stanotte dall'agente
giro), una lettura: 16/20 gia' presenti, di cui 7 sul sito pubblicato e 9 solo in config/eventi_redazione.yaml
(aggiunti stanotte, compariranno alla prossima pubblicazione).
- Presenti: Festa del Radicchio di Spresiano, Olio in Villa a Maser, La Breda di Natale, Imoco - San Giovanni in
  Marignano, Natale a Collalto, Fiera dei Trovarobe a Badoere, Treviso - Arzignano, Mercatini di Valdobbiadene, Mostra
  mercato dell'antiquariato di Roncade, Benetton - Lyon, Concerto di Natale a Musano, Mercatino di Portobuffole', X-Mas
  Run, Mercatino di Godega, Treviso - Carpi, Imoco - Talmassons.
- Mancanti: "A Natale siamo tutti piu' buoni" a Paese (accensione dell'albero 29/11 alle 17:30 e programma fino al 20/12),
  Rudolph Operazione Natale al Cinema Teatro Manzoni di Paese (4/12 21:00), mostra di presepi La Grotta della Cometa
  nella chiesa antica di San Cipriano a Roncade (6/12-24/1), visite al Museo del Caffe' Dersut di Conegliano (12/12).
  Non aggiunti: una ricerca non ha trovato la pagina ufficiale (da cercare sul sito del Comune di Paese, fonte del giro).
Riga per ops/espansione.md:
`- 2026-11-28 · TV · copertura 16/20 (test della revisione, terza prova: 20 eventi dal calendario di trevisoeventi.com; 7 sul sito e 9 aggiunti stanotte in redazione; mancanti il Natale di Paese con Rudolph al Manzoni, i presepi della Grotta della Cometa a Roncade e le visite al Museo Dersut) · criterio di saturazione: non valutato (non e' lunedi')`

## Cosa resta (per la notte dopo)
- In coda senza verifica: Andar per fiere (Collezione Salce; l'unica scheda ufficiale e' su cultura.gov.it, illeggibile:
  un riassunto di ricerca parla di chiusura al 4 novembre, da controllare, forse da togliere); Danzando con il cuore
  (scheda sparita); Mercatini di Tarcento (luogo dichiarato "Via Divisione Julia 13", che OSM non ha a Tarcento);
  Chiarano (Via Roma 65/a non in OSM); Tina Merlin e Auditorium Santo Stefano di Farra (5 eventi); Giavera (Piazza
  Bacilieri); Parco del Donatore di Ramon (6 eventi, OSM ha solo Via San Pancrazio); Kinder Haus alla Galleria Concordia.
- Luoghi senza punto: NOI Fontane, Scuola di musica Luchesi di Silea, biblioteca di Farra, IAT Treviso, Info Point di
  Cison, oratorio di Soligo, biblioteca di Maser, Sala Guarnieri di Pedavena, Museo Secco di Seren: Nominatim non li
  trova; servono il sito del luogo o una scheda.
- Piazza Marconi di Valdobbiadene: OSM la mette a Funer, non sicuro: non aggiunta.
- Il campione nuovo delle 16:24 (20 eventi diversi) non e' stato controllato.

## Fonti nuove da catalogare
- Nome: Comune di Pordenone, schede evento del Natale · url: https://www.comune.pordenone.it/it/vivere-pordenone/eventi/
  · query: elenco su https://natale.comune.pordenone.it/ · tipo: comune (le schede hanno luogo, orari e "Costi" che
  l'elenco del portale natalizio non ha; da usare come official_url).
- Nome: Gli Alcuni, schede spettacolo · url: https://live.alcuni.it/evento/<titolo-gg-mm-aa>/ · query: pagina della
  rassegna https://live.alcuni.it/rassegna-una-fetta-di-teatro-treviso/ · tipo: teatro (la scheda ha data, ora e
  prezzo; la pagina della rassegna non elenca le date: non usarla come official_url).
- Nome: Treviso Eventi, calendario · url: https://www.trevisoeventi.com/calendario-eventi-treviso.htm · tipo:
  aggregatore ammesso (gia' nel catalogo): ottimo per il test di copertura, una lettura da' 30 eventi TV con date.

## Lezioni
- Le schede del Comune di Pordenone hanno sempre una sezione "Costi": leggerla toglie quasi tutti gli accessi
  sconosciuti del Natale di Pordenone.
- Nominatim non trova le piazze scritte con il numero romano ("Piazza XX Settembre"): in OSM sono spesso in lettere
  ("Piazzale Venti Settembre"); cercare con la parola "Settembre" e un riquadro sul comune.
- Le interrogazioni a Nominatim con riquadro sul comune (viewbox e bounded) evitano le omonime in provincia.
- Le pagine eventi di alcuni comuni (San Fior) hanno il programma solo in PDF allegato: si legge con pdftotext.
- teatroaccademia.it risponde con una pagina di controllo anti-bot: non si legge dalla shell.

## Problemi
- Coda e campione rigenerati a meta' lavoro (16:24): il campione nuovo non e' controllato.
- Le letture dalla shell sono contate nella quota (67); le interrogazioni a Nominatim no.
