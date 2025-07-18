#!/usr/bin/env python3
"""Quick test to see the full SQL for Maharashtra query"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from query_agent import english_to_sql

# Test the Maharashtra query to see full SQL
test_query = "what plants are in Maharashtra"
print(f"📋 Query: '{test_query}'")

result = english_to_sql(test_query)
sql_query = result.get('sql', '')
print(f"🔍 Generated SQL:")
print(sql_query)

# Check if it uses zone_name correctly
if 'zm.zone_name' in sql_query:
    print("✅ CORRECT: Using zm.zone_name")
elif 'zm.name' in sql_query:
    print("❌ ERROR: Using zm.name (incorrect)")
else:
    print("ℹ️  INFO: No zone column reference found")
