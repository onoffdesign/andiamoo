# Agente treviso, notte del 2026-11-28 (secondo giro)

Riscritto da capo. Il primo giro di stanotte (46 eventi, 9 correzioni) e' gia' unito (commit e02a4b7); questo resoconto
copre solo il secondo giro, con i comuni e gli ambiti della parte del piano qui sotto.

## Numeri
- Ricerche usate: 97 su 125 (WebSearch + WebFetch). Letture di PDF fatte in locale con pdftotext sui file che WebFetch
  salva da solo: non contate come ricerche.
- Eventi aggiunti: 36 in config/notte/treviso-eventi.yaml (`python -m pipeline.notte --controlla treviso`: parti valide).
  - sport 12: 10 partite in casa della Rucker San Vendemiano (Serie B Nazionale, Prealpi Sanbiagio Arena di Conegliano,
    dal 6/12 al 27/3), 2 del Villorba Rugby femminile (Serie A Elite, 29/11 e 20/12)
  - teatro-spettacoli 8: 2 del Teatro Accademico di Castelfranco (Fino alle stelle, Paola Minaccioni), 4 del Teatro
    Accademia di Conegliano (Schettini, Giacobazzi, Raffaella! Sognando la Carra'), Raffaella Carra' Show al Del Monaco,
    Boeing Boeing a Trevignano, proiezione di Natale a Villa Panizza (Paese)
  - arte-cultura 5: mostre Human Atlas (Casa Robegan, Treviso), Nataly Maier (OltreArte, Conegliano), La Grotta della
    Cometa (presepi, San Cipriano di Roncade); laboratorio di incisione (Paese); serata di musica sacra a Cordignano
  - famiglie-bambini 5: Pan di zenzero (Zero Branco, Natale con un sorriso), Rudolph Operazione Natale, letture animate,
    laboratorio di Natale, albero con Babbo Natale (Paese)
  - mercatini-fiere 3: mercatino dell'antiquariato di Spresiano (29/11 e 27/12) e di San Zenone degli Ezzelini (20/12)
  - musica 2: concerto di tango Chamberjam Europe al Del Monaco (24/3), concerto di Natale a Castagnole (Paese)
  - sagre-feste 1: accensione dell'albero a Padernello (Paese)
- Comuni con eventi nuovi: Conegliano 15 (10 Rucker), Paese 9, Castelfranco 2, Spresiano 2, Treviso 3, Villorba 2,
  Zero Branco 1, San Zenone 1, Roncade 1, Trevignano 1, Cordignano 1.
- Correzioni: nessuna (config/notte/treviso-correzioni.yaml vuoto).

## Comuni e ambiti cercati (date 2026-11-28 in ops/copertura.yaml)
- comuni_TV: Borso del Grappa, Cappella Maggiore, Castelfranco Veneto, Godega di Sant'Urbano, Mansue', Oderzo, Paese,
  Pieve di Soligo, Ponte di Piave, Refrontolo, Roncade, San Vendemiano, San Zenone degli Ezzelini, Spresiano,
  Trevignano, Treviso, Zero Branco. Non cercati a mano: Resana, Volpago, Vidor, Fregona, Revine Lago, Maser (fonti del
  giro o gia' coperti; Vidor, Fregona e Revine hanno solo eventi di Prosecco Run, Boschi a Natale e Babbo Run).
  Mansue', Ponte di Piave, Cappella Maggiore, Refrontolo e Borso restano a zero: 8 ricerche dedicate senza risultati
  (programmi di Natale non pubblicati, comune di Borso con "Nessun evento in programma").
- categorie_TV, i 12 ambiti del piano: Eventi per chi guarda 12 (Rucker, Villorba rugby); Mercatini 3; Laboratori 3;
  Libri e lettura 1 (letture animate); Danza 0 (seconda ricerca a vuoto: nessuno spettacolo di danza nuovo); Fiere 0
  (solo Sant'Antonio Abate fuori provincia); Ambiente 0 e All'aperto 0 (Parco del Sile "nessuna iniziativa", Oasi
  Cervara chiusa in inverno); Cibo 0; Equitazione 0 (proposta `rara`, terza ricerca senza eventi); Arti marziali 0
  (proposta `rara`, gare FIJLKAM solo a Jesolo e Valeggio); Networking 0 (solo Eventbrite, Business Night di
  Confcommercio a ottobre).
- aggregatori aggiornati: happyticket, iltaccodibacco, trevisoeventi, rete BiblioMarca; aggiunte 6 voci nuove
  (myarteven, calendario regionale dei mercatini, legapallacanestro, federugby, tb.camcom, tvb.bibliotechetrevigiane).

## Fonti nuove da catalogare (30 candidati: nome | url | query | tipo | esito)
Ufficiali e ammesse, con resa:
1. Lega Pallacanestro, scheda Rucker San Vendemiano | https://www.legapallacanestro.com/serie-b/rucker-san-vendemiano | "Rucker San Vendemiano calendario" allowed_domains legapallacanestro.com | sport (lega) | resa 10, tabella con data, ora e avversario. Candidata per il giro (html_llm, una volta al mese).
2. MyArteven, Teatro Accademico Castelfranco 2026/27 | https://www.myarteven.it/rassegne/castelfranco-veneto-teatro-accademico-stagione-20262027 | "Arteven stagione Castelfranco" allowed_domains myarteven.it | circuito teatrale | resa 2 (11 date, 9 gia' sul sito).
3. MyArteven, Natale con un sorriso 2026/27 | https://www.myarteven.it/rassegne/natale-con-un-sorriso-20262027 | stessa query | rassegna per famiglie | resa 1 in TV; 16 spettacoli gratuiti in PD, VE, RO, VI, VR utili all'agente italia.
4. MyArteven, Ragazzi che teatro Castelfranco | https://www.myarteven.it/rassegne/castelfranco-veneto-ragazzi-che-teatro-20262027 | stessa query | teatro ragazzi | resa 0 (gia' coperta).
5. Regione Veneto, calendario dei mercatini dell'antiquariato e del collezionismo 2026 | https://elezioni2020.regione.veneto.it/documents/10713/12114597/Calendario%20mercatini%20usato%202026.pdf/7ca1a502-6de9-4e5e-a247-4ec2f3e6cf3d | "mercatino antiquariato <comune> domenica del mese" | ente (PDF) | resa 3; 48 mercatini in 7 province con giorno della regola, orari e luogo: utile a tutte le province venete.
6. Regione Veneto, calendario dei mercati 2026 | https://elezioni2020.regione.veneto.it/documents/10713/12114597/Calendario+regionale+marcati+2026.pdf/be79e5c1-ceae-4e76-8207-3b49630ae080 | stessa ricerca | ente (PDF) | 110 righe TV, solo mercati settimanali: non sono eventi, utile solo per i mercati contadini.
7. Teatro Del Monaco, programma della stagione lirica e concertistica 2026/27 | https://risorse.teatrostabileveneto.it/hubfs/LIRICA%20E%20CONC%2025-26/Programma%20stagione%202027%20-%20TMDM%202.pdf | "Teatro Mario Del Monaco stagione 2026 2027" | teatro (PDF) | resa 1 (gli altri 10 titoli gia' sul sito).
8. Il Tacco di Bacco, pagine comune (oderzo, treviso, castelfranco-veneto, pieve-di-soligo/spettacoli, treviso/mostre) | https://iltaccodibacco.it/oderzo/ | apertura diretta dopo la verifica | aggregatore ammesso | resa 8 (Human Atlas, Nataly Maier, 4 spettacoli di Conegliano e Treviso).
9. Treviso Eventi, schede comune (paese.html, roncade-san-cipriano-grotta-della-cometa..., calendario) | https://www.trevisoeventi.com/paese.html | allowed_domains trevisoeventi.com | aggregatore ammesso dal giro | resa 11.
10. OltreArte Galleria Contemporanea, Conegliano | https://www.oltrearte.com | "OltreArte Conegliano mostra" | galleria | resa 1; da aprire la prossima volta per il calendario.
11. Fondazione AIDA, produzioni in tournee | https://www.fondazioneaida.it/produzione/rudolph-operazione-natale/ | "Fondazione AIDA date tournee" | compagnia teatro ragazzi | resa 1; ha date anche fuori provincia.
12. FIR, calendario Serie A Elite femminile 2026/27 | https://www.federugby.it/serie-a-elite-femminile-il-calendario-2026-27/ | allowed_domains federugby.it | federazione | resa 2 (solo andata: il ritorno non dice chi gioca in casa).
13. Pro Loco di Roncade | http://www.prolocoroncade.it | "Pro Loco Roncade eventi" | pro loco | citata dalla scheda della Grotta della Cometa, da aprire.
14. Comune di Borso del Grappa, eventi | https://www.comune.borsodelgrappa.tv.it/vivere-il-comune/eventi/ | allowed_domains comune.borsodelgrappa.tv.it | comune (design comuni) | vuoto ora; candidato al giro come html_llm.
15. Comune di Borso del Grappa, calendario annuale delle ricorrenze | https://www.comune.borsodelgrappa.tv.it/calendario/ | stessa | comune | solo regole ("ultima domenica di novembre"), senza anno.
Ufficiali ma non leggibili o vuote:
16. CCIAA Treviso-Belluno, Eventi e convegni | https://www.tb.camcom.gov.it/seminari.asp | allowed_domains tb.camcom.gov.it | ente | 503 a WebFetch (anche /content/14974/.../Eventipremiazioni/); Premio Imprenditoria Femminile il 4/12 da confermare.
17. TVB Biblioteche Trevigiane (SebinaOpac) | https://tvb.bibliotechetrevigiane.it/ | allowed_domains bibliotechetrevigiane.it | rete delle biblioteche | 404 e 503 a WebFetch; le notizie compaiono nei risultati di ricerca (Nervesa, Mogliano, Preganziol, Oderzo).
18. Ascom Confcommercio Treviso, appuntamenti | https://www.ascom.tv.it/appuntamenti/ | allowed_domains ascom.tv.it | associazione | 503.
19. Parco Naturale Regionale del Fiume Sile, iniziative | https://www.parcosile.it/it/iniziative.php | allowed_domains parcosile.it | ente parco | "Nessuna iniziativa in programma".
20. Fondazione Imago Mundi (Gallerie delle Prigioni) | https://fondazioneimagomundi.org/en/progetti/exhibitions/ | "Gallerie delle Prigioni mostra" | fondazione | nessuna mostra in corso.
21. Ca' Foscari, agenda (sede di Treviso) | https://www.unive.it/pag/agenda/ | allowed_domains unive.it | universita' | nessun evento pubblico a Treviso a dicembre.
22. FIJLKAM, gare e risultati | https://www.fijlkam.it/gare-e-risultati.html | "torneo judo karate Treviso" | federazione | nessuna gara in provincia.
23. CAI Conegliano | https://www.caiconegliano.it/ | "CAI Conegliano programma escursioni" | associazione | online solo programmi 2022-2025.
24. Museo Civico di Crocetta del Montello | https://museocivicodicrocettadelmontello.ecomuseoglobale.it/ | uscito in ricerca | museo | non valutato.
25. Selaluna APS, incontri | https://selalunaaps.wixsite.com/selaluna/incontri | uscito in ricerca | associazione culturale | non valutato.
26. Il Veneto Legge | https://ilvenetolegge.it/ | uscito in ricerca | iniziativa regionale di lettura | stagionale (settembre).
27. Museo del Caffe' Dersut, Conegliano | https://www.dersut.it | scheda trevisoeventi | museo d'impresa | "primo sabato del mese", costo contraddittorio: non pubblicato.
28. Calendario Podismo Veneto, pagina ANNO 2027 | https://calendariopodismoveneto.blogspot.com/2025/11/anno-2027.html | allowed_domains calendariopodismoveneto.blogspot.com | aggregatore ammesso | resa 0 (solo titoli, una gara TV gia' sul sito).
Da evitare:
29. Alba Edizioni, eventi e presentazioni | https://www.albaedizioni.it/eventi-e-presentazioni | "presentazione libro Treviso dicembre" | editore | date di anni passati (giorni della settimana sfasati).
30. Happy Ticket /it/treviso/ | https://www.happyticket.com/it/treviso/ | - | biglietteria ammessa | e' l'elenco nazionale (191 mila caratteri, Treviso oltre la fine): inutile; le schede scadute rimandano qui.
Da verificare (non usate): zero.eu, arte.it, artribune.com, oasport.it, ilnordest.it, venetotoday.it (link nei risultati).

Da proporre per le fonti del giro: Rucker San Vendemiano (legapallacanestro), le rassegne TV di MyArteven,
il calendario regionale dei mercatini (una volta all'anno), Comune di Borso del Grappa.

## Voci nuove per ops/categorie-ricerca.md (Macro > Ambito > voce: parole di ricerca)
1. Sport > Eventi per chi guarda > basket di Serie B Nazionale: "Rucker San Vendemiano calendario", "Serie B Nazionale girone A"
2. Sport > Eventi per chi guarda > rugby femminile di Serie A Elite: "Villorba Rugby femminile calendario", "Serie A Elite femminile"
3. Sport > Eventi per chi guarda > partite nei palazzetti di sponsor rinominati: "Prealpi Sanbiagio Arena", "Zoppas Arena"
4. Sport > Arti marziali e combattimento > gare federali FIJLKAM in regione: "FIJLKAM Veneto gare", "campionato regionale judo"
5. Sport > Equitazione > campionati indoor di salto ostacoli: "campionato veneto indoor salto ostacoli", "circolo ippico Casale sul Sile"
6. Mercatini e fiere > Mercatini > calendario regionale dei mercatini d'antiquariato: "calendario mercatini antiquariato Regione Veneto 2026"
7. Mercatini e fiere > Mercatini > mercatini dell'ultima domenica del mese: "mercatino ultima domenica Spresiano"
8. Mercatini e fiere > Mercatini > mercatini della terza domenica: "mercatino terza domenica San Zenone"
9. Mercatini e fiere > Fiere > fiere di Sant'Antonio Abate: "fiera di Sant'Antonio Abate gennaio", "sagra de Sant'Antoni Miane"
10. Arte e cultura > Mostre > fotografia da collezioni private: "mostra fotografia collezione Casa Robegan", "Human Atlas"
11. Arte e cultura > Mostre > gallerie d'arte contemporanea private: "galleria contemporanea Conegliano mostra", "OltreArte"
12. Arte e cultura > Mostre > presepi del mondo nelle chiese antiche: "mostra presepi dal mondo", "Grotta della Cometa San Cipriano"
13. Arte e cultura > Libri e lettura > letture animate di associazioni di lettori: "Letture sPaesate", "letture animate biblioteca Natale"
14. Arte e cultura > Libri e lettura > gruppi di lettura delle biblioteche: "gruppo di lettura biblioteca <comune>"
15. Arte e cultura > Conferenze e incontri > guide all'ascolto musicale: "Un viaggio tra i grandi della musica", "guida all'ascolto Cordignano"
16. Famiglie e bambini > Laboratori > laboratori di incisione e stampa per adulti: "laboratorio di incisione biblioteca adulti"
17. Famiglie e bambini > Laboratori > laboratori di Natale in biblioteca: "laboratorio di Natale biblioteca 5-7 anni"
18. Famiglie e bambini > Spettacoli per bambini > rassegne natalizie del circuito Arteven: "Natale con un sorriso Arteven"
19. Famiglie e bambini > Spettacoli per bambini > produzioni di Fondazione AIDA: "Fondazione AIDA Rudolph", "teatro ragazzi AIDA tournee"
20. Famiglie e bambini > All'aperto > accensioni dell'albero nelle frazioni: "accensione albero Padernello", "elfi e letterine Babbo Natale"
21. Spettacoli > Cinema > film di Natale nei cineforum comunali: "Cineforum Labirinto Natale", "film di Natale auditorium villa"
22. Spettacoli > Teatro > filodrammatiche ospiti nelle rassegne domenicali: "Domenica a teatro Trevignano", "filodrammatica"
23. Spettacoli > Comicita' > divulgazione scientifica a teatro: "Vincenzo Schettini teatro", "show di fisica"
24. Spettacoli > Musical e operetta > tributi a Raffaella Carra': "Raffaella Carra' tribute show", "Sognando la Carra'"
25. Musica e party > Concerti > tango da camera: "concerto di tango Piazzolla", "Chamberjam Europe"

## Miglioria del metodo
**I PDF che WebFetch non legge si leggono per intero in locale.** Quando WebFetch risponde che un PDF e' "binario" o
"compresso", il file e' comunque salvato in tool-results (il percorso e' nella risposta): copiarlo in una cartella della
scratchpad e leggerlo con `pdftotext -layout` costa zero ricerche e da' tutto il documento. Stanotte cosi' il calendario
regionale dei mercatini 2026 (48 mercatini in 7 province, 3 mancanti in TV) e il programma intero della stagione lirica e
concertistica del Del Monaco (21 date, 1 mancante). Regola proposta per ops/metodo-ricerca.md: "PDF illeggibile a
WebFetch = pdftotext sul file salvato, mai una seconda lettura".
Due trucchi minori: (a) le pagine di MyArteven sono lunghe 330-360 mila caratteri di menu, gli spettacoli stanno negli
ultimi 100 mila: aprirle subito con offset = lunghezza meno 100000 (stanotte 3 letture perse senza offset);
(b) ora che Il Tacco di Bacco e' ammesso, la pagina di un comune centrale (iltaccodibacco.it/oderzo/,
/treviso/) elenca in una lettura 22 spettacoli e mostre della provincia fino a marzo: buona per il test di copertura
(19 su 22 erano gia' sul sito) e per le mostre delle gallerie private.

## Lezioni
- Ricerche per comune piccolo senza dominio (Ponte di Piave, Mansue', Borso, Refrontolo, Paese, Pieve di Soligo): 8 ricerche,
  0 eventi. I programmi di Natale di Paese erano invece su trevisoeventi.com/paese.html (8 eventi, una lettura).
- Siti ufficiali in errore 503 a WebFetch: tb.camcom.gov.it, ascom.tv.it, bibliotechetrevigiane.it; SebinaOpac
  (tvb.bibliotechetrevigiane.it) da' 404: per le biblioteche restano i siti dei comuni.
- Le schede scadute di Happy Ticket rimandano a /it/treviso/, che e' l'elenco nazionale: non aprirlo.
- WebSearch su ambiti senza dominio (equitazione, arti marziali, networking, ambiente, danza): 7 ricerche, 0 eventi;
  per lo sport da guardare invece la pagina della squadra sul sito della lega (10 eventi con 2 letture).
- Le notizie dei premi aziendali (Premio Fuoriclasse Castagner) escono il giorno dopo la serata: non aprirle.

## Problemi
- Punti da verificare: Stadio comunale di via Marconi a Villorba (2 partite senza lat/lon, campo dalla voce Wikipedia),
  Biblioteca comunale, Cinema Teatro Manzoni, Villa Panizza e chiesa di Castagnole a Paese (senza coordinate: finiranno sul
  centro del comune), Piazza Rigo (Spresiano) e Piazza Rovero (San Zenone) sul centro del comune, dove stanno le piazze.
- Raffaella Carra' Show: il link TicketOne (da verificare) e' solo in ticket_url, i dati vengono dal Tacco di Bacco.
- Il file config/notte/treviso-eventi.yaml a meta' lavoro e' finito nel commit 5727ab7 del giro: e' la versione
  parziale, quella da unire e' l'attuale.
