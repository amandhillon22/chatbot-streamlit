#!/usr/bin/env python3
"""
Test script to validate response improvements
"""

import sys
import os
sys.path.append('/home/linux/Documents/chatbot-diya')

from src.core.query_agent import english_to_sql, ChatContext

def test_response_improvements():
    """Test the improved response formatting"""
    
    print("🎯 Testing Response Improvements")
    print("=" * 50)
    
    chat_context = ChatContext()
    
    test_queries = [
        "Show me distance report",
        "Show all vehicles", 
        "Show all plants",
        "Vehicle hierarchy report"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Testing: '{query}'")
        print("-" * 40)
        
        try:
            result = english_to_sql(query, chat_context)
            
            if result and result.get('sql'):
                sql = result['sql']
                print(f"Generated SQL:\n{sql}")
                
                # Check for improvements
                has_limit = 'LIMIT' in sql.upper()
                has_aliases = ' as ' in sql.lower()
                
                print(f"\n✅ Has LIMIT clause: {has_limit}")
                print(f"✅ Has column aliases: {has_aliases}")
                print(f"📝 Response: {result.get('response', 'No response')}")
                
                # Check if response contains technical info
                response = result.get('response', '')
                has_suggestions = any(word in response.lower() for word in ['would you like', 'you could', 'alternatively', 'suggestion'])
                has_technical = any(word in response.lower() for word in ['sql', 'database', 'table', 'column'])
                
                print(f"🚫 Contains suggestions: {has_suggestions}")
                print(f"🚫 Contains technical info: {has_technical}")
                
                if has_limit and has_aliases and not has_suggestions and not has_technical:
                    print("🎉 SUCCESS: All improvements applied!")
                else:
                    print("❌ ISSUES: Some improvements missing")
                
            else:
                print(f"❌ No SQL generated: {result.get('response', 'Unknown error')}")
                
        except Exception as e:
            print(f"❌ Error testing query: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Response Improvement Test Complete")

if __name__ == "__main__":
    test_response_improvements()
