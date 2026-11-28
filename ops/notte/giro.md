# Agente giro, notte del 2026-11-28

## Numeri
- Eventi aggiunti: 0. Correzioni: 0.
- Ricerche usate: 5 su 125 (3 WebSearch, 2 WebFetch).
- Fonti del giro lette: 0 su 40. Sezione `giro` di ops/copertura.yaml non aggiornata (nessuna fonte letta davvero).
- Verifiche delle fonti: 0 ammesse, 0 vietate, 12 restano in `da_verificare` (nessuna pagina leggibile).

## Problema bloccante
WebFetch in questa sessione non raggiunge i siti: due domini diversi danno lo stesso errore
"getaddrinfo ENOTFOUND ... outside the session's allowed network domains":
- www.libreriasanleonardo.it (fonte libreria-san-leonardo, /notes)
- www.comunemoglianoveneto.it (fonte comune-mogliano, home; il dominio esiste: compare nei risultati di WebSearch)
Come chiede il messaggio d'errore, dopo il secondo dominio non ho provato altri siti. I domini vanno consentiti
nelle impostazioni di rete della sessione (o va usata una sessione con rete web aperta), poi il giro si puo' rifare.
Senza WebFetch non si possono leggere ne' le pagine eventi del giro ne' robots.txt e termini delle 12 fonti da
verificare; i riassunti di WebSearch non sono una lettura della pagina ufficiale e non li ho usati come dati.

## Fonti del giro
Nessuna letta. Nessuna fonte disattivata o modificata in config/sources.yaml: l'errore e' della rete della sessione,
non dei siti. Nota a margine: la ricerca "Comune di Mogliano Veneto eventi dicembre 2026" (anche con allowed_domains
comunemoglianoveneto.it) da' solo allegati MyPortal di anni passati (2023-2025), nessun programma del Natale 2026.

## Verifiche (12)
trevisoeventi.com, ticketone.it, umbriaecultura.it, calendariopodismo.it, trovasagre.com, classicalive.it,
insolitotrantran.it (comunque in domini-illeggibili), itinerarinellarte.it, happyticket.com, running.life,
tviweb.it, eventiesagre.it: tutte restano da verificare, config/fonti-vietate.yaml non toccato.

## Fonti nuove da catalogare
Nessuna.

## Lezioni
- Prima di partire con il giro provare una sola WebFetch: se da' ENOTFOUND "outside the session's allowed network
  domains", la sessione non ha rete web e il giro va rimandato (non disattivare le fonti).
- WebSearch generica "Libreria San Leonardo Treviso presentazioni" esce solo su libreriauniversitaria.it: serve
  allowed_domains libreriasanleonardo.it.
