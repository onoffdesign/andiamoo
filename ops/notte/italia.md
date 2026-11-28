# Agente italia, notte del 2026-11-28 (fase 2b, Resto d'Italia)

Secondo tentativo della notte: WebFetch e rete funzionano. Il primo tentativo (6 ricerche, nessun evento) e' superato da questo.

## Numeri
- Eventi aggiunti in `config/notte/italia-eventi.yaml`: **226** (prima nessun evento futuro in tutti i 40 comuni assegnati).
- `config/notte/italia-correzioni.yaml`: vuoto (nessun evento esistente da correggere in queste province).
- `python -m pipeline.notte --controlla italia`: "Parti valide".
- Ricerche usate: circa 104 su 125 in questo tentativo (14 WebSearch, 8 WebFetch, il resto letture dirette con curl di pagine e API ufficiali, contate una per pagina o per chiamata), piu' le 6 del primo tentativo.

| Prov. | Eventi | Comuni | Categorie |
|---|---|---|---|
| BL | 34 | Belluno 32, Ponte nelle Alpi 2 | teatro-spettacoli 15, musica 11, arte-cultura 4, famiglie 3, sport 1 |
| TS | 31 | Trieste 31 | musica 22, teatro-spettacoli 7, famiglie 1, arte-cultura 1 |
| VR | 30 | Verona 30 | famiglie 13, musica 6, arte-cultura 6, sport 2, sagre-feste 2, mercatini 1 |
| VI | 29 | Vicenza 25, Montecchio Maggiore 3, Mussolente 1 | teatro 7, musica 7, arte-cultura 5, mercatini 4, famiglie 2, sport 2, sagre-feste 2 |
| PD | 26 | Padova 26 | teatro 10, mercatini 4, sagre-feste 3, musica 3, arte-cultura 3, famiglie 2, sport 1 |
| PN | 25 | Pordenone 25 | musica 11, sagre-feste 6, arte-cultura 4, altre 4 |
| VE | 24 | Venezia 22, Fossalta di Piave 2 | musica 12, teatro-spettacoli 7, famiglie 5 |
| UD | 14 | Udine 10, Tarcento 4 | arte-cultura 6, famiglie 6, sport 1, mercatini 1 |
| GO | 12 | Gorizia 12 | teatro-spettacoli 6, musica 3, famiglie 3 |
| RO | 1 | Adria 1 | arte-cultura 1 |

Comuni senza eventi trovati (controllati e scritti in copertura): Conselve, Bovolone, Bosco Chiesanuova, Velo Veronese,
Altavilla Vicentina, Eraclea, Concordia Sagittaria, Alano di Piave (niente nel portale Dolomiti Prealpi), Bertiolo
(pagina eventi del Comune: "Nessun evento in programma"), Palmanova, Casarsa della Delizia, Polcenigo, Sgonico, Monrupino,
San Dorligo della Valle, Monfalcone, San Canzian d'Isonzo, Villesse. Non controllati: Vescovana, Vo', Pettorazza Grimani,
Ceneselli, La Valle Agordina, Frisanco.

## Fonti nuove da catalogare (per ops/fonti.yaml; le strutturate anche per config/sources.yaml)
Strutturate (priorita' alta, coprono la provincia da sole):
- **Dolomiti Prealpi** (turismo Valbelluna, Feltrino, Alpago) | https://www.dolomitiprealpi.it/ | **The Events Calendar**: `https://www.dolomitiprealpi.it/wp-json/tribe/events/v1/events?per_page=50&start_date=AAAA-MM-GG&end_date=AAAA-MM-GG` (148 eventi in 120 giorni) | tipo: ufficio turistico | BL. Attenzione: eventi importati da Feratel senza `venue` ne' orario (start_date solo data): luogo e ora sono nel testo di `description` ("si terra' ... presso il Teatro Comunale Dino Buzzati"). Un caso di data incoerente (Katia Follesa: API febbraio, testo 5 marzo), escluso.
- **VIVA, agenda del Comune di Vicenza** | https://eventi.comune.vicenza.it/Eventi | API OpenCity/OpenContent: `https://eventi.comune.vicenza.it/api/opendata/v2/content/search/classes [event] and calendar[time_interval] = [2026-11-28,2026-12-31] limit 100` (239 eventi a dicembre, paginazione con `nextPageQuery`) | tipo: comune | VI. Campi: `event_title`, `time_interval.recurrences`, `takes_place_in`, `cost_notes`, `is_accessible_for_free`. Link pubblico: `/content/view/full/<mainNodeId>` (canonical `/Eventi/<Titolo>`).
- **Comune di Verona, agenda** | https://www.comune.verona.it/Vivere-il-comune/Eventi/ | stessa API OpenCity su `www.comune.verona.it/api/opendata/v2/...` (94 eventi a dicembre; tanti corsi ricorrenti dei Centri di Comunita' da scartare) | comune | VR. La pagina HTML non mostra eventi (caricati via JS): usare l'API.
- **Comune di Udine, agenda** | https://www.comune.udine.it/Vivere-il-comune/Eventi | stessa API OpenCity (24 eventi a dicembre, soprattutto Civici Musei); luogo con coordinate in `virtual_takes_place_in` | comune | UD.
- **Sala Luttazzi (Comune di Trieste)** | https://salaluttazzi.comune.trieste.it/ | **The Events Calendar**: `/wp-json/tribe/events/v1/events` (27 eventi fino a marzo) | sede/comune | TS. `venue` vuoto: tutti in Sala Luttazzi.
- **Natale a Pordenone (Comune)** | https://natale.comune.pordenone.it/ | una pagina con 151 schede (titolo, data e ora in chiaro, luogo spesso nel testo), link alle schede di comune.pordenone.it | comune | PN. Non strutturata (WordPress con Elementor, niente tribe), ma leggibile con una sola lettura.

Non strutturate ma utili:
- **Padova Cultura (Comune)** | https://padovacultura.padovanet.it/it/manifestazioni | rassegne e stagioni con date; schede come /it/attivita-culturali/natale-padova-2026 | comune | PD.
- **Turismo Padova (Comune)** | https://www.turismopadova.it/eventi/ | 10 pagine di schede /evento/<slug>/; JSON-LD solo WebPage (Yoast), niente tribe | ufficio turistico | PD.
- **Visit Verona (DMO)** | https://www.visitverona.it/it/eventi/ | elenco caricato via JS, ma le schede /it/eventi/<slug> si leggono (data in "19 dicembre 2026 h 20:30") | ufficio turistico | VR.
- **Comune di Vicenza, comunicati** | https://www.comune.vicenza.it/Novita/Comunicati/ | programma del Natale | comune | VI.
- **Teatro La Fenice** | https://www.teatrolafenice.it/calendario/ | calendario completo con orari (stagione intera in una lettura) | sede | VE.
- **Teatro Lirico Giuseppe Verdi di Trieste** | https://www.teatroverdi-trieste.com/it/calendario-spettacoli/ | stagione completa | sede | TS.
- **Turismo FVG** | https://www.turismofvg.it/eventi/<slug> | schede leggibili con curl (data, ora, luogo, organizzatore) | ufficio turistico regionale | UD, PN, TS, GO. Pagina del 36o Festival Teatrale Castello di Gorizia con tutto il programma.
- **Sistema Bibliotecario Provinciale di Rovigo** | https://opacnow.provincia.rovigo.it/it/now/collettivo/eventi | eventi delle biblioteche di tutta la provincia | ente | RO.
- **Siti comunali Municipium** (pagina `/it/events`, schede `/it/eventi/<slug>` con "Date e orari", "Costo", "Luogo"): comune.montecchio-maggiore.vi.it, comune.mussolente.vi.it, comune.tarcento.ud.it. **Siti WordPress "Design Comuni"** (`/eventi/`): comune.fossaltadipiave.ve.it, comune.bertiolo.ud.it.

Da verificare (non usati: aggregatori/testate non ancora in fonti-vietate.yaml come ammesse): mentelocale.it/rovigo (risultava
"da verificare"), eventiesagre.it (da verificare), milazzo.life, siviaggia.it, ilrestodelcarlino.it.

## Eventi visti ma non pubblicati
- Venezia: live.comune.venezia.it, www.comune.venezia.it e www.veneziaunica.it rispondono con una pagina di protezione
  Incapsula (212 byte, niente contenuto): mercatini di Mestre, pista di Campo San Polo, Corteo Acqueo dei Babbi Natale (20/12)
  restano da confermare su altra fonte ammessa. Proposta: aggiungere i tre domini a ops/domini-illeggibili.yaml.
- Fenice: il concerto Frizza del 28/11 e' cancellato (pubblicata solo la replica del 29/11).
- Rovigo: Teatro Sociale (Oratorio di Natale 15/12 20:30 e altri) visto solo in riassunti di ricerca e su mentelocale; il sito
  del Comune (MyPortal 3) e' una pagina JavaScript vuota per WebFetch e curl.
- Verona: Mercatini di Natale, l'agenda dice fine 28/12 nelle ricorrenze ma 27/12 nel testo: pubblicato con fine 27/12.
- Pordenone: pagina "Capodanno a Pordenone 2026" del Comune e' dell'edizione 2025/26 (aggiornata il 30-12-2025): non usata;
  il Capodanno 2026/27 (Planet Funk) viene da natale.comune.pordenone.it. "Melting Christmas" 13-14/12 ha i giorni della
  settimana del 2025: non usato.
- Trieste: Concerto di Fine Anno del Verdi (31/12 18:00) etichettato "Stagione 2025/26": non pubblicato.
- Padova: La Traviata, la scheda dice "mercoledi' 29 dicembre" ma il 29/12/2026 e' martedi'; le date 28, 29, 31 coincidono con
  padovacultura, pubblicate.

## Lezioni per ops/metodo-ricerca.md
- Comuni su piattaforma OpenCity/OpenContent (URL `/Vivere-il-comune/Eventi/` o `eventi.comune.X.it`): l'elenco HTML spesso e'
  vuoto, ma l'API `/api/opendata/v2/content/search/classes [event] and calendar[time_interval] = [da,a] limit 100` da' tutti gli
  eventi con date, luoghi e costi. Funziona a Vicenza, Verona, Udine: provarla su ogni Comune con quel tema.
- Portali turistici WordPress: provare sempre `/wp-json/tribe/events/v1/events` (Dolomiti Prealpi, Sala Luttazzi lo hanno;
  turismopadova.it e teatrolafenice.it no).
- Siti comunali Municipium: `/it/events` elenca tutto in HTML statico; le schede hanno orari e costo. I siti comunali FVG della
  Regione (Palmanova, Casarsa, Polcenigo, Monfalcone, San Canzian, Villesse) sono invece JavaScript puro: inutile leggerli.
- I siti MyPortal 3 della Regione Veneto (comune.rovigo.it, comune.concordiasagittaria.ve.it) sono pagine vuote: cercare il
  programma su teatri, biblioteche (opacnow.provincia.rovigo.it) o comunicati.
- Venezia: i domini del Comune e di Venezia Unica sono protetti da Incapsula; partire da Fenice, Musei Civici e altre sedi.
- Per i piccoli comuni una ricerca generica restituisce quasi solo aggregatori vietati o da verificare: meglio provare
  direttamente `/it/events` (Municipium) o `/eventi/` (Design Comuni WordPress) sul dominio comune.<nome>.<sigla>.it.
- Controllare sempre il giorno della settimana: ha fatto scartare pagine 2025 (Melting Christmas, Capodanno Pordenone) e trovato
  un refuso (Traviata Padova).

## Problemi
- Nessun conflitto sui file condivisi; ops/copertura.yaml modificato solo in `province` e nei nuovi `comuni_<SIGLA>`.
- Molti eventi della stagione teatrale hanno solo il periodo delle repliche (es. Teatro Verdi di Padova, opere della Fenice e
  del Verdi di Trieste): pubblicati come evento unico con inizio e fine e date delle recite nel riassunto.
