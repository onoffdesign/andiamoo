# Registro della redazione notturna

Ogni notte la revisione di Claude aggiunge qui in cima cosa ha fatto (vedi `ops/revisione-notturna.md`).

## 2026-11-02

- **Giro del PC**: NON ha girato stanotte (ultimo rapporto finito il 2026-11-01 alle 01:07). Lavoro sui dati gia'
  pubblicati: coda, campione e rapporto sono quelli di ieri. Fonti a zero nel rapporto di ieri: ticketone, dice,
  qdpnews, gli-alcuni (errore di connessione), biblioteche-treviso: disattivata (robots.txt vieta /myportal/).
- **Segnalazioni dal sito**: nessuna.
- **Coda di revisione** (41 ancora aperte, lavorate circa 32): 21 corretti, 2 rimossi (Domenica Italiana al Botegon
  conclusa; 13a Marcia della Salute doppione di Su l'arden drio la Livenza, tolto anche il doppione in
  eventi_redazione). SiA a Ca' Foscari (9-13, gratuito con registrazione), Fuori copione al Palaverde (19-23),
  6 gare di dicembre con volantino o sito dal Calendario Podismo Veneto, luoghi per Sala Coletti (Santa Caterina),
  Osteria del Django (via Monterumici 11), IC di Roncade (via Vivaldi 30), H-FARM College; titoli ripuliti.
  Restano aperti: accesso dei 4 concerti di Autunno Musicale (le testate non lo dicono), tre eventi di .Ettore,
  Fogliart in Cansiglio (punto di ritrovo e provincia da capire), auditorium di Casale sul Sile, CRM da moku.
- **Controllo a campione**: 7/10 (ricontrollo del campione di ieri dopo le correzioni).
- **Eventi aggiunti** (46): teatro-spettacoli 24, famiglie-bambini 16, musica 3, arte-cultura 2, sagre-feste 1.
  Stagione del Teatro Da Ponte di Vittorio Veneto e sedi TV in tournee (35 date fino a febbraio), Maserada sul Palco
  (4 sabati di novembre), laboratori e visite per famiglie dei Musei Civici (6), Antica Fiera di Santa Lucia (8/11).
- **Comuni controllati**: Vittorio Veneto (Teatro Da Ponte, ottimo), Maser (Pro Loco solo Facebook), Povegliano
  (MyPortal: passato al PC), San Biagio di Callalta (WordPress design-comuni: passato al PC), Loria (MyPortal:
  passato al PC), Refrontolo (Molinetto della Croda senza date 2026/27), piu' Maserada sul Piave.
- **Categorie cercate**: Mercatini (solo guide 2025), Danza (teatro.it in errore), Laboratori (Musei Civici: 6),
  Fiere (Antica Fiera di Santa Lucia). +12 voci nell'albero.
- **Fonti note**: nessuna in scadenza.
- **Fonti nuove catalogate**: 10 (Teatro Da Ponte, Comune di San Biagio, Comune di Povegliano, Comune di Loria,
  trevisoeventi.com, Auditorium Don Vidotto, Visit Museum Treviso, Antica Fiera di Santa Lucia, Pro Loco Vittorio
  Veneto, Il Mosaico Montebelluna; da valutare Hello Mogliano). Spostate in sources.yaml: 5 (teatro-da-ponte,
  comune-san-biagio e comune-castelfranco come html_llm; comune-povegliano C_G944 e comune-loria C_E692 come myportal).
- **Miglioria**: siti con un buon elenco ma senza dati strutturati (tema design-comuni, calendari dei teatri) al PC
  come html_llm, regola nel metodo.
- **Test di copertura**: 2/10. Criterio di saturazione del lunedi': lontano, resta Treviso.
- **Ricerche**: 52 su 70.
- **Per la notte dopo**: controllare nel rapporto le 5 fonti nuove (codici IPA di Povegliano e Loria dedotti dal
  codice catastale; html_llm e doppioni con i 35 eventi Da Ponte gia' in eventi_redazione); confermare su pagine
  ufficiali gli eventi di trevisoeventi mancanti (San Martino a Colle Umberto, Petite Messe a Cusignana, mercatini
  di Portobuffole', Collalto e Roncade, Milipiave, Prealpi in Festa, rassegna di Trevignano); pulizia di
  correzioni.yaml: 15 voci di eventi non piu' sul sito.

## 2026-11-01

- **Giro del PC**: ha girato stanotte (finito alle 01:07, 4,9 minuti, gemma3:12b): 161 eventi sul sito, 60 in
  revisione, 121 nei prossimi 30 giorni. Fonti a zero: ticketone, dice, qdpnews, biblioteche-treviso (0 eventi
  senza errore: forse tipo di contenuto diverso da pnrr_event), gli-alcuni (errore "Server disconnected", forse
  momentaneo). Non toccate stanotte per budget.
- **Segnalazioni dal sito**: nessuna.
- **Coda di revisione** (60, lavorati 30): 18 corretti, 6 verificati, 0 rimossi. Calendario Podismo Veneto:
  orari e link ai volantini per Vertikal del Gevero, Panoramica della Salute, Marcia della Madonna della Salute,
  staffette di cross, Pedemontana in Corsa, Walk in Red. Convegno sul paesaggio con link al Comune di Treviso e
  accesso su iscrizione. Titoli ripuliti per 9 eventi (insolitotrantran, Eventbrite). Confermati sul programma
  4passiFestival e Sile Classica, sagra di Maser (6-21/11), H-FARM a Ca' Tron.
  Restano aperti: Sala Coletti (4passi) e Auditorium dell'IC di Roncade senza indirizzo, Osteria del Django e Area
  Mercato di Maserada senza coordinate, tre eventi di .Ettore a Signoressa (accesso sconosciuto: la pagina eventi
  del sito e' vuota), Domenica Italiana al Botegon (oggi).
- **Controllo a campione**: 3/10 (link 3, accesso 2, orario 1, luogo 1; 3 non verificabili). Corretti Dracula
  all'Edera (link al cinema), La chiamavano Trinita' (ore 12, 28/15 euro), Treviso Sotterranea (link al sito).
- **Eventi aggiunti** (3): sport 1 (Su l'arden drio la Livenza, Albina di Gaiarine, 22/11), mercatini-fiere 2
  (Cose d'Altri Tempi in Borgo Cavour, 27/12 e 24/1).
- **Comuni controllati**: Cappella Maggiore (pagina del Comune in errore), Borso del Grappa, Pieve di Soligo (Comune
  vieta i robot; CAI con uscite per soci), Mansue' (Comune senza eventi futuri), Paese (MyPortal: passato al PC),
  Villorba (Villaggio delle Zucche fino al 2/11 senza pagina ufficiale). Resa quasi zero.
- **Categorie cercate**: Famiglie > All'aperto, Natura > Ambiente, Arte > Libri e lettura, Sagre e cibo > Cibo
  (risultati vecchi o fuori periodo). +10 voci nell'albero.
- **Fonti note**: Fleamapket (2 date confermate del mercatino di Borgo Cavour, resa 2).
- **Fonti nuove catalogate**: 5 (Treviso Sotterranea, Cinema Edera, Libreria San Leonardo, Bardin Garden Store, CAI
  Pieve di Soligo). Spostate in sources.yaml: Comune di Paese (myportal C_G229) e Comune di Maser (myportal C_F009),
  da controllare nel rapporto di domani.
- **Miglioria**: i comuni MyPortal si passano al PC senza ricerche (IPA = C_ + codice catastale), regola nel metodo.
- **Test di copertura**: 5/10.
- **Ricerche**: 55 su 70 (4 sprecate su link non usciti da una ricerca).
- **Per la notte dopo**: controllare comune-paese e comune-maser nel rapporto; biblioteche-treviso a zero;
  Eventbrite: l'accesso resta "sconosciuto" per molti eventi (il PC potrebbe leggere is_free dall'API).

## 2026-10-31

- **Giro del PC**: ha girato stanotte (finito alle 01:13, 3,3 minuti, gemma3:12b): 144 eventi sul sito, 60 in
  revisione, 5 nuovi. Fonti a zero: ticketone (90 secondi, 0 eventi), dice, qdpnews: da guardare.
- **Segnalazioni dal sito**: nessuna.
- **Coda di revisione** (60, lavorati 30): 27 corretti, 2 rimossi (Arredamont e' a Longarone, BL; serata del 30/10
  conclusa), 1 verificato. Sei eventi del 4passiFestival a Santa Caterina confermati sul programma del festival
  (prenotazione), Silent Wifi Concert di Sile Classica (ore 17), 4 gare podistiche confermate sul Calendario Podismo
  Veneto, 10 eventi Eventbrite con la pagina di iscrizione come link, H-FARM a Ca' Tron: posizione giusta.
  Non lavorati per budget gli eventi di stasera (Halloween di 2night) e 30 della coda.
- **Controllo a campione**: 0/10 corretti, errore comune il link (vedi parte 3 e nuova regola in parte 1).
- **Eventi aggiunti** (24): teatro-spettacoli 11, famiglie-bambini 5, arte-cultura 3, musica 3, natura-outdoor 1,
  sagre-feste 1. Stagione di prosa e Ragazzi che Teatro del Teatro Accademico di Castelfranco (13 date fino a
  febbraio), 7 appuntamenti del 4passiFestival, 3 di Sile Classica, sagra della Madonna della Salute di Maser.
- **Comuni controllati**: Castelfranco Veneto (pagina eventi del Comune, ottima), Fregona (visitfregona senza eventi
  futuri), Ponzano Veneto (sito associazioni: solo un evento fuori provincia), Ponte di Piave, Vidor, Revine Lago
  (nessuna pagina utile).
- **Categorie cercate**: Conferenze e incontri, Lavoro (nessun job day TV trovato), Tecnologia e scienza (astrofili
  trevigiani: lezioni pubbliche da riaprire), Spettacoli per bambini (Gli Alcuni). +12 voci nell'albero.
- **Fonti note**: cheventi (errore a WebFetch, 0), sagramap (15 sagre TV di novembre, nessuna confermabile, 0).
- **Fonti nuove catalogate**: 7 (4passiFestival, Sile Classica, Comune di Castelfranco, Gli Alcuni, Biblioteche di
  Treviso, Madonna della Salute di Maser, MyArteven). Spostate in sources.yaml: Gli Alcuni (tribe_api) e Biblioteche
  Comunali di Treviso (myportal C_L407_BIBLIO).
- **Miglioria**: opzione `pagina_iscrizione` per Eventbrite (la pagina dell'evento diventa link d'azione), con test.
- **Test di copertura**: 3/10.
- **Ricerche**: 51 su 70.
- **Problemi aperti per la notte dopo**:
  - Controllare nel rapporto le due fonti nuove (gli-alcuni, biblioteche-treviso): se 0 eventi o errore, sistemarle.
  - 15 sagre TV di novembre (sagramap) senza conferma ufficiale: Prealpi in Festa, San Martino a Vedelago, Moriago e
    Trevignano, San Clemente a Codogne', Costa di Vittorio Veneto, Solighetto...
  - Teatri comunali Arteven della provincia (Conegliano, Mogliano, Oderzo, Vittorio Veneto, Vedelago) da cercare.
  - ticketone a 0 eventi dopo 90 secondi; Million Voices a Bibano e Intima: solo Instagram.

## 2026-10-30

- **Giro del PC**: non ha girato stanotte. L'ultimo rapporto e' del 29/10 alle 19:12 (130 eventi sul sito, 60 in
  revisione). Ho lavorato sui dati gia' pubblicati.
- **Coda di revisione** (60 eventi, lavorati 35): 27 corretti, 2 rimossi, 0 solo verificati.
  - Mercatini ricorrenti divisi in data singola: Badoere di Morgano 1/11 (era "Mordano", periodo apr-dic),
    Godega 15/11, Roncade 14/11 (punto lasciato al centro, via esatta non trovata).
  - Siti ufficiali aggiunti: Trail del Gevero, Corri in Rosa, 6 eventi del Comune di Treviso (pagina del comune).
  - 16 titoli ripuliti (emoji, " - Treviso", titoli giornalistici di 2night).
  - Rimossi 2 eventi conclusi il 29/10.
- **Eventi aggiunti** (13): musica 4, teatro-spettacoli 7, arte-cultura 2. Autunno Musicale 2026 di Musincantus
  (5 appuntamenti + visita alla Biblioteca Capitolare), stagione di prosa del Teatro Accademia di Conegliano
  (6 date, orari non pubblicati), mostra "La materia dei sogni" al Museo di Santa Caterina.
- **Fonti in errore**: TicketOne (0 eventi) passata da /en/cityd/ a /cityd/ e aggiunta Conegliano. DICE e Qdpnews
  (0 eventi) non verificabili: WebFetch non apre i loro link senza un risultato di ricerca.
- **Fonti nuove catalogate**: 13 in ops/fonti.yaml (Musincantus, Teatro Accademia, Musei Civici, Nordest24,
  VenetoToday, cosedicasa, fleamapket, cheventi, Eventi Venetando, sagramap, trevisoinfo, Microturismo,
  TicketOne Conegliano). Spostate in sources.yaml: TicketOne Conegliano (dentro la fonte ticketone).
- **Problemi aperti per la notte dopo**:
  - PC fermo dal 29/10 sera: controllare che il giro delle 01:00 riparta.
  - 25 eventi della coda non lavorati, soprattutto Halloween di 2night del 31/10 (accesso e sito ufficiale) e gare
    di Calendario Podismo senza sito ufficiale.
  - Musincantus: verificare robots.txt e API tribe per passarla al PC.
  - Prealpi in Festa (Cordignano, 4-8 o 4-11 novembre?), San Martino a Mosnigo, Mostra dei vini di Volpago
    (13-28 novembre): date da confermare sui siti dei comuni o delle pro loco prima di aggiungerle.
