#!/usr/bin/env python3
"""
Quick test to verify the system is working after the fix
"""

print("🧪 Testing the fixed chatbot system...")

try:
    print("📥 Importing query agent...")
    from query_agent import english_to_sql, generate_final_response
    print("✅ Query agent imported successfully")
    
    print("\n🧪 Testing distance query...")
    distance_query = "show me vehicles with distance less than 500 km"
    result = english_to_sql(distance_query)
    print(f"Distance query result type: {type(result)}")
    if result:
        print(f"✅ Distance query generated SQL: {result[:200]}...")
    else:
        print("❌ Distance query returned no result")
    
    print("\n🧪 Testing plant-vehicle query...")
    plant_query = "show me the vehicles of mohali plant"
    result2 = english_to_sql(plant_query)
    print(f"Plant query result type: {type(result2)}")
    if result2:
        print(f"✅ Plant query generated SQL: {result2[:200]}...")
    else:
        print("❌ Plant query returned no result")
    
    print("\n🧪 Testing basic vehicle query...")
    basic_query = "show me all vehicles"
    result3 = english_to_sql(basic_query)
    print(f"Basic query result type: {type(result3)}")
    if result3:
        print(f"✅ Basic query generated SQL: {result3[:200]}...")
    else:
        print("❌ Basic query returned no result")
    
    print("\n🎉 All tests completed!")
    
except Exception as e:
    print(f"❌ Error during testing: {e}")
    import traceback
    traceback.print_exc()
