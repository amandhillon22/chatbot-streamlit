#!/usr/bin/env python3
"""
Debug entity extraction for specific query
"""
import sys
sys.path.append('/home/linux/Documents/chatbot-diya')

def debug_entity_extraction():
    from src.core.intelligent_reasoning import IntelligentReasoning
    import re
    
    reasoning = IntelligentReasoning()
    
    query = "what is the size of kailash mahto"
    print(f"🔍 Debugging query: '{query}'")
    
    # Test individual regex patterns
    user_input_lower = query.lower()
    
    print(f"\n1. Lowercase query: '{user_input_lower}'")
    
    # Test capitalized name pattern
    pattern1 = r'\b([A-Z][a-z]+)\s+([A-Z][a-z]+)\b'
    matches1 = re.finditer(pattern1, query)
    print(f"2. Capitalized pattern matches: {[m.group(0) for m in matches1]}")
    
    # Test lowercase name pattern  
    pattern2 = r'\b([a-z]+)\s+([a-z]+)\b'
    matches2 = re.finditer(pattern2, user_input_lower)
    print(f"3. Lowercase pattern matches: {[m.group(0) for m in matches2]}")
    
    # Apply skip words filter
    skip_words = ['of', 'to', 'is', 'in', 'on', 'at', 'by', 'for', 'the', 'and', 'or', 'but', 'what', 'when', 'where', 'why', 'how', 'was', 'were', 'his', 'her', 'it', 'size', 'me', 'about', 'tell', 'give', 'want']
    
    matches2_filtered = []
    for match in re.finditer(pattern2, user_input_lower):
        first_name = match.group(1)
        last_name = match.group(2)
        if (len(first_name) > 2 and len(last_name) > 2 and 
            first_name not in skip_words and last_name not in skip_words):
            matches2_filtered.append(match.group(0))
    
    print(f"4. Filtered lowercase matches: {matches2_filtered}")
    
    # Test actual entity extraction
    entities = reasoning.extract_entities(query)
    print(f"5. Actual entities extracted: {entities}")
    
    return len(entities) > 0

if __name__ == "__main__":
    debug_entity_extraction()
