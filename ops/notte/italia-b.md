# Agente italia-b, notte del 2026-11-28 (Toscana e Marche)

Province: LU, AR, LI, SI, PT, PO, GR, MS (Toscana), AN, PU (Marche). A meta' lavoro il coordinatore ha unito circa 380
eventi di un'altra sessione sulle stesse province (Lucca 49, Siena 41, Livorno 26 dal Goldoni, Pesaro 43, Ancona 56...).
Ho controllato tutto quello che avevo gia' scritto con un confronto automatico (stesso comune, stesso giorno o periodo
sovrapposto, titolo simile, oppure stesso luogo e ora) contro sito, redazione e parti degli altri agenti: tolti 81 doppioni.

## Numeri
- Eventi in `config/notte/italia-b-eventi.yaml`: **107** (`--controlla italia-b`: "Parti valide"). Tutti con venue,
  address, lat e lon.
- Correzioni in `config/notte/italia-b-correzioni.yaml`: **14** (`correggi`): orari e scheda propria per gli spettacoli
  del Teatro Goldoni di Livorno unificati dall'altra sessione con la sola data e il link all'elenco generale.
- Ricerche usate: **108 su 125** (15 WebSearch, 4 WebFetch, 89 letture dirette con curl di pagine, JSON, iCal e
  robots.txt). A parte 91 chiamate a Nominatim per le coordinate (non contate nella quota).

| Regione | Prov. | Eventi | Comuni |
|---|---|---|---|
| Toscana | LU | 49 | Lucca 40, Capannori 9 |
| Toscana | PT | 35 | Montecatini-Terme 26, Pistoia 9 |
| Toscana | SI | 11 | Siena 8, Asciano 1, Monteriggioni 1, Sinalunga 1 |
| Toscana | MS | 7 | Massa 2, Mulazzo 1, Casola in Lunigiana 1, Tresana 1, Fosdinovo 1, Aulla 1 |
| Toscana | AR | 3 | Anghiari 1, Poppi 1, Civitella in Val di Chiana 1 |
| Toscana | LI | 2 | Livorno 1, Rosignano Marittimo 1 (Vada) |
| Toscana | PO, GR | 0 | |
| Marche | AN, PU | 0 | |

Per categoria: arte-cultura 33, musica 18, mercatini-fiere 17, sagre-feste 14, teatro-spettacoli 10,
famiglie-bambini 10, sport 5.

Comuni del piano: Mulazzo (Villaggio di Natale), Montecatini-Terme (26). Cercati senza risultati pubblicabili:
Viareggio, Chiusi, Portoferraio, Sirolo, Fabriano (basket), Mondolfo (Presepepaese: pagina della parrocchia vuota a
WebFetch, irraggiungibile da curl), Villafranca e Comano (nulla di datato sul portale Lunigiana). Non cercati per quota:
Seravezza, Fosciandora, Caprese Michelangelo, Subbiano, Collesalvetti, Castellina in Chianti, Cetona, Larciano,
Serravalle Pistoiese, Vaiano, Carmignano, Monterotondo Marittimo, Montieri, Capalbio, Monte Roberto, Monte Grimano
Terme, Tavoleto. Ambiti: PT Montagna ed escursionismo (Parkrun e Babbo Natale corre per Avis a Montecatini), MS Feste
stagionali (Natale in Lunigiana), AN Sport da guardare (0). `ops/copertura.yaml`: aggiunti Capannori, Anghiari, Poppi,
Civitella, Rosignano Marittimo, Asciano, Monteriggioni, Sinalunga, Fivizzano, Casola, Tresana, Fosdinovo, Aulla e
`categorie_PT`; le altre voci delle mie province le aveva gia' scritte l'altra sessione.

## Fonti nuove da catalogare (ops/fonti.yaml; le strutturate candidate al giro)
Strutturate (priorita' alta):
- **Turismo Lucca, calendario eventi del Comune** | https://eventi.turismo.lucca.it/ | il calendario si legge in JSON
  con POST `https://eventi.turismo.lucca.it/back/function/calendar.php` e i campi `setEvent=setEvent&filterEv=1&monthcal=MM&yearcal=AAAA`
  (40-85 eventi al mese con titolo, DATA_DA/DATA_A, PERIODI, luogo in `MAPS`, prezzo, descrizione; robots.txt `Allow: /`).
  Schede `evento-singolo.php?id=N` | ufficio turistico | LU. Attenzione: DATA_DA/DATA_A a volte non coincidono con la
  descrizione (Bruckner, Concerto d'organo di Montuolo: scartati); gli orari delle repliche sono solo nella descrizione.
- **Montecatini Terme Tourism (Fondazione Turismo WE)** | https://montecatinitermetourism.com/events.ics | feed iCal
  di Events Manager con 50 eventi, luogo con indirizzo e campo GEO (coordinate). L'API REST di Events Manager risponde 401;
  il feed iCal no. robots.txt senza divieti | ufficio turistico | PT. Contiene doppioni in inglese (stessa URL).
- **Visit Tuscany, sitemap degli eventi** | https://www.visittuscany.com/sitemap/sitemap-eventi.xml | elenca tutte le
  schede evento della Toscana (16 del 2026-27 stanotte); le schede `/it/eventi/<slug>/` si leggono con curl e hanno
  luogo, "Quando" con orari, prezzo e sito | ufficio turistico regionale | tutta la Toscana. robots.txt vieta solo i
  parametri ?filters= ?query= ?asset=.
- **VisitLunigiana (Associazione Operatori Turistici Lunigianesi)** | https://visitlunigiana.it/eventi-in-lunigiana/ |
  schede `/events/<slug>/` con JSON-LD `Event` (data, ora, luogo); niente API tribe | associazione turistica | MS.
- **Fondazione Teatro Goldoni** | https://www.goldoniteatro.it/spettacoli/?ts=eventi | elenco con date; le schede hanno
  il campo "Orario/i" (feed RSS con solo 9 voci, REST chiusa) | sede | LI.

Non strutturate:
- **Comune di Pistoia, eventi (Municipium)** | https://www.comune.pistoia.it/it/events (3 pagine) | schede con "Date e
  orari", "Costo", "Luogo" con indirizzo | comune | PT. Il sito pistoiacittadelnatale.com non risponde (timeout).
- **Comune di Siena, programma Siena Incanta** | https://comune.siena.it/novita/siena-incanta-si-accende-il-natale-siena-eventi-spettacoli-e-mostre-internazionali-le |
  programma completo 28/11-10/1 in una pagina | comune | SI.
- **Mercatini di Natale di Arezzo (Confcommercio)** | https://mercatininatalearezzo.it/ | organizzatore | AR.
- Il Giunco (ilgiunco.net, testata di Grosseto): robots.txt e privacy-policy letti, nessun divieto di raccolta
  automatica; da passare all'agente fonti. Ho aperto la home solo per trovare la pagina dei termini (non esiste una
  pagina termini, solo privacy e cookie). Il programma del Natale di Grosseto li' non ha orari ne' luoghi delle parate.
- Cartellone eventi del Comune di Prato (tempolibero.comune.prato.it, tempolibero2.comune.prato.it): 503 a WebFetch e
  nessuna risposta a curl; ha la rassegna "Prato Natale 2026". Da riprovare.
- rivieradelconero.info/en/events/ (AN): WebFetch legge l'elenco (Numana, Loreto, Recanati) ma senza indirizzi; curl in errore.

## Luoghi nuovi verificati (per config/luoghi.yaml; coordinate OpenStreetMap via Nominatim, indirizzo dalla fonte)
- Teatro del Giglio | Lucca | Piazza del Giglio 13 | 43.8403991, 10.5030674
- Chiesa di San Salvatore | Lucca | Piazza del Salvatore | 43.8440921, 10.5029219
- Chiesa di San Francesco | Lucca | Piazza San Francesco | 43.8454916, 10.5114050
- Palazzo Guinigi | Lucca | Via Guinigi 29 | 43.8437846, 10.5072283
- Palazzo Ducale | Lucca | Piazza Napoleone | 43.8413787, 10.5019186
- Foro Boario | Lucca | Via per Camaiore | 43.8563229, 10.5082170
- Cattedrale di San Martino | Lucca | Piazza San Martino | 43.8406300, 10.5060534
- Museo Nazionale di Villa Guinigi | Lucca | Via della Quarquonia 4 | 43.8449826, 10.5123434
- Museo Nazionale di Palazzo Mansi | Lucca | Via Galli Tassi 43 | 43.8436183, 10.4990647
- Villa Bottini | Lucca | Via Elisa 9 | 43.8436516, 10.5102639
- Museo Barsanti e Matteucci | Lucca | Via Sant'Andrea 56 | 43.8435487, 10.5074507
- Biblioteca Statale | Lucca | Via Santa Maria Corteorlandini 12 | 43.8449331, 10.5013311
- Casa del Boia | Lucca | Via dei Bacchettoni | 43.8458120, 10.5141390
- Real Collegio | Lucca | Piazza del Collegio 13 | 43.8465401, 10.5050380
- Oratorio degli Angeli Custodi | Lucca | Via dell'Angelo Custode | 43.8441744, 10.5080707
- Ex Ospedale Psichiatrico di Maggiano | Lucca | Via di Fregionaia 692 | 43.8504538, 10.4246548
- Ex Cavallerizza ducale (Cavallerizza San Donato) | Lucca | Piazzale Verdi | 43.8436907, 10.4963583 (da confermare)
- Villa Reale di Marlia | Capannori | Via della Fraga Alta 2 | 43.9001873, 10.5561112
- Tenuta dello Scompiglio | Capannori | Via di Vorno 67 | 43.7971312, 10.5124058 (punto della Cucina dello Scompiglio, 67b)
- Biblioteca San Giorgio | Pistoia | Via Sandro Pertini 340 | 43.9281323, 10.9100823
- Teatro Il Funaro | Pistoia | Via del Funaro | 43.9376993, 10.9201532
- Piccolo Teatro Mauro Bolognini | Pistoia | Via del Presto 5 | 43.9344344, 10.9167755
- Chiesa di San Giovanni Fuorcivitas | Pistoia | Via Cavour | 43.9320073, 10.9164034
- Teatro Verdi | Montecatini-Terme | Viale Giuseppe Verdi 45 | 43.885104, 10.772458 (campo GEO del calendario ufficiale)
- Terme Tettuccio | Montecatini-Terme | Piazza Domenico Giusti | 43.887838, 10.776449 (GEO del calendario)
- Teatro dei Rinnovati | Siena | Il Campo 1 | 43.3180619, 11.3324676
- Teatro dei Rozzi | Siena | Via delle Terme 15 (Piazza Indipendenza) | 43.3189684, 11.3302334
- Palazzo Chigi Saracini | Siena | Via di Citta' 89 | 43.3171232, 11.3309595
- Santa Maria della Scala | Siena | Piazza del Duomo 1 | 43.3171886, 11.3279706
- Teatro Goldoni | Livorno | Via Carlo Goldoni 83 | 43.5459241, 10.3138890
- Duomo di Livorno | Livorno | Piazza Grande | 43.5500990, 10.3095841
- Teatro dei Servi | Massa | Via Palestro | 44.0396936, 10.1425896
- Museo Diocesano | Massa | Via Alberica | 44.0357933, 10.1422981

## Eventi visti ma non pubblicati
- Lucca: Lo spazio esteso, Lucca in Maschera, Lucca Gustosa (luogo "centro storico"); Vissi d'Arte (Palazzo delle
  Esposizioni non trovato su OSM); Meraki Market e Nella rete dell'algoritmo (luogo non posizionato); Histoire du soldat
  (Teatro Nieri di Ponte a Moriano non su OSM); Bruckner e Concerto d'organo di Montuolo (data o luogo in conflitto nella
  stessa scheda); Le Danze di Galanta (20:30 nei dati, 21:00 nel testo).
- Pistoia: Incanto natalizio (Chiesa di Sant'Andrea non trovata), Fiera antiquaria del 13/12 (luogo "centro storico").
- Siena: Mercatini degli hobbisti di Strada Massetana Romana, Family Park di Villa Rubini e Cittadella della Lizza
  (luoghi non trovati su OSM).
- Numana (AN): tre spettacoli al Teatro Italia (21:00) senza indirizzo del teatro.
- Grosseto: parate natalizie senza orari ne' luoghi esatti (articolo de Il Giunco).

## Lezioni
- Toscana: i portali turistici ufficiali sono la fonte migliore e spesso hanno dati strutturati nascosti (Lucca: JSON del
  calendario via POST; Montecatini: iCal di Events Manager con coordinate; Visit Tuscany: sitemap delle schede evento).
  Provare sempre `/events.ics`, `/wp-json/` (per vedere i namespace), la sitemap degli eventi, prima di aprire le schede.
- Quando due sessioni lavorano le stesse province conviene confrontare per comune + giorno + titolo simile e anche per
  periodo sovrapposto: l'altra sessione aveva messo le repliche teatrali come un solo evento con fine, io una per data.
- I comuni piccoli toscani e marchigiani a fine novembre rendono quasi zero con WebSearch (Viareggio, Chiusi,
  Portoferraio, Sirolo, Mondolfo): escono solo testate da verificare e pagine 2025.

## Problemi
- Prato: il cartellone del Comune non risponde ne' a WebFetch (503) ne' a curl.
- La mia lettura del 2026-11-28 ha usato la home di ilgiunco.net per cercare i termini: nessun divieto trovato, ma la
  fonte va registrata dall'agente fonti prima di usarla come official_url (non l'ho usata per nessun evento).
- `pipeline.fonti_vietate --url` risponde "ammessa (sito ufficiale)" anche per testate mai verificate (ilgiunco.net):
  il controllo non distingue una testata da un sito ufficiale.
