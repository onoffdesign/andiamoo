# Metodo di ricerca

Il manuale di ricerca di ANDIAMO?, scritto e migliorato da Claude notte dopo notte. Contiene **cosa funziona per
trovare eventi con meno ricerche e meno AI**, organizzato per livello: regole generali, regole per regione, regole
per provincia, aggregatori che valgono per piu' province.

Differenza con gli altri file di memoria:
- `ops/lezioni.md` e' il quaderno degli appunti grezzi della notte (al massimo ~80 righe);
- questo file e' il **metodo consolidato**: una lezione confermata almeno due volte, o che vale per piu' province,
  si sposta qui (e si toglie da `lezioni.md`);
- `ops/fonti.yaml` e' il catalogo delle singole fonti; qui si scrive **come** usarle e **in che ordine**.

## Obiettivo e misura

Lo scopo e' usare sempre meno AI e meno ricerche per evento trovato. Ogni notte si misura:
- **ricerche fatte** (WebSearch + WebFetch) e **eventi nuovi aggiunti** dalla ricerca;
- **eventi per ricerca** = eventi nuovi / ricerche. Deve salire nel tempo;
- **fonti passate al PC**: una fonte letta dal PC ogni notte costa zero crediti. E' il miglior risparmio possibile.

Le tre misure vanno nel riepilogo della notte (`ops/riepilogo-notte.json`) e nella tabella in fondo a questo file.

## Regola d'oro: ogni notte una miglioria

Ogni notte almeno **una** miglioria concreta e misurabile, scritta in fondo alla sezione giusta con la data:
- una fonte con dati strutturati spostata al PC (`config/sources.yaml`);
- una query piu' precisa che porta dritto alla pagina eventi (nel campo `query` di `ops/fonti.yaml`);
- un raccoglitore del PC corretto o reso piu' preciso (luogo, orario, prezzo letti meglio);
- una fonte inutile tolta dal giro (meno ricerche sprecate);
- una regola che evita un errore gia' visto (anche in `ops/segnalazioni-e-controllo.md`).

## 1. Regole generali (valgono ovunque)

Ordine di lavoro per una provincia, dal piu' economico al piu' costoso:
1. **Fonti del PC** (`config/sources.yaml`): costano zero. Prima di cercare, guarda cosa ha gia' portato il PC.
2. **Fonti note in scadenza** (`ops/fonti.yaml`): si riaprono con la loro `query`, senza ricerche esplorative.
3. **Comuni e pro loco** non controllati da piu' tempo (`ops/copertura.yaml`).
4. **Categorie di dettaglio** (`ops/categorie-ricerca.md`) non cercate da piu' tempo in quella provincia.
5. **Ricerca esplorativa** di fonti nuove: solo con il tempo che resta.

Eventi annuali: l'archivio storico (`python -m pipeline.archive --cerca`) conserva tutte le edizioni passate. Circa un
mese prima della data dell'anno precedente, cerca la nuova edizione di sagre, festival, gare e rassegne gia' viste:
e' la ricerca con la resa piu' alta in assoluto.

Come cercare:
- Una ricerca deve puntare a una **pagina che elenca piu' eventi** (calendario di un comune, pagina eventi di un
  teatro, gruppo di gare), non a un singolo evento: un elenco rende 5-20 eventi per una sola lettura.
- Per i siti locali italiani la ricerca "standard" rende poco: usare "extended" per comuni, pro loco, rassegne.
- WebFetch apre solo link comparsi nei risultati di ricerca: cercare "titolo + comune + anno" per far uscire la
  pagina giusta.
- Controllare sempre l'anno: molte pagine parlano di edizioni passate.
- Dati strutturati prima di tutto: una pagina con JSON-LD `Event`, un sito WordPress con The Events Calendar
  (`/wp-json/tribe/events/v1/events`) o un comune MyPortal si passano al PC subito.
- Fonti ufficiali come conferma e come `official_url`; aggregatori e piattaforme solo per scoprire.
- Rispettare robots.txt e i termini d'uso dei siti; niente accessi con account.

## 2. Regole per regione

### Veneto
- Molti comuni usano MyPortal della Regione (`/myportal/C_xxxx/`): fonte `myportal` con il codice IPA, gratis per il PC.
- Pro Loco: rete UNPLI Veneto, con pagine eventi per provincia.

## 3. Regole per provincia

Ogni provincia ha la sua sezione con: aggregatori locali specifici, comuni con calendari ben fatti, periodi
dell'anno con piu' eventi, errori tipici. Quando si apre una provincia nuova (vedi `ops/espansione.md`) si copia
lo schema e si parte dalle regole generali e da quelle della regione.

### Treviso (TV) - provincia attiva dal 2026-10
- Eventi di stagione (miglioria del 2026-11-09): mostre, stagioni teatrali, campionati e rassegne tematiche coprono
  mesi interi e si leggono in blocco. Ordine: elenco di itinerarinellarte.it/it/mostre/treviso (10 mostre, 1 sola era
  sul sito; le schede si aprono solo dopo che compaiono in una ricerca "<titolo> <sede> orari biglietti"), pagina
  "biglietti e abbonamenti" del Teatro Stabile del Veneto (12 spettacoli con tutte le repliche), calendari ufficiali di
  squadre e federazioni (imocovolley.it/fixtures, federugby), rassegne UNPLI come Fiori d'Inverno (13 feste del
  radicchio fino a febbraio in una lettura), elenchi eventi delle biblioteche con la stagione del teatro comunale
  (bibliotecazerobranco.it). Il 2026-11-09: 8 letture utili, 59 eventi fino a febbraio.
- Sagre del mese (miglioria del 2026-11-08): leggere prima l'elenco di trovasagre.com/sagre/veneto/treviso (13 sagre
  con frazione e date in una lettura), confrontarlo con `--cerca`, poi confermare solo le mancanti su Pro Loco, Comune
  o Paesi in Festa (Opitergino-Mottense). Molti comuni pubblicano un PDF con il calendario annuale di tutte le
  associazioni (cercare "Eventi <comune> 2026 pdf"): ufficiale, una lettura per tutto l'anno (Povegliano: 5 eventi).
- Aggregatori locali utili: insolitotrantran (eventi piccoli e culturali), 2night (serate, titoli da ripulire),
  eventiesagre (sagre; a volte sbaglia il comune, es. "Mordano" per Badoere di Morgano), calendari podistici
  (calendariopodismo, podismoveneto, running.life), Musincantus per la musica d'autunno.
- Comune di Treviso: MyPortal, gia' letto dal PC.
- Comuni MyPortal (miglioria 2026-11-01): si riconoscono dagli indirizzi `/home/vivere/...` o
  `/home/dettaglio/eventi/...` nei risultati di ricerca; il codice IPA e' `C_` + codice catastale del comune (Treviso
  C_L407, Paese C_G229, Maser C_F009). Appena se ne vede uno si aggiunge a `config/sources.yaml` come `myportal`
  senza altre ricerche: il PC li legge gratis ogni notte. Se il rapporto dopo da' errore o zero eventi, il sito
  ha un codice diverso (controllarlo nel sorgente della pagina) o non pubblica eventi.
- Siti che vietano i robot o danno errore a WebFetch (usare solo i risultati di ricerca): trevisosotterranea.it,
  comune.pievedisoligo.tv.it, rockol.it, itinerarinelgusto.it, comune.cappellamaggiore.tv.it.
  Dal 2026-11-07 anche i siti design-comuni di Quinto, Vedelago e Valdobbiadene (robots_disallowed per WebFetch).
- Feste di paese e rassegne comunali (miglioria 2026-11-07): il calendario di trevisoeventi elenca i titoli, la
  scheda di dettaglio di ciascuno (stesso dominio, si apre con WebFetch) ha programma per giorno, luogo, ingresso e
  sito dell'organizzatore. Una lettura per festa: si aggiunge un evento per giornata con programma, con
  `official_url` il sito dell'organizzatore se c'e', altrimenti la scheda di trevisoeventi (meglio di Facebook).
  Le date dei mercatini mensili nelle schede vanno controllate con la regola (es. 'seconda domenica').
- Teatri: Teatro Accademia di Conegliano (stagione di prosa, orari non sempre pubblicati); Teatro Accademico di
  Castelfranco (stagione Arteven e Ragazzi che Teatro: la scheda del Comune ha date, orari e prezzi). I teatri
  comunali del circuito Arteven sono il buco piu' grande della copertura: partire da MyArteven.
- Festival d'autunno a Treviso: 4passiFestival (fine ottobre-novembre), Sile Classica (ottobre-dicembre),
  Autunno Musicale. Un festival = una lettura per molti eventi.
- Sagre di novembre: sagramap elenca date ma senza link; le pagine ufficiali spesso non esistono (solo Facebook).
- Mercatini ricorrenti: le schede cosedicasa indicano la regola (seconda/terza domenica) e le sospensioni.
- Da evitare: microturismodellevenezie (date contraddittorie), deliziedautunno.tv e cultura.gov.it (vietano i robot).
- Scoperta piu' redditizia (2026-11-02): il calendario di trevisoeventi.com (una lettura, ~25 eventi TV di sagre,
  mercatini, rassegne e sport) e i calendari di stagione dei teatri (Teatro Da Ponte: 35 date TV in una lettura).
  Confermare sul sito ufficiale: alcune schede di trevisoeventi sono di anni passati.
- Siti di comuni con il tema WordPress "design comuni" (indirizzi `/vivere-il-comune/eventi/`, es. Castelfranco,
  San Biagio di Callalta) e calendari di teatri senza JSON-LD: si passano al PC come `html_llm` con un `hint` su
  comune e anno (miglioria 2026-11-02). Le schede MyPortal si riconoscono anche da `/home/vivere/eventi.html` e
  `/eventi/<nome>.html` (Povegliano, Loria).

- Sport da guardare (2026-11-05): i calendari ufficiali delle squadre danno tutte le partite casalinghe della
  stagione in una lettura (Treviso Basket 7, Benetton Rugby 6). L'Imoco Volley non e' leggibile cosi' (la pagina
  del Palaverde mostra solo partite passate): usare il calendario della Lega Volley Femminile.
- Compagnie teatrali in tournee con The Events Calendar (Nautilus Cantiere Teatrale): al PC come `tribe_api`, l'area
  filtra le date fuori provincia. Le pagine evento del FAI (fondoambiente.it/eventi) danno date, prezzi e prenotazione.
- Comuni con il portale `/home/vivere/eventi.html` ma senza codice IPA nella pagina (Silea, Monastier): al PC come
  `html_llm`, non `myportal` con un codice dedotto. Le fonti myportal con codice dedotto del 1-2/11 (Maser,
  Povegliano, Loria) danno errore di connessione dal PC.
- Accesso degli eventi Eventbrite (2026-11-06): non aprire le schede una per una; l'elenco "Eventi in Treviso gratuiti"
  (/d/italy--treviso--85685297/free--events/, anche ?page=N) conferma in una lettura 20 eventi gratuiti con ora e luogo.
  Ora lo legge il PC. Gli eventi Eventbrite che non vi compaiono sono probabilmente a pagamento: serve la scheda.
- Miglioria 2026-11-05: la sigla della provincia nel comune ("Treviso (TV)", "Farra di Soligo TV") faceva fallire la
  ricerca dell'area del comune e spediva i punti in un altro comune (Gli Alcuni: 45 eventi a Vittorio Veneto). Ora
  il geocoder la toglie (`clean_town`), il raccoglitore tribe pulisce i luoghi "• Treviso – Teatro" e ogni fonte
  puo' avere `escludi_titoli` (regex) per scartare le repliche riservate alle scuole.

## 4. Aggregatori che valgono per piu' province

Fonti utili in piu' province: si configurano una volta e si allargano a ogni provincia nuova (nuove pagine citta' o
nuovi filtri), senza ricercarle da capo.

| Aggregatore | Province coperte | Come si allarga |
|---|---|---|
| 2night | Veneto, Friuli | pagina per citta' |
| eventiesagre | tutta Italia | pagina per provincia (solo prima pagina) |
| running.life, gotrail | tutta Italia | pagina calendario per provincia o citta' |
| calendariopodismo | tutta Italia | parametro `localita` |
| TicketOne, DICE, Xceed | tutta Italia | pagine citta' o locale (verificare termini d'uso prima di monetizzare) |
| UNPLI / Pro Loco | per regione | pagina eventi regionale e provinciale |

## 5. Andamento (una riga per notte, la piu' recente in alto)

`- AAAA-MM-GG · provincia attiva · ricerche N · eventi nuovi N · eventi per ricerca N,N · fonti al PC +N · miglioria: ...`

- 2026-11-09 · TV · ricerche 57 · eventi nuovi 66 · eventi per ricerca 1,2 (piu' 2 corretti e 13 conclusi tolti dalla coda) · fonti al PC +0 · miglioria: per mostre, stagioni teatrali, campionati e rassegne tematiche si parte dalla pagina che elenca l'intera stagione (elenco mostre di itinerarinellarte, abbonamenti del Teatro Stabile del Veneto, calendari di squadre e federazioni, rassegna Fiori d'Inverno): 59 eventi da 8 letture; regola nuova nella sezione Treviso
- 2026-11-08 · TV · ricerche 59 · eventi nuovi 14 · eventi per ricerca 0,2 (piu' 9 corretti) · fonti al PC +2 (Comune di Trevignano e Comune di Gaiarine myportal, codici da confermare) · miglioria: elenco delle sagre del mese di trovasagre come primo passo per le sagre (9 mancanti su 13 in una lettura) e PDF annuali degli eventi dei Comuni come fonte ufficiale a basso costo; regola nuova nella sezione Treviso
- 2026-11-07 · TV · ricerche 62 · eventi nuovi 46 · eventi per ricerca 0,7 · fonti al PC +1 (Mattorosso html_llm) · miglioria: le schede di dettaglio di trevisoeventi si aprono con WebFetch e danno in una lettura il programma giorno per giorno e il sito dell'organizzatore: i buchi che il test di copertura trovava da tre notti (sagre di Colle Umberto, Visna' e Castagnole, Anima Teatro, mercatini di antiquariato, Milipiave) sono stati chiusi con una lettura ciascuno. Regola nuova nella sezione Treviso
- 2026-11-06 · TV · ricerche 60 · eventi nuovi 12 · eventi per ricerca 0,2 (piu' 14 corretti in blocco con 2 letture) · fonti al PC +3 (elenco Eventbrite gratuiti, Comune di Sernaglia html_llm, Comune di Mogliano myportal) · miglioria: la fonte Eventbrite legge anche l'elenco "solo gratuiti" (`free_listing_urls`): gli eventi che vi compaiono prendono accesso iscrizione e prezzo gratuito, cosi' l'errore di accesso piu' frequente della coda e del campione sparisce senza ricerche
- 2026-11-05 · TV · ricerche 50 · eventi nuovi 18 · eventi per ricerca 0,4 · fonti al PC +4 (Comune di Quinto, Silea e Monastier come html_llm; Nautilus Cantiere Teatrale come tribe_api) · miglioria: geocoder senza sigla della provincia nel comune, luoghi tribe ripuliti, `escludi_titoli` per le repliche per le scuole (meno errori di posizione e meno non-eventi senza ricerche)
- 2026-11-02 · TV · ricerche 52 · eventi nuovi 46 · eventi per ricerca 0,9 · fonti al PC +5 (Teatro Da Ponte, Comune di San Biagio, Comune di Castelfranco come html_llm; Comune di Povegliano e Comune di Loria come myportal) · miglioria: i siti senza dati strutturati ma con un buon elenco (tema design-comuni, calendari dei teatri) vanno al PC come html_llm invece di essere riletti a mano ogni settimana

- 2026-11-01 · TV · ricerche 55 · eventi nuovi 3 · eventi per ricerca 0,1 · fonti al PC +2 (Comune di Paese, Comune di Maser, MyPortal) · miglioria: i comuni MyPortal si aggiungono al PC senza ricerche (IPA = C_ + codice catastale), regola in sezione Treviso
- 2026-10-31 · TV · ricerche 51 · eventi nuovi 24 · eventi per ricerca 0,5 · fonti al PC +2 (Gli Alcuni, Biblioteche Treviso) · miglioria: per Eventbrite la pagina dell'evento diventa link d'azione (opzione `pagina_iscrizione` in sources.yaml), cosi' ~40 eventi a notte non finiscono piu' in coda per "manca il sito ufficiale"
