#!/bin/bash

# Quick restart script for localhost Flask app
# This kills any existing Flask processes and starts fresh

echo "🔄 Restarting Diya Chatbot..."

# Kill any existing Flask processes
echo "🛑 Stopping existing Flask processes..."
pkill -f "flask_app.py" 2>/dev/null || echo "No existing Flask processes found"
pkill -f "simple_flask_launcher.py" 2>/dev/null || echo "No existing launcher processes found"

# Wait a moment
sleep 2

echo "🚀 Starting optimized Flask application..."

# Activate virtual environment and start app
cd /home/linux/Documents/chatbot-diya
source venv/bin/activate

# Set environment variables
export hostname="localhost"
export dbname="rdc_dump"
export user_name="postgres"  
export password="Akshit@123"
export FLASK_ENV="development"

# Start the application
python3 simple_flask_launcher.py
