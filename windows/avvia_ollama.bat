@echo off
REM Avvia Ollama se non e' gia' attivo. Funziona anche senza accesso a Windows (giro notturno).
curl -s -o nul http://localhost:11434/api/tags && exit /b 0
echo Avvio Ollama
set "OLLAMA_EXE=ollama"
where ollama > nul 2>&1 || set "OLLAMA_EXE=%LOCALAPPDATA%\Programs\Ollama\ollama.exe"
start "" /min "%OLLAMA_EXE%" serve
for /l %%i in (1,1,12) do (
  ping -n 6 127.0.0.1 > nul
  curl -s -o nul http://localhost:11434/api/tags && exit /b 0
)
echo Ollama non risponde dopo 60 secondi
exit /b 1
