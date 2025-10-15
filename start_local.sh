#!/bin/bash

# 🚀 Start Full-Stack Tonkin Knowledge Finder Locally
# This script starts both the backend API and React frontend

echo "🚀 Starting Tonkin Knowledge Finder - Full Stack"
echo "=================================================="
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11+"
    exit 1
fi

# Check if Node.js is available
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+"
    exit 1
fi

echo "📦 Installing Python dependencies..."
pip install -r requirements.txt -q

echo ""
echo "📦 Installing React dependencies..."
cd frontend
npm install --silent

echo ""
echo "🔧 Starting Backend API (FastAPI)..."
cd ..
uvicorn api:app --reload --port 8000 &
BACKEND_PID=$!
echo "✅ Backend API running at: http://localhost:8000"
echo "📚 API Docs available at: http://localhost:8000/docs"

# Wait a bit for backend to start
sleep 3

echo ""
echo "🔧 Starting Frontend (React)..."
cd frontend
npm start &
FRONTEND_PID=$!
echo "✅ Frontend running at: http://localhost:3000"

echo ""
echo "=================================================="
echo "🎉 Full-Stack Application Started!"
echo "=================================================="
echo ""
echo "Frontend: http://localhost:3000"
echo "Backend:  http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Function to kill both processes on exit
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Stopped!"
    exit 0
}

# Trap Ctrl+C
trap cleanup INT TERM

# Wait for processes
wait

