# Agente italia-a, notte del 2026-11-28 (seconda sessione, sera)

Province: NO, VC, VB (Piemonte), GE, SV, SP, IM (Liguria), AO (Valle d'Aosta), FI, PI (Toscana).

## Numeri
- Eventi in `config/notte/italia-a-eventi.yaml`: **315** (`python -m pipeline.notte --controlla italia-a`: "Parti valide").
  Prima di consegnare: confronto di ogni evento con il sito (events.json appena pubblicato con i 299 eventi dell'altra
  sessione), con `eventi_redazione.yaml` e con le parti degli altri agenti, per titolo, data, ora e luogo: **68 doppioni
  tolti** (quasi tutti del PDF di Turismo Novara, gia' pubblicato dall'altra sessione). Controllo a campione con
  `pipeline.editorial --cerca` su 10 titoli: nessun doppione.
- Per regione: **Toscana 221** (FI 177, PI 44), **Liguria 53** (GE 42, SP 11), **Piemonte 35** (NO 35), **Valle d'Aosta 6**.
  VC, VB, SV, IM: 0 (non cercate per tempo; i capoluoghi erano gia' coperti).
- Per comune: Firenze 127, Pisa 44, Genova 27, Rapallo 15, Fiesole 14, Sarzana 11, Novara 11, Campi Bisenzio 9,
  Aosta 6, Borgomanero 5, altri 46 in 33 comuni delle province FI e NO (Barengo 1).
- Correzioni: nessuna (`italia-a-correzioni.yaml` non creato).
- Ricerche: **21 su 125** (WebSearch 16, WebFetch 5, di cui 2 rifiutate: PDF brochure Teatro della Toscana oltre 10 MB,
  genova24.it 403). In piu' letture dirette con curl di pagine ufficiali uscite dalle ricerche o linkate da esse (robots.txt
  letti, nessun divieto): calendario mensile del Maggio (4 pagine), Destination Florence (29 pagine elenco + 155 schede,
  1,5 s tra una e l'altra), VisitGenoa Natale (1 pagina + 24 schede), eventi.pisamo.it, turismo.pisa.it, PDF di
  Turismo Novara, API The Events Calendar di hellorapallo.it. Coordinate: Nominatim (rate limit 629 ripetuti) poi
  Photon (photon.komoot.io, dati OSM) con controllo della distanza dal centro del comune; luoghi gia' sul sito
  allineati alle coordinate del sito (69 eventi).

## Fonti nuove da catalogare (pagine con molti eventi)
- **Maggio Musicale Fiorentino, calendario mensile** | https://www.maggiofiorentino.com/calendario/2026/12 (e /2027/01...) |
  query "Maggio Musicale Fiorentino calendario dicembre 2026" | sede | FI. HTML statico con data, ora, sala, link
  /events/<slug>; anche concerti in provincia (Certaldo, Signa, Montelupo, Sieci, San Casciano, Greve). robots.txt
  libero. **Candidata al giro** (html, una pagina al mese). Gia' in ops/fonti.yaml: aggiornare con l'url mensile.
- **Destination Florence, eventi** | https://www.destinationflorence.com/it/eventi?page=N (0-28) | query "eventi dicembre
  2026 Firenze" | ufficio turistico (Comune e Citta' Metropolitana) | FI, 284 eventi in 37 comuni; le schede hanno
  "Quando" (date e orari), "Prezzi" e "Dove". robots.txt Drupal standard. **Candidata al giro** (gia' in fonti.yaml
  come destinationflorence).
- **Teatro della Pergola** | https://www.teatrodellatoscana.it/teatri/teatro-della-pergola | query "Teatro della Pergola
  stagione 2026/2027" | sede | FI. Elenco con date e link a /it/evento/spettacolo/<slug>; senza orari. Con curl
  risponde una pagina anti-bot, con WebFetch si legge.
- **VisitGenoa, Natale 2026** | https://www.visitgenoa.it/it/natale-2026-genova | query "Natale a Genova 2026 cartellone"
  (allowed_domains visitgenoa.it) | ufficio turistico del Comune | GE. Calendario in 2 pagine (la seconda,
  ?page=1, non risponde), schede con date, orari e luogo in "Info utili". Riaprire a meta' dicembre.
- **Pisa Citta' del Natale (Pisamo)** | https://eventi.pisamo.it/pisa-citta-del-natale/ | query "Pisa Natale 2026
  programma" | comune / societa' comunale | PI. 48 appuntamenti con data, ora e luogo in una pagina. robots.txt libero.
- **Hello Rapallo (Comune di Rapallo)** | https://hellorapallo.it/eventi/ , API https://hellorapallo.it/wp-json/tribe/events/v1/events
  | query "Rapallo Natale 2026 eventi" | comune | GE. WordPress The Events Calendar: **candidata a config/sources.yaml
  tipo tribe_api**. Teatro delle Clarisse quasi tutto il cartellone.
- **Turismo Novara, PDF del calendario** | https://www.turismonovara.it/it/eventimanifestazioni?PrintPDF=1 | gia' usato
  dall'altra sessione: 274 eventi della provincia in un PDF (pdftotext). robots.txt senza regola per tutti i robot.
- Da evitare: visitsarzana.it e teatrodellatoscana.it (pagina anti-bot "One moment, please" con curl); visitsavona.com
  (elenco in JavaScript, vuoto); comune.aosta.it/it/events (Municipium in JavaScript).
- Testate usate (verdetto "ammessa" di pipeline.fonti_vietate, robots.txt letti, termini non letti: per l'agente fonti):
  gazzettamatin.com (Aosta), lavocedigenova.it (robots libero), cittadellaspezia.com. genova24.it: robots libero ma 403
  e Cloudflare. genovatoday.it non aperta (Citynews come trevisotoday, da verificare).

## Luoghi nuovi verificati (coordinate OSM da Nominatim o Photon; luoghi con 2+ eventi)
- Teatro del Maggio Musicale Fiorentino | Firenze | Piazza Vittorio Gui 1 | 43.778877, 11.234874 | 44 eventi
- Teatro della Pergola | Firenze | Via della Pergola 12/32 | 43.773094, 11.261495 | 20 eventi
- Teatro di Fiesole | Fiesole | Largo Piero Farulli 1 | 43.807804, 11.29611 | 14 eventi
- Teatro delle Clarisse | Rapallo | Passo Santa Chiara | 44.34826, 9.235515 | 13 eventi
- Teatrodante Carlo Monni | Campi Bisenzio | Piazza Dante 23 | 43.82095, 11.138124 | 9 eventi
- Piazza Garibaldi | Pisa | Piazza Garibaldi | 43.716443, 10.402228 | 8 eventi
- Palazzo Strozzi | Firenze | Piazza degli Strozzi | 43.771277, 11.251992 | 6 eventi
- Teatro Niccolini | Firenze | Via Ricasoli 3 | 43.773801, 11.256101 | 5 eventi
- Piazza Vittorio Emanuele II | Pisa | Piazza Vittorio Emanuele II | 43.710665, 10.398979 | 5 eventi
- Via Garibaldi | Genova | Via Garibaldi | 44.411524, 8.93253 | 5 eventi
- Teatro Verdi | Firenze | Via Ghibellina 99 | 43.77003, 11.26068 | 4 eventi
- Museo Novecento | Firenze | Piazza di Santa Maria Novella 10 | 43.772866, 11.248841 | 4 eventi
- Teatro di Rifredi (Nuovo Rifredi Scena Aperta) | Firenze | Via Vittorio Emanuele II 303 | 43.79554, 11.241391 | 4 eventi
- Museo La Specola | Firenze | Via Romana 17 | 43.764578, 11.247116 | 4 eventi
- Largo Ciro Menotti | Pisa | Largo Ciro Menotti | 43.717765, 10.402419 | 4 eventi
- Piazza Emile Chanoux | Aosta | Piazza Emile Chanoux | 45.737285, 7.320362 | 4 eventi
- Pieve di Sant'Andrea | Sarzana | Via Rossi | 44.112768, 9.961061 | 4 eventi
- Teatro Goldoni | Firenze | Via Santa Maria 15 | 43.764852, 11.244541 | 3 eventi
- Teatro di Cestello | Firenze | Piazza di Cestello 4 | 43.770173, 11.243725 | 3 eventi
- Chiesa di Santa Brigida | Pontassieve | Via Piana | 43.852379, 11.394862 | 3 eventi
- Piazza Cavour | Barberino di Mugello | Piazza Cavour | 43.99957, 11.239038 | 3 eventi
- Borgo Stretto | Pisa | Borgo Stretto | 43.717426, 10.402247 | 3 eventi
- Piazza XX Settembre | Pisa | Piazza XX Settembre | 43.715398, 10.401601 | 3 eventi
- Piazza Dante Alighieri | Pisa | Piazza Dante Alighieri | 43.717745, 10.399052 | 3 eventi
- Piazza delle Vettovaglie | Pisa | Piazza delle Vettovaglie | 43.716972, 10.401783 | 3 eventi
- Piazza De Ferrari | Genova | Piazza Raffaele De Ferrari | 44.407369, 8.933935 | 3 eventi
- Palazzo dei Vicari | Scarperia e San Piero | Piazza dei Vicari 1 | 43.996166, 11.354539 | 2 eventi
- Galleria dell'Accademia | Firenze | Via Ricasoli 58/60 | 43.776917, 11.258758 | 2 eventi
- Palazzo Pitti | Firenze | Piazza de' Pitti 1 | 43.765281, 11.250257 | 2 eventi
- Limonaia di Villa Vogel | Firenze | Via delle Torri 23 | 43.775731, 11.205745 | 2 eventi
- Parco della Cittadella | Pisa | Lungarno Ranieri Simonelli | 43.715076, 10.389491 | 2 eventi
- Corso Italia | Pisa | Corso Italia | 43.713057, 10.400165 | 2 eventi
- Piazza Chiara Gambacorti | Pisa | Piazza Chiara Gambacorti | 43.714238, 10.401476 | 2 eventi
- Piazza della Vittoria | Genova | Piazza della Vittoria | 44.403074, 8.944988 | 2 eventi
- Piazza Matteotti | Genova | Piazza Giacomo Matteotti | 44.407103, 8.93256 | 2 eventi
- Porto Antico | Genova | Calata Falcone e Borsellino | 44.40937, 8.927403 | 2 eventi
- Biblioteca Civica Gallino | Genova | Via Prete Nicolo' Daste 8a | 44.412276, 8.890533 | 2 eventi
- Cattedrale di Santa Maria Assunta | Sarzana | Piazza Calandrini | 44.112135, 9.962381 | 2 eventi
- Teatro degli Impavidi | Sarzana | Via Mazzini | 44.111616, 9.962905 | 2 eventi
- Biblioteca Comunale | Briga Novarese | Piazza Unità d'Italia | 45.733541, 8.453457 | 2 eventi
- Teatro Faraggiana | Novara | Via dei Caccia, 1F | 45.449516, 8.623644 | 2 eventi
- Cine Teatro Silvio Pellico | Trecate | Piazza Riccardo Cattaneo | 45.430353, 8.739986 | 2 eventi
- Teatro Civico | Oleggio | Via Roma 43 | 45.597431, 8.634455 | 2 eventi
- Teatro Coccia | Novara | Piazza Giacomo Puccini | 45.445529, 8.618166 | 2 eventi

Altri luoghi singoli sono nelle schede (lat, lon e address in ogni evento).

## Lezioni
- I calendari dei portali turistici comunali in Drupal (Destination Florence, VisitGenoa) hanno schede con blocchi
  "Quando / Prezzi / Dove" facili da leggere: una lettura dell'elenco + le schede danno centinaia di eventi.
- Nominatim dalla shell va in rate limit (HTTP 629) quando piu' agenti lo usano: Photon (stessi dati OSM) risponde
  subito; serve sempre il controllo della distanza dal centro del comune (3 punti a 7-37 km scartati).
- Il riconoscimento automatico della categoria dal testo sbaglia sui titoli senza parole chiave (Rent, Il buffo
  mercato del potere): rivedere sempre l'elenco prima di scrivere.

## Problemi
- Non lavorate per tempo: VC, VB, SV, IM e i comuni Valbrevenna, Ceranesi, Cosseria, Castelbianco, Calizzano,
  Borghetto di Vara, Portovenere, Armo, Aquila d'Arroscia, Triora, Antey-Saint-Andre', Introd, Arnad, Castelnuovo di
  Val di Cecina, San Giuliano Terme, Santa Luce; ambiti NO Escursioni, PI Racchetta.
- Aosta: i pomeriggi di Natale nei quartieri Dora (piazza Battaglione Cervino), biblioteca di viale Europa e Cogne
  (via Vuillerminaz) non pubblicati: luoghi non trovati in OSM (solo Excenex aggiunto).
- Sarzana: Christmas Market senza data di chiusura (pubblicato solo il 28/11 con la nota nei fine settimana).
