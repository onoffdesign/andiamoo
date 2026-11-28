# Agente italia-b, notte del 2026-11-28 (Emilia-Romagna e Piemonte)

Province: RA, FE, RN, PC (Emilia-Romagna), TO, CN, NO, AL, AT, BI (Piemonte). Prima di stanotte nessuna di queste
aveva eventi futuri sul sito (`--comune` = 0 per tutti i capoluoghi e i comuni toccati).

## Numeri
- Eventi in `config/notte/italia-b-eventi.yaml`: **183** (`python -m pipeline.notte --controlla italia-b`: "Parti valide").
- Correzioni: nessuna (nessun evento esistente in queste province). Niente file `italia-b-correzioni.yaml`.
- Ricerche usate: **124 su 125** (14 WebSearch, 3 WebFetch, 77 letture dirette con curl di pagine, API e PDF ufficiali,
  30 chiamate a Nominatim per le coordinate; contata una per pagina o chiamata).
- 114 eventi su 183 con lat/lon (agende OpenCity di Alfonsine e Massa Lombarda, oppure OpenStreetMap incrociato con
  l'indirizzo della fonte ufficiale); gli altri hanno via e civico dalla fonte e vanno al geocoder del PC.

| Regione | Prov. | Eventi | Comuni |
|---|---|---|---|
| Emilia-Romagna | RA | 27 | Ravenna 11, Alfonsine 14, Massa Lombarda 2 |
| Emilia-Romagna | PC | 19 | Piacenza 19 |
| Emilia-Romagna | FE | 15 | Ferrara 15 |
| Emilia-Romagna | RN | 12 | Misano Adriatico 11, Rimini 1 |
| Piemonte | NO | 31 | Novara 25, Oleggio 4, Sozzago 1, Carpignano Sesia 1 |
| Piemonte | TO | 25 | Torino 22, Ivrea 2, Sant'Ambrogio di Torino 1 |
| Piemonte | AL | 19 | Alessandria 19 |
| Piemonte | BI | 18 | Biella 18 |
| Piemonte | CN | 13 | Cuneo 13 |
| Piemonte | AT | 4 | Asti 4 |

Totale Emilia-Romagna 73, Piemonte 110. Per categoria: teatro-spettacoli 66, arte-cultura 35, musica 33,
famiglie-bambini 24, sagre-feste 11, sport 7, mercatini-fiere 6, natura-outdoor 1.

Ambiti di categoria: RA Festival musicali (IMAGinACTION al Teatro Alighieri), PC Letture e biblioteche (Natale nelle
biblioteche: Passerini-Landi), NO Tecnologia e scienza (Dialoghi con la scienza al Castello), BI Comunita' (mercatino
solidale del volontariato), FE Musical e operetta (cercato nel cartellone del Comunale: nessun musical nei prossimi 60
giorni). **Non cercati per budget**: RN Vino e bevande, TO Formazione, CN Sport di precisione, AL Sport tradizionali,
AT Ambiente.

Comuni del piano non controllati (restano senza data in copertura): Maiolo, Casteldelci (RN); Castelvetro Piacentino,
Coli, Villanova sull'Arda (PC); Rosta, Azeglio, Andrate (TO); Roascio, Salmour, Roddino (CN); Gavi, Casaleggio Boiro,
Pontestura (AL); Portacomaro, Cinaglio (AT); Mezzana Mortigliengo, Graglia, Occhieppo Superiore (BI).
Controllati solo con una ricerca senza risultati: Casola Valsenio (il sito non risponde all'API OpenCity),
Portomaggiore, Goro, Moncalvo (Fiera del Bue Grasso 2026 senza date ufficiali trovate).

## Fonti nuove da catalogare (per ops/fonti.yaml; le strutturate anche per config/sources.yaml)
Strutturate (priorita' alta):
- **Comune di Alfonsine, agenda OpenCity** | https://www.comune.alfonsine.ra.it/api/opendata/v2/content/search/ |
  query `classes [event] and calendar[time_interval] = [AAAA-MM-GG,AAAA-MM-GG] limit 100` (14 eventi fino al 31/1); i
  luoghi con indirizzo e coordinate con `classes [place] limit 200` (campo `has_address`) | comune | RA.
- **Comune di Massa Lombarda, agenda OpenCity** | https://www.comune.massalombarda.ra.it/api/opendata/v2/content/search/ |
  stessa query (12 eventi, molti corsi e periodi lunghi da filtrare) | comune | RA. Probabilmente vale per tutti i comuni
  dell'Unione della Bassa Romagna (Lugo, Bagnacavallo, Cotignola, Conselice, Fusignano, Bagnara, Sant'Agata):
  candidata a fonte del giro. Ravenna, Casola Valsenio e Misano non rispondono.
- **Fondazione Teatri di Piacenza** | https://teatripiacenza.it/ | **The Events Calendar**:
  `https://teatripiacenza.it/wp-json/tribe/events/v1/events?per_page=50&start_date=...&end_date=...` (12 eventi fino al
  31/1; il venue e' solo il nome della sala, senza indirizzo) | sede | PC.
- **ATL Novara, calendario provinciale in PDF** | https://www.turismonovara.it/it/doc/eventimanifestazioni?PrintPDF=1 |
  un PDF di 46 pagine con tutti gli eventi della provincia da oggi in poi (circa 260 voci con data, comune, luogo
  spesso con indirizzo, orario e descrizione); si legge con pdftotext | ufficio turistico | NO. Le schede web sono
  `appuntamentischeda?Id=N` ma il PDF non le riporta: come official_url ho usato la pagina dell'elenco.
- **Cuneo Cultura (portale cultura del Comune)** | https://cuneocultura.it/wp-json/wp/v2/evento?per_page=100&orderby=modified&order=desc |
  WordPress con tipo `evento` (94 voci), date solo nel testo del contenuto; schede `/evento/<slug>/` | comune | CN.
- **Teatro Regio di Torino** | https://www.teatroregio.torino.it/opera-e-balletto-2026-2027/<slug> | la scheda di ogni
  titolo ha il "Calendario rappresentazioni" con data e ora in chiaro (`2026-12-10 20:00:00 Europe/Rome`); il calendario
  generale e' in JavaScript | sede | TO.
- **Comuni piemontesi con Drupal "vivere-comune/eventi"** (Asti, Alessandria, Novara, Torino): filtro
  `?f%5B0%5D=quando%3Anext_thirty_days&page=N` (stesso di Pavia). Asti 5 eventi, Alessandria 2 (ma l'evento Natale ha il
  programma completo in PDF allegato `/media/1835`, 14 pagine, circa 120 appuntamenti) | comune | AT, AL.

Non strutturate ma utili (una lettura, molti eventi):
- **Teatro Alighieri di Ravenna** | https://www.teatroalighieri.org/spettacoli/ (paginato `/page/N/`) | elenco con date,
  orari e prezzi nelle schede `/events/<slug>/` | sede | RA.
- **Teatro Comunale di Ferrara** | https://www.teatrocomunaleferrara.it/ | curl bloccato da verifica anti bot, WebFetch
  legge la home con tutto il calendario fino a fine gennaio (40 date) | sede | FE.
- **Comune di Piacenza, Natale a Piacenza** | https://www.comune.piacenza.it/it/page/natale-a-piacenza | calendario
  giorno per giorno fino al 24/1 (piazza, biblioteche, teatri) | comune | PC. Il sito e' Municipium (`/it/events`).
- **Ferrara Terra e Acqua, eventi multipli per comune** | https://www.ferrarainfo.com/it/vivi-gli-eventi/tutti-gli-eventi/eventi-multipli/eventi-argenta-2026 |
  le liste principali sono in JavaScript | ufficio turistico | FE.
- **Visit Misano, Natale** | https://visitmisano.it/natale/ | programma completo con orari e luoghi | ufficio turistico | RN.
- **Sagra Musicale Malatestiana 2026, programma PDF** | https://www.comune.rimini.it/system/files/2026-05/Programma%20Sagra%20Musicale%20Malatestiana%202026_rev%201405.pdf | comune | RN.
- **Turismo Torino, agenda** | https://turismotorino.org/it/visita/eventi/agenda | prime 16 voci in HTML (mostre con
  periodo), schede con "Le sedi", "Tariffe", "Date e Orari" | ufficio turistico | TO.
- **Comune di Biella, Natale nel cuore di Biella 2026** | https://comune.biella.it/wp-content/uploads/sites/150/2026/11/Natale-nel-Cuore-di-Biella-2026.doc |
  file Word (convertito con `soffice --headless --convert-to txt`) | comune | BI. Stagione del Teatro Odeon:
  https://comune.biella.it/wp-content/uploads/sites/150/2026/10/Libretto-Biella-26-27.pdf (orario fisso 20.45).
- **Comune di Cuneo, eventi** | https://www.comune.cuneo.it/vivere-il-comune/eventi/ | 34 eventi | comune | CN.

Da verificare (visti solo nei risultati di ricerca, non aperti): ravennanotizie.it, ravennatoday.it, ilrestodelcarlino.it,
mentelocale.it, milazzo.life, ilpiccolo.org, ravennawebtv.it, risveglioduemila.it, viviromagna.it, mincioedintorni.com,
contattoradio.it, ravenna24ore.it, natoconlavaligia.info, italia-italy.org, castelliemiliaromagna.it, correggiolo.it,
lapiazzarimini.it, chiamamicitta.it, altarimini.it, riminitoday.it, viaggiando-italia.it, hotelmisanoadriatico.it,
giornalesm.com, drintle.com, viking.rimini.it, vitaromagna.it, piacenzasera.it, ilpiacenza.it, vivipiacenza.it,
leggerepiace.it, laguida.it, good-vibrations.it, gazzettadasti.it, atnews.it, oblo.it, daop.it, italianascosta.it,
sagr.it, camperonline.it, vitacasalese.it, ilbiellese.it, radiogold.it, piemonte.uno, songkick.com, zero.eu,
operawire.com, eventivalsesia.info. Ufficiali non ancora aperti: visitlmr.it (ATL Langhe Monferrato Roero, la scheda
trovata era un 404), atl.biella.it, cuneoalps, riminiturismo.it (503 sia a curl sia a WebFetch).

## Luoghi nuovi verificati (per config/luoghi.yaml)
Coordinate da OpenStreetMap (Nominatim) incrociate con l'indirizzo della fonte ufficiale, salvo dove indicato.
- Teatro Regio | Torino | Piazza Castello 215 | 45.0705924, 7.6879559 | teatroregio.torino.it + OSM
- Teatro Alighieri | Ravenna | Via Mariani 2 | 44.4171588, 12.2012762 | teatroalighieri.org + OSM
- Teatro Coccia | Novara | Via Fratelli Rosselli 47 | 45.4455285, 8.6181663 | OSM (lato piazza Puccini)
- Teatro Filodrammatici | Piacenza | Via Santa Franca 33 | 45.0493042, 9.6912564 | comune.piacenza.it + OSM
- Teatro Municipale (anche Ridotto e Foyer) | Piacenza | Via Verdi 41 | 45.0492446, 9.6935274 | teatripiacenza.it + OSM
- Biblioteca Passerini-Landi | Piacenza | Via Carducci 14 | 45.0525583, 9.6960579 | OSM
- Teatro Toselli | Cuneo | Via Teatro Toselli 9 | 44.3937032, 7.5534639 | OSM (Teatro Civico Toselli)
- Complesso Monumentale di San Francesco | Cuneo | Via Santa Maria 10 | 44.3947802, 7.5508070 | comune.cuneo.it + OSM
- Castello Visconteo Sforzesco | Novara | Piazza Martiri della Liberta' 3 | 45.4444134, 8.6172913 | OSM
- Basilica di San Gaudenzio | Novara | Via Carlo Bescape' | 45.4487452, 8.6194275 | OSM
- Teatro Civico | Oleggio | Via Roma 43 | 45.5974311, 8.6344550 | turismonovara.it + OSM
- Museo Civico C.G. Fanchini | Oleggio | Vicolo della Chiesa 1 | 45.5960658, 8.6385655 | OSM
- Teatro Alfieri | Asti | Via al Teatro Alfieri | 44.8998797, 8.2058561 | OSM
- Teatro San Francesco | Alessandria | Via San Francesco d'Assisi 15 (OSM: 13) | 44.9110692, 8.6104714 | programma del Comune + OSM
- Piazza della Repubblica | Misano Adriatico | 43.9780026, 12.6983485 | OSM
- Cinema Teatro Astra | Misano Adriatico | Via Gabriele D'Annunzio | 43.9782355, 12.7001651 | visitmisano.it + OSM
- Teatro Amintore Galli | Rimini | Piazza Cavour 22 | 44.0601662, 12.5648638 | OSM
- Santuario di Oropa | Biella | Via Santuario di Oropa | 45.6257302, 7.9824967 | OSM
- Citta' Studi (Auditorium) | Biella | Via Carlo Antonio Azario | 45.5559091, 8.0328237 | OSM, da confermare l'ingresso
- Teatro Odeon | Biella | Via Torino (Chiavazza) | 45.5570472, 8.0623801 | **solo OSM**: indirizzo da confermare
- Alfonsine (agenda OpenCity del Comune, campo has_address): Teatro Vincenzo Monti, Corso Repubblica 24, 44.506618,
  12.040245; Cineteatro Gulliver, Piazza della Resistenza 2, 44.507398, 12.039267; Museo della battaglia del Senio,
  Piazza della Resistenza 2, 44.507448, 12.038936; Biblioteca P. Orioli, Piazza della Resistenza 2, 44.507482,
  12.038451; Piazza Gramsci 44.505539, 12.041005; Piazza Monti 44.499689, 12.040951; Palazzo Marini, Via Roma 10,
  44.499054, 12.042335; Casa Monti, Via Passetto 3, 44.515198, 12.032835; Centro polivalente di Longastrino, Via Bassa
  59, 44.58685, 12.007887.
- Massa Lombarda (OpenCity): Sala del Carmine, Via Rustici angolo Corso Vittorio Veneto, 44.446081, 11.829286; Centro
  di Quartiere di Fruges, Via San Giacomo, 44.45059, 11.804697.
- Senza coordinate (indirizzo dalla fonte, da geocodificare): Teatro Comunale Claudio Abbado di Ferrara (Corso Martiri
  della Liberta' 5, Nominatim non lo trova), Ex Complesso San Francesco di Alessandria (Via XXIV Maggio 5), Biblioteca
  0-18 di Cuneo (Via Santa Maria 11), Biblioteca Civica Francesca Calvo (Piazza Vittorio Veneto 1, Alessandria).

## Eventi visti ma non pubblicati
- Argenta: 3 visite al Museo Civico (13, 20, 27/12) e Piacenza: 2 appuntamenti alla Biblioteca Ragazzi Giana
  Anguissola (3 e 12/12): tolti perche' l'indirizzo del luogo non e' stato trovato entro la quota.
- Biella: Capodanno al Biella Forum (31/12 ore 22) tolto per indirizzo non verificato; Befana del 6/1 con l'anno
  sbagliato nel programma (06/01/2026).
- Rimini: Concerto di Natale per la Citta' (9/12 nel PDF di maggio, 11/12 in altre fonti): date in conflitto.
- Piacenza: Concerto di San Silvestro (18.00 per il teatro, 18.30 per il Comune) e AperiOpera (tenuto l'orario del
  teatro, 18.00); Luna di caffe' (29/11) senza luogo.
- Misano: teatro ragazzi dell'8/12 con titolo uguale a quello del 13/12 (probabile refuso).
- Torino: i titoli di Turismo Torino (Brachetti, Notre Dame de Paris, Sere di Natale alla Reggia, World Press Photo,
  Jessica Lange) non aperti per quota; Teatro Stabile (le pagine "in scena" sono vecchie, il calendario e' assente).
- Novara: nel PDF dell'ATL restano circa 200 voci non usate (provincia intera: Borgomanero, Galliate, Arona...).
- Alessandria: il programma del Natale ha molti altri appuntamenti nei quartieri e a Spinetta Marengo (laboratori del
  Bianconiglio, sfilate, Christmas Show al Quartiere Cristo) non inseriti per tempo.

## Lezioni per ops/metodo-ricerca.md
- **Emilia-Romagna**: i comuni dell'Unione della Bassa Romagna sono OpenCity e rispondono all'API opendata come quelli
  trentini e vicentini; i luoghi con coordinate si leggono con `classes [place]`. Nei teatri di tradizione le schede
  evento hanno orari e prezzi, gli elenchi solo le date.
- **Piemonte**: gli uffici turistici sono la fonte piu' ricca: l'ATL di Novara esporta in PDF l'intero calendario
  provinciale (una lettura, centinaia di eventi). I comuni capoluogo (Asti, Alessandria, Novara, Torino) usano lo stesso
  Drupal con il filtro `quando:next_thirty_days`; i programmi natalizi completi stanno negli allegati PDF o Word delle
  pagine evento (i .doc si convertono con soffice in locale, a costo zero).
- Nominatim non trova i teatri con il nome "Claudio Abbado" o le biblioteche ragazzi: cercare con via e civico.

## Problemi
- Lo scratchpad e' condiviso con un altro agente: un mio script (`scratchpad/txt.py`) e' stato sovrascritto a meta'
  notte; ho spostato i miei file in `scratchpad/italia-b/`. Conviene dare a ogni agente una sottocartella.
- curl non raggiunge teatrogalli.it, riminiturismo.it e fondazioneteatrococcia.it (connessione chiusa dal proxy); il
  Teatro Comunale di Ferrara ha una verifica anti bot (WebFetch funziona).
- `ops/copertura.yaml`: toccate solo `province` (10 sigle) e le nuove sezioni `comuni_RA`...`comuni_BI` e
  `categorie_RA`, `categorie_FE`, `categorie_PC`, `categorie_NO`, `categorie_BI`.
- Alcuni official_url sono pagine di programma (Natale a Piacenza, Natale ad Alessandria e Biella, calendario ATL
  Novara, PDF della Sagra Malatestiana) perche' i singoli appuntamenti non hanno una scheda propria.
