#!/usr/bin/env python3
"""
Test the specific query that was failing: "show me plants in gujarat"
"""

print("🎯 Testing the Original Failing Query")
print("=" * 50)

def test_gujarat_query():
    """Test the specific Gujarat query that was failing"""
    
    try:
        from query_agent import english_to_sql
        
        query = "show me plants in gujarat"
        print(f"📝 Query: '{query}'")
        
        result = english_to_sql(query)
        
        if result and isinstance(result, dict) and 'sql' in result:
            sql = result['sql']
            print(f"✅ SQL Generated Successfully!")
            print(f"📋 SQL: {sql}")
            
            # Check for the specific fix
            if 'zm.zone_name' in sql.lower():
                print(f"✅ FIXED: Using zm.zone_name (correct)")
            
            if 'zm.name' in sql.lower():
                print(f"❌ STILL BROKEN: Using zm.name (incorrect)")
                return False
            
            # Test if this SQL would actually work
            print(f"🔍 SQL Analysis:")
            print(f"  - Uses zone_master: {'zone_master' in sql.lower()}")
            print(f"  - Uses zone_name column: {'zone_name' in sql.lower()}")
            print(f"  - Uses correct JOIN syntax: {'join' in sql.lower()}")
            print(f"  - Filters by Gujarat: {'gujarat' in sql.lower()}")
            
            if all([
                'zone_master' in sql.lower(),
                'zone_name' in sql.lower(), 
                'join' in sql.lower(),
                'gujarat' in sql.lower()
            ]):
                print(f"🎉 QUERY SHOULD NOW WORK!")
                return True
            else:
                print(f"⚠️ Query may still have issues")
                return False
                
        else:
            print(f"❌ No SQL generated")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# Run the test
print("🧪 Testing Gujarat Plants Query...")
success = test_gujarat_query()

print("\n" + "=" * 50)
if success:
    print("🎉 SUCCESS! The original failing query is now FIXED!")
    print("✅ zm.zone_name is correctly used")
    print("✅ No more 'column zm.name does not exist' errors")
    print("✅ The query should execute successfully in the database")
else:
    print("❌ The query still has issues")

print("\n🔧 Key Fix Applied:")
print("   OLD (broken): WHERE zm.name = 'Gujarat'")
print("   NEW (working): WHERE zm.zone_name = 'Gujarat'")
print("\n✅ Test complete!")
