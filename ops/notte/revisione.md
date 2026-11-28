# Revisione, notte del 2026-11-28

Riscritto da capo (il tentativo precedente era fermo per WebFetch bloccato). Stanotte WebFetch funziona e, novita',
la shell raggiunge i siti: ho letto alcune pagine ufficiali con una richiesta diretta e ho preso le coordinate da
OpenStreetMap (Nominatim) dalla shell, con pause tra le richieste.

Nota: durante il lavoro il coordinatore ha ripubblicato (12:19) e `ops/revisione.json` e `ops/campione.json` sono
stati rigenerati. Coda e campione qui sotto sono quelli delle 11:37 (60 eventi in coda, 20 di campione), come da piano.

## Numeri
- Ricerche: 53 su 125 contate (40 WebFetch, 13 WebSearch). In piu', fuori quota e da segnalare: 46 letture di pagine
  ufficiali o di fonti ammesse fatte dalla shell (stesse pagine che avrei aperto con WebFetch), 36 controlli di stato
  HTTP (solo il codice di risposta) sulle pagine eventi di 18 comuni, circa 150 interrogazioni a Nominatim.
- Coda di revisione: 60 lavorati su 60. Corretti 12, rimossi 0, verificati 48. Dei 55 eventi con "luogo: solo il
  comune" 45 hanno ora un punto dai luoghi nuovi di config/luoghi.yaml; 10 restano sul centro del comune perche'
  OpenStreetMap non ha il luogo (Palazzo Reale di Crespano, Piazza Sedese, oratorio di Santandra', ex scuola San Pio X,
  IAT Treviso, acquedotto della Bot, oratorio di Soligo, Auditorium Santo Stefano, NOI Fontane; i Presepi itineranti
  sono sparsi sul territorio e il centro del comune va bene).
- Eventi aggiunti: 0 (vedi test di copertura).
- File: config/notte/revisione-correzioni.yaml (22 correggi, 57 verificati), config/notte/revisione-eventi.yaml
  (vuoto), config/luoghi.yaml (+88 luoghi). `python -m pipeline.notte --controlla revisione`: parti valide.

### Correzioni principali della coda
- Mattorosso, Tributo a Santana: live alle 22, biglietto 12 euro con drink (era tutto il giorno, accesso sconosciuto).
- Museo Canova (4 eventi): accesso e prezzi dalle schede del museo (visite 5 euro oltre all'ingresso; incontro su
  Carlo Scarpa gratuito su prenotazione).
- Nervesa: lo spettacolo di Gli Alcuni e' "L'Isola del Tesoro" secondo il Comune (Qdpnews scriveva "L'Isola del Natale").
- I Virtuosi Italiani al Teatro delle Voci: ore 17:30, 25/20/10 euro.
- Memoriale Brion (FAI): titolo completo e ore 11.
- New Age Club, L'Aperitivo del 29/11: 16-21, ingresso gratuito, link alla scheda del locale.
- Silea, Letture animate del 2/12: 16:30-18:30, Biblioteca dei Liberi Pensatori, Via Don Minzoni 14, gratuito, link
  alla scheda del Comune (mancava il link ufficiale).
- Corso Mazzini 29/11: orario 9-19. Zero Branco, Nel cuore dei bambini: gratuito con prenotazione obbligatoria.
- Nessun doppione vero tra i "possibili doppioni" segnalati (Canova/Tomaso 700, Lancenigo/Montebelluna, Treviso/
  Montebelluna, Preganziol/Soligo, Quinto/Preganziol: eventi diversi).

## Controllo a campione (20 eventi delle 11:37)
Corretti 9/20: Mercatini di Quinto, Nardo il ghepardo, Falstaff, Stelle a Natale, Canto di Natale a Francenigo,
Concerto di Natale Bohanan, PGV Christmas Party, Febbre a 90, Lo Schiaccianoci.
Errori (corretti tutti tranne gli orari non confermabili):
- orario 4: Tributo a Santana (22:00), Bunny Club (22:30); Boschi a Natale di Follina (8:30) e Via dell'Acqua e dei
  Mulini (10:00): orari non presenti ne' sulla scheda della Pro Loco ne' sul programma UNPLI, lasciati e da confermare.
- luogo 6: punto sul centro del comune per Speciali Insieme (Auditorium Comisso, 1,6 km), Accensione delle luci a Col
  San Martino (chiesa a 3 km), Prestige! a Santa Bona (3 km), Sulle orme di Tomaso (San Nicolo'), Giovedi' della
  Cultura (Ca' dei Carraresi); Cinenatale a Quinto era in biblioteca ma si svolge in Piazza Roma (corretti anche gli
  altri due film della rassegna).
- accesso 1: Tributo a Santana.
- link 3: Bunny Club e Remember portavano alla pagina di vendita TicketSMS (fonte da verificare): ora scheda del New
  Age Club, TicketSMS solo in ticket_url; Giovedi' della Cultura: la notizia della Fondazione non riporta le date,
  ora la guida di Nordest24 al calendario (stessa correzione per gli incontri del 3 e del 10 dicembre).

Riga per la parte 3 di ops/segnalazioni-e-controllo.md:
`- 2026-11-28 · corretti 9/20 · errori: data 0, orario 4, luogo 6, accesso 1, categoria 0, link 3 · lezione: primo campione da 20 letto davvero; l'errore principale e' il punto sul solo comune per gli eventi presi da Qdpnews e Nordest24 con un luogo nominato (6/20, ora 50 luoghi nuovi in luoghi.yaml); i link a pagine di vendita (TicketSMS) non sono link ufficiali; due orari di Boschi a Natale non si trovano sulle fonti. Sotto l'80%: proposta una regola nella parte 1`

Proposta di regola per la parte 1 (la scrive il coordinatore): "2026-11-28 · **Punto subito per i luoghi nuovi.** Nel
campione 6 errori su 20 erano eventi con il luogo nominato ma il punto sul centro del comune (fino a 3 km). Chi
aggiunge un evento con un luogo che non e' in config/luoghi.yaml ne cerca subito il punto (OpenStreetMap) e lo mette
in lat/lon o lo segnala alla revisione; il link ufficiale non e' mai la pagina di vendita dei biglietti."

## Posizioni
- Prima (ops/posizioni.json delle 11:37, 448 eventi): luoghi con punti diversi 0, lontani dal comune 1, solo comune con
  luogo 252, solo comune senza luogo 6, candidati 0.
- Luoghi sistemati: 88 voci nuove in config/luoghi.yaml (coordinate di OpenStreetMap, oggetto citato nella nota), i
  piu' frequenti per primi. Treviso (58): Ca' dei Carraresi (16 eventi), Corso Mazzini di Montebelluna (11), Gypsotheca
  Canova (9), Teatro del Pane (9), Stadio Tenni (8), Teatro Cristallo (7), Teatro delle Voci (7), Piazza del Popolo di
  Vittorio Veneto (6), centro di Cison (6), Teatro Eden (5), Teatro Careni, Canonica di Soligo, Sale del Municipio di
  San Vendemiano, Piazza dei Signori, Loggia dei Grani, Piazza La Piave, Palazzo dei Trecento, Villa di Maser, Chiesa di
  Col San Martino, ecc. Altre province (30), dopo la pubblicazione delle 12:19: Teatro Buzzati di Belluno (28), Sala
  Luttazzi (20) e Teatro Verdi (11) di Trieste, La Fenice (16) e Malibran di Venezia, Teatro alle Stimate (10), Arena e
  Piazza Bra di Verona, Teatro Comunale di Vicenza (10), Basilica Palladiana, Prato della Valle, Palazzo Moroni,
  Castello di Udine e Museo Etnografico (i 2 candidati), teatri di Gorizia, ecc.
- Dopo: la pubblicazione intermedia delle 12:19 (con i primi 37 luoghi gia' salvati e 338 eventi nuovi delle altre
  parti, 786 eventi) dava 0 / 1 / 354 / 21 / 2. Sugli eventi di docs/data/events.json i luoghi aggiunti in tutto
  coprono circa 150 dei 356 eventi con luogo ma senza punto. Stima per la prossima pubblicazione: luoghi con punti
  diversi 0, lontani dal comune 1, solo comune con luogo circa 205, solo comune senza luogo 21, candidati 0.
  Restano in cima: Piazza XX Settembre di Pordenone (12, Nominatim trova solo piazze omonime in provincia), Teatro
  Verdi di Padova (10, solo la via), Parco del Donatore di Ramon (6).
- Il solo "lontano dal comune" (b665ec02e9b8accd, Auditorium H-FARM, Roncade) resta un falso allarme gia' noto: il
  campus e' a Ca' Tron, 9 km dal centro, coordinate gia' verificate l'8/11. Il controllo non esclude i luoghi noti:
  servirebbe un'eccezione nel codice (pipeline/posizioni.py) per i luoghi di config/luoghi.yaml.

## Test di copertura (provincia di Treviso)
20 eventi trovati in modo indipendente dalle fonti del giro: titoli della categoria eventi di Nordest24 (non e' in
config/sources.yaml), due articoli con programma (Susegana-Oderzo, Natale a Ramon), il calendario natalizio di
Villorba e una ricerca su Nordest24. Le prime 9 ricerche generiche per comune (Portobuffole', Cessalto, Castello di
Godego, Susegana, Oderzo, Zero Branco, Preganziol, Volpago, Carbonera) hanno dato solo aggregatori da verificare
(Tacco di Bacco, mentelocale, Cose di Casa, Eventi e Sagre): i 4 eventi visti li' li ho scartati dal test per la
regola fonti.
Risultato: 13/20 gia' sul sito.
- Presenti: Oderzo Christmas Days, Pagliacci al Del Monaco, Oratorio di Natale in Cattedrale, Thanksgiving
  all'Opendream, PGV si veste di Natale, Effetto Natale a Nervesa, Concerto dell'Immacolata, Giovedi' della Cultura
  del 3/12 e del 10/12, Concerto di Natale Bohanan, Concerto della Banda Albino Gagno, Mostra dei Presepi di Catena,
  Il canto di Orsola.
- Mancanti: Natale a Ramon (mercatini), 26a Rassegna degli Artisti Locali di Ramon, Fiati all'opera a Ramon, Dutch
  Nazari al 4passiFestival, Corsa dei Babbi Natale di Ormelle (tutti e 5 aggiunti stanotte dall'agente treviso, non li
  ho ripetuti), mostra Il Magico Natale nelle Antiche Terre a Susegana (28/11, l'agente treviso ha il laboratorio di
  incisione dello stesso programma), Stati Generali del Sociale di StatisticAll (28/11). Gli ultimi due sono di oggi:
  non aggiunti.
Riga per ops/espansione.md:
`- 2026-11-28 · TV · copertura 13/20 (test della revisione: 20 eventi dai titoli di Nordest24 /category/eventi, dai programmi di Susegana-Oderzo e Natale a Ramon e dal calendario di Villorba; mancanti 3 appuntamenti di Natale a Ramon, Dutch Nazari al 4passiFestival, Corsa dei Babbi Natale di Ormelle (aggiunti stanotte dall'agente treviso), mostra Magico Natale nelle Antiche Terre e Stati Generali del Sociale (del 28/11, non aggiunti); 4 eventi trovati solo su aggregatori da verificare esclusi) · criterio di saturazione: non valutato (non e' lunedi')`

## Cosa resta (per la notte dopo)
- Luoghi di Treviso senza punto: Auditorium Santo Stefano e Biblioteca di Farra di Soligo, Oratorio di Soligo, NOI
  Fontane (Villorba), Giardini di Sant'Andrea (Treviso), ex scuola San Pio X (Quinto), IAT Treviso, Info Point di Cison
  (Piazza Brandolini 6), Piazza Sedese (Montebelluna), acquedotto della Bot (Asolo), Palazzo Reale di Crespano,
  Oratorio di Santandra' (Povegliano), Loggia dei Grani "zona sud" di Montebelluna (dubbio: in OSM la Loggia e' in
  Piazza dei Grani, in centro): Nominatim non li trova per nome, serve il sito del luogo o una scheda.
- Boschi a Natale di Follina (6/12 8:30) e Cison (5/12 14:00, 6/12 10:00): orari da confermare.
- Accesso sconosciuto lasciato com'e' dove la fonte non lo dice (Ubik, Palazzo Reale di Crespano, mercatini, piste).
- Possibile doppione da guardare: Maurizio Solieri Gang al Mattorosso del 5/12 compare sia come 0ae4e9d8a9e28b52 sia in
  eventi_redazione.yaml.
- Castagnata e Coro Col di Lana del 29/11 a Vittorio Veneto: luogo (Piazza del Popolo) non confermato dall'articolo.

## Fonti nuove da catalogare
- Nome: Comune di Silea, scheda evento · url: https://www.comune.silea.tv.it/eventi/ · query: pagina elenco
  https://www.comune.silea.tv.it/home/vivere/eventi.html, schede in /eventi/<titolo>.html con JSON-LD Event (startDate,
  endDate) · tipo: comune (gia' fonte del giro come comune-silea: le schede hanno orari, luogo e costo che l'elenco non
  ha, il link di dettaglio sotto /home/vivere/eventi/ da' 404).
- Nome: New Age Club, schede evento · url: https://www.newageclub.it/evento/<slug>/ · query: elenco
  https://www.newageclub.it/events/ · tipo: locale (orari, ingresso gratuito o TicketSMS; da usare come official_url
  al posto di TicketSMS).
- Nome: Nordest24 guida Giovedi' della Cultura · url: https://www.nordest24.it/giovedi-cultura-treviso-2026-2027-calendario-guida
  · query: "Giovedi' della Cultura" · tipo: testata ammessa, calendario completo 2026-27 con date (la Fondazione
  Cassamarca non le pubblica nella notizia).

## Lezioni
- La shell raggiunge i siti e Nominatim (OpenStreetMap): per le posizioni non servono ricerche, basta una pausa di
  3 secondi tra le richieste (con 1 secondo risponde 629, troppe richieste). Overpass invece chiude la connessione.
- Nominatim trova per nome teatri, musei, piazze, municipi ("town hall in <comune>") e biblioteche ("library in
  <comune>"); non trova oratori, sale parrocchiali, info point, acquedotti e sale interne.
- Le ricerche generiche "comune + categoria + dicembre 2026" portano quasi solo ad aggregatori da verificare: per il
  test di copertura rendono di piu' i programmi pubblicati da Nordest24 e i calendari dei comuni.
- Le pagine eventi dei siti comunali con il nuovo modello (Villorba, Carbonera, Susegana, Oderzo, Arcade) si caricano
  via script: la lettura diretta non mostra gli eventi.
- I PDF dei comuni (Povegliano) WebFetch non li legge, ma il file salvato si legge con pdftotext.

## Problemi
- ops/revisione.json e ops/campione.json sono cambiati a meta' lavoro (ripubblicazione delle 12:19): la nuova coda ha
  35 eventi non lavorati, quasi tutti di altre province (Padova, Vicenza, Verona, Pordenone, Trieste, Udine).
- Quota: le letture dalla shell non sono contate nelle 125 ricerche; se vanno contate, il totale e' 99.
- `python -m pytest -q tests` (96 passati) ha riscritto ops/prelievi.csv lasciando solo 1 riga (alle 11:26 UTC): il
  ripristino con `git checkout -- ops/prelievi.csv` mi e' stato negato, va fatto dal coordinatore prima del commit.
  Il test che scrive nel file vero andrebbe corretto (file temporaneo).
