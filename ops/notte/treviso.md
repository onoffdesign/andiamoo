# Agente treviso, notte del 2026-11-28

Riscritto da capo (il tentativo precedente della notte era fermo per WebFetch bloccato; stanotte WebFetch funziona).

## Numeri
- Ricerche usate: 98 su 125 (WebSearch + WebFetch; conto anche 1 download con curl della brochure dell'Ateneo, sito ufficiale).
- Eventi aggiunti: 46 in config/notte/treviso-eventi.yaml (controllati con `python -m pipeline.notte --controlla treviso`: parti valide).
  - arte-cultura 15 (6 conferenze dell'Ateneo di Treviso, 3 incontri dell'Ordine Architetti, 4 mostre, 2 visite guidate)
  - sport 10 (9 corse e camminate di dicembre, 1 ultra trail)
  - mercatini-fiere 5 (Natale a Ramon, una voce per giornata di apertura)
  - teatro-spettacoli 4 (proiezioni speciali Cinema Edera e Cinema Busan)
  - musica 4, sagre-feste 3, business 2 (open day H-FARM College), natura-outdoor 2 (benessere e yoga), famiglie-bambini 1
- Comuni piu' toccati: Treviso 15, Loria (Ramon) 8, Ponzano 3, Montebelluna 3; nuovi eventi anche a Ormelle, Castello di Godego, Morgano, Giavera, Asolo, Revine Lago, Oderzo, Susegana, Santa Lucia di Piave, Cison, Castelfranco, Roncade, Mogliano.
- Correzioni (config/notte/treviso-correzioni.yaml): 1 correzione (official_url della mostra La materia dei sogni verso la pagina dei Musei Civici), 8 eventi verificati.
- Da segnalare al coordinatore (non e' un uid pubblicato, non posso correggerlo io): in config/eventi_redazione.yaml la mostra
  "Ludovico Lipparini e la pittura filoellenica" ha start 2026-11-06, official_url digitradio.it e fonte tviweb.it (entrambe da
  verificare). La pagina ufficiale dei Musei Civici dice 14 novembre 2026 - 7 febbraio 2027:
  https://www.museicivicitreviso.it/mostre-ed-eventi/lodovico-lipparini-il-giuramento-di-lord-byron-a-missolungi-e-la-pittura-filellenica-ideali-dindipendenza-nellarte-dellottocento/
  (titolo ufficiale "Lodovico Lipparini. Il Giuramento di Lord Byron a Missolungi e la pittura filellenica"). Con start, official_url
  e fonte corretti la voce rispetta la regola fonti.
- `--doppioni` segnala in redazione "F.O.C.U.S. Sound of Victory (Rassegna Gospel 2026)" del 17/12 gia' sul sito da altra fonte (b9d9253113df1975): non mio, da togliere dalla redazione se completo.

## Fase 0, fonti note (per ops/fonti.yaml)
- Cinema Edera (Treviso): ultimo_controllo 2026-11-28, resa 2 (anteprima Il caso Marie-Claire 30/11, incontro con Nanni Moretti 17/12).
  Miglioria: leggere la home https://www.cinemaedera.it/ (eventi speciali con link alle schede) invece di "i film della settimana";
  query: "Cinema Edera Treviso" con allowed_domains cinemaedera.it.
- Treviso Sotterranea (visite alle mura): ultimo_controllo 2026-11-28, resa 0 (quinto controllo a zero, il dominio non si legge).
  Proposta: `stato: debole`, `frequenza: mensile`.
- Altre fonti del catalogo riaperte (tutte ultimo_controllo 2026-11-28):
  - Visit Museum Treviso (laboratori del weekend): resa 1.
  - Musei Civici di Treviso (mostre ed eventi): resa 0 (1 correzione, 1 segnalazione Lipparini). Pagina utile: https://www.museicivicitreviso.it/mostre-ed-eventi/
  - Auditorium Don Vidotto (Maserada): resa 0; anche /next-events/ e' vuota.
  - Biblioteca comunale di Zero Branco: resa 0 (gia' coperta).
  - Teatro Accademia Conegliano: resa 0, /prosa/ vuota e /events/ dietro verifica anti-bot ("Please wait while your request is being verified"): candidato per ops/domini-illeggibili.yaml.
  - Sile Classica: resa 0 (concerto finale gia' sul sito).
  - Conservatorio Steffani (conscfv.it/eventi): resa 0, elenco fermo al 24/11.
  - Ananda Marga Treviso: resa 3 (concerto Viaggiatori Armonici, mattinata creativita', formazione Balyayoga).
  - Pro Loco di Morgano: resa 0 (gia' coperta).
  - Biblioteca di Casale sul Sile: resa 0 (nessun evento 2026 dopo il 14/11).
  - Comune di Asolo (OpenCity): resa 0, elenco vuoto; rimanda a asolo.it/eventi.
  - Ordine Architetti di Treviso: resa 3.
  - Cison Borgo Vivo: resa 1 (presepi di Mura).
  - Pro Loco Mogliano Veneto: resa 0 (home senza calendario).
  - Cinema Teatro Busan: resa 2 (Herzog).
  - FAI Memoriale Brion: resa 0 (gia' sul sito).
  - Trofeo Triveneto Ciclocross (Federciclismo): resa 0 (5 prove TV, tutte gia' sul sito).
  - Nordest24 /localita/treviso: resa 6 (Ramon 8 voci, Ormelle, Orchestra Impossibile, Patchwork, Dutch Nazari).
  - Calendario Podismo Veneto (pagina del mese): resa 9 (8 corse + Prosecco Ultra Trail confermato su prosecco.run).
  - Qdpnews: resa 3 (Susegana e Santa Lucia).

## Fasi A-E
- Fase B, comuni (data 2026-11-28 in comuni_TV): Asolo, Pieve del Grappa, Riese Pio X, Castello di Godego, San Pietro di Feletto,
  Cordignano, Ormelle, Portobuffole', Zenson di Piave, Preganziol, Morgano, Casale sul Sile, Crocetta del Montello, Pederobba,
  Caerano di San Marco, Mogliano Veneto, Giavera del Montello; anche Loria, Susegana, Santa Lucia di Piave, Ponzano Veneto,
  Cison di Valmarino. Non cercati a mano: Resana, Spresiano, San Vendemiano (gia' fonti del giro in config/sources.yaml).
  Siti dei comuni senza eventi: Preganziol, Crocetta, San Pietro di Feletto ("Nessun evento in programma"), Riese (solo
  distribuzione alberi riservata). Pro Loco Castello di Godego: sito fermo al 2020.
- Fase A, 12 ambiti (data 2026-11-28 in categorie_TV): risultati
  - Conferenze e incontri: 9 (Ateneo di Treviso 6, Ordine Architetti 3). Formazione: 2 open day H-FARM College + 1 corso yoga.
  - Benessere: 1. Concerti: 2. Festival musicali: 1 (4passi). Ciclismo: 0 nuovi (gia' coperto). Startup e innovazione: 0.
  - Lavoro: 0 (solo open day di agenzie passati e eventi online). Tecnologia e scienza: 0 (astrofili senza calendario).
  - Spettacoli per bambini: 0 (TraGazzi di Santa Lucia 2026/27 non ancora pubblicato; la stagione 2025/26 usci' il 10/12).
  - Ginnastica e danza sportiva: 0 (terza ricerca a vuoto: proposta `rara` per i saggi di Natale).
  - Serate e club: 0 pubblicabili (CSO Django 12/12 solo su rockol, illeggibile; manca sito ufficiale).
- Fasi C e D (date in aggregatori e news): calendariopodismoveneto (ammesso) e' stata la miglior resa della notte; Nordest24 e
  Qdpnews gia' a 2026-11-28; trevisomtb, federciclismo, prolocovenete, Pro Loco e UNPLI, musei, cinema, teatri, H-FARM aggiornati.
- Eventi non pubblicati (nessuna fonte ammessa con tutti i dati):
  - CSO Django, Treviso, 12/12/2026: My Dear Killer, BeMyDelay, Eric Culm (visti solo su rockol.it, illeggibile). Motivo: manca il sito del centro sociale.
  - 1o Trofeo Connection, ciclocross nazionale e campionato provinciale, Velo Club San Vendemiano, 5/12/2026 (visto su trevisomtb.it, aggregatore). Motivo: manca pagina dell'organizzatore o di Federciclismo.
  - Ciclocross del Ponte, Fae' di Oderzo, 8/12/2026 (trevisomtb.it): data non confermata (nel 2025 si e' corso il 14/12).
  - Harmonia Ruris Festival, Castelfranco, concerti del 16/12/2026 e 10/1/2027: date dal Comune ma senza titolo, ora e sala; riprovare su happyticket.
  - Gara provinciale di corsa campestre CSI a Santa Cristina (Quinto), 8/12: senza orario.

## Fase E, fonti nuove (da catalogare in ops/fonti.yaml)
Siti ufficiali (usabili):
1. Ateneo di Treviso, brochure dell'anno accademico | https://www.ateneoditreviso.it/ (link in home: /wp-content/uploads/2026/10/Pieghevole-2026-2027-01-7_Pagina_2.jpg) | query "Ateneo di Treviso" allowed_domains ateneoditreviso.it | tipo ente | categorie arte-cultura | comuni Treviso | frequenza annuale (esce in ottobre) | qualita 5 | resa 6. Nota: la brochure e' un'immagine JPG: si scarica e si legge come immagine; conferenze il venerdi' 17:30 al Seminario Vescovile, gratuite.
2. Museo di Storia Naturale e Archeologia di Montebelluna | https://www.museomontebelluna.it/ | query "museo Montebelluna eventi" allowed_domains museomontebelluna.it | museo | arte-cultura, famiglie-bambini | Montebelluna | mensile | 4 | resa 2.
3. H-FARM College, open day | https://college.h-farm.com/en/open-college/ | query "H-FARM College open day" | azienda | business | Roncade | trimestrale | 4 | resa 2 (date fino a luglio 2027: 23/1, 20/3, 8/5, 26/6, 23/7).
4. Prosecco Run / GT Sport | https://www.prosecco.run/ | query "Prosecco Run Vidor" | sport | sport | Vidor, Vittorio Veneto | annuale | 4 | resa 1.
5. Asolo Musica | https://www.asolomusica.com/ | query "Asolo Musica calendario" | associazione | musica | Asolo, Castelfranco (molti eventi a Venezia e nel Vicentino) | mensile | 3 | resa 1 (via Nordest24).
6. Museo Civico di Asolo | https://www.museoasolo.it/ | query "Museo Civico Asolo eventi" | museo | arte-cultura, famiglie-bambini | Asolo | mensile | 3 | resa 0 (gia' coperti da Nordest24).
7. Cinema Edera, home con eventi speciali | https://www.cinemaedera.it/ | gia' in catalogo: cambiare url.
8. Pro Loco Castello di Godego | https://www.prolococastellodigodego.it/ | pro loco | fermo al 2020: da evitare (lezione).
Da verificare (aggregatori/testate: non usati per pubblicare):
- trevisomtb.it (calendario PDF MTB e ciclocross della provincia: https://www.trevisomtb.it/CalendarioPDF.aspx). `fonti_vietate` lo da' "ammessa" solo perche' non e' in elenco, ma e' un portale di notizie: da leggere robots e termini prima di usarlo.
- rockol.it (concerti CSO Django): gia' illeggibile.
- arte.it (calendario mostre per citta'): elenca anche mostre passate (Banksy a Conegliano finita a marzo 2026).
- viberate.com, songkick.com, jambase.com, zero.eu: elenchi concerti, da verificare.
- siviaggia.it, familygo.eu: articoli di sintesi, da verificare.

## Voci nuove per ops/categorie-ricerca.md (Macro > Ambito > voce: parole di ricerca)
1. Arte e cultura > Conferenze e incontri > accademie e atenei cittadini: "Ateneo di Treviso conferenze", "brochure anno accademico"
2. Arte e cultura > Conferenze e incontri > ordini professionali: "Ordine Architetti Treviso eventi", "incontri culturali ordine"
3. Arte e cultura > Conferenze e incontri > istituti storici: "Istresco Nella Storia", "incontri storia contemporanea Treviso"
4. Arte e cultura > Mostre > collettive di artisti locali: "rassegna artisti locali", "mostra collettiva biblioteca"
5. Arte e cultura > Mostre > tessile e patchwork: "mostra quilt", "patchwork Treviso"
6. Arte e cultura > Mostre > presepi nei borghi: "presepi per le vie del borgo", "mostra presepi"
7. Arte e cultura > Visite guidate > sezioni archeologiche dei musei civici: "visita guidata sezione archeologica"
8. Arte e cultura > Tecnologia e scienza > biodiversita' e suoni: "mostra interattiva biodiversita'", "paesaggi sonori"
9. Spettacoli > Cinema > anteprime in lingua originale: "anteprima VOS", "versione originale sottotitolata Treviso"
10. Spettacoli > Cinema > incontri con registi: "incontro con il regista proiezione", "regista in sala"
11. Spettacoli > Cinema > documentari d'autore: "I grandi maestri cinema", "documentario evento"
12. Musica e party > Concerti > ensemble di musica d'atmosfera: "concerto d'inverno ensemble", "Viaggiatori Armonici"
13. Musica e party > Concerti > conferenze-concerto su strumenti antichi: "liuteria storica concerto", "strumenti rinascimentali"
14. Musica e party > Concerti > rap e cantautori in talk: "showcase rapper incontro", "dialogo e live"
15. Musica e party > Festival musicali > festival di giovani interpreti: "Harmonia Ruris", "festival giovani talenti Castelfranco"
16. Sport > Corsa > corse dei Babbi Natale: "corsa dei Babbi Natale", "Babbo Run", "X-Mas Run"
17. Sport > Corsa > marce FIASP di fine anno: "maratonina di San Silvestro", "Christmas walk FIASP"
18. Sport > Corsa > corsa campestre giovanile: "campestre CSI provinciale", "cross scolastico"
19. Sport > Trail, trekking e montagna > ultra trail di colline: "ultra trail Prosecco", "trail 50 km Treviso"
20. Sport > Ciclismo > campionati provinciali di ciclocross: "campionato provinciale ciclocross Treviso", "Velo Club San Vendemiano"
21. Natura e benessere > Benessere > counseling creativo: "SoulCollage", "collage benessere"
22. Natura e benessere > Benessere > formazione insegnanti yoga: "formazione yoga bambini", "Balyayoga"
23. Business e formazione > Formazione > open day universitari: "open day H-FARM College", "orientamento universita' Treviso"
24. Business e formazione > Formazione > corsi per professionisti aperti: "corso prevenzione incendi aperto", "seminario ordine professionale"
25. Mercatini e fiere > Mercatini > mercatini solidali dei donatori: "mercatini donatori di sangue", "mercatino solidale Natale"
26. Sagre e cibo > Feste stagionali > accensioni dell'albero nei comuni: "accensione albero di Natale <comune>", "alberi accesi in contemporanea"
27. Famiglie e bambini > Laboratori > laboratori di incisione e stampa: "laboratorio di incisione biblioteca", "cartoline di Natale laboratorio"
28. Famiglie e bambini > Spettacoli per bambini > rassegne comunali di teatro ragazzi: "TraGazzi Santa Lucia", "Ragazzi, che Teatro!"

## Miglioria del metodo
**Brochure in immagine: scaricarle e leggerle come immagine.** Molti enti culturali (Ateneo di Treviso) pubblicano il programma
dell'anno solo come JPG o PDF scansionato, che WebFetch non legge (rispondeva "i dettagli sono probabilmente nella brochure").
Scaricando il file dal sito ufficiale con `curl` nella cartella di lavoro e aprendolo come immagine si legge l'intero anno in un
colpo: stanotte 6 conferenze fino a marzo (e altre 7 fino a maggio) con una lettura. Regola proposta per ops/metodo-ricerca.md:
"quando WebFetch dice che il calendario e' in un'immagine o in una locandina, prendere l'URL dell'immagine e leggerla
scaricata (solo siti ufficiali)". Seconda miglioria, piccola: per il podismo la pagina del mese del Calendario Podismo Veneto
da' ora e km, mentre le schede delle singole gare sono solo immagini (4 letture a vuoto stanotte): usare la pagina del mese
come fonte e la scheda solo come official_url.

## Lezioni
- Le schede delle gare su calendariopodismoveneto.blogspot.com hanno i volantini come immagini: WebFetch non ne legge i dati.
- I giorni della settimana nella pagina del mese del Calendario Podismo Veneto sono sfasati ("Sab 5" anche per gare di domenica 6): fidarsi della data nel link della scheda.
- Articoli Qdpnews senza anno nell'indirizzo: stanotte 3 su 3 vecchi (Pieve del Grappa gennaio 2026, weekend 2023, Ridatti una mossa maggio 2026, Cappella Sistina gia' passato). Confermata la lezione: aprirli solo se il risultato mostra l'anno.
- Ricerche per ambito senza dominio (ginnastica, lavoro, astronomia, startup, teatro ragazzi): 6 ricerche, 0 eventi. Servono i siti delle societa' o delle sale.
- Comuni design-comuni con "Nessun evento in programma" (Preganziol, Crocetta, San Pietro di Feletto): una lettura sprecata a testa; per i comuni piccoli meglio Nordest24/Qdpnews o la pagina del mese del podismo.
- Teatro Accademia Conegliano: /events/ dietro verifica anti-bot.

## Problemi
- Nessun blocco: WebFetch funziona. Le pagine dei comuni piccoli restano quasi sempre vuote a fine novembre: i programmi di Natale dei comuni minori escono su Nordest24 e Qdpnews nei giorni immediatamente precedenti.
