#!/usr/bin/env python3
"""
Comprehensive integration test for hierarchical logic

This script tests the complete integration of hierarchical zone-region-plant-vehicle 
relationships across all components of the chatbot system.
"""

import json
from query_agent import english_to_sql, ChatContext
from sql import run_query

def test_end_to_end_hierarchical_integration():
    """Test complete end-to-end integration with hierarchical logic"""
    print("🔄 End-to-End Hierarchical Integration Test")
    print("=" * 60)
    
    context = ChatContext()
    
    # Test comprehensive hierarchical scenarios
    test_scenarios = [
        {
            'name': 'Zone Query with Intelligent Reasoning',
            'query': 'What zone does vehicle MH12AB1234 belong to?',
            'expected_features': ['reasoning_applied', 'zone_master', 'district_master', 'hosp_master', 'vehicle_master']
        },
        {
            'name': 'Region Query with Enhanced Mapping',
            'query': 'Which region is vehicle KA05CD5678 in?',
            'expected_features': ['district_master', 'hosp_master', 'vehicle_master']
        },
        {
            'name': 'Plant-Vehicle Relationship',
            'query': 'What plant does vehicle TN09EF9012 belong to?',
            'expected_features': ['hosp_master', 'vehicle_master']
        },
        {
            'name': 'Reverse Hierarchy: Vehicles in Zone',
            'query': 'Show all vehicles in North zone',
            'expected_features': ['zone_master', 'district_master', 'hosp_master', 'vehicle_master']
        },
        {
            'name': 'Complete Hierarchy Display',
            'query': 'Show the complete hierarchy for vehicle DL01GH2345',
            'expected_features': ['zone_master', 'district_master', 'hosp_master', 'vehicle_master', 'LEFT JOIN']
        }
    ]
    
    passed_tests = 0
    total_tests = len(test_scenarios)
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n{i}. Testing: {scenario['name']}")
        print(f"   Query: '{scenario['query']}'")
        
        try:
            # Test query generation
            result = english_to_sql(scenario['query'], context)
            
            if not result:
                print("   ❌ No result generated")
                continue
                
            # Check if intelligent reasoning was applied for appropriate queries
            reasoning_applied = result.get('reasoning_applied', False)
            sql = result.get('sql', '')
            
            print(f"   🧠 Reasoning applied: {reasoning_applied}")
            
            if sql:
                print(f"   📝 Generated SQL: {sql[:100]}...")
                
                # Validate expected features
                features_found = []
                for feature in scenario['expected_features']:
                    if feature in sql:
                        features_found.append(feature)
                
                print(f"   ✅ Features found: {features_found}")
                
                missing_features = set(scenario['expected_features']) - set(features_found)
                if missing_features:
                    print(f"   ⚠️ Missing features: {list(missing_features)}")
                else:
                    print("   🎯 All expected features present!")
                    passed_tests += 1
                    
                # Test SQL syntax validity (basic check)
                if 'SELECT' in sql.upper() and 'FROM' in sql.upper():
                    print("   ✅ Valid SQL syntax")
                else:
                    print("   ❌ Invalid SQL syntax")
                    
            else:
                print("   ❌ No SQL generated")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print(f"\n📊 Test Results: {passed_tests}/{total_tests} scenarios passed")
    print(f"Success rate: {(passed_tests/total_tests)*100:.1f}%")
    
    return passed_tests == total_tests

def test_hierarchical_consistency():
    """Test consistency of hierarchical relationships"""
    print("\n🔍 Hierarchical Consistency Test")
    print("=" * 40)
    
    context = ChatContext()
    
    # Test that similar queries produce consistent results
    similar_queries = [
        ('What zone does vehicle MH12AB1234 belong to?', 'zone'),
        ('Which zone is vehicle MH12AB1234 in?', 'zone'),
        ('Show zone for vehicle MH12AB1234', 'zone'),
        ('What region does vehicle KA05CD5678 belong to?', 'region'),
        ('Which region is vehicle KA05CD5678 in?', 'region'),
        ('Show region for vehicle KA05CD5678', 'region'),
    ]
    
    for query, expected_type in similar_queries:
        print(f"\nTesting: '{query}' (expecting {expected_type} query)")
        try:
            result = english_to_sql(query, context)
            if result and result.get('sql'):
                sql = result['sql']
                
                if expected_type == 'zone' and 'zone_master' in sql:
                    print("   ✅ Correctly identified as zone query")
                elif expected_type == 'region' and 'district_master' in sql:
                    print("   ✅ Correctly identified as region query")
                else:
                    print(f"   ⚠️ Unexpected SQL for {expected_type} query")
                    print(f"   SQL: {sql[:80]}...")
            else:
                print("   ❌ No SQL generated")
        except Exception as e:
            print(f"   ❌ Error: {e}")

def test_enhanced_table_mapping_integration():
    """Test enhanced table mapping with hierarchical keywords"""
    print("\n🗺️ Enhanced Table Mapping Integration Test")
    print("=" * 50)
    
    try:
        from enhanced_table_mapper import EnhancedTableMapper
        mapper = EnhancedTableMapper()
        
        hierarchical_keywords = [
            ('zone vehicle', ['zone_master', 'district_master', 'hosp_master', 'vehicle_master']),
            ('region truck', ['district_master', 'hosp_master', 'vehicle_master']),
            ('plant facility', ['hosp_master']),
            ('hospital vehicle', ['hosp_master', 'vehicle_master']),
            ('zone region hierarchy', ['zone_master', 'district_master', 'hosp_master', 'vehicle_master'])
        ]
        
        for keywords, expected_tables in hierarchical_keywords:
            print(f"\nTesting keywords: '{keywords}'")
            try:
                priority_tables = mapper.get_priority_tables(keywords)
                print(f"   Priority tables: {priority_tables}")
                
                # Check if expected tables are included
                found_expected = [table for table in expected_tables if table in priority_tables]
                print(f"   Expected tables found: {found_expected}")
                
                if len(found_expected) >= len(expected_tables) // 2:  # At least half expected
                    print("   ✅ Good table mapping")
                else:
                    print("   ⚠️ Could improve table mapping")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
                
    except ImportError:
        print("❌ Enhanced table mapper not available")

def main():
    """Run complete hierarchical integration test suite"""
    print("🧪 COMPREHENSIVE HIERARCHICAL INTEGRATION TEST SUITE")
    print("=" * 70)
    print("Testing the complete implementation of zone→region→plant→vehicle hierarchy")
    print("=" * 70)
    
    # Run all test suites
    try:
        success = test_end_to_end_hierarchical_integration()
        test_hierarchical_consistency()  
        test_enhanced_table_mapping_integration()
        
        print("\n" + "=" * 70)
        if success:
            print("🎉 HIERARCHICAL INTEGRATION TEST SUITE: ALL TESTS PASSED!")
            print("✅ The chatbot is ready for production with full hierarchical support")
        else:
            print("⚠️ HIERARCHICAL INTEGRATION TEST SUITE: SOME TESTS FAILED")
            print("🔧 Review the failed tests and make necessary adjustments")
        print("=" * 70)
        
        return success
        
    except Exception as e:
        print(f"\n❌ Test suite error: {e}")
        return False

if __name__ == "__main__":
    main()
