@echo off
REM GenAI Governance Streamlit Frontend Startup Script for Windows

echo 🚀 Starting GenAI Governance Streamlit Frontend...

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.8+ first.
    echo    Download from: https://python.org/
    pause
    exit /b 1
)

REM Check if Streamlit is installed
streamlit --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 📦 Installing Streamlit...
    pip install streamlit
    if %errorlevel% neq 0 (
        echo ❌ Failed to install Streamlit
        pause
        exit /b 1
    )
)

REM Navigate to frontend directory
cd frontend

REM Check if backend is running
echo 🔍 Checking backend connection...
curl -s http://localhost:8000/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Backend is running on http://localhost:8000
) else (
    echo ⚠️  Backend is not running on http://localhost:8000
    echo    Please start the backend first:
    echo    cd backend ^&^& python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
    echo.
    set /p response="Continue anyway? (y/n): "
    if /i not "%response%"=="y" (
        pause
        exit /b 1
    )
)

echo 🎨 Starting Streamlit development server...
echo 📱 Frontend will be available at: http://localhost:8501
echo 🔗 Backend API: http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the Streamlit server
streamlit run app.py 