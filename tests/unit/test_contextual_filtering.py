#!/usr/bin/env python3
"""
import sys
sys.path.append('/home/linux/Documents/chatbot-diya')

Test Enhanced Pronoun Resolution with Contextual Filtering
"""

from src.nlp.enhanced_pronoun_resolver import EnhancedPronounResolver

class MockChatContext:
    """Mock chat context for testing"""
    def __init__(self, items):
        self.last_displayed_items = items

def test_contextual_filtering():
    """Test contextual filtering scenarios"""
    
    # Simulate complaint data with categories
    complaint_data = [
        {
            'id_no': 272,
            'plant_name': 'PB-Mohali',
            'complaint_date': '2025-06-17',
            'complaint_category_id': 1,
            'description': 'Pump issue testing',
            'active_status': 'Y'
        },
        {
            'id_no': 274,
            'plant_name': 'PB-Mohali', 
            'complaint_date': '2025-06-17',
            'complaint_category_id': 2,
            'description': 'Leakage issue testing',
            'active_status': 'Y'
        },
        {
            'id_no': 275,
            'plant_name': 'PB-Mohali',
            'complaint_date': '2025-06-17', 
            'complaint_category_id': 2,
            'description': 'Cracks testing',
            'active_status': 'Y'
        }
    ]
    
    resolver = EnhancedPronounResolver()
    mock_context = MockChatContext(complaint_data)
    
    print("🧪 Testing Contextual Filtering")
    print("=" * 60)
    
    test_queries = [
        "which of them are of category quality",
        "out of these complaint IDs, whose category is quality", 
        "show their categories",
        "filter them by quality",
        "which ones are category operation"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n📝 Test {i}: {query}")
        print(f"📊 Context: {len(complaint_data)} complaints")
        
        # Detect pronoun
        detection = resolver.detect_pronoun_reference(query)
        print(f"🔍 Pronoun detected: {detection.get('has_pronoun_reference', False)}")
        print(f"🎯 Pattern type: {detection.get('pronoun_type')}")
        
        if detection.get('has_pronoun_reference'):
            result = resolver.resolve_context_reference(query, mock_context, detection)
            
            if result and 'sql' in result:
                sql = result['sql']
                print(f"🔧 Generated SQL:\n{sql}")
                
                # Check if SQL includes category filtering
                if "ccc.category_name" in sql or "category" in sql.lower():
                    print("✅ Correctly includes category information")
                else:
                    print("❌ Missing category information")
                    
                # Check if it has proper WHERE conditions
                if "AND" in sql and ("LOWER" in sql or "category" in sql.lower()):
                    print("✅ Correctly applies contextual filtering")
                else:
                    print("❌ Missing contextual filter condition")
                    
            else:
                print("❌ No SQL generated")
        else:
            print("❌ No pronoun detected")
        
        print("-" * 40)
    
    print("\n🎯 All contextual filtering tests completed!")

if __name__ == "__main__":
    test_contextual_filtering()
