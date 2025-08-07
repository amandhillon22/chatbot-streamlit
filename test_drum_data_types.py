#!/usr/bin/env python3
"""
Test drum trip queries with simplified AI-first approach
to verify data type conflict resolution
"""

import requests
import json
import time

def test_drum_queries():
    base_url = "http://localhost:5050"
    
    # Test queries that previously caused data type conflicts
    test_queries = [
        {
            "query": "show me 20 drum trip reports",
            "description": "Simple drum trip query"
        },
        {
            "query": "give the loading time of KA01AL8030",
            "description": "Follow-up query that previously caused data type error"
        },
        {
            "query": "show drum trips where loading time is greater than 30 minutes",
            "description": "Query with drum_in_plant comparison (double precision vs text)"
        }
    ]
    
    print("🎯 TESTING SIMPLIFIED AI-FIRST DRUM QUERIES")
    print("=" * 60)
    
    session_id = f"test_session_{int(time.time())}"
    
    for i, test in enumerate(test_queries, 1):
        print(f"\n📋 Test {i}: {test['description']}")
        print(f"👤 Query: \"{test['query']}\"")
        print("-" * 40)
        
        try:
            # Make API request
            response = requests.post(
                f"{base_url}/query",
                json={
                    "query": test['query'],
                    "session_id": session_id
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get('success'):
                    print("✅ SUCCESS: Query executed without data type errors")
                    
                    # Show SQL generated
                    if 'sql' in result:
                        print(f"🔧 Generated SQL: {result['sql'][:100]}...")
                    
                    # Show data count
                    if 'data' in result and isinstance(result['data'], list):
                        print(f"📊 Retrieved: {len(result['data'])} records")
                        if result['data']:
                            print(f"📝 Sample columns: {list(result['data'][0].keys())}")
                    
                    # Show response
                    if 'response' in result:
                        print(f"🤖 Response: {result['response'][:150]}...")
                        
                else:
                    print(f"❌ FAILED: {result.get('error', 'Unknown error')}")
                    if 'sql' in result:
                        print(f"🔧 Failed SQL: {result['sql']}")
                        
            else:
                print(f"❌ HTTP ERROR: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"Error details: {error_data}")
                except:
                    print(f"Raw response: {response.text[:200]}")
                    
        except Exception as e:
            print(f"❌ EXCEPTION: {e}")
        
        print("=" * 40)
        time.sleep(1)  # Brief pause between tests

if __name__ == "__main__":
    print("🚀 Starting drum trip data type conflict tests...")
    test_drum_queries()
    print("\n🎯 Test completed!")
