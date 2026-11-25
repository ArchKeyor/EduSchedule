@echo off
chcp 65001 > nul
echo ========================================================
echo  EduSchedule / TimeTabling UGB - Carga Oficial do Professor
echo ========================================================
echo.

cd /d "%~dp0\.."

REM 1. Verificar .venv
if not exist ".venv" (
    echo [1/4] Criando ambiente virtual Python...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    echo Instalando dependencias do backend...
    pip install -r backend\requirements.txt
) else (
    echo [1/4] Ambiente virtual Python encontrado.
    call .venv\Scripts\activate.bat
)

REM 1.1 Verificar dependencias do frontend
if not exist "frontend\node_modules" (
    echo Instalando dependencias do frontend (npm install)...
    cd frontend && call npm install && cd ..
)

REM 2. Migracoes e Seed Oficial EDS
echo [2/4] Executando migracoes e seed oficial do professor (EDS)...
python backend\manage.py migrate --noinput
python backend\manage.py seed_data --scenario=eds

REM 3. Iniciar Backend em nova janela
echo [3/4] Iniciando backend Django na porta 8000...
start "TimeTabling Backend (Django)" cmd /k "cd /d %~dp0\.. && .venv\Scripts\activate.bat && python backend\manage.py runserver 127.0.0.1:8000"

REM 4. Iniciar Frontend em nova janela
echo [4/4] Iniciando frontend Vite na porta 5173...
start "TimeTabling Frontend (React)" cmd /k "cd /d %~dp0\..\frontend && npm run dev"

echo.
echo ========================================================
echo  Ambiente 100%% ativo com as turmas do professor!
echo  Frontend UI: http://localhost:5173/
echo  Backend API: http://127.0.0.1:8000/api/
echo ========================================================
echo.
timeout /t 3 > nul
start http://localhost:5173/
pause
