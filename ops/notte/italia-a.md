# Agente italia-a, notte del 2026-11-28

Province: TV, CR, LC, LO, SO (Lombardia e Veneto), BO, MO, RE, PR, FC (Emilia-Romagna).

## Numeri
- Eventi in `config/notte/italia-a-eventi.yaml`: **350** (`python -m pipeline.notte --controlla italia-a`: "Parti valide").
  Prima di stanotte le 9 province nuove avevano 0 eventi futuri sul sito (`--comune` sui capoluoghi e su tutti i
  comuni aggiunti): nessun doppione.
- Per regione: **Emilia-Romagna 221**, **Lombardia 129**, **Veneto 0** (Treviso ha gia' 210 eventi; i 3 comuni e
  l'ambito non hanno dato eventi pubblicabili).
- `config/notte/italia-a-correzioni.yaml`: non creato (nessun evento esistente da correggere).
- Ricerche usate: **89 su 125** (WebSearch 33, WebFetch 56). In piu' 3 letture di robots.txt con curl (controllo
  delle fonti usate, non contate) e 2 pdftotext su PDF gia' salvati da WebFetch (costo zero).
- 223 eventi su 350 hanno lat/lon (vedi "Luoghi nuovi": coordinate da confermare); 5 senza indirizzo (vedi Problemi).

| Prov. | Eventi | Comuni | Categorie |
|---|---|---|---|
| RE | 79 | Reggio nell'Emilia 63, Reggiolo 5, Quattro Castella 2, Gualtieri 2, Campagnola, Cavriago, Bagnolo in Piano, Correggio, Casalgrande, Castelnovo di Sotto, Castellarano 1 | musica 24, teatro 19, arte-cultura 13 (8 mostre), mercatini 11, sagre-feste 5, famiglie 4, sport 3 |
| CR | 52 | Cremona 52 | musica 24, teatro 21, famiglie 3, arte-cultura 3, mercatini 1 |
| FC | 51 | Forli' 51 | teatro 19, musica 9, famiglie 7, arte-cultura 7, sagre-feste 4, mercatini 4, sport 1 |
| BO | 40 | Bologna 32, Casalecchio di Reno 5, Zola Predosa 3 | teatro 24, musica 10, arte-cultura 3, famiglie 2, mercatini 1 |
| SO | 36 | Sondrio 35, Talamona 1 | mercatini 12, teatro 10, musica 5, sagre-feste 4, sport 3, famiglie 1, arte-cultura 1 |
| MO | 32 | Modena 32 | musica 16, teatro 13, famiglie 2, mercatini 1 |
| LC | 22 | Lecco 22 | musica 12, mercatini 3, teatro 2, arte-cultura 2, famiglie 2, sagre-feste 1 |
| LO | 19 | Lodi 19 | teatro 12, musica 4, famiglie 3 |
| PR | 19 | Parma 19 | mercatini 7 (piazza Ghiaia, Mercanteinfiera), teatro 6, musica 5, famiglie 1 |
| TV | 0 | - | - |

Comuni assegnati controllati senza eventi pubblicabili: Resana (pagina eventi del Comune vuota, "0 eventi trovati";
nessun programma 2026 della Pro Loco), Bagnolo Cremasco, Casaletto Vaprio, Quintano, Nibionno, Pagnona, Barzago,
Borghetto Lodigiano (pagina Pro Loco del 2023), Terranova dei Passerini, Somaglia (Municipium `/it/events`: 5 eventi
senza ora ne' luogo), Castenaso (Pro Loco senza date), Grizzana Morandi, Maranello (nessun programma 2026; il
calendario Ferrari non si legge), Finale Emilia (pagina natalizia del 2023), Castelvetro di Modena, Bibbiano, Rolo,
Borgo Val di Taro e Pellegrino Parmense (brochure 2026 dell'Unione Valli Taro e Ceno senza date), Bertinoro (solo testate).
**Non controllati** (budget): Volpago del Montello, Revine Lago, Sernio, Tovo di Sant'Agata, Tizzano Val Parma,
Gatteo, Tredozio. Ambiti non cercati: Storia e rievocazioni (CR), Motori (LC), Ballo (LO), Ambiente (MO).
Ambiti cercati senza risultati: Convegni (TV; Treviso Swallowing Day del 12/12 ha la pagina di studioprogress.it
in 403), Lavoro (RE), Arrampicata (FC; Vertical Forli', via Pandolfa 42, nessuna gara nel periodo).

## Fonti nuove da catalogare
Strutturate o con elenchi completi (priorita' alta):
- **Fondazione I Teatri di Reggio Emilia** | https://www.iteatri.re.it/ (calendario completo:
  https://www.iteatri.re.it/rassegna/stagione-2026-2027/?month=all) | home con tutta la stagione fino a marzo
  (date senza orari) | sede | RE. robots.txt libero.
- **Reggio Emilia Welcome, calendari mensili** | https://www.reggioemiliawelcome.it/it/eventi/calendari-mensili/dicembre-2026
  | una pagina al mese con 60+ eventi di citta', provincia e mostre, spesso con orari e indirizzi | ufficio turistico | RE.
  robots.txt: Crawl-delay 120.
- **Teatro Ponchielli di Cremona** | https://www.teatroponchielli.it/ (calendario /calendario-eventi/) | home con tutta
  la stagione e gli orari | sede | CR. Rassegna Oltreibanchi = repliche scolastiche, da escludere.
- **Turismo Cremona** | https://www.turismocremona.it/it/evento/natale-cremona-2026 | schede evento con elenco degli
  altri eventi del mese | ufficio turistico | CR.
- **Forli' che Brilla** | https://forlichebrillaofficial.it/ | programma completo del Natale di Forli' (oltre 100
  appuntamenti con orari e luoghi, molti indirizzi) | comune/organizzatore | FC. Ripassare a meta' dicembre.
- **Accademia Perduta, Teatro Diego Fabbri** | https://accademiaperduta.it/teatro-diego-fabbri-forli/ | stagione con
  date e orari (21:00 salvo diversa indicazione), date senza anno | sede | FC. Pagine anche per Teatro Piccolo di Forli'
  e Teatro Dragoni di Meldola. teatrodiegofabbri.it risponde 503.
- **Emilia Romagna Teatro, Bologna e Modena** | https://bologna.emiliaromagnateatro.com/ ,
  https://modena.emiliaromagnateatro.com/ | home con la stagione (Arena del Sole, Moline, Storchi, Passioni) e schede
  `/spettacolo/<slug>/` con gli orari | sede | BO, MO. WordPress: provare /wp-json/tribe/events/v1/events.
- **Teatro Comunale Pavarotti-Freni di Modena** | https://www.teatrocomunalemodena.it/spettacoli/ | calendario con
  orari (pulsante "Carica altro": solo fino a meta' dicembre) | sede | MO.
- **Teatro Regio di Parma** | https://teatroregioparma.it/calendario/ (mesi con `?c_year=2027&c_month=1`) | sede | PR.
- **Teatro Due di Parma** | https://www.teatrodue.org/teatro-due-2026-2027/ | sede | PR.
- **Teatro alle Vigne di Lodi** | https://www.teatroallevigne.com/spettacoli/stagione-2026-2027/tutti | stagione
  completa con date e orari | sede | LO.
- **Teatro della Societa' di Lecco** | https://www.teatrosocietalecco.it/ | sede | LC.
- **Comune di Lecco, Lecco Magico Natale 2026** | https://www.comune.lecco.it/Novita/Notizie/Lecco-Magico-Natale-2026 |
  programma completo con orari | comune | LC.
- **Sondrio e Valmalenco eventi** | https://eventi.sondrioevalmalenco.it/ | 40 eventi in 120 giorni, schede con
  coordinate (la stagione del Teatro Sociale e' in /evento/stagione-teatrale-2025-2026, slug vecchio ma contenuto
  2026/27) | consorzio turistico | SO.
- **Bologna Cultura, calendario** | https://www.culturabologna.it/objects/calendario-bologna-cultura (giorni successivi
  `/calendar?range%5B0%5D=2026-12-05`) | 7 giorni per pagina, 100+ eventi con ora e luogo ma senza indirizzo |
  comune | BO (anche Casalecchio, Zola, Imola, Medicina). Ottima per il PC con i luoghi in config/luoghi.yaml.
- **Mercatino di Natale tirolese di Modena** | https://www.mercatinodinataletirolesemodena.it/spettacoli | organizzatore | MO.
- **Comune di Reggiolo, calendario annuale** | https://reggiolo-api.municipiumapp.it/s3/5684/allegati/calendario-eventi-reggiolo-2026.pdf
  | PDF con tutto il 2026 (pdftotext) | comune | RE.
- **Porte di Valtellina** | https://portedivaltellina.it/ | consorzio turistico di Morbegno (Talamona e bassa valle) | SO.

Utili ma non lette per intero o vuote:
- Comune di Parma, Natale 2026: https://www.comune.parma.it/it/Natale2026 rimanda a un catalogo FlippingBook in
  immagini (https://flippingbooks.comune.parma.it/cataloghi/natale-2026/, oltre 200 eventi): servono le immagini o il PDF.
- Emilia Romagna Turismo (https://emiliaromagnaturismo.it/), Appennino Bolognese (appenninobolognese.cittametropolitana.bo.it),
  Parma Welcome (pagina vuota a WebFetch), VisitModena (calendario in JavaScript), Comune di Modena (503),
  valtellina.it (403), Teatro Duse di Bologna (pagina vuota), turismovaltaro.it (brochure senza date).

Da verificare (viste solo nei risultati, non aperte): forlitoday.it, romagnanotizie.net, 4live.it, vitaromagna.it,
forli-eventi.it, modenatoday.it, modena2000.it, sulpanaro.net, bologna2000.com, bolognatoday.it, popolis.it,
stampareggiana.it, laliberta.info, primareggioemilia.it, carpi2000.it, reggio2000.it, cremonaoggi.it, cremonasera.it,
primacremona.it, laprovinciacr.it, crema-news.it, cremavvenimenti.com, parmatoday.it, parmadaily.it, temponews.it,
gentepocket.it, capodannoparma.com, nonsoloeventiparma.it, invaltaro.it, sondriotoday.it, laprovinciaunicatv.it,
valtellinamobile.it, calendariovaltellinese.com, ilgiorno.it, ilrestodelcarlino.it, mentelocale.it, chesagra.it,
ilborghista.it, weekendlombardia.it, trovaeventi.com, portaleventi.it, music-opera.com, bachtrack.com, occhi.it,
emilia-romagna-intour.com (tour guidati a pagamento di Reggio Emilia, molti eventi nel calendario di Reggio Emilia Welcome).

## Eventi visti ma non pubblicati
- **Teatro Comunale di Bologna (tcbo.it)**: 20 eventi (Notte Morricone 28-29/11, Il flauto magico Short Edition 5/12,
  concerti sinfonici e Gioia, Il Re Leone Live 18-20/12, Concerto di fine anno con Markus Stenz 31/12, La straniera
  22 e 24/1, Il ritorno di Ulisse in patria 2-7/3, Sergio Bernal 13-14/3...). Letti dalla home prima che tcbo.it
  entrasse in `vietate` (robots.txt blocca ClaudeBot); tolti tutti dal file. Da cercare su Bologna Welcome o Bologna
  Cultura (che elenca anche il Manzoni) o da mettere in `ops/da-verificare.json`.
- Treviso Swallowing Day (12/12, Auditorium Santa Caterina): pagina dell'organizzatore in 403.
- Bertinoro: mercatini di Natale (29/11, 6/12), concerti DaiDeJazz (1 e 15/12): solo testate da verificare.
- Lodi: Villaggio di Natale in piazza della Vittoria (4-13/12) e Sagra di Santa Lucia: solo aggregatori; le pagine del
  Comune "Magia delle Feste" non hanno l'anno.
- Reggio Emilia: Hourvari (Compagnie Rasposo, Reggiane Parco Innovazione, 9-11/12) e Concerto di Natale in Sala Verdi
  aggiunto solo con l'indirizzo del Teatro Ariosto; Lo Schiaccianoci all'Ariosto del 15-16/12 (orari del mattino, scuole).
- Sondrio: parata, flash mob, Polar Bear Express e laboratori di Sondrio Natale senza luogo preciso.
- Castelvetro di Modena: mercatino dell'8/12 visto solo in un risultato di ricerca.

## Luoghi nuovi (per config/luoghi.yaml; coordinate da confermare)
Nominatim risponde 403 da questo ambiente e non ho potuto incrociare due fonti: gli indirizzi vengono dalle pagine
ufficiali (o dalla mia conoscenza dove indicato), le coordinate sono approssimate e vanno controllate prima di
metterle in luoghi.yaml.
- Teatro Arena del Sole, Via dell'Indipendenza 44, Bologna, 44.5004 11.3437
- Teatro delle Moline, Via delle Moline 1/b, Bologna, 44.4988 11.3460
- Teatro Auditorium Manzoni, Via de' Monari 1/2, Bologna, 44.4969 11.3419 (indirizzo da bachtrack nei risultati)
- Teatro EuropAuditorium, Piazza della Costituzione 4, Bologna, 44.5186 11.3633
- ZolAuditorium, Piazza della Repubblica 1, Zola Predosa (indirizzo da culturabologna.it)
- Villa Edvige Garagnani, Via Masini 11, Zola Predosa (indirizzo da un risultato di ricerca)
- Teatro Storchi, Largo Garibaldi 15, Modena, 44.6456 10.9306
- Teatro delle Passioni, Viale Carlo Sigonio 382, Modena, 44.6366 10.9135
- Teatro Comunale Pavarotti-Freni, Corso Canalgrande 85, Modena, 44.6432 10.9268
- Piazza Grande, Modena, 44.6466 10.9254
- Teatro Municipale Valli, Piazza Martiri del 7 Luglio 7, Reggio nell'Emilia, 44.6995 10.6315
- Teatro Ariosto, Corso Cairoli 1, Reggio nell'Emilia, 44.6993 10.6283 (indirizzo da Reggio Emilia Welcome)
- Teatro Cavallerizza, Viale Allegri 8/a, Reggio nell'Emilia, 44.6997 10.6297 (indirizzo da Reggio Emilia Welcome)
- Teatro Regio di Parma, Strada Garibaldi 16/a, Parma, 44.8040 10.3262
- Teatro Due, Viale Basetti 12/a, Parma, 44.7990 10.3218
- Fiere di Parma, Viale delle Esposizioni 393A, Parma (indirizzo da mercanteinfiera.it)
- Teatro Diego Fabbri, Corso Armando Diaz 47, Forli', 44.2209 12.0447 (indirizzo da forlichebrillaofficial.it)
- Piazza Aurelio Saffi, Forli', 44.2224 12.0407
- Teatro Amilcare Ponchielli, Corso Vittorio Emanuele II 52, Cremona, 45.1352 10.0226 (indirizzo da turismocremona.it)
- Piazza del Comune, Cremona, 45.1334 10.0246; Auditorium Giovanni Arvedi (Museo del Violino), Piazza Marconi 5, Cremona
- Teatro alle Vigne, Via Cavour 66, Lodi, 45.3135 9.5025
- Teatro della Societa', Piazza Garibaldi 10, Lecco (civico da confermare; la Fondazione Teatre e' in Piazza Diaz 1)
- Teatro Sociale di Sondrio, Piazza Garibaldi 26, Sondrio, 46.170546 9.869365 (coordinate dalla scheda di
  eventi.sondrioevalmalenco.it, indirizzo da piu' risultati di ricerca e da lombardiabeniculturali.it): **verificato**
- Palazzo Sartoretti e Biblioteca Giorgio Ambrosoli, Piazza Martiri 1, Reggiolo (da reggioemiliawelcome.it)

## Lezioni per ops/metodo-ricerca.md
- **Emilia-Romagna**: le home dei teatri di produzione (I Teatri di Reggio, ERT, Ponchielli, Regio, Accademia
  Perduta) danno tutta la stagione in una lettura: 20-45 eventi per lettura. Gli uffici turistici dei capoluoghi
  hanno calendari mensili completi (Reggio Emilia Welcome: 68 voci con indirizzi). I siti comunali di Modena
  (503) e Parma (catalogo FlippingBook in immagini) e il calendario di VisitModena (JavaScript) non si leggono.
- **Natale**: i programmi 2026 dei capoluoghi (Lecco, Sondrio, Forli', Cremona) sono gia' pubblicati e
  sono la fonte con piu' eventi per lettura (20-100). Nei comuni piccoli molte pagine natalizie sono ancora del
  2023-2025: chiedere sempre l'anno e la data di pubblicazione per prima cosa.
- **Prima di aprire un teatro controllare `config/fonti-vietate.yaml` appena prima**: tcbo.it e' entrato in `vietate`
  durante la notte, dopo che ne avevo letto la home (20 eventi buttati).
- I comuni piccoli di Lombardia ed Emilia (meno di 5000 abitanti) rendono quasi zero con WebSearch: meglio provare
  direttamente `/it/events` (Municipium) o il PDF annuale del calendario (Reggiolo).

## Problemi
- Nominatim (pipeline.geocode) risponde 403: niente coordinate verificate. 127 eventi senza lat/lon (indirizzo
  presente): li geocodifica il PC alla pubblicazione.
- 5 eventi senza indirizzo: Chiesa di Santa Maria Assunta di Reggiolo (2 concerti), Polifunzionale di Talamona
  (Christmas running), e due gia' sistemati su Piazza Martiri di Reggiolo; il campo `address` manca solo per la
  chiesa e il polifunzionale.
- Conflitto di sede: Lo Schiaccianoci del 17/12 a Lecco e' "Teatro Cenacolo Francescano" nella pagina del Comune e
  "Teatro della Societa'" sul sito del teatro: usato il sito del teatro.
- Mostre in corso (Reggio Emilia, Gualtieri) hanno come inizio il 2026-11-28 perche' le fonti danno solo la fine.
- Eventi di piu' giorni dei teatri senza orari (ERT, I Teatri, Teatro Due) pubblicati come eventi unici con inizio e fine.
- ops/copertura.yaml: modificate solo `province` (10 sigle), `comuni_TV.Resana`, `categorie_TV` (Convegni) e le
  nuove sezioni `comuni_CR/LC/LO/SO/BO/MO/RE/PR/FC` e `categorie_SO/BO/RE/PR/FC`, aggiunte in fondo al file.
