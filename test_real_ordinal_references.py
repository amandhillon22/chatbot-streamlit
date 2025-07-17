#!/usr/bin/env python3
"""
Test script for ordinal reference with REAL database data
"""

from query_agent import ChatContext, english_to_sql, generate_final_response
from sql import run_query
import os
from dotenv import load_dotenv

load_dotenv()

def test_real_ordinal_references():
    """Test ordinal references with actual database data"""
    
    print("🧪 Testing Ordinal Reference with REAL Database Data")
    print("=" * 70)
    
    # Create a chat context
    context = ChatContext()
    
    print("\n1️⃣ First Question: Show me all vehicles")
    result1 = english_to_sql("Show me all vehicles", chat_context=context)
    print(f"Generated SQL: {result1.get('sql', 'None')}")
    
    # Execute the actual SQL to get real data
    try:
        sql_query = result1.get('sql')
        if sql_query and sql_query.strip().lower() != "null":
            print(f"🔄 Executing query to get real data...")
            columns, real_rows = run_query(sql_query)
            print(f"✅ Got {len(real_rows)} real vehicles from database")
            
            # Store the real results in context
            context.add_interaction(
                "Show me all vehicles",
                "Here are all the vehicles from the database",
                sql_query=sql_query,
                columns=columns,
                rows=real_rows
            )
            
            print(f"💾 Stored {len(context.last_displayed_items)} items with ordinal indexing")
            
            # Show first few vehicles for reference
            print(f"\nReal vehicles in database:")
            for i, item in enumerate(context.last_displayed_items[:10], 1):
                if isinstance(item, dict):
                    # Extract the first column value (usually registration number)
                    first_value = list(item.values())[0] if item else "N/A"
                    print(f"  {i}. {first_value}")
                else:
                    print(f"  {i}. {item}")
            
            if len(context.last_displayed_items) >= 7:
                seventh_vehicle = context.last_displayed_items[6]
                print(f"\n📊 7th vehicle should be: {seventh_vehicle}")
                
                print("\n2️⃣ Ordinal Reference Test: What region does the 7th vehicle belong to?")
                
                # Test ordinal extraction
                position, entity = context.extract_ordinal_reference("What region does the 7th vehicle belong to?")
                print(f"🎯 Extracted ordinal: position={position}, entity={entity}")
                
                if position:
                    target_item = context.get_item_by_ordinal(position)
                    print(f"🎯 Target item: {target_item}")
                
                # Test the full flow
                result2 = english_to_sql("What region does the 7th vehicle belong to?", chat_context=context)
                print(f"Generated SQL: {result2.get('sql', 'None')}")
                print(f"Response: {result2.get('response', 'None')}")
                
                # Get the actual registration number of the 7th vehicle
                if isinstance(seventh_vehicle, dict):
                    # Find the registration number field
                    reg_field = None
                    for key in seventh_vehicle.keys():
                        if 'reg' in key.lower() or 'registration' in key.lower() or key in ['vehicle_id', 'id']:
                            reg_field = key
                            break
                    
                    if reg_field:
                        actual_reg_no = seventh_vehicle[reg_field]
                        print(f"\n3️⃣ Specific Vehicle Test: Tell me about vehicle {actual_reg_no}")
                        result3 = english_to_sql(f"Tell me about vehicle {actual_reg_no}", chat_context=context)
                        print(f"Generated SQL: {result3.get('sql', 'None')}")
                        print(f"Response: {result3.get('response', 'None')}")
                        
                        print(f"\n4️⃣ Context Awareness Test: What about its maintenance records?")
                        context_for_llm = context.get_context_for_llm("What about its maintenance records?")
                        print(f"Context provided to LLM:\n{context_for_llm}")
                        
                        result4 = english_to_sql("What about its maintenance records?", chat_context=context)
                        print(f"Generated SQL: {result4.get('sql', 'None')}")
                
                print("\n5️⃣ Alternative Ordinal Test: Show me the first vehicle's details")
                result5 = english_to_sql("Show me the first vehicle's details", chat_context=context)
                print(f"Generated SQL: {result5.get('sql', 'None')}")
                
                # Test different ordinal formats with real data
                print("\n6️⃣ Testing Different Ordinal Formats:")
                max_items = len(context.last_displayed_items)
                test_phrases = [
                    "2nd vehicle",
                    "third vehicle", 
                    "the 5th vehicle",
                    "first item",
                    f"{min(max_items, 10)}th vehicle"  # Use actual max or 10th
                ]
                
                for phrase in test_phrases:
                    pos, ent = context.extract_ordinal_reference(f"Show me the {phrase}")
                    target = context.get_item_by_ordinal(pos) if pos and pos <= max_items else None
                    print(f"  '{phrase}' → position={pos}, entity={ent}, target={target}")
            else:
                print(f"❌ Not enough vehicles ({len(context.last_displayed_items)}) to test 7th vehicle")
                
        else:
            print("❌ No valid SQL generated for vehicle query")
            
    except Exception as e:
        print(f"❌ Database error: {e}")
    
    print("\n✅ Real Ordinal Reference Test Complete!")
    print(f"Total stored items: {len(context.last_displayed_items)}")
    print(f"Last result: {context.last_result.get('total_count', 'N/A')} rows" if context.last_result else "No last result")

if __name__ == "__main__":
    test_real_ordinal_references()
