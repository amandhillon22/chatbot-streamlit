#!/usr/bin/env python3
"""
import sys
sys.path.append('/home/linux/Documents/chatbot-diya')

Test typo detection in pronoun resolver
"""

from src.nlp.enhanced_pronoun_resolver import EnhancedPronounResolver

def test_typo_detection():
    resolver = EnhancedPronounResolver()
    
    print("🧪 Testing Typo Detection in Pronoun Resolver")
    print("=" * 50)
    
    # Test both correct and incorrect spelling
    test_queries = [
        'give their customer names',  # Correct
        'give thier customer names',  # Typo: thier
        'show thier details',         # Typo: thier  
        'what are thire names',       # Typo: thire
        'display their information',  # Correct
        'show thier plant names'      # Typo: thier
    ]
    
    for query in test_queries:
        detection = resolver.detect_pronoun_reference(query)
        print(f'📝 Query: "{query}"')
        print(f'   ✅ Detected: {detection["has_pronoun_reference"]}')
        print(f'   📊 Type: {detection.get("pronoun_type", "None")}')
        print(f'   🔍 Field: {detection.get("extracted_field", "None")}')
        print(f'   🎯 Confidence: {detection.get("confidence", 0.0)}')
        print()

if __name__ == "__main__":
    test_typo_detection()
