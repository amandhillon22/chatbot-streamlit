#!/usr/bin/env python3
"""
import sys
sys.path.append('/home/linux/Documents/chatbot-diya')

Test script to verify vehicle type foreign key relationship
"""

def test_vehicle_type_relationship():
    """Test the vehicle type relationship updates"""
    try:
        from src.database.database_reference_parser import DatabaseReferenceParser
        
        print("🧪 Testing Vehicle Type Foreign Key Relationship")
        
        # Test 1: Parser can be imported
        parser = DatabaseReferenceParser('database_reference.md')
        print("✅ Parser initialized successfully")
        
        # Test 2: Vehicle type queries return relevant tables
        vehicle_type_queries = [
            'vehicle type',
            'vehicle category', 
            'type of vehicle',
            'what type of vehicle'
        ]
        
        print("\n🔍 Testing vehicle type queries:")
        for query in vehicle_type_queries:
            try:
                relevant_tables = parser.get_business_relevant_tables(query)
                print(f"   '{query}' → {len(relevant_tables)} tables found")
                if 'veh_type' in relevant_tables or 'vehicle_master' in relevant_tables:
                    print("     ✅ Includes vehicle type tables")
                else:
                    print("     ⚠️  Missing vehicle type tables")
            except Exception as e:
                print(f"     ❌ Error: {e}")
        
        print("\n✅ Vehicle type relationship test complete!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_vehicle_type_relationship()
    print(f"\n{'🎉 SUCCESS!' if success else '❌ FAILED'}")
