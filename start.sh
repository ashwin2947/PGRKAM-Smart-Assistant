#!/bin/bash

echo "Starting PGRKAM Bot..."

# Start Backend
echo "Starting Backend Server..."
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# Wait for backend to start
sleep 5

# Start Frontend
echo "Starting Frontend..."
cd ../chatbot-ui/web
npm run dev &
FRONTEND_PID=$!

echo "Both servers are running..."
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:5173"
echo "Press Ctrl+C to stop both servers"

# Wait for user interrupt
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait