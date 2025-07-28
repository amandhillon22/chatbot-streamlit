#!/usr/bin/env python3
"""Test different phrasings for active status queries"""

import sys
sys.path.append('.')

from src.core.query_agent import english_to_sql

def test_active_status_phrasings():
    """Test different ways to ask about active status"""
    
    queries = [
        "how many open complaints",
        "show closed complaints", 
        "count active complaints",
        "list active complaints",
        "show active complaints",
        "count open complaints",
        "how many active complaints",
        "show complaints that are active",
        "show complaints that are open",
        "complaints with active status Y",
        "complaints with active status N"
    ]
    
    print("Testing different phrasings for active status queries:")
    print("=" * 60)
    
    for query in queries:
        print(f"\nQuery: '{query}'")
        try:
            result = english_to_sql(query)
            if result and result.get('sql'):
                sql = result['sql']
                if 'active_status' in sql:
                    print(f"✅ SQL: {sql.strip()[:100]}...")
                else:
                    print(f"⚠️ No active_status: {sql.strip()[:60]}...")
            else:
                print("❌ No SQL generated")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_active_status_phrasings()
