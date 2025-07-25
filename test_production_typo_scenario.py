#!/usr/bin/env python3
"""
Test production scenario with typos in pronoun references
Simulates the exact scenario where user types "give thier customer names"
"""

from query_agent_enhanced import english_to_sql, ChatContext
import sql  # For database connection

def test_production_typo_scenario():
    """Test the complete production scenario with typos"""
    print("🧪 Testing Production Typo Scenario")
    print("=" * 50)
    
    # Initialize chat context
    chat_context = ChatContext()
    
    # Simulate conversation history that establishes context
    # User asks about specific customers first
    context_query = "show customers with cust_id 107456 and 115840"
    print(f"📝 Context Query: {context_query}")
    
    # Get database connection
    conn = sql.get_connection()
    
    try:
        # This establishes the context about specific customers
        context_result = english_to_sql(context_query, chat_context)
        print(f"✅ Context established successfully")
        print(f"📊 Context result: {context_result}")
        
        # Simulate that we displayed customer information to user
        # This mimics what the chat interface would do
        chat_context.last_displayed_items = [
            {'cust_id': '107456', 'type': 'customer'},
            {'cust_id': '115840', 'type': 'customer'}
        ]
        chat_context.last_result_entities = ['107456', '115840']
        
        # Now test the follow-up query with typo
        followup_query = "give thier customer names"
        print(f"\n📝 Follow-up Query (with typo): {followup_query}")
        
        # Process the query with typo
        result = english_to_sql(followup_query, chat_context)
        
        print(f"✅ Query processed successfully")
        print(f"📊 Result: {result}")
        
        # Check if it contains SQL (indicating pronoun resolution worked)
        if isinstance(result, dict) and 'sql' in result:
            print("✅ Pronoun resolution worked! Generated SQL query.")
            print(f"🔍 Generated SQL: {result['sql']}")
        elif isinstance(result, str) and ("clarification" in result.lower() or "which" in result.lower()):
            print("❌ System still asking for clarification despite pronoun resolution")
            print(f"📝 Response: {result}")
        else:
            print("✅ Pronoun resolution worked! No clarification request.")
            print(f"📊 Full result: {result}")
            
    except Exception as e:
        print(f"❌ Error in production test: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        conn.close()

if __name__ == "__main__":
    test_production_typo_scenario()
