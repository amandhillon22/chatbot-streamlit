#!/usr/bin/env python3
"""
Test the correct plant-vehicle query handling
"""

from query_agent import ChatContext, english_to_sql
from sql import run_query

def test_plant_vehicle_fix():
    """Test the plant-vehicle relationship queries"""
    
    print("🧪 Testing Plant-Vehicle Query Fix")
    print("=" * 50)
    
    context = ChatContext()
    
    # First, populate context with vehicle data like the live chat did
    print("\n1️⃣ Setup: Populate context with vehicle trip data")
    try:
        columns, rows = run_query("SELECT bus_id, reg_no, plant_id FROM mega_trips LIMIT 20")
        context.add_interaction(
            "show me details of all the vehicles",
            "Here are the vehicle trip details",
            sql_query="SELECT bus_id, reg_no, plant_id FROM mega_trips LIMIT 20",
            columns=columns,
            rows=rows
        )
        print(f"✅ Stored {len(context.last_displayed_items)} vehicles with ordinal indexing")
        
        # Show the 7th vehicle
        if len(context.last_displayed_items) >= 7:
            seventh_vehicle = context.last_displayed_items[6]
            print(f"📊 7th vehicle: {seventh_vehicle}")
            
            # Extract the reg_no from 7th vehicle
            reg_no = None
            if isinstance(seventh_vehicle, dict):
                for key in ['reg_no', 'registration_number']:
                    if key in seventh_vehicle:
                        reg_no = seventh_vehicle[key]
                        break
            
            print(f"🎯 7th vehicle reg_no: {reg_no}")
            
            # Test the plant query
            print(f"\n2️⃣ Test: 'tell me the plant name for the 7th vehicle'")
            result = english_to_sql("tell me the plant name for the 7th vehicle", chat_context=context)
            print(f"Generated SQL: {result.get('sql', 'None')}")
            
            # Execute the query to see if it works
            if result.get('sql'):
                try:
                    columns_result, rows_result = run_query(result.get('sql'))
                    print(f"✅ Query executed successfully: {len(rows_result)} rows")
                    if rows_result:
                        print(f"   Result: {rows_result[0]}")
                    else:
                        print("   No data returned")
                except Exception as e:
                    print(f"❌ Query failed: {e}")
            
            # Test direct plant query
            if reg_no:
                print(f"\n3️⃣ Test: Direct plant query for {reg_no}")
                result2 = english_to_sql(f"What plant does vehicle {reg_no} belong to?", chat_context=context)
                print(f"Generated SQL: {result2.get('sql', 'None')}")
                
                if result2.get('sql'):
                    try:
                        columns_result2, rows_result2 = run_query(result2.get('sql'))
                        print(f"✅ Direct query executed: {len(rows_result2)} rows")
                        if rows_result2:
                            print(f"   Result: {rows_result2[0]}")
                        else:
                            print("   No data returned")
                    except Exception as e:
                        print(f"❌ Direct query failed: {e}")
        
        # Test manual correct query
        print(f"\n4️⃣ Test: Manual correct query")
        correct_sql = """
        SELECT ps.plant_code, ps.cust_name, ps.site_name 
        FROM mega_trips mt 
        JOIN plant_schedule ps ON mt.plant_id = ps.plant_id 
        WHERE mt.reg_no = 'MH47AS5987' 
        LIMIT 1
        """
        try:
            columns_manual, rows_manual = run_query(correct_sql)
            print(f"✅ Manual correct query executed: {len(rows_manual)} rows")
            if rows_manual:
                print(f"   Result: {rows_manual[0]}")
                plant_code, cust_name, site_name = rows_manual[0]
                print(f"   Plant Code: {plant_code}")
                print(f"   Customer: {cust_name}")
                print(f"   Site: {site_name}")
        except Exception as e:
            print(f"❌ Manual query failed: {e}")
    
    except Exception as e:
        print(f"❌ Setup error: {e}")
    
    print("\n✅ Plant-Vehicle Query Test Complete!")

if __name__ == "__main__":
    test_plant_vehicle_fix()
