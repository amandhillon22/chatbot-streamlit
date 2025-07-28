#!/usr/bin/env python3
"""
import sys
sys.path.append('/home/linux/Documents/chatbot-diya')

Test fixed SQL generation for customer pronoun resolution
"""

from src.nlp.enhanced_pronoun_resolver import EnhancedPronounResolver

def test_fixed_sql():
    resolver = EnhancedPronounResolver()
    
    # Mock customer context (from the error scenario)
    class MockChatContext:
        def __init__(self):
            self.last_displayed_items = [
                {
                    'id_no': 305,
                    'cust_id': 107456,
                    'site_id': 150750,
                    '_display_index': 1
                },
                {
                    'id_no': 306, 
                    'cust_id': 115840,
                    'site_id': 182482,
                    '_display_index': 2
                }
            ]
    
    context = MockChatContext()
    
    print("🧪 Testing Fixed Customer Pronoun Resolution")
    print("=" * 50)
    
    # Test the query that caused the error
    query = 'give their details'
    print(f"Query: '{query}'")
    
    # Test pronoun detection
    detection = resolver.detect_pronoun_reference(query)
    print(f"✅ Pronoun detected: {detection['has_pronoun_reference']}")
    print(f"📊 Type: {detection.get('pronoun_type')}")
    print(f"🔍 Field: {detection.get('extracted_field')}")
    
    # Test context resolution
    if detection['needs_context_resolution']:
        resolution = resolver.resolve_context_reference(query, context, detection)
        if resolution:
            print(f"\n✅ SQL Generated Successfully:")
            print("=" * 30)
            print(resolution['sql'])
            print("=" * 30)
            print(f"🎯 Entity type: {resolution['entity_type']}")
            print(f"📊 Field requested: {resolution['requested_field']}")
            print(f"💡 Reasoning: {resolution['reasoning']}")
            
            # Check for the previous error
            if 'customer_master' in resolution['sql']:
                print("❌ Still using wrong table name!")
            elif 'customer_ship_details' in resolution['sql']:
                print("✅ Using correct table name!")
                
            # Check aliases consistency
            sql_lines = resolution['sql'].split('\n')
            select_line = sql_lines[0] if sql_lines else ""
            from_line = sql_lines[1] if len(sql_lines) > 1 else ""
            
            if 'csd.' in select_line and 'csd' in from_line:
                print("✅ Table aliases are consistent!")
            else:
                print("❌ Table alias mismatch detected!")
                print(f"   SELECT: {select_line}")
                print(f"   FROM: {from_line}")
        else:
            print("❌ Failed to generate SQL")

if __name__ == "__main__":
    test_fixed_sql()
