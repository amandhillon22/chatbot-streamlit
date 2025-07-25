#!/usr/bin/env python3
"""
Test the complete complaint-to-customer resolution
"""

from enhanced_pronoun_resolver import EnhancedPronounResolver

class MockChatContext:
    """Mock chat context for testing"""
    def __init__(self, items):
        self.last_displayed_items = items

def test_complaint_to_customer():
    """Test generating customer names from complaint context"""
    
    # Simulate the actual complaint data from the logs
    complaint_data = [
        {
            'id_no': 305, 
            'plant_name': 'PB-Mohali', 
            'cust_id': 107456, 
            'site_id': 150750, 
            'complaint_date': '2025-07-02',
            'complaint_category_id': 1, 
            'description': 'Testing', 
            'complaint_raised_by': 'AjayM@rdc', 
            'active_status': 'Y', 
            '_display_index': 1, 
            '_original_question': 'show the complaints that have been opened this month'
        },
        {
            'id_no': 306, 
            'plant_name': 'PB-Mohali', 
            'cust_id': 115840, 
            'site_id': 182482, 
            'complaint_date': '2025-07-02',
            'complaint_category_id': 2, 
            'description': 'Crack testing', 
            'complaint_raised_by': 'AjayM@rdc', 
            'active_status': 'Y', 
            '_display_index': 2, 
            '_original_question': 'show the complaints that have been opened this month'
        }
    ]
    
    resolver = EnhancedPronounResolver()
    mock_context = MockChatContext(complaint_data)
    
    print("🧪 Testing Complaint → Customer Name Resolution")
    print("=" * 60)
    
    # Test the actual user query
    query = "give customer names for each of them"
    
    print(f"📝 Query: {query}")
    print(f"📊 Complaint context: {len(complaint_data)} complaints")
    
    # Detect pronoun
    detection = resolver.detect_pronoun_reference(query)
    print(f"🔍 Pronoun detected: {detection.get('has_pronoun_reference', False)}")
    
    if detection.get('has_pronoun_reference'):
        result = resolver.resolve_context_reference(query, mock_context, detection)
        
        if result and 'sql' in result:
            sql = result['sql']
            print(f"🔧 Generated SQL:\n{sql}")
            
            # Check if it's the right approach for customer names
            if "customer_ship_details" in sql and "cust_id" in sql:
                print("✅ Correct approach: Using cust_id to get customer names")
            else:
                print("❌ Incorrect approach: Not using proper customer relationship")
                
        else:
            print("❌ No SQL generated")
    else:
        print("❌ No pronoun detected")

if __name__ == "__main__":
    test_complaint_to_customer()
