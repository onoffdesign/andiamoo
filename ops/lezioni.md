# Lezioni della revisione notturna

Quello che Claude impara notte dopo notte su come trovare eventi in provincia di Treviso con meno ricerche:
query che funzionano, siti che non servono, periodi in cui certe fonti pubblicano, errori da non ripetere.
Si legge all'inizio di ogni notte; si aggiorna alla fine (aggiungi, correggi, togli cio' che non vale piu').
Tienila breve: al massimo ~80 righe, raggruppate per tema.

## Ricerche che funzionano
- Per gruppi di eventi Eventbrite nello stesso luogo (es. 6 a Santa Caterina) cercare i titoli insieme: esce il
  festival che li organizza e il suo programma verifica tutto con 2-3 letture.
- Calendario Podismo Veneto (pagina del mese) conferma in una lettura orari e distanze di tutte le gare TV.
- WebSearch "standard" rende poco sui siti locali (risultati USA): per comuni, rassegne e teatri usare "extended".
- WebFetch apre solo link comparsi nei risultati: i link della coda (comune.treviso.it, 2night, eventiesagre) vanno
  prima fatti uscire con una ricerca mirata (titolo + comune + anno).
- Rassegne con programma su sito WordPress (es. musincantus.it): la pagina /eventi/elenco/?tribe-bar-search=<comune>
  da' tutte le date con indirizzo in una volta.
- Mercatini ricorrenti: le schede cosedicasa.com indicano la regola (seconda/terza domenica), le sospensioni e la
  prossima data; servono per dividere in date singole.

## Fonti da evitare o poco utili
- distrettolaghi.it e' il Lago Maggiore (Piemonte), non il Lago di Revine: inutile.
- cheventi.it e arteven.it/pr/treviso danno errore a WebFetch; Eventbrite non si apre senza un risultato di ricerca.
- eventivenetando ed eventiesagre per le sagre spesso mostrano l'edizione di anni passati: controllare l'anno.
- deliziedautunno.tv e cultura.gov.it vietano i robot: non aprirli, usarli solo come titolo nei risultati.
- trevisotoday.it da' errore a WebFetch; venetotoday.it invece si apre.
- microturismodellevenezie.it ha date contraddittorie nella stessa scheda: mai usarla come conferma.

## Calendario (chi pubblica quando)
- Teatri comunali: le stagioni 2026/27 escono a fine ottobre con vendite da inizio novembre (Castelfranco).
- Sagre di San Martino e Madonna della Salute: tutte a novembre, quasi solo su Facebook e aggregatori.

## Errori da non ripetere
- eventiesagre a volte sbaglia il nome del comune (Badoere di Morgano scritto "Mordano", poi geocodificato a caso):
  leggere la scheda prima di rimuovere come "fuori provincia".
- Nel modificare correzioni.yaml con script, l'intestazione commentata contiene "# rimuovi:": inserire le voci
  prima della riga "rimuovi:" che inizia a capo, non della prima occorrenza.
- In correzioni.yaml le date senza ora vanno tra virgolette ("2026-11-01"): altrimenti --applica si blocca
  (TypeError nel sort) anche se --controlla le dice valide.
