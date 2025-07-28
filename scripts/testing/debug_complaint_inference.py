#!/usr/bin/env python3
"""
import sys
sys.path.append('/home/linux/Documents/chatbot-diya')

Debug the entity inference issue with complaints
"""

from src.nlp.enhanced_pronoun_resolver import EnhancedPronounResolver

def test_complaint_inference():
    """Test what's happening with complaint entity inference"""
    
    # Simulate the actual data from the logs
    complaint_data = [
        {
            'id_no': 305, 
            'plant_name': 'PB-Mohali', 
            'cust_id': 107456, 
            'site_id': 150750, 
            'complaint_date': '2025-07-02',  # datetime.date(2025, 7, 2)
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
            'complaint_date': '2025-07-02',  # datetime.date(2025, 7, 2)
            'complaint_category_id': 2, 
            'description': 'Crack testing', 
            'complaint_raised_by': 'AjayM@rdc', 
            'active_status': 'Y', 
            '_display_index': 2, 
            '_original_question': 'show the complaints that have been opened this month'
        }
    ]
    
    resolver = EnhancedPronounResolver()
    
    print("🧪 Testing Complaint Entity Inference")
    print("=" * 50)
    
    print(f"📊 Sample data fields: {set(complaint_data[0].keys())}")
    
    # Test entity inference
    entity_type = resolver._infer_entity_type(complaint_data)
    print(f"🎯 Inferred entity type: {entity_type}")
    
    # Test the pronoun detection for the actual query
    query = "give customer names for each of them"
    detection = resolver.detect_pronoun_reference(query)
    print(f"🔍 Pronoun detection result: {detection}")
    
    print("\n" + "=" * 50)
    return entity_type, detection

if __name__ == "__main__":
    test_complaint_inference()
