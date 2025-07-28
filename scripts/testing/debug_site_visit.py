#!/usr/bin/env python3
"""
sys.path.append('/home/linux/Documents/chatbot-diya')

Debug the site visit query issue
"""

import os
import sys
os.chdir('/home/linux/Documents/chatbot-diya')

print("🔍 DEBUGGING SITE VISIT QUERY ISSUE")
print("=" * 50)

try:
    # Import and test
    from src.core.query_agent import ChatContext, english_to_sql, enhanced_table_mapper
    from src.nlp.enhanced_table_mapper import EnhancedTableMapper
    
    print("✅ Modules imported successfully")
    print(f"Enhanced table mapper status: {enhanced_table_mapper is not None}")
    
    if enhanced_table_mapper is None:
        print("❌ Enhanced table mapper is None - recreating...")
        enhanced_table_mapper = EnhancedTableMapper()
        print("✅ Enhanced table mapper recreated")
    
    # Test the exact query from your chat
    context = ChatContext()
    test_query = "show me the site visit details any one complaint id"
    
    print(f"\n📝 Testing query: '{test_query}'")
    
    # First test the enhanced mapper directly
    from src.core.query_agent import SCHEMA_DICT
    if 'public' in SCHEMA_DICT:
        tables = [f'public.{table}' for table in SCHEMA_DICT['public'].keys()]
        
        # Check if crm_site_visit_dtls exists
        crm_tables = [t for t in tables if 'crm_site_visit' in t.lower()]
        print(f"🔍 CRM site visit tables found: {crm_tables}")
        
        # Test enhanced mapping
        if enhanced_table_mapper:
            # First get priority tables
            priority_tables = enhanced_table_mapper.get_priority_tables(test_query)
            print(f"\n🎯 Priority tables for query: {priority_tables}")
            
            # Test fuzzy matching
            fuzzy_results = enhanced_table_mapper.fuzzy_match_tables(test_query, tables)
            print(f"\n🎯 Fuzzy match results:")
            for i, (table, score) in enumerate(fuzzy_results[:5], 1):
                print(f"   {i}. {table} (score: {score:.3f})")
                if 'crm_site_visit' in table:
                    print(f"      ✅ Found CRM site visit table!")
        
        # Test the full english_to_sql function
        print(f"\n🔧 Testing full english_to_sql function...")
        result = english_to_sql(test_query, chat_context=context)
        
        if result and result.get('sql'):
            sql_text = result['sql']
            print(f"📝 Generated SQL: {sql_text}")
            
            if 'crm_site_visit' in sql_text.lower():
                print("✅ SUCCESS: SQL uses crm_site_visit_dtls table!")
            else:
                print("❌ ISSUE: SQL does not use crm_site_visit_dtls table")
                print("🔍 Checking which table it used...")
                
                # Extract table names from SQL
                import re
                table_pattern = r'FROM\s+(\w+\.\w+|\w+)'
                matches = re.findall(table_pattern, sql_text, re.IGNORECASE)
                print(f"   Tables used in SQL: {matches}")
        else:
            print("❌ No SQL generated")
    
    print(f"\n🎯 DIAGNOSIS:")
    print(f"   Enhanced mapper available: {enhanced_table_mapper is not None}")
    print(f"   CRM tables exist: {len(crm_tables) > 0}")
    
    if enhanced_table_mapper and len(crm_tables) > 0:
        # Test priority mapping directly
        priority_result = enhanced_table_mapper.priority_mappings.get('site visit', [])
        print(f"   Priority mapping for 'site visit': {priority_result}")
        
        if 'crm_site_visit_dtls' in priority_result:
            print("✅ Priority mapping is correct")
        else:
            print("❌ Priority mapping missing or incorrect")
    
except Exception as e:
    print(f"❌ Error during debugging: {e}")
    import traceback
    traceback.print_exc()
