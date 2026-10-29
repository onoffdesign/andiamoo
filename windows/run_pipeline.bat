@echo off
REM Giro notturno: aggiorna il codice (e le correzioni della revisione di Claude), avvia Ollama se serve,
REM raccoglie, elabora con l'AI locale, controlla la qualita' e pubblica.
REM Con l'argomento "notte" (attivita' Andiamoo-Pipeline) a fine giro iberna il PC.
cd /d "%~dp0.."
if not exist logs mkdir logs
echo ===== %date% %time% ===== >> logs\pipeline.log
REM dopo il risveglio la rete puo' metterci un po': aspetta fino a 2 minuti
for /l %%i in (1,1,24) do (
  ping -n 1 github.com > nul 2>&1 && goto rete
  timeout /t 5 /nobreak > nul
)
:rete
git pull --rebase --autostash >> logs\pipeline.log 2>&1
curl -s -o nul http://localhost:11434/api/tags
if errorlevel 1 (
  echo Avvio Ollama >> logs\pipeline.log
  start "" /min ollama serve
  timeout /t 20 /nobreak > nul
)
".venv\Scripts\python.exe" -m pipeline.run >> logs\pipeline.log 2>&1
if /i "%~1"=="notte" powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0fine_notte.ps1" >> logs\pipeline.log 2>&1
