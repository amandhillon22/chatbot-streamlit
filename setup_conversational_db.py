#!/usr/bin/env python3
"""
Initialize Conversational AI Database Tables
This script safely creates the required database tables for conversational AI
"""

import sys
import os
sys.path.append('/home/linux/Documents/chatbot-diya')

from src.core.sql import db_manager
import psycopg2

def create_conversational_tables():
    """Create the conversation tables manually."""
    try:
        with db_manager.get_connection_context() as conn:
            cur = conn.cursor()
            
            print("🔧 Creating conversation context table...")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS conversation_context (
                    session_id VARCHAR(255) PRIMARY KEY,
                    current_topic TEXT,
                    last_vehicle VARCHAR(255),
                    last_date_context TEXT,
                    last_report_type VARCHAR(255),
                    conversation_summary TEXT,
                    active_filters JSONB DEFAULT '{}',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            print("🔧 Creating conversation history table...")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS conversation_history (
                    id SERIAL PRIMARY KEY,
                    session_id VARCHAR(255) NOT NULL,
                    user_message TEXT NOT NULL,
                    bot_response TEXT NOT NULL,
                    extracted_entities JSONB DEFAULT '{}',
                    intent_detected VARCHAR(255),
                    sql_executed TEXT,
                    result_count INTEGER DEFAULT 0,
                    conversation_turn INTEGER DEFAULT 1,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            print("🔧 Creating indexes...")
            cur.execute("CREATE INDEX IF NOT EXISTS conversation_history_session_idx ON conversation_history (session_id, timestamp);")
            cur.execute("CREATE INDEX IF NOT EXISTS conversation_context_updated_idx ON conversation_context (updated_at);")
            
            conn.commit()
            print("✅ Conversational AI database tables created successfully!")
            
            # Test the tables
            cur.execute("SELECT COUNT(*) FROM conversation_context;")
            context_count = cur.fetchone()[0]
            
            cur.execute("SELECT COUNT(*) FROM conversation_history;")
            history_count = cur.fetchone()[0]
            
            print(f"📊 Database Status:")
            print(f"  - Conversation contexts: {context_count}")
            print(f"  - Conversation history entries: {history_count}")
            
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 Initializing Conversational AI Database Tables...")
    success = create_conversational_tables()
    
    if success:
        print("\n✅ Conversational AI database setup complete!")
        print("🔄 Now the sentence embedding manager should initialize properly.")
    else:
        print("\n❌ Failed to set up conversational AI database tables.")
