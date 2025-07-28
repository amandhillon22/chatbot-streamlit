#!/usr/bin/env python3
"""
import sys
sys.path.append('/home/linux/Documents/chatbot-diya')

Quick test for "show their categories" fix
"""

from src.nlp.enhanced_pronoun_resolver import EnhancedPronounResolver

class MockChatContext:
    def __init__(self, items):
        self.last_displayed_items = items

# Test data
complaint_data = [{'id_no': 272, 'complaint_date': '2025-06-17', 'description': 'Pump issue'}]
resolver = EnhancedPronounResolver()
mock_context = MockChatContext(complaint_data)

query = 'show their categories'
print(f"Testing: {query}")

detection = resolver.detect_pronoun_reference(query)
print(f"Detection: {detection}")

if detection.get('has_pronoun_reference'):
    result = resolver.resolve_context_reference(query, mock_context, detection)
    if result:
        print(f"Generated SQL:\n{result['sql']}")
    else:
        print("No result generated")
