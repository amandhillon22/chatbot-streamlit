#!/usr/bin/env python3
"""
Quick test for plant queries
"""

from query_agent_enhanced import english_to_sql

def test_plant_query():
    print("🧪 Testing plant query")
    
    queries = [
        "show me plants in punjab region",
        "list all plants",
        "plants in punjab"
    ]
    
    for query in queries:
        print(f"\n🔍 Query: '{query}'")
        try:
            result = english_to_sql(query)
            if result.get('sql'):
                print(f"✅ SQL: {result['sql']}")
            else:
                print(f"❌ No SQL: {result.get('response', 'No response')}")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_plant_query()
