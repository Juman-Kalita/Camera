#!/bin/bash

echo "Starting Workplace Activity Analytics System..."
echo ""

echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "Starting backend server..."
cd backend
python main.py &
BACKEND_PID=$!

echo ""
echo "Waiting for server to start..."
sleep 5

echo ""
echo "Starting frontend server..."
cd ../frontend
python -m http.server 3000 &
FRONTEND_PID=$!

echo ""
echo "Opening dashboard..."
if command -v xdg-open > /dev/null; then
    xdg-open http://localhost:3000/dashboard.html
elif command -v open > /dev/null; then
    open http://localhost:3000/dashboard.html
fi

echo ""
echo "System is running!"
echo "Backend: http://localhost:8000"
echo "Dashboard: http://localhost:3000/dashboard.html"
echo ""
echo "Press Ctrl+C to stop..."

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
