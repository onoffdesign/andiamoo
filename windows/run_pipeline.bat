@echo off
REM Giro notturno: aggiorna il codice (e le correzioni della revisione di Claude), avvia Ollama se serve,
REM raccoglie, elabora con l'AI locale, controlla la qualita' e pubblica.
cd /d "%~dp0.."
if not exist logs mkdir logs
echo ===== %date% %time% ===== >> logs\pipeline.log
git pull --rebase --autostash >> logs\pipeline.log 2>&1
curl -s -o nul http://localhost:11434/api/tags
if errorlevel 1 (
  echo Avvio Ollama >> logs\pipeline.log
  start "" /min ollama serve
  timeout /t 20 /nobreak > nul
)
".venv\Scripts\python.exe" -m pipeline.run >> logs\pipeline.log 2>&1
