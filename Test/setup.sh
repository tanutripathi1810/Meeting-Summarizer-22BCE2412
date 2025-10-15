#!/bin/bash

# Meeting Summarizer Setup Script
# This script sets up everything needed to run the application

set -e  # Exit on error

echo "=========================================="
echo "  Meeting Summarizer - Setup Script"
echo "=========================================="
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# Check Python version
echo "Checking prerequisites..."
echo ""

if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
print_success "Python $PYTHON_VERSION found"

# All dependencies are via pip, no external tools needed
print_success "No external dependencies required (FFmpeg not needed)"

# Check for OpenAI API Key
print_info "Checking for OpenAI API key..."
if [ -f ".env" ] && grep -q "OPENAI_API_KEY=" .env && ! grep -q "OPENAI_API_KEY=your" .env; then
    print_success "OpenAI API key found in .env"
else
    print_warning "OpenAI API key not configured"
    echo "  You'll need an OpenAI API key to use this application"
    echo "  Get one at: https://platform.openai.com/api-keys"
    echo "  Add it to .env file after setup"
fi

echo ""
echo "=========================================="
echo "  Setting up Python environment"
echo "=========================================="
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    print_info "Creating virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_info "Virtual environment already exists"
fi

# Activate virtual environment
print_info "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
print_info "Upgrading pip..."
pip install --upgrade pip --quiet

# Install/upgrade dependencies
print_info "Installing dependencies..."
pip install --upgrade -r requirements.txt

print_success "All Python packages installed"

echo ""
echo "=========================================="
echo "  Configuration"
echo "=========================================="
echo ""

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    print_info "Creating .env configuration file..."
    cat > .env << 'EOF'
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini

# Whisper Language Configuration
SPEECH_RECOGNITION_LANGUAGE=en
EOF
    print_success ".env file created"
    print_warning "IMPORTANT: Add your OpenAI API key to the .env file!"
else
    print_info ".env file already exists"
fi

# Create necessary directories
print_info "Creating data directories..."
mkdir -p uploads transcripts summaries
print_success "Directories created"

echo ""
echo "=========================================="
echo "  Setup Complete!"
echo "=========================================="
echo ""
print_success "Everything is set up and ready to go!"
echo ""
echo "⚠️  IMPORTANT: Add your OpenAI API key to .env file:"
echo "     Edit .env and replace 'your_openai_api_key_here' with your actual key"
echo "     Get API key from: ${BLUE}https://platform.openai.com/api-keys${NC}"
echo ""
echo "To start the application:"
echo ""
echo "  1. Add OpenAI API key to .env file (required!)"
echo "  2. Run: ${GREEN}./run.sh${NC}"
echo "     Or:  ${GREEN}source venv/bin/activate && python app.py${NC}"
echo ""
echo "  3. Open browser to: ${BLUE}http://localhost:5000${NC}"
echo ""
print_warning "NOTE: If port 5000 is in use (AirPlay Receiver on macOS),"
echo "      you can disable it in System Settings -> General -> AirDrop & Handoff"
echo ""

