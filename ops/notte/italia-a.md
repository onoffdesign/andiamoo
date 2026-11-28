# Agente italia-a, notte del 2026-11-28 (seconda tornata)

Province: NO, VC, VB (Piemonte), GE, SV, SP, IM (Liguria), AO (Valle d'Aosta), FI, PI (Toscana).

## Numeri
- Eventi trovati e scritti: **474**. Di questi **175** erano gia' stati uniti dal coordinatore (una versione intermedia di
  `config/notte/italia-a-eventi.yaml` e' finita nel commit f8fdbff insieme a italia-b) e li ho tolti dal file per non
  duplicarli: nel file restano **299** eventi nuovi. `python -m pipeline.notte --controlla italia-a`: "Parti valide".
- Doppioni: controllati con lo stesso titolo e data su sito, redazione e altre parti della notte; nessuno.
- `config/notte/italia-a-correzioni.yaml`: non creato (nessuna correzione a eventi esistenti).
- Ricerche usate: **97 su 125** (WebSearch 52, WebFetch 45). In piu', a costo zero: 3 PDF letti con pdftotext dai file
  salvati da WebFetch (Teatro Verdi di Firenze, Turismo Novara, TRAC Festival) e circa 170 richieste a Nominatim dalla
  shell per le coordinate (1 al secondo; alcune risposte 629 per troppe richieste).
- Coordinate: 472 eventi su 474 hanno lat/lon; mancano solo i 2 della Sanremo Marathon (Pian di Poma non trovato).

| Prov. | Totale | gia' uniti | nel file | Fonti principali |
|---|---|---|---|---|
| NO | 136 | 0 | 136 | PDF di Turismo Novara (tutta la provincia), Distretto dei Laghi (Arona, Massino Visconti, Oleggio Castello) |
| VC | 83 | 6 | 77 | Visit Valsesia Vercelli (prossimi eventi, schede), Comune di Vercelli (stagione del Civico) |
| GE | 76 | 61 | 15 | Teatro Nazionale (44 titoli), Carlo Felice, Teatro della Tosse, Palazzo Ducale, Porto Antico (Circumnavigando) |
| FI | 47 | 26 | 21 | Teatro Verdi (PDF cronologico), Quartiere 4 del Comune, Maggio Musicale, mercato di Santa Croce |
| SV | 28 | 27 | 1 | Comune di Savona (stagione del Chiabrera) |
| SP | 26 | 14 | 12 | Comune della Spezia (prosa del Teatro Civico), TRAC Festival (pieghevole PDF) |
| VB | 24 | 8 | 16 | Distretto Turistico dei Laghi (stagione del Maggiore, calendario delle feste) |
| PI | 23 | 18 | 5 | Teatro di Pisa (solo dai risultati di ricerca), Turismo Pisa, Terre di Pisa |
| AO | 18 | 4 | 14 | Saison Culturelle, NaturAlp (ciaspolate guidate) |
| IM | 13 | 11 | 2 | Comune di Imperia (stagione del Cavour), Sanremo Marathon |

Per regione: **Piemonte 243**, **Liguria 143**, **Toscana 70**, **Valle d'Aosta 18** (totale 474; nel file 229, 30, 26, 14).
Categorie dei 299 eventi nel file: teatro-spettacoli 101, musica 59, arte-cultura 45, mercatini-fiere 38,
famiglie-bambini 20, natura-outdoor 16, sagre-feste 13, sport 7.

Comuni assegnati: con eventi Vicolungo (1), Trino (2), Santa Luce (1), Castelnuovo di Val di Cecina (1, Montecastelli
Pisano). Senza eventi pubblicabili: Nibbiola (Comune: solo eventi estivi), Barengo, Casanova Elvo, Tricerro, Malesco,
Cossogno, Pieve Vergonte, Rapallo (vedi sotto), Introd, Arnad, Antey-Saint-Andre' (solo testate), Vaglia, Rignano
sull'Arno, Pelago (pagine 2024-2025), San Giuliano Terme (programma 2025), Triora, Sarzana, Portovenere. Non cercati per
budget: Valbrevenna, Ceranesi, Cosseria, Castelbianco, Calizzano, Borghetto di Vara, Armo, Aquila d'Arroscia.
Ambiti: Circo e arti di strada GE (11 spettacoli) e SP (12, TRAC), Escursioni AO (14 ciaspolate), Corsa IM (2), Teatro FI
(26 al Verdi e Fiesole); resa 0: Escursioni NO, Convegni VC (solo 3 conferenze), Festival musicali VB, Ricorrenze SV,
Racchetta PI (solo Playtomic).

## Fonti nuove da catalogare (ops/fonti.yaml e fonti del giro)
Priorita' alta (molti eventi in una lettura):
- **Turismo Novara, PDF di tutti gli eventi** | https://www.turismonovara.it/it/eventimanifestazioni?PrintPDF=1 | query
  "turismonovara eventimanifestazioni PrintPDF" | ufficio turistico (ATL) | tutta la provincia NO | 274 eventi dal
  28/11 con comune, luogo e spesso indirizzo e ora, senza link: si legge con pdftotext sul file salvato da WebFetch.
  Il PC oggi porta solo 25 eventi di Novara da turismonovara.it: conviene un raccoglitore per il PDF (official_url
  https://www.turismonovara.it/it/doc/eventimanifestazioni, come gia' sul sito).
- **Visit Valsesia Vercelli, i prossimi eventi** | https://visitvalsesiavercelli.it/partecipa/eventi-e-news/i-prossimi-eventi/
  | query "visitvalsesiavercelli i prossimi eventi" | ufficio turistico (ATL Terre dell'Alto Piemonte) | VC (Vercelli,
  Valsesia, Trino) | circa 250 eventi fino ad aprile, ognuno con scheda /eventi/<slug>/, ora e luogo; pagina di 285.000
  caratteri (3 letture con offset 0, 100000, 200000). Candidata per sources.yaml (html; verificare se WordPress con
  The Events Calendar).
- **Distretto Turistico dei Laghi, calendario delle feste** | https://www.distrettolaghi.it/it/Natale_Capodanno_Epifania_26_27
  | query "distrettolaghi Natale Capodanno Epifania" | DMO | VB e nord NO | 75 eventi con slug delle schede
  /it/eventi/<slug>, senza orari ne' luoghi nel testo. Elenco generale /it/eventi con ?page=N. L'export
  /it/export_data_eventi risponde 500.
- **Teatro Nazionale di Genova, cartellone** | https://www.teatronazionalegenova.it/rassegne/cartellone-2026-27.htm | sede |
  GE | 44 titoli con teatro e date (orari nelle schede /eventi/2026-2027/<slug>.htm).
- **Porto Antico di Genova, Natale** | https://portoantico.it/magazine-news/eventi-natale-al-porto-antico-2026/ | ente |
  GE | 28 appuntamenti (Circumnavigando al Porto Antico).
- **Teatro Verdi di Firenze, cartellone cronologico (PDF)** |
  https://www.teatroverdifirenze.it/wp-content/uploads/2026/09/cronologico-1-settembre.pdf | sede | FI | tutta la
  stagione con le date (pdftotext), anche Off Verdi (Puccini, Fiesole). Schede /programma/<slug>/.
- **Comune di Firenze, Quartieri** | https://quartieri.comune.fi.it/dalle-redazioni/natale-al-q4-2026 (e
  /calendario-q4) | comune | FI | 30 appuntamenti di quartiere con orari; cercare le pagine dei Quartieri 1-3 e 5.
- **Terre di Pisa, eventi** | https://www.terredipisa.it/pisa-eventi/ | ufficio turistico (Camera di Commercio) | PI
  tutta la provincia | 36 eventi per lettura, "carica successivi" senza URL.
- **Turismo Pisa (Comune), eventi** | https://www.turismo.pisa.it/eventi/index.html/?cat=1 | comune | PI | 64 pagine, ma il
  testo letto non riporta i link delle schede.
- **Comune di Imperia, stagione teatrale** | https://comune.imperia.it/en/page/calendario-della-stagione-teatrale-2026-2027 |
  comune | IM | stagione del Cavour con orari.
- **Comune della Spezia, prosa del Civico** | https://www.comune.laspezia.it/novita/comunicati/teatro-civico-la-spezia-ora-stagione-di-prosa-26-27
  | comune | SP. **TRAC Festival** | https://teatrocivico.it/trac-festival-2026-2027/ (PDF
  https://teatrocivico.it/wp-content/uploads/2026/11/pieghevole-Web_TRAC-2026_2027-1-1.pdf) | sede | SP.
- **Comune di Savona, stagione del Chiabrera** | https://comune.savona.it/it/news/la-nuova-stagione-teatrale-2026-27-del-teatro-chiabrera
  | comune | SV; eventi del Comune https://www.comune.savona.it/index.php/it/eventi.
- **Comune di Vercelli, stagione del Civico** | https://www.comune.vercelli.it/novita/notizie/presentata-stagione-20262027-teatro-civico-vercelli-volti-noti-classici-passato | comune | VC.
- **Distretto dei Laghi, stagione del Maggiore** | https://www.distrettolaghi.it/it/eventi/verbania-stagione-teatrale-2026/2027-dove-nasce-la-gioia-di-capire-la-vita | DMO | VB.
- **Saison Culturelle** | https://saisonculturellevda.it/ | organizzatore (IMARTS per la Regione) | AO | mostra solo le
  prossime due settimane: da riaprire ogni notte.
- **NaturAlp, calendario** | https://www.naturalp.it/outdoor/naturalp-calendario/ (data con ?occurrence=AAAA-MM-GG) |
  organizzatore (guide) | AO e Ceresole Reale (TO) | ciaspolate a turni ogni giorno: tenere solo le date dei prossimi 30 giorni.
- **Palazzo Ducale, calendario** | https://palazzoducale.genova.it/en/events-calendar/ | sede | GE | solo mostre.
- **Hello Rapallo (Comune di Rapallo)** | https://hellorapallo.it/eventi/mese/2026-12/ | comune | GE | 17 eventi del mese,
  ma senza luogo nell'elenco (servono le schede).
- **Comune di Trino, eventi** | https://www.comune.trino.vc.it/eventi | comune | VC | schede Dettaglionews senza luogo.
Strutturati (JSON-LD o The Events Calendar): nessuno confermato stanotte. teatrodipisa.it usa The Events Calendar
(/calendario/...) ma /wp-json/tribe/events/v1/events risponde vuoto a WebFetch.

Da aggiungere a ops/domini-illeggibili.yaml: teatrodipisa.it (3 letture vuote: home, /calendario/elenco/, API tribe),
rivieradeifiori.travel (403 due volte, anche l'API), teatrodellatoscana.it (/it/in-programma in JavaScript, brochure PDF
oltre 10 MB), viottifestival.it (pagina vuota), regione.vda.it /cultura/eventi_spettacoli/saison_culturelle/ (404).

Fonti nuove viste solo nei risultati (aggregatori e testate, NON aperte, restano da verificare per l'agente fonti):
genova24.it, genovaquotidiana.com, telenord.it, 104news.it, genovatoday.it, italian-riviera.com, levantenews.it,
rivieraeventi.it, ivg.it, sanremonews.it, rivieratime.news, cittadellaspezia.com, portlogisticpress.it, contattoradio.it,
aostasera.it, aostanews24.it, gazzettamatin.com, radioflash.fm, radiogold.it, infovercelli24.it, primavercelli.it,
altopiemontemag.it, oblo.it, eventivalsesia.info, novaratoday.it, verbanonews.it, lanazione.it, firenzemadeintuscany.com,
inflorencetoday.com, ilcapoluogo.it, incontro.it, virgilio.it, mappaly.com, tuttomercatinidinatale.it, aspettandonatale.it,
marches-de-noel.fr, music-opera.com, songkick.com, biocorrendo.it, podistiche.it, calendario.podisti.net, finishers.com,
travel.thewom.it, capodanno31.com, guide-trek-alps.com (organizzatore: e' un sito ufficiale di guide, da usare in una
notte futura). Nessuna verifica di robots.txt fatta da me.

## Voci nuove per ops/categorie-ricerca.md (proposte, non scritte)
1. Spettacoli > Circo e arti di strada > festival di circo-teatro d'inverno sotto chapiteau [TRAC Festival, chapiteau, Circo Paniko] → teatrocivico.it
2. Spettacoli > Circo e arti di strada > festival internazionali di circo-teatro nelle feste [Circumnavigando, circo contemporaneo] → portoantico.it, teatrodellatosse.it
3. Spettacoli > Circo e arti di strada > parate sui trampoli per l'accensione delle luminarie [parata sui trampoli, accensione luminarie]
4. Natura e benessere > Escursioni > ciaspolate guidate a turni giornalieri nei parchi alpini [ciaspolata guidata, Gran Paradiso, Cervinia] → naturalp.it
5. Natura e benessere > Escursioni > serate di immagini di viaggio nelle sedi CAI [Immagini dal Mappamondo, sede CAI]
6. Sport > Corsa > maratone di dicembre in riviera [Sanremo Marathon, half marathon, 10K] → sanremomarathon.it
7. Sport > Corsa > passeggiate non competitive con i cani [Stracanina, passeggiata canina]
8. Musica e party > Festival musicali > festival d'organo itineranti nelle parrocchie della provincia [Vercelli Organ Festival]
9. Musica e party > Concerti > concerti del mattino nei ridotti dei teatri [Piccolo Coccia ore 11.30, concerto aperitivo]
10. Musica e party > Concerti > te' musicali pomeridiani nei club dei festival [Viotti Tea, ore 17]
11. Famiglie e bambini > Ricorrenze > discese della Befana dalle torri civiche [discesa della Befana, Torre dell'Angelo]
12. Famiglie e bambini > Ricorrenze > accensioni dell'albero nei quartieri con le scuole [Natale al Q4, accensione albero quartiere]
13. Business e formazione > Convegni e conferenze > convegni di storia nei seminari diocesani [Leone di Vercelli, seminario arcivescovile]
14. Arte e cultura > Mostre > mostre di presepi storici meccanici [presepi meccanici, museo di storia naturale]
15. Mercatini e fiere > mostre mercato di alto artigianato nelle stazioni storiche [Fashion in Flair, Stazione Leopolda]
16. Sagre e cibo > Feste stagionali > alberi di Natale fatti di trattori [AgriXmas, albero di trattori]
17. Spettacoli > Teatro > rassegne teatrali nei saloni delle Pro Loco di valle [Borgosesia in scena, Teatro Pro Loco]
18. Spettacoli > Cinema > cineforum con tre proiezioni a settimana nelle sale d'essai [Vipforum, Effetto notte]

## Luoghi nuovi (per config/luoghi.yaml; coordinate da Nominatim, indirizzi da pagina ufficiale e Nominatim)
- Teatro Carlo Felice, Passo Eugenio Montale 4, Genova, 44.4081451 8.9349002
- Teatro Ivo Chiesa, Piazza Borgo Pila 42, Genova, 44.4045240 8.9481031
- Teatro Eleonora Duse, Via Nicolo' Bacigalupo 6, Genova, 44.4112550 8.9382365
- Teatro Gustavo Modena e Sala Mercato, Piazza Gustavo Modena 3, Genova, 44.4105548 8.8897582
- Teatro della Tosse, Piazza Renato Negri 6, Genova, 44.4049524 8.9318247
- Palazzo Ducale, Piazza Giacomo Matteotti 9, Genova, 44.4075011 8.9332840
- Piazza delle Feste (Porto Antico), Genova, 44.4090664 8.9271757; Calata Mandraccio, 44.4075316 8.9268062
- Auditorium delle Clarisse, Rapallo, 44.3480586 9.2353879 (non usato)
- Teatro Verdi, Via Ghibellina 99, Firenze, 43.7700323 11.2606800
- Teatro Puccini, Via delle Cascine 41, Firenze, 43.7862068 11.2253943 (civico da confermare)
- Teatro di Fiesole, Largo Piero Farulli, Fiesole, 43.8078153 11.2960832
- Teatro del Maggio Musicale Fiorentino, Piazzale Vittorio Gui 1, Firenze, 43.7788769 11.2348742
- Piazza di Santa Croce, Firenze, 43.7688690 11.2614982
- Teatro Verdi, Via Palestro 40, Pisa, 43.7169705 10.4044717 (indirizzo da terredipisa.it)
- Palazzo Blu, Lungarno Gambacorti 9, Pisa, 43.7156502 10.3997452
- Museo Nazionale di San Matteo, Piazza San Matteo in Soarta 1, Pisa, 43.7147201 10.4078619
- Arsenali Repubblicani, Lungarno Ranieri Simonelli, Pisa, 43.7146873 10.3930979 (punto del lungarno; terredipisa scrive Via Bonanno)
- Stazione Leopolda, Pisa, 43.7085890 10.4056663; Certosa di Calci (Museo di Storia Naturale), Via Roma 79, Calci, 43.7221587 10.5227771
- Teatro Comunale Gabriello Chiabrera, Savona, 44.3105267 8.4814745 (indirizzo Piazza Diaz 2 da confermare)
- Teatro Cavour, Via Felice Cascione 35, Imperia, 43.8762622 8.0144903
- Teatro Civico, Corso Cavour 20, La Spezia, 44.1036188 9.8218535; Chapiteau TRAC ai Giardini, Viale Mazzini, 44.1037273 9.8237474
- Teatro Splendor, Via Festaz 82, Aosta, 45.7349785 7.3163232
- Teatro Civico, Via Monte di Pieta' 15, Vercelli, 45.3279312 8.4216795
- Centro Eventi Il Maggiore, Via San Bernardino 49, Verbania, 45.9306469 8.5718717
- Novara: Teatro Faraggiana (Via dei Caccia 1F) 45.4505976 8.6223707; Teatro Pernate Sant'Andrea (Via Turbigo 8, centro via)
  45.4605906 8.6771983; Conservatorio Cantelli 45.4444578 8.6197266; Cinema Araldo e Vip (Via Maestra 12) 45.4543702 8.6204178;
  Palazzo Natta 45.4463102 8.6226236; Biblioteca Negroni (Corso Cavallotti 4) 45.4467952 8.6227071; Spazio Nova (ex Caserma
  Passalacqua) 45.4408145 8.6244812; Teatro MP (Viale Giulio Cesare 378, centro via) 45.4354819 8.6308380; Teatro del
  Cuscino (Via Magalotti 11, centro via) 45.4416904 8.6045223
- Borgomanero: Teatro Rosmini 45.6964938 8.4682316; Cinema Teatro Nuovo (Via IV Novembre) 45.6946701 8.4551990; Villa
  Marazza (Viale Marazza 5) 45.7000768 8.4656488; Palazzo Tornielli 45.6986906 8.4631636
- Trecate: Cine Teatro Silvio Pellico (Piazza Cattaneo 24, punto della piazza) 45.4315108 8.7395227
- Galliate: Castello 45.4787468 8.6956298; Oratorio Beato Quagliotti (Sala Don Manfredda) 45.4761094 8.7005898
- Cerano: Sala Crespi 45.4105316 8.7834326; Ghemme: Palazzo Gallarati 45.5990797 8.4184008
- Vercelli: Museo Leone 45.3267582 8.4232615; Museo del Tesoro del Duomo 45.3298055 8.4234474; Chiesa di San Paolo
  45.3243991 8.4237435; San Pietro Martire 45.3269789 8.4197336; Basilica di Sant'Andrea 45.3287875 8.4191922; Museo
  Borgogna 45.3255807 8.4270413; Viotti Club (Via Ferraris 14) 45.3255631 8.4219635; Torre dell'Angelo / piazza Cavour
  45.3259757 8.4233894 (Nominatim manda "Piazza Cavour, Vercelli" a Buronzo: usare questo punto)
- Varallo: Teatro Civico 45.8143112 8.2537339; Palazzo d'Adda 45.8163046 8.2497826; Biblioteca Farinone Centa 45.8156144 8.2521379
- Borgosesia: Teatro Pro Loco 45.7164578 8.2782617; Cinema Lux 45.7166338 8.2740989; Gattinara: Auditorium Lux 45.6163672 8.3724446
- Trino: Auditorium Famiglia Tricerri (Via Vittime di Bologna 4, centro via) 45.1945700 8.3018707; Chiesa di Ognissanti 45.1938727 8.2948651

## Eventi visti ma non pubblicati (per ops/da-verificare.json o per una notte futura)
- Aosta, Marche' Vert Noel (piazza Chanoux, dal 21/11/2026): data di chiusura (6/1/2027) e orari solo su testate e
  sull'edizione 2023 del Comune; lovevda.it e' vietata.
- Antey-Saint-Andre', Note di Natale (5-7/12): solo aostasera.it e gazzettamatin.com.
- Genova: Christmas Concert (23/12) e New Year's Concert (1/1) del Carlo Felice solo su music-opera.com; Willy Ronis a
  Palazzo Ducale (18/12-29/3) "da confermare"; Casa di Babbo Natale a Palazzo Tursi senza date 2026; Hourvari (chapiteau
  di Voltri, 2-4/12) e Avamposto (3-5/12) senza luogo preciso; Mario Venuti e Tony Canto (28/11, La Claque).
- Firenze: stagione della Pergola (Lo Zar fino al 6/12, Don Chisciotte 19-20/12, Ritorno a casa Gori, Orlando furioso
  12-17/1) solo da mentelocale (vietata): teatrodellatoscana.it non si legge.
- Rapallo: 17 eventi di dicembre su hellorapallo.it (Clarisse, gospel, Orchestra del Carlo Felice 17/12) senza luogo
  nell'elenco: servono le schede.
- Savona: visite guidate al complesso di San Giacomo (2, 5, 6, 19, 27/12 ore 10): indirizzo non trovato (Nominatim 629).
- Pisa: Maratona di Pisa (20/12) e Mezza di San Miniato (8/12) senza luogo di partenza; mercatino di Calci (28-29/11).
- Imperia: Ospedaletti Run (5/12) e Trail del Ciapa' a Cervo (6/12) solo su testate.
- Vercelli: concerto di Capodanno del 31/12 al Civico (19.30 o 21: due orari diversi); Novara: Benvenuti a Windsor
  (5/12 o 12/12: date diverse nello stesso PDF), concerti del Coro CAI, Viaoxiliaquattro (4 serate), Cameri e
  Romentino: luoghi senza coordinate certe.

## Lezioni
- Gli elenchi delle ATL piemontesi valgono una provincia intera: il PDF "PrintPDF=1" di Turismo Novara (274 eventi) e la
  pagina "i prossimi eventi" di Visit Valsesia Vercelli (circa 250 con schede) hanno dato 213 eventi con 4 letture.
  Cercare lo stesso per Biella e Verbano (ATL Terre dell'Alto Piemonte, Distretto dei Laghi).
- I teatri liguri e toscani pubblicano la stagione sul sito del Comune (Savona, Imperia, La Spezia, Vercelli) con date e
  orari in una sola pagina: partire da li' invece che dal sito del teatro.
- Molti siti di teatri grandi sono illeggibili (teatrodipisa.it, teatrodellatoscana.it): i risultati di WebSearch con
  allowed_domains sul dominio ufficiale riportano comunque le date, ma senza orari.
- I PDF a immagine apparente (Teatro Verdi di Firenze) spesso hanno il testo vero: provare sempre pdftotext prima di
  estrarre le immagini.
- Nominatim: "Piazza X, Comune" sbaglia comune quando il nome della piazza esiste altrove (Vercelli, Savona, Firenze):
  aggiungere il CAP (13100, 17100, 50122) o usare un monumento vicino.

## Problemi
- La versione intermedia del mio file e' stata unita dal coordinatore mentre lavoravo (175 eventi). Ho tolto quegli
  eventi dal file: se il coordinatore unisce di nuovo, entrano solo i 299 nuovi. Il Banksy di Pisa unito ha l'indirizzo
  "Lungarno Ranieri Simonelli", coerente con il file attuale.
- Gli eventi del Teatro di Pisa (13) vengono dai risultati di WebSearch sul dominio ufficiale, perche' il sito non si apre:
  date senza orari, da ricontrollare quando il sito sara' leggibile.
- Molti eventi del Distretto dei Laghi (VB) e alcuni di Turismo Novara hanno come luogo il centro del paese o della
  frazione (orari non pubblicati): scritto nella fonte.
- Nessuna approvazione richiesta. Un tentativo di leggere pagine con curl dalla shell e' stato bloccato dal sistema dei
  permessi: ho letto tutto con WebSearch e WebFetch.
