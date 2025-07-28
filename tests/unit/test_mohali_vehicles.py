#!/usr/bin/env python3
"""Test the vehicles in Mohali query after fixing table interpretation"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.query_agent import english_to_sql
from src.core.sql import run_query

def test_vehicles_in_mohali():
    """Test the vehicles in Mohali query"""
    print("🧪 Testing Vehicles in Mohali Query...")
    print("=" * 60)
    
    test_query = "show vehicles in mohali"
    print(f"📋 Query: '{test_query}'")
    
    # Generate the SQL
    result = english_to_sql(test_query)
    
    if not result or not result.get('sql'):
        print(f"❌ ERROR: No SQL generated. Result: {result}")
        return False
    
    sql_query = result.get('sql', '')
    print(f"\n🔍 Generated SQL:")
    print(sql_query)
    
    # Check if it correctly uses hosp_master for plant data
    if 'hosp_master' in sql_query and 'vehicle_master' in sql_query:
        print("✅ CORRECT: Using hosp_master (plant data) and vehicle_master")
    else:
        print("❌ ISSUE: Not using expected tables")
        return False
    
    # Check if it joins correctly
    if 'JOIN' in sql_query and 'mohali' in sql_query.lower():
        print("✅ CORRECT: Using JOIN and filtering by Mohali")
    else:
        print("❌ ISSUE: Missing JOIN or Mohali filter")
        return False
    
    # Test the query execution
    try:
        vehicles = run_query(sql_query)
        print(f"\n🚛 Results: Found {len(vehicles)} vehicles in Mohali plant")
        
        # Show some vehicle registration numbers
        if vehicles and len(vehicles) > 0:
            print("📋 Vehicle registrations found:")
            for i, vehicle in enumerate(vehicles[:10]):  # Show first 10
                if isinstance(vehicle, tuple) and len(vehicle) > 0:
                    print(f"   {i+1}. {vehicle[0]}")
        
        return True
        
    except Exception as e:
        print(f"❌ SQL execution failed: {str(e)}")
        return False

def test_plant_queries():
    """Test various plant-related queries"""
    print(f"\n🧪 Testing Plant-related Queries...")
    print("=" * 40)
    
    test_queries = [
        "show plants in Punjab",
        "vehicles in PB-Ludhiana",
        "what plants are there"
    ]
    
    for query in test_queries:
        print(f"\n📋 Testing: '{query}'")
        result = english_to_sql(query)
        sql = result.get('sql', '')
        
        if 'hosp_master' in sql:
            print(f"✅ {query}: Using hosp_master (correct for plant data)")
        else:
            print(f"❌ {query}: Not using hosp_master for plant data")

if __name__ == "__main__":
    print("🚀 Testing Plant/Vehicle Query Fixes")
    print("=" * 60)
    
    # Test the main Mohali vehicles issue
    mohali_success = test_vehicles_in_mohali()
    
    # Test other plant queries
    test_plant_queries()
    
    print(f"\n🎯 SUMMARY:")
    if mohali_success:
        print("✅ Vehicles in Mohali query is working correctly!")
        print("✅ System now correctly interprets hosp_master as plant data")
    else:
        print("❌ Vehicles in Mohali query still has issues")
