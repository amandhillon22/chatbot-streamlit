#!/bin/bash

echo "🔄 Restarting Chatbot Server..."

# Kill existing Gunicorn processes
echo "🛑 Stopping existing server..."
pkill -f gunicorn
sleep 2

# Check if port is still in use
if lsof -i :5000 > /dev/null 2>&1; then
    echo "⚠️ Port 5000 still in use, forcing kill..."
    sudo fuser -k 5000/tcp
    sleep 2
fi

# Start the server
echo "🚀 Starting server..."
if [ -f "start_production.sh" ]; then
    ./start_production.sh
else
    gunicorn --bind 0.0.0.0:5000 app:app
fi

echo "✅ Server restart complete!"
