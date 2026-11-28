# Agente fonti, notte del 2026-11-28 (terzo giro di verifiche)

## Numeri
- Fonti verificate: 12. Ammesse 8, vietate 1, restano da verificare 3.
- Fonti nuove valutate: 46 (39 catalogate come utilizzabili, 5 vietate per robots.txt, 2 da verificare), tutte in
  ops/fonti.yaml; in config/fonti-vietate.yaml 5 vietate nuove, 1 ammessa nuova (zero.eu), 3 da verificare nuove
  (sardegnaeventi24.it, solosagre.it, sagritaly.com).
- Eventi aggiunti: 0 (config/notte/fonti-eventi.yaml non creato). Correzioni: 0.
- Ricerche usate: 19 su 75 (14 WebSearch, 5 WebFetch). In piu', letture con curl/httpx (user agent dichiarato
  AndiamooBot del progetto, nessun proxy terzo): robots.txt e pagine legali delle fonti da verificare, e una sonda sui
  siti ufficiali (robots.txt, home, API tribe e /wp-json/wp/v2/types), circa 250 richieste.
- `python -m pipeline.notte --controlla fonti`: Parti valide. config/fonti-vietate.yaml: YAML valido.

## Verifiche delle fonti (config/fonti-vietate.yaml)
- **tviweb.it -> ammesse** (3 trattenuti): robots.txt blocca solo wp-admin; /privacy-note-legali-cookies/ letta:
  nessun divieto di raccolta automatica, solo "Nessuna parte del sito ... puo' essere riprodotta o ritrasmessa senza
  specifica autorizzazione scritta" (niente testi copiati).
- **insolitotrantran.it -> ammesse** (8): robots.txt "tutti i motori di ricerca e gli assistenti AI sono i benvenuti"
  (ClaudeBot e Claude-User con Allow /); /privacy/ letta, termini non esistono (nel footer solo Privacy e cookie).
- **running.life -> ammesse** (3) e **gotrail.run -> ammesse** (1): robots.txt blocca solo /<lingua>/map/ e /demo-;
  /privacy-policy (WebFetch, comune a running.life, gotrail.run, walking.life) non parla di scraping e non cita termini
  d'uso; /termini, /terms-of-use e simili danno 404.
- **mentelocale.it -> ammesse** (1): robots.txt Allow /; /informativa-privacy.htm letta, nessun divieto; termini e
  note legali non esistono (404 e ricerca).
- **siviaggia.it -> ammesse** (1): robots.txt blocca solo /cerca/, /search/, /ai/, wp-admin; Note legali di Italiaonline
  (privacy.italiaonline.it/note_legali.html) lette: solo tutela del diritto d'autore, nessun divieto di raccolta
  automatica.
- **trevisando.it -> ammesse** (2): con curl arriva una pagina anti-bot, con WebFetch robots.txt (Yoast, Disallow
  vuoto) e /privacy-policy/ si leggono: nessun divieto, termini d'uso non presenti.
- **eventivenetando.it -> ammesse** (1): e' il sito del Consorzio Pro Loco del Quartier del Piave (rete pro loco,
  categoria ammessa); robots.txt (WebFetch) blocca solo /system, /cgi-bin, /anteprima, /Facebook. Privacy non letta
  (curl riceve la pagina anti-bot): leggere solo con WebFetch.
- **eventiesagre.it -> vietate** (2): i Termini e Condizioni sono su iubenda (iubenda.com/termini-e-condizioni/316839,
  Web Up Italia Srl), sezione "Diritti sui contenuti": "e' fatto divieto agli Utenti di copiare, scaricare,
  condividere ... trasformare ... o creare opere derivate a partire dal contenuto disponibile su questa Applicazione".
  robots.txt non blocca, ma i termini vietano lo scaricamento dei contenuti: nel dubbio vietata. I 2 eventi trattenuti
  vanno cercati su fonti ufficiali.
- **Restano da verificare**:
  - ticketone.it (15): robots.txt di nuovo 503 con WebFetch ed errore di connessione con curl; termini irraggiungibili.
  - classicalive.it (9): robots.txt Allow /; l'informativa privacy linkata nel footer non si trova (provati
    /it/privacy-policy/, /it/cookie-policy/, /it/note-legali/, /it/termini/ e varianti: 404; due ricerche, anche su
    iubenda, a vuoto). Serve l'indirizzo esatto dal footer (lettura manuale) o un contatto con l'associazione (Lecco).
  - 2night.it: robots.txt vieta per tutti proprio /o/disclaimer.html e /o/privacy.html (le pagine legali), oltre a
    /api/; le pagine eventi non sono bloccate. Le pagine dei termini non si possono leggere senza violare robots.txt:
    serve una lettura manuale di Federico.

## Fonti nuove catalogate (ops/fonti.yaml)
Tutte siti ufficiali (enti turistici, teatri, musei, festival, comuni, federazioni) con robots.txt letto, salvo zero.eu
(aggregatore, verificato con termini). Nome | url | query | tipo.
1. VisitLazio (Regione Lazio) | https://www.visitlazio.com/eventi-lazio/ | visitlazio eventi lazio <comune> | ufficio turistico
2. VisitSicily (Regione Siciliana) | https://www.visitsicily.info/eventi/ | visitsicily evento <comune> | ufficio turistico
3. Teatro Massimo Bellini Catania | https://www.teatromassimobellini.it/calendario/ | Teatro Massimo Bellini Catania calendario | teatro
4. Teatro Cilea Reggio Calabria | https://teatrocilea.it/calendario-eventi/ | Teatro Cilea Reggio Calabria stagione | teatro
5. Marche Teatro Ancona | https://www.marcheteatro.it/events/ | Marche Teatro Ancona stagione | teatro
6. Teatro Bellini Napoli | https://www.teatrobellini.it/ | Teatro Bellini Napoli stagione spettacolo | teatro
7. Teatro Lirico di Cagliari | https://www.liricocagliari.it/stagione-2027/ | Teatro Lirico Cagliari evento | teatro
8. Fondazione Ravello | https://www.fondazioneravello.com/eventi/ | Fondazione Ravello eventi | associazione
9. CeDAC Sardegna | https://www.cedacsardegna.it/programmazione/ | CeDAC Sardegna programmazione <comune> | teatro
10. ERT FVG | https://ertfvg.it/calendario/ | ERT FVG calendario <comune> | teatro
11. Teatro Stabile dell'Umbria | https://teatrostabile.umbria.it/calendario/ | Teatro Stabile Umbria calendario | teatro
12. ATCL Lazio | https://atcllazio.it/stagione-teatrale-2026-2027/ | ATCL Lazio stagione teatrale <comune> | teatro
13. Teatro Fenaroli Lanciano | https://www.teatrofenaroli.it/cartellone/ | Teatro Fenaroli Lanciano cartellone | teatro
14. Teatro dei Sassi Matera (debole: schede ferme al 2024) | https://www.teatrodeisassi.it/eventi/ | Teatro dei Sassi Matera eventi | teatro
15. Teatro Regio di Parma | https://teatroregioparma.it/calendario/ | Teatro Regio Parma calendario | teatro
16. Teatro Regio di Torino | https://www.teatroregio.torino.it/calendario | Teatro Regio Torino calendario | teatro
17. Maggio Musicale Fiorentino | https://www.maggiofiorentino.com/calendario | Maggio Musicale Fiorentino calendario | teatro
18. Teatro Stabile di Torino | https://www.teatrostabiletorino.it/ | Teatro Stabile Torino cartellone | teatro
19. Teatro Franco Parenti Milano | https://teatrofrancoparenti.it/calendario-spettacoli/ | Teatro Franco Parenti calendario spettacoli | teatro
20. Teatro di Roma | https://www.teatrodiroma.net/calendario/ | Teatro di Roma calendario | teatro
21. Accademia di Santa Cecilia | https://santacecilia.it/concerti/calendario-concerti/ | Santa Cecilia calendario concerti | associazione
22. Romaeuropa | https://romaeuropa.net/agenda/ | Romaeuropa agenda | festival
23. Palazzo Strozzi | https://www.palazzostrozzi.org/calendario/ | Palazzo Strozzi calendario | museo
24. Triennale Milano | https://www.triennale.org/eventi | Triennale Milano eventi | museo
25. Comune di Ancona | https://www.comune.ancona.it/it/eventi | Comune di Ancona eventi | comune
26. Comune di Catanzaro | https://www.comune.catanzaro.it/vivere-il-comune/eventi/ | Comune di Catanzaro eventi | comune
27. Comune di Siracusa | https://www.comune.siracusa.it/vivere-il-comune/eventi | Comune di Siracusa eventi | comune
28. Comune di Brindisi | https://www.comune.brindisi.it/vivere-il-comune/eventi | Comune di Brindisi eventi | comune
29. Comune di Cosenza | https://www.comune.cosenza.it/it/eventi/ | Comune di Cosenza eventi | comune
30. Bologna Welcome | https://www.bolognawelcome.com/it/eventi | Bologna Welcome eventi | ufficio turistico
31. Destination Florence (feelflorence.it) | https://www.destinationflorence.com/it/eventi | Feel Florence eventi Firenze | ufficio turistico
32. in-Lombardia (Regione Lombardia) | https://www.in-lombardia.it/eventi | in-lombardia eventi <provincia> | ufficio turistico
33. Emilia-Romagna Turismo | https://emiliaromagnaturismo.it/it/eventi | emiliaromagnaturismo eventi <comune> | ufficio turistico
34. FIDAL, calendario gare | https://www.fidal.it/calendario.php?&anno=2026&mese=12 | calendario FIDAL <mese> <regione> | sport
35. Umbria Jazz | https://www.umbriajazz.it/programma/ | Umbria Jazz Winter Orvieto programma | festival
36. Teatro Alighieri Ravenna | https://www.teatroalighieri.org/lists/stagione-dei-teatri/ | Teatro Alighieri Ravenna stagione | teatro
37. Comune di Pescara | https://www.comune.pescara.it/argomento/eventi/ | Comune di Pescara eventi | comune
38. Zero (aggregatore ammesso) | https://zero.eu/it/ | zero.eu eventi <citta'> <data> | aggregatore
39. Teatro Goldoni Livorno | https://www.goldoniteatro.it/spettacoli/?ts=eventi | Teatro Goldoni Livorno spettacoli | teatro

Vietate per robots.txt (ClaudeBot o Claude-User con Disallow /), in vietate e nel catalogo con stato ferma:
teatromassimo.it (Palermo), sardegnaturismo.it, lovevda.it (Valle d'Aosta), lamialiguria.it, tcbo.it (Teatro Comunale
di Bologna). Per Sardegna, Valle d'Aosta e Liguria il portale regionale non si puo' usare: servono comuni e pro loco.
Da verificare: sardegnaeventi24.it, solosagre.it (termini non trovati), sagritaly.com (era gia' nel catalogo e veniva
usata: ora e' da verificare, privacy e termini non trovati).

## Proposte per le fonti del giro (config/sources.yaml, le aggiunge il coordinatore)
Con dati strutturati (provati stanotte):
- VisitLazio | https://www.visitlazio.com/eventi-lazio/ | Lazio (RM, VT, RI, LT, FR) | jsonld (93 eventi futuri nella
  pagina, con indirizzo completo in location.address)
- Teatro Massimo Bellini | https://www.teatromassimobellini.it/calendario/ | Catania | jsonld (7 date future)
- Teatro Bellini | https://www.teatrobellini.it/ | Napoli | jsonld (17 eventi futuri in home)
- Teatro Cilea | https://teatrocilea.it | Reggio Calabria | tribe_api (11 eventi futuri; venue vuota: Teatro Cilea)
- Marche Teatro | https://www.marcheteatro.it | Ancona | tribe_api (30 eventi futuri, Teatro delle Muse e Ridotto)
In html (pagina con l'elenco):
- VisitSicily | https://www.visitsicily.info/eventi/ | Sicilia | html (o API /wp-json/wp/v2/evento-new, 563 schede)
- Palazzo Strozzi | https://www.palazzostrozzi.org/calendario/ | Firenze | html
- Teatro Lirico di Cagliari | https://www.liricocagliari.it/stagione-2027/ | Cagliari | html
- Fondazione Ravello | https://www.fondazioneravello.com/eventi/ | Ravello (SA) | html
- Comune di Ancona | https://www.comune.ancona.it/it/eventi | Ancona | html
- Umbria Jazz | https://www.umbriajazz.it/programma/ | Perugia e Orvieto | html
- Santa Cecilia | https://santacecilia.it/concerti/calendario-concerti/ | Roma | html
- Bologna Welcome | https://www.bolognawelcome.com/it/eventi | Bologna | html
- Emilia-Romagna Turismo | https://emiliaromagnaturismo.it/it/eventi | Emilia-Romagna | html

## Lezioni
- Molti siti ufficiali bloccano esplicitamente ClaudeBot o Claude-User in robots.txt (teatri lirici, portali regionali
  di Sardegna, Liguria, Valle d'Aosta): controllare robots.txt prima di ogni nuova fonte, anche ufficiale.
- I termini generati da iubenda stanno su iubenda.com/termini-e-condizioni/<id> (stesso id della privacy
  iubenda.com/app/privacy-policy/<id>/legal): cosi' si trovano i termini di un sito senza aprirne altre pagine.
- I portali Municipium dei comuni (/it/events: Teramo, Foggia, Taranto, Aosta) e molti teatri caricano gli eventi in
  JavaScript: con curl la pagina e' vuota, serve WebFetch.
- Il tema WordPress dei comuni (Designers Italia) non espone gli eventi nell'API REST.

## Problemi
- Errore mio: la sonda automatica sulla lista di candidati ha aperto anche la home e l'URL dell'API tribe di zero.eu,
  sardegnaeventi24.it, solosagre.it e sagritaly.com prima che fossero verificati (fonti nuove = da trattare come
  vietate). Ne ho preso solo l'esito tecnico (WordPress sì/no, nessun dato strutturato), nessun testo o evento; per
  le tre da verificare non ho usato nulla. In futuro la sonda va lanciata solo su siti ufficiali.
- ticketone.it irraggiungibile per la terza volta stanotte; classicalive.it e 2night.it richiedono una lettura manuale
  (indirizzo dei termini sconosciuto / pagine legali vietate da robots.txt).
- Siti irraggiungibili dalla sonda (errore di connessione o proxy), da riprovare: fondazionepetruzzelli.it,
  teatrorendano.it, teatrodisardegna.it, comune.lecce.it, comune.palermo.it, comune.nuoro.it, comune.chieti.it,
  comune.caserta.it, comune.trapani.it, comune.perugia.it, basilicataturistica.it, abruzzoturismo.it, incampania.com,
  operacarlofelicegenova.it, amatmarche.net, maxxi.art, mann-napoli.it, museomadre.it. 403 dalla sonda: comune.bari.it,
  comune.potenza.it, teatrobiondo.it, yesmilano.it, piemontedalvivo.it, teatropubblicocampano.com.
