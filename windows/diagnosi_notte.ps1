# Diagnosi del giro notturno: perche' il PC non ha lavorato o non si e' ibernato.
# Stampa (e salva in logs\diagnosi.txt) lo stato delle attivita', i timer di risveglio, gli ultimi
# spegnimenti/ibernazioni/risvegli di Windows e la fine del log del giro. Non cambia nulla, tranne attivare la
# cronologia dell'Utilita' di pianificazione (cosi' la prossima volta si vede anche perche' un'attivita' non parte).
#
# Uso (PowerShell come amministratore):
#   powershell -ExecutionPolicy Bypass -File C:\Users\Nitropc\Documents\andiamoo\windows\diagnosi_notte.ps1

$ErrorActionPreference = "Continue"
$Root = Split-Path -Parent $PSScriptRoot
$Out = Join-Path $Root "logs\diagnosi.txt"
New-Item -ItemType Directory -Force -Path (Join-Path $Root "logs") | Out-Null
$since = (Get-Date).AddDays(-5)

& {
    "===== DIAGNOSI $(Get-Date -Format s) ====="
    "--- Attivita' pianificate"
    foreach ($n in "Andiamoo-Pipeline", "Andiamoo-Resoconto") {
        $t = Get-ScheduledTask -TaskName $n -ErrorAction SilentlyContinue
        if (-not $t) { "$n : NON TROVATA"; continue }
        $i = Get-ScheduledTaskInfo -TaskName $n
        "{0} : stato={1} ultimo_avvio={2} risultato=0x{3:X} prossimo={4} accesso={5} risveglio={6}" -f `
            $n, $t.State, $i.LastRunTime, $i.LastTaskResult, $i.NextRunTime, $t.Principal.LogonType, $t.Settings.WakeToRun
    }
    "--- Timer di risveglio attivi"
    powercfg /waketimers
    "--- Piano energetico"
    powercfg /getactivescheme
    powercfg /query SCHEME_CURRENT SUB_SLEEP RTCWAKE | Select-String "Indice impostazione corrente|Current AC Power Setting|Current DC Power Setting|Impostazione corrente"
    "--- Rete (cavo o Wi-Fi; i profili Wi-Fi 'di tutti gli utenti' si collegano anche senza accesso)"
    Get-NetAdapter -Physical -ErrorAction SilentlyContinue | ForEach-Object { "{0} : {1} ({2})" -f $_.Name, $_.Status, $_.MediaType }
    netsh wlan show profiles 2>$null | Select-String "Profilo|Profile"
    "--- Accensioni, spegnimenti, ibernazioni e risvegli dal $($since.ToString('dd/MM'))"
    $ids = @{ "Microsoft-Windows-Kernel-General" = @(12, 13); "Microsoft-Windows-Kernel-Power" = @(41, 42, 107, 506, 507);
              "Microsoft-Windows-Power-Troubleshooter" = @(1); "User32" = @(1074); "EventLog" = @(6008) }
    $ev = foreach ($p in $ids.Keys) {
        Get-WinEvent -FilterHashtable @{ LogName = "System"; ProviderName = $p; Id = $ids[$p]; StartTime = $since } -ErrorAction SilentlyContinue
    }
    $ev | Sort-Object TimeCreated | ForEach-Object {
        $msg = ($_.Message -split "`r?`n" | Where-Object { $_.Trim() } | Select-Object -First 3) -join " | "
        if ($msg.Length -gt 230) { $msg = $msg.Substring(0, 230) }
        "{0:dd/MM HH:mm} {1}/{2} {3}" -f $_.TimeCreated, ($_.ProviderName -replace "Microsoft-Windows-", ""), $_.Id, $msg
    }
    "--- Cronologia dell'Utilita' di pianificazione (Andiamoo)"
    Get-WinEvent -FilterHashtable @{ LogName = "Microsoft-Windows-TaskScheduler/Operational"; StartTime = $since } -ErrorAction SilentlyContinue |
        Where-Object { $_.Message -match "Andiamoo" } | Sort-Object TimeCreated | Select-Object -Last 25 | ForEach-Object {
            "{0:dd/MM HH:mm} {1} {2}" -f $_.TimeCreated, $_.Id, (($_.Message -split "`r?`n")[0])
        }
    "--- Fine del log del giro"
    $log = Join-Path $Root "logs\pipeline.log"
    if (Test-Path $log) {
        Select-String -Path $log -Pattern "=====|Sessione|ibernazione|in uso|ERROR|Pubblicato|rete|Fine del giro|Eventi sul sito|allineato|error:" |
            Select-Object -Last 30 | ForEach-Object { $_.Line }
    } else { "logs\pipeline.log non trovato" }
} 2>&1 | Tee-Object -FilePath $Out

# da ora la cronologia delle attivita' resta registrata (utile per le prossime diagnosi)
wevtutil sl Microsoft-Windows-TaskScheduler/Operational /e:true 2>$null
Write-Host ""
Write-Host "Salvato anche in $Out" -ForegroundColor Green
