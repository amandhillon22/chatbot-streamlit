#!/usr/bin/env python3
"""
Comprehensive Distance Conversion Test
Tests specific conversion scenarios and edge cases.
"""

from query_agent_enhanced import english_to_sql

def test_specific_conversions():
    """Test specific distance conversion scenarios."""
    
    print("🎯 Testing Specific Distance Conversion Scenarios")
    print("=" * 60)
    
    # Test cases with expected behavior
    test_cases = [
        {
            "query": "Total distance from trip_report in kilometers",
            "expect_conversion": True,
            "expect_sql": True,
            "description": "Should convert meters to km for trip_report"
        },
        {
            "query": "Show pump trip cycle_km",
            "expect_conversion": False,
            "expect_sql": True,
            "description": "Should use cycle_km as-is (already in km)"
        },
        {
            "query": "Average total_distance_travelled in km from trip_report",
            "expect_conversion": True,
            "expect_sql": True,
            "description": "Should convert and average"
        },
        {
            "query": "Vehicle with highest mileage",
            "expect_conversion": False,
            "expect_sql": True,
            "description": "Mileage should be used as-is (already in km)"
        },
        {
            "query": "Sum of distance_m from daily_report in kilometers",
            "expect_conversion": True,
            "expect_sql": True,
            "description": "Should convert distance_m to km"
        }
    ]
    
    passed = 0
    total = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        query = test_case["query"]
        expect_conversion = test_case["expect_conversion"]
        expect_sql = test_case["expect_sql"]
        description = test_case["description"]
        
        print(f"\n🧪 Test {i}: {description}")
        print(f"Query: '{query}'")
        print("-" * 50)
        
        try:
            result = english_to_sql(query)
            sql = result.get('sql', '')
            response = result.get('response', '')
            
            # Check if SQL was generated
            if expect_sql and sql:
                print(f"✅ SQL Generated: {sql}")
                
                # Check conversion detection
                has_conversion = 'ROUND(' in sql and '/ 1000' in sql
                if expect_conversion and has_conversion:
                    print("✅ Conversion detected as expected")
                    passed += 1
                elif not expect_conversion and not has_conversion:
                    print("✅ No conversion (as expected)")
                    passed += 1
                elif expect_conversion and not has_conversion:
                    print("⚠️  Expected conversion but not found")
                else:
                    print("⚠️  Unexpected conversion found")
                    
            elif expect_sql and not sql:
                print(f"❌ Expected SQL but got: {response}")
            elif not expect_sql and not sql:
                print(f"✅ No SQL generated (as expected): {response}")
                passed += 1
            else:
                print(f"✅ Unexpected result: {response}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\n🎯 Test Results: {passed}/{total} passed")
    
    # Test edge cases
    print(f"\n🔬 Testing Edge Cases")
    print("-" * 30)
    
    edge_cases = [
        "Show distance in both meters and kilometers",
        "Convert all distances to kilometers",
        "What's the distance in miles?",  # Should handle gracefully
    ]
    
    for query in edge_cases:
        print(f"\n🔍 Edge Case: '{query}'")
        try:
            result = english_to_sql(query)
            if result.get('sql'):
                print(f"SQL: {result['sql']}")
            else:
                print(f"Response: {result.get('response', 'No response')}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_specific_conversions()
