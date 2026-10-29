# Registra due attivita' nell'Utilita' di pianificazione di Windows:
#   Andiamoo-Pipeline  ogni 4 ore: raccolta, AI, pubblicazione
#   Andiamoo-Bot       all'accesso: bot Telegram sempre attivo (si riavvia se si chiude)
#   Andiamoo-API       all'accesso: API del sito per "Aggiungi evento" e "Segnala" (si riavvia se si chiude)
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot

$pipeline = New-ScheduledTaskAction -Execute "$Root\windows\run_pipeline.bat" -WorkingDirectory $Root
$every4h = New-ScheduledTaskTrigger -Once -At (Get-Date).Date.AddHours(6) -RepetitionInterval (New-TimeSpan -Hours 4)
$opts = New-ScheduledTaskSettingsSet -StartWhenAvailable -DontStopIfGoingOnBatteries -AllowStartIfOnBatteries `
        -ExecutionTimeLimit (New-TimeSpan -Hours 3) -MultipleInstances IgnoreNew
Register-ScheduledTask -TaskName "Andiamoo-Pipeline" -Action $pipeline -Trigger $every4h -Settings $opts -Force | Out-Null

$bot = New-ScheduledTaskAction -Execute "$Root\windows\run_bot.bat" -WorkingDirectory $Root
$atLogon = New-ScheduledTaskTrigger -AtLogOn
$botOpts = New-ScheduledTaskSettingsSet -StartWhenAvailable -RestartCount 999 -RestartInterval (New-TimeSpan -Minutes 1) `
           -ExecutionTimeLimit ([TimeSpan]::Zero) -MultipleInstances IgnoreNew
Register-ScheduledTask -TaskName "Andiamoo-Bot" -Action $bot -Trigger $atLogon -Settings $botOpts -Force | Out-Null

$api = New-ScheduledTaskAction -Execute "$Root\windows\run_api.bat" -WorkingDirectory $Root
Register-ScheduledTask -TaskName "Andiamoo-API" -Action $api -Trigger $atLogon -Settings $botOpts -Force | Out-Null

Write-Host "Attivita' registrate: Andiamoo-Pipeline (ogni 4 ore), Andiamoo-Bot e Andiamoo-API (all'accesso)." -ForegroundColor Green
