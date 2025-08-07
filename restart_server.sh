#!/bin/bash

echo "🔄 Restarting Diya Chatbot Server..."
echo "======================================="

# Set the project directory
PROJECT_DIR="/home/linux/Documents/chatbot-diya"
cd "$PROJECT_DIR" || exit 1

# Kill existing Python processes related to the chatbot
echo "🛑 Stopping existing chatbot processes..."
pkill -f "flask_app.py"
pkill -f "start_chatbot.py" 
pkill -f "gunicorn.*flask_app"
sleep 2

# Check if ports are still in use and force kill if necessary
for port in 5000 5050; do
    if lsof -i :$port > /dev/null 2>&1; then
        echo "⚠️ Port $port still in use, forcing kill..."
        sudo fuser -k $port/tcp 2>/dev/null
        sleep 1
    fi
done

# Set Python path
export PYTHONPATH="$PROJECT_DIR:$PYTHONPATH"

echo "🚀 Starting Diya Chatbot Server..."

# Check if we should use production or development mode
if [ "$1" = "production" ] || [ "$1" = "prod" ]; then
    echo "🏭 Starting in PRODUCTION mode..."
    
    # Activate virtual environment if it exists
    if [ -f "$PROJECT_DIR/.venv/bin/activate" ]; then
        source "$PROJECT_DIR/.venv/bin/activate"
        echo "✅ Virtual environment activated"
    fi
    
    # Start with Gunicorn for production
    if command -v gunicorn &> /dev/null; then
        gunicorn --bind 0.0.0.0:5050 --workers 2 --timeout 120 src.api.flask_app:app
    else
        echo "⚠️ Gunicorn not found, falling back to development mode"
        python src/api/flask_app.py
    fi
    
else
    echo "🔧 Starting in DEVELOPMENT mode..."
    
    # Use the startup script for development
    if [ -f "$PROJECT_DIR/scripts/start_chatbot.py" ]; then
        python scripts/start_chatbot.py
    else
        # Fallback to direct Flask app
        python src/api/flask_app.py
    fi
fi

echo "✅ Server startup complete!"
