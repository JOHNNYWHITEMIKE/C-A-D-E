#!/bin/bash

# C-A-D-E Startup Script

echo "🤖 Starting C-A-D-E - Community Application Development Environment"
echo ""

# Check if Docker is available
if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
    echo "✓ Docker detected"
    echo ""
    read -p "Use Docker? (y/n): " use_docker
    
    if [ "$use_docker" = "y" ] || [ "$use_docker" = "Y" ]; then
        echo ""
        echo "🐳 Starting with Docker Compose..."
        docker-compose up -d
        echo ""
        echo "✓ Services started!"
        echo ""
        echo "Access the application at:"
        echo "  Frontend: http://localhost:5173"
        echo "  Backend:  http://localhost:8000"
        echo "  API Docs: http://localhost:8000/docs"
        echo ""
        echo "To stop: docker-compose down"
        exit 0
    fi
fi

# Manual setup
echo ""
echo "📦 Starting manual setup..."
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed"
    exit 1
fi

echo "✓ Python and Node.js detected"
echo ""

# Start backend
echo "🔧 Setting up backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
echo "Installing backend dependencies..."
pip install -q -r requirements.txt

echo "Starting backend server..."
python main.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 3

# Start frontend
echo ""
echo "🎨 Setting up frontend..."
cd frontend

if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi

echo "Starting frontend server..."
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✓ All services started!"
echo ""
echo "Access the application at:"
echo "  Frontend: http://localhost:5173"
echo "  Backend:  http://localhost:8000"
echo "  API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Trap Ctrl+C and cleanup
trap "echo ''; echo '🛑 Stopping services...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT

# Wait for processes
wait $BACKEND_PID $FRONTEND_PID
