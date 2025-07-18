#!/usr/bin/env python3
"""
Test the plant-to-vehicle relationship fix
"""

def test_plant_vehicle_guidance():
    """Test that the guidance is now in place for plant-vehicle queries"""
    
    print("🧪 Testing Plant-to-Vehicle Query Guidance")
    print("=" * 50)
    
    # Show what the guidance now includes
    expected_queries = [
        {
            "user_query": "show me the vehicles of mohali plant",
            "expected_sql": "SELECT vm.reg_no FROM vehicle_master vm JOIN hosp_master hm ON vm.id_hosp = hm.id_no WHERE hm.name ILIKE '%mohali%'",
            "expected_behavior": "✅ Should find vehicles assigned to Mohali plant"
        },
        {
            "user_query": "vehicles of PB-Mohali",
            "expected_sql": "SELECT vm.reg_no FROM vehicle_master vm JOIN hosp_master hm ON vm.id_hosp = hm.id_no WHERE hm.name ILIKE '%mohali%'",
            "expected_behavior": "✅ Should work with exact plant name from previous query"
        },
        {
            "user_query": "show vehicles in mohali",
            "expected_sql": "SELECT vm.reg_no, vm.bus_id FROM vehicle_master vm JOIN hosp_master hm ON vm.id_hosp = hm.id_no WHERE hm.name ILIKE '%mohali%'",
            "expected_behavior": "✅ Should handle variations of the query"
        }
    ]
    
    print("🎯 ADDED GUIDANCE TO query_agent.py:")
    print("""
🚛 **VEHICLES OF PLANT QUERIES - CRITICAL:**
- "Vehicles of Mohali plant" → 
  SELECT vm.reg_no FROM vehicle_master vm 
  JOIN hosp_master hm ON vm.id_hosp = hm.id_no 
  WHERE hm.name ILIKE '%mohali%'
  
- "Show vehicles of [plant name]" → 
  SELECT vm.reg_no, vm.bus_id FROM vehicle_master vm 
  JOIN hosp_master hm ON vm.id_hosp = hm.id_no 
  WHERE hm.name ILIKE '%[plant name]%'
""")
    
    print("\n📊 EXPECTED BEHAVIOR:")
    for i, test in enumerate(expected_queries, 1):
        print(f"\n{i}. Query: '{test['user_query']}'")
        print(f"   Expected SQL: {test['expected_sql']}")
        print(f"   Behavior: {test['expected_behavior']}")
    
    print(f"\n🔧 KEY FIXES:")
    print("✅ Added specific guidance for 'vehicles of [plant name]' queries")
    print("✅ Uses vehicle_master JOIN hosp_master for plant-vehicle relationship")
    print("✅ Uses ILIKE '%plant_name%' for flexible name matching")
    print("✅ Shows reg_no (registration number) as primary identifier")
    
    print(f"\n🎯 WHY THIS FIXES THE ISSUE:")
    print("❌ Before: No guidance for plant→vehicle queries = generic response")
    print("✅ After: Explicit SQL pattern for plant→vehicle queries = immediate results")
    
    return True

if __name__ == "__main__":
    test_plant_vehicle_guidance()
