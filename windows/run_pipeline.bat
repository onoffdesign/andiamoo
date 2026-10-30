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
  ping -n 6 127.0.0.1 > nul
)
:rete
git pull --rebase --autostash >> logs\pipeline.log 2>&1
call "%~dp0avvia_ollama.bat" >> logs\pipeline.log 2>&1
".venv\Scripts\python.exe" -m pipeline.run >> logs\pipeline.log 2>&1
if /i "%~1"=="notte" powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0fine_notte.ps1" >> logs\pipeline.log 2>&1
