@echo off
REM Allinea la cartella del PC a GitHub prima di ogni giro.
REM Sul PC nessun file del repository si modifica a mano: quelli che il PC scrive (sito, rapporti, archivio) si
REM rigenerano a ogni giro dal database del PC (data\, che git non tocca). Quindi si puo' sempre ripartire dalla
REM versione di GitHub, anche se un aggiornamento precedente si era bloccato a meta' (conflitti).
cd /d "%~dp0.."
if exist .git\rebase-merge git rebase --abort
if exist .git\rebase-apply git rebase --abort
if exist .git\MERGE_HEAD git merge --abort
git fetch -q origin main && git reset -q --hard origin/main && (echo Codice allineato a GitHub & exit /b 0)
echo GitHub non raggiungibile: si lavora con il codice gia' presente
exit /b 1
