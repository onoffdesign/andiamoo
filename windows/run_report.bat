@echo off
REM Resoconto del mattino su Telegram (giro del PC + revisione di Claude). Con "notte" poi iberna il PC.
cd /d "%~dp0.."
if not exist logs mkdir logs
echo ===== %date% %time% resoconto ===== >> logs\pipeline.log
for /l %%i in (1,1,24) do (
  ping -n 1 api.telegram.org > nul 2>&1 && goto rete
  ping -n 6 127.0.0.1 > nul
)
:rete
REM il sito pubblicato si rigenera a ogni giro: la copia locale (es. scritta dal tunnel) non deve bloccare il pull
git checkout -- docs/data/events.json >> logs\pipeline.log 2>&1
git pull --rebase --autostash >> logs\pipeline.log 2>&1
".venv\Scripts\python.exe" -m pipeline.report >> logs\pipeline.log 2>&1
if /i "%~1"=="notte" powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0fine_notte.ps1" >> logs\pipeline.log 2>&1
