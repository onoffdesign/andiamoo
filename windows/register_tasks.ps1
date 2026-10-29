# Registra due attivita' nell'Utilita' di pianificazione di Windows:
#   Andiamoo-Pipeline  ogni notte alle 01:00: raccolta, AI locale (Ollama), controllo qualita', pubblicazione
#                      (alle 03:37 la revisione di Claude nel cloud lavora sulla coda che questo giro lascia in ops/)
#   Andiamoo-Bot       all'accesso: bot Telegram sempre attivo (si riavvia se si chiude)
#   Andiamoo-API       all'accesso: API del sito per "Aggiungi evento" e "Segnala" (si riavvia se si chiude)
#   Andiamoo-Tunnel    all'accesso: tunnel Cloudflare che rende l'API raggiungibile dal sito
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot

$pipeline = New-ScheduledTaskAction -Execute "$Root\windows\run_pipeline.bat" -WorkingDirectory $Root
$nightly = New-ScheduledTaskTrigger -Daily -At "01:00"
$opts = New-ScheduledTaskSettingsSet -StartWhenAvailable -DontStopIfGoingOnBatteries -AllowStartIfOnBatteries `
        -ExecutionTimeLimit (New-TimeSpan -Hours 4) -WakeToRun -MultipleInstances IgnoreNew
Register-ScheduledTask -TaskName "Andiamoo-Pipeline" -Action $pipeline -Trigger $nightly -Settings $opts -Force | Out-Null

$bot = New-ScheduledTaskAction -Execute "$Root\windows\run_bot.bat" -WorkingDirectory $Root
$atLogon = New-ScheduledTaskTrigger -AtLogOn
$botOpts = New-ScheduledTaskSettingsSet -StartWhenAvailable -RestartCount 999 -RestartInterval (New-TimeSpan -Minutes 1) `
           -ExecutionTimeLimit ([TimeSpan]::Zero) -MultipleInstances IgnoreNew
Register-ScheduledTask -TaskName "Andiamoo-Bot" -Action $bot -Trigger $atLogon -Settings $botOpts -Force | Out-Null

$api = New-ScheduledTaskAction -Execute "$Root\windows\run_api.bat" -WorkingDirectory $Root
Register-ScheduledTask -TaskName "Andiamoo-API" -Action $api -Trigger $atLogon -Settings $botOpts -Force | Out-Null

$tunnel = New-ScheduledTaskAction -Execute "$Root\windows\run_tunnel.bat" -WorkingDirectory $Root
Register-ScheduledTask -TaskName "Andiamoo-Tunnel" -Action $tunnel -Trigger $atLogon -Settings $botOpts -Force | Out-Null

Write-Host "Attivita' registrate: Andiamoo-Pipeline (ogni notte alle 01:00), Andiamoo-Bot, Andiamoo-API e Andiamoo-Tunnel (all'accesso)." -ForegroundColor Green
