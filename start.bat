@echo off
echo Starting PGRKAM Bot...

REM Install Backend Dependencies
echo Installing backend dependencies...
cd backend
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install backend dependencies
    pause
    exit /b 1
)

REM Start Backend
echo Starting Backend Server...
start "Backend" cmd /k "python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

REM Wait for backend to start
timeout /t 8 /nobreak >nul

REM Install Frontend Dependencies
echo Installing frontend dependencies...
cd ..\chatbot-ui\web
npm install
if %errorlevel% neq 0 (
    echo Failed to install frontend dependencies
    pause
    exit /b 1
)

REM Start Frontend
echo Starting Frontend...
start "Frontend" cmd /k "npm run dev"

echo Both servers are starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo Wait for both servers to fully start before testing
pause