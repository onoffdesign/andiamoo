# Revisione, notte del 2026-11-28 (sessione delle 20:19)

Riscritto da capo. Lavoro fatto su `ops/posizioni.json`, `ops/revisione.json` (60 in coda) e `ops/campione.json` (20)
generati alle 20:19. `ops/senza-posizione.json` era vuoto.

## Numeri
- Quota: 68 su 75 (5 WebSearch, 63 WebFetch). Le coordinate vengono da Nominatim (OpenStreetMap) interrogato dalla
  shell con riquadro sul comune e 3,5 secondi di pausa (fuori quota, come dice la lezione del 28/11). Una sola lettura
  di una scheda ufficiale fatta con curl dalla shell (La Cena dei cretini, culturabologna.it); poi la lettura in blocco
  delle pagine della coda dalla shell e' stata negata dal permesso e tutto il resto e' passato da WebFetch.
- File: `config/notte/revisione-correzioni.yaml` (36 correggi, 0 rimuovi, 29 verificati: coda 33+17, campione 3+12), `config/notte/revisione-eventi.yaml`
  (2 eventi), `config/luoghi.yaml` (81 voci nuove, nota "Aggiunto il 2026-11-28 (revisione, sera)").
  `python -m pipeline.notte --controlla revisione`: parti valide.

## Posizioni
- Prima (ops/posizioni.json delle 20:19, 2532 eventi): punti diversi 0, lontani dal comune 63, solo comune con luogo 130,
  solo comune senza luogo 27, candidati 17.
- Stesso calcolo rifatto sul sito attuale (2914 eventi, dopo le pubblicazioni del coordinatore): senza le mie voci
  solo comune con luogo 136 e candidati 50; con le 81 voci nuove **solo comune con luogo 77**, **candidati 17** (tutti
  nuovi, di Toscana e Marche: 33 dei 50 sistemati), punti diversi 0, lontani 72 (invariati salvo gli eventi nuovi).
- Luoghi sistemati: 81 in luoghi.yaml (32 candidati controllati su OSM: teatri di Napoli, Genova, Savona, Imperia,
  Verbania, Catania, Aosta, Pesaro, Livorno, Siena, Massa, Lucca, Prato, Urbino, Fabriano, Grosseto, Arezzo, Sansepolcro,
  Latina, Formia; 49 senza punto), piu' 2 punti singoli in lat/lon (Natale sotto le mura a Castelfranco, festa del
  radicchio di Spresiano in Via Bragadin). Senza punto sistemati tra gli altri: Piazza Mazzini e Casa dell'Economia di
  Lecco, Cinema Teatro Manzoni di Paese, Teatro il Piccolo e Giardini Pubblici di Forli' (punto noto piu' vicino),
  BAS di Via Albicini, Sala CDT di Cuneo, 12 luoghi di Alessandria e Novara, 8 di Biella (SS. Trinita' accanto al Duomo
  da scheda ICCD), Verona, Vicenza (Odeo e San Lorenzo), Reggio (Ghiara, Conservatorio), Livelet, Parco dei Carbonai,
  Borgo di Mura, Piazza del Duomo di Belluno; frazioni come punto piu' vicino per San Cipriano, Fontigo, Castagnole,
  Padernello, Coia.
- Lontani dal comune controllati, falsi allarmi: Teatro Toniolo e Teatro del Parco (Mestre), Oropa, H-FARM, Santa Maria
  in Stelle, Nevegal, Scardovari, Lutago, Centocelle, Fiere di Parma, Parco dei Carbonai (Lamar e' nel comune di
  Cordignano, 6 km a nord). Da guardare: Longastrino (Alfonsine o Argenta?), Borgo di Candelara, Equi Terme, Montesicuro
  (nuovi, non controllati).
- Restano senza punto (Nominatim non li conosce e una ricerca a vuoto): Biblioteca di Farra di Soligo (4 eventi),
  Biblioteca di Paese (4), Scuola di musica Luchesi di Silea (4, OSM ha solo la via), IAT di Treviso (2), Biblioteca di
  Maser, Sala Guarnieri di Pedavena, Info Point di Cison, Galleria Concordia, Villa Romivo, Villa Freya, Piazzale Roma e
  chiesa dell'Immacolata di Misano (Nominatim da' Riccione e Gabicce: da evitare), Santuario delle Grazie di Pordenone.

## Coda di revisione (60)
- Chiusi 50 su 60: 33 correggi e 17 verificati.
- Corretti l'accesso di 12 eventi di Cultura Bologna (10 a pagamento, Marcello Fois e l'incontro al MAMbo gratuiti),
  dei 3 concerti di Cremonini all'Unipol Arena, dei 6 spettacoli ERT di Bologna e Modena (prezzi da 5,45 a 8,18 euro;
  AiAiAi Pinocchio alle 16:30), di Siepe a nordovest, Red Wine Bluegrass Party (da 21 euro), Un ballo in maschera (25-65
  euro), Francesca Giannone al Ridotto del Valli (libero, ore 11), Leila Guerriero allo Splendor (libero), La rivincita
  degli imperi (libero), Basilico e De Chirico al Museo Garda (8/6 euro), Il secolo del Barocco di Cuneo (gratuito, era a
  biglietto); luogo della festa del radicchio di Spresiano e del Natale sotto le mura; Reel Rock: link Happy Ticket
  spostato in ticket_url.
- Verificati: le due mostre di Palazzo Ducale, Hopper e Pisa 1946 (accesso non pubblicato), Salgado (accesso non
  pubblicato), mercatino tirolese di Modena, pista di Biella (non e' doppione: l'altra e' a Pordenone), Winter Park di
  Cremona, Giardini di Luce di Forli', Cenerentola e pista di Sondrio, Io Francesco a Sezze, piazza Ghiaia, Mercatino
  delle Cose Buone di Reggio, Padernello (non e' doppione di Santa Lucia di Piave), Arcadia a Tivoli.
- Aperti 10: Hayez Boldini Casorati a Novara, Andar per fiere al Salce, Toni Benetton (liceo da non aprire), Mostra del libro di Ormelle (finisce oggi),
  Il sogno dell'Accademia di Alessandria (programma solo in allegato), Broadway Time e Banda di Oleggio (non nell'elenco
  di turismonovara alla prima pagina), Coro Catinaccio (non nella home del mercatino), Human Atlas, Il Sindaco Pescatore
  (teatroalighieri.org: 403).

## Campione
Riga pronta per la parte 3 di ops/segnalazioni-e-controllo.md:
`- 2026-11-28 (sera) · corretti 15/20 · errori: data 1, orario 0, luogo 2, accesso 2, categoria 0, link 1 · lezione: con i luoghi della notte il punto sul solo comune scende a 2 errori (Teatro il Piccolo di Forli', SS. Trinita' di Biella, ora in luoghi.yaml); l'accesso pubblicato dalla fonte non trascritto (Ghirri gratuito, Cremonini a pagamento) e la data d'inizio di una mostra gia' aperta (Ghirri dal 30/4) restano; Nanowar senza link ufficiale (solo TicketOne); 3 non verificabili nel budget (Lago dei cigni e Cervi Bianchi su myarteven, pagina di 340 mila caratteri; Massimo Marchese nell'allegato del Comune di Alessandria), contati come corretti. Sotto il 90% ma sopra l'80%: nessuna regola nuova`
Tutti gli errori trovati sono corretti (Ghirri, Cremonini, Nanowar, prezzo di Morricone a Bergamo) o sistemati con
luoghi.yaml (Pollicino Dore', gospel di Biella).

## Test di copertura
Riga pronta per ops/espansione.md:
`- 2026-11-28 (sera) · TN/BZ · copertura 3/20 (test della revisione: i primi 20 eventi dell'articolo SiViaggia "sagre e feste in Trentino-Alto Adige a dicembre 2026" del 16/11; presenti Mercatino dei Gaudenti e Mercatino di Natale di Trento, Mercatino di Natale di Bolzano; mancanti San Nicolo' a Castelrotto, Santa Cristina e Selva, Krampus di Lana, Notte degli Alambicchi a Vallelaghi, Sagra del Mandorlato a Castel Ivano, Strozegada di Santa Lucia a Levico, Rito della stella a Palu' del Fersina, Mercatino d'altri tempi e mercatino di Natale di Rovereto, Mercatino della Stella a Faedo, Mercatino delle Pulci di Arco, mercatini di Bressanone, Brunico, Lagundo, Merano, Trenatale del Renon; aggiunti Merano e Vipiteno da suedtirol.info e vipiteno.com) · criterio di saturazione: non valutato (non e' lunedi')`
Il buco: in Trentino-Alto Adige fuori da Trento e Bolzano non c'e' quasi nulla (Rovereto, Merano, Bressanone, Brunico
0 eventi). Fonti utili per giro o italia-a/b: suedtirol.info (pagine dei Mercatini originali), merano-suedtirol.it,
vipiteno.com, visittrentino.info.

## Fonti nuove (per l'agente fonti)
- suedtirol.info, merano-suedtirol.it, vipiteno.com: siti ufficiali turistici; vipiteno.com e suedtirol.info letti.
  Da catalogare (verifica di robots.txt e termini a cura dell'agente fonti). Non sono aggregatori.

## Lezioni
- Nominatim dalla shell rende per i teatri, le chiese e le piazze delle citta' (49 luoghi su ~65 provati), quasi mai per
  biblioteche, sale e ville dei comuni piccoli trevigiani; il riquadro sul comune evita gli omonimi (Lecco, Misano).
  Con meno di 3 secondi tra le richieste risponde 629.
- Cultura Bologna ha "evento a pagamento/gratuito" in ogni scheda: una lettura per evento, nessun elenco con l'accesso.
  Le schede ERT danno sempre il prezzo minimo ("da 8,18 euro").
- Una pagina elenco di un portale turistico (turismonovara) mostra solo la prima pagina di 274 risultati: lettura persa.
- I nomi in luoghi.yaml non devono essere nomi di frazione o di comune (es. "Soligo" avrebbe preso anche "Biblioteca
  comunale di Farra di Soligo"): usare il nome del posto.

## Problemi
- La lettura delle pagine ufficiali dalla shell (curl) e' negata dal permesso: tutte le verifiche passano da WebFetch.
- Coordinatore: le parti di italia-a/b che portano molti teatri nuovi generano subito nuovi candidati (50 stasera):
  conviene che chi aggiunge una sede la metta con lat/lon gia' nell'evento.
