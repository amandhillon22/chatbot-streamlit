#!/usr/bin/env python3
"""
Test Plant Query Fixes
"""

import os
import sys
import warnings
warnings.filterwarnings('ignore')

os.chdir('/home/linux/Documents/chatbot-diya')

print("🌱 TESTING PLANT QUERY FIXES")
print("=" * 50)

try:
    from query_agent import ChatContext, english_to_sql
    
    context = ChatContext()
    
    # Test the problematic queries from the user's conversation
    test_queries = [
        "what is the plant id of mohali",
        "what is the name of the plant whose plant id is 460", 
        "give me site visit details of mohali plant"
    ]
    
    print("🧪 Testing Plant Queries:")
    print("-" * 30)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Query: '{query}'")
        
        try:
            result = english_to_sql(query, chat_context=context)
            
            if result.get('reasoning_applied'):
                print(f"   🧠 Intelligent reasoning applied: {result.get('reasoning_type')}")
                print(f"   💬 Response: {result.get('response', 'None')[:100]}...")
            
            if result.get('sql'):
                sql_text = result['sql']
                print(f"   📝 Generated SQL: {sql_text[:200]}...")
                
                # Check if it's using the right columns for plant names
                if 'plant_id = 460' in sql_text and ('site_name' in sql_text or 'cust_name' in sql_text):
                    print(f"   ✅ GOOD: Uses site_name/cust_name for plant name (not plant_code)")
                elif 'mohali' in query.lower() and ('site_name' in sql_text or 'cust_name' in sql_text):
                    print(f"   ✅ GOOD: Searches in site_name/cust_name for Mohali")
                elif 'crm_site_visit_dtls' in sql_text and 'plant_schedule' in sql_text:
                    print(f"   ✅ GOOD: Joins site visit with plant data")
                else:
                    print(f"   ⚠️ Check: Verify the SQL uses correct plant name columns")
            else:
                print(f"   ❌ No SQL generated")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Test intelligent reasoning specifically
    print(f"\n🧠 Testing Intelligent Reasoning for Plant Queries:")
    print("-" * 30)
    
    from intelligent_reasoning import IntelligentReasoning
    reasoning = IntelligentReasoning()
    
    reasoning_test = "what is the name of the plant whose plant id is 460"
    reasoning_result = reasoning.analyze_query_intent(reasoning_test, context)
    
    if reasoning_result:
        print(f"✅ Intent detected: {reasoning_result['intent']}")
        print(f"📊 Extracted: {reasoning_result['extracted_data']}")
        
        sql = reasoning.generate_intelligent_query(reasoning_result)
        if sql:
            print(f"🔧 Intelligent SQL: {sql.strip()}")
            
            if 'site_name' in sql and 'cust_name' in sql:
                print(f"✅ EXCELLENT: Intelligent reasoning uses correct plant name columns!")
            else:
                print(f"⚠️ Check: Verify intelligent SQL uses site_name/cust_name")
    else:
        print(f"❌ No intelligent reasoning detected")
    
    print(f"\n🎯 SUMMARY:")
    print("The fixes should ensure that:")
    print("✅ 'Plant name for ID 460' shows site_name/cust_name (not plant_code)")
    print("✅ 'Mohali plant' searches in site_name/cust_name fields") 
    print("✅ Site visit queries join crm_site_visit_dtls with plant_schedule")
    print("✅ Intelligent reasoning handles plant queries automatically")
    
except Exception as e:
    print(f"❌ Test failed: {e}")
    import traceback
    traceback.print_exc()
