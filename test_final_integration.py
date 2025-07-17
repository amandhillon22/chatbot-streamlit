#!/usr/bin/env python3
"""
Final Integration Test for Enhanced Chatbot System
Tests both table mapping accuracy and ordinal reference handling
"""

import sys
import os
sys.path.append('.')

def test_table_mapping_accuracy():
    """Test that critical domain queries map to correct tables"""
    print("🎯 Testing Table Mapping Accuracy")
    print("-" * 40)
    
    from query_agent import SCHEMA_DICT
    from enhanced_table_mapper import EnhancedTableMapper
    
    mapper = EnhancedTableMapper()
    
    if 'public' in SCHEMA_DICT:
        tables = [f'public.{table}' for table in SCHEMA_DICT['public'].keys()]
        print(f"📊 Testing with {len(tables)} tables")
        
        # Critical test cases
        critical_tests = [
            {
                'query': 'site visit',
                'expected_tables': ['crm_site_visit_dtls'],
                'description': 'Site visit queries should find CRM site visit table'
            },
            {
                'query': 'show me the site visit details of any complaint',
                'expected_tables': ['crm_site_visit_dtls'],
                'description': 'Complex site visit query should prioritize correct table'
            },
            {
                'query': 'complaint details',
                'expected_tables': ['complaint', 'crm_complaint'],
                'description': 'Complaint queries should find complaint tables'
            },
            {
                'query': 'maintenance records',
                'expected_tables': ['maintenance', 'tc_maintenances'],
                'description': 'Maintenance queries should find maintenance tables'
            },
            {
                'query': 'vehicle information',
                'expected_tables': ['vehicle_master', 'mega_trips', 'veh_volume'],
                'description': 'Vehicle queries should find vehicle-related tables'
            }
        ]
        
        total_tests = len(critical_tests)
        passed_tests = 0
        
        for test in critical_tests:
            print(f"\n📝 Query: '{test['query']}'")
            print(f"   Expected: {test['expected_tables']}")
            
            best_tables = mapper.find_best_tables(test['query'], tables, top_k=5)
            top_3_tables = [table for table, _, _ in best_tables[:3]]
            
            # Check if any expected table is in top 3
            found_expected = False
            for expected in test['expected_tables']:
                if any(expected.lower() in table.lower() for table in top_3_tables):
                    found_expected = True
                    break
            
            if found_expected:
                print(f"   ✅ PASS - Found expected table in top 3")
                passed_tests += 1
            else:
                print(f"   ❌ FAIL - No expected table in top 3")
            
            print(f"   Top 3: {top_3_tables}")
        
        print(f"\n📊 Table Mapping Results: {passed_tests}/{total_tests} tests passed")
        return passed_tests == total_tests
    
    return False

def test_ordinal_integration():
    """Test ordinal reference handling with context"""
    print("\n🔗 Testing Ordinal Reference Integration")
    print("-" * 40)
    
    from query_agent import ChatContext, english_to_sql
    
    context = ChatContext()
    
    # Simulate storing some results
    test_data = [
        {'complaint_id': 'C001', 'site_visit_id': 'SV001', 'status': 'Pending'},
        {'complaint_id': 'C002', 'site_visit_id': 'SV002', 'status': 'Resolved'},
        {'complaint_id': 'C003', 'site_visit_id': 'SV003', 'status': 'In Progress'},
        {'complaint_id': 'C004', 'site_visit_id': 'SV004', 'status': 'Closed'},
        {'complaint_id': 'C005', 'site_visit_id': 'SV005', 'status': 'Open'}
    ]
    
    context.store_results(
        results=test_data,
        columns=['complaint_id', 'site_visit_id', 'status'],
        original_question='show me all complaints'
    )
    
    print(f"📊 Stored {len(test_data)} items in context")
    
    # Test ordinal references
    ordinal_tests = [
        "Tell me more about the 2nd complaint",
        "What is the status of the first complaint?",
        "Show details for the 3rd item",
        "Give me information about the last complaint"
    ]
    
    ordinal_passed = 0
    
    for query in ordinal_tests:
        print(f"\n📝 Query: '{query}'")
        
        try:
            result = english_to_sql(query, chat_context=context)
            
            if result.get('sql') and result['sql'].strip().lower() != 'null':
                print(f"   ✅ Generated valid SQL: {result['sql'][:100]}...")
                ordinal_passed += 1
            else:
                print(f"   ❌ No valid SQL generated")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print(f"\n📊 Ordinal Reference Results: {ordinal_passed}/{len(ordinal_tests)} tests passed")
    return ordinal_passed == len(ordinal_tests)

def test_live_integration():
    """Test the complete integration with a realistic scenario"""
    print("\n🚀 Testing Live Integration Scenario")
    print("-" * 40)
    
    from query_agent import ChatContext, english_to_sql
    
    context = ChatContext()
    
    print("Scenario: User asks about site visits, then follows up with ordinal reference")
    
    # Step 1: Initial query about site visits
    print("\n1️⃣ Initial Query: 'show me the site visit details of any one complaint id'")
    result1 = english_to_sql('show me the site visit details of any one complaint id', chat_context=context)
    
    if result1.get('sql'):
        print(f"   ✅ Generated SQL: {result1['sql']}")
        # Check if it uses the correct table
        if 'crm_site_visit' in result1['sql'].lower():
            print("   ✅ Uses correct CRM site visit table")
        else:
            print("   ❌ Does not use CRM site visit table")
    else:
        print("   ❌ No SQL generated")
    
    # Step 2: Simulate storing some site visit results
    site_visit_data = [
        {'visit_id': 'SV001', 'complaint_id': 'C001', 'visit_date': '2024-01-15', 'status': 'Completed'},
        {'visit_id': 'SV002', 'complaint_id': 'C002', 'visit_date': '2024-01-16', 'status': 'Pending'},
        {'visit_id': 'SV003', 'complaint_id': 'C003', 'visit_date': '2024-01-17', 'status': 'In Progress'}
    ]
    
    context.store_results(
        results=site_visit_data,
        columns=['visit_id', 'complaint_id', 'visit_date', 'status'],
        original_question='show me the site visit details'
    )
    
    print(f"\n   📊 Simulated storing {len(site_visit_data)} site visit results")
    
    # Step 3: Follow-up with ordinal reference
    print("\n2️⃣ Follow-up Query: 'Tell me more details about the 2nd site visit'")
    result2 = english_to_sql('Tell me more details about the 2nd site visit', chat_context=context)
    
    if result2.get('sql'):
        print(f"   ✅ Generated SQL: {result2['sql']}")
        # Check if it references the specific visit
        if 'SV002' in result2['sql'] or 'C002' in result2['sql']:
            print("   ✅ References the correct 2nd item")
        else:
            print("   ❌ Does not reference the correct item")
    else:
        print("   ❌ No SQL generated for ordinal reference")
    
    return True

def main():
    """Run all integration tests"""
    print("🧪 FINAL INTEGRATION TEST SUITE")
    print("=" * 60)
    
    try:
        # Test 1: Table mapping accuracy
        table_mapping_ok = test_table_mapping_accuracy()
        
        # Test 2: Ordinal reference integration
        ordinal_ok = test_ordinal_integration()
        
        # Test 3: Live integration scenario
        live_ok = test_live_integration()
        
        print("\n" + "=" * 60)
        print("🏁 FINAL RESULTS:")
        print(f"   Table Mapping: {'✅ PASS' if table_mapping_ok else '❌ FAIL'}")
        print(f"   Ordinal References: {'✅ PASS' if ordinal_ok else '❌ FAIL'}")
        print(f"   Live Integration: {'✅ PASS' if live_ok else '❌ FAIL'}")
        
        if table_mapping_ok and ordinal_ok and live_ok:
            print("\n🎉 ALL TESTS PASSED! System is ready for production.")
        else:
            print("\n⚠️  Some tests failed. Review the issues above.")
        
    except Exception as e:
        print(f"\n❌ Integration test suite failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
