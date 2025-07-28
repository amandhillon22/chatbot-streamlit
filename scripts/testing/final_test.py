#!/usr/bin/env python3
"""Test comprehensive plant/vehicle queries"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.query_agent import english_to_sql

def test_queries():
    print("🧪 Testing Comprehensive Plant/Vehicle Queries...")
    
    tests = [
        ("show vehicles in mohali", "Vehicles in plant"),
        ("plants in Punjab", "Plants in region"), 
        ("what plants are there", "All plants"),
        ("vehicles in PB-Ludhiana", "Vehicles in specific plant")
    ]
    
    for query, desc in tests:
        print(f"\n📋 {desc}: '{query}'")
        result = english_to_sql(query)
        sql = result.get('sql', '').lower()
        print(f"   SQL: {sql[:80]}...")
        
        if 'hosp_master' in sql:
            print("   ✅ Uses hosp_master (plant data)")
        if 'vehicle_master' in sql:
            print("   ✅ Uses vehicle_master")

if __name__ == "__main__":
    test_queries()
