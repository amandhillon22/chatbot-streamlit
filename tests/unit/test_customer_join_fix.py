#!/usr/bin/env python3
"""
import sys
sys.path.append('/home/linux/Documents/chatbot-diya')

Test the corrected customer join for the enhanced pronoun resolver
"""

from src.nlp.enhanced_pronoun_resolver import EnhancedPronounResolver

def test_customer_join_fix():
    """Test that customer queries generate correct joins"""
    print("🧪 Testing Customer Join Fix")
    print("=" * 40)
    
    resolver = EnhancedPronounResolver()
    
    # Mock chat context with customer data (like the scenario mentioned)
    class MockChatContext:
        def __init__(self):
            self.last_displayed_items = [
                {
                    'cust_id': '107456',
                    'customer_name': 'Customer A',
                    '_display_index': 1,
                    '_original_question': 'show customers with cust_id 107456 and 115840'
                },
                {
                    'cust_id': '115840',
                    'customer_name': 'Customer B',
                    '_display_index': 2,
                    '_original_question': 'show customers with cust_id 107456 and 115840'
                }
            ]
    
    context = MockChatContext()
    
    # Test a customer query that would use the join
    query = "show their addresses"
    print(f"📝 Testing query: '{query}'")
    
    # Test detection
    detection = resolver.detect_pronoun_reference(query)
    print(f"🎯 Pronoun detected: {detection['has_pronoun_reference']}")
    print(f"🔍 Field: {detection.get('extracted_field')}")
    
    # Test entity inference
    entity_type = resolver._infer_entity_type(context.last_displayed_items)
    print(f"🏷️ Inferred entity type: {entity_type}")
    
    # Test resolution
    if detection['needs_context_resolution']:
        resolution = resolver.resolve_context_reference(query, context, detection)
        if resolution:
            print(f"\n✅ Generated SQL:")
            print(f"   {resolution['sql']}")
            
            # Check for the corrected join
            sql = resolution['sql']
            if 'sm.id_no' in sql and 'csd.ship_to_id = sm.id_no' in sql:
                print("✅ Correct join: Uses sm.id_no instead of sm.ship_to_id")
            else:
                print("❌ Join issue: Check the join condition")
                
        else:
            print("❌ Could not resolve context")

if __name__ == "__main__":
    test_customer_join_fix()
