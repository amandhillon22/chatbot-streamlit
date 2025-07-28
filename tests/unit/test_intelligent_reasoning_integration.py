#!/usr/bin/env python3
"""
sys.path.append('/home/linux/Documents/chatbot-diya')

Test Intelligent Reasoning Integration
"""

import os
import sys
os.chdir('/home/linux/Documents/chatbot-diya')

print("🧠 TESTING INTELLIGENT REASONING INTEGRATION")
print("=" * 60)

try:
    # Test the intelligent reasoning module first
    from src.core.intelligent_reasoning import IntelligentReasoning
    print("✅ Intelligent reasoning module imported")
    
    # Test the enhanced query_agent
    from src.core.query_agent import ChatContext, english_to_sql
    print("✅ Enhanced query_agent imported")
    
    # Create a mock conversation context
    context = ChatContext()
    
    # Simulate storing complaint data (like what happened in the chat)
    complaint_data = [
        {
            'complaint_id': 172,
            'plant_id': 435,
            'customer_id': 119898,
            'site_id': 201794,
            'date_of_visit': '2025-03-19',
            'liability': 200000.0,
            'reason_for_visit': 'Pump Issue'
        }
    ]
    
    context.store_results(
        results=complaint_data,
        columns=['complaint_id', 'plant_id', 'customer_id', 'site_id', 'date_of_visit', 'liability', 'reason_for_visit'],
        original_question='site visit details of complaint id 172'
    )
    
    print(f"📊 Stored complaint data in context: {len(complaint_data)} items")
    
    # Test the intelligent reasoning with the actual user query
    test_queries = [
        "can you tell me the plant name for complaint id 172",
        "what is the plant name for the one mentioned in complaint id 172",
        "tell me the plant name if you have the plant id", 
        "the plant name for that complaint"
    ]
    
    print(f"\n🧪 Testing Intelligent Reasoning Queries:")
    print("-" * 40)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Query: '{query}'")
        
        try:
            result = english_to_sql(query, chat_context=context)
            
            if result.get('reasoning_applied'):
                print(f"   ✅ Intelligent reasoning applied!")
                print(f"   🎯 Reasoning type: {result.get('reasoning_type')}")
                print(f"   📝 Generated SQL: {result.get('sql', 'None')[:100]}...")
                print(f"   💬 Response: {result.get('response', 'None')[:100]}...")
            else:
                print(f"   ❌ No intelligent reasoning applied")
                if result.get('sql'):
                    print(f"   📝 Regular SQL: {result.get('sql', 'None')[:100]}...")
                else:
                    print(f"   ❌ No SQL generated")
                    
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Test direct intelligent reasoning
    print(f"\n🔍 Direct Intelligent Reasoning Test:")
    print("-" * 40)
    
    reasoning = IntelligentReasoning()
    test_query = "can you tell me the plant name for complaint id 172"
    
    reasoning_result = reasoning.analyze_query_intent(test_query, context)
    if reasoning_result:
        print(f"✅ Intent detected: {reasoning_result['intent']}")
        print(f"📊 Extracted: {reasoning_result['extracted_data']}")
        
        sql = reasoning.generate_intelligent_query(reasoning_result)
        if sql:
            print(f"🔧 SQL: {sql.strip()}")
    else:
        print(f"❌ No reasoning detected")
    
    print(f"\n🎉 Intelligent Reasoning Integration Test Complete!")
    
except Exception as e:
    print(f"❌ Integration test failed: {e}")
    import traceback
    traceback.print_exc()
