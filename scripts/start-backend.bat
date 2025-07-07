@echo off
REM GenAI Governance Backend Startup Script for Windows

echo 🚀 Starting GenAI Governance Backend...

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.8+ first.
    echo    Download from: https://python.org/
    pause
    exit /b 1
)

REM Check if required packages are installed
echo 📦 Checking dependencies...
python -c "import fastapi, uvicorn" >nul 2>&1
if %errorlevel% neq 0 (
    echo 📦 Installing required packages...
    pip install fastapi uvicorn
    if %errorlevel% neq 0 (
        echo ❌ Failed to install required packages
        pause
        exit /b 1
    )
)

REM Navigate to backend directory
cd backend

echo 🔧 Starting FastAPI server...
echo 📱 Backend will be available at: http://localhost:8000
echo 📚 API Documentation: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the FastAPI server
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000 