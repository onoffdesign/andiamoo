# Agente italia, notte del 2026-11-28

## Esito
Lavoro interrotto su indicazione del coordinatore: WebFetch e' bloccato dalla rete della sessione
(errore `getaddrinfo ENOTFOUND` su padovacultura.padovanet.it e su www.comune.verona.it). I riassunti di
WebSearch non valgono come dati verificati, quindi nessun evento pubblicato.

- Eventi aggiunti: 0 (tutte le 10 province: PD, VR, VI, VE, RO, BL, UD, PN, TS, GO)
- Correzioni, rimozioni, verificati: 0
- Ricerche usate: 6 su 125 (3 WebSearch, 3 WebFetch falliti)
- ops/copertura.yaml non toccato: nessuna provincia o comune e' stato davvero controllato, le date restano "mai".
- Controllo preliminare: `python -m pipeline.editorial --comune` dice 0 eventi futuri e nessuna fonte per tutti i 40
  comuni assegnati (capoluoghi compresi). Tutti presenti in config/comuni.csv.

## Fonti nuove da catalogare (scoperte nei risultati di WebSearch, non lette)
Tutte siti ufficiali di Comuni o uffici turistici; da aprire quando WebFetch torna a funzionare.
- Padova Cultura (Comune di Padova) | https://padovacultura.padovanet.it/it/manifestazioni | query: "Padova eventi dicembre 2026 agenda" con allowed_domains padovanet.it | tipo: comune | PD | dati strutturati: non verificato. Ha anche un calendario mensile /it/calendar/month/AAAA-MM e la pagina "Natale a Padova 2026" (/it/attivita-culturali/natale-padova-2026).
- Comune di Verona, Eventi | https://www.comune.verona.it/Vivere-il-comune/Eventi/ | query: "Comune di Verona eventi dicembre 2026 Natale programma" con allowed_domains comune.verona.it, visitverona.it | tipo: comune | VR | dati strutturati: non verificato (schede per evento, es. /Eventi/Mercatini-di-Natale-2026).
- Visit Verona (ufficio turistico) | https://www.visitverona.it/it/eventi/ | stessa query | tipo: ufficio turistico | VR | dati strutturati: non verificato.

## Eventi visti solo nei riassunti di WebSearch (da confermare su fonte, non pubblicati)
- Padova: Villaggio di Natale agli Eremitani (27/11/2026-06/01/2027), Fiera di Natale in centro (dal 05/12/2026), Cantanatale (20/12/2026, piazzetta Pedrocchi, ora non indicata), 800 Padova Festival (03-08/12/2026), Predatori di pianura di Andrea Pennacchi al Teatro Verdi (15-20/12/2026), pista di ghiaccio in Prato della Valle (fino al 24/01/2027).
- Verona: Mercatini di Natale in Piazza Bra e Piazza dei Signori (dal 21/11/2026; fine 27 o 28/12 secondo la fonte: date contraddittorie), Oratorio di Natale di Bach nel Duomo (19/12/2026 ore 20:30, prenotazione), Adigeo Verona Christmas Run (20/12: il riassunto dice "sabato", ma il 20/12/2026 e' domenica, quindi forse pagina 2025).

## Regole di metodo proposte (ops/metodo-ricerca.md)
- Veneto, Padova: la ricerca con allowed_domains padovanet.it e l'anno porta dritto a padovacultura.padovanet.it (pagina del Natale e manifestazioni): partire da li'.
- Veneto, Verona: allowed_domains comune.verona.it e visitverona.it danno le schede del Comune e dell'ufficio turistico; controllare il giorno della settimana per riconoscere le pagine dell'anno prima.

## Problemi
- WebFetch non risolve i domini (ENOTFOUND): la rete della sessione va aperta ai siti esterni prima della prossima notte, altrimenti la fase 2b non si puo' fare.
