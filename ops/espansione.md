# Espansione per province

ANDIAMO? cresce **una provincia alla volta**. Si lavora su una provincia finche' e' "satura" (gli eventi trovati non
aumentano piu' di tanto), poi si aggiunge la successiva. Le province gia' sature non si abbandonano: restano nel
giro del PC e nella manutenzione notturna, ma la ricerca nuova si concentra sulla provincia attiva.

## Provincia attiva

**Treviso (TV)**, da ottobre 2026.

## Criterio di saturazione

**Criterio confermato da Federico: si', il 2026-10-30** (soglie come scritte qui sotto). Ogni lunedi' Claude
valuta il criterio; quando e' rispettato aggiunge la provincia successiva seguendo la procedura e lo scrive nel
riepilogo. Se Federico cambia le soglie, si aggiornano qui con la data.

Una provincia e' satura quando, **per due settimane di fila**, valgono tutte e quattro:

1. **Copertura**: nel test di copertura (vedi sotto) almeno **9 eventi su 10** trovati in modo indipendente sono
   gia' sul sito. E' la misura principale: dice quanta parte degli eventi reali stiamo gia' prendendo.
2. **Comuni controllati**: tutti i comuni della provincia in `ops/copertura.yaml` controllati almeno **due volte**.
3. **Crescita ferma**: in `ops/saturazione.csv` gli eventi dei prossimi 30 giorni crescono meno del **5% a
   settimana** (contando a parita' di periodo dell'anno: dicembre e l'estate hanno naturalmente piu' eventi).
4. **Qualita'**: controllo a campione (`ops/segnalazioni-e-controllo.md`) corretto almeno al **90%** (9 su 10 col
   piano Pro, 18 su 20 col Max).

Il punto 3 da solo non basta: nuovi eventi vengono pubblicati ogni giorno, quindi il numero non si ferma mai del
tutto. Per questo conta soprattutto il test di copertura.

### Test di copertura (ogni notte, sulla provincia attiva)

1. Scegli 10 eventi **in modo indipendente dal sito**: il primo evento dei prossimi 30 giorni trovato con 10
   ricerche diverse, variando comune (estratto a caso da `ops/copertura.yaml`) e categoria (da
   `ops/categorie-ricerca.md`). Non usare fonti gia' in `config/sources.yaml`: il test deve misurare cio' che ci
   sfugge.
2. Per ognuno: `python -m pipeline.editorial --cerca "titolo" --data AAAA-MM-GG`. Trovato o no.
3. Quelli mancanti si aggiungono come eventi nuovi (il test serve anche alla ricerca).
4. Scrivi la riga nel registro qui sotto.

## Ordine delle province

Regola: la prossima provincia e' quella **confinante** con l'area gia' coperta e con **piu' abitanti**, finendo prima
tutta la regione. Poi la regione confinante. Ordine delle regioni: Veneto, Friuli-Venezia Giulia, Trentino-Alto
Adige, poi Nord Italia (Lombardia, Emilia-Romagna, Piemonte, Liguria, Valle d'Aosta), poi Centro (Toscana,
Marche, Umbria, Lazio), poi Sud e isole (Abruzzo, Molise, Campania, Puglia, Basilicata, Calabria, Sicilia,
Sardegna). Prima di scegliere, verifica gli abitanti sul sito ISTAT (demo.istat.it): le cifre qui sotto sono
indicative.

Ordine previsto (si ricalcola a ogni passaggio):

| # | Provincia | Regione | Abitanti (indicativi) | Perche' adesso | Stato |
|---|---|---|---|---|---|
| 1 | Treviso (TV) | Veneto | ~880.000 | partenza | attiva |
| 2 | Padova (PD) | Veneto | ~935.000 | confina con TV, la piu' popolosa | in attesa |
| 3 | Verona (VR) | Veneto | ~930.000 | confina con PD | in attesa |
| 4 | Vicenza (VI) | Veneto | ~850.000 | confina con TV, PD, VR | in attesa |
| 5 | Venezia (VE) | Veneto | ~835.000 | confina con TV, PD | in attesa |
| 6 | Rovigo (RO) | Veneto | ~225.000 | confina con PD, VR, VE | in attesa |
| 7 | Belluno (BL) | Veneto | ~200.000 | confina con TV, VI | in attesa |
| 8 | Udine (UD) | Friuli-Venezia Giulia | ~515.000 | confina con VE, BL | in attesa |
| 9 | Pordenone (PN) | Friuli-Venezia Giulia | ~310.000 | confina con TV, VE, BL, UD | in attesa |
| 10 | Gorizia (GO) | Friuli-Venezia Giulia | ~140.000 | confina con UD | in attesa |
| 11 | Trieste (TS) | Friuli-Venezia Giulia | ~230.000 | confina con GO | in attesa |
| 12 | Trento (TN) | Trentino-Alto Adige | ~545.000 | confina con VI, VR, BL | in attesa |
| 13 | Bolzano (BZ) | Trentino-Alto Adige | ~535.000 | confina con TN, BL | in attesa |

Quando Italia e' tutta coperta, si continua solo a migliorare metodo (`ops/metodo-ricerca.md`) e categorie
(`ops/categorie-ricerca.md`).

## Come si aggiunge una provincia

Solo quando il criterio di saturazione e' rispettato. Nella stessa notte:
1. `config/settings.yaml`: aggiungi la sigla in `area.provinces` (es. `["Treviso", "PD"]`) e allarga `area.bbox`
   perche' contenga anche la nuova provincia; aggiorna `site.tagline`, `site.center` e `site.zoom` per l'area intera.
2. `docs/index.html`: aggiorna la descrizione del sito (oggi dice "provincia di Treviso").
3. `ops/copertura.yaml`: aggiungi la sezione dei comuni della nuova provincia (elenco completo dal sito ISTAT o dalla
   Regione), tutti a `null`.
4. `ops/metodo-ricerca.md`: aggiungi la sezione della provincia, partendo da regole generali e regionali; aggiungi
   le pagine della nuova provincia agli aggregatori multi-provincia gia' noti (sezione 4).
5. `config/sources.yaml`: allarga le fonti multi-provincia (pagine citta' di TicketOne, running.life, eventiesagre...).
6. Aggiorna la tabella qui sopra (stato e data) e scrivi la decisione nel registro.
7. Verifica: `python -m pipeline.editorial --controlla` e `python -m pytest -q tests` tutti verdi, poi commit.

Il carico cresce con ogni provincia: se il giro del PC supera le 2 ore o la revisione notturna non riesce piu' a
finire coda e manutenzione, segnalalo nei `problemi` del riepilogo prima di aggiungere altre province.

## Registro

Test di copertura e decisioni, una riga per notte (la piu' recente in alto):
`- AAAA-MM-GG · TV · copertura 7/10 (mancanti: ...) · eventi prossimi 30 giorni N (settimana +N%) · comuni controllati 2 volte N/94`

- 2026-10-31 · TV · copertura 3/10 (mancanti: 2 incontri del 4passiFestival, lettura animata di Sile Classica, 2 spettacoli del Teatro Accademico di Castelfranco, sagra Madonna della Salute di Maser, letture in biblioteca a Castelfranco; aggiunti tutti tranne l'ultimo) · eventi prossimi 30 giorni 123 · comuni controllati 2 volte 0/94 · lontana dalla saturazione: mancano teatri comunali e sagre
