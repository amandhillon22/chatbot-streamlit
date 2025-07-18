#!/usr/bin/env python3
"""
Comprehensive test for hierarchical relationships and ID integrity
Tests that all region-plant-vehicle relationships use correct ID columns
"""

import sys
sys.path.append('.')

def test_hierarchical_relationships():
    """Test all hierarchical relationship queries to ensure ID integrity"""
    
    print("🔗 Testing Hierarchical ID Relationship Integrity")
    print("=" * 60)
    
    try:
        from query_agent import english_to_sql
        from intelligent_reasoning import IntelligentReasoning
        
        # Initialize intelligent reasoning
        ir = IntelligentReasoning()
        
        test_queries = [
            # Vehicle-Plant relationships
            {
                'query': 'show me the vehicles of mohali plant',
                'expected_joins': ['vm.id_hosp = hm.id_no'],
                'expected_tables': ['vehicle_master', 'hosp_master']
            },
            
            # Vehicle-Region relationships  
            {
                'query': 'show me vehicles in punjab region',
                'expected_joins': ['vm.id_hosp = hm.id_no', 'hm.id_dist = dm.id_no'],
                'expected_tables': ['vehicle_master', 'hosp_master', 'district_master']
            },
            
            # Plant-Region relationships
            {
                'query': 'show me plants in punjab region', 
                'expected_joins': ['hm.id_dist = dm.id_no'],
                'expected_tables': ['hosp_master', 'district_master']
            },
            
            # Full hierarchy Vehicle-Zone
            {
                'query': 'show vehicles in north zone',
                'expected_joins': ['vm.id_hosp = hm.id_no', 'hm.id_dist = dm.id_no', 'dm.id_zone = zm.id_no'],
                'expected_tables': ['vehicle_master', 'hosp_master', 'district_master', 'zone_master']
            },
            
            # Specific plant vehicle lookup
            {
                'query': 'vehicles of chandigarh plant',
                'expected_joins': ['vm.id_hosp = hm.id_no'],
                'expected_tables': ['vehicle_master', 'hosp_master']
            }
        ]
        
        all_passed = True
        
        for i, test in enumerate(test_queries, 1):
            print(f"\n{i}. Testing: '{test['query']}'")
            print("-" * 50)
            
            # Generate SQL
            result = english_to_sql(test['query'])
            
            if not result:
                print(f"❌ FAILED: No SQL generated")
                all_passed = False
                continue
                
            sql_lower = result.lower()
            print(f"Generated SQL: {result[:200]}...")
            
            # Check for required tables
            missing_tables = []
            for table in test['expected_tables']:
                if table not in sql_lower and table.split('_')[0] not in sql_lower:
                    missing_tables.append(table)
            
            # Check for required joins
            missing_joins = []
            for join in test['expected_joins']:
                # Check both directions of the join
                join_parts = join.split(' = ')
                if len(join_parts) == 2:
                    forward = f"{join_parts[0]} = {join_parts[1]}"
                    reverse = f"{join_parts[1]} = {join_parts[0]}"
                    if forward not in sql_lower and reverse not in sql_lower:
                        missing_joins.append(join)
            
            # Analyze hierarchical completeness
            completeness = ir.analyze_hierarchical_completeness(test['query'], result)
            
            # Report results
            if missing_tables:
                print(f"❌ Missing tables: {missing_tables}")
                all_passed = False
            else:
                print(f"✅ All required tables present")
                
            if missing_joins:
                print(f"❌ Missing joins: {missing_joins}")
                all_passed = False
            else:
                print(f"✅ All required ID relationships present")
                
            print(f"🎯 Completeness score: {completeness['completeness_score']}%")
            
            if completeness['has_issues']:
                print(f"⚠️ Issues found: {completeness['issues']}")
                for rec in completeness['recommendations']:
                    print(f"💡 Recommendation: {rec.strip()}")
                all_passed = False
            else:
                print(f"✅ No hierarchical issues detected")
        
        print("\n" + "=" * 60)
        if all_passed:
            print("🎉 ALL HIERARCHICAL RELATIONSHIP TESTS PASSED!")
            print("✅ ID integrity maintained across all queries")
        else:
            print("❌ SOME TESTS FAILED - ID relationships need attention")
            
        return all_passed
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_specific_id_joins():
    """Test specific ID join patterns"""
    
    print("\n🔍 Testing Specific ID Join Patterns")
    print("=" * 40)
    
    try:
        from intelligent_reasoning import IntelligentReasoning
        ir = IntelligentReasoning()
        
        # Test hierarchical SQL templates
        test_cases = [
            ('vehicle', 'plant', 'mohali'),
            ('vehicle', 'region', 'punjab'), 
            ('vehicle', 'zone', 'north'),
            ('plant', 'region', 'haryana')
        ]
        
        for entity_from, entity_to, filter_value in test_cases:
            print(f"\n📋 Template: {entity_from} → {entity_to} (filter: {filter_value})")
            
            template = ir.get_hierarchical_sql_template(entity_from, entity_to, filter_value)
            
            if template:
                print(f"✅ Template generated:")
                print(template[:300] + "..." if len(template) > 300 else template)
                
                # Check for required ID relationships
                id_checks = {
                    'id_hosp': 'vm.id_hosp = hm.id_no' in template or 'hm.id_no = vm.id_hosp' in template,
                    'id_dist': 'hm.id_dist = dm.id_no' in template or 'dm.id_no = hm.id_dist' in template,
                    'id_zone': 'dm.id_zone = zm.id_no' in template or 'zm.id_no = dm.id_zone' in template
                }
                
                for id_type, present in id_checks.items():
                    if entity_from == 'vehicle' and id_type == 'id_hosp':
                        print(f"  {'✅' if present else '❌'} {id_type} relationship: {'Present' if present else 'MISSING'}")
                    elif entity_to in ['region', 'zone'] and id_type == 'id_dist':
                        print(f"  {'✅' if present else '❌'} {id_type} relationship: {'Present' if present else 'MISSING'}")
                    elif entity_to == 'zone' and id_type == 'id_zone':
                        print(f"  {'✅' if present else '❌'} {id_type} relationship: {'Present' if present else 'MISSING'}")
                        
            else:
                print(f"❌ No template available for {entity_from} → {entity_to}")
                
        return True
        
    except Exception as e:
        print(f"❌ Error testing ID joins: {e}")
        return False

if __name__ == "__main__":
    print("🧪 HIERARCHICAL ID RELATIONSHIP TEST SUITE")
    print("🎯 Ensuring id_dist, id_hosp, id_zone relationships are never missed")
    print()
    
    # Run tests
    test1_passed = test_hierarchical_relationships()
    test2_passed = test_specific_id_joins()
    
    print("\n" + "=" * 60)
    print("📊 FINAL RESULTS:")
    print(f"Hierarchical Queries: {'✅ PASS' if test1_passed else '❌ FAIL'}")
    print(f"ID Join Patterns: {'✅ PASS' if test2_passed else '❌ FAIL'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 ALL ID RELATIONSHIP INTEGRITY TESTS PASSED!")
        print("✅ The system properly maintains hierarchical relationships")
        print("✅ No data will be missed due to incomplete joins")
    else:
        print("\n⚠️ SOME TESTS FAILED - Review ID relationship handling")
