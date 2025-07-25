#!/usr/bin/env python3
"""
Debug the specific failing queries
"""

import sys
sys.path.append('.')

from query_agent import english_to_sql

def debug_failing_queries():
    """Debug the specific queries that were failing"""
    
    print("🐛 DEBUGGING FAILING QUERIES")
    print("=" * 50)
    
    failing_queries = [
        "count of active complaints",
        "show open complaints with product correction done"
    ]
    
    for i, query in enumerate(failing_queries, 1):
        print(f"\n{i}. Debugging: '{query}'")
        print("-" * 40)
        
        try:
            result = english_to_sql(query)
            
            print(f"📋 Full result: {result}")
            
            if result:
                if 'sql' in result:
                    sql = result['sql']
                    print(f"🔧 SQL type: {type(sql)}")
                    print(f"🔧 SQL value: {sql}")
                    
                    if sql:
                        print(f"📝 SQL content: {sql}")
                    else:
                        print(f"❌ SQL is None or empty")
                        
                if 'response' in result:
                    print(f"💬 Response: {result['response']}")
                    
            else:
                print(f"❌ Result is None")
                
        except Exception as e:
            print(f"❌ Exception: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    debug_failing_queries()
