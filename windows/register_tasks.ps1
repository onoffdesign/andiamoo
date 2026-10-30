# Registra le attivita' che partono all'accesso a Windows (il giro notturno e' in imposta_notte.ps1):
#   Andiamoo-Bot       all'accesso: bot Telegram sempre attivo (si riavvia se si chiude)
#   Andiamoo-API       all'accesso: API del sito per "Aggiungi evento" e "Segnala" (si riavvia se si chiude)
#   Andiamoo-Tunnel    all'accesso: tunnel Cloudflare che rende l'API raggiungibile dal sito
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot

# Giro notturno (01:00) e resoconto (07:30) si registrano con windows\imposta_notte.ps1, che li fa partire anche
# senza accesso a Windows. Qui restano solo le attivita' che partono all'accesso.

$bot = New-ScheduledTaskAction -Execute "$Root\windows\run_bot.bat" -WorkingDirectory $Root
$atLogon = New-ScheduledTaskTrigger -AtLogOn
$botOpts = New-ScheduledTaskSettingsSet -StartWhenAvailable -RestartCount 999 -RestartInterval (New-TimeSpan -Minutes 1) `
           -ExecutionTimeLimit ([TimeSpan]::Zero) -MultipleInstances IgnoreNew
Register-ScheduledTask -TaskName "Andiamoo-Bot" -Action $bot -Trigger $atLogon -Settings $botOpts -Force | Out-Null

$api = New-ScheduledTaskAction -Execute "$Root\windows\run_api.bat" -WorkingDirectory $Root
Register-ScheduledTask -TaskName "Andiamoo-API" -Action $api -Trigger $atLogon -Settings $botOpts -Force | Out-Null

$tunnel = New-ScheduledTaskAction -Execute "$Root\windows\run_tunnel.bat" -WorkingDirectory $Root
Register-ScheduledTask -TaskName "Andiamoo-Tunnel" -Action $tunnel -Trigger $atLogon -Settings $botOpts -Force | Out-Null

Write-Host "Attivita' registrate all'accesso: Andiamoo-Bot, Andiamoo-API e Andiamoo-Tunnel. Per la notte: windows\imposta_notte.ps1" -ForegroundColor Green
