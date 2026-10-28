@echo off
REM Un giro della pipeline: aggiorna il codice, raccoglie, elabora con l'AI e pubblica.
cd /d "%~dp0.."
if not exist logs mkdir logs
git pull --rebase --autostash >> logs\pipeline.log 2>&1
".venv\Scripts\python.exe" -m pipeline.run >> logs\pipeline.log 2>&1
