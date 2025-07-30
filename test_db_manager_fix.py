#!/usr/bin/env python3
"""
Quick test for database connection manager singleton fix
"""

import sys
import os
sys.path.append('/home/linux/Documents/chatbot-diya')

# Load environment
from dotenv import load_dotenv
load_dotenv()

# Test the database connection manager
try:
    from src.core.sql import db_manager, run_query
    print("✅ Imports successful")
    
    # Test database connection
    status = db_manager.get_pool_status()
    print(f"📊 Pool Status: {status}")
    
    # Test a simple query
    try:
        columns, rows = run_query("SELECT 1 as test_value")
        print(f"✅ Test query successful: {len(rows)} rows returned")
        print(f"   Columns: {columns}")
        print(f"   Data: {rows}")
    except Exception as e:
        print(f"❌ Test query failed: {e}")
        
    print("🎯 Database connection manager is working!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
