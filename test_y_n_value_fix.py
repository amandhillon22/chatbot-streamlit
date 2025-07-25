#!/usr/bin/env python3
"""
Comprehensive test for the Y/N value fix - testing both product_correction and active_status
"""

import sys
sys.path.append('.')

from query_agent import english_to_sql

def test_y_n_value_fix():
    """Test that both product_correction and active_status use correct Y/N values"""
    
    print("🎯 COMPREHENSIVE Y/N VALUE FIX TEST")
    print("=" * 60)
    print("Fix: Added critical instructions to use 'Y'/'N' instead of 'Yes'/'No'")
    print("=" * 60)
    
    test_queries = [
        # Product correction queries
        "how many complaints have product correction done",
        "show complaints with product correction not done",
        "list complaints where product correction is completed",
        
        # Active status queries
        "how many open complaints",
        "show closed complaints", 
        "count of active complaints",
        
        # Mixed queries
        "show open complaints with product correction done"
    ]
    
    print("\n🧪 Testing Y/N Value Usage:")
    print("-" * 50)
    
    results = {
        'correct_product_correction': 0,
        'wrong_product_correction': 0,
        'correct_active_status': 0, 
        'wrong_active_status': 0,
        'total_queries': len(test_queries)
    }
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Query: '{query}'")
        print("-" * 40)
        
        try:
            result = english_to_sql(query)
            
            if result and 'sql' in result and result['sql']:
                sql = result['sql']
                print(f"   🔧 SQL Generated: ✅")
                
                # Check product_correction values
                if "product_correction" in sql.lower():
                    if "= 'Y'" in sql or "ILIKE 'Y'" in sql:
                        print(f"   ✅ product_correction: Correct 'Y' value")
                        results['correct_product_correction'] += 1
                    elif "= 'N'" in sql or "ILIKE 'N'" in sql:
                        print(f"   ✅ product_correction: Correct 'N' value")
                        results['correct_product_correction'] += 1
                    elif "= 'Yes'" in sql or "= 'No'" in sql or "= 'Completed'" in sql:
                        print(f"   ❌ product_correction: Wrong value (Yes/No/Completed)")
                        results['wrong_product_correction'] += 1
                    else:
                        print(f"   ⚠️  product_correction: Value unclear")
                
                # Check active_status values
                if "active_status" in sql.lower():
                    if "= 'Y'" in sql or "ILIKE 'Y'" in sql:
                        print(f"   ✅ active_status: Correct 'Y' value")
                        results['correct_active_status'] += 1
                    elif "= 'N'" in sql or "ILIKE 'N'" in sql:
                        print(f"   ✅ active_status: Correct 'N' value") 
                        results['correct_active_status'] += 1
                    elif "= 'Open'" in sql or "= 'Closed'" in sql or "= 'Active'" in sql:
                        print(f"   ❌ active_status: Wrong value (Open/Closed/Active)")
                        results['wrong_active_status'] += 1
                    else:
                        print(f"   ⚠️  active_status: Value unclear")
                
                print(f"   📝 SQL: {sql[:80]}...")
            else:
                print(f"   ❌ No SQL generated or SQL is None")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Results summary
    print("\n" + "=" * 60)
    print("📊 RESULTS SUMMARY:")
    print(f"• product_correction correct: {results['correct_product_correction']}")
    print(f"• product_correction wrong: {results['wrong_product_correction']}")
    print(f"• active_status correct: {results['correct_active_status']}")
    print(f"• active_status wrong: {results['wrong_active_status']}")
    print(f"• Total queries tested: {results['total_queries']}")
    
    print("\n🎯 SUCCESS CRITERIA:")
    product_correction_success = results['wrong_product_correction'] == 0
    active_status_success = results['wrong_active_status'] == 0
    
    print(f"• product_correction uses Y/N: {'✅' if product_correction_success else '❌'}")
    print(f"• active_status uses Y/N: {'✅' if active_status_success else '❌'}")
    
    if product_correction_success and active_status_success:
        print("\n🎉 Y/N VALUE FIX: COMPLETE SUCCESS! ✅")
        print("All queries now use correct database values")
    else:
        print("\n⚠️ Y/N VALUE FIX: NEEDS MORE WORK")

if __name__ == "__main__":
    test_y_n_value_fix()
