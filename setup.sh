#!/bin/bash

# Setup script for AI Agent Recommender

echo "🤖 AI Agent Recommender Setup"
echo "=============================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Check if .env exists
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your OPENAI_API_KEY"
else
    echo ".env file already exists"
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Run setup
echo ""
echo "Running data setup..."
python -m src.cli.main setup

echo ""
echo "✅ Setup complete!"
echo ""
echo "To use the CLI:"
echo "  python -m src.cli.main interactive"
echo ""
echo "To start the web UI:"
echo "  streamlit run web/app.py"
echo ""
echo "To start the API server:"
echo "  uvicorn src.api.main:app --reload"

