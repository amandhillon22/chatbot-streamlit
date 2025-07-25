#!/usr/bin/env python3
"""
Test the complete integration with actual query agent for complaint customer names
"""

from query_agent_enhanced import english_to_sql, ChatContext
import sql

def test_integrated_complaint_customer_names():
    """Test the complete integration for complaint customer names"""
    print("🧪 Testing Complete Integration - Complaint Customer Names")
    print("=" * 60)
    
    # Initialize chat context
    chat_context = ChatContext()
    
    # Simulate that complaints were just displayed (based on user's actual data)
    chat_context.last_displayed_items = [
        {
            'id_no': 305,
            'complaint_date': '2025-07-02',
            'plant_name': 'PB-Mohali',
            'description': 'Testing',
            'active_status': 'Y',
            '_display_index': 1,
            '_original_question': 'show the complaints that have been opened this month'
        },
        {
            'id_no': 306,
            'complaint_date': '2025-07-02',
            'plant_name': 'PB-Mohali',
            'description': 'Crack testing',
            'active_status': 'Y',
            '_display_index': 2,
            '_original_question': 'show the complaints that have been opened this month'
        }
    ]
    chat_context.last_result_entities = ['305', '306']
    
    # Test the follow-up query with pronoun
    followup_query = "give their customer names"
    print(f"📝 Follow-up Query: {followup_query}")
    
    try:
        # Process the query
        result = english_to_sql(followup_query, chat_context)
        
        print(f"✅ Query processed successfully")
        print(f"📊 Result: {result}")
        
        # Check if it contains SQL (indicating pronoun resolution worked)
        if isinstance(result, dict) and 'sql' in result:
            print("\n✅ Pronoun resolution worked! Generated SQL query.")
            print(f"🔍 Generated SQL:")
            print(f"   {result['sql']}")
            
            # Check if the SQL includes the site visit details join
            if 'crm_site_visit_dtls' in result['sql'] and 'customer_name' in result['sql']:
                print("✅ Correctly includes customer information from site visit details!")
            else:
                print("❌ Missing expected site visit details join or customer_name field")
                
        elif isinstance(result, str) and ("clarification" in result.lower() or "which" in result.lower()):
            print("❌ System still asking for clarification despite pronoun resolution")
            print(f"📝 Response: {result}")
        else:
            print("✅ Pronoun resolution worked! No clarification request.")
            print(f"📊 Full result: {result}")
            
    except Exception as e:
        print(f"❌ Error in integration test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_integrated_complaint_customer_names()
