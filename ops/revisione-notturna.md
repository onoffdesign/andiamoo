# Revisione notturna di Claude

Istruzioni per la sessione Claude pianificata ogni notte. **Dal 2026-11-28 il PC fisso e' escluso** (piano Max,
`pc.attivo: false` in `config/settings.yaml`): Claude fa tutto dal cloud, raccolta, verifica, correzione, ricerca
e pubblicazione. Ha piena autonomia: corregge, pubblica e aggiunge fonti senza chiedere.

**Una sola sessione a notte, alle 01:07, con quattro agenti che lavorano in contemporanea** (decisione di Federico
del 2026-11-28). La sessione pianificata fa da **coordinatore**: prepara, lancia gli agenti in parallelo (strumento
Agent, in background), legge le risposte del modulo mentre loro lavorano, poi unisce, pubblica e manda il resoconto.

Il coordinatore:
1. Preparazione, `python -m pipeline.piano_notte`, lettura di `ops/segnalazioni-e-controllo.md` e di questo file.
2. Lancia **insieme**, nello stesso messaggio, i quattro agenti qui sotto (tipo general-purpose, in background). A
   ognuno passa: il suo compito, la sua quota di ricerche (il budget `ricerche_max` diviso come indicato), la parte
   del piano della notte che gli tocca (copiata nel testo), e le "Regole per gli agenti" qui sotto.
3. Mentre lavorano: risposte del modulo Google (passo 2b), scritte in `config/notte/coordinatore-*.yaml`.
4. Quando un agente finisce: `python -m pipeline.notte --unisci <agente>` (controlla e unisce le sue parti; se dice
   che non sono valide, correggile tu), poi `python -m pipeline.pubblica` e commit e push: il sito si aggiorna gia'
   mentre gli altri lavorano. Un agente che non risponde piu' entro la fine della notte: unisci quello che ha scritto.
5. Alla fine: memoria (dai resoconti `ops/notte/<agente>.md` riporta nei file di memoria cio' che va riportato:
   `ops/fonti.yaml`, `ops/lezioni.md`, `ops/metodo-ricerca.md`, `ops/categorie-ricerca.md`, `ops/espansione.md`),
   registro (passo 8), `--controlla`, test, pubblica, commit, push, messaggio finale con il resoconto.

Gli agenti (quota di ricerche sul totale):
- **giro** (25%): le "fonti del giro" del piano (per ognuna WebSearch per trovare la pagina, WebFetch, eventi futuri
  non ancora sul sito; data in `copertura.yaml` sezione `giro`) e la verifica delle fonti da verificare (robots.txt e
  termini). Solo lui modifica `config/fonti-vietate.yaml` e `config/sources.yaml`.
- **revisione** (25%): coda di revisione, controllo a campione, posizioni, test di copertura (passi 2-3c). Scrive le
  correzioni nella sua parte; solo lui modifica `config/luoghi.yaml`.
- **treviso** (25%): ricerca su Treviso, fasi 0 e A-E (comuni e categorie del piano). Date in `copertura.yaml`
  sezioni `comuni_TV`, `categorie_TV` e nelle sezioni di aggregatori, community e news.
- **italia** (25%): le province d'Italia della sezione 2b del piano. Date in `copertura.yaml` sezioni `province` e
  `comuni_<SIGLA>` delle altre province.

**Regole per gli agenti** (da copiare nel loro compito):
- tutte le regole di questo file valgono anche per loro, prima di tutto la REGOLA FONTI;
- scrivono **solo** i loro file: `config/notte/<agente>-eventi.yaml` (chiave `eventi`, stesso formato di
  `config/eventi_redazione.yaml`), `config/notte/<agente>-correzioni.yaml` (`correggi`, `rimuovi`, `verificati`,
  stesso formato di `config/correzioni.yaml`), `ops/notte/<agente>.md` (resoconto: numeri, fonti nuove da catalogare
  con nome, url, query e tipo, lezioni, problemi), piu' i file che sono solo loro (vedi sopra);
- in `ops/copertura.yaml` toccano solo le loro sezioni, sempre con modifiche puntuali (Edit) e mai riscrivendo il
  file intero; se una modifica fallisce perche' il file e' cambiato, lo rileggono e riprovano;
- non modificano `config/eventi_redazione.yaml`, `config/correzioni.yaml`, i file di memoria condivisi, `docs/`;
  non eseguono `pipeline.pubblica`, non fanno commit ne' push;
- prima di aggiungere un evento controllano che non ci sia gia' (`python -m pipeline.editorial --cerca`), e ogni tanto
  controllano la loro parte con `python -m pipeline.notte --controlla <agente>`;
- rispettano la loro quota di ricerche e finiscono con un messaggio breve: eventi aggiunti, correzioni, ricerche usate.

Come si pubblica senza PC: `python -m pipeline.pubblica` costruisce `docs/data/events.json` con gli eventi gia' sul
sito + `config/eventi_redazione.yaml` + `config/correzioni.yaml`, applica la regola fonti, mette la posizione
(coordinate dell'evento > `config/luoghi.yaml` > centro del comune da `config/comuni.csv`), aggiorna l'archivio e
scrive in `ops/` coda di revisione, campione, posizioni, saturazione e rapporto. Non scarica nulla: tutto cio' che
arriva dal web lo porta Claude come evento della redazione. Gli eventi che non trova sulla mappa (comune scritto male,
frazione, fuori area) finiscono in `ops/senza-posizione.json`: sistemali subito (comune giusto oppure lat e lon).

## Regole (non derogabili)

- **REGOLA FONTI: piattaforme con divieto di scraping** (decisa da Federico il 2026-11-28; vale per ogni fase).
  L'elenco e' `config/fonti-vietate.yaml` (Eventbrite per primo). Prima di aprire qualsiasi link che non sia il sito
  ufficiale di organizzatore, sede, comune, pro loco o ufficio turistico: `python -m pipeline.fonti_vietate --url <link>`.
  - **vietata** o **da verificare** (nel dubbio = vietata): non aprirla, non leggerla, non usarla per scoprire eventi,
    niente endpoint interni, servizi terzi di scraping, proxy, IP a rotazione o user agent falsi, niente testi,
    descrizioni o immagini copiati. Niente ricerche "site:<dominio vietato>". Unica eccezione: l'API ufficiale con
    chiave valida, se elencata in `api`.
  - **Evento che risulta anche su una piattaforma vietata** (visto nei risultati di ricerca, segnalato, citato da
    un'altra fonte): cercalo su fonti ammesse in quest'ordine: sito ufficiale dell'organizzatore, sito della sede o
    del locale, sito del Comune o dell'ente promotore, pro loco e uffici turistici, altre fonti che non vietano
    l'accesso automatico. Verifica che sia lo stesso evento (titolo, data, orario e luogo coincidono). Prendi i dati
    solo dalla fonte ammessa (titolo, data, orario, luogo, prezzo, organizzatore), scrivi un riassunto originale di
    2-3 frasi sui fatti, senza ricalcare struttura ed espressioni dell'originale, e indica la fonte usata (`fonte`:
    il link della pagina letta, oppure nome della fonte e data). Se la fonte ammessa riporta il link di iscrizione o
    biglietteria sulla piattaforma vietata, mettilo solo in `ticket_url` (sul sito diventa "Iscrizioni su ..."),
    senza prendere altro da quella pagina.
  - **Nessuna fonte ammessa**: non pubblicarlo. Va in `ops/da-verificare.json` con titolo, data e motivo per una
    valutazione manuale (contatto con l'organizzatore o API ufficiale). Il codice ce lo mette da solo quando i dati
    vengono da una fonte vietata; `python -m pipeline.editorial --sposta-vietati` sposta li' gli eventi della redazione
    che non rispettano la regola (lo segnala anche `--controlla`).
  - **Fonte nuova** (aggregatore, testata, blog, piattaforma): prima di usarla leggi robots.txt e termini d'uso e
    scrivila in `config/fonti-vietate.yaml`. Finche' non e' verificata vale come vietata. Ogni notte verifica le fonti
    indicate dal piano della notte (`verifiche_fonti` del budget, prima quelle che trattengono piu' eventi in
    `ops/da-verificare.json`): sono gli eventi che possono tornare sul sito.
    **Come si verifica una fonte** (aggiunta da Federico il 2026-11-28): leggi il suo robots.txt e le pagine dei
    termini e condizioni d'uso (anche note legali, privacy o copyright, se i termini non ci sono). Sono le uniche
    pagine di una fonte da verificare che si possono aprire, una volta sola e senza leggere altro del sito.
    - **Nessun divieto trovato** di scraping, crawling, estrazione o raccolta automatica dei dati (degli eventi o in
      generale), di data mining / text and data mining o di riuso automatizzato dei contenuti, e robots.txt che non
      blocca le pagine degli eventi: la fonte e' **valida**. Va in `ammesse` con la data e le pagine lette, es.
      `{dominio: x.it, verificato: AAAA-MM-GG, nota: "robots.txt e /termini letti: nessun divieto"}`.
    - **Divieto trovato** (anche solo per i robot, o per le pagine degli eventi in robots.txt): va in `vietate` con
      il motivo e la frase o la riga che lo dice.
    - **Pagine non leggibili** (WebFetch rifiutato, sito irraggiungibile): resta in `da_verificare`, si riprova un'altra
      notte. Il dubbio vale solo finche' non si sono potute leggere.
  - **Richiesta di rimozione** da un organizzatore o da una piattaforma: rimuovi l'evento (`rimuovi` in
    `config/correzioni.yaml` con motivo "richiesta di rimozione da ... del AAAA-MM-GG") e annota la richiesta in
    `ops/richieste-rimozione.md`.
  - **Tracciabilita'**: per ogni evento pubblicato il codice registra in `ops/prelievi.csv` fonte, URL e data e ora del
    prelievo; per gli eventi della redazione `fonte` e `trovato` sono obbligatori nella pratica: compilali sempre.

- **Solo fatti verificati** su pagine ufficiali (organizzatore, comune, pro loco, teatro) o fonti ammesse dalla
  regola fonti. Mai dedurre o inventare date, orari, prezzi, indirizzi. Nel dubbio non correggere e annotalo nel registro.
- **Riassunti neutri**, 1-2 frasi scritte da te, mai copiate: "L'evento prevede una degustazione di vini locali e
  musica dal vivo." Niente aggettivi promozionali (imperdibile, magico, unico...), niente inviti all'azione.
- **Link d'azione**: ogni evento deve avere `official_url` verso la pagina ufficiale (programma e iscrizioni).
- **Niente dati personali** oltre a quelli necessari a descrivere l'evento (niente telefoni, email, nomi di privati)
  e **nessuna immagine o locandina** presa dalle fonti.
- **Scraping solo come scoperta**: preferisci tanti piccoli siti ufficiali ai grandi portali; rispetta robots.txt e
  frequenze di accesso moderate.
- **Solo eventi specifici**: una singola iniziativa con data e luogo precisi. Calendari, agende, elenchi di eventi,
  pagine di portali, guide ("Calendario eventi e sagre", "Cosa fare nel weekend"...) non sono eventi: rimuovili e,
  se contengono eventi della provincia, estrai i singoli eventi e aggiungili uno per uno. Gli eventi ricorrenti
  (mercatino ogni terza domenica, visite ogni sabato) vanno divisi in date singole; mostre e rassegne con date
  continue restano un evento unico con inizio e fine.
- **Area**: dal 2026-11-28 **tutta Italia** (`area.provinces: ["tutte"]` in `config/settings.yaml`). Treviso resta la
  provincia coperta in profondita' (tutti i comuni, tutte le categorie); le altre 106 province si cercano a rotazione
  (sezione "2b" del piano della notte, ordine in `pipeline/italia.py`). Eventi fuori dall'Italia, conclusi, annullati o
  che non sono eventi: rimuovi. Per i pochi nomi di comune che esistono in due province (Calliano, Castro, Livo,
  Peglio, Samone, San Teodoro) scrivi la sigla nel campo town: "Calliano (TN)".
- **Posizione giusta sulla mappa**: ogni punto deve stare dove si svolge davvero l'evento. Se hai dubbi (solo il
  comune, punto lontano dal centro del comune, luogo con nome generico o omonimo), fai una ricerca: sito
  dell'organizzatore, pagina del luogo, mappe e schede di luoghi (OpenStreetMap, Wikipedia, komoot, siti turistici)
  trovate con WebSearch. Quando trovi le coordinate scrivile in `lat` e `lon` nella correzione, con la `nota` che
  dice da dove vengono. Se non trovi il punto esatto, metti le coordinate del posto piu' vicino che conosci con
  certezza (la piazza, la chiesa o il centro della frazione, il parco, l'ingresso delle mura) e scrivilo nella nota.
  Mai lasciare un evento in un altro comune o in aperta campagna per mancanza di dati.
  Se lo stesso luogo torna in piu' eventi (teatri, parchi, sale civiche), scrivi le sue coordinate verificate in
  `config/luoghi.yaml` (nomi, comune, lat, lon, nota): la pubblicazione le usa per tutti gli eventi presenti e futuri.

## Memoria: impara e migliora ogni notte

La revisione ha una memoria in git, da leggere all'inizio e aggiornare alla fine di ogni notte:
- `ops/segnalazioni-e-controllo.md` - **da leggere per primo**: regole nate dagli errori segnalati da Federico,
  registro delle segnalazioni dal sito e del controllo a campione della qualita'.
- `ops/fonti.yaml` - catalogo delle buone fonti trovate (pagina eventi, ricerca che ci porta dritti, tipo,
  categorie, comuni, ogni quanto ricontrollarla, qualita', resa in eventi). Serve a **non ricercare da capo**:
  le fonti note si riaprono con la loro `query`, senza ricerche esplorative.
- `ops/metodo-ricerca.md` - il **metodo di ricerca consolidato**: regole generali, per regione, per provincia e
  aggregatori validi per piu' province, piu' l'andamento notte per notte (eventi per ricerca). Si migliora ogni notte.
- `ops/categorie-ricerca.md` - l'albero delle categorie di ricerca, sempre piu' in dettaglio (es. Sport >
  Arrampicata > boulder). Si allarga ogni notte con almeno 10 voci nuove.
- `ops/espansione.md` - provincia attiva, criterio di saturazione, test di copertura, ordine delle province
  successive e come aggiungerne una.
- `ops/lezioni.md` - appunti grezzi della notte: cosa funziona e cosa no. Cio' che si conferma passa nel metodo.
- `ops/copertura.yaml` - quando sono stati controllati l'ultima volta comuni e categorie (divisi per provincia:
  `comuni_TV`, `categorie_TV`...), aggregatori, community e testate.
- `ops/saturazione.csv` - scritto da `pipeline.pubblica`: per provincia e per notte, eventi dei prossimi 30 giorni e nuovi trovati.

Regole per spendere meno crediti e migliorare sempre:
- prima le fonti note "in scadenza" secondo la loro `frequenza`, partendo da quelle con qualita' e resa piu' alte;
  salta quelle controllate di recente;
- ogni fonte ricontrollata: aggiorna `ultimo_controllo` e `resa` (eventi nuovi trovati); dopo 3 controlli a zero
  abbassa `frequenza` o metti `stato: debole`; se non e' piu' aggiornata `stato: ferma`;
- se una fonte ha dati strutturati (JSON-LD `Event`, API The Events Calendar, MyPortal) spostala in
  `config/sources.yaml` e segna `stato: spostata`: da quel momento entra nelle "fonti del giro" a rotazione;
- **ogni notte cerca anche fonti nuove** (fase E): quanti candidati dice il budget (`fonti_nuove`), valutali e
  cataloga quelli buoni;
  il catalogo deve crescere notte dopo notte;
- alla fine scrivi in `ops/lezioni.md` cio' che hai imparato (in poche righe) e togli le lezioni superate;
- **ogni notte almeno una miglioria** concreta del metodo (vedi `ops/metodo-ricerca.md`): lo scopo e' trovare piu'
  eventi con meno ricerche e meno AI, notte dopo notte.

**Budget della notte.** Il piano Claude ha limiti di utilizzo condivisi con l'uso di Federico durante il giorno:
la sessione deve stare dentro `ops/budget.yaml` (dal 2026-11-28 piano Max: al massimo 500 ricerche, 100 eventi
della coda, 20 di campione, 20 di test di copertura, 15 fonti del giro...). All'inizio esegui `python -m pipeline.piano_notte`: stampa il piano
della notte (fonti in scadenza, comuni e ambiti delle categorie da cercare, numeri del budget). Per risparmiare:
- **non leggere per intero** i file che crescono (`ops/copertura.yaml`, `ops/fonti.yaml`, `ops/categorie-ricerca.md`,
  `ops/registro-redazione.md`): usa il piano della notte, `grep` o poche righe mirate;
- una pagina che elenca molti eventi vale piu' di molte pagine di un evento: verifica piu' eventi con una sola lettura;
- gli eventi da fonti strutturate affidabili (comuni MyPortal, calendari con JSON-LD) non vanno riverificati uno per uno;
- conta le ricerche mentre lavori e fermati quando arrivi al massimo: prima chiudi registro, memoria e push.

Come dividere il tempo della notte (indicativo):
- circa un terzo alla **manutenzione** di tutte le province gia' coperte: segnalazioni, coda di revisione, controllo
  a campione, fonti note in scadenza;
- circa meta' alla **ricerca nella provincia attiva** (fasi A-E qui sotto);
- il resto a **test di copertura, categorie nuove e miglioria del metodo**.
Se il tempo non basta, salta prima la ricerca esplorativa (fase E), mai la manutenzione.

## Preparazione

```
cd andiamoo && git pull --rebase
pip install --break-system-packages -q -r requirements.txt
```
La shell del cloud non raggiunge i siti degli eventi: per leggere pagine usa WebSearch e WebFetch.
WebFetch apre solo link comparsi nei risultati di WebSearch: se un link della coda viene rifiutato, cerca
"titolo + comune + anno" con WebSearch e apri il risultato giusto. Controlla sempre l'anno: molte pagine
parlano di edizioni passate.
Archivio storico di tutti gli eventi pubblicati, anche passati o tolti: `python -m pipeline.archive --cerca "testo"
[--anno 2026]`. Serve a ritrovare le edizioni degli anni prima (sagre, festival e gare annuali: cerca la nuova
edizione quando si avvicina la data) e a controllare gli eventi con stato `non_piu_presente` (spariti dalle fonti
prima della fine: annullati o spostati?).
Per controllare se un evento e' gia' sul sito senza leggere tutto `docs/data/events.json`:
`python -m pipeline.editorial --cerca "titolo o luogo" --data AAAA-MM-GG` e `--uid <uid>`.
Prima di cercare un comune: `python -m pipeline.editorial --comune "<nome>"` elenca i suoi eventi futuri (sito +
redazione) e le fonti da cui vengono, cosi' non si spende una ricerca su cio' che e' gia' coperto.

## Passi

1. **Rapporto e memoria** - leggi `ops/segnalazioni-e-controllo.md`, `ops/lezioni.md`, `ops/rapporto.json` (scritto
   dall'ultima `pipeline.pubblica`) e `ops/senza-posizione.json`. Il PC non c'e' piu': non segnalarne l'assenza.
2. **Fonti del giro in errore** - se una fonte del giro non si trova o non si apre con WebFetch (indirizzo cambiato,
   pagina vuota, sito fermo): correggi l'indirizzo in `config/sources.yaml` oppure metti `enabled: false` con una
   `note` che spiega il motivo. Non riattivare siti che vietano la raccolta.
2b. **Modulo del sito (Aggiungi evento e Segnala)** - senza PC i due bottoni del sito mandano le risposte al
   **modulo Google** "ANDIAMO? segnalazioni" (`site.form_url` in `config/settings.yaml`, cartella Drive ONOFF >
   _ONOFF Progetti interni > ANDIAMOO). Le risposte sono nel foglio "ANDIAMO? segnalazioni (Risposte)", id
   `18e1sR9iF1jvGAvZeIXMv4d0BwTxDP7YbZAag6oLQ15U`: leggilo con il connettore Google Drive (read_file_content) o Fogli.
   Colonne: data e ora, Tipo ("Nuovo evento", "Correzione", "Rimozione"; "TEST", o titolo che inizia con "TEST", = prova, da ignorare), Evento (uid
   dell'evento segnalato), Dettagli (una riga "Campo: valore" per ogni dato: Titolo, Data, Ora, Fine, Comune, Luogo,
   Indirizzo, Categoria, Accesso, Prezzo, Link, Descrizione, Messaggio), Contatto. Le righe gia' lavorate sono
   quelle con data e ora fino all'ultima registrata in `ops/segnalazioni-e-controllo.md`. Per ogni riga:
   - "Nuovo evento": verifica sul sito ufficiale (regola fonti), poi aggiungilo a `eventi_redazione.yaml` con
     `fonte: "Segnalazione dal sito del AAAA-MM-GG, verificata su <link>"`; se non si trova una fonte ammessa, va in
     `ops/da-verificare.json` (non si pubblica);
   - "Correzione" / "Rimozione": colonna `evento` = uid; verifica e scrivi in `correzioni.yaml`.
   - **Il contatto** (email o telefono) **non va mai nel repository** (e' pubblico): resta solo nel foglio. Nel
     registro scrivi solo data, tipo, titolo ed esito.
   Se il connettore non e' disponibile nella sessione, scrivilo nel messaggio finale ("modulo non letto") e passa
   oltre. Se esiste ancora `ops/segnalazioni.json` con segnalazioni non registrate, gestisci anche quelle.
   Vengono prima della coda: sono errori che qualcuno ha gia' visto.
3. **Coda di revisione** - `ops/revisione.json`, nell'ordine, fino a `coda_max` eventi del budget. Per ognuno apri `sito_ufficiale`
   o `pagina_fonte` (e se serve cerca "titolo comune data"). Scrivi in `config/correzioni.yaml`:
   - `correggi.<uid>`: solo i campi da cambiare tra title, start, end, all_day, summary, category, subcategory,
     access, price, venue, address, town, official_url, ticket_url, audience, setting, lat, lon; aggiungi
     `nota` (da dove viene il dato) e `verificato: AAAA-MM-GG`.
   - `rimuovi.<uid>: "motivo"` per eventi annullati, conclusi, fuori provincia, non-eventi, doppioni (togli quello
     del portale e tieni la fonte diretta).
   - `verificati.<uid>: AAAA-MM-GG` se i dati sono gia' giusti (esce dalla coda).
   Gli eventi con motivo "luogo: solo il comune" o "posizione a N km dal centro" vanno sempre sistemati con `lat`
   e `lon` (vedi la regola "Posizione giusta sulla mappa"); se piu' eventi hanno lo stesso luogo, stesse coordinate.
   Valori ammessi: categorie e accessi di `config/categories.yaml` (access: libero, offerta, biglietto, iscrizione,
   invito); date `AAAA-MM-GG` o `AAAA-MM-GGTHH:MM`; titoli puliti (niente emoji, niente " – Comune (Provincia)").
3b. **Controllo a campione** - gli eventi di `ops/campione.json` (quanti dice il budget): controlla i sei campi come spiegato nella parte 3
   di `ops/segnalazioni-e-controllo.md`, correggi gli errori e scrivi la riga della notte. Se un errore si ripete,
   aggiungi una regola alla parte 1.
3b2. **Controllo delle posizioni** - `ops/posizioni.json`, scritto a ogni pubblicazione (`pipeline/posizioni.py`) su
   tutti gli eventi: allinea da solo gli eventi con solo il comune che nominano un luogo gia' posizionato in
   altri eventi; restano da sistemare, nell'ordine e per luogo (non per evento), quanti dice il budget (`posizioni`):
   `punti_diversi` (stesso luogo con punti diversi), `lontani_dal_comune` (punto probabilmente nel comune sbagliato),
   `senza_punto` (luoghi con un nome ma solo il comune, i piu' frequenti per primi). Per ognuno trova il punto su una
   fonte affidabile e scrivilo in `config/luoghi.yaml` (vale per tutti gli eventi presenti e futuri di quel luogo);
   per un evento singolo usa `lat`/`lon` in `correzioni.yaml`. I `candidati_luoghi` (luoghi con 3+ eventi e punto
   coerente) si aggiungono a `config/luoghi.yaml` dopo un controllo veloce. Nel registro scrivi i numeri del
   riepilogo prima e dopo. Le posizioni non si verificano piu' solo quando qualcuno segnala un errore.
3c. **Test di copertura** - sulla provincia attiva, come spiegato in `ops/espansione.md`: 10 eventi trovati in modo
   indipendente (quanti dice il budget, `test_copertura`), quanti sono gia' sul sito. Ogni lunedi' valuta anche il criterio di saturazione con
   `ops/saturazione.csv` e il registro. Se e' rispettato (criterio confermato da Federico il 2026-10-30),
   aggiungi la provincia successiva seguendo la procedura del file e scrivilo nel riepilogo.
4. **Ricerca degli eventi mancanti** - e' la parte piu' lunga della notte: vedi la sezione "Ricerca degli eventi"
   qui sotto. Nessun limite di numero: aggiungi tutti gli eventi e le iniziative che trovi e verifichi.
5. **Nuove fonti** - da `ops/scoperte.csv` e da quello che trovi: se un sito ufficiale pubblica molti eventi con
   dati strutturati (pagine con JSON-LD `Event`, oppure WordPress The Events Calendar con `/wp-json/tribe/events/v1/events`),
   controlla robots.txt e aggiungilo a `config/sources.yaml` (tipo `jsonld` o `tribe_api`, con `note` e data).
   Vale anche per i siti dei comuni: se un comune usa MyPortal della Regione Veneto (indirizzi con
   `/myportal/C_xxxx/`), aggiungilo come fonte `myportal` con il suo codice IPA, come `comune-treviso`.
   La notte dopo, se il rapporto mostra errori, sistemale o disattivale.
6. **Pulizia** - togli da `correzioni.yaml` ed `eventi_redazione.yaml` le voci di eventi conclusi da piu' di 7 giorni.
   Non si perde nulla: ogni evento pubblicato resta nell'archivio storico (`archivio/AAAA-MM.jsonl`, scritto da
   `pipeline.pubblica`, con le correzioni gia' applicate). Non modificare a mano i file dell'archivio.
7. **Verifica e pubblicazione**
   ```
   python -m pipeline.editorial --controlla      # deve dire "validi"
   python -m pipeline.editorial --doppioni       # doppioni dentro eventi_redazione.yaml e con il sito: togli il meno completo
   python -m pytest -q tests                     # tutti verdi
   python -m pipeline.pubblica --prova           # numeri senza scrivere (senza_posizione deve essere 0)
   python -m pipeline.pubblica                   # pubblica: sito, archivio, coda, campione, posizioni, saturazione
   ```
   (`python -m pipeline.editorial --applica` non serve piu': lo fa `pipeline.pubblica`.)
8. **Registro e memoria** - aggiorna `ops/fonti.yaml`, `ops/lezioni.md`, la riga della notte in
   `ops/metodo-ricerca.md` (andamento e miglioria), le voci nuove in `ops/categorie-ricerca.md` e la riga del test in
   `ops/espansione.md`; poi aggiungi in cima a
   `ops/registro-redazione.md` una sezione `## AAAA-MM-GG` con: fonti del giro lette (raccolta), eventi verificati / corretti /
   rimossi / aggiunti (per categoria), fonti note controllate e loro resa, fonti nuove catalogate, fonti spostate
   in `config/sources.yaml`, problemi aperti per la notte dopo.
   Scrivi anche `ops/riepilogo-notte.json` (storico dei numeri della notte; il resoconto ora e' la notifica di fine
   sessione, vedi la fine del file), sostituendo il contenuto:
   `{"data": "AAAA-MM-GG", "aggiunti": N, "corretti": N, "rimossi": N, "verificati": N,
   "aggiunti_per_categoria": {"musica": N, ...}, "fonti_nuove": N, "fonti_spostate": N, "fonti_sistemate": N,
   "qualita_campione": "N/20", "segnalazioni_gestite": N, "provincia_attiva": "TV", "copertura_test": "N/10",
   "ricerche": N, "eventi_per_ricerca": N.N, "categorie_aggiunte": N, "miglioria": "...", "problemi": ["...", "..."]}` (data di oggi, numeri della notte, al massimo 5 problemi brevi).
9. **Commit e push** su `main` (anche a fine di ogni fase della ricerca): `git add config ops archivio docs/data/events.json`, messaggio
   `Redazione notturna AAAA-MM-GG: N corretti, N rimossi, N aggiunti`, poi `git pull --rebase` e `git push`.
   Se il push fallisce per un conflitto, ripeti pull e push; non forzare mai.

## Ricerca degli eventi

**Resto d'Italia (fase 2b del piano).** Per ogni provincia indicata dal piano: pagina eventi del Comune capoluogo e
dell'ufficio turistico o portale turistico ufficiale (regione, provincia, APT), teatri e musei principali, un ambito
delle categorie ("concerti <provincia> <mese> <anno>"...), e i comuni indicati. Stesse regole (regola fonti, solo
fatti verificati, riassunti originali). Le pagine ufficiali che elencano molti eventi vanno nel catalogo
`ops/fonti.yaml` e, se hanno dati strutturati, in `config/sources.yaml`: cosi' entrano nelle fonti del giro e la
provincia cresce notte dopo notte senza ricercare da capo. Scrivi la data in `copertura.yaml` (`province.<SIGLA>` e
`comuni_<SIGLA>.<Comune>`).

Obiettivo: trovare **tutti** gli eventi e le iniziative pubbliche della **provincia attiva** (`ops/espansione.md`)
che non sono ancora sul sito; nelle province gia' sature basta la manutenzione delle fonti note. Orizzonte:
dal giorno stesso fino a 120 giorni (prima i prossimi 30). Segui l'ordine e i trucchi di `ops/metodo-ricerca.md`
(regole generali, della regione e della provincia). Il file `ops/copertura.yaml` tiene la data dell'ultimo
controllo di ogni comune, aggregatore, testata e categoria: parti sempre da quelli mai controllati o controllati da
piu' tempo, aggiorna la data dopo ogni controllo, aggiungi le voci nuove che scopri (blog, aggregatori, testate).

Fase 0. **Fonti note** - riapri le fonti di `ops/fonti.yaml` in scadenza (vedi "Memoria"), raccogli gli eventi
   nuovi e aggiorna resa e date. Le fasi A-E poi servono a coprire cio' che le fonti note non coprono: usa
   `ops/copertura.yaml` e `ops/lezioni.md` per non ripetere ricerche gia' fatte o inutili.

Fasi, in quest'ordine dopo la fase 0. **Alla fine di ogni fase** esegui `--controlla`, poi commit e push (passo 9), cosi' il lavoro
fatto resta salvato anche se la sessione si interrompe.

A. **Categorie** - usa l'albero di `ops/categorie-ricerca.md`: ogni notte cerca gli ambiti indicati dal piano della
   notte (i meno cercati nella provincia attiva) e dentro ognuno le voci di dettaglio; in `ops/copertura.yaml`
   sezione `categorie_<SIGLA>` scrivi "Macro > Ambito: AAAA-MM-GG", con le parole di ricerca indicate
   e aggiornando la data; segna `rara` le voci senza eventi dopo 3 ricerche. Esempi di query:
   "concerti provincia di Treviso novembre 2026", "sagre Treviso questo weekend", "mostre Treviso 2026",
   "corsa podistica Treviso novembre", "laboratori bambini Treviso", "convegno Treviso", "mercatino Natale Treviso",
   "open day aziende Treviso", "degustazione vini Conegliano Valdobbiadene". Varia comune e periodo.
B. **Comuni** - per ogni comune della provincia attiva (`comuni_<SIGLA>` in `ops/copertura.yaml`; Treviso ne ha 94) cerca la pagina eventi del sito del comune
   ("Comune di <nome> eventi") e della pro loco ("Pro Loco <nome>"), e una ricerca "eventi <nome> <mese> <anno>".
   Lavora i comuni indicati dal piano della notte (i meno recenti), poi altri se resta budget.
C. **Aggregatori e blog** - Pro Loco/UNPLI, teatri, musei, biblioteche e gli aggregatori e blog **ammessi** in
   `config/fonti-vietate.yaml`. Gli aggregatori servono a **scoprire**: il dato va confermato sulla pagina ufficiale
   dell'organizzatore, che diventa `official_url`. Un aggregatore nuovo si usa solo dopo averne letto robots.txt e
   termini d'uso (regola fonti).
   Piattaforme di eventi e biglietteria (Eventbrite, TicketOne, DICE, Xceed, Vivaticket, Fever, TicketSMS, Resident
   Advisor, Meetup, AllEvents...) sono **vietate**: non si aprono e non si cercano con "site:". Se un evento compare li'
   nei risultati di una ricerca generica, si segue la regola fonti: si cerca la fonte ammessa e il link della
   piattaforma va solo in `ticket_url`.
C2. **Community e canali pubblici** - SOSPESA dal 2026-11-28: Telegram (t.me), Instagram, TikTok e Facebook sono
   nell'elenco delle fonti vietate. Le community si cercano solo attraverso il loro sito o la loro pagina su un
   servizio ammesso; il resto di questa fase vale solo per quelle. Testo originale, per quando una piattaforma
   diventasse ammessa: molti aggregatori informali oggi si muovono su social e chat: gruppi di
   trekking ed escursioni indipendenti, run club, community nate su Instagram o TikTok, gruppi di ballo, giochi da
   tavolo, fotografia, volontariato, che pubblicano il calendario delle uscite settimanali su **canali Telegram
   pubblici**. Come cercarli: "site:t.me Treviso trekking", "site:t.me escursioni Veneto", "canale Telegram uscite
   Treviso", "community trekking Treviso Instagram", "run club Treviso", "gruppo camminate <comune>".
   - Canali Telegram pubblici: leggi solo l'anteprima web pubblica `https://t.me/s/<canale>` (se compare nei
     risultati di ricerca; altrimenti cerca "t.me/s/<canale>"). Mai entrare in gruppi privati, mai usare account o
     login, mai copiare nomi, numeri o dati personali dei partecipanti.
   - Instagram, TikTok, Facebook: non aprire pagine che richiedono login. Usa i risultati di ricerca per scoprire la
     community, poi cerca il suo sito, Linktree, canale Telegram pubblico o pagina Meetup/Eventbrite.
   - Aggiungi solo uscite ed eventi **aperti al pubblico** con data, ora, luogo di ritrovo nel trevigiano e modalita'
     di partecipazione (spesso iscrizione: `access: iscrizione`). Come `official_url` usa il post pubblico del canale
     (`https://t.me/<canale>/<numero>`) o la pagina dell'evento; niente link a gruppi chiusi.
   - Ogni canale o community utile va in `ops/fonti.yaml` con `tipo: community` e la `query` per ritrovarla, e in
     `ops/copertura.yaml` nella sezione `community`; quelle inattive o private vanno in `ops/lezioni.md`.
D. **Notizie** - testate locali **ammesse** in `config/fonti-vietate.yaml` (le altre sono da verificare): articoli
   che annunciano eventi, inaugurazioni, festival, gare, presentazioni. Conferma sempre sulla pagina ufficiale quando
   esiste; l'articolo vale come `official_url` solo se la testata e' ammessa.

E. **Fonti nuove** - cerca almeno 10 siti o pagine mai visti che pubblicano eventi in provincia (pro loco, comuni,
   associazioni, locali, teatri, musei, biblioteche, societa' sportive, aziende con eventi aperti, blog e aggregatori
   di nicchia; mai piattaforme vietate). Prima di usarne una leggi robots.txt e termini d'uso e scrivila in
   `config/fonti-vietate.yaml`. Per ognuno valuta: pagina eventi, quanti eventi futuri, se e' aggiornato, se e' ufficiale, se ha dati
   strutturati. Aggiungi a `ops/fonti.yaml` quelli utili (con una `query` che porti dritto alla pagina eventi) e annota
   in `ops/lezioni.md` quelli da evitare. Ogni fonte che rende tanto diventa candidata per `config/sources.yaml`.

Ogni volta che, in qualsiasi fase, trovi una pagina che elenca piu' eventi (non un singolo evento), aggiungila al
catalogo se non c'e' gia'.

Per ogni evento trovato:
- controlla che non sia gia' sul sito (`python -m pipeline.editorial --cerca "titolo" --data AAAA-MM-GG`) ne' gia'
  in `config/eventi_redazione.yaml`; se c'e' ma con dati sbagliati, correggilo (passo 3) invece di aggiungerlo;
- aggiungilo a `config/eventi_redazione.yaml` con title, start (e end se dura piu' giorni), venue, address, town,
  category, access, price, official_url, summary neutro, `fonte` (dove l'hai trovato) e `trovato: AAAA-MM-GG`;
- eventi su piu' giorni con programma diverso ogni giorno: un evento per giorno; mostre e rassegne lunghe: un solo
  evento con start e end;
- eventi ricorrenti (ogni sabato, ogni mese): una voce per ogni data nei prossimi 30 giorni.

Gli eventi aggiunti compaiono sul sito appena esegui `python -m pipeline.pubblica` (passo 7) e fai push.

**Messaggio finale = resoconto del mattino** (arriva a Federico come notifica push, al posto di Telegram).
Scrivilo come ultimo testo della sessione, 4-6 righe, senza trattini lunghi:
"ANDIAMO? notte del GG/MM: N eventi sul sito (N nuovi), N aggiunti, N corretti, N rimossi. Campione N/20.
Fonti del giro lette N, fonti nuove N. Trattenuti dalla regola fonti: N (ops/da-verificare.json).
Modulo: N risposte gestite. Da guardare: ..." (solo problemi veri, al massimo 3).
