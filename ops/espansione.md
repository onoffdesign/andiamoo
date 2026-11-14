# Espansione per province

ANDIAMO? cresce **una provincia alla volta**. Si lavora su una provincia finche' e' "satura" (gli eventi trovati non
aumentano piu' di tanto), poi si aggiunge la successiva. Le province gia' sature non si abbandonano: restano nel
giro del PC e nella manutenzione notturna, ma la ricerca nuova si concentra sulla provincia attiva.

## Provincia attiva

**Treviso (TV)**, da ottobre 2026.

## Criterio di saturazione

**Criterio confermato da Federico: si', il 2026-10-30** (soglie come scritte qui sotto). Ogni lunedi' Claude
valuta il criterio; quando e' rispettato aggiunge la provincia successiva seguendo la procedura e lo scrive nel
riepilogo. Se Federico cambia le soglie, si aggiornano qui con la data.

Una provincia e' satura quando, **per due settimane di fila**, valgono tutte e quattro:

1. **Copertura**: nel test di copertura (vedi sotto) almeno **9 eventi su 10** trovati in modo indipendente sono
   gia' sul sito. E' la misura principale: dice quanta parte degli eventi reali stiamo gia' prendendo.
2. **Comuni controllati**: tutti i comuni della provincia in `ops/copertura.yaml` controllati almeno **due volte**.
3. **Crescita ferma**: in `ops/saturazione.csv` gli eventi dei prossimi 30 giorni crescono meno del **5% a
   settimana** (contando a parita' di periodo dell'anno: dicembre e l'estate hanno naturalmente piu' eventi).
4. **Qualita'**: controllo a campione (`ops/segnalazioni-e-controllo.md`) corretto almeno al **90%** (9 su 10 col
   piano Pro, 18 su 20 col Max).

Il punto 3 da solo non basta: nuovi eventi vengono pubblicati ogni giorno, quindi il numero non si ferma mai del
tutto. Per questo conta soprattutto il test di copertura.

### Test di copertura (ogni notte, sulla provincia attiva)

1. Scegli 10 eventi **in modo indipendente dal sito**: il primo evento dei prossimi 30 giorni trovato con 10
   ricerche diverse, variando comune (estratto a caso da `ops/copertura.yaml`) e categoria (da
   `ops/categorie-ricerca.md`). Non usare fonti gia' in `config/sources.yaml`: il test deve misurare cio' che ci
   sfugge.
2. Per ognuno: `python -m pipeline.editorial --cerca "titolo" --data AAAA-MM-GG`. Trovato o no.
3. Quelli mancanti si aggiungono come eventi nuovi (il test serve anche alla ricerca).
4. Scrivi la riga nel registro qui sotto.

## Ordine delle province

Regola: la prossima provincia e' quella **confinante** con l'area gia' coperta e con **piu' abitanti**, finendo prima
tutta la regione. Poi la regione confinante. Ordine delle regioni: Veneto, Friuli-Venezia Giulia, Trentino-Alto
Adige, poi Nord Italia (Lombardia, Emilia-Romagna, Piemonte, Liguria, Valle d'Aosta), poi Centro (Toscana,
Marche, Umbria, Lazio), poi Sud e isole (Abruzzo, Molise, Campania, Puglia, Basilicata, Calabria, Sicilia,
Sardegna). Prima di scegliere, verifica gli abitanti sul sito ISTAT (demo.istat.it): le cifre qui sotto sono
indicative.

Ordine previsto (si ricalcola a ogni passaggio):

| # | Provincia | Regione | Abitanti (indicativi) | Perche' adesso | Stato |
|---|---|---|---|---|---|
| 1 | Treviso (TV) | Veneto | ~880.000 | partenza | attiva |
| 2 | Padova (PD) | Veneto | ~935.000 | confina con TV, la piu' popolosa | in attesa |
| 3 | Verona (VR) | Veneto | ~930.000 | confina con PD | in attesa |
| 4 | Vicenza (VI) | Veneto | ~850.000 | confina con TV, PD, VR | in attesa |
| 5 | Venezia (VE) | Veneto | ~835.000 | confina con TV, PD | in attesa |
| 6 | Rovigo (RO) | Veneto | ~225.000 | confina con PD, VR, VE | in attesa |
| 7 | Belluno (BL) | Veneto | ~200.000 | confina con TV, VI | in attesa |
| 8 | Udine (UD) | Friuli-Venezia Giulia | ~515.000 | confina con VE, BL | in attesa |
| 9 | Pordenone (PN) | Friuli-Venezia Giulia | ~310.000 | confina con TV, VE, BL, UD | in attesa |
| 10 | Gorizia (GO) | Friuli-Venezia Giulia | ~140.000 | confina con UD | in attesa |
| 11 | Trieste (TS) | Friuli-Venezia Giulia | ~230.000 | confina con GO | in attesa |
| 12 | Trento (TN) | Trentino-Alto Adige | ~545.000 | confina con VI, VR, BL | in attesa |
| 13 | Bolzano (BZ) | Trentino-Alto Adige | ~535.000 | confina con TN, BL | in attesa |

Quando Italia e' tutta coperta, si continua solo a migliorare metodo (`ops/metodo-ricerca.md`) e categorie
(`ops/categorie-ricerca.md`).

## Come si aggiunge una provincia

Solo quando il criterio di saturazione e' rispettato. Nella stessa notte:
1. `config/settings.yaml`: aggiungi la sigla in `area.provinces` (es. `["Treviso", "PD"]`) e allarga `area.bbox`
   perche' contenga anche la nuova provincia; aggiorna `site.tagline`, `site.center` e `site.zoom` per l'area intera.
2. `docs/index.html`: aggiorna la descrizione del sito (oggi dice "provincia di Treviso").
3. `ops/copertura.yaml`: aggiungi la sezione dei comuni della nuova provincia (elenco completo dal sito ISTAT o dalla
   Regione), tutti a `null`.
4. `ops/metodo-ricerca.md`: aggiungi la sezione della provincia, partendo da regole generali e regionali; aggiungi
   le pagine della nuova provincia agli aggregatori multi-provincia gia' noti (sezione 4).
5. `config/sources.yaml`: allarga le fonti multi-provincia (pagine citta' di TicketOne, running.life, eventiesagre...).
6. Aggiorna la tabella qui sopra (stato e data) e scrivi la decisione nel registro.
7. Verifica: `python -m pipeline.editorial --controlla` e `python -m pytest -q tests` tutti verdi, poi commit.

Il carico cresce con ogni provincia: se il giro del PC supera le 2 ore o la revisione notturna non riesce piu' a
finire coda e manutenzione, segnalalo nei `problemi` del riepilogo prima di aggiungere altre province.

## Registro

Test di copertura e decisioni, una riga per notte (la piu' recente in alto):
`- AAAA-MM-GG · TV · copertura 7/10 (mancanti: ...) · eventi prossimi 30 giorni N (settimana +N%) · comuni controllati 2 volte N/94`
- 2026-11-14 · TV · copertura 3/10 (7 eventi della guida culturale del weekend di Qdpnews e 3 sagre di fine novembre di TrovaSagre; presenti: GIOVANNI - Internato Militare Italiano a Montebelluna, Festival del Radicchio di Paderno, Cena del Lesso di Sant'Angelo; mancanti: Per le vie del mistero a Treviso, Il codice del Bestiario a Castelfranco, Animali fantastici al Museo del Cenedese, concerto della Dama Castellana alla Sala dei Battuti (tutti aggiunti), mostra La storia si veste e laboratorio di ceramica di Scomigo (non aggiunti: orari e accesso non pubblicati, laboratorio riservato), Festa di Sant'Andrea a Colbertaldo (solo aggregatori)) · eventi prossimi 30 giorni: 426 sul sito (il PC non gira dall'11/11) · comuni controllati 2 volte 0/94 · i buchi sono il festival UNPLI Spettacoli di Mistero e la cultura del Quartier del Piave (Eventi Venetando), ora catalogati
- 2026-11-13 · TV · copertura 6/10 (primi 10 eventi TV della guida TViWeb del weekend 13-15/11; presenti: Birre Artigianali di Camalo', Delizie d'Autunno, Profumi e Sapori d'Autunno, cioccolato in Piazza dei Signori (Fondentemente), Lipparini al Bailo, Mostra dei vini del Montello; mancanti: Sagra di San Martino a Vedelago e Festa dell'Agricoltura di Giavera (aggiunte), Festa della Madonna della Salute di Salvatoronda (solo aggregatori, non aggiunta), 4passiFestival (date sbagliate nella guida: il weekend centrale era il 6-8/11; aggiunti i 3 incontri di novembre)) · eventi prossimi 30 giorni: 426 sul sito (il PC non gira dall'11/11) · comuni controllati 2 volte 0/94 · i buchi sono le sagre parrocchiali dei comuni senza fonte al PC e le feste dei comuni piccoli
- 2026-11-12 · TV · copertura 8/10 (prime 10 sagre dall'elenco TrovaSagre del weekend, fonte gia' nota quindi test poco indipendente; mancanti: Festa di San Martino a Santa Maria del Sile, la festa stessa della Madonna della Salute di Bibano (c'era solo il dj set); aggiunti Santa Maria del Sile e Santa Caterina di Barbisano, fuori dalle prime 10) · eventi prossimi 30 giorni: 428 sul sito al giro dell'11/11 · comuni controllati 2 volte 0/94 · le sagre sono coperte bene, i buchi restano le feste di quartiere e di frazione
- 2026-11-11 · TV · copertura 4/10 (10 ricerche diverse per comune e categoria, primo evento trovato; presenti: Monte Christmas Walk a Montebelluna, antiquariato di Roncade, Birre Artigianali di Camalo', Delizie d'Autunno a Maserada; mancanti: Giornate Martiniane di Oderzo, inaugurazione dell'anno accademico del Conservatorio di Castelfranco, presentazioni alla Ubik di Treviso, presentazione Land Editore alla biblioteca di Montebelluna, serata di Ananda Marga a Ponzano, Fondentemente in Piazza dei Signori: aggiunti tutti) · fuori test: 0/10 del Teatro Accademia su TicketOne (la fonte ticketone del PC da' 0 eventi) · eventi prossimi 30 giorni: non aggiornato (il PC non gira dal 6/11) · comuni controllati 2 volte 0/94 · i buchi sono librerie, enti culturali dei comuni (Oderzo Cultura) e spettacoli commerciali in biglietteria
- 2026-11-10 · TV · copertura 3/10 (dall'elenco delle sagre di trovasagre dal 10/11; presenti: Sagra del Frico, Birre Artigianali di Camalo', Profumi e Sapori d'Autunno; mancanti: San Martino a Sarano, San Martino a Musano, Madonna della Salute a Bibano (c'e' solo una serata) e a Villanova, Mostra dei vini del Montello, San Martin a Roganzuolo e a Falze', aggiunte le 4 con date certe; oltre i 10 mancavano anche Solighetto e la Cena del Lesso, aggiunte) · eventi prossimi 30 giorni: non aggiornato (il PC non gira dal 6/11) · comuni controllati 2 volte 0/94 · le sagre restano la categoria meno coperta: si pubblicano quasi solo su Facebook e aggregatori

- 2026-11-09 · TV · copertura 8/10 (dal calendario di trevisoeventi, eventi dal 9/11; presenti: Colle Umberto, Visna', San Mauro, Note da Oscar, Petite Messe, antiquariato di Roncade e di Godega, Mirandolina; mancanti: Premio di pittura di Cordignano e Profumi e Sapori d'Autunno a Susegana, aggiunti stanotte) · prova in piu' sulle mostre: 1/10 dell'elenco di itinerarinellarte gia' sul sito (aggiunte 5), feste del radicchio di Fiori d'Inverno 0/13 (aggiunte tutte), stagione di prosa del Del Monaco 0/12 · eventi prossimi 30 giorni: non aggiornato (il PC non gira dal 6/11) · comuni controllati 2 volte 0/94 · valutazione del lunedi': criterio di saturazione non rispettato (copertura sotto 9/10 e lontana sulle categorie di stagione, campione 3/10, PC fermo), resta Treviso
- 2026-11-08 · TV · copertura 7/10 (dal calendario di trevisoeventi, eventi dal 9/11 diversi da quelli di ieri dove possibile; presenti: Colle Umberto, Visna', San Mauro, antiquariato di Roncade, Anima Teatro, Maserada sul Palco, Note da Oscar; mancanti: Premio di pittura di Cordignano, Petite Messe a Cusignana, visite al Museo del Caffe' Dersut; aggiunta Cusignana) · prova in piu' sulle sagre: 4/13 dell'elenco di trovasagre gia' sul sito, aggiunte Lorenzaga e Camalo' · eventi prossimi 30 giorni: non aggiornato (il PC non ha girato) · comuni controllati 2 volte 0/94
- 2026-11-07 · TV · copertura 4/10 (dal calendario di trevisoeventi, primi 10 eventi TV dal 7/11; presenti: Prealpi in Festa, Antica Fiera di Santa Lucia, Maserada sul Palco, antiquariato di Roncade; mancanti: San Martin a Mojan, Premio di pittura di Cordignano, sagra di San Martino a Colle Umberto, Festa d'Autunno a Visna', Anima Teatro a Monastier, sagra di San Mauro a Castagnole; aggiunti stanotte tutti tranne il Premio di pittura) · eventi prossimi 30 giorni: non aggiornato (il PC non ha girato stanotte) · comuni controllati 2 volte 0/94. Nota: i mancanti delle notti scorse sono stati chiusi aprendo le schede di trevisoeventi
- 2026-11-06 · TV · copertura 1/10 (dal calendario di trevisoeventi, prossimi 10 giorni; presente solo l'antiquariato di Roncade; mancanti: Prealpi in Festa, sagra di San Martino a Colle Umberto, Festa d'Autunno a Visna', San Martin a Mojan, Anima Teatro a Monastier, Milipiave a Spresiano, antiquariato di Collalto, Imoco - Macerata, Treviso - Novara. Aggiunti stanotte Prealpi in Festa (3 giornate) e le partite del Treviso FBC) · eventi prossimi 30 giorni: non aggiornato (il PC non gira dal 3/11) · comuni controllati 3 volte 0/94. Nota: la lista dei mancanti e' quasi uguale a ieri: gli eventi della redazione non escono sul sito finche' il PC non gira
- 2026-11-05 · TV · copertura 0/10 (dal calendario di trevisoeventi, prossimi 10 giorni; mancanti: sagra di San Martino a Colle Umberto, Festa d'Autunno a Visna', Prealpi in Festa a Cordignano, San Martin a Mojan, Anima Teatro a Monastier, Milipiave a Spresiano, Imoco - Macerata al Palaverde, sagra di San Mauro a Castagnole, Petite Messe a Cusignana, Note da Oscar a Villa Onigo; nessuno confermato su una pagina ufficiale, solo Facebook o aggregatori) · eventi prossimi 30 giorni: non aggiornato (il PC non gira dal 3/11) · comuni controllati 2 volte 0/94. Nota: il buco e' sempre lo stesso, le feste di paese e le rassegne comunali pubblicate solo su Facebook e trevisoeventi
- 2026-11-02 · TV · copertura 2/10 (presenti: Maratonina di San Biagio, mercatino di Godega; mancanti: Uno nessuno tutti al Teatro Da Ponte, presentazione su Francesco Baracca a Povegliano, Antica Fiera di Santa Lucia, mercatino di Portobuffole', sagra di San Martino a Colle Umberto, Petite Messe a Cusignana, Imoco Volley al Palaverde, Maserada sul Palco; aggiunti Da Ponte, Antica Fiera e Maserada, gli altri non confermati su pagine ufficiali) · eventi prossimi 30 giorni 121 (il PC non ha girato stanotte) · comuni controllati 2 volte 0/94 · valutazione del lunedi': criterio di saturazione lontano (copertura, comuni e campione sotto soglia), resta Treviso. Nota: 7 dei 10 eventi vengono da due elenchi (Teatro Da Ponte e trevisoeventi), non da 10 ricerche diverse
- 2026-11-01 · TV · copertura 5/10 (presenti: Dracula al Cinema Edera, pranzo La chiamavano Trinita', domenica ecologica di Treviso, Treviso Sotterranea, 4passiFestival; mancanti: mercatino Cose d'Altri Tempi (aggiunte le date confermate di dicembre e gennaio), Villaggio delle Zucche di Villorba (nessuna pagina ufficiale, finisce il 2/11), corso di autodifesa a Pieve di Soligo e uscita CAI Malga Mont (non confermabili), rassegna I martedi' a 4 euro dell'Edera) · eventi prossimi 30 giorni vedi saturazione.csv · comuni controllati 2 volte 0/94 · lontana dalla saturazione
- 2026-10-31 · TV · copertura 3/10 (mancanti: 2 incontri del 4passiFestival, lettura animata di Sile Classica, 2 spettacoli del Teatro Accademico di Castelfranco, sagra Madonna della Salute di Maser, letture in biblioteca a Castelfranco; aggiunti tutti tranne l'ultimo) · eventi prossimi 30 giorni 123 · comuni controllati 2 volte 0/94 · lontana dalla saturazione: mancano teatri comunali e sagre
