# Elenca le automazioni del PC (programmi all'avvio, attivita' pianificate, accesso automatico),
# ne fa una copia di sicurezza e ELIMINA quelle che scegli in una finestra.
# Le attivita' di Windows (\Microsoft\...) e quelle di ANDIAMO? non vengono toccate.
#
# Uso, da PowerShell aperto come amministratore, nella cartella del progetto:
#   powershell -ExecutionPolicy Bypass -File windows\reset_automazioni.ps1
#
# La copia di sicurezza va in Documenti\backup-automazioni-<data>: da li' si puo' ripristinare
# (file .reg con doppio clic, attivita' con "Importa attivita'" nell'Utilita' di pianificazione).

#Requires -RunAsAdministrator
$ErrorActionPreference = "Continue"
$stamp = Get-Date -Format "yyyy-MM-dd_HHmm"
$backup = Join-Path ([Environment]::GetFolderPath("MyDocuments")) "backup-automazioni-$stamp"
New-Item -ItemType Directory -Force -Path $backup, "$backup\attivita", "$backup\esecuzione-automatica" | Out-Null
$items = New-Object System.Collections.ArrayList

# 1. Programmi che partono all'avvio (registro)
$runKeys = @(
    @{ Path = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run";             Reg = "HKCU\Software\Microsoft\Windows\CurrentVersion\Run";             File = "avvio-utente.reg" },
    @{ Path = "HKLM:\Software\Microsoft\Windows\CurrentVersion\Run";             Reg = "HKLM\Software\Microsoft\Windows\CurrentVersion\Run";             File = "avvio-pc.reg" },
    @{ Path = "HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Run"; Reg = "HKLM\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Run"; File = "avvio-pc-32bit.reg" }
)
foreach ($k in $runKeys) {
    if (-not (Test-Path $k.Path)) { continue }
    reg export $k.Reg (Join-Path $backup $k.File) /y | Out-Null
    $props = (Get-ItemProperty $k.Path).PSObject.Properties | Where-Object { $_.Name -notlike "PS*" }
    foreach ($p in $props) {
        [void]$items.Add([pscustomobject]@{ Tipo = "Programma all'avvio"; Nome = $p.Name; Dettaglio = [string]$p.Value; Dove = $k.Path })
    }
}

# 2. Collegamenti nelle cartelle Esecuzione automatica
foreach ($f in @([Environment]::GetFolderPath("Startup"), [Environment]::GetFolderPath("CommonStartup"))) {
    Get-ChildItem $f -File -ErrorAction SilentlyContinue | Where-Object { $_.Name -ne "desktop.ini" } | ForEach-Object {
        Copy-Item $_.FullName "$backup\esecuzione-automatica\" -Force
        [void]$items.Add([pscustomobject]@{ Tipo = "Programma all'avvio (cartella)"; Nome = $_.Name; Dettaglio = $_.FullName; Dove = $f })
    }
}

# 3. Attivita' pianificate non di Windows (anche quelle che accendono il PC)
Get-ScheduledTask | Where-Object { $_.TaskPath -notlike "\Microsoft\*" -and $_.TaskName -notlike "Andiamoo-*" } | ForEach-Object {
    $safe = ($_.TaskPath + $_.TaskName) -replace '[\\/:*?"<>|]', '_'
    Export-ScheduledTask -TaskName $_.TaskName -TaskPath $_.TaskPath | Out-File "$backup\attivita\$safe.xml" -Encoding utf8
    $azioni = ($_.Actions | ForEach-Object { "$($_.Execute) $($_.Arguments)".Trim() }) -join "; "
    $tipo = if ($_.Settings.WakeToRun) { "Attivita' pianificata (accende il PC)" } else { "Attivita' pianificata" }
    [void]$items.Add([pscustomobject]@{ Tipo = $tipo; Nome = $_.TaskName; Dettaglio = $azioni; Dove = $_.TaskPath })
}

# 4. Accesso automatico a Windows
$wl = "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon"
$w = Get-ItemProperty $wl
if ($w.AutoAdminLogon -eq "1") {
    reg export "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" "$backup\accesso-automatico.reg" /y | Out-Null
    [void]$items.Add([pscustomobject]@{ Tipo = "Accesso automatico"; Nome = "AutoAdminLogon"; Dettaglio = "Windows entra da solo come $($w.DefaultUserName)"; Dove = $wl })
}

# Stato attuale del risparmio energia e dei risvegli programmati (solo copia, non si modifica qui)
powercfg /waketimers > "$backup\risvegli-programmati.txt"
powercfg /query > "$backup\risparmio-energia.txt"
$items | Export-Csv "$backup\elenco.csv" -NoTypeInformation -Encoding UTF8

if ($items.Count -eq 0) { Write-Host "Nessuna automazione trovata." -ForegroundColor Green; exit 0 }
Write-Host "Trovate $($items.Count) automazioni. Copia di sicurezza in: $backup" -ForegroundColor Cyan
Write-Host "Nella finestra seleziona cosa eliminare (Ctrl+A = tutto, Ctrl+clic = piu' righe) e premi OK." -ForegroundColor Yellow
$sel = $items | Out-GridView -Title "Seleziona le automazioni da ELIMINARE e premi OK (Annulla = nessuna)" -PassThru
if (-not $sel) { Write-Host "Nessuna modifica." -ForegroundColor Green; exit 0 }

foreach ($i in $sel) {
    switch -Wildcard ($i.Tipo) {
        "Programma all'avvio"            { Remove-ItemProperty -Path $i.Dove -Name $i.Nome -ErrorAction SilentlyContinue }
        "Programma all'avvio (cartella)" { Remove-Item -LiteralPath $i.Dettaglio -Force -ErrorAction SilentlyContinue }
        "Attivita' pianificata*"         { Unregister-ScheduledTask -TaskName $i.Nome -TaskPath $i.Dove -Confirm:$false -ErrorAction SilentlyContinue }
        "Accesso automatico"             {
            Set-ItemProperty $wl -Name AutoAdminLogon -Value "0"
            Remove-ItemProperty $wl -Name DefaultPassword -ErrorAction SilentlyContinue
        }
    }
    Write-Host "Eliminato: $($i.Tipo) - $($i.Nome)"
}
Write-Host ""
Write-Host "Fatto. Copia di sicurezza in: $backup" -ForegroundColor Green
Write-Host "Restano le impostazioni del BIOS (accensione programmata): si cambiano solo dal BIOS all'avvio." -ForegroundColor Yellow
