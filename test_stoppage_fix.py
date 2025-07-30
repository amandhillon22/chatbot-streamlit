#!/usr/bin/env python3
"""
Test the stoppage_report fix
"""

import sys
import os
sys.path.append('/home/linux/Documents/chatbot-diya')

# Load environment
from dotenv import load_dotenv
load_dotenv()

# Test the query generation
try:
    from src.core.query_agent import english_to_sql
    
    # Test the problematic query
    test_query = "give me stoppage report of some vehicles on date 2 july 2025"
    
    print(f"🧪 Testing query: {test_query}")
    result = english_to_sql(test_query)
    
    print(f"📄 Result: {result}")
    
    if result and 'sql' in result:
        sql = result['sql']
        print(f"🔍 Generated SQL:")
        print(sql)
        
        # Check if it contains the wrong table name
        if 'stoppage_report' in sql.lower():
            print("❌ STILL USING stoppage_report!")
        elif 'util_report' in sql.lower():
            print("✅ Correctly using util_report!")
        else:
            print("⚠️ No stoppage table referenced")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
