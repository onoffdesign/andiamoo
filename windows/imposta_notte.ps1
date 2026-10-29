# Prepara il PC fisso per il lavoro notturno di ANDIAMO?:
#   - alle 01:00 Windows si risveglia da solo (da ibernazione o sospensione) e parte il giro,
#     anche se nessuno ha fatto l'accesso;
#   - a fine giro il PC va in ibernazione (consumo come da spento), a meno che qualcuno lo stia usando;
#   - il tasto di accensione iberna invece di spegnere, cosi' la notte il risveglio funziona.
#
# Uso, da PowerShell aperto come amministratore, nella cartella del progetto:
#   powershell -ExecutionPolicy Bypass -File windows\imposta_notte.ps1

#Requires -RunAsAdministrator
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot

# 1. Ibernazione e risvegli programmati
powercfg /hibernate on
powercfg /SETACVALUEINDEX SCHEME_CURRENT SUB_SLEEP RTCWAKE 1      # consenti i timer di risveglio (corrente)
powercfg /SETDCVALUEINDEX SCHEME_CURRENT SUB_SLEEP RTCWAKE 1
powercfg /SETACVALUEINDEX SCHEME_CURRENT SUB_BUTTONS PBUTTONACTION 2   # tasto di accensione = iberna
powercfg /SETACTIVE SCHEME_CURRENT
# mostra "Iberna" nel menu Start > Arresta
$fly = "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\FlyoutMenuSettings"
New-Item -Path $fly -Force | Out-Null
Set-ItemProperty -Path $fly -Name ShowHibernateOption -Value 1 -Type DWord

# 2. Giro notturno: parte anche senza accesso a Windows
Write-Host ""
Write-Host "Inserisci la password di Windows di questo utente (per un account Microsoft e' la password dell'account," -ForegroundColor Yellow
Write-Host "non il PIN): serve perche' il giro parta di notte senza accesso. La conserva Windows, non il progetto." -ForegroundColor Yellow
$cred = Get-Credential -UserName "$env:USERDOMAIN\$env:USERNAME" -Message "Password di Windows per il giro notturno di ANDIAMO?"
$action = New-ScheduledTaskAction -Execute "$Root\windows\run_pipeline.bat" -Argument "notte" -WorkingDirectory $Root
$trigger = New-ScheduledTaskTrigger -Daily -At "01:00"
$settings = New-ScheduledTaskSettingsSet -WakeToRun -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries `
            -ExecutionTimeLimit (New-TimeSpan -Hours 4) -MultipleInstances IgnoreNew
Register-ScheduledTask -TaskName "Andiamoo-Pipeline" -Action $action -Trigger $trigger -Settings $settings `
    -User $cred.UserName -Password $cred.GetNetworkCredential().Password -RunLevel Limited -Force | Out-Null

Write-Host ""
Write-Host "Fatto:" -ForegroundColor Green
Write-Host " - ogni notte alle 01:00 il PC si risveglia e parte il giro di ANDIAMO?, poi torna in ibernazione;"
Write-Host " - la sera spegnilo con il tasto di accensione o con Start > Arresta > Iberna (NON 'Arresta il sistema':"
Write-Host "   da spento del tutto Windows non puo' riaccenderlo);"
Write-Host " - risvegli programmati attivi ora:"
powercfg /waketimers
