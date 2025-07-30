#!/usr/bin/env python3
"""
Test script for Decimal JSON encoding fix
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_decimal_encoding():
    """Test the Decimal JSON encoding fix"""
    try:
        from decimal import Decimal
        import json
        from src.core.sql import DecimalEncoder
        
        print("🧪 Testing Decimal JSON encoding fix...")
        
        # Test data with Decimal objects (like from PostgreSQL)
        test_data = {
            'distance': Decimal('10.5'),
            'amount': Decimal('123.456'), 
            'name': 'test_vehicle',
            'count': 42
        }
        
        print(f"Original data: {test_data}")
        print(f"Data types: {[(k, type(v)) for k, v in test_data.items()]}")
        
        # Try encoding with custom encoder
        result = json.dumps(test_data, cls=DecimalEncoder)
        print(f"JSON encoded: {result}")
        
        # Try decoding back
        decoded = json.loads(result)
        print(f"Decoded back: {decoded}")
        print(f"Decoded types: {[(k, type(v)) for k, v in decoded.items()]}")
        
        print("✅ Decimal JSON encoding fix works correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Decimal encoding test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_decimal_encoding()
    
    if success:
        print("\n🎉 JSON SERIALIZATION FIX: ✅ IMPLEMENTED SUCCESSFULLY")
        print("💡 PostgreSQL Decimal objects now serialize correctly to JSON")
    else:
        print("\n❌ JSON SERIALIZATION FIX: ❌ FAILED")
        print("❌ Additional fixes needed")
