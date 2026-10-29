@echo off
REM Bot Telegram per le segnalazioni (resta acceso).
cd /d "%~dp0.."
if not exist logs mkdir logs
".venv\Scripts\python.exe" -m bot.telegram_bot >> logs\bot.log 2>&1
