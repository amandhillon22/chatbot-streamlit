#!/bin/bash

# Kill any existing processes on ports 5000 and 5050
sudo kill -9 $(sudo lsof -t -i:5000) 2>/dev/null || true
sudo kill -9 $(sudo lsof -t -i:5050) 2>/dev/null || true

# Set production environment and port
export FLASK_ENV=production
export FLASK_APP=flask_app.py
export PORT=5050
export FLASK_RUN_HOST='0.0.0.0'

# Start the Flask application
python3 flask_app.py
