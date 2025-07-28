#!/usr/bin/env python3
"""
import sys
sys.path.append('/home/linux/Documents/chatbot-diya')

Test the corrected JOIN condition for complaints
"""

from src.nlp.enhanced_pronoun_resolver import EnhancedPronounResolver

class MockChatContext:
    def __init__(self, items):
        self.last_displayed_items = items

# Test with complaint data
complaint_data = [
    {'id_no': 303, 'complaint_date': '2025-06-30', 'description': 'Pipeline issue'},
    {'id_no': 304, 'complaint_date': '2025-06-30', 'description': 'Testing'}
]

resolver = EnhancedPronounResolver()
mock_context = MockChatContext(complaint_data)

query = 'which of them are of category quality'
print(f'🧪 Testing: {query}')

detection = resolver.detect_pronoun_reference(query)
if detection.get('has_pronoun_reference'):
    result = resolver.resolve_context_reference(query, mock_context, detection)
    if result:
        print('\n📝 Generated SQL:')
        print(result['sql'])
        print()
        
        # Check if the correct JOIN is used
        sql = result['sql']
        if 'cd.complaint_type_id = ccct.id_no' in sql:
            print('✅ Correct JOIN condition: cd.complaint_type_id = ccct.id_no')
        elif 'cd.complaint_category_type_id = ccct.id_no' in sql:
            print('❌ Incorrect JOIN condition: cd.complaint_category_type_id = ccct.id_no')
        else:
            print('❓ JOIN condition not found in SQL')
            
        print('\n🎯 SQL Analysis:')
        print(f"Contains correct JOIN: {'cd.complaint_type_id = ccct.id_no' in sql}")
        print(f"Contains incorrect JOIN: {'cd.complaint_category_type_id = ccct.id_no' in sql}")
    else:
        print('❌ No result generated')
else:
    print('❌ No pronoun detected')
