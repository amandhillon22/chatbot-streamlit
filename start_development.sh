#!/bin/bash

# Kill any existing processes on development port
sudo kill -9 $(sudo lsof -t -i:5000) 2>/dev/null || true

# Set development environment
export FLASK_ENV=development
export FLASK_APP=flask_app.py

# Start the Flask application
python3 flask_app.py
