@echo off
REM API del sito ("Aggiungi evento" e "Segnala"): ascolta su 127.0.0.1:8787, esposta con Cloudflare Tunnel.
cd /d "%~dp0.."
if not exist logs mkdir logs
".venv\Scripts\python.exe" -m pipeline.api >> logs\api.log 2>&1
