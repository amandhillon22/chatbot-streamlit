#!/bin/bash
# Chatbot Startup Script
# This script activates the virtual environment and starts the Flask application

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🤖 Eon Intelisense Chatbot${NC}"
echo -e "${BLUE}================================${NC}"

# Check if we're in the right directory
if [ ! -f "src/api/flask_app.py" ]; then
    echo -e "${RED}❌ Error: flask_app.py not found. Please run this script from the chatbot directory.${NC}"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo -e "${RED}❌ Error: Virtual environment not found. Please create .venv first.${NC}"
    exit 1
fi

echo -e "${YELLOW}🔧 Activating virtual environment...${NC}"

# Activate virtual environment
source .venv/bin/activate

echo -e "${GREEN}✅ Virtual environment activated${NC}"

# Check if dependencies are installed
echo -e "${YELLOW}🔍 Checking dependencies...${NC}"
if ! python -c "import flask" 2>/dev/null; then
    echo -e "${YELLOW}📦 Installing dependencies...${NC}"
    pip install -r requirements.txt
fi

echo -e "${GREEN}✅ Dependencies ready${NC}"

# Start the application
echo -e "${YELLOW}🚀 Starting Flask application...${NC}"
echo -e "${BLUE}📱 Application will be available at: http://localhost:5000${NC}"
echo -e "${BLUE}🔐 Default login: admin01 / 123456${NC}"
echo -e "${YELLOW}💡 Press Ctrl+C to stop the server${NC}"
echo ""

# Run the startup script
python scripts/start_chatbot.py
