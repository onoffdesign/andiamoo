# Agente giro, notte del 2026-11-28 (quarto giro)

(Riscritto da capo. Questo giro ha letto per la prima volta le 7 fonti del giro "mai" lette, tutte fuori dal Veneto
tranne running.life e gotrail, poi ha riaperto alcune fonti note di ops/fonti.yaml.)

## Numeri
- Eventi aggiunti in config/notte/giro-eventi.yaml: 150 (61 nei prossimi 30 giorni). `python -m pipeline.notte --controlla giro`: parti valide.
  - Teatro Bellini (Napoli): 50 (Sala Grande, Piccolo Bellini e Bellini Kids fino al 31/3). Il sito non da' gli orari: le
    teniture sono un evento con inizio e fine; con orario solo Misurare il salto delle rane (28 e 29/11) e Neanche Parenti (28, 29/11 e 1/12).
  - Marche Teatro, Teatro delle Muse (Ancona): 39 repliche di prosa, danza e fuori abbonamento fino al 18/3, divise per data con
    l'orario generale della pagina (20:30, domenica 16:30). Fuori abbonamento senza orario confermato (Il lago dei cigni 27/12,
    A Christmas Carol 29/12, La vie en rose 19/1, Angelo Duro 18/3) messi solo con la data. Le false confidenze: due pagine
    dicono 27-31/1 e 28-31/1, messe solo le date comuni 28-31. Bancal: la pagina della stagione dice 26-27/2, un'altra 27-28/2:
    messo solo il 27/2 alle 20:30.
  - VisitLazio: 21 (Christmas Market Villa Grazioli a Grottaferrata 28-29/11, mostra Arcadia a Villa d'Este a Tivoli fino al 4/4,
    Corri per il Verde 13/12 al Parco di Centocelle, Concerti dell'Avvento in Cattedrale a Latina 29/11, 8 e 18/12, Festa
    dell'Olio Nuovo a Cerveteri 5-6/12, Sagra del Tozzetto a Vetralla 5-6/12, Paese di Babbo Natale a Collalto Sabino 5 date,
    musical Io Francesco a Sezze 29/11, Tomba di Cicerone a Formia 29/11, 7 e 13/12, mostra mercato del presepio a Greccio fino al 6/1).
  - Teatro Cilea (Napoli): 14 (7 repliche con orario di Biagio Izzo dal 25/12 al 3/1, le altre teniture con inizio e fine).
  - Teatro Massimo Bellini (Catania): 7 (Recital House of Puccini 28/11, La bella addormentata, Le nozze dell'Orso e Il quinto
    moschettiere al Sangiorgi, Capodanno 1/1 ore 19, Carmen dal 14/2, Nabucco dal 6/3).
  - Fonti note riaperte (Treviso): 15 (Teatro Del Monaco: Malinconico 11-14/3, L'ultima domenica di agosto 18-21/3, 7 contro Tebe
    9/3, Stand Up La luce del Natale 6/1; Treviso Basket con Cantu' 14/3 e Roma 21/3; Imoco con Bergamo 7/2; Benetton con Ulster
    27/3; Treviso FBC con Juventus Next Gen 21/3).
  - running.life: 4 (Corsa dei Babbi Natale a Ponzano 29/11, Run 4 Hope a Vazzola 28/2, Pieve in Rosa 7/3, Marcia dei Castelli
    a Susegana 14/3; nessuna ha l'orario).
- Correzioni in config/notte/giro-correzioni.yaml: 10, tutte sugli eventi di Trevignano Cultura presi da trevisoeventi.com.
  - c154ab989bd88661 (31/1 ore 17:30) era "4 Elementi: Quartetto Aires" a Falze': la scheda ufficiale dice che quel giorno c'e'
    "Il tango incontra il jazz: da Piazzolla a Gershwin" della Blue Note Small Orchestra al Teatro Comunale (il Quartetto Aires
    e' il 17/1 a Villa Onigo, gia' sul sito). Corretti titolo, riassunto, luogo, prezzo.
  - Le altre 9: official_url dalla pagina dell'aggregatore alla scheda ufficiale di trevignanocultura.it, piu' prezzi e accessi
    (Gardizero 15 euro, Capodanno 20 euro e Teatro Comunale invece di "Falze'", Vernia 20 euro, Concerto di Natale in chiesa a
    Musano ingresso libero, Quartetto Aires ingresso libero, Boeing Boeing 8 euro).
- Fonti del giro lette: le 7 "mai" (teatro-bellini-napoli, running-life, teatro-cilea, visit-lazio, marche-teatro, gotrail,
  teatro-massimo-bellini), date in ops/copertura.yaml sezione giro. Fra le trevigiane gia' lette oggi ho riaperto solo
  nautilus-teatro (11 eventi, tutti gia' sul sito), dolomiti-prealpi (prima pagina dell'API: i titoli controllati sono gia'
  sul sito), visit-fregona (API vuota, nessun evento futuro) e comune-castelfranco (solo Bianco Natale 5/12, gia' sul sito):
  sono sature, non ho speso altro su di loro.
- Fonti note riaperte (da aggiornare in ops/fonti.yaml, ultimo_controllo 2026-11-28):
  Treviso Basket resa 2, Benetton Rugby resa 1, Imoco Volley resa 1, Treviso FBC resa 1, Teatro Stabile del Veneto Del Monaco
  resa 10, Trevignano Cultura resa 0 nuovi ma 10 correzioni, Biblioteca Zero Branco resa 0 (Nel cuore dei bambini gia' sul sito),
  Collalto di Susegana resa 0 (gia' tutto sul sito, controllato con --comune senza aprirla), parkrun Treviso resa 0 (sabati fino
  al 26/12 gia' sul sito, senza aprirla).
- Ricerche usate: 78 su 100 (6 WebSearch, 72 WebFetch, di cui 22 a Nominatim per le coordinate).

## Da fare per il coordinatore
- config/sources.yaml: teatro-cilea non e' il Teatro Francesco Cilea di Reggio Calabria ma il Teatro Cilea di Napoli
  (teatrocilea.it, Via San Domenico 11, Vomero): corretti nome e nota. Il collettore tribe_api non ha un comune di default:
  se il PC tornasse attivo, gli eventi uscirebbero senza comune.
- Possibili doppioni con gli agenti italia-a e italia-b se stanotte hanno coperto Napoli, Ancona, Catania o il Lazio:
  prima di unire, guardare `--comune Napoli`, `Ancona`, `Catania`.
- Gaber. Mi fa male il mondo (Neri Marcore') e' sia ad Ancona (28-29/11) sia a Napoli (1-6/12): sono due tournee diverse, non doppioni.
- Benetton - Ulster 27/3 e Treviso - Juventus Next Gen 21/3 non hanno address (come le altre partite gia' sul sito a Monigo e al Tenni):
  le coordinate sono quelle di config/luoghi.yaml e degli eventi gia' pubblicati.
- Corsa dea Befana a Spresiano (6/1, running.life: ritrovo sede Noi SS. Trinita' / G.M. Piave Lovadina, Via Nazionale 2) non
  aggiunta: Via Nazionale a Spresiano ha tre tratti in OSM e il punto non e' certo, e manca l'orario. Santa Klaus Run 20/12
  e' gia' sul sito.
- Ridges Trail Vittorio Veneto 14/2 (gotrail): la scheda ha dati del 2023, non aggiunta.

## Luoghi nuovi (nome | comune | indirizzo | lat, lon | fonti)
Coordinate di OpenStreetMap (Nominatim letto con WebFetch), indirizzi dalle pagine ufficiali.
- Teatro Cilea | Napoli | Via San Domenico 11 | 40.8399872, 14.2161263 | teatrocilea.it + OSM node 13810369389 | 14 eventi
- Teatro Bellini, Piccolo Bellini (stesso edificio) | Napoli | Via Conte di Ruvo | 40.8509562, 14.2508856 | teatrobellini.it + OSM way 270951006 (civico non letto sul sito) | 50 eventi
- Teatro delle Muse | Ancona | Piazza della Repubblica | 43.6195966, 13.5101245 | marcheteatro.it + OSM way 179360424 | 39 eventi
- Teatro Metropolitan | Catania | Via Sant'Euplio 21 | 37.5098986, 15.0843868 | teatromassimobellini.it + OSM way 47042710 | 4 eventi
- Teatro Sangiorgi | Catania | Via Sangiuliano 233 | 37.5046424, 15.0885455 | teatromassimobellini.it + OSM relation 1861511 | 2 eventi
- Teatro Massimo Bellini | Catania | Via Giuseppe Perrotta 12 | 37.504157, 15.0898267 | teatromassimobellini.it + OSM way 28399127 | 1 evento
- Park Hotel Villa Grazioli, Villa Grazioli | Grottaferrata | Piazza Eugenio Conti 1 | 41.7992866, 12.6770008 | visitlazio.com + OSM way 171942401 | 2 eventi
- Villa d'Este | Tivoli | Piazza Trento 5 | 41.9624053, 12.7967683 | visitlazio.com + OSM node 5955386790 (biglietteria) | 1 evento
- Parco di Centocelle | Roma | Via Casilina | 41.8747578, 12.5681044 | visitlazio.com + OSM way 314953429 | 1 evento
- Cattedrale di San Marco | Latina | Via Sisto V (VisitLazio scrive Piazza del Popolo 1) | 41.4644049, 12.902675 | OSM way 180004045 | 3 eventi
- Piazza Santa Maria | Cerveteri | Piazza Santa Maria | 41.9988621, 12.0995418 | visitlazio.com + OSM way 1493358722 | 2 eventi
- Via Cassia 157 | Vetralla | Via Cassia 157 | 42.32092, 12.05366 | visitlazio.com + OSM node 2311460096 (civico 157 di Via Cassia Interna) | 2 eventi
- Tomba di Cicerone | Formia | Via Appia km 139 | 41.2515672, 13.5786977 | visitlazio.com + OSM way 159656918 | 3 eventi
- Piazza Vittorio Emanuele II | Pieve di Soligo | Piazza Vittorio Emanuele II | 45.8996349, 12.1725943 | running.life + OSM way 132221062 | 1 evento
Punti approssimati (da non mettere in luoghi.yaml senza una verifica): Collalto Sabino Piazza Marconi 1 e Sezze Cattedrale di
Santa Maria (Via Armando Diaz 1) al centro del comune di config/comuni.csv (Nominatim non trova piazza e cattedrale); Greccio
al centro del comune (VisitLazio scrive Via Limiti Nord 17 a Limiti di Greccio ma parla del borgo medievale); Vazzola sede
Pro Loco (Piazzetta Donatori di Sangue 1) al centro del comune; Susegana Via XXIV Maggio 1 sul tratto di via del capoluogo
(OSM way 75522501); Ponzano Stadio comunale di Paderno, Via de Bellato 2: in OSM Via del Bellato e' a Merlengo (way 389571342), punto sulla via.

## Fonti nuove da catalogare (per l'agente fonti)
- Il Paese di Babbo Natale (Collalto Sabino) | https://www.ilpaesedibabbonatale.info/ | query "Il Paese di Babbo Natale Collalto Sabino" | organizzatore (sito ufficiale dell'evento, non aperto)
- Corri in Rosa | https://corrinrosa.run/pieve-di-soligo/ | query "Pieve in Rosa corrinrosa" | sport, organizzatore (non aperto)
- Associazione Corale San Marco (Latina) | https://www.coralesanmarco.it | query "Concerti dell'Avvento Latina Corale San Marco" | associazione (non aperta)

## Lezioni
- Nominatim si apre con WebFetch anche senza ricerca (https://nominatim.openstreetmap.org/search?q=...&format=json): una
  chiamata per luogo, buono per teatri e piazze con nome; per le vie lunghe da' piu' tratti e serve il civico.
- Le pagine "sala" dei teatri (teatrobellini.it/sala-grande/, /spettacoli/piccolo-bellini/, /spettacoli-bellini-kids/) danno
  tutta la stagione con date e link in una lettura; la home del Bellini e' troncata. Gli orari sono solo nelle schede.
- VisitLazio: l'elenco e' troncato a una settimana; ogni scheda costa una lettura ma ha indirizzo, orari e link ufficiale.
  Rende per le province del Lazio, finora vuote sul sito.
- Le fonti trevigiane del giro lette tre volte oggi sono sature: un quarto giro non trova niente di nuovo.
- running.life: il testo dell'elenco contiene una richiesta rivolta ai modelli (ignorata); le schede hanno ritrovo e distanze
  ma quasi mai l'orario.

## Problemi
- Nessuna approvazione richiesta. Il curl dalla shell e' stato negato dal sistema di permessi: tutto letto con WebFetch.
