# Prepara il PC fisso per il lavoro notturno di ANDIAMO?:
#   - alle 01:00 Windows si risveglia da solo (da ibernazione o sospensione) e parte il giro
#     nella sessione rimasta aperta (anche a schermo bloccato);
#   - a fine giro il PC va in ibernazione (consumo come da spento), a meno che qualcuno lo stia usando;
#   - il tasto di accensione iberna invece di spegnere, cosi' la notte il risveglio funziona.
#
# Uso, da PowerShell aperto come amministratore, nella cartella del progetto:
#   powershell -ExecutionPolicy Bypass -File windows\imposta_notte.ps1

#Requires -RunAsAdministrator
param([switch]$SenzaAccesso)
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

# 2. Giro notturno alle 01:00 nella sessione dell'utente (nessuna password richiesta).
#    Funziona perche' l'ibernazione conserva la sessione aperta: al risveglio il giro parte li' dentro, anche a
#    schermo bloccato. Con -SenzaAccesso invece parte anche dopo un riavvio senza accesso (chiede la password).
$action = New-ScheduledTaskAction -Execute "$Root\windows\run_pipeline.bat" -Argument "notte" -WorkingDirectory $Root
$trigger = New-ScheduledTaskTrigger -Daily -At "01:00"
$settings = New-ScheduledTaskSettingsSet -WakeToRun -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries `
            -ExecutionTimeLimit (New-TimeSpan -Hours 4) -MultipleInstances IgnoreNew
if ($SenzaAccesso) {
    $cred = Get-Credential -UserName "$env:USERDOMAIN\$env:USERNAME" -Message "Password di Windows per il giro notturno di ANDIAMO?"
    Register-ScheduledTask -TaskName "Andiamoo-Pipeline" -Action $action -Trigger $trigger -Settings $settings `
        -User $cred.UserName -Password $cred.GetNetworkCredential().Password -RunLevel Limited -Force | Out-Null
} else {
    $principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive -RunLevel Limited
    Register-ScheduledTask -TaskName "Andiamoo-Pipeline" -Action $action -Trigger $trigger -Settings $settings `
        -Principal $principal -Force | Out-Null
}

Write-Host ""
Write-Host "Fatto:" -ForegroundColor Green
Write-Host " - ogni notte alle 01:00 il PC si risveglia e parte il giro di ANDIAMO?, poi torna in ibernazione;"
Write-Host " - la sera iberna il PC dalla tua sessione: tasto di accensione o Start > Arresta > Iberna"
Write-Host "   (NON 'Arresta il sistema' ne' 'Disconnetti': il giro parte nella sessione rimasta aperta);"
Write-Host " - risvegli programmati attivi ora:"
powercfg /waketimers
