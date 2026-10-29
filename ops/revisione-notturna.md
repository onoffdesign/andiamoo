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
- **Area**: solo provincia di Treviso. Eventi fuori provincia, conclusi, annullati o che non sono eventi: rimuovi.
- Coordinate (`lat`, `lon`) solo se lette da un link mappa ufficiale; altrimenti indica luogo e indirizzo e il PC
  geolocalizza al giro successivo.

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

1. **Rapporto del PC** - leggi `ops/rapporto.json`. Se `finito_alle` non e' di stanotte, il PC non ha girato:
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
8. **Registro** - aggiungi in cima a `ops/registro-redazione.md` una sezione `## AAAA-MM-GG` con: stato del giro
   del PC, eventi verificati / corretti / rimossi / aggiunti (per categoria), comuni e aggregatori controllati,
   fonti cambiate, problemi aperti per la notte dopo.
9. **Commit e push** su `main` (anche a fine di ogni fase della ricerca): `git add config ops docs/data/events.json`, messaggio
   `Redazione notturna AAAA-MM-GG: N corretti, N rimossi, N aggiunti`, poi `git pull --rebase` e `git push`.
   Se il push fallisce per un conflitto, ripeti pull e push; non forzare mai.

## Ricerca degli eventi

Obiettivo: trovare **tutti** gli eventi e le iniziative pubbliche in provincia di Treviso che non sono ancora sul sito,
dal giorno stesso fino a 120 giorni (prima i prossimi 30). Il file `ops/copertura.yaml` tiene la data dell'ultimo
controllo di ogni comune, aggregatore, testata e categoria: parti sempre da quelli mai controllati o controllati da
piu' tempo, aggiorna la data dopo ogni controllo, aggiungi le voci nuove che scopri (blog, aggregatori, testate).

Fasi, in quest'ordine. **Alla fine di ogni fase** esegui `--controlla`, poi commit e push (passo 9), cosi' il lavoro
fatto resta salvato anche se la sessione si interrompe.

A. **Categorie** - per ognuna delle 15 categorie di `config/categories.yaml` (e le sottocategorie: per lo sport
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
D. **Notizie** - testate locali (Tribuna di Treviso, Gazzettino, TrevisoToday, Oggi Treviso, Qdpnews, tv e radio
   locali): articoli che annunciano eventi, inaugurazioni, festival, gare, presentazioni. Conferma sempre sulla
   pagina ufficiale quando esiste; se c'e' solo l'articolo di una testata affidabile, usalo come `official_url`.

Per ogni evento trovato:
- controlla che non sia gia' sul sito (`python -m pipeline.editorial --cerca "titolo" --data AAAA-MM-GG`) ne' gia'
  in `config/eventi_redazione.yaml`; se c'e' ma con dati sbagliati, correggilo (passo 3) invece di aggiungerlo;
- aggiungilo a `config/eventi_redazione.yaml` con title, start (e end se dura piu' giorni), venue, address, town,
  category, access, price, official_url, summary neutro, `fonte` (dove l'hai trovato) e `trovato: AAAA-MM-GG`;
- eventi su piu' giorni con programma diverso ogni giorno: un evento per giorno; mostre e rassegne lunghe: un solo
  evento con start e end;
- eventi ricorrenti (ogni sabato, ogni mese): una voce per ogni data nei prossimi 30 giorni.

Gli eventi aggiunti compaiono sul sito dopo il giro del PC della notte successiva (che li geolocalizza).

Chiudi con un messaggio di 3-5 righe: stato del PC, numeri della notte, eventuali problemi da guardare.
