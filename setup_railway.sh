#!/bin/bash

# Railway Deployment Setup Script

echo "🚂 Railway Deployment Setup"
echo "============================"
echo ""

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Installing..."
    npm install -g @railway/cli
fi

echo "✅ Railway CLI installed"
echo ""

# Check if logged in
if railway whoami &> /dev/null; then
    echo "✅ Already logged in to Railway"
    railway whoami
else
    echo "⚠️  Not logged in to Railway"
    echo "Please run: railway login"
    echo "This will open your browser to authenticate."
    exit 1
fi

echo ""
echo "📦 Setting up Railway project..."
echo ""

# Initialize if not already done
if [ ! -f ".railway/config.json" ]; then
    echo "Initializing Railway project..."
    railway init
else
    echo "✅ Railway project already initialized"
fi

echo ""
echo "🔐 Setting environment variables..."
echo ""

# Check if OPENAI_API_KEY is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  OPENAI_API_KEY not set in environment"
    read -p "Enter your OpenAI API key: " api_key
    railway variables set OPENAI_API_KEY="$api_key"
else
    echo "Setting OPENAI_API_KEY from environment..."
    railway variables set OPENAI_API_KEY="$OPENAI_API_KEY"
fi

# Set other variables
railway variables set OPENAI_MODEL="${OPENAI_MODEL:-gpt-4-turbo-preview}"
railway variables set CHROMA_PERSIST_DIR="/tmp/embeddings"

echo ""
echo "✅ Environment variables set"
echo ""
echo "📤 Ready to deploy!"
echo ""
echo "Run the following to deploy:"
echo "  railway up"
echo ""
echo "Or deploy from GitHub:"
echo "  1. Go to Railway dashboard"
echo "  2. Connect your GitHub repo"
echo "  3. Railway will auto-deploy on push"
echo ""

