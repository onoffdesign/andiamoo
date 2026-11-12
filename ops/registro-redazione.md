# Registro della redazione notturna

Ogni notte la revisione di Claude aggiunge qui in cima cosa ha fatto (vedi `ops/revisione-notturna.md`).

## 2026-11-12

- **Giro del PC**: NON ha girato stanotte (ultimo rapporto finito il 2026-11-11 alle 09:19, giro a mano dopo cinque
  notti ferme; 428 eventi sul sito, 60 in coda). Il giro dell'11/11 ha rinnovato coda, campione e posizioni ma e' stato
  fatto prima del codice nuovo delle posizioni (luoghi.yaml, frazioni): i 51 eventi con solo il comune si
  ricalcolano al prossimo giro. Correzioni applicate con --applica (sito a 428 eventi, 120 correzioni applicate).
- **Fonti in errore**: non riaperte (rapporto dell'11/11 da guardare con il giro nuovo).
- **Segnalazioni dal sito**: nessuna.
- **Coda di revisione** (24 eventi lavorati su 60): 17 corretti, 0 rimossi, 15 verificati. Mattorosso: ora e ingresso
  di Spreafico (doppione del vecchio uid con luogo e link), Noche Reggaeton (22, gratuito +18), Cindy & The Rock History
  (22, 12 euro con drink), karaoke (22, gratuito). Fondentemente (accesso libero, link Confartigianato), firmacopie Ubik
  (fino alle 18:30), Mogliano-Viadana (biglietto, Via Colelli 2, Ciaotickets), Palio delle Botti (aperto a tutti),
  Festival del Radicchio di Paderno (link Fiori d'Inverno al posto di un sito umbro), Giornate Martiniane al Museo della
  Battaglia (indirizzo), Villa Freya (Via Forestuzzo), 6 serate della Sagra del Frico (salone dietro la chiesa).
  Verificate come periodo continuo 8 mostre lunghe, le 4 repliche di Alcesti, 2 presentazioni Ubik, il talk H-FARM.
  Restano aperti: sagre di Sarano, Musano, Villanova e Camalo' (accesso non pubblicato, posizione dalla frazione al
  prossimo giro), eventi di Sernaglia e Silea senza scheda, Autunno Sanfiorese (calendario solo nel PDF), Mostra dei
  vini del Montello (solo siti vietati), Segusino, Zero Branco.
- **Controllo a campione**: 4/10 (vedi segnalazioni-e-controllo).
- **Posizioni**: prima 0 punti diversi, 0 lontani, 51 con luogo senza punto, 25 candidati; aggiunti 17 luoghi noti a
  config/luoghi.yaml dai candidati (teatri Del Monaco, Accademia, Da Ponte, Accademico, Damiano Chiesa, Palaverde,
  Mattorosso, Monigo, Quaggia, Santa Caterina, Bailo, Ubik, Palazzo Foscolo, Storga, Comisso, Vicinalis, Lorenzaga) e
  2 indirizzi (Villa Freya, Museo della Battaglia). I numeri dopo li dara' il prossimo giro del PC.
- **Eventi aggiunti** (10): sagre-feste 7 (Festa di San Martino a Santa Maria del Sile 13, 14, 15/11; Festa di Santa
  Caterina a Barbisano 20, 21, 22, 25/11), musica 2 (Salotto Musicale a Onè di Fonte: Chopin 14/11, Bach 21/11),
  arte-cultura 1 (I 98 eroi dell'Austria alla Ubik, 25/11).
- **Comuni controllati**: San Polo di Piave, Cornuda, Chiarano, Fonte (passati al PC), San Zenone degli Ezzelini (solo
  portali nei risultati), Mareno di Piave (home MyPortal senza eventi).
- **Categorie cercate**: Sport di precisione, Arrampicata, Montagna ed escursionismo (resa 0: CAI Treviso con schede
  ancora vuote), Sagre (TrovaSagre: 2 feste mancanti). +11 voci nell'albero.
- **Fonti note**: Mattorosso (gia' al PC, schede per orari e prezzi), TrovaSagre (+3 feste), Oderzo Cultura (0 nuovi),
  Ubik Treviso (+1). Comune di Orsago non riaperto (debole, trimestrale).
- **Fonti nuove catalogate**: 6 (Comuni di Cornuda, Chiarano, Fonte, San Polo di Piave; Istituto Musicale Malipiero;
  CAI Treviso uscite). Spostate in sources.yaml: 4 (i quattro comuni, html_llm).
- **Miglioria**: comuni piccoli riconosciuti dal tipo di portale e passati al PC con una lettura (regola nella sezione
  Treviso del metodo); luoghi ricorrenti da candidati del PC senza ricerche.
- **Test di copertura**: 8/10 (sagre di TrovaSagre).
- **Ricerche**: 61 su 70 (4 rifiutate subito: link presi dai file del repository).
- **Problemi aperti**: il giro del PC delle 01:00 non e' partito anche stanotte (l'ultimo e' stato a mano l'11/11
  mattina); controllare nel prossimo rapporto le 4 fonti nuove dei comuni e le posizioni ricalcolate; accesso non
  pubblicato da molte sagre e rassegne (campione sotto l'80%); calendario dell'Autunno Sanfiorese solo in PDF.

## 2026-11-11

- **Giro del PC**: NON ha girato per la quinta notte di fila (ultimo rapporto finito il 2026-11-06 alle 09:40; nessun
  commit del PC da allora). Coda, campione, segnalazioni e rapporto sono quelli del 6/11; gli eventi aggiunti dalla
  redazione dal 6/11 (oltre 170 con quelli di stanotte) non sono sul sito finche' il PC non li geolocalizza.
  Correzioni applicate con --applica (141 attive, sito a 286 eventi).
- **Fonti in errore** (rapporto del 6/11): ticketone a 0 eventi anche con le pagine /cityd/: aggiunte le pagine /venue/
  del Teatro Accademia e dell'Auditorium Cassamarca (da controllare nel prossimo rapporto). Restano insolitotrantran
  (API 404), comune-maser, -povegliano, -loria, -silea, -monastier (timeout dal PC), 2night e dice a zero.
- **Segnalazioni dal sito**: nessuna.
- **Coda di revisione** (15 aperti su 57): 0 corretti, 0 rimossi, 0 verificati. Provate 3 ricerche (schede di
  Sernaglia con titolo esatto, Biblioweek di San Biagio, Macedonia Sintetica al CW Gate): nessuna pagina utile. Restano
  aperti i 7 eventi di Sernaglia (luogo al centro del comune), Biblioweek, Farra profuma d'autunno, CRM da moku e radical
  design da .Ettore (solo Eventbrite), Circolando fuori casa a Codogne', passeggiata di Cison, Macedonia Sintetica,
  "Venezia, quello che non si vede" del 10/12.
- **Controllo a campione**: 3/10, stesso campione del 6/11, nessuna ricerca spesa (vedi segnalazioni-e-controllo).
- **Eventi aggiunti** (30): arte-cultura 11 (mostra Cesco Magnolato a Oderzo fino al 24/1, Giornate Martiniane 15, 19,
  23, 24/11, 4 presentazioni alla Ubik di Treviso, Land Editore alla biblioteca di Montebelluna, mostra su Lipparini al
  Bailo fino al 7/2), teatro-spettacoli 10 (Teatro Accademia di Conegliano: Legnanesi, Ornano, K Pop Dream, Awed Dadda e
  Dose, Valentina Persia, 2 repliche di Eleazaro Rossi, Il lago dei cigni; Eleazaro Rossi all'Auditorium Cassamarca 2
  repliche esaurite), musica 3 (Carroccia e Michael al Teatro Accademia, inaugurazione del Conservatorio Steffani),
  famiglie-bambini 3 (Storie sotto l'albero a Oderzo 12/11, 26/11, 10/12), natura-outdoor 2 (Il museo intorno al Covolo,
  SoulCollage ad Ananda Marga), mercatini-fiere 1 (Fondentemente in Piazza dei Signori 13-15/11).
- **Comuni controllati**: Oderzo (Fondazione Oderzo Cultura, 10 eventi), Breda di Piave (sito Municipium, nessun evento
  nuovo verificato), Istrana (Villa Lattes senza eventi datati), Casier, Salgareda (Festa d'autunno con date "indicative",
  non aggiunta), Meduna di Livenza: resa 0 per gli ultimi cinque.
- **Categorie cercate**: Spettacoli > Comicita' (12 eventi tra TicketOne e Please Stand Up), Spettacoli > Musical e
  operetta (resa 0 dalla ricerca, 2 tributi da TicketOne), Musica e party > Ballo (milonghe solo con schede vecchie),
  Natura e benessere > Animali (resa 0). +11 voci nell'albero.
- **Fonti note**: cheventi non riaperta (vietata): messa ferma per toglierla dal piano.
- **Fonti nuove catalogate**: 8 (Fondazione Oderzo Cultura, TicketOne Teatro Accademia, Please Stand Up, Conservatorio
  Steffani, Ubik Treviso, Comune di Roncade, Ananda Marga Treviso, guida del weekend di TViWeb). Spostate in sources.yaml:
  3 (comune-roncade html_llm, pagine /venue/ dentro la fonte ticketone).
- **Miglioria**: per gli spettacoli commerciali si legge la pagina del locale su TicketOne (/venue/), che passa al PC;
  regola nuova nella sezione Treviso del metodo.
- **Test di copertura**: 4/10 (mancavano Oderzo Cultura, Conservatorio, Ubik, Land Editore, Ananda Marga, Fondentemente:
  aggiunti).
- **Ricerche**: 61 su 70.
- **Problemi aperti**: il PC non pubblica dal 6/11 mattina (quinta notte); la fonte ticketone del PC da' 0 eventi (forse
  protezione anti-bot: se anche le /venue/ restano a zero va letta con il browser o da Claude); 15 eventi in coda senza
  fonte apribile; Festa d'autunno di Salgareda senza date confermate; candidati html_llm da valutare (Oderzo Cultura,
  Ubik Treviso, Breda di Piave Municipium).

## 2026-11-10

- **Giro del PC**: NON ha girato per la quarta notte di fila (ultimo rapporto finito il 2026-11-06 alle 09:40). Coda,
  campione e rapporto sono ancora quelli del 6/11; gli eventi aggiunti dalla redazione dal 6/11 (oltre 140) non sono
  sul sito finche' il PC non li geolocalizza. Correzioni e rimozioni applicate con --applica.
- **Segnalazioni dal sito**: nessuna.
- **Coda di revisione** (24 aperti su 57 all'inizio) e campione: 5 corretti, 0 rimossi, 4 verificati. Quinto di
  Treviso: "Venezia, quello che non si vede" dell'11/11 (20:30 in biblioteca, Via D'Annunzio 9, gratuito), "Voci di
  carta" del 20/11 (17:30-18:30, gratuito), "Sicurezza e prevenzione" del 21/11 (ore 15 alle ex scuole Pio X, ingresso
  libero). Corsa dei Babbi Natale di Ponzano: partenza alle 10 (non 9) dallo stadio, Via del Bellato 2, 7 euro, sito
  dell'organizzatore. X-mas Run di Treviso: domenica 13/12 alle 10 da Piazza dei Signori, iscrizioni su avaibooksports.
  Verificati i 4 concerti di Autunno Musicale (date, ore e chiese giuste; l'ingresso non e' pubblicato da nessuno).
  Restano aperti: 7 eventi di Sernaglia (sito vietato, schede non trovate), "Venezia, quello che non si vede" del 10/12
  (luogo da confermare), Circolando fuori casa a Codogne' (scheda rifiutata), Farra profuma d'autunno, CRM da moku e
  radical design da .Ettore (solo Eventbrite), passeggiata Beescover a Cison, Macedonia Sintetica al CW Gate.
- **Controllo a campione**: 3/10, stesso campione del 6/11, nessuna ricerca spesa (vedi segnalazioni-e-controllo).
- **Eventi aggiunti** (22): sagre-feste 7 (San Martino a Sarano e a Musano, Madonna della Salute a Villanova, 50a
  Mostra dei vini del Montello a Volpago, Sant'Andrea e Immacolata a Solighetto, Cena del Lesso a Sant'Angelo,
  accensione del presepe a San Fior), teatro-spettacoli 3 (Compagnia Colonna Infame a San Fior), musica 3 (Festival
  Organistico di Collalto 15/11 e 20/12, concerto del 29/11 a San Fior), famiglie-bambini 3 (gruppo di lettura ragazzi
  e Sannicolibri a San Fior), mercatini-fiere 3 (Natale a Collalto 5, 6, 8/12), arte-cultura 2 (Le Immagini della
  Fantasia 44 a Sarmede fino al 14/2, mostra su Canova e Nelson alla Gypsotheca di Possagno fino al 25/4), sport 1
  (ciclocross di San Fior il 27/12).
- **Comuni controllati**: Possagno (mostra), Susegana (sito del borgo di Collalto, 5 eventi), San Fior (PDF di Autunno
  Sanfiorese, 10 eventi; date con giorno della settimana sbagliato non aggiunte), Sarmede (mostra), Fontanelle e
  Monfumo (resa 0).
- **Categorie cercate**: Sport > Corsa (2 correzioni, nessuna gara nuova: il PC legge gia' Calendario Podismo Veneto),
  Famiglie e bambini > Letture e biblioteche (3 da San Fior e Quinto), Famiglie e bambini > Ricorrenze (presepi: date
  2026 non ancora uscite), Sport > Sport tradizionali e popolari (resa 0). +13 voci nell'albero.
- **Fonti note**: TrovaSagre (6 eventi e test di copertura), Treviso Sotterranea (0, solo articoli vecchi), cheventi non
  riaperta (vietata).
- **Fonti nuove catalogate**: 5 (Collalto di Susegana, Autunno Sanfiorese del Comune di San Fior, schede eventi del
  Comune di Quinto, Podopodo, TrovaEventi). Spostate in sources.yaml: 0.
- **Miglioria**: per la coda dei comuni con elenco vietato si cercano le schede con titolo esatto e dominio del comune
  (si aprono); i calendari stagionali dei comuni piccoli si leggono dal PDF allegato alla notizia.
- **Test di copertura**: 3/10 sulle sagre di trovasagre (aggiunte le mancanti con date certe).
- **Ricerche**: 52 su 70.
- **Problemi aperti**: il PC non pubblica dal 6/11 mattina (quarta notte); sagre poco coperte (3/10); 7 eventi di
  Sernaglia in coda senza fonte apribile; San Martin di Roganzuolo e Falze' (11/11) e festa di Bibano non aggiunti per
  mancanza di dati; date dubbie nel PDF di San Fior (17, 18, 21/12).

## 2026-11-09

- **Giro del PC**: NON ha girato per la terza notte di fila (ultimo rapporto finito il 2026-11-06 alle 09:40). Coda,
  campione e rapporto sono quelli del 6/11; tutti gli eventi aggiunti dalla redazione dal 6/11 (oltre 120) non sono
  ancora sul sito perche' il PC deve geolocalizzarli. Correzioni e rimozioni sono state applicate con --applica.
- **Segnalazioni dal sito**: nessuna.
- **Coda di revisione** (38 aperti su 57) e campione: 2 corretti, 13 rimossi (conclusi tra il 6 e l'8/11), 0
  verificati. "Papa' ha bruciato i biscotti" del Mese del Bambino: titolo giusto, al Cinema Edera (Piazza Martiri di
  Belfiore 2) alle 10:30. Camminata d'Autunno del 22/11: link alla pagina di Hills Nordic Walking, comune Farra di
  Soligo (ritrovo non pubblicato). Restano aperti: eventi di Sernaglia e Quinto (siti vietati a WebFetch), accesso di
  Circolando fuori casa a Codogne' e di Autunno Musicale, CRM da moku e radical design da .Ettore (solo Eventbrite),
  Macedonia Sintetica al CW Gate (solo Instagram), X-mas Run (12 o 13/12), Corsa dei Babbi Natale di Ponzano.
- **Controllo a campione**: 3/10 (3 conclusi; data 1, orario 1, luogo 1, link 1).
- **Eventi aggiunti** (66): teatro-spettacoli 31 (stagione di prosa del Teatro Del Monaco: 7 spettacoli, 28 repliche
  dal 19/11 al 21/2; Teatro Comisso di Zero Branco: 3 spettacoli), sagre-feste 13 (rassegna Fiori d'Inverno: feste del
  radicchio a Paderno, Spresiano, Quinto, Castelfranco, Preganziol, Treviso, Zero Branco, Dosson, Mogliano, Vedelago),
  sport 10 (Imoco Volley al Palaverde 6 partite da gennaio, Mogliano Rugby 4 partite in casa), arte-cultura 10 (mostre:
  Renato Casaro e L'Ultima Rinascita alla Collezione Salce, Ritratti di donna a Palazzo Sarcinelli, Klimt a Villa
  Freya, Villa Romivo con 2 aperture straordinarie; Premio di pittura di Cordignano; 2 incontri nella biblioteca di
  Zero Branco), musica 1 (Una notte per Faber al Comisso), mercatini-fiere 1 (Profumi e Sapori d'Autunno a Susegana).
- **Comuni controllati**: Zero Branco (biblioteca: nuova fonte, 6 eventi), Montebelluna (mostra di Villa Romivo; sito
  del Comune vietato a WebFetch), Cimadolmo (Pro Loco ferma al 2017), Cavaso del Tomba e Tarzo (solo portali).
- **Categorie cercate**: Arte e cultura > Mostre (5 mostre, 1 su 10 era sul sito), Spettacoli > Teatro (28 date),
  Sport > Sport di squadra (10 partite), Sport > Sport d'acqua (resa 0). +11 voci nell'albero.
- **Fonti note**: Treviso Eventi (2 eventi nuovi e test di copertura), Treviso Sotterranea e cheventi non riaperte
  (vietate o in errore).
- **Fonti nuove catalogate**: 7 (itinerarinellarte mostre TV, Teatro Stabile del Veneto stagione del Del Monaco,
  Biblioteca di Zero Branco, Imoco Volley fixtures, Federugby Serie A Elite, Fiori d'Inverno, Hills Nordic Walking).
  Spostate in sources.yaml: 0 (la biblioteca di Zero Branco e' candidata html_llm).
- **Miglioria**: per mostre, stagioni teatrali, campionati e rassegne tematiche si parte dalla pagina che elenca la
  stagione intera: 59 eventi da 8 letture. Regola nella sezione Treviso del metodo. Corrette anche 41 sottocategorie
  non valide (prosa, radicchio) che --controlla non segnala.
- **Test di copertura**: 8/10 (trevisoeventi); mostre di itinerarinellarte 1/10; criterio di saturazione del lunedi'
  non rispettato, resta Treviso.
- **Ricerche**: 57 su 70.
- **Problemi aperti**: il PC non pubblica dal 6/11 mattina (terza notte); partite casalinghe dell'Imoco di novembre e
  dicembre e ritorno del Mogliano Rugby da confermare; mostre ancora da aggiungere (Andar per fiere, Magnolato a
  Oderzo, Battistin a Vittorio Veneto); stagione lirica del Del Monaco; luoghi delle feste del radicchio.

## 2026-11-08

- **Giro del PC**: NON ha girato per la seconda notte di fila (ultimo rapporto finito il 2026-11-06 alle 09:40). Coda,
  campione e rapporto sono quelli del 6/11; gli eventi aggiunti dalla redazione dal 6/11 non sono ancora sul sito.
- **Segnalazioni dal sito**: nessuna.
- **Coda di revisione** (46 aperti su 57) e campione: 9 corretti, 0 rimossi, 1 verificato. Calendario Podismo Veneto di
  dicembre: Camminata di Natale a Castello di Godego (9:00, era "Godego") e Corsa dei Babbi Natale di Ormelle con il link
  al mese. Cornuda Santa Klaus da sagritaly: 6/12 dalle 8 alle 18 in Piazza Giovanni XXIII, palio alle 15. Maserada sul
  Palco (14, 21, 28/11): ore 21 e Viale Cacciaganga 2 da trevisoeventi. Sile Classica 22/11: Auditorium dell'Istituto
  Comprensivo. Bim Boom Jam: comune Sernaglia della Battaglia. Villa Bornello: tolto lo slogan dal luogo. H-FARM a Ca'
  Tron: punto giusto (verificato). Restano aperti: accesso di Autunno Musicale e Maserada sul Palco (non pubblicato),
  Farra profuma d'autunno (solo Eventbrite), passeggiate Beescover di Tarzo e Cison (sito in errore), eventi di Quinto e
  Sernaglia, X-mas Run (12/12 per Podismo Veneto, 13/12 per calendariopodismo), Corsa dei Babbi Natale di Ponzano.
- **Controllo a campione**: 3/10 (3 conclusi; luogo 3, link 1, data 1, orario 1).
- **Eventi aggiunti** (14): sagre-feste 10 (Sagra del Frico a Lorenzaga 6 serate, Rassegna Triveneta delle Birre
  Artigianali a Camalo' 13-22/11, Gusti d'Autunno a Camalo', Festa di Sant'Andrea a Santandra', Palio delle Botti tra
  Soligo e Col San Martino 14/11), musica 2 (Petite Messe di Rossini a Cusignana 14/11, Concerto dell'Anniversario a
  Povegliano 8/12), mercatini-fiere 1 (mercatino di Natale di Segusino 15/11), arte-cultura 1 (letture sulla violenza di
  genere a Povegliano 28/11).
- **Comuni controllati**: Gaiarine e Trevignano (siti MyPortal: passati al PC), Farra di Soligo (Palio delle Botti),
  Vazzola (solo la Festa d'Autunno gia' presente), Cessalto (sito vietato a WebFetch), Follina (sito della Pro Loco vuoto).
  Sagra Madonna dea Salute di Albina (20-22/11) solo su microturismo: non aggiunta.
- **Categorie cercate**: Musica partecipata, Patrimonio e tradizioni, Racchetta, Cinema: resa 0 (pagine di anni passati).
  +10 voci.
- **Fonti note**: Libreria San Leonardo (1 evento, oggi stesso: non aggiunto), Cinema Edera (rassegne in errore),
  Treviso Sotterranea e cheventi non riaperte (vietate o in errore).
- **Fonti nuove catalogate**: 5 (trovasagre, PDF eventi del Comune di Povegliano, Paesi in Festa, Sagritaly, Pro Loco
  Segusino). Spostate in sources.yaml: 2 (comune-trevignano C_L402 e comune-gaiarine C_D854, codici catastali da
  confermare nel primo rapporto).
- **Miglioria**: per le sagre si parte dall'elenco del mese di trovasagre (9 mancanti su 13 in una lettura) e dai PDF annuali
  degli eventi dei Comuni; regola nella sezione Treviso del metodo.
- **Test di copertura**: 7/10 (trevisoeventi); sagre di trovasagre 4/13.
- **Ricerche**: 59 su 70.
- **Problemi aperti**: il PC non pubblica dal 6/11 mattina; sagre di trovasagre ancora da confermare (Sarano, Roganzuolo,
  Musano, Villanova, Solighetto, Cena del Lesso, Festival del Radicchio di Ponzano, Mostra dei vini di Volpago);
  codici IPA di Trevignano e Gaiarine da controllare; fonti comunali in timeout dal PC.

## 2026-11-07

- **Giro del PC**: il giro dell'01:00 di stanotte NON ha pubblicato (ultimo rapporto finito il 2026-11-06 alle 09:40,
  giro a mano di Federico: 299 eventi, 16,4 minuti). Coda e campione sono quelli del 6/11. Fonti in errore nel rapporto:
  insolitotrantran (API tribe 404, e il sito da' errore anche a WebFetch), comune-maser, comune-povegliano, comune-loria,
  comune-silea e comune-monastier (WinError 10060, timeout dal PC; i primi tre da 3 giri); 2night, ticketone, dice e
  comune-paese a zero. Non disattivate: da guardare dal PC.
- **Segnalazioni dal sito**: nessuna.
- **Coda di revisione** (57, lavorati circa 30) e campione: 45 corretti, 0 rimossi, 3 verificati.
  Stadio di Monigo: coordinate da Wikipedia per le 6 partite del Benetton Rugby (erano sparse nel comune). Gli Alcuni:
  tolto il punto provvisorio in centro a 29 schede (Parco degli Alberi Parlanti, ora Viale G. G. Felissent 56 da
  mailticket, e Teatro Sant'Anna, Viale Brigata Treviso 18): il PC le geolocalizza per indirizzo. Podismo: volantini del
  Calendario Podismo Veneto come link per 7 gare (Marcia di San Nicolo' a Pianzano, Monte Christmas Walk, Babbo Run,
  Babbi Natale di Asolo, Santa Klaus Run 10:00, LitTLe RuN 9:30, Maratonina di San Silvestro 8:30). Prosecco Ultra Trail
  da Vittorio Veneto con iscrizione da 80 euro; Spreafico al Mattorosso con link e prezzo del locale; Quattro donne e un
  bastardo al Teatro Comunale di Falze' (Via Puccini 1, 8 euro). Pulizia: tolte 4 correzioni di eventi del 30/10.
  Restano aperti: eventi del Comune di Quinto e di Sernaglia (siti non apribili con WebFetch), accesso di Autunno
  Musicale e Maserada sul Palco, X-mas Run Treviso (12/12 per Podismo Veneto, 13/12 per calendariopodismo).
- **Controllo a campione**: 1/10 (luogo 2, link 2, accesso 1, orario 1; 2 conclusi, 2 non aperti).
- **Eventi aggiunti** (46): sagre-feste 19 (sagra di San Martino a Colle Umberto 7 giornate, Festa d'Autunno a Visna'
  9, sagra di San Mauro a Castagnole, San Martin a Mojan 7 e 8/11), musica 11 (10 date del Mattorosso, Note da Oscar a
  Villa Onigo 15/11), sport 7 (parkrun Treviso 5 sabati, social run del Mattorosso, Imoco - Macerata 8/11),
  teatro-spettacoli 5 (Anima Teatro a Monastier 4 date, Saverio Raimondo al Mattorosso), mercatini-fiere 4 (Milipiave a
  Spresiano, antiquariato di Portobuffole' 8/11 e 13/12, antiquariato di Collalto).
- **Comuni controllati**: Carbonera, Castelcucco, Colle Umberto (solo portali; per Colle Umberto la sagra da
  trevisoeventi), Vedelago e Valdobbiadene (siti del Comune vietati a WebFetch; sagra di San Martino di Vedelago solo
  con articoli del 2023). Chiarano non fatto.
- **Categorie cercate**: Collezionismo (Milipiave, Portobuffole', Collalto), Sport per tutti (parkrun, social run),
  Circo e arti di strada (solo circhi in tournee, nessuna data TV confermata), Storia e rievocazioni (San Martin a
  Mojan). +10 voci.
- **Fonti note**: Sagramap (6 sagre TV di novembre, resa 5 dopo le verifiche), VenetoToday (nessun evento nuovo),
  trevisoeventi (test di copertura e 8 schede). cheventi non riaperta (errore a WebFetch).
- **Fonti nuove catalogate**: 5 (Mattorosso, Trevignano Cultura, parkrun Treviso, Associazione Istadea, Pro Loco
  Mogliano). Spostate in sources.yaml: 1 (mattorosso html_llm, da controllare nel primo rapporto per i doppioni).
- **Miglioria**: regola nuova per Treviso: le schede di trevisoeventi danno programma e organizzatore in una lettura,
  un evento per giornata, official_url l'organizzatore o la scheda. Chiusi i buchi del test di copertura di tre notti.
- **Test di copertura**: 4/10.
- **Ricerche**: 62 su 70.
- **Problemi aperti**: il giro dell'01:00 non pubblica (eventi della redazione dal 6/11 non ancora sul sito); fonti
  comunali in timeout dal PC; insolitotrantran in errore; Trevignano Cultura e Pro Loco Mogliano da provare come
  tribe_api dal PC; Premio di pittura di Cordignano e sagra di Moriago non aggiunti (non confermati).

## 2026-11-06

- **Giro del PC**: NON ha girato per la terza notte di fila (ultimo rapporto finito il 2026-11-03 alle 01:23). Coda,
  campione e segnalazioni sono quelli del 3/11; gli eventi aggiunti dalla redazione dal 2/11 non sono ancora sul sito.
- **Segnalazioni dal sito**: nessuna.
- **Coda di revisione** (33 rimasti, lavorati 12) e altri eventi: 20 corretti, 1 rimosso, 0 verificati.
  Eventbrite: l'elenco dei gratuiti di Treviso ha confermato accesso (gratuito su iscrizione) e orario di 14 eventi
  (In principium erat verbum, Giammarco Sicuro, G Star, Tomaso da Modena, Il canto di Orsola, Concerto di San Leonardo,
  Quinto Concerto Sinfonico, Deep Trend H-FARM, Guido Damini, La Roste Ride, Autumn social run, STORIES, due del
  4passiFestival). San Biagio: convegno sul clima in viticoltura (10/11 18-21, Sala Polivalente, gratuito), Ge.Ni. primo
  soccorso pediatrico (21/11 9-13, Skhole', iscrizione), LeggiAMO in Biblioteca 14/11 e 12/12 (biblioteca, su
  prenotazione). Antica Fiera di Santa Lucia: orari dell'8/11. Castelfranco: tolta la pagina della stagione di prosa
  (gli spettacoli sono gia' uno per uno), cerimonia del 4 novembre spostata da sport a ricorrenze.
  Restano aperti: accesso di Autunno Musicale e Maserada sul Palco, Giallo in Castello (nessuna scheda 2026 di novembre),
  Sile Classica 22/11 (ingresso non pubblicato), eventi Eventbrite non gratuiti (.Ettore, Cosniga, CRM da moku, A scena
  aperta, Giovanni IMI, Farra profuma d'autunno), Fogliart e Macedonia Sintetica (solo Instagram).
- **Controllo a campione**: 3/10 (accesso 4, link 2, luogo 1), stesso campione del 3/11.
- **Eventi aggiunti** (12): sagre-feste 5 (Prealpi in Festa a Cordignano 6, 7 e 8/11; Antica Fiera di Santa Lucia 7/11),
  sport 3 (Treviso FBC al Tenni con Novara, Pergolettese, Arzignano), musica 2 (Cappella Sistina a Sernaglia 7/11,
  Harmonia Mundi all'Antica Fiera 6/11), mercatini-fiere 1 (libro e stampa antichi ad Asolo 7-8/11), famiglie-bambini 1
  (burattini di Pinocchio a Sernaglia 8/11), arte-cultura 1 (sicurezza in strada a Codogne' 19/11).
- **Comuni controllati**: Sernaglia della Battaglia (design-comuni: al PC), Codogne' (pagina eventi vuota), Miane (Festa
  dei Marroni finita il 1/11), Motta di Livenza (sito del Comune non apribile), Moriago e Arcade (solo portali).
- **Categorie cercate**: Motori (solo calendari nazionali), Mercati agricoli (mercati settimanali fissi: non eventi),
  Convegni (festival gia' coperti), Vino (degustazioni su appuntamento del Consorzio: non eventi). +11 voci.
- **Fonti note**: Nordest24 (guida del weekend, 3 eventi), Eventi Venetando (Prealpi in Festa, 3 eventi), trevisoeventi
  (test di copertura). VenetoToday non riaperta.
- **Fonti nuove catalogate**: 5 (elenco Eventbrite gratuiti, Comune di Sernaglia, Comune di Codogne', Comune di Mogliano,
  Treviso FBC). Spostate in sources.yaml: 3 (eventbrite `free_listing_urls`, comune-sernaglia html_llm,
  comune-mogliano myportal C_F269, da controllare nel primo rapporto).
- **Miglioria**: la fonte jsonld accetta `free_listing_urls`: gli eventi di un elenco "solo gratuiti" prendono accesso
  iscrizione e prezzo gratuito (Eventbrite); test nuovo.
- **Test di copertura**: 1/10.
- **Pulizia**: tolte 2 rimozioni di eventi conclusi prima del 30/10.
- **Ricerche**: 60 su 70.
- **Problemi aperti**: il PC fermo dal 3/11 (nessun evento nuovo sul sito da tre notti); San Martin a Mojan (7-8/11) e
  Imoco - Macerata (8/11) non confermati; sagre di Colle Umberto, Visna' e Castagnole solo su aggregatori.

## 2026-11-05

- **Giro del PC**: NON ha girato stanotte ne' la notte del 4/11 (ultimo rapporto finito il 2026-11-03 alle 01:23,
  12,6 minuti, 256 eventi). Nessuna redazione notturna il 3 e il 4/11. Lavoro sui dati gia' pubblicati: coda e
  campione sono quelli del 3/11. Nel rapporto del 3/11: comune-maser, comune-povegliano e comune-loria in errore di
  connessione (WinError 10060, timeout dal PC); comune-san-biagio 10 e comune-castelfranco 5 eventi nuovi (html_llm
  funziona); gli-alcuni 47 nuovi ma tutti con il punto sbagliato; teatro-da-ponte 1 (le 35 date sono gia' in
  eventi_redazione).
- **Segnalazioni dal sito**: nessuna.
- **Coda di revisione** (60, lavorati 27): 35 corretti, 17 rimossi, 0 verificati.
  Gli Alcuni: 30 schede a Treviso (Teatro Sant'Anna, Parco degli Alberi Parlanti, Teatro Del Monaco) erano a
  Vittorio Veneto o in campagna per il comune "Treviso (TV)": luogo, indirizzo e comune corretti, punto provvisorio
  in Piazza dei Signori; 14 repliche "| scuole" rimosse (riservate alle classi) e la mattina per le scuole di Fuori
  copione al Palaverde. San Biagio di Callalta: Requiem di Faure' (7/11 20:45, chiesa di Sant'Andrea di Barbarana,
  offerta libera), Zeroplastic a Olmi (8/11, iscrizione gratuita), StraWoman (15/11 10-13), convegno sulle api
  (18/11 20:00, Sala Consiliare, gratuito); due schede del 4/11 concluse rimosse. Anatomia di un film: corso su
  iscrizione. Restano aperti: accesso di Autunno Musicale (testate e La Vita del Popolo non lo dicono; "Tra codici e
  manoscritti" alle 10 su musincantus, 9:30 e 11 su La Vita del Popolo), eventi Eventbrite di .Ettore, Castelfranco
  (Giallo in Castello, 8 novembre), Fogliart in Cansiglio, Maserada sul Palco (ingresso solo nella scheda di Vicini).
- **Controllo a campione**: 0/10 (accesso 6, luogo 2, link 2).
- **Eventi aggiunti** (18): sport 13 (7 partite casalinghe di Treviso Basket al Palaverde, 6 del Benetton Rugby a
  Monigo), arte-cultura 2 (I racconti del Memoriale al Memoriale Brion, FAI, 8 e 29/11), teatro-spettacoli 2
  (Nautilus a Falze' l'8/11 e a San Biagio il 23/1), natura-outdoor 1 (serata sui rapaci a Silea, 13/11).
- **Comuni controllati**: Silea (portale con schede complete: al PC), Quinto di Treviso (design-comuni: al PC),
  Monastier di Treviso (stesso portale di Silea: al PC), Orsago (nessun evento in programma), Gorgo al Monticano e
  Altivole (solo portali; per Altivole il FAI al Memoriale Brion).
- **Categorie cercate**: Eventi per chi guarda (13 partite), Networking (Confcommercio e Confapi, nulla di futuro;
  trevisoimprese.it vieta i robot), Equitazione e Arti marziali (solo calendari federali generici). +11 voci.
- **Fonti note**: Hello Mogliano (solo post vecchi: debole).
- **Fonti nuove catalogate**: 8 (Comune di Quinto, Silea, Monastier, Orsago, FAI Memoriale Brion, Treviso Basket,
  Benetton Rugby, Nautilus Cantiere Teatrale). Spostate in sources.yaml: 4 (comune-quinto, comune-silea,
  comune-monastier come html_llm; nautilus-teatro come tribe_api). Sistemata: gli-alcuni (escludi_titoli).
- **Miglioria**: nel codice, il geocoder toglie la sigla della provincia dal comune (`clean_town`), il raccoglitore
  tribe ripulisce i luoghi "• Treviso – ..." e ogni fonte puo' avere `escludi_titoli`; due test nuovi.
- **Test di copertura**: 0/10 (feste di paese e rassegne solo su Facebook e trevisoeventi).
- **Ricerche**: 50 su 70.
- **Per la notte dopo**: controllare nel rapporto che i punti di Gli Alcuni siano a Treviso e le 4 fonti nuove;
  trovare le coordinate del Teatro Sant'Anna (Viale Brigata Treviso 18) e del Parco degli Alberi Parlanti (Viale
  Felissent) e sostituire il punto provvisorio; Maser, Povegliano e Loria in timeout dal PC; Italia XV - Queensland
  Reds a Monigo (20/11) da confermare sulla pagina FIR; pulizia di correzioni.yaml (voci di eventi non piu' sul sito).

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
