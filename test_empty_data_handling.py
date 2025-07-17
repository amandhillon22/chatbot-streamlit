#!/usr/bin/env python3
"""
Test how the system handles empty/null data and improve messaging
"""

from query_agent import ChatContext, english_to_sql, generate_final_response
from sql import run_query
import os
from dotenv import load_dotenv

load_dotenv()

def test_empty_data_handling():
    """Test how the system handles empty/null data scenarios"""
    
    print("🧪 Testing Empty/Null Data Handling")
    print("=" * 50)
    
    context = ChatContext()
    
    # First get the vehicle list for context
    print("\n1️⃣ Setup: Get vehicle list for context")
    try:
        columns, real_rows = run_query("SELECT DISTINCT reg_no FROM public.drv_veh_qr_assign LIMIT 10")
        context.add_interaction(
            "show me all vehicles",
            f"Here are the vehicles",
            sql_query="SELECT DISTINCT reg_no FROM public.drv_veh_qr_assign LIMIT 10",
            columns=columns,
            rows=real_rows
        )
        print(f"✅ Got {len(real_rows)} vehicles for testing")
        
        if real_rows:
            test_vehicle = real_rows[0][0]  # Get first vehicle
            print(f"🎯 Testing with vehicle: {test_vehicle}")
            
            # Test 1: Query for data that likely doesn't exist
            print(f"\n2️⃣ Test 1: Query for region data (likely empty)")
            result1 = english_to_sql(f"What region is vehicle {test_vehicle} in?", chat_context=context)
            print(f"Generated SQL: {result1.get('sql', 'None')}")
            
            if result1.get('sql'):
                try:
                    columns1, rows1 = run_query(result1.get('sql'))
                    print(f"Query result: {len(rows1)} rows")
                    
                    if len(rows1) == 0:
                        print("🔍 EMPTY RESULT SET - Testing response generation")
                        response1 = generate_final_response(f"What region is vehicle {test_vehicle} in?", columns1, rows1, chat_context=context)
                        print(f"Generated response: {response1}")
                    else:
                        print(f"Data found: {rows1}")
                        # Check if data is null/empty
                        has_meaningful_data = False
                        for row in rows1:
                            for value in row:
                                if value is not None and str(value).strip():
                                    has_meaningful_data = True
                                    break
                        
                        if not has_meaningful_data:
                            print("🔍 NULL/EMPTY DATA - Testing response generation")
                            response1 = generate_final_response(f"What region is vehicle {test_vehicle} in?", columns1, rows1, chat_context=context)
                            print(f"Generated response: {response1}")
                        else:
                            print("✅ Meaningful data found")
                
                except Exception as e:
                    print(f"Query failed: {e}")
            
            # Test 2: Query for non-existent vehicle
            print(f"\n3️⃣ Test 2: Query for non-existent vehicle")
            fake_vehicle = "FAKE123XYZ"
            result2 = english_to_sql(f"Show me details for vehicle {fake_vehicle}", chat_context=context)
            print(f"Generated SQL: {result2.get('sql', 'None')}")
            
            if result2.get('sql'):
                try:
                    columns2, rows2 = run_query(result2.get('sql'))
                    print(f"Query result: {len(rows2)} rows")
                    
                    if len(rows2) == 0:
                        print("🔍 NON-EXISTENT VEHICLE - Testing response generation")
                        response2 = generate_final_response(f"Show me details for vehicle {fake_vehicle}", columns2, rows2, chat_context=context)
                        print(f"Generated response: {response2}")
                
                except Exception as e:
                    print(f"Query failed: {e}")
            
            # Test 3: Ordinal reference to vehicle with missing data
            print(f"\n4️⃣ Test 3: Ordinal reference with missing data")
            result3 = english_to_sql("What region does the first vehicle belong to?", chat_context=context)
            print(f"Generated SQL: {result3.get('sql', 'None')}")
            
            if result3.get('sql'):
                try:
                    columns3, rows3 = run_query(result3.get('sql'))
                    print(f"Query result: {len(rows3)} rows")
                    
                    response3 = generate_final_response("What region does the first vehicle belong to?", columns3, rows3, chat_context=context)
                    print(f"Generated response: {response3}")
                
                except Exception as e:
                    print(f"Query failed: {e}")
    
    except Exception as e:
        print(f"❌ Setup error: {e}")
    
    print("\n5️⃣ Testing direct empty data response")
    # Test with manually empty data
    empty_columns = ['reg_no', 'region']
    empty_rows = []
    empty_response = generate_final_response("What region does vehicle ABC123 belong to?", empty_columns, empty_rows, chat_context=context)
    print(f"Empty data response: {empty_response}")
    
    print("\n6️⃣ Testing null data response")
    # Test with null data
    null_columns = ['reg_no', 'region']
    null_rows = [['ABC123', None]]
    null_response = generate_final_response("What region does vehicle ABC123 belong to?", null_columns, null_rows, chat_context=context)
    print(f"Null data response: {null_response}")
    
    print("\n✅ Empty/Null Data Test Complete!")

if __name__ == "__main__":
    test_empty_data_handling()
