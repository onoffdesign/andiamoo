@echo off
REM Prova del giro notturno nella stessa modalita' della notte (senza accesso a Windows), senza raccogliere
REM eventi e senza ibernare. La lancia imposta_notte.ps1; risultato in logs\prova_notte.log
cd /d "%~dp0.."
if not exist logs mkdir logs
set LOG=logs\prova_notte.log
echo ===== PROVA %date% %time% ===== > %LOG%
echo utente: %USERNAME% >> %LOG%
ping -n 1 github.com > nul 2>&1 && (echo [OK] rete >> %LOG%) || (echo [NO] rete: github.com non risponde >> %LOG%)
git fetch -q origin >> %LOG% 2>&1 && (echo [OK] GitHub lettura >> %LOG%) || (echo [NO] GitHub lettura >> %LOG%)
git push --dry-run -q origin HEAD:refs/heads/prova-chiave-pc >> %LOG% 2>&1 && (echo [OK] GitHub scrittura >> %LOG%) || (echo [NO] GitHub scrittura >> %LOG%)
call "%~dp0avvia_ollama.bat" >> %LOG% 2>&1
curl -s -o nul http://localhost:11434/api/tags && (echo [OK] Ollama >> %LOG%) || (echo [NO] Ollama non risponde >> %LOG%)
".venv\Scripts\python.exe" -c "import pipeline.run; from pipeline.config import env; print('[OK] Python e progetto'); print('[OK] Telegram configurato' if env('TELEGRAM_TOKEN') and env('TELEGRAM_ADMIN_CHAT_ID') else '[NO] Telegram: manca TELEGRAM_TOKEN o TELEGRAM_ADMIN_CHAT_ID nel file .env')" >> %LOG% 2>&1
echo FINE PROVA >> %LOG%
