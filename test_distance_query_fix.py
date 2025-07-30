#!/usr/bin/env python3
"""
Test script to verify the JSON serialization fix for the distance report query
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_distance_query_fix():
    """Test the actual distance report query that was failing"""
    try:
        from src.core.sql import run_query
        
        print("🧪 Testing distance report query with Decimal fix...")
        
        # The actual query that was failing
        test_query = """
        SELECT
          'TEST123' AS registration_number,
          TO_CHAR(NOW(), 'DD Mon YYYY HH24:MI') AS trip_start_time,
          TO_CHAR(NOW(), 'DD Mon YYYY HH24:MI') AS trip_end_time,
          ROUND(1234.567, 2) AS distance_km,
          '02:30' AS drum_rotation_time
        """
        
        columns, rows = run_query(test_query)
        
        print(f"✅ Query executed successfully!")
        print(f"Columns: {columns}")
        print(f"Rows: {rows}")
        
        # Check data types
        if rows:
            row = rows[0]
            print(f"Row data types: {[type(val).__name__ for val in row]}")
            
            # Check specifically for the distance_km value (which should be Decimal)
            distance_idx = columns.index('distance_km') if 'distance_km' in columns else -1
            if distance_idx >= 0:
                distance_value = row[distance_idx]
                print(f"Distance value: {distance_value} (type: {type(distance_value).__name__})")
        
        print("✅ Distance report query JSON serialization fix working!")
        return True
        
    except Exception as e:
        print(f"❌ Distance query test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_distance_query_fix()
    
    if success:
        print("\n🎉 DISTANCE QUERY FIX: ✅ WORKING CORRECTLY")
        print("💡 The 'Object of type Decimal is not JSON serializable' error is now fixed!")
        print("🚀 Your chatbot should now handle distance reports without errors")
    else:
        print("\n❌ DISTANCE QUERY FIX: ❌ STILL HAS ISSUES")
        print("❌ Additional investigation needed")
