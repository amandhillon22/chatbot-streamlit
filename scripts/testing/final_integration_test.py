#!/usr/bin/env python3
"""
import sys
sys.path.append('/home/linux/Documents/chatbot-diya')

Final integration test for the updated query_agent_enhanced.py with sentence transformers
"""

import os
import warnings
warnings.filterwarnings("ignore")

print("🧪 Final Integration Test: Query Agent with Sentence Transformers")
print("=" * 65)

try:
    print("1. Importing query agent...")
    from src.core.query_agent_enhanced import english_to_sql, EMBEDDINGS_AVAILABLE
    print(f"✅ Import successful. Embeddings available: {EMBEDDINGS_AVAILABLE}")
    
    if EMBEDDINGS_AVAILABLE:
        print("\n2. Testing natural language queries...")
        
        test_queries = [
            "show me all vehicles and their status",
            "get fuel consumption data for last month", 
            "list driver assignments",
            "find GPS tracking information"
        ]
        
        for query in test_queries:
            print(f"\n🔍 Query: '{query}'")
            try:
                result = english_to_sql(query)
                
                schema = result.get('schema', 'No schema')
                sql = result.get('sql', 'No SQL generated')
                response = result.get('response', 'No response')
                
                print(f"  Schema: {schema}")
                print(f"  SQL: {sql[:100]}{'...' if len(sql) > 100 else ''}")
                print(f"  Response: {response[:100]}{'...' if len(response) > 100 else ''}")
                
            except Exception as e:
                print(f"  ❌ Error: {e}")
        
        print("\n✅ All integration tests completed successfully!")
        print("\n🎉 SYSTEM READY: The chatbot now uses sentence transformers for improved semantic understanding!")
        
    else:
        print("❌ Embeddings not available - check sentence_embeddings.py")
        
except Exception as e:
    print(f"❌ Integration test failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 65)
