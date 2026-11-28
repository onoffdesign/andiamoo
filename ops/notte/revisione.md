# Revisione, notte del 2026-11-28

Interrotta su richiesta del coordinatore: WebFetch e' bloccato dalla rete della sessione (ENOTFOUND, provato su
mapcarta.com). Su sua indicazione i riassunti di WebSearch non valgono come dati verificati, quindi stanotte non ho
scritto correzioni, eventi o luoghi.

## Numeri
- Ricerche usate: 13 su 125 (12 WebSearch, 1 WebFetch fallito).
- Coda di revisione: 0 lavorati su 60 (corretti 0, rimossi 0, verificati 0).
- Campione: non controllato (0/20 aperti). Riga per la parte 3:
  `- 2026-11-28 · campione non controllato · errori: data 0, orario 0, luogo 0, accesso 0, categoria 0, link 0 · lezione: WebFetch bloccato dalla rete della sessione (ENOTFOUND), nessuna fonte ufficiale leggibile; i 20 eventi restano da controllare la notte dopo`
- Posizioni: prima e dopo uguali (luoghi con punti diversi 0, lontani dal comune 1, solo comune con luogo 252,
  solo comune senza luogo 6, candidati 0). Nessuna voce aggiunta a config/luoghi.yaml.
- Test di copertura: non fatto. Riga per espansione.md:
  `- 2026-11-28 · TV · test di copertura della revisione non fatto (WebFetch bloccato dalla rete della sessione) · criterio di saturazione: non valutato (non e' lunedi')`

## Coda e posizioni: cosa resta (per la notte dopo)
- 55 eventi su 60 della coda hanno "luogo: solo il comune": quasi tutti eventi della redazione presi da Qdpnews e
  Nordest24 (programmi del Natale di Treviso, Montebelluna, Nervesa, Vittorio Veneto, Farra di Soligo, Villorba,
  StatisticAll, Museo Canova). Sistemarli per luogo in config/luoghi.yaml copre insieme coda e posizioni.
- Luoghi piu' frequenti senza punto: Ca' dei Carraresi (13+3), Corso Mazzini Montebelluna (11), Gypsotheca Canova
  Possagno (9), Teatro del Pane Villorba (9), Stadio Tenni (8), Teatro Cristallo Oderzo (7), Teatro delle Voci (7),
  Piazza del Popolo Vittorio Veneto (6), centro di Cison (6).
- Il solo evento "lontano dal comune" (b665ec02e9b8accd, Sile Classica all'Auditorium H-FARM College, Via Olivetti 1,
  Roncade) e' un falso allarme gia' noto: il campus H-FARM e' a Ca' Tron, 7-9 km dal centro (verificato l'8/11, vedi
  correzioni.yaml). Si potrebbe aggiungere a luoghi.yaml per toglierlo dalla lista.
- Piste per le coordinate, da confermare con una lettura quando WebFetch funziona: Mapcarta (N1237704175 Ca' dei
  Carraresi, W158961097 Gypsoteca Canova, 33736100 Stadio Tenni, 32918642 e N10309345309 Palazzo dei Trecento),
  italia-italy.org per il municipio di Vittorio Veneto (Piazza del Popolo 14). Mapcarta non trova Teatro del Pane,
  Teatro Cristallo di Oderzo, Teatro delle Voci, Teatro Eden ne' Piazza del Popolo di Vittorio Veneto (4 ricerche a vuoto).

## Fonti nuove da catalogare
Nessuna.

## Lezioni
- mapcarta.com non si apre da WebFetch in questa sessione (ENOTFOUND): prima di spendere ricerche sulle posizioni
  provare una sola WebFetch su un dominio noto.
- Le ricerche Mapcarta trovano musei, stadi e palazzi con nome, non teatri parrocchiali, sale associative e piazze
  di comuni minori (conferma della lezione del 26/11).

## Problemi
- WebFetch bloccato dalla rete della sessione: coda, campione, posizioni e test non fatti.
