# Prepara il PC fisso per il lavoro notturno di ANDIAMO?:
#   - alle 01:00 Windows si risveglia da solo (da ibernazione o sospensione) e parte il giro
#     ANCHE SE NESSUNO HA FATTO L'ACCESSO (schermata "Accedi"): non serve la password di Windows;
#   - a fine giro il PC va in ibernazione (consumo come da spento), a meno che qualcuno lo stia usando;
#   - il tasto di accensione iberna invece di spegnere, cosi' la notte il risveglio funziona.
#
# Uso, da PowerShell aperto come amministratore, nella cartella del progetto:
#   powershell -ExecutionPolicy Bypass -File windows\imposta_notte.ps1

#Requires -RunAsAdministrator
param(
    [switch]$Interattivo,   # vecchia modalita': il giro parte solo se la tua sessione e' aperta
    [switch]$ConPassword    # ripiego se la prova senza password fallisce: Windows chiede la tua password e la conserva
)
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

# 2. Giro notturno alle 01:00 anche senza accesso a Windows.
#    Le attivita' girano con il tuo utente in modalita' "esegui anche se l'utente non e' connesso, senza
#    memorizzare la password" (S4U): nessuna password richiesta. In questa modalita' Windows non sblocca le
#    credenziali salvate, quindi GitHub si raggiunge con una chiave dedicata al progetto (chiave_github.ps1).
if (-not $Interattivo) {
    & powershell -NoProfile -ExecutionPolicy Bypass -File "$Root\windows\chiave_github.ps1"
    if ($LASTEXITCODE -ne 0) { throw "Collegamento a GitHub non riuscito: rilancia questo script dopo aver aggiunto la chiave." }
}
$action = New-ScheduledTaskAction -Execute "$Root\windows\run_pipeline.bat" -Argument "notte" -WorkingDirectory $Root
$trigger = New-ScheduledTaskTrigger -Daily -At "01:00"
$settings = New-ScheduledTaskSettingsSet -WakeToRun -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries `
            -ExecutionTimeLimit (New-TimeSpan -Hours 4) -MultipleInstances IgnoreNew
# Resoconto su Telegram alle 07:30, dopo la revisione di Claude (03:37): risveglio, invio, di nuovo ibernazione
$repAction = New-ScheduledTaskAction -Execute "$Root\windows\run_report.bat" -Argument "notte" -WorkingDirectory $Root
$repTrigger = New-ScheduledTaskTrigger -Daily -At "07:30"
$repSettings = New-ScheduledTaskSettingsSet -WakeToRun -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries `
               -ExecutionTimeLimit (New-TimeSpan -Minutes 20) -MultipleInstances IgnoreNew
$who = "$env:USERDOMAIN\$env:USERNAME"
if ($ConPassword) {
    $cred = Get-Credential -UserName $who -Message "Password di Windows (o dell'account Microsoft) per il giro notturno"
    $pw = $cred.GetNetworkCredential().Password
    foreach ($t in @(@("Andiamoo-Pipeline", $action, $trigger, $settings), @("Andiamoo-Resoconto", $repAction, $repTrigger, $repSettings))) {
        Register-ScheduledTask -TaskName $t[0] -Action $t[1] -Trigger $t[2] -Settings $t[3] -User $who -Password $pw `
            -RunLevel Highest -Force | Out-Null
    }
    $principal = $null
} else {
    $logon = if ($Interattivo) { "Interactive" } else { "S4U" }
    $principal = New-ScheduledTaskPrincipal -UserId $who -LogonType $logon -RunLevel Highest
    Register-ScheduledTask -TaskName "Andiamoo-Pipeline" -Action $action -Trigger $trigger -Settings $settings `
        -Principal $principal -Force | Out-Null
    Register-ScheduledTask -TaskName "Andiamoo-Resoconto" -Action $repAction -Trigger $repTrigger -Settings $repSettings `
        -Principal $principal -Force | Out-Null
}

# 3. Prova subito, nella stessa modalita' della notte (senza raccogliere eventi e senza ibernare):
#    rete, GitHub in lettura e scrittura, Ollama, Python. Il risultato e' in logs\prova_notte.log
$probe = New-ScheduledTaskAction -Execute "$Root\windows\prova_notte.bat" -WorkingDirectory $Root
$probeSettings = New-ScheduledTaskSettingsSet -ExecutionTimeLimit (New-TimeSpan -Minutes 10)
if ($ConPassword) {
    Register-ScheduledTask -TaskName "Andiamoo-Prova" -Action $probe -Settings $probeSettings -User $who -Password $pw `
        -RunLevel Highest -Force | Out-Null
} else {
    Register-ScheduledTask -TaskName "Andiamoo-Prova" -Action $probe -Settings $probeSettings -Principal $principal -Force | Out-Null
}
$log = "$Root\logs\prova_notte.log"
Remove-Item $log -ErrorAction SilentlyContinue
Start-ScheduledTask -TaskName "Andiamoo-Prova"
Write-Host "Prova del giro senza accesso in corso (fino a 2 minuti)..."
for ($i = 0; $i -lt 60 -and -not (Select-String -Path $log -Pattern "FINE PROVA" -Quiet -ErrorAction SilentlyContinue); $i++) {
    Start-Sleep -Seconds 3
}
if (Test-Path $log) {
    Get-Content $log
    if (Select-String -Path $log -Pattern "\[NO\]" -Quiet) {
        Write-Host "Qualcosa non va (righe [NO] qui sopra): manda questo testo a Claude." -ForegroundColor Red
    } else {
        Write-Host "Prova riuscita: il giro notturno funziona anche senza accesso a Windows." -ForegroundColor Green
    }
} else {
    $info = Get-ScheduledTaskInfo -TaskName "Andiamoo-Prova"
    Write-Host "La prova non e' partita (codice $('0x{0:X}' -f $info.LastTaskResult))." -ForegroundColor Red
    if (-not $ConPassword) { Write-Host "Rilancia lo script con -ConPassword: Windows ti chiedera' la password del tuo account." -ForegroundColor Yellow }
}
Unregister-ScheduledTask -TaskName "Andiamoo-Prova" -Confirm:$false

Write-Host ""
Write-Host "Fatto:" -ForegroundColor Green
Write-Host " - ogni notte alle 01:00 il PC si risveglia e parte il giro di ANDIAMO?, poi torna in ibernazione;"
Write-Host " - alle 07:30 si risveglia per mandarti il resoconto su Telegram, poi torna in ibernazione;"
Write-Host " - funziona anche se il PC resta sulla schermata 'Accedi': non serve fare l'accesso;"
Write-Host " - la sera iberna il PC (tasto di accensione o Start > Arresta > Iberna). Da 'Arresta il sistema'"
Write-Host "   alcuni PC non si risvegliano da soli: se succede, usa sempre Iberna;"
Write-Host " - risvegli programmati attivi ora:"
powercfg /waketimers
