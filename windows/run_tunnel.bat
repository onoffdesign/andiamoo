@echo off
REM Tunnel Cloudflare per l'API: rende raggiungibile dal sito "Aggiungi evento" e "Segnala".
cd /d "%~dp0.."
if not exist logs mkdir logs
".venv\Scripts\python.exe" -m pipeline.tunnel >> logs\tunnel.log 2>&1
