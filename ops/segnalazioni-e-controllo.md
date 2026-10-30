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

## 2. Segnalazioni dal sito

Il PC esporta ogni notte in `ops/segnalazioni.json` le segnalazioni degli ultimi 30 giorni (mai i contatti di chi
scrive). Per ognuna non ancora presente qui sotto: verifica sulla fonte ufficiale, poi correggi o rimuovi in
`config/correzioni.yaml`, oppure annota perche' non serve. Se lo stesso tipo di errore torna, aggiungi una regola
alla parte 1.

Formato: `- AAAA-MM-GG · segnalazione #id · uid · cosa diceva (in breve) · cosa e' stato fatto`

(nessuna segnalazione registrata finora)

## 3. Controllo a campione

Il PC sceglie ogni notte N eventi a caso dei prossimi 30 giorni (N = `campione` in `ops/budget.yaml`) (`ops/campione.json`, sempre gli stessi per la
stessa data). Per ognuno apri la fonte ufficiale e controlla sei campi: **data**, **orario**, **luogo** (punto sulla
mappa compreso), **accesso e prezzo**, **categoria**, **link ufficiale** (funziona e porta all'evento giusto).
Un evento e' "corretto" solo se tutti e sei sono giusti. Gli errori trovati si correggono subito come nel passo 3.

Formato (una riga per notte, la piu' recente in alto):
`- AAAA-MM-GG · corretti N/10 · errori: data N, orario N, luogo N, accesso N, categoria N, link N · lezione: ...`

Obiettivo: almeno il 90% stabile. Se una notte scende sotto l'80%, la causa principale va scritta nella parte 1 e
segnalata nei `problemi` del riepilogo.

(nessun controllo registrato finora)
