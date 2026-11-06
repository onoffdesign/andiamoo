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
call "%~dp0aggiorna_codice.bat" >> logs\pipeline.log 2>&1
REM NB: le righe fino a "call aggiorna_codice" restano uguali: l'aggiornamento riscrive questo file mentre gira,
REM quindi si cambia solo cio' che viene dopo.
REM Rete ancora assente? Dopo il risveglio, senza nessuno collegato, il Wi-Fi puo' metterci di piu': altri 10 minuti.
set RETE=0
for /l %%i in (1,1,120) do (
  ping -n 1 github.com > nul 2>&1 && (set RETE=1& goto rete_ok)
  ping -n 6 127.0.0.1 > nul
)
:rete_ok
if "%RETE%"=="0" (
  echo %date% %time% Nessuna rete dopo 12 minuti: giro saltato. Stato della rete: >> logs\pipeline.log
  ipconfig >> logs\pipeline.log 2>&1
  netsh wlan show interfaces >> logs\pipeline.log 2>&1
  goto fine
)
call "%~dp0avvia_ollama.bat" >> logs\pipeline.log 2>&1
".venv\Scripts\python.exe" -m pipeline.run >> logs\pipeline.log 2>&1
echo %date% %time% Fine del giro (codice %errorlevel%) >> logs\pipeline.log
:fine
if /i "%~1"=="notte" powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0fine_notte.ps1" >> logs\pipeline.log 2>&1
