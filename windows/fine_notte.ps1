# A fine giro notturno: iberna il PC, a meno che qualcuno lo stia usando.
# "In uso" = c'e' una sessione aperta (explorer.exe) e lo schermo non e' bloccato (LogonUI.exe assente).
# Funziona anche su Windows Home.
$sessione = Get-Process -Name explorer -ErrorAction SilentlyContinue
$bloccato = Get-Process -Name LogonUI -ErrorAction SilentlyContinue
if ($sessione -and -not $bloccato) {
    Write-Output "$(Get-Date -Format s) Il PC e' in uso (sessione aperta e sbloccata): niente ibernazione."
} else {
    Write-Output "$(Get-Date -Format s) Giro finito: ibernazione."
    shutdown /h
}
