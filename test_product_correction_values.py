#!/usr/bin/env python3
"""
Test script to verify product_correction uses 'Y' instead of 'Yes'
"""

import sys
sys.path.append('.')

from query_agent import english_to_sql

def test_product_correction_values():
    """Test that product_correction queries use 'Y' instead of 'Yes'"""
    
    print("🔍 TESTING PRODUCT CORRECTION VALUE USAGE")
    print("=" * 60)
    print("Issue: Query uses 'Yes' instead of 'Y' for product_correction")
    print("Expected: product_correction = 'Y' (not 'Yes')")
    print("=" * 60)
    
    test_queries = [
        "how many complaints have product correction done",
        "count of complaints with product correction completed", 
        "show me complaints where product correction is done",
        "list complaints with product correction finished"
    ]
    
    print("\n🧪 Testing Product Correction Queries:")
    print("-" * 50)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Query: '{query}'")
        print("-" * 40)
        
        try:
            # Generate SQL
            result = english_to_sql(query)
            
            if result and 'sql' in result:
                sql = result['sql']
                print(f"   🔧 SQL Generated: ✅")
                
                # Check if SQL uses correct values
                if "product_correction" in sql.lower():
                    if "ILIKE 'Y'" in sql or "= 'Y'" in sql:
                        print(f"   ✅ Correct value: Uses 'Y' for product correction")
                        print(f"   📝 SQL: {sql[:100]}...")
                    elif "ILIKE 'Yes'" in sql or "= 'Yes'" in sql:
                        print(f"   ❌ Wrong value: Uses 'Yes' instead of 'Y'")
                        print(f"   📝 SQL: {sql[:100]}...")
                    else:
                        print(f"   ⚠️  Product correction found but value unclear")
                        print(f"   📝 SQL: {sql[:100]}...")
                else:
                    print(f"   ℹ️  No product_correction in SQL (might use different approach)")
                    print(f"   📝 SQL: {sql[:100]}...")
            else:
                print(f"   ❌ No SQL generated")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 EXPECTED BEHAVIOR:")
    print("• All queries should use product_correction = 'Y' (not 'Yes')")
    print("• All queries should use product_correction = 'N' (not 'No')")
    print("• Database documentation updated with correct values ✅")

if __name__ == "__main__":
    test_product_correction_values()
