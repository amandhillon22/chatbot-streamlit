#!/usr/bin/env python3
"""
Test the region query fix with real data
"""

from query_agent import ChatContext, english_to_sql, generate_final_response
from sql import run_query
import os
from dotenv import load_dotenv

load_dotenv()

def test_region_fix():
    """Test the region query fix"""
    
    print("🧪 Testing Region Query Fix")
    print("=" * 50)
    
    # Create a chat context
    context = ChatContext()
    
    print("\n1️⃣ First, get vehicles list (to populate context)")
    result1 = english_to_sql("show me all vehicles", chat_context=context)
    
    # Execute and store results
    try:
        sql_query = result1.get('sql')
        if sql_query and sql_query.strip().lower() != "null":
            columns, real_rows = run_query(sql_query)
            print(f"✅ Got {len(real_rows)} vehicles from database")
            
            # Store the results in context
            context.add_interaction(
                "show me all vehicles",
                f"Here are the vehicles",
                sql_query=sql_query,
                columns=columns,
                rows=real_rows
            )
            
            # Show first few vehicles
            print(f"\nFirst 7 vehicles:")
            for i, item in enumerate(context.last_displayed_items[:7], 1):
                if isinstance(item, dict):
                    reg_no = list(item.values())[0] if item else "N/A"
                    print(f"  {i}. {reg_no}")
                    
        else:
            print("❌ No valid SQL generated")
            return
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    print("\n2️⃣ Now test region query for 7th vehicle")
    result2 = english_to_sql("What region does the 7th vehicle belong to?", chat_context=context)
    print(f"Generated SQL: {result2.get('sql', 'None')}")
    
    # Execute the region query
    try:
        sql2 = result2.get('sql')
        if sql2 and sql2.strip().lower() != "null":
            columns2, rows2 = run_query(sql2)
            print(f"✅ Region query executed: {len(rows2)} rows returned")
            if rows2:
                print(f"   Result: {rows2[0]}")
            else:
                print("   No data returned")
        else:
            print("❌ No SQL generated for region query")
    except Exception as e:
        print(f"❌ Region query failed: {e}")
    
    print("\n3️⃣ Test generic region query")
    result3 = english_to_sql("Show me all vehicles with their regions", chat_context=context)
    print(f"Generated SQL: {result3.get('sql', 'None')}")
    
    # Execute the generic region query
    try:
        sql3 = result3.get('sql')
        if sql3 and sql3.strip().lower() != "null":
            columns3, rows3 = run_query(sql3)
            print(f"✅ Generic region query executed: {len(rows3)} rows returned")
            if rows3:
                print(f"   Sample results:")
                for i, row in enumerate(rows3[:5], 1):
                    print(f"   {i}. {row}")
            else:
                print("   No data returned")
        else:
            print("❌ No SQL generated for generic region query")
    except Exception as e:
        print(f"❌ Generic region query failed: {e}")
    
    print("\n4️⃣ Test specific vehicle region lookup")
    # Get the 7th vehicle registration number
    if len(context.last_displayed_items) >= 7:
        seventh_vehicle = context.last_displayed_items[6]
        if isinstance(seventh_vehicle, dict):
            reg_no = None
            for key in ['reg_no', 'registration_number', 'vehicle_id']:
                if key in seventh_vehicle:
                    reg_no = seventh_vehicle[key]
                    break
            
            if reg_no:
                print(f"Testing direct query for vehicle: {reg_no}")
                result4 = english_to_sql(f"What region is vehicle {reg_no} in?", chat_context=context)
                print(f"Generated SQL: {result4.get('sql', 'None')}")
                
                # Execute direct query
                try:
                    sql4 = result4.get('sql')
                    if sql4 and sql4.strip().lower() != "null":
                        columns4, rows4 = run_query(sql4)
                        print(f"✅ Direct query executed: {len(rows4)} rows returned")
                        if rows4:
                            print(f"   Result: {rows4[0]}")
                        else:
                            print("   No data returned")
                    else:
                        print("❌ No SQL generated for direct query")
                except Exception as e:
                    print(f"❌ Direct query failed: {e}")
    
    print("\n✅ Region Fix Test Complete!")

if __name__ == "__main__":
    test_region_fix()
