#!/bin/bash

# Script to help take screenshots of the application

echo "📸 Screenshot Helper Script"
echo "============================"
echo ""
echo "This script will help you take screenshots of the application."
echo ""

# Check if API is running
API_URL="${API_URL:-http://localhost:8000}"
echo "Checking if API is running at $API_URL..."

if curl -s "$API_URL/health" > /dev/null 2>&1; then
    echo "✅ API is running!"
else
    echo "⚠️  API is not running. Please start it first:"
    echo "   uvicorn src.api.main:app --reload"
    echo ""
    read -p "Press Enter when API is running, or Ctrl+C to exit..."
fi

# Check if Streamlit is running
STREAMLIT_URL="${STREAMLIT_URL:-http://localhost:8501}"
echo "Checking if Streamlit is running at $STREAMLIT_URL..."

if curl -s "$STREAMLIT_URL" > /dev/null 2>&1; then
    echo "✅ Streamlit is running!"
else
    echo "⚠️  Streamlit is not running. Please start it first:"
    echo "   streamlit run web/app.py"
    echo ""
    read -p "Press Enter when Streamlit is running, or Ctrl+C to exit..."
fi

echo ""
echo "📸 Ready to take screenshots!"
echo ""
echo "Please take screenshots of:"
echo "1. Web UI - Main interface: $STREAMLIT_URL"
echo "2. Web UI - Search results (after searching)"
echo "3. Web UI - Conversation mode"
echo "4. API Docs: $API_URL/docs"
echo ""
echo "Save screenshots to: docs/images/"
echo ""
echo "Suggested filenames:"
echo "  - docs/images/web-ui-main.png"
echo "  - docs/images/web-ui-search.png"
echo "  - docs/images/web-ui-conversation.png"
echo "  - docs/images/api-docs.png"
echo ""

# Open browsers
echo "Opening browsers..."
open "$STREAMLIT_URL" 2>/dev/null || xdg-open "$STREAMLIT_URL" 2>/dev/null || echo "Please open $STREAMLIT_URL manually"
open "$API_URL/docs" 2>/dev/null || xdg-open "$API_URL/docs" 2>/dev/null || echo "Please open $API_URL/docs manually"

echo ""
echo "After taking screenshots, update README.md with the image references!"

