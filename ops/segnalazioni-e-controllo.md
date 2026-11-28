# Segnalazioni e controllo

Memoria degli errori e della qualita'. La revisione notturna lo legge **per primo** (prima di `lezioni.md`) e lo
aggiorna ogni notte. Serve a non ripetere gli errori gia' trovati da Federico e dal pubblico, e a misurare se il
lavoro migliora davvero.

Tre parti:
1. **Errori segnalati da Federico**: regole permanenti nate da errori veri. Non si tolgono mai; se una regola
   diventa codice (il PC la applica da solo) si scrive accanto "(ora nel codice)" ma resta qui.
2. **Segnalazioni dal sito**: cosa e' arrivato da "Segnala un errore" e cosa si e' fatto.
3. **Controllo a campione**: ogni notte alcuni eventi a caso (10 col piano Pro, vedi `ops/budget.yaml`) verificati
   sulla fonte ufficiale, con il risultato.

Ogni errore che si ripete (dal sito o dal campione) diventa una nuova riga nella parte 1.

## 1. Errori segnalati da Federico (regole permanenti)

- 2026-10-29 · **Solo eventi specifici.** Un calendario o elenco ("Calendario mensile eventi e sagre" di
  eventiesagre) era sul sito come evento. Calendari, agende, guide e pagine di portali non sono eventi: si rimuovono
  e se ne estraggono i singoli eventi della provincia. Ricorrenti divisi in date singole. (ora anche nel codice)
- 2026-10-29 · **Niente segnaposto nei campi.** Era comparso "sconosciuto" come prezzo e "(indirizzo esatto non
  disponibile)" come indirizzo. Un dato che non si conosce resta vuoto. (ora nel codice)
- 2026-10-29 · **Eventi passati.** Gli eventi di oggi restano visibili tutto il giorno; quelli finiti spariscono dal
  giorno dopo, secondo l'ora italiana. (ora nel codice)
- 2026-10-29 · **Posizione giusta.** Gli eventi di Treviso con solo il comune erano finiti al centro della
  provincia, 16 km a nord (Treviso Sotterranea a Porta San Tomaso, Museo Salce a Santa Margherita). Un comune non va
  mai confuso con la provincia omonima; ogni punto lontano dal centro del suo comune si verifica e si corregge con
  coordinate di una fonte affidabile; se il punto esatto non si trova, si mette nel posto piu' vicino certo. (ora
  anche nel codice: il PC scarta la provincia e segnala i punti a piu' di 6 km dal centro)

- 2026-10-31 · **Il link deve portare all'evento.** Controllo a campione 0/10, sempre per il link: un profilo Instagram
  o un campo vuoto non sono un link ufficiale. Per gli eventi con link social si cerca il sito o la pagina
  dell'evento; se non c'e', resta in coda. (Superata il 2026-11-28 per Eventbrite: vedi la regola fonti qui sotto.)

- 2026-11-28 · **Verifica delle fonti** (decisa da Federico): se in robots.txt e nei termini e condizioni non c'e'
  nessun divieto di scraping dei dati degli eventi o simili (crawling, estrazione automatica, data mining, riuso
  automatizzato), la fonte e' valida e va in `ammesse` con data e pagine lette. Divieto trovato: `vietate` con la
  frase. Pagine non leggibili: resta da verificare. Il "nel dubbio vietata" vale solo finche' non si sono lette.

- 2026-11-28 · **REGOLA FONTI: piattaforme con divieto di scraping** (decisa da Federico). Elenco in
  `config/fonti-vietate.yaml`, Eventbrite per primo; nel dubbio una fonte vale come vietata. Sulle vietate: niente
  visite, letture o analisi automatiche (nemmeno per scoprire eventi), niente endpoint interni, servizi di scraping
  terzi, proxy o user agent falsi, niente testi o immagini. Un evento che compare li' si pubblica solo se si trova
  su una fonte ammessa (organizzatore, sede, comune, pro loco, altre fonti ammesse), stesso titolo, data, orario e
  luogo, con dati presi solo da li', riassunto originale di 2-3 frasi e fonte indicata; il link della piattaforma
  solo come "Iscrizioni su ..." (`ticket_url`). Senza fonte ammessa: `ops/da-verificare.json`. Log dei prelievi in
  `ops/prelievi.csv`, richieste di rimozione in `ops/richieste-rimozione.md`. (ora nel codice: il PC non legge le
  fonti vietate o da verificare, nemmeno dalla cache; export e `--applica` tolgono dal sito gli eventi presi da li')

- 2026-11-05 · **Sigla della provincia nel comune.** "Treviso (TV)" faceva cercare il comune sbagliato: 45 eventi di
  Gli Alcuni a Treviso erano a Vittorio Veneto (37 km). Si toglie la sigla prima di geolocalizzare e si controlla
  sempre la distanza dal centro del comune. Le repliche riservate alle scuole non sono eventi pubblici: si
  rimuovono. (ora nel codice: `clean_town` in geocode, `escludi_titoli` nelle fonti)

- 2026-11-06 · **Accesso degli eventi Eventbrite.** Nel campione e nella coda l'errore piu' frequente e' l'accesso
  "sconosciuto" degli eventi Eventbrite (il JSON-LD dell'elenco non ha il prezzo). Si legge l'elenco "solo gratuiti"
  di Eventbrite: chi vi compare e' gratuito su iscrizione. (ora nel codice: `free_listing_urls` della fonte eventbrite)

- 2026-11-11 · **Punti sparsi nel centro storico.** Gli eventi di Gli Alcuni al Parco degli Alberi Parlanti (Viale
  G. G. Felissent 56) comparivano in punti a caso del centro di Treviso: Nominatim non trovava l'indirizzo con le
  iniziali e il PC ripiegava sul centro del comune, che sulla mappa viene sparso. Per i luoghi che tornano ogni
  settimana si scrivono le coordinate verificate in `config/luoghi.yaml`; il geocoder prova anche l'indirizzo senza
  iniziali e senza parentesi e, se trova solo la frazione (Dosson, Camalo', Collalto), mette il punto sulla frazione e
  non sul centro del comune. (ora nel codice: `known_place`, `place_queries`, precisione `frazione`)
  Federico: "non posso essere io a dirtelo ogni volta". Da allora il PC controlla a ogni giro la posizione di
  tutti gli eventi (`pipeline/posizioni.py`, risultato in `ops/posizioni.json`) e la revisione notturna sistema i
  luoghi segnalati ogni notte (passo 3b2). (ora nel codice)

- 2026-11-28 · **Punto subito per i luoghi nuovi.** Nel campione 6 errori su 20 erano eventi con il luogo nominato
  ma il punto sul centro del comune (fino a 3 km), quasi tutti presi da Qdpnews e Nordest24. Chi aggiunge un evento con
  un luogo che non e' in `config/luoghi.yaml` ne cerca subito il punto (OpenStreetMap) e lo mette in lat/lon o lo
  segnala alla revisione. Il link ufficiale non e' mai la pagina di vendita dei biglietti (TicketSMS): serve la
  scheda del locale o dell'organizzatore.

## 2. Segnalazioni dal sito

Il PC esporta ogni notte in `ops/segnalazioni.json` le segnalazioni degli ultimi 30 giorni (mai i contatti di chi
scrive). Per ognuna non ancora presente qui sotto: verifica sulla fonte ufficiale, poi correggi o rimuovi in
`config/correzioni.yaml`, oppure annota perche' non serve. Se lo stesso tipo di errore torna, aggiungi una regola
alla parte 1.

Formato: `- AAAA-MM-GG · segnalazione #id · uid · cosa diceva (in breve) · cosa e' stato fatto`

(nessuna segnalazione registrata finora; 2026-11-01, 2026-11-02, 2026-11-05, 2026-11-06, 2026-11-07, 2026-11-08, 2026-11-09, 2026-11-10, 2026-11-11 2026-11-12, 2026-11-13, 2026-11-14, 2026-11-15, 2026-11-16, 2026-11-17, 2026-11-18, 2026-11-19, 2026-11-20, 2026-11-21, 2026-11-22, 2026-11-23, 2026-11-24, 2026-11-25, 2026-11-26, 2026-11-27 e 2026-11-28: nessuna arrivata (il 28/11, letto due volte anche nella notte, il modulo Google aveva solo due righe di prova TEST, l'ultima del 28/11/2026 11.09.13); il PC ha riesportato il file l'11/11 mattina con 0 segnalazioni)

## 3. Controllo a campione

Il PC sceglie ogni notte N eventi a caso dei prossimi 30 giorni (N = `campione` in `ops/budget.yaml`) (`ops/campione.json`, sempre gli stessi per la
stessa data). Per ognuno apri la fonte ufficiale e controlla sei campi: **data**, **orario**, **luogo** (punto sulla
mappa compreso), **accesso e prezzo**, **categoria**, **link ufficiale** (funziona e porta all'evento giusto).
Un evento e' "corretto" solo se tutti e sei sono giusti. Gli errori trovati si correggono subito come nel passo 3.

Formato (una riga per notte, la piu' recente in alto):
`- AAAA-MM-GG · corretti N/10 · errori: data N, orario N, luogo N, accesso N, categoria N, link N · lezione: ...`

Obiettivo: almeno il 90% stabile. Se una notte scende sotto l'80%, la causa principale va scritta nella parte 1 e
segnalata nei `problemi` del riepilogo.

- 2026-11-28 (notte, seconda prova) · corretti 9/20 · errori: data 0, orario 4, luogo 6, accesso 1, categoria 0, link 3 · lezione: primo campione da 20 letto davvero; l'errore principale e' il punto sul solo comune per gli eventi presi da Qdpnews e Nordest24 con un luogo nominato (6/20, ora 88 luoghi nuovi in luoghi.yaml); i link a pagine di vendita (TicketSMS) non sono link ufficiali; due orari di Boschi a Natale non si trovano sulle fonti. Sotto l'80%: regola aggiunta nella parte 1 (punto subito per i luoghi nuovi)
- 2026-11-28 (notte, prima prova) · campione nuovo di 20 non controllato · errori: non misurati · lezione: WebFetch bloccato dalla rete della sessione (ENOTFOUND), nessuna fonte ufficiale leggibile; i 20 eventi restano da controllare la notte dopo
- 2026-11-28 · corretti 6/10 · errori: data 0, orario 0, luogo 1, accesso 2, categoria 0, link 2 · lezione: diciassettesima notte con il campione dell'11/11 (il PC non gira), nessuna ricerca spesa: restano gli stessi quattro aperti, quasi tutti conclusi. Sotto l'80%: cause gia' note, nessuna regola nuova
- 2026-11-27 · corretti 6/10 · errori: data 0, orario 0, luogo 1, accesso 2, categoria 0, link 2 · lezione: sedicesima notte con il campione dell'11/11 (il PC non gira), nessuna ricerca spesa: restano gli stessi quattro aperti, quasi tutti conclusi. Sotto l'80%: cause gia' note, nessuna regola nuova
- 2026-11-26 · corretti 6/10 · errori: data 0, orario 0, luogo 1, accesso 2, categoria 0, link 2 · lezione: quindicesima notte con il campione dell'11/11 (il PC non gira), nessuna ricerca spesa: restano gli stessi quattro aperti, quasi tutti conclusi. Sotto l'80%: cause gia' note, nessuna regola nuova
- 2026-11-25 · corretti 6/10 · errori: data 0, orario 0, luogo 1, accesso 2, categoria 0, link 2 · lezione: quattordicesima notte con il campione dell'11/11 (il PC non gira), nessuna ricerca spesa: restano gli stessi quattro aperti, quasi tutti conclusi. Sotto l'80%: cause gia' note, nessuna regola nuova
- 2026-11-24 · corretti 6/10 · errori: data 0, orario 0, luogo 1, accesso 2, categoria 0, link 2 · lezione: tredicesima notte con il campione dell'11/11 (il PC non gira), nessuna ricerca spesa: restano gli stessi quattro aperti, quasi tutti conclusi. Sotto l'80%: cause gia' note, nessuna regola nuova
- 2026-11-23 · corretti 6/10 · errori: data 0, orario 0, luogo 1, accesso 2, categoria 0, link 2 · lezione: dodicesima notte con il campione dell'11/11 (il PC non gira), nessuna ricerca spesa: restano gli stessi quattro aperti, quasi tutti conclusi. Sotto l'80%: cause gia' note, nessuna regola nuova; ora il piano della notte avvisa da solo quando il PC e' fermo
- 2026-11-22 · corretti 6/10 · errori: data 0, orario 0, luogo 1, accesso 2, categoria 0, link 2 · lezione: undicesima notte con il campione dell'11/11 (il PC non gira), nessuna ricerca spesa: restano gli stessi quattro aperti, quasi tutti conclusi. Sotto l'80%: cause gia' note, nessuna regola nuova
- 2026-11-21 · corretti 6/10 · errori: data 0, orario 0, luogo 1, accesso 2, categoria 0, link 2 · lezione: decima notte con il campione dell'11/11 (il PC non gira), nessuna ricerca spesa: restano gli stessi quattro aperti (accesso non pubblicato di Giornate Martiniane e Sagra del Frico, luogo e link delle Letture animate di Silea, link Instagram e accesso di Borgo Caiada), ormai quasi tutti conclusi. Sotto l'80%: cause gia' note, nessuna regola nuova
- 2026-11-20 · corretti 6/10 · errori: data 0, orario 0, luogo 1, accesso 2, categoria 0, link 2 · lezione: nona notte con il campione dell'11/11 (il PC non gira), nessuna ricerca spesa: restano gli stessi quattro aperti (accesso non pubblicato di Giornate Martiniane e Sagra del Frico, luogo e link delle Letture animate di Silea, link Instagram e accesso di Borgo Caiada). Sotto l'80%: cause gia' note, nessuna regola nuova
- 2026-11-19 · corretti 6/10 · errori: data 0, orario 0, luogo 1, accesso 2, categoria 0, link 2 · lezione: ottava notte con il campione dell'11/11 (il PC non gira), nessuna ricerca spesa: restano gli stessi quattro aperti (accesso non pubblicato di Giornate Martiniane e Sagra del Frico, luogo e link delle Letture animate di Silea, link Instagram e accesso di Borgo Caiada), cercati a vuoto da 6-7 notti. Sotto l'80%: cause gia' note, nessuna regola nuova
- 2026-11-18 · corretti 6/10 · errori: data 0, orario 0, luogo 1, accesso 2, categoria 0, link 2 · lezione: settima notte con il campione dell'11/11 (il PC non gira), nessuna ricerca spesa: stessi quattro aperti (accesso non pubblicato di Giornate Martiniane e Sagra del Frico, luogo e link delle Letture animate di Silea, link Instagram e accesso di Borgo Caiada), gia' cercati a vuoto da 5-6 notti. Sotto l'80%: cause gia' note, nessuna regola nuova
- 2026-11-17 · corretti 6/10 · errori: data 0, orario 0, luogo 1, accesso 2, categoria 0, link 2 · lezione: sesta notte con il campione dell'11/11 (il PC non gira), nessuna ricerca spesa: restano gli stessi quattro aperti (accesso non pubblicato di Giornate Martiniane e Sagra del Frico, luogo e link delle Letture animate di Silea, link Instagram e accesso di Borgo Caiada), tutti cercati a vuoto da 4-5 notti. Sotto l'80%: cause gia' note, nessuna regola nuova
- 2026-11-16 · corretti 6/10 · errori: data 0, orario 0, luogo 1, accesso 2, categoria 0, link 2 · lezione: quinta notte con il campione dell'11/11 (il PC non gira), nessuna ricerca spesa (tutti gli aperti cercati a vuoto da 3-4 notti). Giusti i due conclusi (La Valutazione del Paesaggio, Open Day H-FARM), Alcesti, Prosecco Ultra Trail, Natale a Collalto, Concerto dell'Immacolata (corretto ieri). Restano l'accesso non pubblicato di Giornate Martiniane e Sagra del Frico, luogo e link delle Letture animate di Silea, link Instagram e accesso 'invito' di Borgo Caiada (un mercatino non e' su invito: da ricontrollare quando esce una pagina). Sotto l'80%: cause gia' note, nessuna regola nuova
- 2026-11-15 · corretti 5/10 · errori: data 0, orario 0, luogo 1, accesso 3, categoria 0, link 2 · lezione: quarta notte con il campione dell'11/11 (il PC non gira). Giusti La Valutazione del Paesaggio e Open Day H-FARM (conclusi), Alcesti, Prosecco Ultra Trail, Natale a Collalto. Corretto stanotte l'accesso del Concerto dell'Immacolata (ingresso libero con offerta responsabile, riportato da ClassicaLive dalla scheda Musincantus): dopo la correzione 6/10. Restano l'accesso non pubblicato di Giornate Martiniane e Sagra del Frico, luogo e link delle Letture animate di Silea, il link Instagram di Borgo Caiada; nessuna ricerca spesa su questi (gia' cercati 3 notti). Sotto l'80%: cause gia' note, nessuna regola nuova
- 2026-11-14 · corretti 5/10 · errori: data 0, orario 0, luogo 1, accesso 3, categoria 0, link 2 · lezione: terza notte con il campione dell'11/11 (il PC non gira). Giusti Alcesti, Open Day H-FARM (oggi), Prosecco Ultra Trail, Natale a Collalto (punto del castello applicato ieri) e La Valutazione del Paesaggio (concluso il 12/11, era giusto). Due ricerche spese senza esito per il link di Borgo Caiada (nessuna pagina oltre Instagram e insolitotrantran) e per l'accesso delle Giornate Martiniane (non pubblicato). Restano l'accesso non pubblicato di tre eventi e luogo e link delle Letture animate di Silea. Sotto l'80%: cause gia' note (dati non pubblicati dagli organizzatori, PC fermo), nessuna regola nuova
- 2026-11-13 · corretti 4/10 · errori: data 0, orario 0, luogo 2, accesso 3, categoria 0, link 2 · lezione: stesso campione dell'11/11 (il PC non gira). Giusti Alcesti, Open Day H-FARM, Prosecco Ultra Trail e La Valutazione del Paesaggio (ora concluso). Corretto stanotte il punto di Natale a Collalto (Castello di Collalto da Mapcarta, prima sul centro di Susegana). Restano l'accesso non pubblicato di tre eventi (Giornate Martiniane, Sagra del Frico, Concerto dell'Immacolata), luogo e link delle Letture animate di Silea (il sito del Comune vieta WebFetch) e il link Instagram di Borgo Caiada (una ricerca, nessuna pagina ufficiale). Sotto l'80%: cause gia' note, nessuna regola nuova
- 2026-11-12 · corretti 4/10 · errori: data 0, orario 0, luogo 2, accesso 3, categoria 0, link 2 · lezione: campione nuovo (giro del PC dell'11/11). Giusti Alcesti al Del Monaco, Open Day H-FARM, Prosecco Ultra Trail e La Valutazione del Paesaggio (MyPortal del Comune, non riaperto). L'accesso non e' pubblicato dall'organizzatore per tre eventi (La cultura genera valore delle Giornate Martiniane, Sagra del Frico, Concerto dell'Immacolata): errori non correggibili, non di trascrizione. Luogo e link mancanti per le Letture animate di Silea (elenco del Comune senza scheda) e per Borgo Caiada (solo Instagram, nessuna pagina ufficiale nei risultati); Natale a Collalto ha il punto sul centro del comune, ora la frazione si posiziona dal codice nuovo. Sotto l'80%: la causa principale e' l'accesso non pubblicato, gia' nota (regola sagre e rassegne: lasciare vuoto, non dedurre)
- 2026-11-11 · corretti 3/10 · errori: data 1, orario 1, luogo 1, accesso 0, categoria 0, link 1 · lezione: quinto giorno con il campione del 6/11 (il PC non gira), nessuna ricerca spesa: tre eventi conclusi gia' tolti, giusti Treviso Basket - Scafati, Spreafico al Mattorosso (12/11) e Prosecco Ultra Trail; aperti gli stessi quattro punti (data del 3/12 di Villa Bornello, visita per famiglie della Materia dei sogni, link Instagram di Bim Boom Jam, punto del Parco degli Alberi Parlanti). Sotto l'80%: la causa resta il PC fermo, gia' nei problemi
- 2026-11-10 · corretti 3/10 · errori: data 1, orario 1, luogo 1, accesso 0, categoria 0, link 1 · lezione: quarto giorno con lo stesso campione del 6/11 (il PC non gira), nessuna ricerca spesa: i tre eventi conclusi sono gia' tolti, restano giusti Treviso Basket - Scafati, Spreafico al Mattorosso e Prosecco Ultra Trail; aperti gli stessi quattro punti (data del 3/12 di Villa Bornello, visita per famiglie della Materia dei sogni, link Instagram di Bim Boom Jam, punto del Parco degli Alberi Parlanti). Sotto l'80%: la causa resta il PC fermo, gia' nei problemi
- 2026-11-09 · corretti 3/10 · errori: data 1, orario 1, luogo 1, accesso 0, categoria 0, link 1 · lezione: terzo giorno con lo stesso campione (il PC non gira dal 6/11). Tre eventi gia' conclusi (Non e' un mondo per donne, Prealpi in Festa, Cappella Sistina a Sernaglia): tolti dal sito. Restano giusti Treviso Basket - Scafati, Spreafico al Mattorosso e Prosecco Ultra Trail. Ancora aperti: data del 3/12 di Villa Bornello, visita per famiglie della Materia dei sogni, link Instagram di Bim Boom Jam (nessuna pagina dell'Isola B nei risultati), punto del Parco degli Alberi Parlanti (in attesa del PC). Sotto l'80%: causa il PC fermo, gia' nei problemi
- 2026-11-08 · corretti 3/10 · errori: data 1, orario 1, luogo 3, accesso 0, categoria 0, link 1 · lezione: stesso campione del 6/11 (il PC non gira), tre eventi gia' conclusi. Giusti Treviso Basket - Scafati, Spreafico al Mattorosso e Prosecco Ultra Trail dopo le correzioni di ieri. Corretti stanotte: comune di Bim Boom Jam (Falze' di Piave e' frazione di Sernaglia), nome del luogo di Villa Bornello (era uno slogan). Restano: la data del 3/12 di Villa Bornello (la pagina del podcast parla solo dell'edizione di aprile), la visita per famiglie della Materia dei sogni (non elencata nella pagina dei Musei Civici), il link Instagram di Bim Boom Jam e il punto del Parco degli Alberi Parlanti (in attesa del giro del PC). Sotto l'80%: la causa resta il PC fermo (campione e correzioni non si rinnovano), gia' nei problemi
- 2026-11-07 · corretti 1/10 · errori: data 0, orario 1, luogo 2, accesso 1, categoria 0, link 2 · lezione: campione nuovo (giro del PC del 6/11 mattina). Due eventi del 6/11 gia' conclusi e due non aperti per budget (visita La materia dei sogni, Villa Bornello). Giusto solo Treviso Basket - Scafati. Corretti: Prosecco Ultra Trail (parte da Vittorio Veneto, non da Vidor), link e prezzo di Spreafico al Mattorosso (pagina del locale al posto di Instagram), punto del Parco degli Alberi Parlanti (era il provvisorio in centro: ora indirizzo Viale Felissent 56 da geolocalizzare). Restano l'accesso del concerto della Cappella Sistina (non pubblicato) e il link Instagram di Bim Boom Jam. Sotto l'80%: la causa principale resta il link social degli eventi di insolitotrantran, gia' nella parte 1
- 2026-11-06 · corretti 3/10 · errori: data 0, orario 0, luogo 1, accesso 4, categoria 0, link 2 · lezione: stesso campione del 3/11 (il PC non gira), ricontrollato dopo le correzioni. STORIES all'Anima Club ora giusto (gratuito su iscrizione, 22:30) grazie all'elenco Eventbrite dei gratuiti; restano l'accesso di tre eventi Eventbrite assenti da quell'elenco (Bosa Ceramiche, Medicina cinese, Viaggio nel radical design: probabilmente a pagamento, scheda non apribile) e di Autunno Musicale, i link Instagram (Pro Loco Maserada, Macedonia Sintetica) e il luogo della staffetta di cross. Sotto l'80%: regola aggiunta nella parte 1 (accesso Eventbrite)
- 2026-11-05 · corretti 0/10 · errori: data 0, orario 0, luogo 2, accesso 6, categoria 0, link 2 · lezione: campione del 3/11 (il PC non gira da allora). L'accesso e' l'errore principale: 4 eventi Eventbrite (.Ettore, Cosniga, Anima Club) e Autunno Musicale senza ingresso pubblicato; corretti Anatomia di un film (corso su iscrizione) e la posizione di Nardo il ghepardo (Gli Alcuni, era a Vittorio Veneto). Restano i link Instagram di Pro Loco Maserada e Macedonia Sintetica. Sotto l'80%: causa nella parte 1 (posizione) e in lezioni (Eventbrite senza prezzo nel JSON-LD dell'elenco)
- 2026-11-02 · corretti 7/10 · errori: data 0, orario 1, luogo 1, accesso 2, categoria 0, link 0 · lezione: il PC non ha girato, campione uguale a ieri: ricontrollato dopo le correzioni. Il link non e' piu' un errore; restano la staffetta di cross di Santa Lucia (solo il comune), la visita ad Anzano (pagina del Comune per la prenotazione, ma orario e costo 2026 non pubblicati) e il CRM da moku (solo Eventbrite, non apribile). Sotto l'80%: la causa sono i dati che l'organizzatore non pubblica (orario, accesso), non errori di trascrizione.
- 2026-11-01 · corretti 3/10 · errori: data 0, orario 1, luogo 1, accesso 2, categoria 0, link 3 · lezione: il link resta l'errore principale (Instagram per Edera e Treviso Sotterranea, nessun link per la staffetta di cross); tre eventi non verificabili nel budget (visita ad Anzano: pagina del Comune in errore; CRM da moku e 25 novembre all'Edera: solo Eventbrite). Corretti subito tutti gli errori trovati.
- 2026-10-31 · corretti 0/10 · errori: data 0, orario 2, luogo 1, accesso 2, categoria 1, link 10 · lezione: il link e' l'errore di tutti: gli eventi Eventbrite non avevano official_url e quelli di insolitotrantran puntano al profilo Instagram dell'organizzatore. Eventbrite risolto nel codice (pagina_iscrizione); per insolitotrantran serve cercare il sito dell'evento. Sei eventi su dieci non verificabili per budget (solo Instagram).
