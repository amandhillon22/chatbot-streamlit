#!/usr/bin/env python3
"""
import sys
sys.path.append('/home/linux/Documents/chatbot-diya')

Quick test after fixing the schema duplication issue
"""

print("🧪 Testing after fixing schema duplication...")

try:
    from src.core.query_agent import english_to_sql
    
    # Test a simple hierarchical query
    test_query = "show me the vehicles of mohali plant"
    print(f"Testing: '{test_query}'")
    
    result = english_to_sql(test_query)
    
    if result:
        print(f"✅ SQL Generated successfully!")
        print(f"Length: {len(result)} characters")
        
        # Check for key hierarchical elements
        result_lower = result.lower()
        checks = {
            'id_hosp': 'id_hosp' in result_lower,
            'vehicle_master': 'vehicle_master' in result_lower,
            'hosp_master': 'hosp_master' in result_lower,
            'JOIN': 'join' in result_lower
        }
        
        print("🔍 Hierarchical relationship checks:")
        for check, passed in checks.items():
            print(f"  {'✅' if passed else '❌'} {check}: {'Present' if passed else 'Missing'}")
            
        if all(checks.values()):
            print("🎉 All hierarchical relationships present!")
        else:
            print("⚠️ Some hierarchical relationships missing")
            
        # Show a sample of the SQL
        print(f"\n📋 Generated SQL preview:")
        print(result[:300] + "..." if len(result) > 300 else result)
        
    else:
        print("❌ No SQL generated")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n✅ Quick test complete!")
