#!/bin/bash

# Kill any existing processes on ports 5000 and 5050
sudo kill -9 $(sudo lsof -t -i:5000) 2>/dev/null || true
sudo kill -9 $(sudo lsof -t -i:5050) 2>/dev/null || true

# Change to project directory
cd /home/linux/Documents/chatbot-diya

# Set production environment and port
export FLASK_ENV=production
export FLASK_APP=src.api.flask_app:app
export PORT=5050
export FLASK_RUN_HOST='0.0.0.0'

# Activate virtual environment and start the Flask application
source /home/linux/Documents/chatbot-diya/.venv/bin/activate
/home/linux/Documents/chatbot-diya/.venv/bin/python -m src.api.flask_app
