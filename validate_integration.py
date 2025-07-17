#!/usr/bin/env python3
"""Simple validation script"""
print("✅ Script started")

try:
    import os
    print(f"📁 Working directory: {os.getcwd()}")
    
    import sys
    print(f"🐍 Python path: {sys.executable}")
    
    print("📦 Testing imports...")
    
    # Test basic imports
    from dotenv import load_dotenv
    print("✅ dotenv imported")
    
    load_dotenv()
    print("✅ Environment loaded")
    
    # Test SQL connection
    from sql import get_connection
    print("✅ sql module imported")
    
    # Test query agent
    from query_agent import ChatContext, english_to_sql
    print("✅ query_agent imported")
    
    # Test enhanced mapper
    from enhanced_table_mapper import EnhancedTableMapper
    print("✅ enhanced_table_mapper imported")
    
    print("\n🧪 Testing basic functionality...")
    
    # Create instances
    context = ChatContext()
    mapper = EnhancedTableMapper()
    print("✅ Objects created")
    
    # Test a simple query
    result = english_to_sql("test query", chat_context=context)
    print(f"✅ Basic query result: {type(result)}")
    
    # Test the critical site visit query
    site_visit_result = english_to_sql("show me the site visit details of any one complaint id", chat_context=context)
    
    if site_visit_result and site_visit_result.get('sql'):
        sql_text = site_visit_result['sql'].lower()
        print(f"\n🎯 Site visit query SQL: {site_visit_result['sql'][:200]}...")
        
        if 'crm_site_visit' in sql_text:
            print("✅ CRITICAL SUCCESS: Uses CRM site visit table!")
        else:
            print("❌ ISSUE: Does not use CRM site visit table")
            print(f"   Full SQL: {site_visit_result['sql']}")
    else:
        print("❌ No SQL generated for site visit query")
    
    print("\n🎉 Integration validation completed!")
    
except Exception as e:
    print(f"❌ Error during validation: {e}")
    import traceback
    traceback.print_exc()
