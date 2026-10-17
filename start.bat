@echo off
REM Smart Shopping Platform - one-click start for Windows
setlocal
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
  echo [ERROR] Python 3.10 or newer is required. Install it from https://www.python.org/downloads/ ^(tick "Add Python to PATH"^).
  pause & exit /b 1
)
where npm >nul 2>nul
if errorlevel 1 (
  echo [ERROR] Node.js 18 or newer is required. Install it from https://nodejs.org/
  pause & exit /b 1
)

if not exist .env (
  copy /Y .env.example .env >nul
  echo Created .env from .env.example. You can add AI_API_KEY there later ^(optional^).
)

if not exist backend\venv\Scripts\python.exe (
  echo Creating Python virtual environment...
  python -m venv backend\venv || (echo [ERROR] Could not create venv & pause & exit /b 1)
)
echo Installing backend packages...
call backend\venv\Scripts\python.exe -m pip install --disable-pip-version-check -q -r backend\requirements.txt || (echo [ERROR] pip install failed & pause & exit /b 1)

if not exist frontend\node_modules (
  echo Installing frontend packages ^(first time only, takes a minute^)...
  pushd frontend
  call npm install --no-audit --no-fund || (echo [ERROR] npm install failed & popd & pause & exit /b 1)
  popd
)

echo Starting backend  on http://localhost:8000  ^(database is created and seeded automatically^)
start "Smart Shopping - Backend" cmd /k "cd /d %~dp0backend && venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000"
echo Starting frontend on http://localhost:5173
start "Smart Shopping - Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

timeout /t 8 >nul
start http://localhost:5173
echo.
echo Done. Demo logins are listed in README.md ^(user@example.com / admin@example.com^).
echo Close the two black windows to stop the servers.
endlocal
