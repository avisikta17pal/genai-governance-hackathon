@echo off
REM GenAI Governance Frontend Startup Script for Windows

echo 🚀 Starting GenAI Governance Frontend...

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed. Please install Node.js 16+ first.
    echo    Download from: https://nodejs.org/
    pause
    exit /b 1
)

REM Check if npm is installed
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ npm is not installed. Please install npm first.
    pause
    exit /b 1
)

REM Navigate to frontend directory
cd frontend

REM Check if node_modules exists
if not exist "node_modules" (
    echo 📦 Installing dependencies...
    npm install
    if %errorlevel% neq 0 (
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Check if backend is running
echo 🔍 Checking backend connection...
curl -s http://localhost:8000/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Backend is running on http://localhost:8000
) else (
    echo ⚠️  Backend is not running on http://localhost:8000
    echo    Please start the backend first:
    echo    cd backend ^&^& uvicorn main:app --reload --host 0.0.0.0 --port 8000
    echo.
    set /p response="Continue anyway? (y/n): "
    if /i not "%response%"=="y" (
        pause
        exit /b 1
    )
)

echo 🎨 Starting React development server...
echo 📱 Frontend will be available at: http://localhost:3000
echo 🔗 Backend API: http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the development server
npm start 