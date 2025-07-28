#!/usr/bin/env python3
"""
import sys
sys.path.append('/home/linux/Documents/chatbot-diya')

Quick test of the enhanced pronoun resolution with real system
"""

from src.core.query_agent import ChatContext, english_to_sql

def test_real_scenario():
    context = ChatContext()
    
    print('🔥 Testing Enhanced Pronoun Resolution with Real System')
    print('=' * 55)
    
    print('\n1. Initial query: show me vehicles')
    result1 = english_to_sql('show me vehicles', chat_context=context)
    print(f'SQL: {result1.get("sql", "None")[:100]}...')
    
    # Simulate storing results (as would happen in real app)
    context.store_displayed_results(
        ['reg_no', 'vehicle_type', 'plant_id'], 
        [
            ['UP16GT8409', 'Truck', 460], 
            ['KA01AK6654', 'Car', 461],
            ['PB65BB5450', 'Bus', 462]
        ], 
        'show me vehicles', 
        result1.get('sql')
    )
    print(f'✅ Stored 3 vehicles in context')
    
    print('\n2. Follow-up: show their details')
    result2 = english_to_sql('show their details', chat_context=context)
    
    if result2.get('context_resolution_applied'):
        print('✅ SUCCESS: Pronoun resolved with context!')
        print(f'SQL: {result2.get("sql", "None")[:120]}...')
        print(f'Response: {result2.get("response", "None")[:80]}...')
        print(f'Reasoning: {result2.get("reasoning", "None")}')
    else:
        print('❌ FAILED: Pronoun not resolved')
        print(f'Response: {result2.get("response", "None")[:120]}...')
    
    print('\n3. Another follow-up: what are their plant names')
    result3 = english_to_sql('what are their plant names', chat_context=context)
    
    if result3.get('context_resolution_applied'):
        print('✅ SUCCESS: Plant names pronoun resolved!')
        print(f'SQL: {result3.get("sql", "None")[:120]}...')
    else:
        print('❌ FAILED: Plant names pronoun not resolved')
        print(f'Response: {result3.get("response", "None")[:120]}...')
    
    print('\n4. Edge case: tell me more about them')
    result4 = english_to_sql('tell me more about them', chat_context=context)
    
    if result4.get('context_resolution_applied'):
        print('✅ SUCCESS: Generic pronoun resolved!')
        print(f'SQL: {result4.get("sql", "None")[:120]}...')
    else:
        print('❌ FAILED: Generic pronoun not resolved')
        print(f'Response: {result4.get("response", "None")[:120]}...')

if __name__ == "__main__":
    test_real_scenario()
