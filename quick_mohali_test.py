#!/usr/bin/env python3
"""Quick test for Mohali vehicles SQL generation"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from query_agent import english_to_sql

def quick_test():
    print("🔍 Testing Mohali Vehicles SQL Generation...")
    
    test_query = "show vehicles in mohali"
    print(f"📋 Query: '{test_query}'")
    
    result = english_to_sql(test_query)
    sql_query = result.get('sql', '')
    
    print(f"\n🔍 Generated SQL:")
    print(sql_query)
    
    # Quick analysis
    if 'hosp_master' in sql_query and 'vehicle_master' in sql_query:
        print("✅ Uses hosp_master and vehicle_master")
    if 'mohali' in sql_query.lower():
        print("✅ Filters by Mohali")
    if 'JOIN' in sql_query:
        print("✅ Uses JOIN")

if __name__ == "__main__":
    quick_test()
