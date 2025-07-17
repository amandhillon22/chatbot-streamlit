#!/usr/bin/env python3
"""
Test script to validate the enhanced table mapping system
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import query_agent
from enhanced_table_mapper import EnhancedTableMapper

def test_enhanced_table_mapping():
    """Test the enhanced table mapping system with domain-specific queries"""
    print("🚀 Testing Enhanced Table Mapping System")
    print("=" * 60)
    
    # Initialize the mapper
    mapper = EnhancedTableMapper()
    
    # Get tables from SCHEMA_DICT
    if 'public' in query_agent.SCHEMA_DICT:
        tables = [f'public.{table}' for table in query_agent.SCHEMA_DICT['public'].keys()]
        print(f"📊 Available tables: {len(tables)}")
        
        # Find tables with 'site' or 'visit' in name for reference
        site_visit_tables = [t for t in tables if 'site' in t.lower() or 'visit' in t.lower()]
        complaint_tables = [t for t in tables if 'complaint' in t.lower()]
        maintenance_tables = [t for t in tables if 'maintenance' in t.lower()]
        vehicle_tables = [t for t in tables if 'vehicle' in t.lower() or 'veh' in t.lower()]
        
        print(f"🎯 Reference - Site/Visit tables: {site_visit_tables}")
        print(f"🎯 Reference - Complaint tables: {complaint_tables}")
        print(f"🎯 Reference - Maintenance tables: {maintenance_tables}")
        print(f"🎯 Reference - Vehicle tables: {vehicle_tables[:5]}...")  # Show first 5
        print()
        
        # Test specific domain queries
        test_queries = [
            'site visit',
            'show me the site visit details',
            'site visit details of complaint',
            'complaint details',
            'maintenance records',
            'vehicle information',
            'plant details',
            'driver information',
            'route details'
        ]
        
        print("🧪 Testing Domain-Specific Queries:")
        print("-" * 40)
        
        for query in test_queries:
            print(f"\n📝 Query: '{query}'")
            best_tables = mapper.find_best_tables(query, tables, top_k=5)
            
            # Show top 3 results with scores
            print(f"   Top tables:")
            for i, (table, score, match_type) in enumerate(best_tables[:3], 1):
                print(f"   {i}. {table} (score: {score:.3f}, type: {match_type})")
                
            # Validate specific queries
            if 'site visit' in query.lower():
                if any('crm_site_visit' in table for table, _, _ in best_tables[:3]):
                    print("   ✅ CORRECT: Found crm_site_visit_dtls in top 3")
                else:
                    print("   ❌ ISSUE: crm_site_visit_dtls not in top 3")
                    
            elif 'complaint' in query.lower():
                if any('complaint' in table for table, _, _ in best_tables[:3]):
                    print("   ✅ CORRECT: Found complaint table in top 3")
                else:
                    print("   ❌ ISSUE: No complaint table in top 3")
                    
            elif 'maintenance' in query.lower():
                if any('maintenance' in table for table, _, _ in best_tables[:3]):
                    print("   ✅ CORRECT: Found maintenance table in top 3")
                else:
                    print("   ❌ ISSUE: No maintenance table in top 3")
                    
            elif 'vehicle' in query.lower():
                if any('vehicle' in table or 'veh' in table for table, _, _ in best_tables[:3]):
                    print("   ✅ CORRECT: Found vehicle-related table in top 3")
                else:
                    print("   ❌ ISSUE: No vehicle table in top 3")
    
    print("\n" + "=" * 60)
    print("✅ Enhanced Table Mapping Test Complete!")

def test_ordinal_integration():
    """Test integration of ordinal references with enhanced table mapping"""
    print("\n🔗 Testing Ordinal Reference Integration")
    print("=" * 60)
    
    # Initialize chat context
    context = query_agent.ChatContext()
    
    # Simulate storing some results
    test_data = [
        {'complaint_id': 'C001', 'site_visit_id': 'SV001', 'status': 'Pending'},
        {'complaint_id': 'C002', 'site_visit_id': 'SV002', 'status': 'Resolved'},
        {'complaint_id': 'C003', 'site_visit_id': 'SV003', 'status': 'In Progress'}
    ]
    
    context.store_results(
        results=test_data,
        columns=['complaint_id', 'site_visit_id', 'status'],
        original_question="Show me all complaints with site visits"
    )
    
    print(f"📊 Stored {len(test_data)} items in context")
    
    # Test ordinal reference
    ordinal_query = "Show me details of the 2nd complaint"
    
    # Check if ordinal reference is detected
    is_ordinal = query_agent.is_ordinal_reference(ordinal_query)
    print(f"🔍 Is ordinal reference: {is_ordinal}")
    
    if is_ordinal:
        ordinal_info = query_agent.extract_ordinal_reference(ordinal_query)
        print(f"📋 Ordinal info: {ordinal_info}")
        
        # Get referenced item
        referenced_item = context.get_item_by_ordinal(ordinal_info['position'], ordinal_info['entity'])
        print(f"🎯 Referenced item: {referenced_item}")
        
        # Test enhanced prompt
        enhanced_prompt = query_agent.enhance_prompt_with_ordinal(ordinal_query, context)
        print(f"✨ Enhanced prompt: {enhanced_prompt}")
    
    print("✅ Ordinal Integration Test Complete!")

if __name__ == "__main__":
    try:
        test_enhanced_table_mapping()
        test_ordinal_integration()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
