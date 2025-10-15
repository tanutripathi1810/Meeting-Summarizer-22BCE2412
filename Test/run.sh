#!/bin/bash

# Meeting Summarizer - Run Script
# Quick script to start the application

set -e

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_error "Virtual environment not found!"
    echo "Please run ./setup.sh first"
    exit 1
fi

# Check if port 5000 is available
if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    print_warning "Port 5000 is already in use!"
    echo ""
    echo "On macOS, this is often AirPlay Receiver."
    echo "To disable it:"
    echo "  System Settings → General → AirDrop & Handoff"
    echo "  → Turn off 'AirPlay Receiver'"
    echo ""
    echo "Alternatively, you can modify app.py to use a different port."
    echo ""
    read -p "Try to run anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check if OpenAI API key is configured
if [ ! -f ".env" ] || ! grep -q "OPENAI_API_KEY=" .env || grep -q "OPENAI_API_KEY=your" .env; then
    print_error "OpenAI API key not configured!"
    echo ""
    echo "Please add your OpenAI API key to .env file:"
    echo "  1. Edit .env file"
    echo "  2. Replace 'your_openai_api_key_here' with your actual API key"
    echo "  3. Get API key from: https://platform.openai.com/api-keys"
    echo ""
    exit 1
fi

echo ""
echo "=========================================="
echo "  Starting Meeting Summarizer"
echo "=========================================="
echo ""
print_info "Activating virtual environment..."
source venv/bin/activate

print_info "Starting Flask server..."
echo ""
echo "Once started, open your browser to:"
echo -e "${BLUE}http://localhost:5000${NC}"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the app
python app.py

