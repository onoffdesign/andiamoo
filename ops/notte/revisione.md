# Revisione, notte del 2026-11-28 (quarta prova)

Riscritto da capo. Lavoro fatto su `ops/posizioni.json`, `ops/revisione.json` e `ops/campione.json` generati alle 16:54
(1216 eventi controllati, 60 in coda, 20 di campione).

## Numeri
- Quota: 63 su 75. 7 WebSearch, 1 WebFetch e 55 letture di pagine ufficiali o di fonti ammesse dalla shell (curl,
  contate come WebFetch, una per pagina; tra queste il PDF dell'Autunno Sanfiorese letto con pdftotext). Fuori quota,
  come nelle prove precedenti: circa 230 interrogazioni a Nominatim (OpenStreetMap) dalla shell, con 1,1 secondi di
  pausa. Overpass non risponde dalla sessione (connessione chiusa o timeout su tre server).
- Posizioni: 105 luoghi nuovi in config/luoghi.yaml (da 165 a 270) e 1 luogo spostato (Cordignano); 4 punti singoli
  in lat/lon nelle correzioni, piu' 5 punti di eventi della coda e del campione.
- Coda di revisione: 60 lavorati su 60. Corretti 13, rimossi 0, verificati 40 (37 dopo la sistemazione del luogo o la
  lettura della fonte, 3 falsi allarmi di posizione). Ne restano 7 (vedi "Cosa resta").
- Campione: 10/20 corretti; 7 correzioni scritte, 11 verificati.
- Test di copertura: 4/20 (provincia di Padova), 6 eventi aggiunti in config/notte/revisione-eventi.yaml.
- File: config/notte/revisione-correzioni.yaml (24 correggi, 51 verificati, 0 rimuovi),
  config/notte/revisione-eventi.yaml (6 eventi), config/luoghi.yaml. `python -m pipeline.notte --controlla revisione`:
  parti valide.

## Posizioni
- Prima (16:54): luoghi con punti diversi 4 (in realta' 2, ognuno elencato due volte: Teatro comunale di Trevignano e
  Aula Magna della scuola di Cordignano), lontani dal comune 5 eventi, solo comune con luogo 293, solo comune senza
  luogo 29, candidati 13.
- Ricalcolo con gli stessi eventi dopo il lavoro (script sui file del repository, senza pubblicare): solo comune con
  luogo da 314 a 132 eventi, candidati da 13 a 0, punti diversi 0 dopo le correzioni (il ricalcolo non legge le
  correzioni della notte). Con le parti degli altri agenti unite dopo (1897 eventi): solo comune con luogo 177,
  candidati 37 (erano 51 prima dei 13 aggiunti per ultimi), lontani 61.
- Punti diversi: Trevignano, l'evento 4d45272078d3abc0 aveva un punto suo a 450 m dagli altri 9: ora quello di
  luoghi.yaml. Cordignano: Via Gazzari 1 e' la sede dell'istituto comprensivo, la scuola media e' in Via Vittorio
  Veneto 12 (tuttitalia.it): punto spostato sull'edificio della scuola (OSM way 234787583) e lo stesso punto
  nell'evento 521981068923ec69, che era a 700 m.
- Lontani dal comune, tutti falsi allarmi verificati: Lutago (frazione di Valle Aurina), Santa Maria in Stelle
  (frazione di Verona), Nevegal (Belluno), H-FARM (Ca' Tron, Roncade). Dopo l'unione delle parti degli altri agenti ne
  compaiono di nuovi, anche questi falsi allarmi: Teatro Toniolo e Teatro del Parco (Mestre, comune di Venezia, 50
  eventi), Santuario di Oropa (Biella), Scardovari (Porto Tolle). Da guardare: Centro polivalente di Longastrino,
  Via Bassa 59, scritto "Alfonsine" (Longastrino e' quasi tutta nel comune di Argenta, FE).
- Senza punto, i piu' frequenti per primi (tutti con l'oggetto di OpenStreetMap nella nota): Teatro Donizetti (33
  eventi), Teatro Sociale di Como con Foyer e Sala Bianca (30), Teatro Manzoni di Monza (14), Teatro comunale di
  Pergine con il Foyer Bepi Roner (9), Teatro Sociale di Bergamo (8), Teatro Grande di Brescia con il Ridotto (7),
  Parco del Donatore di Ramon (6, punto della via), Auditorium Santo Stefano di Farra e NOI Fontane (5 ciascuno, punto
  noto piu' vicino: la chiesa parrocchiale), Dosson, Ananda Marga, Piazza Marconi di Valdobbiadene, Mantova (Teatro
  Sociale, Bibiena, PalaUnical, Piazza Martiri di Belfiore), Pavia (Cineteatro Volta, biblioteche Bonetta, Ragazzi e
  Mirabello Scala, Palazzo centrale dell'Universita'), Varese (Villa Panza, Ippodromo, Museo Castiglioni), Bresso,
  Ossona, Usmate, Verona (Filarmonico, Duomo, San Michele Extra), Padova (Basilica del Santo, Piazza Capitaniato,
  Auditorium Pollini), Vicenza, Venezia, Belluno, Tarcento, Predaia, Seren del Grappa (Museo Secco, Via Marconi 19),
  Omate, e 25 luoghi della provincia di Treviso (Loggia dei Grani, Villa Correr Pisani, Duomo di Montebelluna, Palateatro
  e chiesa di Fontane, stadio del rugby di Villorba, Casa Giorgione, Piavon, Canottieri Sile, Palazzo Sarcinelli,
  Biancade, Solighetto, Piazza Rigo, Paderno, Campea, Grotte del Caglieron, ecc.).
- Candidati: tutti i 13 delle 16:54 (Teatro Comunale e Teatro di Gries di Bolzano, Teatro Sociale, Buonconsiglio,
  Roccabruna, piazze e Gallerie di Trento, Prealpi SanBiagio Arena, Piazza Raiffeisen, Morter) e 13 dei 51 comparsi
  dopo l'unione (Toniolo, Teatro del Parco, Thiene, Astra, Salieri, Regio di Torino, Comunale di Vicenza, Russolo,
  Modernissimo, Villa dei Leoni, Coccia, Marconi di Abano, Don Bosco di Chioggia), tutti con il punto comune degli
  eventi gia' pubblicati (controllato su OpenStreetMap, entro 200 m) per non creare punti diversi.
- Teatro Nuovo di Verona: punto nell'evento (4f6ca99deffbaeaa) e non in luoghi.yaml, perche' il nome e' contenuto in
  "Cinema-Teatro Nuovo di San Michele Extra".

## Coda di revisione (60)
- Corretti: accesso e prezzo di Albers a Villa Panza (intero 20 euro), Musicantica e Doppia esposizione a Trento
  (gratuiti), Dinosauri e DinoCuccioli 28 e 29/11 (3 euro), Alla scoperta di Pavia (ingresso libero con prenotazione
  obbligatoria), Tutte dormono sulla collina e Ateius a Pavia (gratuiti), Con tutto il rispetto a Taio (gratuito);
  luogo e indirizzo delle biblioteche di Pavia, dei Mercatini di Tarcento (IAT, Via Divisione Julia 13), di Natale a
  Pergine (Piazza Garibaldi, punto noto piu' vicino); prezzo "evento di beneficenza" di Canto di me stesso.
- Verificati: 31 eventi con il solo problema del luogo, ora risolto da luoghi.yaml; schede lette senza costo
  pubblicato (Tremlett, Cyclo-Cross, Limana, Bardies, Creazzo); nessun doppione vero tra i 4 "possibili doppioni"
  (Trento, Padova, Possagno: eventi diversi).

## Controllo a campione (20 eventi delle 16:54)
Corretti 10/20: Accensione dell'albero in Piazza dei Signori, parkrun Treviso, Mondi su carta a Fossalta, visita al
Buonconsiglio, Corso Mazzini 12/12 e 20/12, Un Natale di desideri a Oderzo, Bunny Club al New Age, Il Mago di Oz
alle Stimate, La magia dell'inchiostro a San Fior.
Errori (corretti tutti tranne la Marcia di Oderzo):
- luogo 7: punto sul centro del comune per Con tutto il rispetto (Predaia), La danza delle libellule e Boudchart
  (Bergamo), TeatrOrnago (Omate), Concerto di Natale al Santo (Padova), La zona rossa (Museo Secco); Marcia dei Babbi
  Natale di Oderzo senza luogo.
- accesso 2: Predaia (gratuito, era sconosciuto), visita in LIS al Museo Canova (gratuita con prenotazione, era
  biglietto).
- link 3: Nardo il ghepardo e Black Gold portavano alla pagina della rassegna di Gli Alcuni (ora la scheda); la
  Marcia di Oderzo ha come link un blog podistico che non da' luogo ne' orario: non corretto, da cercare la pagina
  dell'organizzatore.
- In piu': Boudchart ha anche una replica alle 20:30 del 12/12 che non e' sul sito.

Riga per la parte 3 (la scrive il coordinatore):
`- 2026-11-28 (notte, quarta prova) · corretti 10/20 · errori: data 0, orario 0, luogo 7, accesso 2, categoria 0, link 3 · lezione: sotto l'80% per il punto sul solo comune negli eventi delle fonti nuove di Lombardia e Trentino (teatri di Bergamo, Pavia, Omate, Predaia) e di Padova: sistemati con 105 luoghi nuovi; resta il link alla pagina della rassegna di Gli Alcuni invece della scheda dello spettacolo (seconda notte)`

## Test di copertura (provincia di Padova)
20 eventi presi in modo indipendente dall'elenco di Turismo Padova (turismopadova.it/eventi, pagine 1-3, non in
config/sources.yaml), cercati con `python -m pipeline.editorial --comune Padova` e nei file della notte.
- Presenti 4: Tony Gallo. Melancholy, Disney in concerto, La Traviata, Concerto di Natale al Santo.
- Mancanti 16: Vespri di Avvento a Santa Giustina, Sogniamo con OPSA&Friends, Accendiamo il Natale (Via Sette
  Martiri), Percorsi di Natale a Camposampiero, Dietro le quinte del Teatro Verdi, Parole e musica per Emergency,
  L'isola del Natale (Gli Alcuni a Padova, 28/11), Casa Conti, Nicola De Maria e la Transavanguardia, Jack e il
  fagiolo magico, Latin Mood, Amici della Musica con Beatrice Martin, Pleyel in duo, Le parole per dirla, Concerti per
  l'Avvento degli Amici della Musica, Miroirs di Andrea Rebaudengo.
- Aggiunti 6 (schede lette): OPSA&Friends, Dietro le quinte, Emergency, Latin Mood, Beatrice Martin, Nicola De Maria;
  senza orario dove la scheda non lo pubblica. Gli altri 10 restano da aggiungere (schede di turismopadova.it).
Riga per ops/espansione.md:
`- 2026-11-28 (notte, quarta prova) · PD · copertura 4/20 (test della revisione: 20 eventi dall'elenco di turismopadova.it pagine 1-3; presenti Tony Gallo, Disney in concerto, La Traviata, Concerto di Natale al Santo; 6 dei 16 mancanti aggiunti, restano Vespri di Avvento, Accendiamo il Natale, Percorsi di Natale a Camposampiero, L'isola del Natale, Casa Conti, Jack e il fagiolo magico, Pleyel in duo, Le parole per dirla, Concerti per l'Avvento, Miroirs) · criterio di saturazione: non valutato (non e' lunedi')`

## Cosa resta (per la notte dopo)
- In coda senza verifica: Andar per fiere (Collezione Salce: fonte ufficiale illeggibile, forse chiusa il 4/11), Human
  Atlas a Casa Robegan (link a iltaccodibacco, nessuna pagina ufficiale trovata con una ricerca), Mostra del libro di
  Ormelle (finisce oggi), feste del radicchio di Spresiano e Quinto senza luogo, Padernello (Piazza San Filippo Neri non
  in OSM), Sala Guarnieri di Pedavena, auditorium di Chiarano (Via Roma 65/a non in OSM), Liechtr'zeit a San Leonardo.
- Luoghi senza punto trovato: biblioteche di Farra, Paese e Maser, Scuola Luchesi di Silea (Via Cendon 23, via lunga
  in tre tratti), Cinema Teatro Manzoni di Paese (in OSM c'e' un "Cinema Multisala Manzoni" in Via della Costituzione,
  non confermato), IAT Treviso, Info Point di Cison (Piazza Brandolini 6), Sala Guarnieri; dopo l'unione Teatro Abbado
  di Ferrara (15), Biblioteca 0-18 di Cuneo (6), San Francesco di Alessandria (5).
- Candidati non messi per mancanza di riscontro in OSM: Teatro Vivaldi di Jesolo, Remondini di Bassano, Millepini di
  Asiago, Pascutto di San Stino, Serafin di Cavarzere; Teatro Alighieri di Ravenna (OSM da' solo la fermata).

## Lezioni
- Le schede dei Comuni con il modello AgID (Pavia, Trento, Predaia, Tarcento, Ornago, Chiarano) hanno sempre le
  sezioni "Dove" e "Costo": una lettura toglie insieme luogo e accesso sconosciuto. Il testo utile e' a fine pagina.
- I teatri delle fonti nuove (Donizetti, Sociale di Como, Manzoni di Monza) arrivano con indirizzo e civico giusti:
  Nominatim li trova subito per nome; conviene metterli in luoghi.yaml lo stesso giorno in cui entra la fonte.
- Per i candidati con punto gia' coerente si tiene il punto degli eventi pubblicati, non quello di OSM, anche se a
  150 m: altrimenti gli eventi futuri finirebbero in un punto diverso da quelli gia' sul sito.
- Un nome generico in luoghi.yaml ("Teatro Nuovo", "Soligo") cattura anche altri luoghi che lo contengono
  ("Cinema-Teatro Nuovo di San Michele Extra", "Farra di Soligo"): in quei casi meglio il punto nell'evento.
- oderzocultura.it risponde con una pagina anti-bot alla shell, WebFetch la legge.

## Problemi
- luoghi.yaml vale solo per gli eventi della redazione: gli eventi gia' sul sito presi da altre fonti (es. comune-silea)
  non lo usano, servono lat/lon nella correzione (fatto per la Biblioteca dei Liberi Pensatori).
- `ops/posizioni.json` elenca ogni luogo con punti diversi due volte (chiave del nome e chiave dell'indirizzo): i 4
  "punti diversi" erano 2.
- Campione al 50%, sotto l'80%: causa principale il punto sul solo comune dei luoghi delle fonti nuove, ora coperti.
