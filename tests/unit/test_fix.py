#!/usr/bin/env python3
"""
sys.path.append('/home/linux/Documents/chatbot-diya')

Simple test to verify the enhanced table mapping fix
"""

import os
import sys

# Ensure we're in the right directory and using the virtual environment
os.chdir('/home/linux/Documents/chatbot-diya')
sys.path.insert(0, '/home/linux/Documents/chatbot-diya/venv/lib/python3.12/site-packages')

try:
    print("🔧 TESTING ENHANCED TABLE MAPPING FIX")
    print("=" * 50)
    
    # Suppress streamlit warnings
    import warnings
    warnings.filterwarnings('ignore')
    
    from src.core.query_agent import ChatContext, english_to_sql
    
    context = ChatContext()
    test_query = "show me the site visit details any one complaint id"
    
    print(f"📝 Testing query: '{test_query}'")
    
    # Test the enhanced mapping
    result = english_to_sql(test_query, chat_context=context)
    
    if result and result.get('sql'):
        sql_text = result['sql']
        print(f"\n📊 Generated SQL:")
        print(sql_text)
        
        # Check if it uses the correct table
        if 'crm_site_visit_dtls' in sql_text.lower():
            print("\n✅ SUCCESS! The enhanced table mapping is now working correctly!")
            print("✅ Query uses the crm_site_visit_dtls table as expected")
        elif 'crm_site_visit' in sql_text.lower():
            print("\n✅ PARTIAL SUCCESS! Uses a CRM site visit table")
        else:
            print("\n❌ ISSUE: Still not using the CRM site visit table")
            
            # Extract which table it used
            import re
            from_match = re.search(r'FROM\s+(\S+)', sql_text, re.IGNORECASE)
            if from_match:
                used_table = from_match.group(1)
                print(f"   Instead used table: {used_table}")
    else:
        print("\n❌ No SQL generated")
    
    # Also test the enhanced table mapper directly
    print(f"\n🔍 Direct enhanced table mapper test:")
    
    from src.nlp.enhanced_table_mapper import EnhancedTableMapper
    from src.core.query_agent import SCHEMA_DICT
    
    mapper = EnhancedTableMapper()
    
    if 'public' in SCHEMA_DICT:
        available_tables = [f'public.{table}' for table in SCHEMA_DICT['public'].keys()]
        
        # Test priority mapping
        priority_tables = mapper.get_priority_tables(test_query)
        print(f"Priority tables: {priority_tables}")
        
        # Check if crm_site_visit_dtls is now properly matched
        crm_found = False
        for priority_table in priority_tables:
            public_table = f'public.{priority_table}'
            if public_table in available_tables:
                print(f"✅ Found matching table: {public_table}")
                if 'crm_site_visit' in public_table:
                    crm_found = True
        
        if crm_found:
            print("✅ Enhanced table mapping should now work correctly!")
        else:
            print("❌ CRM site visit table still not properly matched")
    
    print(f"\n🎉 Test completed!")
    
except Exception as e:
    print(f"❌ Error during test: {e}")
    import traceback
    traceback.print_exc()
