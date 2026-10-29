# Installazione sul PC fisso (Windows 10/11). Eseguire da PowerShell nella cartella del progetto:
#   powershell -ExecutionPolicy Bypass -File windows\setup.ps1
# Installa Python, Git, Ollama e cloudflared (se mancano), scarica il modello AI, prepara l'ambiente Python,
# registra le attivita' pianificate. Si puo' rilanciare: i passaggi gia' fatti vengono saltati.

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
Write-Host "Cartella progetto: $Root" -ForegroundColor Cyan

function Need($cmd) { -not (Get-Command $cmd -ErrorAction SilentlyContinue) }

# 1. Programmi di base
if (Need "python") {
    Write-Host "Installo Python 3.12..." -ForegroundColor Yellow
    winget install --id Python.Python.3.12 -e --accept-source-agreements --accept-package-agreements
}
if (Need "git") {
    Write-Host "Installo Git..." -ForegroundColor Yellow
    winget install --id Git.Git -e --accept-source-agreements --accept-package-agreements
}
if (Need "ollama") {
    Write-Host "Installo Ollama..." -ForegroundColor Yellow
    winget install --id Ollama.Ollama -e --accept-source-agreements --accept-package-agreements
}
if (Need "cloudflared") {
    Write-Host "Installo cloudflared (tunnel per l'API del sito)..." -ForegroundColor Yellow
    winget install --id Cloudflare.cloudflared -e --accept-source-agreements --accept-package-agreements
}
# aggiorna il PATH della sessione dopo le installazioni
$env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")

# 2. Modello AI (gemma3:12b, circa 8 GB: sta nella memoria della RTX 4070 Super)
$model = (Select-String -Path "config\settings.yaml" -Pattern 'text_model:\s*"([^"]+)"').Matches[0].Groups[1].Value
Write-Host "Scarico il modello $model (solo la prima volta, alcuni minuti)..." -ForegroundColor Yellow
ollama pull $model

# 3. Ambiente Python
if (-not (Test-Path ".venv")) { python -m venv .venv }
& .\.venv\Scripts\python.exe -m pip install --upgrade pip
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
& .\.venv\Scripts\python.exe -m playwright install chromium

# 4. Configurazione
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Creato .env: aprilo e inserisci token Telegram e id amministratore." -ForegroundColor Magenta
}
New-Item -ItemType Directory -Force -Path "logs" | Out-Null

# 5. Test rapido
& .\.venv\Scripts\python.exe -m pytest -q tests

# 6. Attivita' pianificate
& "$PSScriptRoot\register_tasks.ps1"

Write-Host ""
# 7. Avvio subito di API e tunnel (poi partono da soli a ogni accesso)
Start-ScheduledTask -TaskName "Andiamoo-API"
Start-ScheduledTask -TaskName "Andiamoo-Tunnel"

Write-Host "Fatto. Primo giro manuale:  windows\run_pipeline.bat" -ForegroundColor Green
