#!/usr/bin/env python3
"""
import sys
sys.path.append('/home/linux/Documents/chatbot-diya')

Quick test of improved empty data handling
"""

from src.core.query_agent import ChatContext, generate_final_response

def test_improved_empty_data():
    """Test the improved empty data messaging"""
    
    print("🧪 Testing Improved Empty Data Handling")
    print("=" * 50)
    
    context = ChatContext()
    
    # Test 1: Empty result set
    print("\n1️⃣ Test: Empty result set")
    empty_columns = ['reg_no', 'region']
    empty_rows = []
    response1 = generate_final_response("What region does vehicle MH46CL4636 belong to?", empty_columns, empty_rows, chat_context=context)
    print(f"Response: {response1}")
    
    # Test 2: Null/empty data
    print("\n2️⃣ Test: Null data in result")
    null_columns = ['reg_no', 'regional_name']
    null_rows = [['MH46CL4636', None]]
    response2 = generate_final_response("What region does vehicle MH46CL4636 belong to?", null_columns, null_rows, chat_context=context)
    print(f"Response: {response2}")
    
    # Test 3: Empty string data
    print("\n3️⃣ Test: Empty string data")
    empty_str_columns = ['reg_no', 'regional_name']
    empty_str_rows = [['MH46CL4636', '']]
    response3 = generate_final_response("What region does vehicle MH46CL4636 belong to?", empty_str_columns, empty_str_rows, chat_context=context)
    print(f"Response: {response3}")
    
    # Test 4: Non-existent vehicle
    print("\n4️⃣ Test: Non-existent vehicle")
    nonexistent_columns = ['reg_no', 'details']
    nonexistent_rows = []
    response4 = generate_final_response("Show me details for vehicle FAKE123", nonexistent_columns, nonexistent_rows, chat_context=context)
    print(f"Response: {response4}")
    
    print("\n✅ Improved Empty Data Test Complete!")

if __name__ == "__main__":
    test_improved_empty_data()
