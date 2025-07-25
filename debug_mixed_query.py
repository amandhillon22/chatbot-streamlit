#!/usr/bin/env python3
"""Debug mixed query issue"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath('.'))

from query_agent import english_to_sql

# Test the specific mixed query that's failing
query = "show open complaints with product correction done"
print(f"Testing query: '{query}'")

try:
    result = english_to_sql(query)
    print(f"Result: {result}")
    
    if result:
        print("✅ SQL generated successfully")
        if "'Y'" in result:
            print("✅ Contains correct Y/N values")
        else:
            print("❌ Missing Y/N values")
    else:
        print("❌ No SQL generated")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
