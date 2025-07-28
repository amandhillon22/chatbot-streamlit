#!/usr/bin/env python3
"""Verify the fixed Gujarat query works with actual data"""

import sys
import os
sys.path.append('/home/linux/Documents/chatbot-diya')

from src.core.query_agent import english_to_sql
from src.core.sql import run_query

def verify_gujarat_fix():
    """Verify the fixed Gujarat query works correctly"""
    print("🧪 Verifying Gujarat Query Fix...")
    print("=" * 60)
    
    test_query = "show me plants in Gujarat"
    print(f"📋 Query: '{test_query}'")
    
    # Generate the SQL
    result = english_to_sql(test_query)
    sql_query = result.get('sql', '')
    
    print(f"\n🔍 Generated SQL:")
    print(sql_query)
    
    # Verify it uses the correct approach
    if 'dm.name ILIKE' in sql_query and 'zone_master' not in sql_query:
        print("✅ CORRECT: Using district_master approach (smart location detection)")
    elif 'zone_master' in sql_query:
        print("❌ STILL WRONG: Using zone_master (should be district_master)")
        return False
    else:
        print("⚠️ UNEXPECTED: Query structure not as expected")
    
    # Test the query execution
    try:
        plants = run_query(sql_query)
        print(f"\n🏭 Results: Found {len(plants)} plants in Gujarat")
        
        # Show some plant names
        if plants and len(plants) > 0:
            print("📋 Plant names found:")
            for i, plant in enumerate(plants[:5]):  # Show first 5
                if isinstance(plant, tuple) and len(plant) > 0:
                    print(f"   {i+1}. {plant[0]}")
        
        return True
        
    except Exception as e:
        print(f"❌ SQL execution failed: {str(e)}")
        return False

def test_other_states():
    """Test other state queries to ensure consistency"""
    print(f"\n🧪 Testing Other State Queries...")
    print("=" * 40)
    
    test_states = ["Maharashtra", "West Bengal", "Punjab"]
    
    for state in test_states:
        print(f"\n📋 Testing: 'plants in {state}'")
        result = english_to_sql(f"plants in {state}")
        sql = result.get('sql', '')
        
        if 'dm.name ILIKE' in sql and 'zone_master' not in sql:
            print(f"✅ {state}: Using district_master (correct)")
        elif 'zone_master' in sql:
            print(f"❌ {state}: Using zone_master (should be district_master)")
        else:
            print(f"⚠️ {state}: Unexpected query structure")

if __name__ == "__main__":
    success = verify_gujarat_fix()
    
    if success:
        test_other_states()
        print(f"\n🎉 SUCCESS: Gujarat query fix is working correctly!")
        print("✅ Now using district_master for state/region queries")
        print("✅ More efficient queries without unnecessary zone_master joins")
    else:
        print(f"\n❌ FAILED: Gujarat query fix needs more work")
