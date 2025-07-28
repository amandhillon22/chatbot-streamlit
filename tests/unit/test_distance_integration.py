#!/usr/bin/env python3
"""
import sys
sys.path.append('/home/linux/Documents/chatbot-diya')

Test Distance Unit Integration
Tests the complete integration of distance unit detection and conversion
with the main query agent system.
"""

from src.core.query_agent_enhanced import english_to_sql
from src.database.distance_units import distance_manager

def test_distance_queries():
    """Test various distance-related queries to verify conversion works."""
    
    print("🧪 Testing Distance Unit Integration")
    print("=" * 60)
    
    # Test queries that should trigger distance conversion
    test_queries = [
        "Show total distance in kilometers",
        "What's the total distance covered in km?",
        "Show all vehicles with mileage",
        "Distance traveled in meters",
        "Total distance in km for all trips",
        "Show vehicle odometer readings",
        "Which vehicle has covered the most distance in kilometers?",
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🔍 Test {i}: '{query}'")
        print("-" * 40)
        
        try:
            result = english_to_sql(query)
            
            if result.get('sql'):
                sql = result['sql']
                print(f"✅ Generated SQL:")
                print(f"   {sql}")
                
                # Check if conversion is applied
                if 'ROUND(' in sql and '/ 1000' in sql:
                    print("🎯 ✅ Meter-to-kilometer conversion detected!")
                elif any(word in query.lower() for word in ['km', 'kilometer']):
                    print("⚠️  No conversion detected (may be intentional if already in km)")
                else:
                    print("ℹ️  No conversion needed")
                    
                print(f"📝 Response: {result.get('response', 'No response')}")
                
            else:
                print(f"❌ No SQL generated")
                print(f"📝 Response: {result.get('response', 'No response')}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("🔍 Distance Column Detection Summary:")
    print(f"Found {len(distance_manager.distance_columns)} distance columns:")
    
    for column_key, unit in list(distance_manager.distance_columns.items())[:10]:  # Show first 10
        print(f"  • {column_key}: {unit}")
    
    if len(distance_manager.distance_columns) > 10:
        print(f"  ... and {len(distance_manager.distance_columns) - 10} more")

if __name__ == "__main__":
    test_distance_queries()
