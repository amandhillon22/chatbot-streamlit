#!/usr/bin/env python3
"""
import sys
sys.path.append('/home/linux/Documents/chatbot-diya')

Debug the table name matching issue
"""

import os
os.chdir('/home/linux/Documents/chatbot-diya')

try:
    from src.core.query_agent import SCHEMA_DICT
    from src.nlp.enhanced_table_mapper import EnhancedTableMapper
    
    # Get available tables in the format used by the system
    if 'public' in SCHEMA_DICT:
        available_tables = [f'public.{table}' for table in SCHEMA_DICT['public'].keys()]
    
    mapper = EnhancedTableMapper()
    query = "show me the site visit details any one complaint id"
    
    print("🔍 DEBUGGING TABLE NAME MATCHING")
    print("=" * 50)
    
    # Check priority results
    priority_tables = mapper.get_priority_tables(query)
    print(f"Priority tables returned: {priority_tables}")
    
    # Check if any of these exist in available_tables
    print(f"\nChecking if priority tables exist in available_tables:")
    for priority_table in priority_tables:
        # Check exact match
        exact_match = priority_table in available_tables
        
        # Check with public. prefix
        public_match = f'public.{priority_table}' in available_tables
        
        print(f"  {priority_table}:")
        print(f"    Exact match: {exact_match}")
        print(f"    With public prefix: {public_match}")
        
        if public_match:
            print(f"    ✅ Found: public.{priority_table}")
    
    # Check if crm_site_visit_dtls specifically exists
    crm_variants = [
        'crm_site_visit_dtls',
        'public.crm_site_visit_dtls'
    ]
    
    print(f"\n🎯 Checking CRM site visit table variants:")
    for variant in crm_variants:
        exists = variant in available_tables
        print(f"  {variant}: {exists}")
    
    # Find all tables with 'site' and 'visit' in the name
    site_visit_tables = [t for t in available_tables if 'site' in t.lower() and 'visit' in t.lower()]
    print(f"\n📊 All site visit tables found: {site_visit_tables}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
