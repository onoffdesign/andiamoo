# Agente italia, notte del 2026-11-28 (fase 2b, Resto d'Italia, secondo giro)

Province di questo giro: TN, BZ, MI, BS, BG, MB, VA, CO, PV, MN. Il resoconto del giro precedente (Veneto e Friuli,
226 eventi) e' gia' unito dal coordinatore nel commit 44c5f50.

## Numeri
- Eventi in `config/notte/italia-eventi.yaml`: **275** (prima 2 eventi futuri in tutte le 40 localita' assegnate).
- `config/notte/italia-correzioni.yaml`: vuoto (nessun evento esistente da correggere in queste province).
- `python -m pipeline.notte --controlla italia`: "Parti valide". Nessun doppione con il sito (`--comune` su tutti i comuni).
- Ricerche usate: circa 115 su 125 (9 WebSearch, nessun WebFetch, il resto letture dirette con curl di pagine e API
  ufficiali, contate una per pagina o per chiamata).
- 141 eventi su 275 hanno lat/lon prese dalla fonte ufficiale (agende OpenCity, Open Data Hub, Teatro Sociale di Como).

| Prov. | Eventi | Comuni | Categorie principali |
|---|---|---|---|
| BZ | 80 | Bolzano 55, San Leonardo in Passiria 11, Laces 8, Valle Aurina 6 | teatro 21, musica 18, arte-cultura 12, famiglie 10, sagre-feste 9, mercatini 9, natura 1 |
| TN | 74 | Trento 61, Pergine Valsugana 12, Predaia 1 | teatro 21, musica 16, arte-cultura 13, famiglie 10, sagre-feste 8, mercatini 5, sport 1 |
| BG | 45 | Bergamo 45 | teatro 25, musica 16, arte-cultura 3, famiglie 1 |
| CO | 30 | Como 30 | musica 14, teatro 9, famiglie 4, arte-cultura 3 |
| MB | 16 | Monza 14, Usmate Velate 1, Agrate Brianza (Omate) 1 | teatro 14, arte-cultura 1, musica 1 |
| BS | 10 | Brescia 10 | musica 5, arte-cultura 5 |
| MI | 6 | Milano 1 (Otello alla Scala), Bresso 3, Ossona 2 | famiglie 3, musica 2, sagre-feste 1 |
| PV | 5 | Pavia 5 | arte-cultura 3, musica 1, famiglie 1 |
| MN | 5 | Mantova 5 | teatro 4, sagre-feste 1 |
| VA | 4 | Varese 4 | arte-cultura 3, sport 1 |

Per categoria (totale): teatro-spettacoli 94, musica 73, arte-cultura 43, famiglie-bambini 29, sagre-feste 19,
mercatini-fiere 14, sport 2, natura-outdoor 1.

Mercatini di Natale come eventi unici con start ed end: Trento (20/11-6/1, piazza Fiera e piazza Mostra), Bolzano
(26/11-6/1, piazza Walther), Mercatino solidale di Bolzano, Natale a Pergine (weekend 14/11-27/12), Paese dei presepi
di Lutago (Valle Aurina). Accensioni, sfilate di San Nicolo' e Krampus, concerti e presepi viventi sono a parte.

Comuni controllati senza eventi trovati: Male' (nessuna pagina 2026: El Nos Nadal e' ancora l'edizione 2025/26 su
visitvaldisole.it), Castelcovati, Verano Brianza, Venegono Superiore, Ostiglia ("in questo momento non sono previsti
eventi" sui siti Municipium). **Non controllati** (pagina `/it/events` assente o sito irraggiungibile, budget finito):
Vanzaghello, Angolo Terme, Marone, Gorlago, Averara, Parre, Uboldo, Orino, Bregnano, Cucciago, Cavargna, Badia Pavese,
Corana, Gambarana, Canneto sull'Oglio, Suzzara: restano senza data in copertura.

## Fonti nuove da catalogare (per ops/fonti.yaml; le strutturate anche per config/sources.yaml)
Strutturate (priorita' alta):
- **Comune di Trento, agenda** | https://www.comune.trento.it/Vivere-il-Comune/Eventi | API OpenCity:
  `https://www.comune.trento.it/api/opendata/v2/content/search/classes [event] and calendar[time_interval] = [da,a] limit 200`
  (258 eventi fino al 10/1, paginazione con `nextPageQuery`, da riaprire in https) | comune | TN. Scheda pubblica
  `/content/view/full/<mainNodeId>`; luogo con indirizzo e coordinate in `virtual_takes_place_in`. Molte attivita'
  ripetute del Villaggio di piazza Dante e delle biblioteche: scegliere.
- **Comuni trentini Comunweb (stessa API OpenCity)** | https://www.comune.pergine.tn.it , https://www.comune.predaia.tn.it |
  stessa query | comune | TN. Pergine 31 eventi, Predaia 6, Male' 0. Probabilmente vale per quasi tutti i 166 comuni
  del Trentino (`www.comune.<nome>.tn.it`): candidata a fonte del giro per provincia. Attenzione: `recurrences` a volte
  non coincide con il testo (stagione della Banda di Pergine: settimanale nell'API, 4 date nel testo): fidarsi del testo.
- **Comune di Bolzano, OpenAgenda (BzEvents)** | https://eventi.comune.bolzano.it/ | API OpenContent:
  `https://eventi.comune.bolzano.it/api/opendata/v2/content/search/classes [event] and calendar[] = [da,a] limit 200`
  (62 eventi fino al 10/1; `calendar[time_interval]` qui da' errore 500) | comune | BZ. Scheda pubblica
  `/agenda/event/<mainNodeId>` con JSON-LD; `geo` con coordinate. `from_time` del Teatro Stabile spesso a 20:00 fisso:
  l'orario vero e' in `orario_svolgimento`.
- **Open Data Hub Alto Adige (eventi LTS)** | https://tourism.api.opendatahub.com/v1/Event | API aperta:
  `?pagesize=3000&begindate=AAAA-MM-GG&enddate=AAAA-MM-GG&language=it&fields=...` (2269 eventi in 120 giorni in tutta la
  provincia, Bolzano 259, Merano 124) | ente regionale (NOI/IDM) | BZ. Comune in `LocationInfo.MunicipalityInfo.Name.it`,
  date e orari in `EventDate`, coordinate. Link pubblico costruito con l'Id LTS: Valle Aurina
  `https://www.ahrntal.com/it/vacanza-in-valle-aurina/manifestazioni/rid-<Id>-<slug>.html`, Val Passiria e Merano
  `https://www.merano-suedtirol.it/it/pianificare-le-vacanze/eventi/rid-<Id>-<slug>.html`, Val Venosta
  `https://www.venosta.net/it/informazioni-servizi/attualita/tutti-gli-eventi/rid-<Id>-<slug>.html` (canonical giusto,
  contenuto caricato in JavaScript). Testo italiano spesso vuoto: riassunti dal titolo. Molti "Guest Pass" per soli ospiti
  degli hotel: scartati.
- **Fondazione Teatro Donizetti (Bergamo)** | https://www.teatrodonizetti.it/spettacoli-teatro-donizetti/ | feed JSON:
  `https://www.teatrodonizetti.it/wp-json/teatrodonizetti/v1/calendar-feed?lang=it&start=AAAA-MM-GG&end=AAAA-MM-GG`
  (59 eventi fino al 31/1: Donizetti, Sociale, Sala Tremaglia, Santa Maria Maggiore) | sede | BG. Scheda
  `/evento/<slug>/<data>/`; senza `start`/`end` il feed risponde 502.
- **Teatro Sociale di Como** | https://teatrosocialecomo.it/ | **The Events Calendar**:
  `https://teatrosocialecomo.it/wp-json/tribe/events/v1/events?per_page=50&start_date=...&end_date=...` (45 eventi fino
  al 31/1, con costo, sala e coordinate) | sede | CO.

Non strutturate ma utili (una lettura, molti eventi):
- **Teatro Grande di Brescia, calendario** | https://teatrogrande.it/it/calendario | mese corrente e successivo con orari e
  sale | sede | BS.
- **Teatro Manzoni di Monza** | https://www.teatromanzonimonza.it/ | home con tutta la stagione 2026/27 (date, senza
  orari), schede `/stagione-teatrale-26-27/<slug>` | sede | MB.
- **Siti comunali Municipium** (`/it/events`, schede con "Date e orari", "Costo", "Luogo"): comune.mantova.it (molti
  eventi, elenco paginato), comune.bresso.mi.it, comune.ossona.mi.it, comune.ornago.mb.it, comune.castelcovati.bs.it,
  comune.veranobrianza.mb.it, comune.venegonosuperiore.va.it, comune.ostiglia.mn.it.
- **Comune di Pavia (Drupal)** | https://www.comune.pavia.it/vivere-comune/eventi?f%5B0%5D=quando%3Anext_thirty_days |
  elenco con date e orari, luogo spesso solo nella scheda, paginato (`&page=N`) | comune | PV.
- **Comune di Varese e Usmate Velate** (tema "vivere_il_comune/eventi/evento_N.html") | https://www.comune.varese.it/ |
  la home ha il calendario del giorno; schede con date, luogo e indirizzo | comune | VA, MB.
- **Visit Trento (APT)** | https://www.visittrento.it/en/festivals-and-major-events/the-trento-christmas-market |
  grandi eventi | ufficio turistico | TN.
- **Teatro alla Scala, documenti di stagione** | https://www.teatroallascala.org/static/upload/03-/03--stagione-d-opera-2026-2027.doc |
  date di tutte le recite (senza orari) | sede | MI. Le pagine HTML della Scala non sono state provate.
- **Turismo Mantova** | https://www.turismo.mantova.it/eventi | schede `/eventi/<id>/<slug>` | ufficio turistico | MN
  (non letto per budget).

Da verificare (visti solo nei risultati di ricerca, non aperti): mentelocale.it (Bergamo, Brescia, Mantova, Pavia),
iltaccodibacco.it, idealista.it, holafly.com, cosedicasa.com, dolomiti.it, songkick.com, milazzo.life, in-lombardia.it,
ilgiorno.it, quotidiano.net, ecodibergamo.it.

## Eventi visti ma non pubblicati
- Pavia, Teatro Fraschini: Un ballo in maschera (3 e 5/12) e Ensemble Symphony Orchestra (23/12) visti solo su
  mentelocale e songkick; il sito teatrofraschini.it ha l'elenco /programma/ senza date e le API non hanno risposto.
- Pavia: Lupin il musical (28/11 20:30) senza luogo nell'elenco del Comune.
- Bergamo: Bottega dell'economia carceraria e Teatro dell'oppresso (senza luogo nel feed) e gli incontri "Intorno a".
- Brescia: Barocco & other stories del 18/12 annullato dal teatro.
- Milano: le altre opere della Scala (Pecheurs de perles, Don Giovanni, Boheme) hanno le date nel documento ma
  l'abbinamento data-titolo non era sicuro nel testo estratto; Otello pubblicato come evento unico 4/12-5/1 con le recite.
- Bresso: Siepe di Natale del 5, 12 e 19/12 e Il giro del mondo in 80 giorni (6/1) non aperti per budget.
- Varese: decine di eventi nel calendario della home (Book City, premi letterari, conferenze) non aperti per budget.

## Lezioni per ops/metodo-ricerca.md
- **Trentino**: i siti comunali Comunweb (`www.comune.<nome>.tn.it`) rispondono all'API OpenCity: una chiamata per
  comune da' tutti gli eventi con date e luoghi. Il capoluogo ha 258 eventi in 6 settimane.
- **Alto Adige**: l'Open Data Hub e' la fonte unica per tutta la provincia (eventi LTS di tutte le associazioni turistiche);
  il link pubblico si costruisce con l'Id LTS sui siti delle associazioni (`rid-<Id>-<slug>.html`). suedtirol.info con
  l'Id da' 404.
- **Lombardia**: i capoluoghi non hanno API comuni (Milano, Brescia, Monza rispondono 403 all'API OpenCity); i teatri
  principali hanno calendari strutturati (Donizetti feed JSON, Sociale di Como tribe) e valgono piu' del sito del Comune.
  Molti comuni piccoli usano Municipium (`/it/events`); quando l'indirizzo `www.comune.<nome>.<sigla>.it/it/events` da'
  404 o non esiste, il comune usa un altro fornitore e serve una ricerca.
- Le pagine `/it/events` di Municipium mostrano titolo e data ma non ora e luogo: per gli eventi servono le schede (una
  lettura per evento). Conviene scegliere quelli con piu' pubblico.
- Agrate Brianza: la rassegna TeatrOrnago e' ospitata a Omate (frazione di Agrate) fino al 2027: comune giusto nel town.

## Problemi
- Nessun conflitto sui file condivisi; `ops/copertura.yaml` modificato solo in `province` (10 sigle nuove) e nelle nuove
  sezioni `comuni_TN`, `comuni_BZ`, `comuni_MI`, `comuni_BS`, `comuni_BG`, `comuni_MB`, `comuni_VA`, `comuni_CO`,
  `comuni_PV`, `comuni_MN` (solo i comuni davvero controllati).
- Stagioni con solo il periodo (Teatro Manzoni di Monza, Otello alla Scala): eventi unici con inizio e fine, senza orario.
- Gli eventi delle valli altoatesine hanno come `official_url` le schede delle associazioni turistiche, che caricano il
  testo in JavaScript: il titolo e la data sono nell'Open Data Hub (`fonte`).
- Milano, Pavia, Varese e Mantova restano poco coperte: alla prossima rotazione partire dalle fonti sopra (Municipium di
  Mantova paginato, elenco 30 giorni di Pavia, schede di Varese) e cercare i calendari di Piccolo Teatro e Scala.
