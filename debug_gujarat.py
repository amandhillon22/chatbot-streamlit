#!/usr/bin/env python3
"""Debug the Gujarat query generation process"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from query_agent import english_to_sql

def debug_gujarat_query():
    """Debug the Gujarat query to see why it's still using zone_master"""
    print("🔍 Debugging Gujarat Query Generation...")
    print("=" * 60)
    
    test_query = "show me plants in Gujarat"
    print(f"📋 Query: '{test_query}'")
    
    # Temporarily modify to add debug output
    import query_agent
    
    # Patch the intelligent reasoning check
    original_reasoning = query_agent.intelligent_reasoning
    
    class DebugWrapper:
        def __init__(self, original):
            self.original = original
            
        def analyze_query_intent(self, prompt, chat_context):
            print(f"🧠 Intelligent reasoning called with: '{prompt}'")
            if self.original:
                result = self.original.analyze_query_intent(prompt, chat_context)
                if result:
                    print(f"🎯 Intelligent reasoning result: {result['intent']}")
                    print(f"📊 Extracted data: {result['extracted_data']}")
                else:
                    print("❌ Intelligent reasoning returned None")
                return result
            return None
            
        def generate_intelligent_query(self, reasoning_result):
            if self.original:
                result = self.original.generate_intelligent_query(reasoning_result)
                if result:
                    print(f"🏭 Generated intelligent SQL: {result[:100]}...")
                return result
            return None
    
    query_agent.intelligent_reasoning = DebugWrapper(original_reasoning)
    
    # Run the query
    result = english_to_sql(test_query)
    sql_query = result.get('sql', '')
    
    print(f"\n🔍 Final Generated SQL:")
    print(sql_query)
    
    # Restore original
    query_agent.intelligent_reasoning = original_reasoning
    
    # Analyze the result
    if 'zone_master' in sql_query and 'district_master' in sql_query:
        print("\n❓ ANALYSIS: Using both zone_master and district_master")
        print("   This suggests the full hierarchical chain is being used")
    elif 'zone_master' in sql_query:
        print("\n❌ ISSUE: Only using zone_master (incorrect for Gujarat)")
    elif 'district_master' in sql_query:
        print("\n✅ GOOD: Using district_master (correct for Gujarat)")
    else:
        print("\n⚠️ UNEXPECTED: Not using expected tables")

if __name__ == "__main__":
    debug_gujarat_query()
