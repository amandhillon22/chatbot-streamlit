#!/usr/bin/env python3
"""
Test the updated enhanced pronoun resolver with complaint customer names
"""

from enhanced_pronoun_resolver import EnhancedPronounResolver

def test_complaint_customer_names():
    """Test customer names for complaints using the site visit details table"""
    print("🧪 Testing Complaint Customer Names Resolution")
    print("=" * 50)
    
    resolver = EnhancedPronounResolver()
    
    # Mock chat context with complaint data (similar to your actual data)
    class MockChatContext:
        def __init__(self):
            self.last_displayed_items = [
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
            self.history = []
    
    context = MockChatContext()
    
    # Test the customer names query
    query = "give their customer names"
    print(f"📝 Testing query: '{query}'")
    
    # Test pronoun detection
    detection = resolver.detect_pronoun_reference(query)
    print(f"   🎯 Detected: {detection['has_pronoun_reference']}")
    print(f"   📊 Type: {detection.get('pronoun_type')}")
    print(f"   🔍 Field: {detection.get('extracted_field')}")
    
    # Test entity inference
    entity_type = resolver._infer_entity_type(context.last_displayed_items)
    print(f"   🏷️ Inferred entity type: {entity_type}")
    
    # Test context resolution
    if detection['needs_context_resolution']:
        resolution = resolver.resolve_context_reference(query, context, detection)
        if resolution:
            print(f"   ✅ Generated SQL:")
            print(f"   {resolution['sql']}")
            print(f"   🎯 Entity: {resolution['entity_type']}")
            print(f"   📊 Field: {resolution['requested_field']}")
            print(f"   💭 Reasoning: {resolution['reasoning']}")
        else:
            print(f"   ❌ Could not resolve context")
    
    # Test clarification avoidance
    should_avoid = resolver.should_avoid_clarification(query, context)
    print(f"   🚫 Avoid clarification: {should_avoid}")

if __name__ == "__main__":
    test_complaint_customer_names()
