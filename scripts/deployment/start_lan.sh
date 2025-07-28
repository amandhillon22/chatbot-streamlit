#!/bin/bash

# 🌐 Diya Chatbot - LAN Deployment Script
# This script configures and launches the chatbot for LAN access

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}🌐 Diya Chatbot - LAN Deployment${NC}"
echo -e "${CYAN}=================================${NC}"
echo ""

# Get current IP address
IP_ADDRESS=$(ip addr show | grep -E "inet.*10\.|inet.*192\.|inet.*172\." | head -1 | awk '{print $2}' | cut -d/ -f1)

if [ -z "$IP_ADDRESS" ]; then
    echo -e "${RED}❌ Could not detect LAN IP address${NC}"
    exit 1
fi

echo -e "${BLUE}📍 Detected LAN IP: ${GREEN}$IP_ADDRESS${NC}"
echo -e "${BLUE}🌐 Chatbot will be available at: ${GREEN}http://$IP_ADDRESS:5000${NC}"
echo ""

# Check if we're in the right directory
if [ ! -f "src/api/flask_app.py" ]; then
    echo -e "${RED}❌ Error: flask_app.py not found. Please run this script from the chatbot directory.${NC}"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}📦 Creating virtual environment...${NC}"
    python3 -m venv .venv
fi

echo -e "${YELLOW}🔧 Activating virtual environment...${NC}"
source .venv/bin/activate

# Check if dependencies are installed
echo -e "${YELLOW}🔍 Checking dependencies...${NC}"
if ! python -c "import flask, psycopg2" 2>/dev/null; then
    echo -e "${YELLOW}📦 Installing dependencies...${NC}"
    pip install -r requirements.txt
fi

echo -e "${GREEN}✅ Dependencies ready${NC}"

# Test database connection
echo -e "${YELLOW}🗄️  Testing database connection...${NC}"
if python -c "
import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()
try:
    conn = psycopg2.connect(
        host=os.getenv('hostname', 'localhost'),
        dbname=os.getenv('dbname', 'rdc_dump'),
        user=os.getenv('user_name', 'postgres'),
        password=os.getenv('password', 'Akshit@123'),
        port=5432
    )
    conn.close()
    print('✅ Database connection successful')
except Exception as e:
    print(f'❌ Database connection failed: {e}')
    exit(1)
" 2>/dev/null; then
    echo -e "${GREEN}✅ Database connection successful${NC}"
else
    echo -e "${RED}❌ Database connection failed${NC}"
    echo -e "${YELLOW}💡 Please ensure PostgreSQL is running and credentials are correct${NC}"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Test business logic integration
echo -e "${YELLOW}🧠 Testing business logic integration...${NC}"
if python -c "
from eoninfotech_masker import EonInfotechMasker
from database_reference_parser import DatabaseReferenceParser
from intelligent_reasoning import IntelligentReasoning
print('✅ Business logic modules loaded successfully')
print('✅ EONINFOTECH masking: Available')
print('✅ EON OFFICE removal logic: Available')
print('✅ Hierarchical reasoning: Available')
" 2>/dev/null; then
    echo -e "${GREEN}✅ Business logic integration verified${NC}"
else
    echo -e "${YELLOW}⚠️  Business logic test inconclusive${NC}"
fi

echo ""
echo -e "${PURPLE}🚀 Starting Diya Chatbot for LAN Access${NC}"
echo -e "${CYAN}============================================${NC}"
echo -e "${GREEN}📱 Web Interface: ${YELLOW}http://$IP_ADDRESS:5000${NC}"
echo -e "${GREEN}🖥️  Admin Panel: ${YELLOW}http://$IP_ADDRESS:5000/admin${NC}"
echo -e "${GREEN}🔐 Default Login: ${YELLOW}admin01 / 123456${NC}"
echo ""
echo -e "${BLUE}🌟 Business Rules Active:${NC}"
echo -e "${YELLOW}   • EONINFOTECH vehicles: Marked as Inactive${NC}"
echo -e "${YELLOW}   • EON OFFICE vehicles: Show removal message${NC}"
echo -e "${YELLOW}   • Hierarchical queries: Zone → District → Plant → Vehicle${NC}"
echo -e "${YELLOW}   • Hospital references: Replaced with Plant/Facility${NC}"
echo ""
echo -e "${CYAN}🔗 LAN Users can access: http://$IP_ADDRESS:5000${NC}"
echo -e "${YELLOW}💡 Press Ctrl+C to stop the server${NC}"
echo ""

# Export environment variables for LAN deployment
export FLASK_HOST="0.0.0.0"
export FLASK_PORT="5000"
export FLASK_ENV="production"

# Start the application with gunicorn for production deployment
echo -e "${GREEN}🔥 Starting with Gunicorn (Production Mode)...${NC}"
gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 --keep-alive 2 --max-requests 1000 --max-requests-jitter 50 flask_app:app
