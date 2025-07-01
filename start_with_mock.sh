#!/bin/bash

# CrowdGuard Startup Script with Mock Data Generator (uses uv)

echo "🛡️  CrowdGuard - Starting with Mock Data Generator"
echo "=================================================="
echo ""

# Ensure uv is installed
if ! command -v uv &>/dev/null; then
    echo "❌ uv is not installed!"
    echo ""
    echo "Install uv first:"
    echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo "  or: brew install uv"
    exit 1
fi

# Create venv and install dependencies with uv (idempotent)
echo "📦 Syncing environment with uv..."
uv sync --no-dev
echo ""

# Check if MongoDB is running
echo "Checking MongoDB connection..."
if ! uv run python -c "from pymongo import MongoClient; client = MongoClient('mongodb://localhost:27017', serverSelectionTimeoutMS=2000); client.server_info()" 2>/dev/null; then
    echo "❌ MongoDB is not running!"
    echo ""
    echo "Please start MongoDB first:"
    echo "  macOS: brew services start mongodb-community"
    echo "  Linux: sudo systemctl start mongodb"
    echo "  Or use MongoDB Atlas and set MONGO_URL environment variable"
    exit 1
fi

echo "✅ MongoDB is running"
echo ""

# Check if database is seeded
echo "Checking if database is seeded..."
uv run python -c "from pymongo import MongoClient; client = MongoClient('mongodb://localhost:27017'); db = client['crowdguard_db']; count = db.users.count_documents({}); exit(0 if count > 0 else 1)" 2>/dev/null

if [ $? -ne 0 ]; then
    echo "Database not seeded. Seeding now..."
    uv run python -m backend.seed_data
    echo ""
fi

echo "✅ Database is ready"
echo ""

# Start mock data generator in background
echo "🎲 Starting mock data generator..."
uv run python -m backend.mock_data &
MOCK_PID=$!

# Start the FastAPI server
echo "🚀 Starting FastAPI server..."
echo "   API: http://localhost:8000"
echo "   Dashboard: http://localhost:8000/index.html"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Trap Ctrl+C and kill both processes
trap "echo ''; echo 'Stopping services...'; kill $MOCK_PID 2>/dev/null; exit" INT

uv run uvicorn backend.main:app --reload

