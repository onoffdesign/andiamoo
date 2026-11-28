# Revisione, notte del 2026-11-28 (sessione della sera)

Riscritto da capo. Lavoro fatto su `ops/posizioni.json` (17:58), `ops/revisione.json` (60 in coda) e `ops/campione.json`
(20 eventi). Nessuna voce di `ops/senza-posizione.json` (era vuoto).

## Numeri
- Quota: 72 su 75 (8 WebSearch, 64 WebFetch). Tra le WebFetch, 24 interrogazioni a Nominatim (OpenStreetMap) e 3
  tentativi a vuoto su Overpass (timeout e 503: non usarlo). All'inizio circa 30 interrogazioni a Nominatim dalla
  shell, poi fermate perche' il permesso e' stato negato: da li' in avanti solo WebFetch, contate nella quota.
- Posizioni: 46 luoghi nuovi in config/luoghi.yaml (7 dai candidati, 39 dai senza punto e dalla coda), 2 punti
  singoli in lat/lon nelle correzioni, 11 luoghi "lontani dal comune" controllati (falsi allarmi, nessuna modifica).
- Coda di revisione (file delle 19:57): 27 su 60 chiusi con una voce (11 correggi, 16 verificati); altri 4 hanno ora il
  punto da luoghi.yaml ma l'accesso non e' stato letto. Ne restano 33, quasi tutti teatri di Bologna e Modena con accesso
  sconosciuto.
- Campione: 12/20.
- Test di copertura: 7/20; 1 evento aggiunto in config/notte/revisione-eventi.yaml.
- File: config/notte/revisione-correzioni.yaml (21 correggi, 0 rimuovi, 28 verificati), config/notte/revisione-eventi.yaml
  (1 evento), config/luoghi.yaml (46 voci con "aggiunto il 2026-11-28 (revisione)"; la prima parte e' gia' entrata nel
  commit ed86f12 del coordinatore). `python -m pipeline.notte --controlla revisione`: parti valide. Test: 96 passati.

## Posizioni
- Prima (ops/posizioni.json delle 17:58, 2211 eventi): punti diversi 0, lontani dal comune 62 eventi, solo comune con
  luogo 205, solo comune senza luogo 28, candidati 8.
- Stesso calcolo rifatto sul repository attuale (2400 eventi, con quelli aggiunti dopo le 17:58): solo comune con luogo
  da 261 a 172 (89 eventi ora con il punto), candidati da 8 a 0, punti diversi 0, lontani 62 (invariati: sono falsi
  allarmi).
- Senza punto, sistemati (OSM = Nominatim, con l'oggetto nella nota): Teatro Comunale Abbado di Ferrara (15 eventi),
  Biblioteca 0-18 di Cuneo (6), Teatro delle Passioni di Modena (6, ingresso in Via Peretti 9 dal pieghevole di ERT),
  Ex complesso di San Francesco di Alessandria (5), Barbisano (4, punto della frazione), Reggio Emilia Welcome IAT-R
  (3), Sant'Artemio di Treviso, ZolAuditorium, Biblioteca Calvo di Alessandria, Cortile del Broletto di Novara, Museo
  Garda di Ivrea (punto della piazza), Palazzo Reale di Crespano (punto della piazza), MAUTO, OGR, Palazzo Barolo e
  Galleria Sabauda a Torino, Palazzo Oropa e Piazza Monsignor Rossi a Biella, Piazza Alfieri ad Asti, Museo Civico di
  Bassano (Wikipedia).
- Punto noto piu' vicino (luogo gia' in luoghi.yaml o punto coerente di altri eventi, scritto nella nota): Chiostro di
  San Mercuriale, Biblioteca Capitolare e Piazza Duomo di Treviso, Borgo Cavour, parrocchia di Catena, Mostra del vino
  di Col San Martino, Piazza Caduti nei Lager di Farra (parcheggio dell'Auditorium, dal calendario del Comune), chiesa
  di Ramon, Biblioteca Cozzi di Zero Branco, San Michele Extra, Cortile Federico II di Cremona, Piazza Martiri di
  Reggiolo, Piazza XX Settembre di Lecco, Piazza della Vittoria e Corso Garibaldi di Reggio, Via Cavour di Padova,
  centro storico di Vicenza; centri di Roncade, Segusino, Villorba e Asolo (centro del comune ISTAT o piazza gia' nota).
- Candidati: tutti gli 8 aggiunti (Piazza Garibaldi di Sondrio con il "Centro di Sondrio", Piazza Saffi, Piazza della
  Repubblica di Misano, Piazza Prampolini, Piazza San Prospero, Piazza Ghiaia, Piazza Gramsci di Alfonsine), ognuno
  controllato contro un luogo gia' noto o il centro del comune (entro 200 m).
- Lontani dal comune, tutti falsi allarmi: Teatro Toniolo e Teatro del Parco (Mestre, comune di Venezia, 50 eventi),
  Santuario di Oropa (Biella), H-FARM e Auditorium H-Farm (Ca' Tron, Roncade), Santa Maria in Stelle (Verona), Nevegal
  (Belluno), Scardovari (Porto Tolle), Lutago (Valle Aurina), Fiere di Parma (6 km, zona fiera a nord della citta').
  Da guardare ancora: Centro polivalente di Longastrino, Via Bassa 59, scritto "Alfonsine" (Longastrino e' divisa tra
  Argenta e Alfonsine, non verificato).
- Restano senza punto, i piu' frequenti: Biblioteca di Farra di Soligo (4), Scuola di musica Luchesi di Silea (4,
  Nominatim trova solo la via), Biblioteca di Paese (4) e Cinema Teatro Manzoni di Paese (3), stand di San Martino di
  Colle Umberto (3), Villa Romivo di Montebelluna (3), stand di Vedelago (3), Piazza Mazzini di Lecco (3: Nominatim da'
  la piazza omonima di Casatenovo, da evitare), Auditorium Vidotto di Maserada (3), Santa Maria del Sile (3), Giardini
  Pubblici di Forli' (2). Le ricerche sulle biblioteche dei piccoli comuni trevigiani non hanno dato l'indirizzo.

## Coda di revisione (60)
- Corretti: accesso e prezzo di Macbeth (Ferrara), Il ragazzo dai pantaloni rosa (Valli), Bancal (Fabbri), L'esecuzione
  (Pavarotti-Freni), Age (Storchi, anche l'orario 20:30), La scuola di magia (ZolAuditorium), Tiepolo alla Galleria
  Sabauda, Banksy a Palazzo Barolo, Kusama alle OGR (tutti a biglietto con i prezzi); concorso Cappuccilli al Ridotto
  del Ponchielli (ingresso libero); Magico Paese di Natale di Asti (gratuito).
- Verificati sulla fonte, senza prezzo pubblicato: mercatino, pista e Giardini di Luce di Forli', mercatino e Cortile
  Federico II di Cremona, mercatino di Lecco, accensione delle luci di Sondrio, Monet al Teatro Due, le 6 mostre e la
  pista di Reggio Emilia (date di fine giuste), Saetta McQueen al MAUTO.
- Risolti dai luoghi nuovi (punto): Ivrea (2), Alessandria (Calvo), Biella (pista), Zola, Ferrara, Torino.
- Falsi allarmi chiusi: Teatro del Parco (Mestre, comune di Venezia), "possibili doppioni" tra eventi di citta' diverse
  (Verona e Castelfranco, Padova e Sondrio).
- Restano (33): Giardini Pubblici di Forli' (2, senza punto), Winter Park di Cremona (senza punto), Natale sotto le mura
  di Castelfranco, Mostra del Libro di Ormelle, Padernello, Ivrea, Alessandria e Biella (punto sistemato, accesso non
  letto), Galleria del Liceo di Treviso, Salce, Castello di Novara, Cuneo, Teatro Due, Coccia, Oleggio, Storchi
  Ridotto, mercatino di Modena, radicchio di Spresiano, e i teatri e musei di Bologna e Casalecchio (culturabologna ed
  ERT, accesso sconosciuto, non letti per quota).

## Controllo a campione (20 eventi)
Corretti 12/20 · errori: data 0, orario 1, luogo 6, accesso 4, categoria 0, link 1.
Giusti: Serial Singers a Modena, Rassegna degli artisti di Ramon, L'elefantino a Piacenza, Prima della Scala a Sondrio,
Innuendo a Belluno, mercatini di Valdobbiadene, Marco Polo a Bolzano (aggiunto il prezzo), Madre per sempre a San Dona',
I tre pini di Natale a Farra, Aperitivo della Vigilia a Montebelluna, Presepi d'autore a Forli', Domenica in mostra al
Canova (aggiunto il prezzo).
Errori (tutti corretti tranne dove detto):
- luogo 6: Memorial Frazzoni (ZolAuditorium) e Anna Oxa (Teatro Abbado) sul centro del comune, ora in luoghi.yaml;
  Fiati all'opera (chiesa di Ramon) e La Magia del Dono (Portici di Palazzo Oropa), ora in luoghi.yaml; Babbo Run di
  Revine Lago senza luogo (scritto "Area polifunzionale di Revine", manca il punto); incontro sulla sicurezza di
  Sernaglia senza luogo (la fonte non lo dice).
- accesso 4: Palazzo Magnani (15 euro), Giselle (da 12,50 euro), Memorial Frazzoni e Anna Oxa (a pagamento), scritti
  "sconosciuto" mentre la fonte dava il prezzo.
- orario 1: Babbo Run, le 10:00 non compaiono sulla pagina (non corretto).
- link 1: incontro di Sernaglia senza link (ora la scheda del Comune).
- La Magia del Dono di Biella: la pagina del Comune non contiene il programma (rimanda a un PDF), contenuto non
  verificato.
Lezione: sotto l'80% per le stesse due cause delle notti scorse, il punto sul solo comune per i teatri e le sale delle
province nuove (Emilia, Piemonte) e l'accesso lasciato "sconosciuto" quando la scheda del teatro pubblica i prezzi.
Proposta per la parte 1 (la scrive il coordinatore): chi aggiunge eventi da schede di teatri legge anche la riga dei
prezzi e scrive access: biglietto e price; "sconosciuto" solo se la scheda non ne parla.

## Test di copertura
7/20. Eventi presi da due elenchi non presenti in config/sources.yaml:
- PDF di iltaccodibacco.it/asiago (provincia di Vicenza), 12 eventi, 0 sul sito: The Huntrix Experience a Bolzano
  Vicentino, mostra di Salgado al Museo Civico di Bassano (aggiunta stanotte, dal sito finestresullarte.info), Genesis e
  ABBAdream e Celentano e Maccio Capatonda alla CMP Arena, Dire Straits Reload e Concato e Morricone e Awed al Teatro
  Astra di Schio, Morricone e Caccamo al Jacopo da Ponte. Non aggiunti: per i concerti si trovano solo TicketOne e
  aggregatori, quasi tutti oltre i 30 giorni.
- Programma del Natale del Comune di Lecco, 8 eventi, 7 sul sito (manca l'apertura del villaggio "Natale tra Lago e
  Monti" del 5/12). Nota: l'elenco e' gia' la fonte di altri eventi del sito, quindi questa parte del test e' meno
  indipendente.
- Da controllare: lo Schiaccianoci del 17/12 a Lecco e' sul sito al Teatro della Societa', il Comune lo scrive al
  Teatro Cenacolo Francescano. Non corretto (nel dubbio).

## Lezioni
- WebFetch apre anche indirizzi non comparsi nei risultati (Nominatim, Wikipedia, schede note): Nominatim con
  "via e civico, comune" trova quasi sempre il punto nelle citta' (Torino, Novara, Alessandria, Zola, Biella), quasi mai
  per nome del luogo o nei paesi piccoli (Silea, Paese, Farra, Lecco). Overpass non risponde.
- I PDF salvati da WebFetch si leggono con pdftotext (elenchi di iltaccodibacco.it).
- Molti luoghi si sistemano senza ricerche: lo stesso posto ha gia' un punto in un altro evento con un nome diverso
  (abbazia e chiostro, piazza e palazzo comunale). Conviene confrontare per parole del nome e dell'indirizzo prima di
  cercare.
- Gli eventi il cui luogo e' cambiato in config/correzioni.yaml restano sul centro del comune anche se il luogo e' in
  luoghi.yaml (la pubblicazione non ricalcola il punto dopo la correzione): servono lat e lon nella correzione
  (Tarcento, Zero Branco). Possibile miglioria del codice.

## Problemi
- Shell: l'accesso a Nominatim da riga di comando e' stato negato dai permessi a meta' lavoro; usate solo WebFetch.
- Fonti nuove viste: nessuna da catalogare. cosedicasa.com e' gia' vietata (comparsa nei risultati, non aperta);
  TicketOne compare nei risultati per i concerti del test (non aperta).
- Approvazioni chieste: nessuna, a parte il permesso negato per le richieste a Nominatim dalla shell.
