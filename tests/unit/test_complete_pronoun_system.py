#!/usr/bin/env python3
"""
import sys
sys.path.append('/home/linux/Documents/chatbot-diya')

Comprehensive test of the Enhanced Pronoun Resolution System
with corrected database relationships
"""

from src.nlp.enhanced_pronoun_resolver import EnhancedPronounResolver

class MockChatContext:
    """Mock chat context for testing"""
    def __init__(self, items):
        self.last_displayed_items = items

def test_pronoun_system():
    """Test various pronoun scenarios with different entity types"""
    resolver = EnhancedPronounResolver()
    
    # Test scenarios with different entity types
    test_cases = [
        {
            "query": "show their addresses",
            "mock_items": [
                {"cust_id": "107456", "customer_name": "Customer A"},
                {"cust_id": "115840", "customer_name": "Customer B"}
            ],
            "entity_type": "customers",
            "expected_join": "LEFT JOIN site_master sm ON csd.ship_to_id = sm.id_no"
        },
        {
            "query": "what is their complaint status",
            "mock_items": [
                {"complaint_id": "12345", "complaint_desc": "Issue A"},
                {"complaint_id": "67890", "complaint_desc": "Issue B"}
            ],
            "entity_type": "complaints",
            "expected_table": "crm_complaint_dtls"
        },
        {
            "query": "show thier details",  # Typo test
            "mock_items": [
                {"vehicle_registration_number": "MH12AB1234", "model": "Model A"}
            ],
            "entity_type": "vehicles",
            "expected_table": "crm_site_visit_dtls"
        },
        {
            "query": "find its information",
            "mock_items": [
                {"plant_name": "Gujarat", "plant_id": "GUJ001"}
            ],
            "entity_type": "plants",
            "expected_table": "mst_plant"
        }
    ]
    
    print("🧪 Testing Complete Enhanced Pronoun Resolution System")
    print("=" * 60)
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n📝 Test {i}: {test['query']}")
        print(f"🎯 Mock Items: {len(test['mock_items'])} items")
        
        # Create mock context and test
        mock_context = MockChatContext(test['mock_items'])
        
        # Detect pronoun and resolve
        detection = resolver.detect_pronoun_reference(test['query'])
        print(f"🔍 Pronoun detected: {detection.get('has_pronoun_reference', False)}")
        
        if detection.get('has_pronoun_reference'):
            result = resolver.resolve_context_reference(test['query'], mock_context, detection)
            
            if result and 'sql' in result:
                sql = result['sql']
                print(f"🔧 Generated SQL:\n{sql}")
                
                # Validate expected elements
                if "expected_join" in test:
                    if test["expected_join"] in sql:
                        print(f"✅ Correct join condition found")
                    else:
                        print(f"❌ Expected join not found: {test['expected_join']}")
                
                if "expected_table" in test:
                    if test["expected_table"] in sql:
                        print(f"✅ Correct table found: {test['expected_table']}")
                    else:
                        print(f"❌ Expected table not found: {test['expected_table']}")
            else:
                print("❌ No SQL generated")
        else:
            print("❌ No pronoun reference detected")
        
        print("-" * 40)
    
    print("\n🎯 All tests completed!")

if __name__ == "__main__":
    test_pronoun_system()
