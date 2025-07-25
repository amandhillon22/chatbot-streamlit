#!/usr/bin/env python3
"""
Direct test of the SQL generation for complaint customer names
"""

from enhanced_pronoun_resolver import EnhancedPronounResolver

def test_sql_generation():
    """Test direct SQL generation for complaint customer names"""
    print("🧪 Testing SQL Generation for Complaint Customer Names")
    print("=" * 55)
    
    resolver = EnhancedPronounResolver()
    
    # Simulate the exact context from user's scenario
    class MockChatContext:
        def __init__(self):
            self.last_displayed_items = [
                {
                    'id_no': 305,
                    'complaint_date': '2025-07-02',
                    'plant_name': 'PB-Mohali',
                    'description': 'Testing',
                    'active_status': 'Y'
                },
                {
                    'id_no': 306,
                    'complaint_date': '2025-07-02', 
                    'plant_name': 'PB-Mohali',
                    'description': 'Crack testing',
                    'active_status': 'Y'
                }
            ]
    
    context = MockChatContext()
    
    # Test the exact query from user
    query = "give their customer names"
    
    print(f"📝 Query: {query}")
    print(f"📊 Context: {len(context.last_displayed_items)} complaints")
    
    # Test detection
    detection = resolver.detect_pronoun_reference(query)
    print(f"🎯 Pronoun detected: {detection['has_pronoun_reference']}")
    print(f"🔍 Field: {detection.get('extracted_field')}")
    
    # Test resolution
    resolution = resolver.resolve_context_reference(query, context, detection)
    
    if resolution:
        print(f"\n✅ SQL Generated Successfully:")
        print(f"🔧 SQL Query:")
        print("   " + "\n   ".join(resolution['sql'].split('\n')))
        
        print(f"\n📋 Query Analysis:")
        print(f"   📊 Entity Type: {resolution['entity_type']}")
        print(f"   🔍 Requested Field: {resolution['requested_field']}")
        print(f"   📝 Reasoning: {resolution['reasoning']}")
        
        # Verify the SQL has the correct components
        sql = resolution['sql']
        checks = {
            'Has customer_name field': 'customer_name' in sql,
            'Joins customer_ship_details': 'customer_ship_details' in sql,
            'Uses complaint IDs 305, 306': "'305'" in sql and "'306'" in sql,
            'Uses table alias cd': 'cd.' in sql,
            'Uses table alias csd': 'csd.' in sql,
            'Joins via cust_id': 'cust_id' in sql
        }
        
        print(f"\n🔍 SQL Validation:")
        for check, passed in checks.items():
            status = "✅" if passed else "❌"
            print(f"   {status} {check}")
            
        print(f"\n🎯 Expected Result: This SQL should return customer names for complaint IDs 305 and 306")
    else:
        print("❌ Failed to generate SQL")

if __name__ == "__main__":
    test_sql_generation()
