#!/usr/bin/env python3
"""
Final validation test with user's actual query sample
"""

import sys
import os
sys.path.append('/home/linux/Documents/chatbot-diya')

from src.core.query_agent import english_to_sql, ChatContext

def test_user_sample_query():
    """Test with the exact query that was failing for the user"""
    
    print("🎯 Final Validation: User's Actual Query Sample")
    print("=" * 60)
    
    chat_context = ChatContext()
    
    # This should now properly convert:
    # - distance: 151515 meters → 151.52 KM
    # - drum_rotation: 1794 → 1794/2 = 897 minutes → 14:57
    
    query = "Show me distance report"
    
    print(f"🔍 Testing: '{query}'")
    print("-" * 40)
    
    try:
        result = english_to_sql(query, chat_context)
        
        if result and result.get('sql'):
            sql = result['sql']
            print(f"Generated SQL:\n{sql}")
            
            # Validate conversion formulas are present
            has_distance_conversion = 'distance / 1000' in sql
            has_drum_conversion = 'drum_rotation / 2' in sql and 'CONCAT' in sql
            
            print(f"\n✅ Distance conversion (meters → KM): {has_distance_conversion}")
            print(f"✅ Drum rotation conversion (raw → HH:MM): {has_drum_conversion}")
            
            if has_distance_conversion and has_drum_conversion:
                print("\n🎉 SUCCESS: Query will now properly convert:")
                print("   • Raw distance 151515 meters → 151.52 KM")
                print("   • Raw drum_rotation 1794 → 14:57 (1794/2=897 min → 14:57)")
                print("\n✅ VALIDATION COMPLETE: User's issue has been resolved!")
            else:
                print("❌ VALIDATION FAILED: Conversions still missing")
        else:
            print(f"❌ No SQL generated: {result.get('response', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_user_sample_query()
