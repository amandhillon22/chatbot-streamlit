#!/usr/bin/env python3
"""
Test script to validate the improved query agent column validation
"""

import sys
import os
sys.path.append('/home/linux/Documents/chatbot-diya')

from src.core.query_agent import english_to_sql, ChatContext

def test_query(query_text, description):
    print(f"\n🧪 Testing: {description}")
    print(f"Query: '{query_text}'")
    print("=" * 50)
    
    result = english_to_sql(query_text, ChatContext())
    
    if result.get('sql'):
        print(f"✅ SQL Generated: {result['sql']}")
    else:
        print(f"⚠️  No SQL: {result.get('response', 'No response')}")
    
    return result

if __name__ == "__main__":
    # Test cases that should work
    test_query("How many vehicles are there?", "Simple vehicle count")
    
    # Test cases that should fail gracefully (no veh_type column)
    test_query("Show me vehicles by category", "Vehicle categorization (should fail gracefully)")
    
    # Test cases that should work with available columns
    test_query("Show me vehicles grouped by manufacturer", "Vehicle by manufacturer")
    
    print("\n" + "=" * 70)
    print("✅ All tests completed!")
