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
- **Ogni notte**: aggiungi almeno 10 voci nuove, distribuite su piu' macro categorie, nate da cio' che hai visto
  nelle fonti (un tipo di evento che non c'era) o da ricerche mirate (federazioni sportive, calendari di settore,
  associazioni). Segna la data accanto alle voci nuove.
- **Resa per provincia**: in `ops/copertura.yaml` (sezione `categorie_<SIGLA>`) la data dell'ultima ricerca di ogni
  voce in quella provincia. Una voce cercata 3 volte senza eventi in una provincia si segna `rara` e si ricerca una
  volta al mese.
- **Dove cercare**: quando una voce ha una fonte che rende (federazione, calendario di settore), scrivila accanto
  con `→ fonte` e mettila in `ops/fonti.yaml`: la volta dopo non serve ricercare.

## Sport (`sport`)

- **Corsa** [podistica, non competitiva, camminata ludico-motoria, corsa su strada, fun run]
  - non competitive e marce [marcia, camminata, Fiasp] → calendariopodismo, podismoveneto
  - mezza maratona e maratona · 10 km · staffette · corse a tema (color run, notturne, in maschera)
  - trail running [trail, skyrace, ultratrail, vertical] → gotrail
  - corsa campestre [cross] · corsa in montagna
- **Ciclismo** [gran fondo, cicloturistica, randonnée, gravel]
  - strada · mountain bike [XC, enduro, marathon MTB] · gravel · ciclocross · e-bike · BMX
  - cicloturistiche ed eroiche · pedalate per famiglie · bike test e raduni
- **Arrampicata** [arrampicata, climbing, boulder, falesia]
  - boulder [contest boulder, open boulder] · lead [difficolta'] · speed · falesia [raduno in falesia]
  - palestre indoor (open day, corsi base) · ice climbing · gare FASI
- **Montagna ed escursionismo** (vedi anche Natura) [escursione CAI, uscita sociale]
  - escursioni guidate · via ferrata · scialpinismo · ciaspolate [racchette da neve] · alpinismo
- **Sport d'acqua** [regata, gara di nuoto]
  - nuoto in piscina · nuoto in acque libere · canoa e kayak · rafting · SUP [stand up paddle] · canottaggio
  - vela · pesca sportiva
- **Sport di squadra** [torneo, partita, campionato]
  - calcio · calcio a 5 · basket · pallavolo · beach volley · rugby · pallamano · hockey · baseball e softball
- **Racchetta** [torneo, open] · tennis · padel · ping pong · badminton · pickleball
- **Arti marziali e combattimento** [stage, torneo, open day] · judo · karate · taekwondo · boxe · kickboxing · scherma
- **Sport invernali** · sci alpino · sci di fondo · snowboard · pattinaggio su ghiaccio
- **Motori** [raduno, rally, gara] · rally · motocross · enduro moto · auto e moto d'epoca (raduni) · karting
- **Equitazione** [concorso ippico] · salto ostacoli · endurance · passeggiate a cavallo · palio
- **Sport di precisione** · tiro con l'arco · golf · bocce · biliardo · freccette
- **Ginnastica e danza sportiva** · ginnastica artistica e ritmica · danza sportiva · cheerleading
- **Sport tradizionali e popolari** · palio e giochi storici · tiro alla fune · corsa nei sacchi
- **Eventi per chi guarda** [partita, match] · partite di serie A-B-C delle squadre locali · grandi eventi sportivi
- **Sport per tutti** · open day delle societa' · giornate dello sport · sport adattato e paralimpico

## Arte e cultura (`arte-cultura`)

- **Mostre** [mostra, esposizione, vernissage, inaugurazione] · arte antica · arte contemporanea · fotografia
  · illustrazione e fumetto · design · collettive di artisti locali
- **Visite guidate** [visita guidata, passeggiata culturale] · centri storici · ville venete · chiese e abbazie
  · percorsi sotterranei e mura · musei aperti la sera · giornate FAI e ville aperte
- **Libri e lettura** [presentazione del libro, incontro con l'autore, festival letterario] · gruppi di lettura
  · letture per adulti · poesia e slam poetry
- **Conferenze e incontri** [conferenza, talk, dialogo] · storia locale · scienza e divulgazione · filosofia
  · ambiente · astronomia (serate osservative)
- **Storia e rievocazioni** [rievocazione storica] · Grande Guerra · medioevo e rinascimento · commemorazioni
- **Patrimonio e tradizioni** · dialetto e cultura veneta · artigianato tradizionale · musei etnografici
- **Tecnologia e scienza** · maker e robotica · divulgazione scientifica · eventi di astronomia
- **Comunita'** · incontri di quartiere · volontariato · feste delle associazioni · gruppi di conversazione

## Musica e party (`musica`)

- **Concerti** [concerto, live] · rock e indie · cantautori · jazz [jam session] · blues · classica e cameristica
  · lirica e opera · musica corale [coro, rassegna corale] · bande e fanfare · musica sacra e organo · metal
  · hip hop e rap · elettronica live · world e folk · tributi e cover band
- **Festival musicali** · estivi all'aperto · rassegne d'autunno · festival di musica antica
- **Serate e club** [DJ set, serata, party] · techno e house · reggaeton e latino · anni 80-90-2000 · aperitivo con DJ
- **Ballo** [serata danzante] · liscio · balli latini · swing e lindy hop · tango · balli di gruppo
- **Musica partecipata** · open mic · karaoke · jam session aperte

## Sagre e cibo (`sagre-feste`)

- **Sagre** [sagra, festa paesana, festa patronale] · di prodotto (zucca, radicchio, castagne e marroni, asparagi,
  funghi, baccala', pesce, spiedo, polenta) · patronali · feste di frazione
- **Vino e bevande** [degustazione, cantine aperte] · Prosecco e colline del Conegliano Valdobbiadene · mostre dei vini
  · birre artigianali · distillati e grappa · cantine aperte
- **Cibo** · street food · cene a tema · corsi di cucina · mercati contadini con degustazioni
- **Feste stagionali** · Halloween · San Martino · Natale (feste in piazza) · Carnevale (sfilate) · Panevin ed
  Epifania · feste di primavera e d'estate

## Spettacoli (`teatro-spettacoli`)

- **Teatro** [spettacolo, stagione teatrale] · prosa · teatro dialettale · commedia · teatro ragazzi (vedi Famiglie)
  · teatro di strada · improvvisazione
- **Comicita'** · stand-up comedy · cabaret
- **Danza** · balletto · danza contemporanea · saggi delle scuole di danza
- **Circo e arti di strada** · circo contemporaneo · giocoleria · festival di artisti di strada
- **Cinema** [proiezione, rassegna, cineforum] · cineforum · cinema all'aperto · festival di cortometraggi
  · documentari · prime visioni con ospiti
- **Musical e operetta** · musical · operetta

## Famiglie e bambini (`famiglie-bambini`)

- **Laboratori** [laboratorio per bambini] · creativi · scientifici · di lettura · di cucina
- **Letture e biblioteche** [ora del racconto, letture animate] · nati per leggere
- **Spettacoli per bambini** · teatro ragazzi · burattini e marionette · magia
- **All'aperto** · fattorie didattiche · cacce al tesoro · feste di quartiere per famiglie · parchi avventura
- **Ricorrenze** · Halloween per bambini · Santa Lucia · Babbo Natale e villaggi di Natale · Carnevale dei bambini

## Mercatini e fiere (`mercatini-fiere`)

- **Mercatini** [mercatino] · antiquariato e modernariato [ricorrenza mensile] · hobbistica e artigianato
  · vintage e usato · mercatini di Natale · baratto e swap party · libri usati
- **Mercati agricoli** · mercato contadino · Campagna Amica
- **Fiere** [fiera, expo] · fiere storiche di paese · fiere di settore · fiere dell'auto e moto d'epoca · fiere del
  fumetto e del gioco
- **Collezionismo** · numismatica e filatelia · vinili e dischi · giocattoli d'epoca

## Business e formazione (`business`)

- **Convegni e conferenze** [convegno, seminario] · impresa · innovazione · sostenibilita'
- **Formazione** [workshop, corso, masterclass] · digitale e marketing · lingue · fotografia · scrittura
- **Lavoro** · job day e fiere del lavoro · orientamento universitario
- **Startup e innovazione** · hackathon · pitch · open day di incubatori
- **Networking** · aperitivi di networking · eventi di associazioni di categoria

## Natura e benessere (`natura-outdoor`)

- **Escursioni** [escursione guidata, passeggiata naturalistica] · camminate in collina e sul Montello · lungo i fiumi
  (Sile, Piave) · notturne e al chiaro di luna · birdwatching · forest bathing
- **Ambiente** · pulizia di parchi e fiumi · piantumazioni · educazione ambientale
- **Benessere** [yoga, meditazione] · yoga all'aperto · meditazione · pilates · camminata nordica [nordic walking]
- **Orti e giardini** · giardini aperti · corsi di orticoltura · mostre di piante e fiori
- **Animali** · eventi cinofili [raduno cani, sfilata cani] · fattorie aperte

## Voci aggiunte (registro)

Una riga per notte: `- AAAA-MM-GG · +N voci · dove: Sport > Arrampicata (+3), Musica > Ballo (+2) ...`

- 2026-10-30 · prima versione dell'albero, scritta a partire dalle 9 categorie del sito
