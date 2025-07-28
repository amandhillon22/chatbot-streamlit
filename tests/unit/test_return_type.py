#!/usr/bin/env python3
"""
import sys
sys.path.append('/home/linux/Documents/chatbot-diya')

Check what english_to_sql actually returns
"""

print("🔍 Checking return type of english_to_sql...")

try:
    from src.core.query_agent import english_to_sql
    
    test_query = "show me the vehicles of mohali plant"
    print(f"Testing: '{test_query}'")
    
    result = english_to_sql(test_query)
    
    print(f"Return type: {type(result)}")
    print(f"Result: {result}")
    
    if isinstance(result, dict):
        print("📋 Dictionary keys:")
        for key, value in result.items():
            print(f"  {key}: {type(value)} = {str(value)[:100]}...")
            
        # Extract SQL if it exists
        sql = result.get('sql')
        if sql:
            print(f"\n✅ SQL found: {sql[:200]}...")
            
            # Check hierarchical elements in SQL
            if isinstance(sql, str):
                sql_lower = sql.lower()
                checks = {
                    'id_hosp': 'id_hosp' in sql_lower,
                    'vehicle_master': 'vehicle_master' in sql_lower,
                    'hosp_master': 'hosp_master' in sql_lower,
                    'JOIN': 'join' in sql_lower
                }
                
                print("\n🔍 Hierarchical relationship checks:")
                for check, passed in checks.items():
                    print(f"  {'✅' if passed else '❌'} {check}: {'Present' if passed else 'Missing'}")
        else:
            print("❌ No SQL in result")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n✅ Type check complete!")
