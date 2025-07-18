#!/usr/bin/env python3
"""
Test correct column names for geographical hierarchy queries
Specifically tests that zone_master.zone_name is used (not .name)
"""

print("🧪 Testing Correct Column Names for Geographical Queries")
print("=" * 60)

def test_geographical_query(query, expected_column_patterns):
    """Test that geographical queries use correct column names"""
    print(f"\n🔍 Testing: '{query}'")
    
    try:
        from query_agent import english_to_sql
        result = english_to_sql(query)
        
        if result and isinstance(result, dict) and 'sql' in result:
            sql = result['sql']
            print(f"✅ SQL Generated: {sql}")
            
            # Check for expected column patterns
            sql_lower = sql.lower()
            all_correct = True
            
            print(f"🔍 Checking column name patterns:")
            for pattern, description in expected_column_patterns.items():
                present = pattern.lower() in sql_lower
                print(f"  {'✅' if present else '❌'} {description}: {'Present' if present else 'MISSING'}")
                if not present:
                    all_correct = False
            
            # Check for common mistakes
            mistakes = {
                'zm.name': 'Should use zm.zone_name instead of zm.name',
                'zone_master.name': 'Should use zone_master.zone_name',
            }
            
            print(f"🚫 Checking for common mistakes:")
            has_mistakes = False
            for mistake, explanation in mistakes.items():
                if mistake.lower() in sql_lower:
                    print(f"  ❌ FOUND MISTAKE: {mistake} - {explanation}")
                    has_mistakes = True
                else:
                    print(f"  ✅ No mistake: {mistake}")
            
            if all_correct and not has_mistakes:
                print(f"🎉 ALL COLUMN NAMES CORRECT!")
                return True
            else:
                print(f"⚠️ Some column names need correction")
                return False
                
        else:
            print(f"❌ No SQL generated")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# Define test cases with expected column patterns
test_cases = [
    {
        'query': 'show me plants in gujarat',
        'expected_patterns': {
            'zm.zone_name': 'zone_master uses zone_name column',
            'hm.name': 'hosp_master uses name column',
            'dm.name': 'district_master uses name column (optional for this query)',
        },
        'description': 'Plants in zone - must use zm.zone_name'
    },
    {
        'query': 'plants in punjab region',
        'expected_patterns': {
            'dm.name': 'district_master uses name column',
            'hm.name': 'hosp_master uses name column',
        },
        'description': 'Plants in region - dm.name should be used'
    },
    {
        'query': 'vehicles in north zone',
        'expected_patterns': {
            'zm.zone_name': 'zone_master uses zone_name column',
            'vm.reg_no': 'vehicle_master uses reg_no column',
        },
        'description': 'Vehicles in zone - must use zm.zone_name'
    },
    {
        'query': 'show all zones',
        'expected_patterns': {
            'zone_name': 'Must select zone_name from zone_master',
        },
        'description': 'List zones - must use zone_name column'
    },
    {
        'query': 'show all regions',
        'expected_patterns': {
            'dm.name': 'Must select name from district_master for regions',
        },
        'description': 'List regions - must use dm.name'
    }
]

print("🚀 Running Column Name Correctness Tests...")
print("-" * 60)

all_tests_passed = True
test_results = []

for i, test_case in enumerate(test_cases, 1):
    print(f"\n{i}. {test_case['description']}")
    print(f"   Expected patterns: {list(test_case['expected_patterns'].keys())}")
    
    success = test_geographical_query(test_case['query'], test_case['expected_patterns'])
    test_results.append(success)
    
    if not success:
        all_tests_passed = False
    
    print("-" * 50)

# Final Summary
print("\n" + "=" * 60)
print("📊 COLUMN NAME CORRECTNESS RESULTS")
print("=" * 60)

for i, (test_case, result) in enumerate(zip(test_cases, test_results), 1):
    status = "✅ PASS" if result else "❌ FAIL"
    print(f"{i}. {test_case['description']}: {status}")

print("\n" + "🎯 OVERALL RESULT:")
if all_tests_passed:
    print("🎉 ALL COLUMN NAME TESTS PASSED!")
    print("✅ zone_master.zone_name is correctly used")
    print("✅ district_master.name is correctly used") 
    print("✅ hosp_master.name is correctly used")
    print("✅ vehicle_master.reg_no is correctly used")
    print("✅ No zm.name mistakes found")
else:
    print("⚠️ SOME TESTS FAILED - Column names need attention")

print("\n🔑 Key Column Name Rules:")
print("   • zone_master → zone_name (NOT name)")
print("   • district_master → name (for regions)")
print("   • hosp_master → name (for plants)")
print("   • vehicle_master → reg_no (for registration)")
print("\n✅ Test completed!")
