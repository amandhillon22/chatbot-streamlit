#!/usr/bin/env python3
"""
Simple test to verify intelligent reasoning works
"""

import os
import sys
import warnings
warnings.filterwarnings('ignore')

os.chdir('/home/linux/Documents/chatbot-diya')

print("🧠 SIMPLE INTELLIGENT REASONING TEST")
print("=" * 50)

try:
    from query_agent import ChatContext, english_to_sql
    
    # Create context with complaint data
    context = ChatContext()
    
    # Simulate the exact scenario from the chat
    context.last_displayed_items = [
        {
            'complaint_id': 172,
            'plant_id': 435,
            'customer_id': 119898,
            'site_id': 201794,
            '_original_question': 'site visit details of complaint id 172'
        }
    ]
    
    # Test the exact query from the user
    test_query = "can you tell me the plant name for complaint id 172"
    print(f"📝 Testing: '{test_query}'")
    
    result = english_to_sql(test_query, chat_context=context)
    
    print(f"\n📊 Result:")
    print(f"  SQL: {result.get('sql', 'None')}")
    print(f"  Response: {result.get('response', 'None')}")
    print(f"  Reasoning Applied: {result.get('reasoning_applied', False)}")
    
    if result.get('reasoning_applied'):
        print(f"✅ SUCCESS: Intelligent reasoning is working!")
    else:
        print(f"❌ Intelligent reasoning not applied")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
