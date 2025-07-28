#!/usr/bin/env python3
"""Test the specific Gujarat query issue - reproduce and verify the fix"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.query_agent import english_to_sql
from src.core.sql import run_query

def test_gujarat_query():
    """Test the original failing query about plants in Gujarat"""
    print("🧪 Testing Gujarat Query Issue...")
    print("=" * 60)
    
    # Test the exact query that was failing
    test_query = "show me plants in Gujarat"
    print(f"\n📋 Query: '{test_query}'")
    
    try:
        # Generate the SQL
        result = english_to_sql(test_query)
        
        if not result or not result.get('sql'):
            print(f"❌ ERROR: No SQL generated. Result: {result}")
            return False
        
        sql_query = result.get('sql', '')
        print(f"\n🔍 Generated SQL:")
        print(sql_query)
        
        # Check if the SQL contains the correct column name
        if 'zm.zone_name' in sql_query:
            print("✅ CORRECT: Using zm.zone_name")
        elif 'zm.name' in sql_query:
            print("❌ ERROR: Still using zm.name (incorrect)")
            return False
        else:
            print("⚠️  WARNING: No zone_name reference found")
        
        # Try to execute the SQL to see if it works
        try:
            test_result = run_query(sql_query)
            print(f"✅ SQL executed successfully! Found {len(test_result)} records")
            return True
        except Exception as e:
            print(f"❌ SQL execution failed: {str(e)}")
            if "column zm.name does not exist" in str(e):
                print("🚨 CRITICAL: Still generating incorrect column name!")
            return False
            
    except Exception as e:
        print(f"❌ Process failed: {str(e)}")
        return False

def test_other_zone_queries():
    """Test other zone-related queries to ensure consistency"""
    print("\n🧪 Testing Other Zone Queries...")
    print("=" * 60)
    
    test_queries = [
        "vehicles in West Bengal",
        "what plants are in Maharashtra", 
        "show all zones"
    ]
    
    all_passed = True
    
    for query in test_queries:
        print(f"\n📋 Query: '{query}'")
        try:
            result = english_to_sql(query)
            
            if not result or not result.get('sql'):
                print(f"❌ ERROR: No SQL generated. Result: {result}")
                all_passed = False
                continue
            
            sql_query = result.get('sql', '')
            print(f"🔍 Generated SQL: {sql_query[:100]}...")
            
            # Check for correct column usage
            if 'zm.zone_name' in sql_query or 'zone_name' in sql_query:
                print("✅ CORRECT: Using zone_name")
            elif 'zm.name' in sql_query:
                print("❌ ERROR: Using zm.name (incorrect)")
                all_passed = False
            else:
                print("ℹ️  INFO: No zone column reference")
                
        except Exception as e:
            print(f"❌ Process failed: {str(e)}")
            all_passed = False
    
    return all_passed

if __name__ == "__main__":
    print("🚀 Gujarat Column Name Fix Test")
    print("=" * 60)
    
    # Test the main issue
    gujarat_test = test_gujarat_query()
    
    # Test other zone queries
    other_tests = test_other_zone_queries()
    
    print("\n" + "=" * 60)
    print("📊 FINAL RESULTS:")
    print(f"Gujarat Query Test: {'✅ PASSED' if gujarat_test else '❌ FAILED'}")
    print(f"Other Zone Tests: {'✅ PASSED' if other_tests else '❌ FAILED'}")
    
    if gujarat_test and other_tests:
        print("🎉 ALL TESTS PASSED! The column name issue is fixed.")
    else:
        print("⚠️  SOME TESTS FAILED! The issue may still exist.")
