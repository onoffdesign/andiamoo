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
- Aggregatori locali utili: insolitotrantran (eventi piccoli e culturali), 2night (serate, titoli da ripulire),
  eventiesagre (sagre; a volte sbaglia il comune, es. "Mordano" per Badoere di Morgano), calendari podistici
  (calendariopodismo, podismoveneto, running.life), Musincantus per la musica d'autunno.
- Comune di Treviso: MyPortal, gia' letto dal PC.
- Teatri: Teatro Accademia di Conegliano (stagione di prosa, orari non sempre pubblicati); Teatro Accademico di
  Castelfranco (stagione Arteven e Ragazzi che Teatro: la scheda del Comune ha date, orari e prezzi). I teatri
  comunali del circuito Arteven sono il buco piu' grande della copertura: partire da MyArteven.
- Festival d'autunno a Treviso: 4passiFestival (fine ottobre-novembre), Sile Classica (ottobre-dicembre),
  Autunno Musicale. Un festival = una lettura per molti eventi.
- Sagre di novembre: sagramap elenca date ma senza link; le pagine ufficiali spesso non esistono (solo Facebook).
- Mercatini ricorrenti: le schede cosedicasa indicano la regola (seconda/terza domenica) e le sospensioni.
- Da evitare: microturismodellevenezie (date contraddittorie), deliziedautunno.tv e cultura.gov.it (vietano i robot).

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

- 2026-10-31 · TV · ricerche 51 · eventi nuovi 24 · eventi per ricerca 0,5 · fonti al PC +2 (Gli Alcuni, Biblioteche Treviso) · miglioria: per Eventbrite la pagina dell'evento diventa link d'azione (opzione `pagina_iscrizione` in sources.yaml), cosi' ~40 eventi a notte non finiscono piu' in coda per "manca il sito ufficiale"
