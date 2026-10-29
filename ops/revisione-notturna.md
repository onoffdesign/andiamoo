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
4. **Eventi mancanti** - cerca eventi dei prossimi 21 giorni in provincia di Treviso (comuni, pro loco, teatri,
   musei, biblioteche, sagre, sport amatoriale, eventi aziendali aperti). Le notizie servono a scoprirli, la conferma
   va presa dalla pagina ufficiale. Controlla che non siano gia' sul sito (`--cerca`). Aggiungine fino a 20 in
   `config/eventi_redazione.yaml` (campi in `pipeline/collectors/redazione.py`; obbligatori title, start, town,
   official_url; summary neutro; `trovato: AAAA-MM-GG`). Compaiono sul sito dopo il giro del PC della notte dopo.
5. **Nuove fonti** - da `ops/scoperte.csv` e da quello che trovi: se un sito ufficiale pubblica molti eventi con
   dati strutturati (pagine con JSON-LD `Event`, oppure WordPress The Events Calendar con `/wp-json/tribe/events/v1/events`),
   controlla robots.txt e aggiungilo a `config/sources.yaml` (tipo `jsonld` o `tribe_api`, con `note` e data).
   Al massimo 3 per notte; la notte dopo, se il rapporto mostra errori, sistemale o disattivale.
6. **Pulizia** - togli da `correzioni.yaml` ed `eventi_redazione.yaml` le voci di eventi conclusi da piu' di 7 giorni.
7. **Verifica e pubblicazione**
   ```
   python -m pipeline.editorial --controlla      # deve dire "validi"
   python -m pytest -q tests                     # tutti verdi
   python -m pipeline.editorial --applica        # correzioni e rimozioni subito sul sito
   ```
8. **Registro** - aggiungi in cima a `ops/registro-redazione.md` una sezione `## AAAA-MM-GG` con: stato del giro
   del PC, eventi verificati / corretti / rimossi / aggiunti, fonti cambiate, problemi aperti per la notte dopo.
9. **Commit e push** su `main`: `git add config ops docs/data/events.json`, messaggio
   `Redazione notturna AAAA-MM-GG: N corretti, N rimossi, N aggiunti`, poi `git pull --rebase` e `git push`.
   Se il push fallisce per un conflitto, ripeti pull e push; non forzare mai.

Chiudi con un messaggio di 3-5 righe: stato del PC, numeri della notte, eventuali problemi da guardare.
