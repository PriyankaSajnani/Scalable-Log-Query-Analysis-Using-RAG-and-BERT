$ErrorActionPreference = "Stop"

# === Fix Path Resolution ===
$ScriptDir = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent
$logFile = "$ScriptDir\loglens_run.log"
$venvPath = "$env:USERPROFILE\LogLensEnv"
$reqFile = "$ScriptDir\requirements.txt"

function Write-Log {
    param($message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$timestamp - $message" | Out-File -Append -FilePath $logFile
}

Write-Log "Script started."

function Confirm-Success {
    param($label)
    Write-Host "$label ✔" -ForegroundColor Green
    Write-Log "$label success."
}

# === 1. Check Python ===
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "Python is not installed. Please install Python first." -ForegroundColor Red
    Write-Log "Python not found. Aborting."
    exit
}
Confirm-Success "Python detected"

# === 2. Check Ollama ===
$ollama = Get-Command ollama -ErrorAction SilentlyContinue
if (-not $ollama) {
    Write-Host "Ollama is not installed. Please install Ollama first." -ForegroundColor Red
    Write-Log "Ollama not found. Aborting."
    exit
}
Confirm-Success "Ollama detected"

# === 3. Check LLaMA model ===
Write-Host "Checking for llama 3.2 model..." -ForegroundColor Yellow
$modelList = ollama ls 2>&1
if (-not ($modelList -match "llama\s*3\.2")) {
    Write-Host "llama 3.2 model not found. Attempting to install..." -ForegroundColor Yellow
    Write-Log "llama 3.2 not found. Pulling..."
    $pullOutput = ollama pull llama:3.2 2>&1
    Write-Log "Pull output: $pullOutput"

    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to install llama 3.2 model automatically." -ForegroundColor Red
        Write-Host "Please run manually: ollama pull llama:3.2" -ForegroundColor Cyan
        Write-Log "llama:3.2 pull failed."
        Read-Host "Press Enter to continue..."
    } else {
        Confirm-Success "llama 3.2 installed"
    }
} else {
    Confirm-Success "llama 3.2 already installed"
}

# === 4. Create virtual environment ===
if (-not (Test-Path "$venvPath\Scripts\Activate.ps1")) {
    Write-Host "Creating virtual environment at $venvPath..." -ForegroundColor Yellow
    python -m venv $venvPath
    Confirm-Success "Virtual environment created"
} else {
    Write-Log "Virtual environment already exists."
    Write-Host "Virtual environment already exists." -ForegroundColor Cyan
}

# === 5. Activate and Install Requirements ===
Write-Host "Installing Python libraries from requirements.txt..." -ForegroundColor Yellow

. "$venvPath\Scripts\Activate.ps1"
pip install --upgrade pip
pip install -r $reqFile

Confirm-Success "Libraries installed"

# === 6. Final Welcome Message ===
Write-Host "`n==========================================" -ForegroundColor Cyan
Write-Host "      Welcome to LogLens People!" -ForegroundColor Green
Write-Host "   Please refer to the README to get started." -ForegroundColor Yellow
Write-Host "==========================================" -ForegroundColor Cyan
Write-Log "Installation complete. Ready for use."
