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
call "%~dp0aggiorna_codice.bat" >> logs\pipeline.log 2>&1
REM NB: le righe fino a "call aggiorna_codice" restano uguali (l'aggiornamento riscrive questo file mentre gira).
set RETE=0
for /l %%i in (1,1,60) do (
  ping -n 1 api.telegram.org > nul 2>&1 && (set RETE=1& goto rete_ok)
  ping -n 6 127.0.0.1 > nul
)
:rete_ok
if "%RETE%"=="0" (
  echo %date% %time% Nessuna rete: resoconto non inviato >> logs\pipeline.log
  goto fine
)
".venv\Scripts\python.exe" -m pipeline.report >> logs\pipeline.log 2>&1
:fine
if /i "%~1"=="notte" powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0fine_notte.ps1" >> logs\pipeline.log 2>&1
