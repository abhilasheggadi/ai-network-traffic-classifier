@echo off
REM AI Network Traffic Classifier - Quick Start Script (Windows)
REM Starts FastAPI backend and Streamlit dashboard

echo.
echo =====================================
echo    AI Network Traffic Classifier
echo =====================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Error: Virtual environment not found!
    echo Please run: python -m venv venv
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if packages are installed
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo Error: Dependencies not installed!
    echo Please run: pip install -r requirements.txt
    pause
    exit /b 1
)

REM Create logs directory if it doesn't exist
if not exist "logs\" mkdir logs

echo.
echo Environment ready!
echo.

REM Start FastAPI backend in new window
echo Starting FastAPI Backend (port 8000)...
start "FastAPI Backend" cmd /k "python -m uvicorn backend.main:app --reload --port 8000"
timeout /t 2 /nobreak

REM Start Streamlit dashboard
echo Starting Streamlit Dashboard (port 8501)...
echo.
echo =====================================
echo Dashboard:  http://localhost:8501
echo API:        http://127.0.0.1:8000
echo API Docs:   http://127.0.0.1:8000/docs
echo =====================================
echo.
python -m streamlit run src/dashboard/app.py --server.port 8501

pause
