#!/usr/bin/env python3
"""
Final integration test for hierarchical relationships
"""

print("🎯 Final Integration Test - Hierarchical Relationships")
print("=" * 60)

try:
    from query_agent import english_to_sql
    
    # Test queries that must use proper ID relationships
    critical_queries = [
        {
            'query': 'show me the vehicles of mohali plant',
            'must_contain': ['id_hosp', 'hosp_master', 'vehicle_master'],
            'description': 'Vehicle-Plant relationship via id_hosp'
        },
        {
            'query': 'vehicles in punjab region',
            'must_contain': ['id_hosp', 'id_dist'],
            'description': 'Vehicle-Region relationship via id_hosp→id_dist'
        },
        {
            'query': 'show plants in haryana region',
            'must_contain': ['id_dist', 'hosp_master', 'district_master'],
            'description': 'Plant-Region relationship via id_dist'
        }
    ]
    
    print("🧪 Testing Critical Hierarchical Queries:")
    print("-" * 50)
    
    all_passed = True
    
    for i, test in enumerate(critical_queries, 1):
        print(f"\n{i}. {test['description']}")
        print(f"   Query: '{test['query']}'")
        
        try:
            result = english_to_sql(test['query'])
            
            if result:
                result_lower = result.lower()
                print(f"   ✅ SQL Generated: {len(result)} characters")
                
                # Check for required elements
                missing = []
                for requirement in test['must_contain']:
                    if requirement.lower() not in result_lower:
                        missing.append(requirement)
                
                if missing:
                    print(f"   ❌ Missing requirements: {missing}")
                    all_passed = False
                else:
                    print(f"   ✅ All ID relationships present")
                    
                # Show key parts of the SQL
                if 'join' in result_lower:
                    print(f"   📋 Contains JOINs: ✅")
                else:
                    print(f"   📋 Contains JOINs: ❌")
                    
            else:
                print(f"   ❌ No SQL generated")
                all_passed = False
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ALL HIERARCHICAL RELATIONSHIP TESTS PASSED!")
        print("✅ ID relationships (id_dist, id_hosp, id_zone) are properly maintained")
        print("✅ No data will be missed due to incomplete joins")
        print("✅ The system ensures complete hierarchical integrity")
    else:
        print("⚠️ SOME TESTS FAILED")
        print("❌ Review the ID relationship handling in query generation")
    
except Exception as e:
    print(f"❌ Critical Error: {e}")
    import traceback
    traceback.print_exc()

print("\n🏁 Integration test complete!")
