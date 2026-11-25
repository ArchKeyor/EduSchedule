# Script de Inicializacao Automatica das Turmas do Professor (EDS)
$ErrorActionPreference = "Stop"

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host " EduSchedule / TimeTabling UGB - Carga Oficial do Professor" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

$rootDir = Split-Path -Parent $PSScriptRoot
Set-Location $rootDir

# 1. Checar venv
if (-not (Test-Path ".venv")) {
    Write-Host "[1/4] Criando ambiente virtual Python..." -ForegroundColor Yellow
    python -m venv .venv
    & .\.venv\Scripts\pip.exe install -r backend\requirements.txt
} else {
    Write-Host "[1/4] Ambiente virtual Python encontrado." -ForegroundColor Green
}

# 1.1 Checar node_modules
if (-not (Test-Path "frontend\node_modules")) {
    Write-Host "Instalando dependencias do frontend (npm install)..." -ForegroundColor Yellow
    npm --prefix frontend install
}

# 2. Migracoes e Seed
Write-Host "[2/4] Executando migracoes e seed oficial EDS..." -ForegroundColor Yellow
& .\.venv\Scripts\python.exe backend\manage.py migrate --noinput
& .\.venv\Scripts\python.exe backend\manage.py seed_data --scenario=eds

# 3. Servidores
Write-Host "[3/4] Iniciando servidores em background..." -ForegroundColor Yellow
Start-Process -FilePath "cmd.exe" -ArgumentList "/k", "cd /d `"$rootDir`" && .\.venv\Scripts\activate.bat && python backend\manage.py runserver 127.0.0.1:8000" -WindowStyle Minimized
Start-Process -FilePath "cmd.exe" -ArgumentList "/k", "cd /d `"$rootDir\frontend`" && npm run dev" -WindowStyle Minimized

Start-Sleep -Seconds 3

Write-Host ""
Write-Host "========================================================" -ForegroundColor Green
Write-Host " Ambiente 100% ativo com as turmas do professor!" -ForegroundColor Green
Write-Host " Frontend UI: http://localhost:5173/" -ForegroundColor Cyan
Write-Host " Backend API: http://127.0.0.1:8000/api/" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Green

Start-Process "http://localhost:5173/"
