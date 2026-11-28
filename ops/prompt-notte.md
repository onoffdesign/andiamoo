# Istruzioni della sessione notturna (lette dall'automazione "ANDIAMO? notte eventi")

L'automazione pianificata contiene solo una riga che rimanda a questo file: per cambiare il lavoro della notte si
modifica questo file, non l'automazione.

Notte di ANDIAMO?, la mappa pubblica degli eventi in tutta Italia (Treviso coperta in profondita', le altre province a
rotazione; repository GitHub onoffdesign/andiamoo, pubblico, sito su GitHub Pages). Il PC fisso e' escluso: tutto il
lavoro della notte lo fa questa sessione, che fa da coordinatore di quattro agenti che lavorano in contemporanea.

1. Il repository onoffdesign/andiamoo e' collegato all'attivita': lavora nella sua cartella (se non c'e', aggiungilo
   con add_repo, owner "onoffdesign", repo "andiamoo", accesso "push"). Passa su main, fai git pull --rebase e
   installa i requisiti (pip install --break-system-packages -q -r requirements.txt). Pubblica sempre su main, mai su
   rami claude/.
2. Esegui `python -m pipeline.piano_notte` (piano della notte e budget, ops/budget.yaml, piano Max) e leggi
   ops/segnalazioni-e-controllo.md e ops/revisione-notturna.md. Segui alla lettera la parte "Una sola sessione a notte
   ... quattro agenti che lavorano in contemporanea".
3. Lancia insieme, nello stesso messaggio, con lo strumento Agent (tipo general-purpose, in background), i quattro
   agenti giro, revisione, treviso e italia, ognuno con il suo compito, la sua quota di ricerche, la sua parte del
   piano della notte copiata nel testo e le "Regole per gli agenti" del file (incluse la REGOLA FONTI e la verifica
   delle fonti con robots.txt e termini). Ogni agente scrive solo i suoi file in config/notte/ e ops/notte/, non
   pubblica e non fa commit.
4. Mentre lavorano, leggi le risposte nuove del modulo Google del sito ("Aggiungi evento" e "Segnala") con il
   connettore Google Drive o Google Sheets (foglio "ANDIAMO? segnalazioni (Risposte)", id
   18e1sR9iF1jvGAvZeIXMv4d0BwTxDP7YbZAag6oLQ15U), come spiegato nel passo 2b, e scrivi in
   config/notte/coordinatore-eventi.yaml e coordinatore-correzioni.yaml. I contatti di chi scrive non vanno mai nel
   repository. Se il connettore non risponde, scrivilo nel resoconto e prosegui.
5. Quando un agente finisce: `python -m pipeline.notte --unisci <agente>` (se le parti non sono valide correggile),
   `python -m pipeline.pubblica`, commit e push su main (git add config ops archivio docs/data/events.json;
   git pull --rebase; git push origin main; mai forzare).
6. Alla fine: riporta nei file di memoria cio' che serve dai resoconti ops/notte/<agente>.md, aggiorna il registro
   (passo 8), poi `python -m pipeline.editorial --controlla`, `python -m pytest -q tests`, `python -m pipeline.pubblica`,
   commit e push su main.
7. Hai piena autonomia: correggi, rimuovi, aggiungi eventi e fonti, aggiorna la memoria e pubblica senza chiedere
   conferme (di notte non c'e' nessuno a rispondere). Non usare altri connettori oltre a Google Drive e Google Sheets.
   Scrivi tutto in italiano e non usare mai il trattino lungo (em dash).
8. Il tuo ultimo messaggio e' il resoconto del mattino che arriva a Federico come notifica: 4-6 righe nel formato
   indicato alla fine di ops/revisione-notturna.md (eventi sul sito e nuovi, aggiunti a Treviso e nel resto d'Italia,
   corretti, rimossi, campione, fonti del giro lette, fonti verificate e fonti nuove, province cercate, trattenuti
   dalla regola fonti, risposte del modulo, ricerche usate rispetto al budget, al massimo 3 problemi veri). Se durante
   la sessione ti e' stata chiesta qualche approvazione (lettura di pagine web o altro), scrivilo in una riga. Non
   parlare del PC.
