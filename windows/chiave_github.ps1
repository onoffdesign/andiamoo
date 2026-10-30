# Collega il PC a GitHub con una "chiave di distribuzione" (deploy key) valida solo per il progetto andiamoo.
#
# Perche': il giro notturno deve partire anche quando nessuno ha fatto l'accesso a Windows. In quel caso Windows
# non sblocca le credenziali salvate (Gestione credenziali) e il "git push" con la password di GitHub fallisce.
# Una chiave SSH dedicata e' un file del PC: funziona anche senza accesso, e da' accesso solo a questo progetto.
#
# La chiave privata resta sul PC (cartella .ssh dell'utente). Su GitHub va solo la parte pubblica.
#
# Uso (lo richiama imposta_notte.ps1; si puo' anche lanciare da solo):
#   powershell -ExecutionPolicy Bypass -File windows\chiave_github.ps1

$ErrorActionPreference = "Continue"   # i messaggi di git su stderr non devono fermare lo script
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
$Repo = "onoffdesign/andiamoo"
$SshDir = Join-Path $env:USERPROFILE ".ssh"
$Key = Join-Path $SshDir "andiamoo_deploy"
$Ssh = "C:/Windows/System32/OpenSSH/ssh.exe"
$Remote = "ssh://git@ssh.github.com:443/$Repo.git"     # porta 443: passa anche dalle reti che bloccano la 22

if (-not (Test-Path "C:\Windows\System32\OpenSSH\ssh-keygen.exe")) {
    throw "Manca il client OpenSSH di Windows: Impostazioni > App > Funzionalita' facoltative > Aggiungi 'Client OpenSSH'."
}

# 1. chiave dedicata (senza frase segreta, perche' deve funzionare di notte senza nessuno davanti)
if (-not (Test-Path $Key)) {
    New-Item -ItemType Directory -Force -Path $SshDir | Out-Null
    Start-Process -FilePath "C:\Windows\System32\OpenSSH\ssh-keygen.exe" -Wait -NoNewWindow `
        -ArgumentList @("-q", "-t", "ed25519", "-C", "andiamoo-pc-$env:COMPUTERNAME", "-f", "`"$Key`"", "-N", '""')
    Write-Host "Chiave creata: $Key" -ForegroundColor Green
}
$Pub = (Get-Content "$Key.pub" -Raw).Trim()

# 2. git usa la chiave per questo progetto
$KeyFwd = $Key -replace "\\", "/"
git config core.sshCommand "`"$Ssh`" -i `"$KeyFwd`" -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new"

function Test-Push {
    $old = (git remote get-url origin)
    git remote set-url origin $Remote
    git ls-remote origin HEAD *> $null
    $okRead = ($LASTEXITCODE -eq 0)
    git push --dry-run origin HEAD:refs/heads/prova-chiave-pc *> $null     # prova di scrittura, non crea nulla
    $okWrite = ($LASTEXITCODE -eq 0)
    if (-not ($okRead -and $okWrite)) { git remote set-url origin $old }
    return ($okRead -and $okWrite)
}

if (Test-Push) {
    Write-Host "GitHub raggiungibile con la chiave del PC: lettura e scrittura OK." -ForegroundColor Green
    exit 0
}

# 3. la parte pubblica va aggiunta su GitHub (una volta sola)
Set-Clipboard -Value $Pub
Write-Host ""
Write-Host "Serve un passaggio su GitHub (una volta sola):" -ForegroundColor Yellow
Write-Host " 1. si apre la pagina 'Deploy keys' del progetto (accedi a GitHub se te lo chiede);"
Write-Host " 2. Title: ANDIAMO PC fisso"
Write-Host " 3. Key: incolla (Ctrl+V) - e' gia' negli appunti. E' questa riga:"
Write-Host "    $Pub" -ForegroundColor Cyan
Write-Host " 4. spunta 'Allow write access' e premi 'Add key'."
Start-Process "https://github.com/$Repo/settings/keys/new"
Read-Host "Quando hai premuto 'Add key', torna qui e premi Invio"

if (Test-Push) {
    Write-Host "GitHub raggiungibile con la chiave del PC: lettura e scrittura OK." -ForegroundColor Green
    exit 0
}
Write-Host "La chiave non funziona ancora. Controlla di aver spuntato 'Allow write access', poi rilancia questo script." -ForegroundColor Red
exit 1
