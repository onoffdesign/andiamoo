# Categorie di ricerca

L'albero delle categorie che la revisione notturna usa per **cercare** gli eventi, sempre piu' in dettaglio. Ogni
notte Claude lo allarga con ricerche vere: nuove discipline, specialita', formati, ricorrenze tipiche del
territorio. Non e' l'elenco dei filtri del sito: il sito resta con le sue 9 categorie (`config/categories.yaml`);
queste voci servono a non dimenticare nessun tipo di evento e diventano `subcategory` e tag degli eventi trovati.

## Come si usa e come cresce

- **Livelli**: macro categoria del sito, poi ambito (es. Arrampicata), poi specialita' (es. boulder). Si va avanti
  finche' ha senso per cercare: se una specialita' ha eventi propri (gare, raduni, corsi) merita la sua riga.
- **Parole di ricerca**: tra parentesi quadre i termini che funzionano nelle ricerche, in italiano e nei nomi usati
  dagli organizzatori (es. "contest", "open", "trofeo").
- **Ogni notte**: aggiungi le voci nuove previste dal budget (`categorie_nuove` in `ops/budget.yaml`, oggi 10), distribuite su piu' macro categorie, nate da cio' che hai visto
  nelle fonti (un tipo di evento che non c'era) o da ricerche mirate (federazioni sportive, calendari di settore,
  associazioni). Segna la data accanto alle voci nuove.
- **Resa per provincia**: in `ops/copertura.yaml` (sezione `categorie_<SIGLA>`) la data dell'ultima ricerca di ogni
  ambito in quella provincia, come "Sport > Arrampicata: 2026-11-02". Una voce cercata 3 volte senza eventi in una provincia si segna `rara` e si ricerca una
  volta al mese.
- **Dove cercare**: quando una voce ha una fonte che rende (federazione, calendario di settore), scrivila accanto
  con `→ fonte` e mettila in `ops/fonti.yaml`: la volta dopo non serve ricercare.

## Sport (`sport`)

- **Corsa** [podistica, non competitiva, camminata ludico-motoria, corsa su strada, fun run]
  - non competitive e marce [marcia, camminata, Fiasp] → calendariopodismo, podismoveneto
  - mezza maratona e maratona · 10 km · staffette · corse a tema (color run, notturne, in maschera)
  - trail running [trail, skyrace, ultratrail, vertical] → gotrail
  - corsa campestre [cross] · corsa in montagna
  - corse dei Babbi Natale [Babbi Natale, Santa Klaus run, X-mas run] (fine novembre - dicembre) → podopodo, trovaeventi
  - corse benefiche di associazioni [corsa solidale, per la ricerca] · ciclocross di dicembre [trofeo ciclocross, memorial]
  · calendario annuale delle marce non competitive provinciali [Trevisando, marce non competitive <anno>] (2026-11-22) → trevisando.it · marce di San Nicolo' e dell'Immacolata [marcia San Nicolo', marcia dell'Immacolata] (2026-11-22) · corse di solidarieta' di Santo Stefano [little run, corsa 26 dicembre] (2026-11-22)
  · corse solidali di Santo Stefano [run 26 dicembre] (2026-11-24)
- **Ciclismo** [gran fondo, cicloturistica, randonnée, gravel]
  - strada · mountain bike [XC, enduro, marathon MTB] · gravel · ciclocross · e-bike · BMX
  - cicloturistiche ed eroiche · pedalate per famiglie · bike test e raduni
  · circuiti di ciclocross regionali [Trofeo Triveneto CX, Master Cross] (2026-11-16) → federciclismo trofeo-triveneto · ciclocross giovanile e staffette a squadre [team relay, giovanissimi] (2026-11-16) · ciclocross di fine anno e Santo Stefano [cross di fine anno] (2026-11-16)
- **Arrampicata** [arrampicata, climbing, boulder, falesia] · rassegne di film di arrampicata [Reel Rock, film festival montagna]
  - boulder [contest boulder, open boulder] · lead [difficolta'] · speed · falesia [raduno in falesia]
  - palestre indoor (open day, corsi base) · ice climbing · gare FASI
  · palestre della provincia [Gioco Verticale - Le Bloc a Treviso, Orizzonti Verticali a Montebelluna, Arena Boulder]:
    i siti non pubblicano eventi datati, contest solo sui social (2026-11-12: resa 0) · calendario gare FASI [federclimb calendario gare] · prove della Veneto Boulder Cup FASI [boulder cup, programma di gara] (2026-11-27: nessuna prova in provincia nei prossimi 120 giorni)
- **Montagna ed escursionismo** (vedi anche Natura) [escursione CAI, uscita sociale]
  - escursioni guidate · via ferrata · scialpinismo · ciaspolate [racchette da neve] · alpinismo
  · uscite delle sezioni CAI [CAI Treviso uscite, gruppi Seniores, Kalipe', Neveganti]: mete in provincia (Cartizze,
    Monfenera, Monte Baldo di Vittorio Veneto), schede complete solo pochi giorni prima · uscite di fine anno con pranzo
- **Sport d'acqua** [regata, gara di nuoto] (in autunno rara: nessun evento il 2026-11-09) · regate in costume di Natale sul fiume [regata dei Babbi Natale, canottieri] (2026-11-23)
  · campionati di canottaggio di fondo sul Sile [canottieri, tricolori di fondo] · meeting di nuoto nelle piscine comunali [swim cup, trofeo]
  - nuoto in piscina · nuoto in acque libere · canoa e kayak · rafting · SUP [stand up paddle] · canottaggio
  - vela · pesca sportiva
- **Sport di squadra** [torneo, partita, campionato]
  - calcio · calcio a 5 · basket · pallavolo · beach volley · rugby · pallamano · hockey · baseball e softball
  - rugby di Serie A Elite in casa [calendario federugby, Mogliano] · Champions League di pallavolo femminile [CEV, Palaverde]
- **Racchetta** [torneo, open] · tennis · padel · ping pong · badminton · pickleball
  · tornei open FITP di padel [calendario tornei padel FITP Veneto, PDF regionale] · esibizioni ed eventi nei club [padel cup, clinic]
  · tornei di padel di fine anno nei circoli [torneo di Natale padel, open di dicembre] (2026-11-22): in provincia escono solo su Playtomic e social, resa 0
- **Arti marziali e combattimento** [stage, torneo, open day] · judo · karate · taekwondo · boxe · kickboxing · scherma
  · gare regionali FIJLKAM con informativa PDF (Conegliano) [informativa, trofeo] (2026-11-19: solo calendari e PDF, resa 0) · stage di Natale delle palestre di karate [stage di Natale karate]
  · gare regionali FIJLKAM [fijlkam calendario gare Veneto]
- **Sport invernali** · sci alpino · sci di fondo · snowboard · pattinaggio su ghiaccio · piste di pattinaggio in piazza [on ice, pista del ghiaccio] (novembre-gennaio, 2026-11-23) · inaugurazione delle piste di ghiaccio in piazza [inaugurazione pista, piazza Cima] (2026-11-28)
  · piste di ghiaccio di Natale nelle piazze e nei centri commerciali [pista di ghiaccio, on ice] (da fine novembre) · gare e saggi di pattinaggio artistico sulle piste di Natale [saggio pattinaggio]
- **Motori** [raduno, rally, gara] · rally · motocross · enduro moto · auto e moto d'epoca (raduni) · karting · motoraduni di Babbo Natale [babbi natale in moto, raccolta benefica] · raduni della Befana in moto
  · calendario ACI Sport del mese [acisport calendari] · mostre scambio di auto e moto d'epoca · autocross
- **Equitazione** [concorso ippico] · salto ostacoli · endurance · passeggiate a cavallo · palio
  · concorsi indoor invernali nei maneggi coperti [concorso indoor, salto ostacoli inverno] (2026-11-19: resa 0, escono solo calendari nazionali) · befana a cavallo e presepi equestri [presepe a cavallo]
  · concorsi FISE del Veneto [equiresults calendario, rideup]
- **Sport di precisione** · tiro con l'arco · golf · bocce · biliardo · freccette
  · gare indoor di tiro con l'arco da novembre a febbraio [inviti FITArco, ianseo] · tiro 3D nel bosco (Crocetta)
    · gare di bocce nei bocciodromi comunali [bocciofila, gara a coppie] (2026-11-12: nessun evento TV trovato)
- **Ginnastica e danza sportiva** · ginnastica artistica e ritmica · danza sportiva · cheerleading
  · saggi di Natale delle societa' di ginnastica [saggio di Natale, palazzetto] (meta' dicembre) · gare regionali FGI ospitate nei palazzetti della provincia [federginnastica, prova regionale]
- **Sport tradizionali e popolari** · palio e giochi storici · tiro alla fune · corsa nei sacchi
  · giochi popolari dentro le sagre (pignatte, corsa nei sacchi, partita delle vecchie glorie) · palio di Sant'Andrea (Solighetto) · Panevin e foghera (5-6 gennaio)
- **Eventi per chi guarda** [partita, match] · partite di serie A-B-C delle squadre locali · grandi eventi sportivi
  · basket di Serie A al Palaverde [Treviso Basket calendario] · rugby URC e Challenge Cup a Monigo [Benetton Rugby calendario]
  · pallavolo A1 femminile al Palaverde [Imoco] · Champions League di pallavolo al Palaverde [CEV Champions League Imoco] (2026-11-20) · calcio di Serie C allo stadio Tenni [Treviso calcio]
- **Sport per tutti** · open day delle societa' · giornate dello sport · sport adattato e paralimpico
  · corse libere gratuite del sabato mattina [parkrun Treviso, Parco dello Storga] · social run dei locali e dei negozi di sport [social run, run club] · camminate dei Babbi Natale [corsa dei Babbi Natale, Santa Klaus run]
  · camminate in costume da Babbo Natale [camminata dei Babbi Natale, Christmas run] · parkrun del sabato (5 km cronometrati) [parkrun] (2026-11-26) · tornei solidali di Natale negli oratori [torneo di burraco, calcio balilla, NOI] (2026-11-27)

## Arte e cultura (`arte-cultura`)

- **Mostre** [mostra, esposizione, vernissage, inaugurazione] · arte antica · arte contemporanea · fotografia
  · illustrazione e fumetto · design · collettive di artisti locali · mostre fotografiche sulla storia del Piave [alluvione, mostra fotografica]
  · manifesti pubblicitari e grafica d'epoca [Collezione Salce] · mostre in ville con parco [villa, giardino, biglietto mostra e parco] · collezioni private aperte nei fine settimana [apertura straordinaria, curatore] · premi di pittura delle Pro Loco [premio nazionale di pittura, acquerello]
  · mostre diffuse su piu' sedi di una citta' [mostra diffusa, centenario] (2026-11-17)
  · mostre di costumi teatrali e restauro tessile [Avanscena, costumi di scena] · mostre nelle gallerie dei licei artistici [galleria del liceo, inaugurazione] · retrospettive di scultori del territorio [Toni Benetton] (2026-11-20)
  · mostre nelle gallerie dei licei artistici [galleria del liceo artistico] (2026-11-24) · rassegne per gli anniversari di un artista [700 anni, centenario]
- **Visite guidate** [visita guidata, passeggiata culturale] · centri storici · ville venete · chiese e abbazie · beni del FAI [fondoambiente eventi, I racconti del Memoriale] · visite speleologiche ad acquedotti e sotterranei [Asolo Sotterranea, acquedotto della Bot] (2026-11-25)
  · percorsi sotterranei e mura · musei aperti la sera · giornate FAI e ville aperte
  · itinerari guidati con letture e musica nelle chiese [sulle orme di] (2026-11-24) · visite guidate dello IAT legate a una rassegna [IAT visita guidata] · visite animate nei musei civici durante le feste [visita animata, vacanze di Natale al museo] (2026-11-27)
- **Libri e lettura** [presentazione del libro, incontro con l'autore, festival letterario] · gruppi di lettura · lettura di Dante canto per canto [Tutta la Commedia, lectura Dantis] · presentazioni in libreria universitaria
  · calendario settimanale delle presentazioni delle librerie di catena [eventi nelle librerie] (2026-11-18) → treviso.ubiklibri.it/eventi.html · firmacopie del sabato in libreria [firmacopie]
  · letture per adulti · poesia e slam poetry
- **Conferenze e incontri** [conferenza, talk, dialogo] · storia locale · scienza e divulgazione · filosofia · cicli settimanali di conferenze delle fondazioni [Giovedi' della Cultura, Fondazione Cassamarca] (2026-11-28)
  · ambiente · astronomia (serate osservative) · festival di cittadinanza e cooperazione [festival, dialogo, 4passi]
  · guide all'ascolto con letture [guida all'ascolto, viaggio tra i grandi della musica] (2026-11-16) → trevisoeventi pagine comune · conferenze di centri culturali e spirituali [conferenza pubblica, simbolismo] (2026-11-16)
  · teatro forum e incontri partecipati · cicli comunali su salute e territorio [salute e territorio, agricoltura biologica] · sfilate di moda equosolidale nelle botteghe [sfilata, Altromercato, 4passi] · festival della statistica e dei dati [StatisticAll, Istat] (2026-11-27) · incontri collaterali alle mostre nei municipi [incontro in Municipio, storia dell'arte] (2026-11-27)
- **Storia e rievocazioni** [rievocazione storica] · Grande Guerra · medioevo e rinascimento · commemorazioni · presepi viventi [presepio vivente, figuranti] · presepi inclusivi · passeggiate sulle tracce dei pittori dell'Ottocento [Ciardi] · cortei natalizi della tradizione [ciarastea, Giuseppe e Maria cercano alloggio] (2026-11-23)
  · feste di San Martino con il santo a cavallo e il taglio del mantello [San Martin, San Martino a cavallo] · feste contadine con mostra di animali e benedizione delle macchine agricole [festa contadina, benedizione dei trattori]
- **Patrimonio e tradizioni** · dialetto e cultura veneta · artigianato tradizionale · musei etnografici
  · palio e giochi tradizionali di paese [palio delle botti, transumanza delle botti] · musei d'impresa con aperture mensili [museo del caffe', primo sabato del mese] · aperture di palazzi delle fondazioni [Ca' Spineda, visita gratuita]
  · falo' dell'Epifania [panevin, pan e vin, brusa la vecia] (2026-11-22): i programmi escono a fine dicembre, cercare dal 20/12
- **Tecnologia e scienza** · maker e robotica · divulgazione scientifica · eventi di astronomia
  · lezioni pubbliche dei gruppi di astrofili [lezioni per il pubblico, astrofili]
  · serate di osservazione degli astrofili trevigiani [astrofili trevigiani, appuntamenti] (sito solo http, WebFetch in loop: 2026-11-17) · lezioni-concerto e lezioni di musica nelle fondazioni [lezione di musica, Landscapes] (2026-11-17) · sport e statistica [basket in numeri, dati] (2026-11-27)
- **Comunita'** · incontri di quartiere · volontariato · feste delle associazioni · gruppi di conversazione · pesche di beneficenza e feste solidali nei locali [pesca benefica, AIL] (2026-11-28) · feste del Ringraziamento delle comunita' straniere [Thanksgiving] (2026-11-28)
  · iniziative della rete provinciale Pari Opportunita' verso il 25 novembre [25 novembre, panchina rossa, walk in red] · serate di prevenzione e salute dei comuni [si-cura, prevenzione, serata informativa] · donazioni di sangue AVIS con colazione [donazione, avis] · gruppi di lettura delle biblioteche [gruppo di lettura]
  · conferenze nei musei legate alle mostre in corso [conferenza, museo, Gypsotheca] (2026-11-26)

## Musica e party (`musica`)

- **Concerti** [concerto, live] · rock e indie · cantautori · jazz [jam session] · blues · classica e cameristica · cori gospel nei quartieri [gospel, coro] · concerti bandistici di Natale [banda in festa] (2026-11-23) · concerti di musiche da film a Capodanno [colonne sonore, Capodanno in teatro] (2026-11-28)
  · stagioni cameristiche delle orchestre con sale proprie [I Virtuosi Italiani, Teatro delle Voci, Teatro Eden] (2026-11-18) → ivirtuositaliani.eu · concerti narrati con attore e strumento antico [concerto narrato, viola da gamba]
  · lirica e opera · musica corale [coro, rassegna corale] · bande e fanfare · musica sacra e organo · metal
  · hip hop e rap · elettronica live · world e folk · tributi e cover band
  · concerti tributo nei teatri [tribute show, tribute band, omaggio a] (2026-11-16) → TicketOne /cityd/<comune>/concerti-55/, canzoni.it · stagioni musicali dei cinema-teatri [cinema teatro, Oderzo suona] (2026-11-16) → cinemacristallo · cori gospel in tournee [mass choir] (2026-11-16)
  · stagioni liriche dei teatri comunali [stagione lirica, opera, operetta] (2026-11-15) → risorse.teatrostabileveneto · concerti di Natale gospel [gospel, concerto di Natale] (2026-11-15)
  · date dei tour nei club con pacchetti meet and greet [meet and greet, club tour] (2026-11-24)
- **Festival musicali** · estivi all'aperto · rassegne d'autunno · festival di musica antica
  · festival di musica a cappella [a cappella, VivaVoce] (2026-11-15) · festival organistici dei comuni [festival organistico, organi storici] (2026-11-15)
  · stagioni sinfoniche delle orchestre regionali [Filarmonia Veneta, Gocce musicali] (2026-11-15) → classicalive
- **Serate e club** [DJ set, serata, party] · techno e house · reggaeton e latino · anni 80-90-2000 · aperitivo con DJ · Capodanno in piazza con dj e spettacolo piromusicale [Capodanno in piazza, piromusicale] (2026-11-23) · feste diurne per over 30 [daytime party] (2026-11-25)
  · feste a tema dei club (cartoni, film, tributi) [party a tema, shrek party] · anniversari dei locali con dj ospiti gratuiti [celebration weekend] · serate Remember della vigilia di Natale [remember]
- **Ballo** [serata danzante] · liscio · balli latini · swing e lindy hop · tango [milonga settimanale, pomeridiana di tango] · balli di gruppo · balere e orchestre di liscio [calendario per locale, serata di San Silvestro in balera] (2026-11-25)
- **Musica partecipata** · open mic · karaoke · jam session aperte · drum circle [cerchio di percussioni] · rassegne di cori scolastici in piazza [cori delle scuole, Natale] (2026-11-23)
  · open mic di stand-up comedy [open mic comicita'] · jam nelle sale prove comunali [free jam session, Progetto Giovani]
  · concerti in cuffia [silent concert, silent wifi]
  · concerti da ascoltare a occhi chiusi con poesia e coro [a occhi chiusi] (2026-11-17)
  · camminate cantate e cori itineranti di Natale [Cantar Nadal, canti di Natale] (2026-11-26)

## Sagre e cibo (`sagre-feste`)

- **Sagre** [sagra, festa paesana, festa patronale] · di prodotto (zucca, radicchio, castagne e marroni, asparagi,
  funghi, baccala', pesce, spiedo, polenta) · patronali · feste di frazione
  · feste dei santuari mariani di novembre [Madonna della Salute] · sagre di San Martino
  · feste di quartiere dei circoli NOI [circolo NOI, festa di quartiere] · feste di Santa Caterina e Sant'Andrea
    (fine novembre, Barbisano, Colbertaldo, Solighetto) · cene del lesso e dello spiedo delle Pro Loco · tombole e tombolate di Santo Stefano e dell'Epifania negli oratori [tombolata, NOI] (2026-11-27)
- **Vino e bevande** [degustazione, cantine aperte] · Prosecco e colline del Conegliano Valdobbiadene · mostre dei vini · degustazioni di Natale in cantina [brindisi, bollicine di Natale] · serate del vino novello
  · Veneto Wine Stars (Conegliano) · Go To Veneto (Strada del Conegliano Valdobbiadene) · birrifici artigianali
  (non sono eventi le degustazioni in cantina su appuntamento del calendario del Consorzio)
  · birre artigianali · distillati e grappa · cantine aperte
- **Cibo** · street food · cene a tema · corsi di cucina · mercati contadini con degustazioni · pranzi benefici con pasta di tradizione [pranzo solidale, magnar ben] · mostre mercato del radicchio [mostra del radicchio, Fiori d'Inverno] (gennaio)
  · cenoni di Capodanno con spettacolo nei teatri e nei circoli [cenone di Capodanno, cena spettacolo] (2026-11-18) → teatrodelpane.it
  · mostre mercato dell'olio nelle ville [Olio in Villa] (fine novembre) · te' e merende al museo [te' al museo] (2026-11-17)
- **Feste stagionali** · Halloween · San Martino · Natale (feste in piazza) · Carnevale (sfilate) · Panevin ed · accensione dell'albero e delle luminarie [accensione albero, luminarie] · sculture di ghiaccio dal vivo [scultori del ghiaccio] (2026-11-23) · presepi itineranti e diffusi nei comuni [presepi itineranti, presepi diffusi] (2026-11-28)
  Epifania · feste di primavera e d'estate
  · accensione dell'albero e apertura dei villaggi di Natale (fine novembre) [accensione albero, villaggio di Natale]
  · feste del Ringraziamento e dell'agricoltura a San Martino con trattori d'epoca [festa del Ringraziamento, palio della gerla]
  · fiere di Santa Lucia (13 dicembre) [Santa Lucia, fiera]
  · passaggio di San Nicolo' per le vie e nelle frazioni (4-6 dicembre) [San Nicolo', passaggio] (2026-11-26)
  · Krampus nei mercatini di fine novembre [Krampus, Pelund] (2026-11-26) · Panevin nelle frazioni (5 gennaio) [Panevin]

## Spettacoli (`teatro-spettacoli`)

- **Teatro** [spettacolo, stagione teatrale] · prosa · teatro dialettale · commedia · teatro ragazzi (vedi Famiglie)
  · monologhi di teatro civile nei cinema di paese [Tina Merlin, Vajont, cinema Manzoni] (2026-11-19) · spettacoli di parole e musica con giornalisti e cantautori [Concita De Gregorio] (2026-11-19)
  · teatro di strada · improvvisazione
  · stagioni di prosa dei teatri stabili con turni di abbonamento [stagione di prosa, biglietti e abbonamenti, repliche] · stagioni dei teatri comunali di paese nel circuito Arteven [stagione teatrale, auditorium, Vivaticket]
  · rassegne di teatro amatoriale nei paesi [rassegna teatrale, compagnie amatoriali, auditorium] · letture teatrali per le ricorrenze civili [4 novembre] · spettacolo di Capodanno a teatro [Capodanno a teatro] · teatro classico a puntate sui miti greci [rassegna Class]
- **Comicita'** · stand-up comedy [repliche pomeridiane e serali] · cabaret · serate comiche a puntate nei ridotti [Funny Friday] · teatro dialettale comico [Legnanesi] · creator e youtuber a teatro · comici in tournee nei teatri comunali [Teatro Accademia] · stand-up nei club musicali (2026-11-25)
- **Danza** · balletto · danza contemporanea · saggi delle scuole di danza · balletti di Natale in tournee [Schiaccianoci] · compagnie di balletto russo in tournee [Il lago dei cigni]
  · balletti di Natale delle compagnie italiane nei teatri commerciali [Balletto di Siena, Schiaccianoci] (2026-11-18) → scoppiospettacoli · spettacoli natalizi per famiglie nei teatri associativi tra Natale e Capodanno [villaggio incantato]
- **Circo e arti di strada** · circo contemporaneo · giocoleria · festival di artisti di strada · circo di Natale in tournee [circo acrobatico, Christmas edition] · clown e circo musicale nei palazzetti
  · circhi di Natale in tournee [circo di Natale, Circusfans tournee] · trampolieri e artisti di strada nei mercatini di Natale [trampolieri, mercatino di Natale]
- **Cinema** [proiezione, rassegna, cineforum] · cineforum · cinema all'aperto · festival di cortometraggi · rassegne di film natalizi in biblioteca [Cinenatale] (2026-11-28)
  · cineforum di vallata [Cineforum Quartier del Piave, rassegna d'autunno] · cinema a prezzo ridotto in piu' sale [Martedi' al Cinema 4 euro] · proiezioni gratuite per ricorrenze [25 novembre, ingresso gratuito]
  · documentari · prime visioni con ospiti · documentari con gli autori in sala
- **Musical e operetta** · musical · operetta · tributi musicali a teatro [Battisti, Michael Jackson] · spettacoli K-pop per famiglie
  · grandi musical in tournee nei palazzetti [Notre Dame de Paris, Prealpi SanBiagio Arena] (2026-11-19) → TicketOne · illusionisti e prestigiatori nei teatri commerciali [L'Illusionista] (2026-11-19)

## Famiglie e bambini (`famiglie-bambini`)

- **Laboratori** [laboratorio per bambini] · creativi · scientifici · di lettura · di cucina · laboratori di cucina per bambini nelle feste di piazza [laboratorio di tiramisu'] (2026-11-28)
  · laboratori del sabato pomeriggio nei musei civici [laboratori weekend, Museo Bailo, Santa Caterina] · visite guidate per famiglie alle mostre
  · laboratori a pagamento delle fondazioni culturali nelle feste (Natale, Carnevale) [rassegna Non e' una barba, Oderzo Cultura] (2026-11-19) · notti al museo in pigiama per bambini [superpoteri in pigiama]
  · giochi di indagine per famiglie nelle ville venete a Natale [caccia al tesoro, detective, Villa di Maser] (2026-11-20)
- **Letture e biblioteche** [ora del racconto, letture animate] · nati per leggere · laboratori creativi nei musei civici [mosaico, Piccoli Klimt] · rassegne invernali di incontri con autori [Winter & Writers] (2026-11-25)
  · gruppi di lettura per ragazzi 11-14 anni · gruppi di lettura degli adulti [book club, libro del mese] · letture di San Nicolo' [Sannicolibri] · cicli di incontri con autori in biblioteca [Il Veneto legge, BiblioMarca]
- **Spettacoli per bambini** · teatro ragazzi · burattini e marionette · magia · spettacoli con videoproiezioni in piazza [spettacolo in piazza, videoproiezioni] (2026-11-28)
  · rassegne domenicali dei teatri comunali [teatro ragazzi, domeniche a teatro, Ragazzi che Teatro]
  · letture animate con musica dal vivo
  · rassegne comunali di prosa per famiglie la domenica pomeriggio [Domenica a teatro, ingresso 8 euro] (2026-11-16) → trevisoeventi stagione Trevignano Cultura · spettacoli natalizi per ragazzi nei teatri commerciali [K-pop, missione Natale] (2026-11-16)
- **All'aperto** · fattorie didattiche · cacce al tesoro · feste di quartiere per famiglie · parchi avventura · laboratori nei garden center [laboratorio bambini garden] · piantumazione di bulbi per bambini · villaggi delle zucche [villaggio delle zucche] (ottobre)
  · ruote panoramiche e piste di ghiaccio dei Natali in centro [ruota panoramica, pista di pattinaggio] (2026-11-18) · case di Babbo Natale nei cortili dei centri storici [casa di Babbo Natale]
- **Ricorrenze** · Halloween per bambini · Santa Lucia · Babbo Natale e villaggi di Natale · Carnevale dei bambini · arrivo della Befana in piazza [Befana, carboncini] · pomeriggi a tema in biblioteca [Natale a Hogwarts] (2026-11-23) · mercatini natalizi di autoproduzioni nei club [DIY Xmas Market] · feste a tema nella sera di Natale (2026-11-25)
  · cassette delle lettere di Babbo Natale e slitte virtuali nelle piazze [slitta virtuale] (2026-11-18)
  · accensione del presepe e dell'albero (8 dicembre) · mostre di presepi (date dell'anno escono a fine novembre) · San Nicolo' (6 dicembre)
  · slitta e giro di Babbo Natale per il paese (24 dicembre) [slitta di Babbo Natale] (2026-11-26)
  · letture per 0-3 anni in biblioteca [letture cucu', nati per leggere] · Babbo Natale nelle sedi di Alpini e Pro Loco [Babbo Natale incontra i bambini] (2026-11-26) · Babbo Natale per le vie delle frazioni la Vigilia [Babbo Natale per le vie] (2026-11-27) · calze e animazione della Befana nei teatri e auditorium comunali [incanti di Epifania, calza della Befana] (2026-11-27)

## Mercatini e fiere (`mercatini-fiere`)

- **Mercatini** [mercatino] · antiquariato e modernariato [ricorrenza mensile] · hobbistica e artigianato · antiquariato mensile nei borghi del centro [Cose d'Altri Tempi, quarta domenica] · mercatini solidali dei laboratori per persone con disabilita' [mercatino solidale] (2026-11-23)
  · vintage e usato · mercatini di Natale · baratto e swap party · libri usati
  · mercatini di Natale di paese gia' da meta' novembre [mercatino di Natale <comune>]
  · mercatini natalizi a weekend nei borghi [Stelle a Natale, artigianato vivo] (primi due weekend di dicembre)
  · mercatini di Natale nei giorni festivi (8, 13 e 20 dicembre) con accensione dell'albero e cori [mercatini di Natale Valdobbiadene] (2026-11-19) · antiquariato in piazza nei giorni di dicembre [Fiera del Trovarobe, mercatino dell'Antico]
- **Mercati agricoli** · mercato contadino · Campagna Amica · mercati straordinari di Natale e di stagione
  · mostre mercato di prodotti d'autunno [profumi e sapori] (i mercati settimanali fissi sono un servizio, non un evento)
  · giornate dell'olio nuovo nelle ville con i produttori [olio in villa, olio nuovo] (2026-11-20)
- **Fiere** [fiera, expo] · fiere storiche di paese · fiere di settore · fiere dell'auto e moto d'epoca · fiere del
  · mercatini di Natale comunali con casette assegnate per avviso pubblico [avviso casette mercatini di Natale] (2026-11-18): l'avviso del Comune da' le date ufficiali
  fumetto e del gioco
  · rievocazioni storiche delle fiere antiche [antica fiera, rievocazione storica] · mostre mercato dei prodotti d'autunno [profumi e sapori d'autunno]
  · fiere agricole di dicembre nei quartieri fieristici [fiera dell'agricoltura, macchine agricole, zootecnia] (2026-11-22) → fieresantalucia.it · padiglioni dei prodotti tipici dentro le fiere agricole [ex Filande] (2026-11-22) · fiere di inizio anno dei quartieri fieristici [fiera di gennaio, fiera di primavera] (2026-11-22)
- **Collezionismo** · numismatica e filatelia · vinili e dischi · giocattoli d'epoca · collezionismo militare [militaria, Milipiave]
  · mercatini mensili di antiquariato nei centri storici [antiquariato seconda domenica, Portobuffole', Collalto] · mostre mercato di antiquariato nei borghi con passeggiate storiche [antiquariato Collalto, lavatoio] · tornei di carte delle sagre [torneo di briscola, burraco di San Martino]
  · mercatini con pausa invernale (dicembre sospeso) [sospeso a dicembre, ultima domenica del mese] (2026-11-22): controllare la regola prima di aggiungere le date · mercatini dell'usato di fine gennaio [ripresa mercatini gennaio] (2026-11-22)
  · mercatini benefici parrocchiali delle domeniche d'Avvento [mercatino d'Avvento, mercatino benefico] (2026-11-26)

## Business e formazione (`business`)

- **Convegni e conferenze** [convegno, seminario] · impresa · innovazione · sostenibilita'
  · incontri tecnici per agricoltori (CIA, Coldiretti, Condifesa) · incontri d'impresa su Eventbrite [Eventbrite business gratuiti]
  · festival dell'educazione [EducarSi', 4passiFestival]
  · convegni tecnici delle aziende in sedi museali [convegno tecnico, iscrizione, Volteco] · summit dell'imprenditoria con ospiti dello sport [Let's Experience] (2026-11-20)
- **Formazione** [workshop, corso, masterclass] · digitale e marketing · lingue · fotografia · scrittura
  · corsi delle Camere di commercio (spesso solo e-learning) [CCIAA formazione] (2026-11-15) · minirassegne culturali infrasettimanali nelle ville comunali [DeINDOPARA] (2026-11-15)
- **Lavoro** [job day, career day, recruiting day] · job day e fiere del lavoro · orientamento universitario
  · career day di universita' e ITS
  · job meeting itineranti delle universita' [Job Meeting, career day] (in provincia rari, resa 0 il 2026-11-17)
- **Startup e innovazione** · hackathon · pitch · open day di incubatori · talk ispirazionali nei campus [inspirational talk, H-FARM] (2026-11-15)
- **Networking** · aperitivi di networking · eventi di associazioni di categoria
  · business night delle associazioni di commercianti [Confcommercio business night] · incontri Confapi
  · assemblee di categoria aperte su registrazione [assemblea panificatori, Federmoda] · giornate di networking nei concessionari [networking d'impresa, Centro Porsche] (2026-11-20)

## Natura e benessere (`natura-outdoor`)

- **Escursioni** [escursione guidata, passeggiata naturalistica] · camminate in collina e sul Montello · lungo i fiumi · ciaspolate guidate sul Grappa [ciaspolata Monte Grappa] (2026-11-28: solo operatori commerciali senza date)
  (Sile, Piave) · notturne e al chiaro di luna · birdwatching · forest bathing · camminate di nordic walking aperte a tutti [nordic walking, camminata d'autunno]
  · passeggiate urbane ai margini della citta' (Legambiente)
  · camminate abbinate alle mostre mercato d'autunno [camminata, colline nascoste] · percorsi tra i presepi nel bosco del Montello [presepi nel bosco] (dicembre)
  · escursioni delle Pro Loco del primo weekend di dicembre [Boschi a Natale] (2026-11-24) · grotte e forre [Grotte del Caglieron] · sentieri dei carbonai e dei mulini [carbonai, mulini] · parchi archeologici didattici [Livelet, palafitte]
- **Ambiente** · pulizia di parchi e fiumi · piantumazioni · educazione ambientale · domeniche ecologiche con distribuzione di piantine [domenica ecologica, alberi in pianura] · Puliamo il Mondo di Legambiente [puliamo il mondo] (settembre-ottobre)
  · raccolte di rifiuti di Plastic Free e FIPSAS [plastic free, zeroplastic]
  · raccolte dei volontari Plastic Free [cleanup Plastic Free] (elenco solo con registrazione: 2026-11-17) · gruppi di ecovolontari dei comuni [Passi Puliti, ecovolontari] · Festa dell'albero del 21 novembre [Giornata nazionale degli alberi, festa degli alberi]
- **Benessere** [yoga, meditazione] · yoga all'aperto · meditazione · pilates · camminata nordica [nordic walking]
  · bagni di gong e suono [bagno di gong, master gong] (2026-11-15) · giornate dello yoga cittadine [YogaDay] (2026-11-15)
- **Orti e giardini** · giardini aperti · corsi di orticoltura · mostre di piante e fiori · laboratori con gli apicoltori [apicoltore, cera d'api] · corsi di potatura invernale dei comuni e delle associazioni [corso di potatura, innesti] (2026-11-27: solo PDF fuori provincia)
- **Animali** · eventi cinofili [raduno cani, sfilata cani, mostra canina] · fattorie aperte · serate su fauna e migrazioni [rapaci, birdwatching] · mostre ornitologiche · benedizione degli animali [Sant'Antonio Abate, gennaio]

## Voci aggiunte (registro)

Una riga per notte: `- AAAA-MM-GG · +N voci · dove: Sport > Arrampicata (+3), Musica > Ballo (+2) ...`

- 2026-10-30 · prima versione dell'albero, scritta a partire dalle 9 categorie del sito
- 2026-10-31 · +12 voci · dove: Arte e cultura > Conferenze (+2), Tecnologia e scienza (+1), Musica > Musica partecipata (+2), Spettacoli > Cinema (+1), Famiglie > Spettacoli per bambini (+2), Natura > Escursioni (+1), Business > Lavoro (+1), Sagre (+2)
- 2026-11-11 · +11 voci · dove: Musica > Ballo (+2), Spettacoli > Comicita' (+3), Musical e operetta (+2), Natura > Animali (+3), Spettacoli > Danza (+1, balletto classico in tournee)
- 2026-11-02 · +12 voci · dove: Spettacoli > Teatro (+4), Comicita' (+1), Danza (+1), Famiglie > Laboratori (+2), Mercatini (+1), Fiere (+2), Collezionismo (+1)
- 2026-11-05 · +11 voci · dove: Sport > Eventi per chi guarda (+4), Arti marziali (+1), Equitazione (+1), Business > Networking (+2), Natura > Ambiente (+1), Animali (+1), Arte e cultura > Visite guidate (+1)
- 2026-11-06 · +11 voci · dove: Sport > Motori (+3), Sagre > Vino e bevande (+3), Mercatini > Mercati agricoli (+2), Business > Convegni e conferenze (+3)
- 2026-11-25 · +10 voci · dove: Musica > Ballo (+2), Serate e club (+1), Spettacoli > Comicita' (+2), Famiglie > Letture e biblioteche (+2), Ricorrenze (+2), Arte e cultura > Visite guidate (+1)
- 2026-11-24 · +10 voci · dove: Natura > Escursioni (+4), Arte e cultura > Mostre (+2), Visite guidate (+2), Musica > Concerti (+1), Sport > Corsa (+1)
- 2026-11-12 · +11 voci · dove: Sport > Arrampicata (+2), Montagna ed escursionismo (+2), Sport di precisione (+3), Sagre (+4)
- 2026-11-07 · +10 voci · dove: Sport > Sport per tutti (+3), Arte e cultura > Storia e rievocazioni (+2), Spettacoli > Circo e arti di strada (+2), Mercatini > Collezionismo (+3)
- 2026-11-08 · +10 voci · dove: Sport > Racchetta (+2), Arte e cultura > Patrimonio e tradizioni (+3), Musica > Musica partecipata (+2), Spettacoli > Cinema (+3)
- 2026-11-09 · +11 voci · dove: Arte e cultura > Mostre (+4), Spettacoli > Teatro (+2), Sport > Sport d'acqua (+2), Sport di squadra (+2), Natura > Escursioni (+1)
- 2026-11-13 · +11 voci · dove: Arte e cultura > Visite guidate (+2), Mostre (+1), Conferenze e incontri (+2), Sagre > Feste stagionali (+3), Natura > Escursioni (+2), Orti e giardini (+1)
- 2026-11-14 · +11 voci · dove: Sport > Sport invernali (+2), Ginnastica e danza sportiva (+2), Arte e cultura > Comunita' (+4), Musica > Serate e club (+3)
- 2026-11-15 · +10 voci · dove: Musica > Festival musicali (+3), Musica > Concerti (+2), Business > Startup (+1), Business > Formazione (+2), Natura > Benessere (+2)
- 2026-11-17 · +11 voci · dove: Arte e cultura > Tecnologia e scienza (+2), Mostre (+1), Business > Lavoro (+1), Sagre > Cibo (+2), Natura > Ambiente (+3), Mercatini (+1), Musica > Musica partecipata (+1)
- 2026-11-16 · +10 voci · dove: Sport > Ciclismo (+3), Musica > Concerti (+3), Arte e cultura > Conferenze e incontri (+2), Famiglie > Spettacoli per bambini (+2)
- 2026-11-18 · +11 voci · dove: Arte e cultura > Libri e lettura (+2), Spettacoli > Danza (+2), Musica > Concerti (+2), Mercatini > Fiere (+1), Famiglie > All'aperto (+2), Famiglie > Ricorrenze (+1), Sagre > Cibo (+1, cenoni di Capodanno nei teatri)
- 2026-11-19 · +12 voci · dove: Famiglie > Laboratori (+2), Mercatini (+2), Spettacoli > Musical (+2), Teatro (+2), Sport > Arti marziali (+2), Equitazione (+2)
- 2026-11-20 · +10 voci · dove: Arte e cultura > Mostre (+3), Famiglie > Laboratori (+1), Mercatini > Mercati agricoli (+1), Business > Convegni (+2), Networking (+2), Sport > Eventi per chi guarda (+1)
- 2026-11-21 · +10 voci · dove: Sport > Arrampicata (+1), Motori (+2), Arte e cultura > Storia e rievocazioni (+3), Sagre > Vino e bevande (+2), Spettacoli > Circo e arti di strada (+2)

- 2026-11-22 · +10 voci · dove: Sport > Corsa (+3), Mercatini > Fiere (+3), Collezionismo (+2), Sport > Racchetta (+1), Arte e cultura > Patrimonio e tradizioni (+1)
- 2026-11-23 · +11 voci · dove: Sport > Sport d'acqua (+1), Sport invernali (+1), Musica > Musica partecipata (+1), Concerti (+2), Serate (+1), Sagre > Feste stagionali (+2), Arte e cultura > Storia e rievocazioni (+1), Famiglie > Ricorrenze (+2), Mercatini (+1); nate dal programma del Natale a Treviso
- 2026-11-26 · +11 voci · dove: Sagre > Feste stagionali (+3), Famiglie (+3), Sport > Corsa (+2), Musica > Musica partecipata (+1), Arte e cultura > Conferenze (+1), Mercatini > Mercatini di Natale (+1); nate dal calendario del Natale di Farra di Soligo, da TrovaSagre e dall'agenda del Museo Canova

- 2026-11-27 · +10 voci · dove: Arte e cultura > Visite guidate (+1), Conferenze e incontri (+2), Tecnologia e scienza (+1), Sagre (+1), Famiglie > Ricorrenze (+2), Natura > Orti e giardini (+1), Sport > Arrampicata (+1), Sport > Sport per tutti (+1, tornei di calcio balilla e burraco solidali negli oratori)
- 2026-11-28 · +10 voci · dove: Sport invernali (+1), Arte e cultura > Conferenze (+1), Comunita' (+2), Musica > Concerti (+1), Sagre > Feste stagionali (+1), Spettacoli > Cinema (+1), Famiglie > Laboratori (+1), Spettacoli per bambini (+1), Natura > Escursioni (+1)
