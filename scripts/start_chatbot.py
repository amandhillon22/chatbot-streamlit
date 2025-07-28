#!/usr/bin/env python3
"""
sys.path.append('/home/linux/Documents/chatbot-diya')

Startup script for Diya Chatbot
"""

import subprocess
import sys
import os
from database.setup_database import setup_database

def main():
    print("🤖 Diya Chatbot Startup")
    print("=" * 30)
    
    # Check if database setup is needed
    print("🔧 Setting up database...")
    if setup_database():
        print("✅ Database ready")
    else:
        print("❌ Database setup failed")
        sys.exit(1)
    
    # Start the Flask application
    print("🚀 Starting Flask application...")
    try:
        # Import and run the Flask app directly
        from src.api.flask_app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Shutting down gracefully...")
    except Exception as e:
        print(f"❌ Error starting application: {e}")

if __name__ == '__main__':
    main()
