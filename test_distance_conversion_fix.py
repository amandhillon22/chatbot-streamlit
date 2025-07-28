#!/usr/bin/env python3
"""
Test script to validate distance report conversion fixes
"""

import sys
import os
sys.path.append('/home/linux/Documents/chatbot-diya')

from src.core.query_agent import english_to_sql, ChatContext

def test_distance_conversion():
    """Test if distance conversion formulas are being applied"""
    
    print("🧪 Testing Distance Report Conversion Fixes")
    print("=" * 50)
    
    # Initialize chat context
    chat_context = ChatContext()
    
    # Test cases for distance report queries
    test_queries = [
        "Show me distance report",
        "Distance report for vehicle PB04SL5678",
        "Show distance traveled by vehicles",
        "Display drum rotation data",
        "Inter plant travel distance"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Testing: '{query}'")
        print("-" * 40)
        
        try:
            result = english_to_sql(query, chat_context)
            
            if result and result.get('sql'):
                sql = result['sql']
                print(f"Generated SQL:\n{sql}")
                
                # Check for conversion formulas
                has_distance_conversion = 'distance / 1000' in sql or 'distance/1000' in sql
                has_drum_conversion = 'drum_rotation / 2' in sql or 'CONCAT' in sql
                
                print(f"\n✅ Distance conversion applied: {has_distance_conversion}")
                print(f"✅ Drum rotation conversion applied: {has_drum_conversion}")
                
                if 'distance_report' in sql.lower():
                    if not has_distance_conversion and 'distance' in sql:
                        print("❌ MISSING: Distance conversion formula")
                    if not has_drum_conversion and 'drum_rotation' in sql:
                        print("❌ MISSING: Drum rotation conversion formula")
                    
                    if has_distance_conversion and has_drum_conversion:
                        print("🎉 SUCCESS: All conversions applied correctly!")
                
            else:
                print(f"❌ No SQL generated: {result.get('response', 'Unknown error')}")
                
        except Exception as e:
            print(f"❌ Error testing query: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Distance Conversion Test Complete")

if __name__ == "__main__":
    test_distance_conversion()
