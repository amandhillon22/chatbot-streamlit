#!/usr/bin/env python3
"""
Database setup script for Diya Chatbot
This script creates the necessary tables and default user
"""

import psycopg2
import hashlib
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host=os.getenv("hostname", "localhost"),
        dbname=os.getenv("dbname", "rdc_dump"),
        user=os.getenv("user_name", "postgres"),
        password=os.getenv("password", "Akshit@123"),
        port=5432
    )

def setup_database():
    """Create tables and default user"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        print("🔧 Setting up database tables...")
        
        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            );
        """)
        
        # Create chat sessions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_sessions (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                session_id VARCHAR(100) UNIQUE NOT NULL,
                title VARCHAR(200),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Create chat messages table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_messages (
                id SERIAL PRIMARY KEY,
                session_id INTEGER REFERENCES chat_sessions(id) ON DELETE CASCADE,
                message_type VARCHAR(20) NOT NULL,
                content TEXT NOT NULL,
                sql_query TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_chat_sessions_user_id ON chat_sessions(user_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_chat_messages_session_id ON chat_messages(session_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_chat_sessions_created_at ON chat_sessions(created_at DESC);")
        
        # Create default admin user
        password_hash = hashlib.md5('123456'.encode()).hexdigest()
        cursor.execute("""
            INSERT INTO users (username, password_hash) 
            VALUES (%s, %s)
            ON CONFLICT (username) DO NOTHING
        """, ('admin01', password_hash))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("✅ Database setup completed successfully!")
        print("👤 Default user created:")
        print("   Username: admin01")
        print("   Password: 123456")
        print()
        print("🚀 You can now start the application:")
        print("   python flask_app.py")
        
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False
    
    return True

if __name__ == '__main__':
    print("🔧 Diya Chatbot Database Setup")
    print("=" * 40)
    
    success = setup_database()
    
    if success:
        print("\n🎉 Setup completed! Your chatbot is ready to use.")
    else:
        print("\n❌ Setup failed. Please check your database configuration.")
