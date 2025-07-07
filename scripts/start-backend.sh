#!/bin/bash

# GenAI Governance Backend Startup Script

echo "🚀 Starting GenAI Governance Backend..."

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.8+ first."
    echo "   Download from: https://python.org/"
    exit 1
fi

# Check if required packages are installed
echo "📦 Checking dependencies..."
if ! python -c "import fastapi, uvicorn" &> /dev/null; then
    echo "📦 Installing required packages..."
    pip install fastapi uvicorn
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install required packages"
        exit 1
    fi
fi

# Navigate to backend directory
cd backend

echo "🔧 Starting FastAPI server..."
echo "📱 Backend will be available at: http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the FastAPI server
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000 