# Revisione notturna di Claude

Istruzioni per la sessione Claude pianificata ogni notte (03:37, ora italiana). Arriva dopo il giro del PC fisso
(01:00), che raccoglie gli eventi, li elabora con l'AI locale (Ollama) e lascia in `ops/` il rapporto e la coda
di revisione. Claude fa quello che il modello locale non sa fare bene: verifica sul web, corregge, trova eventi
mancanti e nuove fonti. Ha piena autonomia: corregge, pubblica e aggiunge fonti senza chiedere.

## Regole (non derogabili)

- **Solo fatti verificati** su pagine ufficiali (organizzatore, comune, pro loco, teatro, biglietteria) o fonti
  affidabili. Mai dedurre o inventare date, orari, prezzi, indirizzi. Nel dubbio non correggere e annotalo nel registro.
- **Riassunti neutri**, 1-2 frasi scritte da te, mai copiate: "L'evento prevede una degustazione di vini locali e
  musica dal vivo." Niente aggettivi promozionali (imperdibile, magico, unico...), niente inviti all'azione.
- **Link d'azione**: ogni evento deve avere `official_url` verso la pagina ufficiale (programma e iscrizioni).
- **Niente dati personali** (telefoni, email, nomi di privati) e **niente immagini** copiate.
- **Scraping solo come scoperta**: preferisci tanti piccoli siti ufficiali ai grandi portali; rispetta robots.txt.
- **Solo eventi specifici**: una singola iniziativa con data e luogo precisi. Calendari, agende, elenchi di eventi,
  pagine di portali, guide ("Calendario eventi e sagre", "Cosa fare nel weekend"...) non sono eventi: rimuovili e,
  se contengono eventi della provincia, estrai i singoli eventi e aggiungili uno per uno. Gli eventi ricorrenti
  (mercatino ogni terza domenica, visite ogni sabato) vanno divisi in date singole; mostre e rassegne con date
  continue restano un evento unico con inizio e fine.
- **Area**: solo provincia di Treviso. Eventi fuori provincia, conclusi, annullati o che non sono eventi: rimuovi.
- Coordinate (`lat`, `lon`) solo se lette da un link mappa ufficiale; altrimenti indica luogo e indirizzo e il PC
  geolocalizza al giro successivo.

## Memoria: impara e migliora ogni notte

La revisione ha una memoria in git, da leggere all'inizio e aggiornare alla fine di ogni notte:
- `ops/fonti.yaml` - catalogo delle buone fonti trovate (pagina eventi, ricerca che ci porta dritti, tipo,
  categorie, comuni, ogni quanto ricontrollarla, qualita', resa in eventi). Serve a **non ricercare da capo**:
  le fonti note si riaprono con la loro `query`, senza ricerche esplorative.
- `ops/lezioni.md` - cosa funziona e cosa no: query utili, siti inutili, chi pubblica quando, errori fatti.
- `ops/copertura.yaml` - quando sono stati controllati l'ultima volta comuni, aggregatori, testate e categorie.

Regole per spendere meno crediti e migliorare sempre:
- prima le fonti note "in scadenza" secondo la loro `frequenza`, partendo da quelle con qualita' e resa piu' alte;
  salta quelle controllate di recente;
- ogni fonte ricontrollata: aggiorna `ultimo_controllo` e `resa` (eventi nuovi trovati); dopo 3 controlli a zero
  abbassa `frequenza` o metti `stato: debole`; se non e' piu' aggiornata `stato: ferma`;
- se una fonte ha dati strutturati (JSON-LD `Event`, API The Events Calendar, MyPortal) spostala in
  `config/sources.yaml` e segna `stato: spostata`: da quel momento la legge il PC ogni notte gratis;
- **ogni notte cerca anche fonti nuove** (fase E): almeno 10 candidati mai visti, valutali e cataloga quelli buoni;
  il catalogo deve crescere notte dopo notte;
- alla fine scrivi in `ops/lezioni.md` cio' che hai imparato (in poche righe) e togli le lezioni superate.

## Preparazione

```
cd andiamoo && git pull --rebase
pip install --break-system-packages -q -r requirements.txt
```
La shell del cloud non raggiunge i siti degli eventi: per leggere pagine usa WebSearch e WebFetch.
WebFetch apre solo link comparsi nei risultati di WebSearch: se un link della coda viene rifiutato, cerca
"titolo + comune + anno" con WebSearch e apri il risultato giusto. Controlla sempre l'anno: molte pagine
parlano di edizioni passate.
Per controllare se un evento e' gia' sul sito senza leggere tutto `docs/data/events.json`:
`python -m pipeline.editorial --cerca "titolo o luogo" --data AAAA-MM-GG` e `--uid <uid>`.

## Passi

1. **Rapporto del PC e memoria** - leggi `ops/lezioni.md`, `ops/fonti.yaml` e `ops/rapporto.json`. Se `finito_alle` non e' di stanotte, il PC non ha girato:
   annotalo nel registro (e nel messaggio finale) e lavora sui dati gia' pubblicati.
2. **Fonti in errore** - per le fonti con `errore` o con zero eventi trovati: apri la pagina con WebFetch, correggi
   in `config/sources.yaml` (indirizzi cambiati, mesi, parametri) oppure metti `enabled: false` con una `note` che
   spiega il motivo. Non riattivare siti che vietano la raccolta.
3. **Coda di revisione** - `ops/revisione.json`, nell'ordine, fino a 40 eventi. Per ognuno apri `sito_ufficiale`
   o `pagina_fonte` (e se serve cerca "titolo comune data"). Scrivi in `config/correzioni.yaml`:
   - `correggi.<uid>`: solo i campi da cambiare tra title, start, end, all_day, summary, category, subcategory,
     access, price, venue, address, town, official_url, ticket_url, audience, setting, lat, lon; aggiungi
     `nota` (da dove viene il dato) e `verificato: AAAA-MM-GG`.
   - `rimuovi.<uid>: "motivo"` per eventi annullati, conclusi, fuori provincia, non-eventi, doppioni (togli quello
     del portale e tieni la fonte diretta).
   - `verificati.<uid>: AAAA-MM-GG` se i dati sono gia' giusti (esce dalla coda).
   Valori ammessi: categorie e accessi di `config/categories.yaml` (access: libero, offerta, biglietto, iscrizione,
   invito); date `AAAA-MM-GG` o `AAAA-MM-GGTHH:MM`; titoli puliti (niente emoji, niente " – Comune (Provincia)").
4. **Ricerca degli eventi mancanti** - e' la parte piu' lunga della notte: vedi la sezione "Ricerca degli eventi"
   qui sotto. Nessun limite di numero: aggiungi tutti gli eventi e le iniziative che trovi e verifichi.
5. **Nuove fonti** - da `ops/scoperte.csv` e da quello che trovi: se un sito ufficiale pubblica molti eventi con
   dati strutturati (pagine con JSON-LD `Event`, oppure WordPress The Events Calendar con `/wp-json/tribe/events/v1/events`),
   controlla robots.txt e aggiungilo a `config/sources.yaml` (tipo `jsonld` o `tribe_api`, con `note` e data).
   Vale anche per i siti dei comuni: se un comune usa MyPortal della Regione Veneto (indirizzi con
   `/myportal/C_xxxx/`), aggiungilo come fonte `myportal` con il suo codice IPA, come `comune-treviso`.
   La notte dopo, se il rapporto mostra errori, sistemale o disattivale.
6. **Pulizia** - togli da `correzioni.yaml` ed `eventi_redazione.yaml` le voci di eventi conclusi da piu' di 7 giorni.
7. **Verifica e pubblicazione**
   ```
   python -m pipeline.editorial --controlla      # deve dire "validi"
   python -m pytest -q tests                     # tutti verdi
   python -m pipeline.editorial --applica        # correzioni e rimozioni subito sul sito
   ```
8. **Registro e memoria** - aggiorna `ops/fonti.yaml` e `ops/lezioni.md`, poi aggiungi in cima a
   `ops/registro-redazione.md` una sezione `## AAAA-MM-GG` con: stato del giro del PC, eventi verificati / corretti /
   rimossi / aggiunti (per categoria), fonti note controllate e loro resa, fonti nuove catalogate, fonti spostate
   in `config/sources.yaml`, problemi aperti per la notte dopo.
   Scrivi anche `ops/riepilogo-notte.json` (lo legge il resoconto Telegram delle 07:30), sostituendo il contenuto:
   `{"data": "AAAA-MM-GG", "aggiunti": N, "corretti": N, "rimossi": N, "verificati": N,
   "aggiunti_per_categoria": {"musica": N, ...}, "fonti_nuove": N, "fonti_spostate": N, "fonti_sistemate": N,
   "problemi": ["...", "..."]}` (data di oggi, numeri della notte, al massimo 5 problemi brevi).
9. **Commit e push** su `main` (anche a fine di ogni fase della ricerca): `git add config ops docs/data/events.json`, messaggio
   `Redazione notturna AAAA-MM-GG: N corretti, N rimossi, N aggiunti`, poi `git pull --rebase` e `git push`.
   Se il push fallisce per un conflitto, ripeti pull e push; non forzare mai.

## Ricerca degli eventi

Obiettivo: trovare **tutti** gli eventi e le iniziative pubbliche in provincia di Treviso che non sono ancora sul sito,
dal giorno stesso fino a 120 giorni (prima i prossimi 30). Il file `ops/copertura.yaml` tiene la data dell'ultimo
controllo di ogni comune, aggregatore, testata e categoria: parti sempre da quelli mai controllati o controllati da
piu' tempo, aggiorna la data dopo ogni controllo, aggiungi le voci nuove che scopri (blog, aggregatori, testate).

Fase 0. **Fonti note** - riapri le fonti di `ops/fonti.yaml` in scadenza (vedi "Memoria"), raccogli gli eventi
   nuovi e aggiorna resa e date. Le fasi A-E poi servono a coprire cio' che le fonti note non coprono: usa
   `ops/copertura.yaml` e `ops/lezioni.md` per non ripetere ricerche gia' fatte o inutili.

Fasi, in quest'ordine dopo la fase 0. **Alla fine di ogni fase** esegui `--controlla`, poi commit e push (passo 9), cosi' il lavoro
fatto resta salvato anche se la sessione si interrompe.

A. **Categorie** - per ognuna delle 9 categorie di `config/categories.yaml` (e le sottocategorie: per lo sport
   podismo, ciclismo, nuoto, basket, tennis, volley, calcio amatoriale, trail...) cerca con piu' query, ad esempio
   "concerti provincia di Treviso novembre 2026", "sagre Treviso questo weekend", "mostre Treviso 2026",
   "corsa podistica Treviso novembre", "laboratori bambini Treviso", "convegno Treviso", "mercatino Natale Treviso",
   "open day aziende Treviso", "degustazione vini Conegliano Valdobbiadene". Varia comune e periodo.
B. **Comuni** - per ogni comune di `ops/copertura.yaml` (sono 94) cerca la pagina eventi del sito del comune
   ("Comune di <nome> eventi") e della pro loco ("Pro Loco <nome>"), e una ricerca "eventi <nome> <mese> <anno>".
   Fai piu' comuni possibile, dal meno recente: in pochi giorni devono essere controllati tutti.
C. **Aggregatori e blog** - insolitotrantran, eventiesagre, 2night, zero.eu, itinerarinelgusto, TrevisoToday eventi,
   Oggi Treviso, calendari podistici, Pro Loco/UNPLI, teatri, musei, biblioteche e gli altri della lista, anche di
   nicchia. Cerca anche aggregatori e blog simili che non sono ancora nella lista e aggiungili. Gli aggregatori servono
   a **scoprire**: il dato va confermato sulla pagina ufficiale dell'organizzatore, che diventa `official_url`.
   Piattaforme di eventi e biglietteria da controllare ogni notte, filtrando per provincia di Treviso (e locali e
   comuni della provincia): Meetup, Comehome, Pablo meeter, Wemeet, Fever, TicketSMS, Resident Advisor, DICE, Xceed,
   Vivaticket, TuttiConcerti, Concerti-Italia, Rockol (sezione Concerti), Eventbrite, AllEvents. Cerca con query
   tipo "<piattaforma> Treviso", "site:<dominio> Treviso", "site:<dominio> <comune>". Se un sito blocca i robot o
   richiede l'accesso, usa solo i risultati di ricerca per scoprire l'evento e confermalo sulla pagina ufficiale.
C2. **Community e canali pubblici** - molti aggregatori informali oggi si muovono su social e chat: gruppi di
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
D. **Notizie** - testate locali (Tribuna di Treviso, Gazzettino, TrevisoToday, Oggi Treviso, Qdpnews, tv e radio
   locali): articoli che annunciano eventi, inaugurazioni, festival, gare, presentazioni. Conferma sempre sulla
   pagina ufficiale quando esiste; se c'e' solo l'articolo di una testata affidabile, usalo come `official_url`.

E. **Fonti nuove** - cerca almeno 10 siti o pagine mai visti che pubblicano eventi in provincia (pro loco, comuni,
   associazioni, locali, teatri, musei, biblioteche, societa' sportive, aziende con eventi aperti, blog e aggregatori
   di nicchia, piattaforme di biglietteria, canali Telegram pubblici e community locali). Per ognuno valuta: pagina eventi, quanti eventi futuri, se e' aggiornato, se e' ufficiale, se ha dati
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

Gli eventi aggiunti compaiono sul sito dopo il giro del PC della notte successiva (che li geolocalizza).

Chiudi con un messaggio di 3-5 righe: stato del PC, numeri della notte (eventi aggiunti, fonti nuove nel
catalogo, fonti passate al PC), eventuali problemi da guardare.
