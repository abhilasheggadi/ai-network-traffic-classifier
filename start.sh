#!/bin/bash

# AI Network Traffic Classifier - Quick Start Script
# Starts FastAPI backend and Streamlit dashboard

echo "🚀 Starting AI Network Traffic Classifier..."
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${RED}❌ Virtual environment not found!${NC}"
    echo "Please run: python -m venv venv"
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Check if packages are installed
if ! python -c "import streamlit" 2>/dev/null; then
    echo -e "${RED}❌ Dependencies not installed!${NC}"
    echo "Please run: pip install -r requirements.txt"
    exit 1
fi

# Create logs directory if it doesn't exist
mkdir -p logs

echo ""
echo -e "${GREEN}✅ Environment ready!${NC}"
echo ""

# Start FastAPI backend
echo -e "${BLUE}🔧 Starting FastAPI Backend (port 8000)...${NC}"
python -m uvicorn backend.main:app --reload --port 8000 > logs/backend.log 2>&1 &
BACKEND_PID=$!
sleep 2

# Check if backend started successfully
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo -e "${RED}❌ Failed to start backend!${NC}"
    cat logs/backend.log
    exit 1
fi

echo -e "${GREEN}✅ Backend running (PID: $BACKEND_PID)${NC}"
echo ""

# Start Streamlit dashboard
echo -e "${BLUE}📊 Starting Streamlit Dashboard (port 8501)...${NC}"
python -m streamlit run src/dashboard/app.py --server.port 8501 > logs/dashboard.log 2>&1 &
DASHBOARD_PID=$!
sleep 3

# Check if dashboard started successfully
if ! kill -0 $DASHBOARD_PID 2>/dev/null; then
    echo -e "${RED}❌ Failed to start dashboard!${NC}"
    cat logs/dashboard.log
    kill $BACKEND_PID
    exit 1
fi

echo -e "${GREEN}✅ Dashboard running (PID: $DASHBOARD_PID)${NC}"
echo ""

# Show access URLs
echo -e "${GREEN}═════════════════════════════════════════${NC}"
echo -e "${GREEN}🎉 Everything is running!${NC}"
echo -e "${GREEN}═════════════════════════════════════════${NC}"
echo ""
echo -e "${BLUE}📊 Dashboard:${NC}  http://localhost:8501"
echo -e "${BLUE}🔧 API:${NC}        http://127.0.0.1:8000"
echo -e "${BLUE}📚 API Docs:${NC}    http://127.0.0.1:8000/docs"
echo ""
echo -e "${GREEN}Logs:${NC}"
echo "  Backend:  logs/backend.log"
echo "  Dashboard: logs/dashboard.log"
echo ""
echo -e "${GREEN}Press Ctrl+C to stop both services${NC}"
echo ""

# Cleanup on exit
trap "echo ''; echo 'Stopping services...'; kill $BACKEND_PID $DASHBOARD_PID 2>/dev/null; echo 'Done!'; exit" INT TERM

# Wait for both processes
wait $BACKEND_PID $DASHBOARD_PID
