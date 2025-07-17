#!/usr/bin/env python3
"""
Test script to simulate the exact live scenario
"""

from query_agent import ChatContext, english_to_sql, generate_final_response
from sql import run_query
import os
from dotenv import load_dotenv

load_dotenv()

def test_live_scenario():
    """Test the exact scenario from the live chat"""
    
    print("🧪 Testing EXACT Live Chat Scenario")
    print("=" * 50)
    
    # Create a chat context (simulating a new session)
    context = ChatContext()
    
    print("\n1️⃣ User asks: 'show me all the vehicles'")
    result1 = english_to_sql("show me all the vehicles", chat_context=context)
    print(f"Generated SQL: {result1.get('sql', 'None')}")
    
    # Execute the actual SQL to simulate what Flask app does
    try:
        sql_query = result1.get('sql')
        if sql_query and sql_query.strip().lower() != "null":
            print(f"🔄 Executing SQL to get real data...")
            columns, real_rows = run_query(sql_query)
            print(f"✅ Got {len(real_rows)} vehicles from database")
            
            # Store the real results in context (like Flask app does)
            context.add_interaction(
                "show me all the vehicles",
                f"Here are the registration numbers for all {len(real_rows)} vehicles",
                sql_query=sql_query,
                columns=columns,
                rows=real_rows
            )
            
            print(f"💾 Stored {len(context.last_displayed_items)} items with ordinal indexing")
            
            # Show the first 18 vehicles (as shown in live chat)
            print(f"\nReal vehicles returned (first 18):")
            for i, item in enumerate(context.last_displayed_items[:18], 1):
                if isinstance(item, dict):
                    # Extract the first column value (registration number)
                    reg_no = list(item.values())[0] if item else "N/A"
                    print(f"{i:2d}. {reg_no}")
                else:
                    print(f"{i:2d}. {item}")
            
            if len(context.last_displayed_items) >= 7:
                seventh_vehicle = context.last_displayed_items[6]  # 0-indexed
                print(f"\n📊 7th vehicle in our data: {seventh_vehicle}")
                
                print("\n2️⃣ User asks: 'What region does the 7th vehicle belong to?'")
                
                # Test ordinal extraction
                position, entity = context.extract_ordinal_reference("What region does the 7th vehicle belong to?")
                print(f"🎯 Extracted ordinal: position={position}, entity={entity}")
                
                if position:
                    target_item = context.get_item_by_ordinal(position)
                    print(f"🎯 Target item: {target_item}")
                
                # Test the full flow (as live chat would do)
                result2 = english_to_sql("What region does the 7th vehicle belong to?", chat_context=context)
                print(f"Generated SQL: {result2.get('sql', 'None')}")
                print(f"Response: {result2.get('response', 'None')}")
                
                # Execute this SQL too to see what happens
                sql2 = result2.get('sql')
                if sql2 and sql2.strip().lower() != "null":
                    try:
                        columns2, rows2 = run_query(sql2)
                        print(f"🔍 SQL execution result: {len(rows2)} rows returned")
                        if rows2:
                            print(f"   Data: {rows2[:3]}")  # Show first few rows
                        else:
                            print("   No data returned - this explains the 'couldn't find' message!")
                    except Exception as e:
                        print(f"❌ SQL execution failed: {e}")
                
                # Get the actual registration number of the 7th vehicle
                if isinstance(seventh_vehicle, dict):
                    reg_field = None
                    for key in seventh_vehicle.keys():
                        if 'reg' in key.lower() or key == 'reg_no':
                            reg_field = key
                            break
                    
                    if reg_field:
                        actual_reg_no = seventh_vehicle[reg_field]
                        print(f"\n3️⃣ User asks: 'Tell me about vehicle {actual_reg_no}' (REAL 7th vehicle)")
                        result3 = english_to_sql(f"Tell me about vehicle {actual_reg_no}", chat_context=context)
                        print(f"Generated SQL: {result3.get('sql', 'None')}")
                        
                        # Execute this SQL too
                        sql3 = result3.get('sql')
                        if sql3 and sql3.strip().lower() != "null":
                            try:
                                columns3, rows3 = run_query(sql3)
                                print(f"🔍 SQL execution result: {len(rows3)} rows returned")
                                if rows3:
                                    print(f"   Success! Found data for {actual_reg_no}")
                                else:
                                    print(f"   No data found for {actual_reg_no}")
                            except Exception as e:
                                print(f"❌ SQL execution failed: {e}")
                        
                        print(f"\n4️⃣ User asks: 'What about its maintenance records?'")
                        result4 = english_to_sql("What about its maintenance records?", chat_context=context)
                        print(f"Generated SQL: {result4.get('sql', 'None')}")
                        
                        print(f"\n5️⃣ User asks: 'Show me the first vehicle's details'")
                        result5 = english_to_sql("Show me the first vehicle's details", chat_context=context)
                        print(f"Generated SQL: {result5.get('sql', 'None')}")
                        
                        # Test with first vehicle too
                        first_vehicle = context.last_displayed_items[0]
                        if isinstance(first_vehicle, dict) and reg_field:
                            first_reg_no = first_vehicle[reg_field]
                            print(f"   (Should query for: {first_reg_no})")
                            
                            # Execute this SQL
                            sql5 = result5.get('sql')
                            if sql5 and sql5.strip().lower() != "null":
                                try:
                                    columns5, rows5 = run_query(sql5)
                                    print(f"🔍 SQL execution result: {len(rows5)} rows returned")
                                    if rows5:
                                        print(f"   Success! Found data for first vehicle")
                                    else:
                                        print(f"   No data found for first vehicle")
                                except Exception as e:
                                    print(f"❌ SQL execution failed: {e}")
                        
            else:
                print(f"❌ Not enough vehicles ({len(context.last_displayed_items)}) to test 7th vehicle")
                
        else:
            print("❌ No valid SQL generated for vehicle query")
            
    except Exception as e:
        print(f"❌ Database error: {e}")
    
    print("\n✅ Live Scenario Test Complete!")

if __name__ == "__main__":
    test_live_scenario()
