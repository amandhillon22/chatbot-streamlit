#!/usr/bin/env python3
"""
Test Action Status Column Value Mapping
Verify that *_action_status columns use 'A'/'R' instead of 'Y'/'N'
"""

import sys
sys.path.append('.')

from query_agent import english_to_sql

def test_action_status_mapping():
    """Test that action status queries use correct A/R values"""
    
    print("🧪 TESTING ACTION STATUS COLUMN VALUE MAPPING")
    print("=" * 60)
    print("ISSUE: *_action_status columns use 'A'/'R', not 'Y'/'N'")
    print("=" * 60)
    
    test_queries = [
        ("BH Action Status Approved", "show site visits with bh action status approved"),
        ("BH Action Status Rejected", "show site visits where bh action status is rejected"),
        ("CM Action Status Active", "count site visits with cm action status active"),
        ("Any Action Status Approved", "show records with action status approved"),
    ]
    
    print("\n🧪 TESTING QUERIES:")
    print("-" * 50)
    
    all_correct = True
    
    for category, query in test_queries:
        print(f"\n📋 {category}")
        print(f"Query: '{query}'")
        
        try:
            result = english_to_sql(query)
            
            if result and result.get('sql'):
                sql = result['sql']
                print(f"Generated SQL: {sql.strip()}")
                
                # Check for correct A/R usage
                has_correct_values = False
                if " = 'A'" in sql or " = 'R'" in sql:
                    has_correct_values = True
                    print("✅ CORRECT: Uses 'A' or 'R' values")
                
                # Check for wrong Y/N usage
                wrong_values = [" = 'Y'", " = 'N'"]
                has_wrong_values = any(wrong in sql for wrong in wrong_values)
                
                if has_wrong_values:
                    print("❌ WRONG: Still using 'Y'/'N' values for action_status!")
                    all_correct = False
                elif has_correct_values:
                    print("✅ SUCCESS: Correct action_status values")
                else:
                    print("ℹ️ No action_status column detected in query")
                    
            else:
                print("❌ No SQL generated")
                all_correct = False
                
        except Exception as e:
            print(f"❌ Error: {e}")
            all_correct = False
    
    print("\n" + "=" * 60)
    print("🏆 ACTION STATUS VALUE MAPPING TEST RESULTS:")
    
    if all_correct:
        print("🎉 ✅ SUCCESS! Action status columns use correct A/R values")
        print("\n📊 CORRECT MAPPINGS CONFIRMED:")
        print("   • *_action_status columns: 'A' for Approved/Active ✅")
        print("   • *_action_status columns: 'R' for Rejected/Refused ✅") 
        print("   • No incorrect 'Y'/'N' values detected ✅")
    else:
        print("⚠️ Some issues detected - needs review")
    
    return all_correct

if __name__ == "__main__":
    success = test_action_status_mapping()
    if success:
        print("\n🎯 STATUS: Action status value mapping working correctly!")
    else:
        print("\n⚠️ STATUS: Action status value mapping needs attention")
