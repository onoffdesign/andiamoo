# Registro della redazione notturna

Ogni notte la revisione di Claude aggiunge qui in cima cosa ha fatto (vedi `ops/revisione-notturna.md`).

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
