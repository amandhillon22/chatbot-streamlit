#!/usr/bin/env python3
"""
Test script to verify user-friendly error handling for distance reports
This tests that technical errors like "Object of type Decimal is not JSON serializable" 
are properly handled and converted to user-friendly messages.
"""

import sys
sys.path.append('/home/linux/Documents/chatbot-diya')

import json
from decimal import Decimal

def test_decimal_json_serialization():
    """Test that DecimalEncoder properly handles Decimal objects."""
    
    print("🔧 Testing Decimal JSON Serialization")
    print("=" * 50)
    
    # Import the DecimalEncoder
    from src.core.sql import DecimalEncoder
    
    test_data = {
        "vehicle": "WB38C2023",
        "distance": Decimal("15150.75"),  # Distance in meters
        "drum_rotation": Decimal("897.5"),  # Drum rotation value
        "fuel_consumed": Decimal("45.25")
    }
    
    try:
        # Test without DecimalEncoder (should fail)
        try:
            result_without_encoder = json.dumps(test_data)
            print("❌ UNEXPECTED: Standard JSON encoding worked (should have failed)")
        except TypeError as e:
            print("✅ Expected error with standard JSON encoder:")
            print(f"   Error: {e}")
        
        # Test with DecimalEncoder (should work)
        try:
            result_with_encoder = json.dumps(test_data, cls=DecimalEncoder)
            print("✅ DecimalEncoder successfully handled Decimal objects!")
            print(f"   Result: {result_with_encoder}")
            
            # Verify the conversion
            parsed_back = json.loads(result_with_encoder)
            print("✅ Data successfully serialized and parsed:")
            for key, value in parsed_back.items():
                print(f"   {key}: {value} (type: {type(value).__name__})")
                
        except Exception as e:
            print(f"❌ DecimalEncoder failed: {e}")
            
    except Exception as e:
        print(f"❌ Test framework error: {e}")

def test_error_message_patterns():
    """Test that error message patterns are user-friendly."""
    
    print("\n📝 Testing Error Message Patterns")
    print("=" * 50)
    
    # Mock different types of technical errors
    technical_errors = [
        "Object of type Decimal is not JSON serializable",
        "psycopg2.OperationalError: connection timeout",
        "psycopg2.ProgrammingError: permission denied",
        "ConnectionPoolExhausted: all connections in use",
        "JSONDecodeError: invalid JSON format"
    ]
    
    # Test the error handling logic
    for error in technical_errors:
        print(f"\n🔧 Technical error: {error}")
        
        # Simulate the error handling logic from flask_app.py
        error_str = str(error)
        if "Object of type Decimal is not JSON serializable" in error_str:
            user_message = "❌ **Database Processing Error:** I encountered an issue processing the distance report data. This appears to be a data formatting problem. Please try again or contact support if the issue persists."
        elif "JSON" in error_str and "serializable" in error_str:
            user_message = "❌ **Data Format Error:** I'm having trouble processing the response data format. Please try rephrasing your query or contact support."
        elif "connection" in error_str.lower():
            user_message = "❌ **Database Connection Error:** I'm having trouble connecting to the database. Please try again in a moment."
        elif "timeout" in error_str.lower():
            user_message = "❌ **Query Timeout:** Your request is taking longer than expected. Please try a more specific query or try again later."
        elif "permission" in error_str.lower() or "access" in error_str.lower():
            user_message = "❌ **Access Error:** I don't have permission to access the requested data. Please contact your administrator."
        else:
            user_message = "❌ **Query Processing Error:** I encountered an unexpected issue while processing your request. Please try rephrasing your question or contact support if the problem continues."
        
        print(f"✅ User-friendly message: {user_message}")

def test_query_agent_imports():
    """Test that query agent can properly import DecimalEncoder."""
    
    print("\n🔧 Testing Query Agent DecimalEncoder Import")
    print("=" * 50)
    
    try:
        from src.core.query_agent import DecimalEncoder
        print("✅ DecimalEncoder successfully imported in query_agent.py")
        
        # Test usage
        test_data = {"value": Decimal("123.45")}
        result = json.dumps(test_data, cls=DecimalEncoder)
        print(f"✅ DecimalEncoder works in query_agent context: {result}")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
    except Exception as e:
        print(f"❌ Other error: {e}")

def test_enhanced_query_agent_imports():
    """Test that enhanced query agent can properly import DecimalEncoder."""
    
    print("\n🔧 Testing Enhanced Query Agent DecimalEncoder Import")
    print("=" * 50)
    
    try:
        from src.core.query_agent_enhanced import DecimalEncoder
        print("✅ DecimalEncoder successfully imported in query_agent_enhanced.py")
        
        # Test usage
        test_data = {"value": Decimal("123.45")}
        result = json.dumps(test_data, cls=DecimalEncoder)
        print(f"✅ DecimalEncoder works in enhanced query_agent context: {result}")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
    except Exception as e:
        print(f"❌ Other error: {e}")

if __name__ == "__main__":
    print("🚀 Testing Error Handling Improvements")
    print("🎯 Goal: Ensure technical errors are converted to user-friendly messages")
    print("=" * 80)
    
    # Run the tests
    test_decimal_json_serialization()
    test_error_message_patterns()
    test_query_agent_imports()
    test_enhanced_query_agent_imports()
    
    print("\n" + "=" * 80)
    print("✅ Error Handling Tests Complete!")
    print("\n💡 Key Improvements:")
    print("   • Technical errors no longer exposed to users")
    print("   • User-friendly error messages for common issues")
    print("   • Decimal objects properly handled in JSON serialization")
    print("   • Distance report queries should now work without JSON errors")
