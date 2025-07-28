#!/usr/bin/env python3
"""
Test the specific active_status queries that seem to be failing
"""

import sys
sys.path.append('.')

from src.core.query_agent import english_to_sql

def test_active_status_queries():
    """Test the active_status queries specifically"""
    
    print("🔍 TESTING ACTIVE_STATUS QUERIES")
    print("=" * 50)
    
    queries = [
        "how many open complaints",
        "show closed complaints", 
        "count of active complaints"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n{i}. Query: '{query}'")
        print("-" * 30)
        
        try:
            result = english_to_sql(query)
            
            print(f"📋 Full result type: {type(result)}")
            print(f"📋 Full result: {result}")
            
            if result and isinstance(result, dict):
                if 'sql' in result:
                    sql = result.get('sql')
                    print(f"🔧 SQL type: {type(sql)}")
                    print(f"🔧 SQL value: '{sql}'")
                    
                    if sql and isinstance(sql, str):
                        print(f"📝 SQL: {sql}")
                        if "active_status = 'Y'" in sql:
                            print("✅ Uses correct active_status = 'Y'")
                        elif "active_status = 'N'" in sql:
                            print("✅ Uses correct active_status = 'N'")
                        elif "active_status" in sql.lower():
                            print("⚠️ Uses active_status but value unclear")
                        else:
                            print("ℹ️ No active_status in query")
                    else:
                        print("❌ SQL is None or not a string")
                else:
                    print("❌ No 'sql' key in result")
            else:
                print("❌ Result is None or not a dict")
                
        except Exception as e:
            print(f"❌ Exception: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_active_status_queries()
