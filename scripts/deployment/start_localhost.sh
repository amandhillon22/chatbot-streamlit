#!/bin/bash

# 🚀 Diya Chatbot Localhost Startup Script
# This script handles everything needed to start the application on localhost

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}🤖 Diya Chatbot - Localhost Startup${NC}"
echo -e "${CYAN}====================================${NC}"

# Check if we're in the right directory
if [ ! -f "src/api/flask_app.py" ]; then
    echo -e "${RED}❌ Error: flask_app.py not found. Please run this script from the chatbot directory.${NC}"
    exit 1
fi

# Function to check if PostgreSQL is running
check_postgres() {
    echo -e "${YELLOW}🔍 Checking PostgreSQL connection...${NC}"
    if pg_isready -h localhost -p 5432 >/dev/null 2>&1; then
        echo -e "${GREEN}✅ PostgreSQL is running${NC}"
        return 0
    else
        echo -e "${RED}❌ PostgreSQL is not running or not accessible${NC}"
        echo -e "${YELLOW}💡 Please start PostgreSQL service first:${NC}"
        echo -e "   sudo systemctl start postgresql"
        echo -e "   or"
        echo -e "   sudo service postgresql start"
        return 1
    fi
}

# Function to set up virtual environment
setup_venv() {
    if [ ! -d "venv" ]; then
        echo -e "${YELLOW}🏗️  Creating virtual environment...${NC}"
        python3 -m venv venv
    fi
    
    echo -e "${YELLOW}🔧 Activating virtual environment...${NC}"
    source venv/bin/activate
    
    echo -e "${YELLOW}📦 Installing/updating dependencies...${NC}"
    pip install --upgrade pip
    pip install -r requirements.txt
    
    echo -e "${GREEN}✅ Virtual environment ready${NC}"
}

# Function to set up environment variables
setup_env() {
    echo -e "${YELLOW}🔧 Setting up environment variables...${NC}"
    
    # Set default database configuration for localhost
    export hostname="${hostname:-localhost}"
    export dbname="${dbname:-rdc_dump}"
    export user_name="${user_name:-postgres}"
    export password="${password:-Akshit@123}"
    
    # Set Flask configuration
    export FLASK_ENV="${FLASK_ENV:-development}"
    export SECRET_KEY="${SECRET_KEY:-dev-secret-key-change-in-production}"
    
    # Set Gemini API key (user needs to provide this)
    if [ -z "$GOOGLE_API_KEY" ]; then
        echo -e "${YELLOW}⚠️  GOOGLE_API_KEY not set. Some AI features may not work.${NC}"
        echo -e "${BLUE}💡 To set it: export GOOGLE_API_KEY='your-api-key'${NC}"
    fi
    
    echo -e "${GREEN}✅ Environment variables configured${NC}"
}

# Function to test database connection
test_db_connection() {
    echo -e "${YELLOW}🔍 Testing database connection...${NC}"
    python3 -c "
import os
import psycopg2
try:
    conn = psycopg2.connect(
        host=os.getenv('hostname', 'localhost'),
        dbname=os.getenv('dbname', 'rdc_dump'),
        user=os.getenv('user_name', 'postgres'),
        password=os.getenv('password', 'Akshit@123'),
        port=5432
    )
    cursor = conn.cursor()
    cursor.execute('SELECT version();')
    version = cursor.fetchone()
    print(f'✅ Database connection successful: {version[0][:50]}...')
    cursor.close()
    conn.close()
except Exception as e:
    print(f'❌ Database connection failed: {e}')
    exit(1)
    "
}

# Function to start the application
start_app() {
    echo -e "${PURPLE}🚀 Starting Diya Chatbot Application...${NC}"
    echo -e "${BLUE}📱 Application will be available at:${NC}"
    echo -e "${CYAN}   🌐 Flask App: http://localhost:5000${NC}"
    echo -e "${CYAN}   🎨 Streamlit UI: http://localhost:8501 (if running)${NC}"
    echo -e "${BLUE}🔐 Default admin login: admin01 / 123456${NC}"
    echo -e "${YELLOW}💡 Press Ctrl+C to stop the server${NC}"
    echo -e "${CYAN}========================================${NC}"
    echo ""
    
    # Change to project directory
    cd /home/linux/Documents/chatbot-diya
    
    # Option to run Flask directly or use the startup script
    if [ "$1" == "--flask-direct" ]; then
        echo -e "${YELLOW}🔧 Starting Flask directly...${NC}"
        /home/linux/Documents/chatbot-diya/.venv/bin/python -m src.api.flask_app
    elif [ "$1" == "--streamlit" ]; then
        echo -e "${YELLOW}🎨 Starting Streamlit UI...${NC}"
        /home/linux/Documents/chatbot-diya/.venv/bin/streamlit run src/api/app.py --server.port 8501
    else
        echo -e "${YELLOW}🔧 Using startup script...${NC}"
        /home/linux/Documents/chatbot-diya/.venv/bin/python scripts/start_chatbot.py
    fi
}

# Main execution flow
main() {
    echo -e "${BLUE}🔄 Starting localhost deployment sequence...${NC}"
    
    # Step 1: Check PostgreSQL
    if ! check_postgres; then
        exit 1
    fi
    
    # Step 2: Setup virtual environment
    setup_venv
    
    # Step 3: Setup environment
    setup_env
    
    # Step 4: Test database connection
    test_db_connection
    
    # Step 5: Start the application
    start_app "$1"
}

# Handle script arguments
case "$1" in
    --help|-h)
        echo -e "${CYAN}🤖 Diya Chatbot Startup Help${NC}"
        echo -e "${CYAN}=============================${NC}"
        echo "Usage: $0 [option]"
        echo ""
        echo "Options:"
        echo "  (no args)        Start with Python startup script (recommended)"
        echo "  --flask-direct   Start Flask application directly"
        echo "  --streamlit      Start Streamlit UI instead"
        echo "  --help, -h       Show this help message"
        echo ""
        echo "Environment Variables (optional):"
        echo "  hostname         Database host (default: localhost)"
        echo "  dbname           Database name (default: rdc_dump)"
        echo "  user_name        Database user (default: postgres)"
        echo "  password         Database password (default: Akshit@123)"
        echo "  GOOGLE_API_KEY   Gemini API key for AI features"
        echo ""
        echo "Examples:"
        echo "  $0                           # Start with default settings"
        echo "  $0 --flask-direct           # Start Flask directly"
        echo "  GOOGLE_API_KEY=xyz $0        # Start with Gemini API key"
        exit 0
        ;;
    *)
        main "$1"
        ;;
esac
