# Agente giro, notte del 2026-11-28 (terzo giro)

(Riscritto da capo. I due giri precedenti di oggi avevano letto tutte le 41 fonti del giro e aggiunto 61 + 98 eventi, gia'
uniti dal coordinatore. Questo giro ha cercato le date non ancora prese, soprattutto oltre i primi 30 giorni, e ha
riaperto 10 fonti note di ops/fonti.yaml con il controllo piu' vecchio.)

## Numeri
- Eventi aggiunti in config/notte/giro-eventi.yaml: 458 (101 nei prossimi 30 giorni). `python -m pipeline.notte --controlla giro`: parti valide.
  - MyArteven (circuito teatrale regionale del Veneto, fonte nota): 377 repliche di 56 teatri e piazze del Veneto fino al 28/3
    (stagioni di Mestre Toniolo e Teatro del Parco, Thiene, Vicenza, Legnago, Jesolo, San Dona', Bassano, Schio, Portogruaro,
    Rovigo, Cittadella, Castelfranco e altre; rassegne per famiglie di Natale in piazza). Sul sito ce n'erano solo 31.
  - Museo Canova (Possagno): 33 visite guidate dal 19/12 a fine marzo (famiglie, Domenica in mostra, Napoleone, Canova
    neoclassico, Canova che mito, Natale al Museo 29-30/12 e 4-5/1 con prezzo 5 euro). Come il giro precedente, niente
    visite spontanee e in inglese.
  - Gli Alcuni: 15 (date di gennaio-marzo a Padova Teatro Verdi, Teatro San Carlo e Esperia, Sacile Teatro Ruffo, e 3 date
    di marzo a Treviso che il PC non prende perche' oltre le sue 3 pagine). Escluse le repliche "| scuole".
  - Mattorosso (Montebelluna): 14 serate dal 29/12 al 27/2 (solo data, l'elenco non ha orari).
  - Teatro Accademia (Conegliano, fonte nota): 8. Due spettacoli nuovi della prosa (Contrazioni pericolose 10/3, Franciscus
    di Cristicchi 25/3) e 6 eventi che in eventi_redazione hanno fonte TicketOne e sono trattenuti in ops/da-verificare.json,
    ora presi dalla scheda ufficiale del teatro (vedi sotto).
  - Musincantus (fonte nota): 7 spettacoli della stagione CortinAteatro a Cortina d'Ampezzo (comune senza eventi sul sito).
  - Scopri Oderzo: 4 (Portici in Musica 12/12, Grossi guai al Polo Nord 19/12, Concerto di fine anno della Filarmonia
    Veneta 31/12 al Teatro Cristallo, Pan e Vin 6/1).
- Correzioni in config/notte/giro-correzioni.yaml: 5 (Teatro Accademia: Rosencrantz e Guildenstern 6/12, L'amante 16/12,
  Venerdi' 13 10/1, Lungs 21/1, Uno nessuno centomila 9/2 erano senza orario e con official_url sulla pagina generica
  /prosa/: ora ore 21 e scheda dello spettacolo).
- Fonti del giro lette di nuovo: gli-alcuni, museo-canova, teatro-da-ponte (calendario completo: tutte le 39 date fino a
  marzo gia' sul sito), mattorosso, scopri-oderzo (dicembre-marzo), libreria-san-leonardo, comune-paese. Le altre erano
  state lette oggi dai giri precedenti; tutte hanno gia' la data 2026-11-28 in ops/copertura.yaml (aggiunta musincantus).
- Fonti note riaperte (ops/fonti.yaml, controllo piu' vecchio): Musincantus, Teatro Accademia Conegliano, MyArteven, Musei
  Civici Treviso, Sile Classica, Auditorium Maserada, Visit Museum Treviso, Pro Loco Vittorio Veneto, Pro Loco Mogliano,
  FAI Memoriale Brion. Da aggiornare in ops/fonti.yaml (non e' un mio file): ultimo_controllo 2026-11-28; resa Musincantus 7,
  Teatro Accademia 8, MyArteven 377, le altre 0 (gia' tutto sul sito o nessun evento futuro; I racconti del Memoriale finisce il 29/11).
- Ricerche usate: 57 su 100 (0 WebSearch, 21 WebFetch, 36 letture con curl di API, pagine ufficiali e Nominatim).

## Da fare per il coordinatore
- **Teatro Accademia e TicketOne**: in eventi_redazione.yaml ci sono voci con fonte ticketone.it, trattenute. Per sei di
  queste ho messo in giro-eventi le voci con i dati della scheda ufficiale del Teatro Accademia (fonte ammessa, link
  TicketOne solo in ticket_url): Valentina Persia 12/12, Eleazaro Rossi Kamikaze 13/12, Il lago dei cigni 19/12, La
  Sirenetta 20/12 ore 17, South Carolina Mass Choir 22/12, Omaggio a Morricone 9/1. Le vecchie voci TicketOne di questi sei
  vanno tolte da eventi_redazione.yaml (e da ops/da-verificare.json) per non avere doppioni.
- **Michael starring Gus Jackson** (voce TicketOne del 10/12): la scheda del teatro dice 10/12 ore 21 ma il testo parla di
  sabato 7 novembre e di un cambio di interprete: date in conflitto, lasciato trattenuto.
- **Lo Schiaccianoci del Balletto di Siena** (27/12, sito alle 18:00 da scoppiospettacoli.it): l'elenco del Teatro
  Accademia lo mette alle 21:00. Non corretto, da controllare sulla scheda dell'organizzatore.
- ops/fonti.yaml: aggiornare le 10 voci riaperte (sopra). MyArteven diventa la fonte piu' ricca del Veneto per il teatro.
- I 62 luoghi nuovi qui sotto vanno in config/luoghi.yaml.

## Luoghi nuovi (nome | comune | indirizzo | lat, lon | eventi)
Fonti: per i teatri del circuito Arteven indirizzo e coordinate dalla scheda del teatro su myarteven.it (pin Google Maps),
controllate contro il centro del comune in config/comuni.csv (tutti entro 8 km, Venezia-Mestre e Porto Tolle-Scardovari
entro 15 km); dove c'era gia' un punto in config/luoghi.yaml (Teatro Accademico di Castelfranco, Teatro Verdi di Padova,
Esperia) ho usato quello. Adria: coordinate da OpenStreetMap (Teatro Comunale node 13706211082, il pin Arteven ha la
longitudine sbagliata; Politeama node 3353099529), indirizzi da Arteven. Teatro San Carlo di Padova: indirizzo da Gli
Alcuni, punto sulla via (OSM way 23314525, via corta: il teatro non e' su OSM). Cortina: indirizzi da Musincantus,
punti OSM (Alexander Girardi Hall way 112802319, Basilica way 492079070). Teatro Ruffo di Sacile: punto gia' usato
dagli eventi pubblicati.
- Teatro Marconi | Abano Terme | Via San Pio X 1 | 45.36072, 11.78836 | 7 eventi
- Cinema Teatro Politeama | Adria | Corso Vittorio Emanuele II 211 | 45.05129, 12.05751 | 3 eventi
- Teatro Comunale di Adria | Adria | Vicolo Camillo Benso Cavour 9 | 45.05486, 12.05732 | 3 eventi
- Teatro Millepini | Asiago | Via Millepini 1 | 45.87306, 11.50222 | 11 eventi
- Teatro E. Balzan | Badia Polesine | Via Danieli | 45.09402, 11.4899 | 1 eventi
- Teatro Berico | Barbarano Mossano | Via IV Novembre | 45.40952, 11.54032 | 1 eventi
- Castello degli Ezzelini | Bassano del Grappa | Piazza Castello Ezzelini 3 | 45.76911, 11.73046 | 1 eventi
- Teatro Remondini | Bassano del Grappa | Via Santissima Trinita' 8 | 45.76931, 11.7152 | 11 eventi
- Teatro Aurora | Campodarsego | Piazza Europa | 45.50228, 11.90773 | 6 eventi
- Teatro Dario Fo | Camponogara | Piazza Castellaro 36 | 45.383, 12.07193 | 6 eventi
- Teatro parrocchiale di Canda | Canda | Piazza Dante Alighieri | 45.03413, 11.49751 | 1 eventi
- Teatro Cotogni | Castelmassa | Piazza Vittorio Veneto | 45.01715, 11.3084 | 6 eventi
- Teatro Tullio Serafin | Cavarzere | Via Roma 8 | 45.13562, 12.08172 | 8 eventi
- Piazza della Memoria, Fossona | Cervarese Santa Croce | Piazza della Memoria | 45.40258, 11.68883 | 1 eventi
- Auditorium San Nicolo' | Chioggia | Calle San Nicolo' | 45.22043, 12.27911 | 1 eventi
- Teatro Don Bosco | Chioggia | Calle Don Bosco 361 | 45.2158, 12.27664 | 7 eventi
- Teatro Sociale | Cittadella | Via Indipendenza 19 | 45.64859, 11.78031 | 7 eventi
- Alexander Girardi Hall | Cortina d'Ampezzo | Via Marangoni 1 | 46.54033, 12.13141 | 5 eventi
- Basilica dei Santi Filippo e Giacomo | Cortina d'Ampezzo | Corso Italia 88 | 46.53744, 12.13645 | 2 eventi
- Sala Civica | Costermano sul Garda | Via Belvedere | 45.58634, 10.73723 | 1 eventi
- Cinema Teatro Italia | Dolo | Via Comunetto 5 | 45.42646, 12.0738 | 6 eventi
- Teatro Farinelli | Este | Via Antonio Zanchi 5 | 45.2299, 11.65054 | 5 eventi
- Teatro dei Filodrammatici | Este | Via Calle della Musica 13 | 45.22875, 11.65146 | 4 eventi
- Piazza Vendramin | Fiesso Umbertiano | Piazza Vendramin | 44.96122, 11.60545 | 1 eventi
- Teatro parrocchiale di Fiesso Umbertiano | Fiesso Umbertiano | SP20 582 | 44.96227, 11.60131 | 1 eventi
- Biblioteca Civica di Jesolo | Jesolo | Piazzetta Jesolo 1 | 45.53687, 12.63884 | 1 eventi
- Teatro Auditorium Vivaldi | Jesolo | Viale del Bersagliere 1 | 45.50349, 12.62696 | 15 eventi
- Teatro Salieri | Legnago | Via XX Settembre 26 | 45.19134, 11.30761 | 16 eventi
- Piazza Costituzione | Legnaro | Piazza Costituzione | 45.34369, 11.96042 | 3 eventi
- Teatro Comunale Ballarin | Lendinara | Via Gian Battista Conti 4 | 45.08325, 11.59622 | 6 eventi
- Piazza Martiri della Liberta' | Meolo | Piazza Martiri della Liberta' | 45.61895, 12.4527 | 1 eventi
- Teatro Villa dei Leoni | Mira | Riviera Silvio Trentin 3 | 45.4343, 12.12637 | 8 eventi
- Teatro Comunale di Mirano | Mirano | Via della Vittoria 75 | 45.49063, 12.11347 | 6 eventi
- Teatro Sant'Antonio | Montecchio Maggiore | Via Pieve 6, Alte Ceccato | 45.50898, 11.40023 | 6 eventi
- Teatro Modernissimo | Noventa Vicentina | Via Broli 6 | 45.28851, 11.53385 | 10 eventi
- Palazzetto dello Sport F. Fontebasso | Noventa di Piave | Via Guaiane | 45.66372, 12.53538 | 4 eventi
- Piccolo Teatro | Padova | Via Asolo 2 | 45.38249, 11.85213 | 6 eventi
- Teatro San Carlo | Padova | Via Pietro Giovanni Guarneri 22 | 45.42726, 11.88874 | 5 eventi
- Piazza Vittorio Emanuele II | Piove di Sacco | Piazza Vittorio Emanuele II | 45.29704, 12.03495 | 3 eventi
- Teatro Filarmonico | Piove di Sacco | Piazza Giacomo Matteotti 5 | 45.29615, 12.03374 | 10 eventi
- Teatro parrocchiale di Scardovari | Porto Tolle | Viale della Repubblica 6 | 44.89875, 12.45101 | 1 eventi
- Sala Eracle | Porto Viro | Corso Risorgimento 119 | 45.0241, 12.21701 | 2 eventi
- Teatro Russolo | Portogruaro | Via Silvio Pellico | 45.77761, 12.83699 | 12 eventi
- Auditorium Sant'Antonio | Rosolina | Via Don Giuseppe Sambo | 45.07677, 12.24679 | 1 eventi
- Teatro Sociale | Rovigo | Piazza Giuseppe Garibaldi 14 | 45.0705, 11.7894 | 7 eventi
- Teatro Ruffo | Sacile | Piazzetta Antonio Pasqual 22 | 45.95308, 12.50255 | 4 eventi
- Teatro Metropolitano Astra | San Donà di Piave | Via Giannino Ancillotto 16 | 45.63067, 12.56248 | 17 eventi
- Auditorium Quirino De Giorgio | San Giorgio delle Pertiche | Via Roma 364 | 45.54297, 11.8762 | 2 eventi
- Cinema Teatro Giardino | San Giorgio delle Pertiche | Via Roma 64 | 45.54163, 11.91255 | 3 eventi
- Teatro R. Pascutto | San Stino di Livenza | Via Papa Giovanni XXIII 7 | 45.72891, 12.67573 | 10 eventi
- Teatro Astra | Schio | Via Battaglione Val Leogra 45 | 45.71306, 11.35861 | 3 eventi
- Teatro Civico | Schio | Via Pietro Maraschin 19 | 45.7124, 11.35383 | 10 eventi
- Teatro Jubilaeum 2000 | Stienta | Via Giovanni XXIII 54 | 44.93759, 11.54321 | 1 eventi
- Teatro Comunale di Thiene | Thiene | Viale Francesco Bassani 28 | 45.70795, 11.47854 | 30 eventi
- Teatro Comunale Martini | Trecenta | Piazza Giuseppe Garibaldi 1 | 45.03148, 11.46065 | 1 eventi
- Teatro Cinema Super | Valdagno | Viale Trento 28 | 45.64678, 11.29851 | 6 eventi
- Teatro Toniolo, Mestre | Venezia | Piazzetta Cesare Battisti 1 | 45.49321, 12.23773 | 40 eventi
- Teatro del Parco, Mestre | Venezia | Via Sergio Gori 11, Parco Albanese | 45.49952, 12.25798 | 13 eventi
- Teatro Camploy | Verona | Via Cantarane 32 | 45.43921, 11.01095 | 6 eventi
- Teatro Comunale di Vicenza, Ridotto | Vicenza | Viale Giuseppe Mazzini 39 | 45.54807, 11.53191 | 4 eventi
- Teatro Comunale di Vicenza, Sala Maggiore | Vicenza | Viale Giuseppe Mazzini 39 | 45.54807, 11.53191 | 12 eventi
- Teatro Comisso di Villa Guidini | Zero Branco | Via G. B. Guidini | 45.60837, 12.17951 | 1 eventi

## Fonti del giro: esito
- gli-alcuni: curl riceve l'anti-bot anche sulla prima pagina; WebFetch legge l'API (50 eventi dal 7/1, 470 mila
  caratteri, 5 letture con offset), la pagina 2 (21-28 marzo) no. Nota in config/sources.yaml.
- museo-canova: API ok; le visite di gennaio-marzo non erano sul sito (il PC non ha mai letto questa fonte: tutti gli
  eventi Canova sul sito vengono dalla redazione). La scheda Natale al Museo dice "dal 26 dicembre al 6 gennaio ogni giorno
  alle 11 e alle 16", ma l'API ha solo 7/12, 28-30/12 e 4-5/1: messe solo le date dell'API.
- teatro-da-ponte: curl anti-bot, WebFetch ok; nessuna data mancante.
- mattorosso: elenco fino al 27/2.
- scopri-oderzo: ogni mese ha JSON-LD Event (con location virtuale); febbraio e marzo vuoti. Nota in config/sources.yaml.
- libreria-san-leonardo: con curl /notes si legge (WebFetch no); ultimo incontro il 27/11, nessuno futuro. Nota aggiunta.
- comune-paese: la home e' MyPortal ma non mostra il codice IPA; non risolto (nessuna modifica).
- Nuova fonte in config/sources.yaml: **musincantus** (tribe_api, https://www.musincantus.it).

## Fonti nuove da catalogare
- **MyArteven, calendario delle repliche** | https://www.myarteven.it/ | la home contiene nel sorgente un array JSON
  `rappresentazionitotal = [...]` con tutte le repliche (484, dal giorno a maggio): data, ora, slug, teatro con indirizzo e
  coordinate, spettacolo con compagnia e descrizione, rassegna. Schede: /rassegne/<rassegna>/<spettacolo>/<replica>. Tipo
  teatro (circuito regionale), query: nessuna, leggere la home con curl. Ammessa (sito ufficiale, robots rispettato). Merita
  un collettore apposta nel PC (nessun tipo di config/sources.yaml lo legge oggi).
- **Teatro Accademia, tutti gli eventi** | https://teatroaccademia.it/events/ (e /events/elenco/pagina/2/) | teatro | anche
  gli spettacoli di organizzatori esterni, con link TicketOne: fonte ammessa per eventi che altrimenti arrivano da TicketOne.
  curl riceve l'anti-bot, WebFetch legge.
- **Musincantus CortinAteatro** | https://www.musincantus.it/wp-json/tribe/events/v1/events | stagione teatrale di Cortina
  d'Ampezzo | ora in config/sources.yaml.

## Lezioni
- Prima di riaprire una fonte nota con WebFetch conviene un curl della home: MyArteven (6,8 MB) aveva tutto il calendario
  regionale dentro la pagina, 377 eventi nuovi con una sola lettura.
- I siti ospitati dallo stesso hosting di live.alcuni.it, teatrolorenzodaponte.it e teatroaccademia.it rispondono a curl
  con la pagina "One moment, please": WebFetch invece passa.
- Il controllo doppioni automatico va fatto con il comune e con una soglia di parole in comune del 60%, e senza contare il
  proprio file di uscita (altrimenti gli eventi si scartano da soli).
- Il nome della compagnia in Arteven spesso e' il nome dell'attore: nei riassunti ho scritto "con <nome>" e non "della compagnia".

## Problemi
- Gli Alcuni pagina 2 (5 date del 21-28 marzo) non leggibile.
- MyArteven: 16 repliche saltate per luogo senza coordinate affidabili (Tecnogas Auditorium di Albignasego, 9 date;
  piazze di Pegolotte di Cona, Ceggia, Montemerlo di Cervarese, Golena del Piave a Noventa, teatro parrocchiale di Ficarolo,
  Sala Jacopo da Ponte di Bassano) e 1 replica di mattina in un giorno feriale (probabile replica per le scuole).
- Titoli Arteven sono in maiuscolo: convertiti con maiuscole a ogni parola tranne articoli e preposizioni; qualche titolo
  puo' avere maiuscole poco naturali.
