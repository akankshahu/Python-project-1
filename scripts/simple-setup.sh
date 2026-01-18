#!/bin/bash

# Simple setup script - No Docker needed!

echo "=========================================="
echo "DataMAx Simple Setup (No Docker)"
echo "=========================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required"
    exit 1
fi

echo "✅ Python found"

# Setup backend
echo ""
echo "Setting up backend..."
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -q fastapi uvicorn sqlalchemy pydantic pydantic-settings python-dotenv

# Create .env file with SQLite
cat > .env << EOF
DATABASE_URL=sqlite:///./datamax.db
SECRET_KEY=dev-secret-key
ENVIRONMENT=development
LOG_LEVEL=INFO
API_V1_PREFIX=/api/v1
PROJECT_NAME=DataMAx
EOF

echo "✅ Backend setup complete"
echo ""
echo "=========================================="
echo "Ready to run!"
echo "=========================================="
echo ""
echo "To start the backend:"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  uvicorn app.main:app --reload"
echo ""
echo "Then open: http://localhost:8000/docs"
echo ""
