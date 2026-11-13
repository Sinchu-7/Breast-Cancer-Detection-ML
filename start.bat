@echo off
setlocal

set "ROOT=%~dp0"
set "PYTHON=python"

if exist "%ROOT%venv\Scripts\python.exe" set "PYTHON=%ROOT%venv\Scripts\python.exe"
if exist "%ROOT%.venv\Scripts\python.exe" set "PYTHON=%ROOT%.venv\Scripts\python.exe"

where python >nul 2>nul
if errorlevel 1 if not exist "%PYTHON%" (
    echo Python was not found. Install Python or create the project's venv.
    exit /b 1
)

where npm >nul 2>nul
if errorlevel 1 (
    echo npm was not found. Install Node.js and npm before starting the app.
    exit /b 1
)

if not exist "%ROOT%frontend\node_modules\vite\bin\vite.js" (
    echo Frontend dependencies are missing. Run "npm install" in the frontend folder.
    exit /b 1
)

"%PYTHON%" -c "import fastapi, uvicorn" >nul 2>nul
if errorlevel 1 (
    echo Backend dependencies are missing. Run "python -m pip install -r requirements.txt".
    exit /b 1
)

start "Histology Research API" /D "%ROOT%" "%PYTHON%" -m uvicorn backend.main:app --app-dir "%ROOT%" --host 127.0.0.1 --port 8000
start "Histology Research Frontend" /D "%ROOT%frontend" cmd /k "npm run dev -- --port 5173"
start "" "http://127.0.0.1:5173/"

echo.
echo Frontend: http://127.0.0.1:5173/
echo API docs: http://127.0.0.1:8000/docs
echo Close the API and frontend windows to stop the services.
