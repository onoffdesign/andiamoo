# Agente treviso, notte del 2026-11-28

## Numeri
- Ricerche usate: 7 su 125 (5 WebSearch, 2 WebFetch falliti).
- Eventi aggiunti: 0. Correzioni: 0.
- Lavoro interrotto su richiesta del coordinatore: WebFetch bloccato dalla rete della sessione
  (getaddrinfo ENOTFOUND su www.cinemaedera.it e www.qdpnews.it). I riassunti di WebSearch non valgono come dati verificati.

## Fase 0, fonti note
- Treviso Sotterranea (visite alle mura): 1 WebSearch "Treviso Sotterranea percorso visita dicembre 2026", nessuna data
  di dicembre 2026 nei risultati (solo articoli vecchi e una visita dell'8/11 gia' passata). Da aggiornare:
  ultimo_controllo 2026-11-28, resa ultimi [0, 0, 0] (quarto controllo a zero: valutare `frequenza: mensile` o `stato: debole`).
- Cinema Edera: WebSearch con allowed_domains cinemaedera.it ha trovato la pagina della settimana (25/11-1/12/2026, con
  un'anteprima lunedi' 30/11 "Il caso Marie-Claire"), ma WebFetch e' fallito: dati non verificati. Non aggiornare la resa
  (controllo non concluso); da riprovare la prossima notte.

## Fasi A-E
- Fase B (20 comuni): solo `pipeline.editorial --comune` eseguito per tutti (costo zero). Senza eventi futuri: Caerano di
  San Marco, Resana, Giavera del Montello, Zenson di Piave, Castello di Godego, Crocetta del Montello, San Pietro di Feletto,
  Riese Pio X, Pederobba. Nessuna ricerca fatta: le date in ops/copertura.yaml `comuni_TV` NON sono state aggiornate.
- Fase A (12 ambiti): non cercati, date in `categorie_TV` non aggiornate.
- Fasi C e D: 2 WebSearch su Qdpnews (allowed_domains) e Nordest24 per il Natale. Da riprendere quando WebFetch funziona:
  - "Magico Natale nelle Antiche Terre" (Susegana e Santa Lucia di Piave): accensione degli alberi domenica 29/11 alle 18,
    a Susegana in piazza Martiri della Liberta' con Ludobus e Pro Loco; non sul sito. Fonti da leggere:
    https://www.qdpnews.it/comuni/coneglianese/susegana/il-magico-natale-nelle-antiche-terre-tanti-eventi-e-due-alberi-accesi-in-contemporanea/
    e https://www.nordest24.it/veneto-sabato-avvento-susegana-abano-oderzo-28-novembre-2026
  - "Natale a Treviso": villaggio in piazza Rinaldi e accensione dell'albero (articolo Qdpnews
    https://www.qdpnews.it/comuni/treviso-citta/natale-a-treviso-domani-apre-il-villaggio-in-piazza-rinaldi-domenica-saccende-il-grande-albero/): controllare se gia' sul sito.
  - Qdpnews "E' arrivato dicembre: ecco gli eventi del weekend nel territorio trevigiano" (controllare l'anno).
  - Nervesa (Effetto Natale 29/11) e Vittorio Veneto (Magico Natale 27/11-6/1) gia' sul sito.
  - Nordest24 "Palazzo Attems, laboratori ultimo weekend di novembre": e' Gorizia, per l'agente italia.
  Nessuna data aggiornata nelle sezioni aggregatori e news di ops/copertura.yaml.
- Fase E (fonti nuove): non fatta. Da verificare (non usati): sagrapedia.com, portaleventi.it, tviweb.it (gia' in verifica), digitradio.it.

## Voci nuove per ops/categorie-ricerca.md
Non preparate (lavoro interrotto).

## Miglioria del metodo
Proposta: all'inizio della notte una prova di WebFetch su una sola pagina nota (es. Qdpnews) prima di lanciare gli agenti;
se fallisce con ENOTFOUND la notte si ferma subito o lavora solo sulle parti senza rete (coda, posizioni da file, pulizia),
cosi' non si spendono ricerche su dati che non si possono verificare.

## Problemi
- WebFetch bloccato dalla rete della sessione: tutti i domini danno ENOTFOUND. Va consentito l'accesso nelle impostazioni
  di rete della sessione cloud.
