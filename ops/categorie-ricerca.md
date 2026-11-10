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
- **Ciclismo** [gran fondo, cicloturistica, randonnée, gravel]
  - strada · mountain bike [XC, enduro, marathon MTB] · gravel · ciclocross · e-bike · BMX
  - cicloturistiche ed eroiche · pedalate per famiglie · bike test e raduni
- **Arrampicata** [arrampicata, climbing, boulder, falesia]
  - boulder [contest boulder, open boulder] · lead [difficolta'] · speed · falesia [raduno in falesia]
  - palestre indoor (open day, corsi base) · ice climbing · gare FASI
- **Montagna ed escursionismo** (vedi anche Natura) [escursione CAI, uscita sociale]
  - escursioni guidate · via ferrata · scialpinismo · ciaspolate [racchette da neve] · alpinismo
- **Sport d'acqua** [regata, gara di nuoto] (in autunno rara: nessun evento il 2026-11-09)
  · campionati di canottaggio di fondo sul Sile [canottieri, tricolori di fondo] · meeting di nuoto nelle piscine comunali [swim cup, trofeo]
  - nuoto in piscina · nuoto in acque libere · canoa e kayak · rafting · SUP [stand up paddle] · canottaggio
  - vela · pesca sportiva
- **Sport di squadra** [torneo, partita, campionato]
  - calcio · calcio a 5 · basket · pallavolo · beach volley · rugby · pallamano · hockey · baseball e softball
  - rugby di Serie A Elite in casa [calendario federugby, Mogliano] · Champions League di pallavolo femminile [CEV, Palaverde]
- **Racchetta** [torneo, open] · tennis · padel · ping pong · badminton · pickleball
  · tornei open FITP di padel [calendario tornei padel FITP Veneto, PDF regionale] · esibizioni ed eventi nei club [padel cup, clinic]
- **Arti marziali e combattimento** [stage, torneo, open day] · judo · karate · taekwondo · boxe · kickboxing · scherma
  · gare regionali FIJLKAM [fijlkam calendario gare Veneto]
- **Sport invernali** · sci alpino · sci di fondo · snowboard · pattinaggio su ghiaccio
- **Motori** [raduno, rally, gara] · rally · motocross · enduro moto · auto e moto d'epoca (raduni) · karting
  · calendario ACI Sport del mese [acisport calendari] · mostre scambio di auto e moto d'epoca · autocross
- **Equitazione** [concorso ippico] · salto ostacoli · endurance · passeggiate a cavallo · palio
  · concorsi FISE del Veneto [equiresults calendario, rideup]
- **Sport di precisione** · tiro con l'arco · golf · bocce · biliardo · freccette
- **Ginnastica e danza sportiva** · ginnastica artistica e ritmica · danza sportiva · cheerleading
- **Sport tradizionali e popolari** · palio e giochi storici · tiro alla fune · corsa nei sacchi
  · giochi popolari dentro le sagre (pignatte, corsa nei sacchi, partita delle vecchie glorie) · palio di Sant'Andrea (Solighetto) · Panevin e foghera (5-6 gennaio)
- **Eventi per chi guarda** [partita, match] · partite di serie A-B-C delle squadre locali · grandi eventi sportivi
  · basket di Serie A al Palaverde [Treviso Basket calendario] · rugby URC e Challenge Cup a Monigo [Benetton Rugby calendario]
  · pallavolo A1 femminile al Palaverde [Imoco] · calcio di Serie C allo stadio Tenni [Treviso calcio]
- **Sport per tutti** · open day delle societa' · giornate dello sport · sport adattato e paralimpico
  · corse libere gratuite del sabato mattina [parkrun Treviso, Parco dello Storga] · social run dei locali e dei negozi di sport [social run, run club] · camminate dei Babbi Natale [corsa dei Babbi Natale, Santa Klaus run]

## Arte e cultura (`arte-cultura`)

- **Mostre** [mostra, esposizione, vernissage, inaugurazione] · arte antica · arte contemporanea · fotografia
  · illustrazione e fumetto · design · collettive di artisti locali
  · manifesti pubblicitari e grafica d'epoca [Collezione Salce] · mostre in ville con parco [villa, giardino, biglietto mostra e parco] · collezioni private aperte nei fine settimana [apertura straordinaria, curatore] · premi di pittura delle Pro Loco [premio nazionale di pittura, acquerello]
- **Visite guidate** [visita guidata, passeggiata culturale] · centri storici · ville venete · chiese e abbazie · beni del FAI [fondoambiente eventi, I racconti del Memoriale]
  · percorsi sotterranei e mura · musei aperti la sera · giornate FAI e ville aperte
- **Libri e lettura** [presentazione del libro, incontro con l'autore, festival letterario] · gruppi di lettura · lettura di Dante canto per canto [Tutta la Commedia, lectura Dantis] · presentazioni in libreria universitaria
  · letture per adulti · poesia e slam poetry
- **Conferenze e incontri** [conferenza, talk, dialogo] · storia locale · scienza e divulgazione · filosofia
  · ambiente · astronomia (serate osservative) · festival di cittadinanza e cooperazione [festival, dialogo, 4passi]
  · teatro forum e incontri partecipati
- **Storia e rievocazioni** [rievocazione storica] · Grande Guerra · medioevo e rinascimento · commemorazioni
  · feste di San Martino con il santo a cavallo e il taglio del mantello [San Martin, San Martino a cavallo] · feste contadine con mostra di animali e benedizione delle macchine agricole [festa contadina, benedizione dei trattori]
- **Patrimonio e tradizioni** · dialetto e cultura veneta · artigianato tradizionale · musei etnografici
  · palio e giochi tradizionali di paese [palio delle botti, transumanza delle botti] · musei d'impresa con aperture mensili [museo del caffe', primo sabato del mese] · aperture di palazzi delle fondazioni [Ca' Spineda, visita gratuita]
- **Tecnologia e scienza** · maker e robotica · divulgazione scientifica · eventi di astronomia
  · lezioni pubbliche dei gruppi di astrofili [lezioni per il pubblico, astrofili]
- **Comunita'** · incontri di quartiere · volontariato · feste delle associazioni · gruppi di conversazione

## Musica e party (`musica`)

- **Concerti** [concerto, live] · rock e indie · cantautori · jazz [jam session] · blues · classica e cameristica
  · lirica e opera · musica corale [coro, rassegna corale] · bande e fanfare · musica sacra e organo · metal
  · hip hop e rap · elettronica live · world e folk · tributi e cover band
- **Festival musicali** · estivi all'aperto · rassegne d'autunno · festival di musica antica
- **Serate e club** [DJ set, serata, party] · techno e house · reggaeton e latino · anni 80-90-2000 · aperitivo con DJ
- **Ballo** [serata danzante] · liscio · balli latini · swing e lindy hop · tango · balli di gruppo
- **Musica partecipata** · open mic · karaoke · jam session aperte · drum circle [cerchio di percussioni]
  · open mic di stand-up comedy [open mic comicita'] · jam nelle sale prove comunali [free jam session, Progetto Giovani]
  · concerti in cuffia [silent concert, silent wifi]

## Sagre e cibo (`sagre-feste`)

- **Sagre** [sagra, festa paesana, festa patronale] · di prodotto (zucca, radicchio, castagne e marroni, asparagi,
  funghi, baccala', pesce, spiedo, polenta) · patronali · feste di frazione
  · feste dei santuari mariani di novembre [Madonna della Salute] · sagre di San Martino
- **Vino e bevande** [degustazione, cantine aperte] · Prosecco e colline del Conegliano Valdobbiadene · mostre dei vini
  · Veneto Wine Stars (Conegliano) · Go To Veneto (Strada del Conegliano Valdobbiadene) · birrifici artigianali
  (non sono eventi le degustazioni in cantina su appuntamento del calendario del Consorzio)
  · birre artigianali · distillati e grappa · cantine aperte
- **Cibo** · street food · cene a tema · corsi di cucina · mercati contadini con degustazioni · pranzi benefici con pasta di tradizione [pranzo solidale, magnar ben] · mostre mercato del radicchio [mostra del radicchio, Fiori d'Inverno] (gennaio)
- **Feste stagionali** · Halloween · San Martino · Natale (feste in piazza) · Carnevale (sfilate) · Panevin ed
  Epifania · feste di primavera e d'estate

## Spettacoli (`teatro-spettacoli`)

- **Teatro** [spettacolo, stagione teatrale] · prosa · teatro dialettale · commedia · teatro ragazzi (vedi Famiglie)
  · teatro di strada · improvvisazione
  · stagioni di prosa dei teatri stabili con turni di abbonamento [stagione di prosa, biglietti e abbonamenti, repliche] · stagioni dei teatri comunali di paese nel circuito Arteven [stagione teatrale, auditorium, Vivaticket]
  · rassegne di teatro amatoriale nei paesi [rassegna teatrale, compagnie amatoriali, auditorium] · letture teatrali per le ricorrenze civili [4 novembre] · spettacolo di Capodanno a teatro [Capodanno a teatro] · teatro classico a puntate sui miti greci [rassegna Class]
- **Comicita'** · stand-up comedy · cabaret · serate comiche a puntate nei ridotti [Funny Friday]
- **Danza** · balletto · danza contemporanea · saggi delle scuole di danza · balletti di Natale in tournee [Schiaccianoci]
- **Circo e arti di strada** · circo contemporaneo · giocoleria · festival di artisti di strada
  · circhi di Natale in tournee [circo di Natale, Circusfans tournee] · trampolieri e artisti di strada nei mercatini di Natale [trampolieri, mercatino di Natale]
- **Cinema** [proiezione, rassegna, cineforum] · cineforum · cinema all'aperto · festival di cortometraggi
  · cineforum di vallata [Cineforum Quartier del Piave, rassegna d'autunno] · cinema a prezzo ridotto in piu' sale [Martedi' al Cinema 4 euro] · proiezioni gratuite per ricorrenze [25 novembre, ingresso gratuito]
  · documentari · prime visioni con ospiti · documentari con gli autori in sala
- **Musical e operetta** · musical · operetta

## Famiglie e bambini (`famiglie-bambini`)

- **Laboratori** [laboratorio per bambini] · creativi · scientifici · di lettura · di cucina
  · laboratori del sabato pomeriggio nei musei civici [laboratori weekend, Museo Bailo, Santa Caterina] · visite guidate per famiglie alle mostre
- **Letture e biblioteche** [ora del racconto, letture animate] · nati per leggere
  · gruppi di lettura per ragazzi 11-14 anni · gruppi di lettura degli adulti [book club, libro del mese] · letture di San Nicolo' [Sannicolibri] · cicli di incontri con autori in biblioteca [Il Veneto legge, BiblioMarca]
- **Spettacoli per bambini** · teatro ragazzi · burattini e marionette · magia
  · rassegne domenicali dei teatri comunali [teatro ragazzi, domeniche a teatro, Ragazzi che Teatro]
  · letture animate con musica dal vivo
- **All'aperto** · fattorie didattiche · cacce al tesoro · feste di quartiere per famiglie · parchi avventura · laboratori nei garden center [laboratorio bambini garden] · piantumazione di bulbi per bambini · villaggi delle zucche [villaggio delle zucche] (ottobre)
- **Ricorrenze** · Halloween per bambini · Santa Lucia · Babbo Natale e villaggi di Natale · Carnevale dei bambini
  · accensione del presepe e dell'albero (8 dicembre) · mostre di presepi (date dell'anno escono a fine novembre) · San Nicolo' (6 dicembre)

## Mercatini e fiere (`mercatini-fiere`)

- **Mercatini** [mercatino] · antiquariato e modernariato [ricorrenza mensile] · hobbistica e artigianato · antiquariato mensile nei borghi del centro [Cose d'Altri Tempi, quarta domenica]
  · vintage e usato · mercatini di Natale · baratto e swap party · libri usati
  · mercatini di Natale di paese gia' da meta' novembre [mercatino di Natale <comune>]
- **Mercati agricoli** · mercato contadino · Campagna Amica · mercati straordinari di Natale e di stagione
  · mostre mercato di prodotti d'autunno [profumi e sapori] (i mercati settimanali fissi sono un servizio, non un evento)
- **Fiere** [fiera, expo] · fiere storiche di paese · fiere di settore · fiere dell'auto e moto d'epoca · fiere del
  fumetto e del gioco
  · rievocazioni storiche delle fiere antiche [antica fiera, rievocazione storica] · mostre mercato dei prodotti d'autunno [profumi e sapori d'autunno]
- **Collezionismo** · numismatica e filatelia · vinili e dischi · giocattoli d'epoca · collezionismo militare [militaria, Milipiave]
  · mercatini mensili di antiquariato nei centri storici [antiquariato seconda domenica, Portobuffole', Collalto] · mostre mercato di antiquariato nei borghi con passeggiate storiche [antiquariato Collalto, lavatoio] · tornei di carte delle sagre [torneo di briscola, burraco di San Martino]

## Business e formazione (`business`)

- **Convegni e conferenze** [convegno, seminario] · impresa · innovazione · sostenibilita'
  · incontri tecnici per agricoltori (CIA, Coldiretti, Condifesa) · incontri d'impresa su Eventbrite [Eventbrite business gratuiti]
  · festival dell'educazione [EducarSi', 4passiFestival]
- **Formazione** [workshop, corso, masterclass] · digitale e marketing · lingue · fotografia · scrittura
- **Lavoro** [job day, career day, recruiting day] · job day e fiere del lavoro · orientamento universitario
  · career day di universita' e ITS
- **Startup e innovazione** · hackathon · pitch · open day di incubatori
- **Networking** · aperitivi di networking · eventi di associazioni di categoria
  · business night delle associazioni di commercianti [Confcommercio business night] · incontri Confapi

## Natura e benessere (`natura-outdoor`)

- **Escursioni** [escursione guidata, passeggiata naturalistica] · camminate in collina e sul Montello · lungo i fiumi
  (Sile, Piave) · notturne e al chiaro di luna · birdwatching · forest bathing · camminate di nordic walking aperte a tutti [nordic walking, camminata d'autunno]
  · passeggiate urbane ai margini della citta' (Legambiente)
- **Ambiente** · pulizia di parchi e fiumi · piantumazioni · educazione ambientale · domeniche ecologiche con distribuzione di piantine [domenica ecologica, alberi in pianura] · Puliamo il Mondo di Legambiente [puliamo il mondo] (settembre-ottobre)
  · raccolte di rifiuti di Plastic Free e FIPSAS [plastic free, zeroplastic]
- **Benessere** [yoga, meditazione] · yoga all'aperto · meditazione · pilates · camminata nordica [nordic walking]
- **Orti e giardini** · giardini aperti · corsi di orticoltura · mostre di piante e fiori
- **Animali** · eventi cinofili [raduno cani, sfilata cani] · fattorie aperte · serate su fauna e migrazioni [rapaci, birdwatching]

## Voci aggiunte (registro)

Una riga per notte: `- AAAA-MM-GG · +N voci · dove: Sport > Arrampicata (+3), Musica > Ballo (+2) ...`

- 2026-10-30 · prima versione dell'albero, scritta a partire dalle 9 categorie del sito
- 2026-10-31 · +12 voci · dove: Arte e cultura > Conferenze (+2), Tecnologia e scienza (+1), Musica > Musica partecipata (+2), Spettacoli > Cinema (+1), Famiglie > Spettacoli per bambini (+2), Natura > Escursioni (+1), Business > Lavoro (+1), Sagre (+2)
- 2026-11-02 · +12 voci · dove: Spettacoli > Teatro (+4), Comicita' (+1), Danza (+1), Famiglie > Laboratori (+2), Mercatini (+1), Fiere (+2), Collezionismo (+1)
- 2026-11-05 · +11 voci · dove: Sport > Eventi per chi guarda (+4), Arti marziali (+1), Equitazione (+1), Business > Networking (+2), Natura > Ambiente (+1), Animali (+1), Arte e cultura > Visite guidate (+1)
- 2026-11-06 · +11 voci · dove: Sport > Motori (+3), Sagre > Vino e bevande (+3), Mercatini > Mercati agricoli (+2), Business > Convegni e conferenze (+3)
- 2026-11-07 · +10 voci · dove: Sport > Sport per tutti (+3), Arte e cultura > Storia e rievocazioni (+2), Spettacoli > Circo e arti di strada (+2), Mercatini > Collezionismo (+3)
- 2026-11-08 · +10 voci · dove: Sport > Racchetta (+2), Arte e cultura > Patrimonio e tradizioni (+3), Musica > Musica partecipata (+2), Spettacoli > Cinema (+3)
- 2026-11-09 · +11 voci · dove: Arte e cultura > Mostre (+4), Spettacoli > Teatro (+2), Sport > Sport d'acqua (+2), Sport di squadra (+2), Natura > Escursioni (+1)
