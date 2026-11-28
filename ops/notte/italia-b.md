# Agente italia-b, notte del 2026-11-28 (Toscana e Marche)

Province: LU, AR, LI, SI, PT, PO, GR, MS (Toscana), AN, PU (Marche). Prima di stanotte nessun capoluogo aveva eventi
futuri sul sito (`--comune` = 0), tranne Ancona (39 eventi di Marche Teatro dal giro: non toccati).

## Numeri
- Eventi in `config/notte/italia-b-eventi.yaml`: **380** (`python -m pipeline.notte --controlla italia-b`: "Parti valide").
  Nessun doppione con sito, redazione o parte di italia-a (controllo `site_duplicates` + `duplicates`).
- 374 eventi su 380 con lat/lon (OpenStreetMap via Nominatim, incrociato con l'indirizzo della fonte ufficiale quando c'era).
  Senza coordinate: 5 eventi generici di San Vincenzo (la fonte non da' il luogo) e il mercato antiquario attorno alla
  cattedrale di Lucca (piazza San Martino non trovata).
- Correzioni: nessuna (nessun evento esistente in queste province). Niente file `italia-b-correzioni.yaml`.
- Ricerche: **86 su 125** (45 WebSearch, 40 WebFetch, 1 lettura con curl della home di toscanaspettacolo.it; un secondo
  curl sull'API WordPress e' stato negato dal permesso e non l'ho ripetuto). In piu' circa 95 chiamate a Nominatim
  dalla shell per le coordinate (1 ogni 4 secondi; molte risposte 629 per il traffico degli altri agenti).
- Eventi per ricerca: 4,4.

| Regione | Prov. | Eventi | Comuni |
|---|---|---|---|
| Toscana | LU | 63 | Lucca 49, Viareggio 7, Pietrasanta 6, Castelnuovo di Garfagnana 1 |
| Toscana | MS | 41 | Massa 18, Carrara 12, Pontremoli 7, Fivizzano 4 |
| Toscana | LI | 41 | Livorno 26, San Vincenzo 9, Castagneto Carducci 6 |
| Toscana | SI | 41 | Siena 41 |
| Toscana | AR | 24 | Arezzo 16, Sansepolcro 7, Anghiari 1 |
| Toscana | PO | 23 | Prato 23 |
| Toscana | PT | 14 | Pistoia 13, Montecatini-Terme 1 |
| Toscana | GR | 10 | Grosseto 10 |
| Marche | PU | 69 | Pesaro 43, Urbino 8, Cagli 7, Fano 6, Urbania 4, San Lorenzo in Campo 1 |
| Marche | AN | 54 | Ancona 17, Jesi 9, Senigallia 7, Fabriano 6, Osimo 5, Chiaravalle 4, Corinaldo 3, Maiolati Spontini 3 |

Totale Toscana 257, Marche 123. Per categoria: soprattutto teatro-spettacoli (stagioni teatrali), poi musica,
famiglie-bambini, sagre-feste (Natale, Carnevale di Viareggio, Candele a Candelara), mercatini-fiere, arte-cultura.

Ambiti di categoria: AR Montagna ed escursionismo (CAI Arezzo, Monti Rognosi 6/12), MS Feste stagionali (Lunigiana:
Casa di Babbo Natale a Pontremoli, presepe vivente di Equi Terme, Sapori di Natale a Fivizzano), PU Mercati agricoli
(Campagna Amica, mercato coperto di via Giolitti: 7 date), SI Teatro (Teatri di Siena, 30 titoli). Cercati senza
risultati da fonte ammessa: LU Corsa, LI Circo e arti di strada (a Livorno niente; il circo l'ho trovato a Pistoia e
Arezzo), GR Motori, AN Eventi per chi guarda (Ancona in Serie D, nessun calendario ufficiale). **Non cercati**: PT
Montagna ed escursionismo, PO Storia e rievocazioni.

Comuni del piano non controllati (restano senza data): Fosciandora (LU); Caprese Michelangelo, Subbiano (AR);
Collesalvetti (LI); Castellina in Chianti, Cetona (SI); Larciano, Serravalle Pistoiese (PT); Vaiano, Carmignano (PO);
Monterotondo Marittimo, Montieri, Capalbio (GR); Monte Grimano Terme, Tavoleto (PU). Controllati con una ricerca senza
fonte ufficiale leggibile: Seravezza (pagina del Comune 403), Portoferraio, Chiusi, Montemurlo, Sirolo, Monte Roberto,
Mondolfo, Comano.

## Fonti nuove da catalogare (per ops/fonti.yaml; le migliori anche per le fonti del giro)
- **Fondazione Toscana Spettacolo, circuito teatrale regionale** | https://www.toscanaspettacolo.it/calendario/ |
  query "Fondazione Toscana Spettacolo calendario spettacoli" | ente (circuito) | Toscana, 10 province | WordPress con tipo
  `spettacolo` (`/spettacolo/<slug>/`, feed `/spettacoli-teatro-toscana/feed/`). **WebFetch la legge vuota** (3 prove:
  home, /calendario/, feed); con curl la home risponde (robots.txt: Allow /, blocca solo wp-admin ecc.). Candidata
  forte per il giro come raccoglitore html/wp-json (va provata `/wp-json/wp/v2/spettacolo`): vale quanto MyArteven per il
  Veneto. Da mettere in `ops/domini-illeggibili.yaml` per WebFetch.
- **AMAT, Platea delle Marche** | https://www.amatmarche.net/platea-delle-marche-3/ | query "amatmarche Platea delle
  Marche" | ente (circuito) | tutte le Marche | una pagina con tutte le repliche del circuito (data, ora, titolo,
  teatro, comune, scheda): 100 eventi di AN e PU in una lettura. In catalogo c'e' gia' solo la home AMAT: aggiornare
  l'url a questa pagina e proporla per il giro.
- **Teatri di Pesaro (AMAT e Comune)** | https://www.teatridipesaro.it/ | query "Teatri di Pesaro spettacoli" | teatro |
  Pesaro | schede `/spettacolo/<slug>/` (WordPress), 32 date fino a marzo senza orari in elenco.
- **Teatro del Giglio Lucca, stagione** | https://www.teatrodelgigliogiacomopuccini.it/it/cartellone/stagione/2026-2027/ |
  query "Teatro del Giglio Lucca stagione 2026-2027" | teatro | Lucca | elenco con date e ore di ogni replica.
- **Turismo Lucca, Lucca Magico Natale** | https://turismo.lucca.it/lucca-magico-natale-2026/ | query "Lucca Magico
  Natale 2026" | ufficio turistico (Comune di Lucca) | Lucca | calendario natalizio completo con ore e luoghi.
- **Arezzo Citta' del Natale, programma** | https://www.arezzocittadelnatale.it/programma/ | query "Arezzo Citta' del
  Natale programma" | ente (Comune) | Arezzo | eventi datati con ore e luogo (pagina lunga, leggere anche con offset).
- **Fiera Antiquaria di Arezzo** | https://fieraantiquaria.org/ | query "Fiera Antiquaria Arezzo prossima edizione" |
  organizzatore | Arezzo | date di ogni edizione mensile nelle news.
- **Fondazione Guido d'Arezzo, stagione di prosa** | https://www.fondazioneguidodarezzo.com/stagione-di-prosa-2026-2027/ |
  teatro | Arezzo (Petrarca, Mecenate) | calendario anche in `/calendario/categoria/teatro/`.
- **Cinema Teatro Dante Sansepolcro** | https://www.cinemateatrodante.net/teatro/stagione-teatrale/ | teatro | Sansepolcro.
- **CAI Arezzo** | https://www.caiarezzo.it/ | query "CAI Arezzo uscite" | associazione | AR | schede `/uscite/<slug>`
  con ritrovo, quote e iscrizione.
- **CAI Toscana, calendario regionale 2026 (PDF)** | https://organizzazione.cai.it/gr-toscana/wp-content/uploads/sites/66/2026/01/2026-Attivita-CAI-in-Toscana-Versione-per-Cellulare.pdf |
  associazione | tutta la Toscana | tutte le uscite delle sezioni toscane dell'anno (data, sezione, titolo, difficolta');
  si legge con pdftotext. Utile per scoprire; i dettagli vanno presi dalle schede delle sezioni.
- **Fondazione Teatro Goldoni Livorno** | https://www.goldoniteatro.it/spettacoli/ | gia' in catalogo: 40 date fino ad
  aprile, ma senza orari nell'elenco.
- **Visit San Vincenzo (Comune)** | https://visitsanvincenzo.it/it/calendario-eventi/eventi/ | ufficio turistico | San Vincenzo.
- **Comune di Castagneto Carducci, stagione Teatro Roma (PDF)** | https://www.visitcastagneto.com/visit/wp-content/uploads/2026/10/Stagione-Teatrale-2026-2027-Teatro-Roma-Castagneto-Carducci.pdf | teatro | LI.
- **Comune di Massa, stagione Teatro Guglielmi (PDF)** | https://www.comune.massa.ms.it/sites/default/files/2026-08/stagione%20prosa%20brochure%202026-27.pdf | teatro | Massa.
- **Comune di Carrara, stagione Teatro degli Animosi** | https://www.comune.carrara.ms.it/it/news/al-via-dal-23-ottobre-la-stagione-2026-27-del-teatro-degli-animosi | teatro | Carrara.
- **Lunigiana Land (Ambito turistico della Lunigiana, Unione dei Comuni)** | https://www.lunigiana.land/categoria-evento/eventi-locali/ |
  query "lunigiana.land eventi" | ufficio turistico | MS, 14 comuni | anche le categorie fiere, musica, arte e cultura.
- **Versiliana Festival (Teatro Comunale di Pietrasanta)** | https://versilianafestival.it/ | teatro | Pietrasanta.
- **Carnevale di Viareggio, sito ufficiale** | https://viareggio.ilcarnevale.com/news/ | organizzatore | Viareggio.
- **Comune di Siena, Siena Incanta** | https://comune.siena.it/novita/siena-incanta-si-accende-il-natale-siena-eventi-spettacoli-e-mostre-internazionali-le |
  comune | Siena | e la stagione dei Teatri di Siena: https://www.comune.siena.it/vivere-il-comune/eventi/stagione-teatrale-20262027-teatri-di-siena
- **Comune di Pistoia, Pistoia Citta' del Natale** | https://www.comune.pistoia.it/it/news/il-natale-e-di-tutt-pistoia-citta-del-natale-2026-oltre-un-mese-di-festa-cultura-e-divertimento-allinsegna-della-solidarieta | comune | Pistoia.
- **Teatri di Pistoia** | https://www.teatridipistoia.it/ | teatro | Pistoia | schede `/spettacoli/<slug>/`.
- **Teatro Metastasio Prato** | https://www.metastasio.it/ | query "Teatro Metastasio Prato" | teatro | Prato | la home
  elenca cartellone, MetRagazzi e progetti con date (orari standard 20.45, sab 19.30, dom 16.30).
- **Teatro degli Industri, Teatri di Grosseto (Comune)** | https://www.teatroindustri.it/ | teatro | Grosseto | schede `/evento/<slug>/`.
- **Ancona Tourism (Comune), Ancona che brilla** | https://anconatourism.it/news/ancona-che-brilla-2026-dalla-nuova-piazza-della-repubblica-si-accende-il-natale-ad-ancona/ | ufficio turistico | Ancona.
- **Comune di Fabriano, stagione Teatro Gentile** | https://comune.fabriano.an.it/novita/stagione-2026-27-del-teatro-gentile-di-fabriano/ | teatro | Fabriano.
- **Pro Loco di Candelara** | https://www.candelara.it/programma/ | pro loco | Pesaro.
- **Campagna Amica, mercati di Pesaro** | https://www.campagnamica.it/la-nostra-rete/mercato/mercato-coperto-di-pesaro/ |
  ente (Coldiretti) | Pesaro | schede dei mercati con giorni e orari (anche Agrimercato San Decenzio, Villa San Martino).
- **Montecatini Terme Tourism (Comune)** | https://montecatinitermetourism.com/events/ | ufficio turistico | Montecatini.

Nessuna fonte con JSON-LD o The Events Calendar verificata stanotte (non ho potuto provare le API dalla shell).

### Fonti non ammesse o da verificare (non usate, nessuna lettura oltre ai risultati di ricerca)
Aggregatori e testate visti nei risultati, da far verificare all'agente fonti (robots.txt e termini): seiversilia.it,
versiliabimbi.it, laversilia.it, visitlunigiana.it (non e' il portale dell'Ambito, che e' lunigiana.land),
sagretoscane.com, tempoliberotoscana.it, oksiena.it, sienafree.it, sienasociale.it, centritalianews.it, ilgiunco.net,
maremmanews.it, grossetonotizie.com, luccaindiretta.it, luccanews24.it, versiliapost.it, livornotoday.it,
arezzonotizie.it, lortica.it, notiziediprato.it, viverefano.it, fanoinforma.it, marcheinfinite.com, anconatoday.it.
`pipeline.fonti_vietate --url` le da' "ammesse (sito ufficiale)" per default perche' non sono in elenco: attenzione, per
la regola valgono come da verificare.

## Per ops/da-verificare.json (eventi visti solo su testate non verificate)
- Teatro Mascagni di Chiusi, stagione 2026/27: DILF con Pierpaolo Spollon 8/12, Antigone 26/1, La governante 14/2,
  Callas Callas Callas 6/3, Lettere a un giovane poeta 19/3 (sienafree, centritalianews); manca la pagina della
  Fondazione Orizzonti d'Arte.
- Sala Banti di Montemurlo: La meccanica della gelosia 11/12, Little Boy 29/1 (toscanatv, edicoladellenotizie).
- Teatro Dovizi di Bibbiena: La fiaba dell'amore lento 9/12 (La Nazione, arezzo24).
- Teatro Verdi di San Vincenzo: orario 21.15 dei cinque spettacoli (solo Il Telegrafo; sul sito del Comune non c'e').
- Mondolfo, Natale tra borgo e mare: Luminaria 29/11 ore 16, presepe vivente Presepepaese 26-27/12 (la pagina del
  Comune risponde 404).
- Teatro Verdi di Montecatini e San Silvestro al Teatro del Giglio di Lucca (solo LuccaInDiretta).

## Eventi scartati per luogo senza indirizzo (da riprendere con la scheda del teatro)
Loreto, Teatro Comunale Bastione Sangallo (Le voci del violino 29/11, La ferita la letizia 18/12, Appeso a un filo 17/1,
Venerdi' 13 13/3); Cupramontana, Teatro Concordia (Ti posso spiegare 28/11, Fra luna e mare 13/2, Naturale sconosciuto
6/3); Numana, Teatro Italia (L'attimo fuggente 15/1); Osimo, Loop Live Club (Fracasso 18/12); Sassocorvaro, Rocca
Ubaldinesca (Il naso d'argento 8/12); Lucca, Teatro Nieri di Ponte a Moriano (Histoire du soldat 29/11). Tutti da
https://www.amatmarche.net/platea-delle-marche-3/ e dal sito del Teatro del Giglio.

## Luoghi nuovi verificati (per config/luoghi.yaml)
Formato: nome | comune | indirizzo | lat, lon. Coordinate da OpenStreetMap (Nominatim), indirizzo dalla fonte
ufficiale dell'evento quando c'era, altrimenti dalla scheda OSM. Da controllare a vista: Teatro Mecenate (Arezzo, OSM
lo mette in via Dante, 2 km a sud-ovest del centro) e Teatro degli Animosi (OSM: via San Piero; il Comune scrive
Piazza De Andre' 1, stesso isolato).
- Teatro Guglielmi | Massa | Via Bastione | 44.0358879, 10.1410327
- Teatro dei Servi | Massa | Via Palestro | 44.0396936, 10.1425896
- Teatro degli Animosi | Carrara | Piazza Fabrizio De Andre' 1 | 44.0787911, 10.0967175
- Palazzo Comunale, Vetrina della Citta' | Pontremoli | Piazza della Repubblica | 44.377117, 9.882894
- Borgo di Equi Terme | Fivizzano | Equi Terme | 44.168239, 10.152565
- Centro storico di Fivizzano | Fivizzano | - | 44.23835, 10.12599
- Teatro del Giglio | Lucca | Piazza del Giglio | 43.8403991, 10.5030674
- Ex Cavallerizza | Lucca | Piazzale Verdi | 43.8428632, 10.4966412
- Mercato del Carmine | Lucca | Piazza del Carmine | 43.8442616, 10.5055879
- Piazza Napoleone | Lucca | Piazza Napoleone | 43.8413101, 10.5024855
- Piazza San Giusto | Lucca | Piazza San Giusto | 43.8418783, 10.5037734
- Piazza dell'Anfiteatro | Lucca | Piazza Anfiteatro | 43.8453496, 10.5061437
- Foro Boario | Lucca | Strada Provinciale Lucca-Camaiore | 43.8563229, 10.508217
- Oratorio degli Angeli Custodi | Lucca | Via dell'Angelo Custode | 43.8441744, 10.5080707
- Biblioteca Statale di Lucca | Lucca | Via San Giorgio | 43.8449331, 10.5013311
- Museo Nazionale di Palazzo Mansi | Lucca | Via Galli Tassi 43 | 43.8436183, 10.4990647
- Teatro di San Girolamo | Lucca | Via San Girolamo | 43.8402571, 10.5025027
- Auditorium della chiesa di San Francesco | Lucca | Piazza San Francesco | 43.8454916, 10.511405
- Piazza Santa Maria | Lucca | Piazza Santa Maria | 43.8477046, 10.5073699
- Teatro Comunale di Pietrasanta | Pietrasanta | Piazza Duomo 4 | 43.9577356, 10.2323801
- Teatro Alfieri | Castelnuovo di Garfagnana | Via Guglielmo Marconi | 44.1126141, 10.4124098
- Viali a mare | Viareggio | Viale Giosue' Carducci | 43.8759554, 10.2384624
- Gran Teatro Giacomo Puccini, Auditorium Enrico Caruso | Viareggio | Via delle Torbiere | 43.8342948, 10.3069417
- Piazza Sant'Agostino | Arezzo | Piazza Sant'Agostino | 43.462503, 11.8814945
- Piazza Guido Monaco | Arezzo | Piazza Guido Monaco | 43.4631545, 11.8785315
- Via Madonna Laura | Arezzo | Via Madonna Laura | 43.467842, 11.8827554
- Piazza Grande | Arezzo | Piazza Grande | 43.4647154, 11.8842838
- Teatro Petrarca | Arezzo | Via Guido Monaco 12 | 43.4647344, 11.8800665
- Teatro Mecenate | Arezzo | Via Dante | 43.4514596, 11.8616884
- Cinema Teatro Dante | Sansepolcro | Via XX Settembre 156 | 43.5699814, 12.1430615
- Riserva naturale dei Monti Rognosi | Anghiari | - | 43.5766958, 12.0027208
- Teatro Goldoni | Livorno | Via Carlo Goldoni | 43.5459241, 10.313889
- Duomo di Livorno | Livorno | Via Santa Giulia | 43.550099, 10.3095841
- Cinema Teatro Verdi | San Vincenzo | Via Vittorio Emanuele II | 43.1026771, 10.5390995
- Teatro Roma | Castagneto Carducci | Via Gramsci | 43.1602635, 10.6074866
- Teatro dei Rinnovati | Siena | Piazza del Campo 1 | 43.3180619, 11.3324676
- Teatro dei Rozzi | Siena | Via delle Terme 15 | 43.3189684, 11.3302334
- Piazza del Campo | Siena | Piazza del Campo | 43.3189467, 11.3316569
- Santa Maria della Scala | Siena | Piazza del Duomo 1 | 43.3171886, 11.3279706
- Palazzo Chigi Saracini | Siena | Via di Citta' | 43.3171232, 11.3309595
- Pian dei Mantellini | Siena | Pian dei Mantellini | 43.3145426, 11.3273351
- Cattedrale di Santa Maria Assunta | Siena | Piazza del Duomo | 43.3177948, 11.3290896
- Giardini de La Lizza | Siena | La Lizza | 43.3235451, 11.3260885
- Piazza Matteotti | Siena | Piazza Giacomo Matteotti | 43.3215554, 11.3286618
- Piazza del Duomo | Pistoia | Piazza del Duomo | 43.9336412, 10.917409
- Giardino di piazza della Resistenza | Pistoia | Piazza della Resistenza | 43.929298, 10.9205849
- Palazzo comunale, Sale Affrescate | Pistoia | Piazza del Duomo | 43.9336412, 10.917409
- Piccolo Teatro Mauro Bolognini | Pistoia | Via del Presto 5 | 43.9344344, 10.9167755
- Teatro Il Funaro | Pistoia | Via del Funaro | 43.9376993, 10.9201532
- Piazza del Popolo | Montecatini-Terme | Piazza del Popolo | 43.8829828, 10.771231
- Teatro Metastasio | Prato | Via Benedetto Cairoli | 43.8797415, 11.0994773
- Teatro Fabbricone | Prato | Via Ferdinando Targetti | 43.8908634, 11.0998529
- Teatro Magnolfi | Prato | Via Piero Gobetti | 43.8829718, 11.1053604
- Museo del Tessuto | Prato | Via Puccetti 3 | 43.8765212, 11.0982478
- Teatro degli Industri | Grosseto | Via Giuseppe Mazzini 101 | 42.7602463, 11.1117822
- Teatro Moderno | Grosseto | Via Tripoli | 42.7640147, 11.1152224
- Teatro Tullio Giacconi | Chiaravalle | Corso Giacomo Matteotti | 43.5999718, 13.3253684
- Teatro La Fenice | Senigallia | Via Cesare Battisti 24 | 43.7125046, 13.2182501
- Teatro Goldoni | Corinaldo | Via del Teatro 1 | 43.64932, 13.04549
- Teatro Gentile da Fabriano | Fabriano | Via Gentile da Fabriano 1 | 43.3365268, 12.9051479
- Teatro Studio Valeria Moriconi | Jesi | Via Posterma | 43.5246377, 13.2454791
- Teatro Pergolesi | Jesi | Piazza della Repubblica | 43.5218747, 13.2439244
- Teatro La Nuova Fenice | Osimo | Piazza Guglielmo Marconi | 43.4856056, 13.4844019
- Teatro Spontini | Maiolati Spontini | Via Gaspare Spontini | 43.477338, 13.1188525
- Piazza della Repubblica, scalinata del Teatro delle Muse | Ancona | Piazza della Repubblica | 43.6190546, 13.5098727
- Chiesa del Gesu' | Ancona | Piazza Benvenuto Stracca | 43.6226743, 13.5115039
- Borgo di Varano | Ancona | - | 43.5694069, 13.5442005
- Mole Vanvitelliana | Ancona | - | 43.614367, 13.5044233
- Montesicuro | Ancona | - | 43.553211, 13.4616056
- Piazza Roma | Ancona | Piazza Roma | 43.6178592, 13.5130692
- Teatro Sperimentale | Ancona | Via Redipuglia 59 | 43.6135194, 13.5154073
- Museo Archeologico Nazionale delle Marche | Ancona | Via Gabriele Ferretti 6 | 43.6234055, 13.5107468
- Corso Garibaldi | Ancona | Corso Giuseppe Garibaldi | 43.6175018, 13.514641
- Cattedrale di San Ciriaco | Ancona | Piazza del Duomo | 43.6253314, 13.5102303
- Forte Altavilla | Ancona | Pietralacroce | 43.6026298, 13.5426119
- Porto Antico, Arco di Traiano | Ancona | Molo Nord | 43.6252721, 13.5065081
- Teatro Rossini | Pesaro | Piazzale Carlo Albani 1 | 43.9078818, 12.9087047
- Teatro Sperimentale | Pesaro | Via Gioacchino Rossini | 43.9103068, 12.9133822
- Chiesa della Santissima Annunziata | Pesaro | Via dell'Annunziata 25 | 43.9115255, 12.9125387
- Mercato coperto Campagna Amica | Pesaro | Via Giovanni Giolitti 214/220 | 43.8961795, 12.9084175
- Borgo di Candelara | Pesaro | - | 43.858604, 12.8897537
- Teatro della Fortuna | Fano | Piazza XX Settembre 1 | 43.8439657, 13.0175208
- Teatro Sanzio | Urbino | Via Giacomo Matteotti | 43.7242602, 12.635457
- Teatro Comunale | Cagli | Piazza Papa Nicolo' IV | 43.5455763, 12.6474839
- Teatro Bramante | Urbania | Piazza San Cristoforo | 43.6678961, 12.5216017
- Teatro Mario Tiberini | San Lorenzo in Campo | Via Mario Tiberini 3 | 43.604517, 12.9448542

## Voci nuove per ops/categorie-ricerca.md (proposte, non scritte)
1. Spettacoli > Teatro > circuiti teatrali regionali di Toscana e Marche [Fondazione Toscana Spettacolo, AMAT Platea delle Marche]
2. Spettacoli > Teatro > stagioni teatrali in PDF dei comuni [stagione teatrale 2026/2027 pdf Comune di]
3. Spettacoli > Teatro > stagioni OFF per la generazione Z [Z Generation Meets Theatre, stagione OFF]
4. Spettacoli > Circo e arti di strada > circo contemporaneo sotto chapiteau nelle piazze a Natale [chapiteau piazza Natale circo contemporaneo]
5. Spettacoli > Circo e arti di strada > circo natalizio nelle piazze dei centri storici [Xmas Circus, circo in piazza]
6. Sagre e cibo > Feste stagionali > corsi mascherati del Carnevale [Carnevale di Viareggio corsi mascherati, carri allegorici]
7. Sagre e cibo > Feste stagionali > feste delle candele nei borghi [Candele a Candelara, spegnimento luci borgo]
8. Sagre e cibo > Feste stagionali > case di Babbo Natale nei palazzi comunali [Magica Casa di Babbo Natale, villaggio di Natale]
9. Mercatini e fiere > Mercati agricoli > mercati coperti di Campagna Amica [mercato coperto Campagna Amica, giovedi e sabato]
10. Mercatini e fiere > Antiquariato > fiere antiquarie mensili dei capoluoghi [Fiera Antiquaria di Arezzo, prima domenica del mese]
11. Mercatini e fiere > Artigianato > mercati medievali rievocati in piazza [Mercato nel Campo, mercato medievale]
12. Arte e cultura > Storia e rievocazioni > presepi viventi nei forti e nei borghi [presepe vivente Forte Altavilla, Equi Terme]
13. Arte e cultura > Storia e rievocazioni > rievocazioni del presepe di Greccio [Anno Domini 1223, San Francesco presepe]
14. Sport > Montagna ed escursionismo > calendari regionali CAI in PDF [Attivita' CAI in Toscana calendario]
15. Musica > Concerti > stagioni concertistiche delle accademie musicali [Micat in Vertice Accademia Chigiana]
16. Famiglie e bambini > Spettacoli per bambini > rassegne regionali di teatro per famiglie [Andar per Fiabe AMAT, MetRagazzi]

## Lezioni
- I circuiti teatrali regionali rendono di piu': AMAT Platea delle Marche 100 eventi in una lettura, Teatri di Siena
  30 titoli. In Toscana la Fondazione Toscana Spettacolo non e' leggibile da WebFetch, ma i Comuni pubblicano le
  stagioni FTS in PDF o in una news (Massa, Carrara, Castagneto): una lettura per teatro.
- I programmi del Natale dei Comuni capoluogo (Siena, Lucca, Pistoia, Arezzo, Ancona) danno 15-50 eventi con ore e
  luoghi in una lettura: cercarli con "Natale 2026" tra virgolette e il nome del programma.
- Nominatim dalla shell rifiuta molte richieste (HTTP 629) quando piu' agenti lavorano insieme: serve una pausa di 4
  secondi e una seconda passata; i nomi di piazza comuni (piazza del Duomo, corso Garibaldi, piazza Matteotti) senza CAP
  portano in un altro comune della provincia (Pescia, Arcevia, Piancastagnaio): mettere sempre il CAP.
- Le ricerche su comuni piccoli (Monte Roberto, Sirolo, Fosciandora) non trovano pagine ufficiali: meglio spendere
  sulle pagine di circuito e sui portali turistici d'ambito (lunigiana.land).

## Problemi
- toscanaspettacolo.it: WebFetch restituisce pagina vuota (3 prove). comune.prato.it: 503 due volte (la pagina del Natale
  2026 di Prato non e' stata letta). comune.seravezza.lucca.it: 403. comune.mondolfo.pu.it: 404 sulla news del Natale.
- Il compito diceva che la shell non raggiunge i siti, ma la raggiunge: ho letto con curl solo la home di
  toscanaspettacolo.it; il secondo curl (API) e' stato negato e da li' ho usato solo WebSearch e WebFetch (piu'
  Nominatim per le coordinate, come da metodo).
- Molti teatri (Goldoni di Livorno, Teatri di Pesaro, Industri, Teatri di Siena) non danno l'ora negli elenchi: gli
  eventi hanno solo la data. Il giro, leggendo le schede, puo' completare gli orari.
