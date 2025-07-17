#!/usr/bin/env python3
"""
Test script for ordinal reference and conversation context functionality
"""

from query_agent import ChatContext, english_to_sql, generate_final_response

def test_ordinal_references():
    """Test the enhanced ordinal reference functionality"""
    
    print("🧪 Testing Ordinal Reference & Conversation Context")
    print("=" * 60)
    
    # Create a chat context
    context = ChatContext()
    
    print("\n1️⃣ First Question: Show me all vehicles")
    result1 = english_to_sql("Show me all vehicles", chat_context=context)
    print(f"SQL: {result1.get('sql', 'None')}")
    
    # Simulate storing results from the first query
    mock_columns = ["reg_no", "vehicle_type", "region"]
    mock_rows = [
        ["UP16GT8409", "Truck", "North"],
        ["KA01AK6654", "Car", "South"], 
        ["KA01AM3985", "Van", "West"],
        ["KA51AH2981", "Truck", "East"],
        ["MH43BX5200", "Car", "Central"],
        ["PB65BB5450", "Bus", "North"],
        ["MH12SX6301", "Truck", "West"],  # This is the 7th vehicle
        ["KA01AH8095", "Car", "South"],
        ["TN37DL7178", "Van", "South"],
        ["TN30U7904", "Bus", "South"]
    ]
    
    # Add interaction with results
    context.add_interaction(
        "Show me all vehicles",
        "Here are all the vehicles in the fleet",
        sql_query="SELECT reg_no, vehicle_type, region FROM vehicles LIMIT 10",
        columns=mock_columns,
        rows=mock_rows
    )
    
    print(f"✅ Stored {len(context.last_displayed_items)} items with ordinal indexing")
    print(f"📊 7th vehicle should be: {context.last_displayed_items[6] if len(context.last_displayed_items) > 6 else 'Not found'}")
    
    print("\n2️⃣ Ordinal Reference Test: What region does the 7th vehicle belong to?")
    
    # Test ordinal extraction
    position, entity = context.extract_ordinal_reference("What region does the 7th vehicle belong to?")
    print(f"🎯 Extracted ordinal: position={position}, entity={entity}")
    
    if position:
        target_item = context.get_item_by_ordinal(position)
        print(f"🎯 Target item: {target_item}")
    
    # Test the full flow
    result2 = english_to_sql("What region does the 7th vehicle belong to?", chat_context=context)
    print(f"SQL: {result2.get('sql', 'None')}")
    print(f"Response: {result2.get('response', 'None')}")
    
    print("\n3️⃣ Specific Vehicle Test: Tell me about vehicle MH12SX6301")
    result3 = english_to_sql("Tell me about vehicle MH12SX6301", chat_context=context)
    print(f"SQL: {result3.get('sql', 'None')}")
    print(f"Response: {result3.get('response', 'None')}")
    
    print("\n4️⃣ Context Awareness Test: What about its maintenance records?")
    context_for_llm = context.get_context_for_llm("What about its maintenance records?")
    print(f"Context provided to LLM:\n{context_for_llm}")
    
    result4 = english_to_sql("What about its maintenance records?", chat_context=context)
    print(f"SQL: {result4.get('sql', 'None')}")
    
    print("\n5️⃣ Alternative Ordinal Test: Show me the first vehicle's details")
    result5 = english_to_sql("Show me the first vehicle's details", chat_context=context)
    print(f"SQL: {result5.get('sql', 'None')}")
    
    # Test different ordinal formats
    print("\n6️⃣ Testing Different Ordinal Formats:")
    test_phrases = [
        "2nd vehicle",
        "third vehicle", 
        "the 5th vehicle",
        "first item",
        "10th vehicle"
    ]
    
    for phrase in test_phrases:
        pos, ent = context.extract_ordinal_reference(f"Show me the {phrase}")
        print(f"  '{phrase}' → position={pos}, entity={ent}")
    
    print("\n✅ Ordinal Reference Test Complete!")
    print(f"Total stored items: {len(context.last_displayed_items)}")
    print(f"Last result has {context.last_result['total_count']} rows" if context.last_result else "No last result")

if __name__ == "__main__":
    test_ordinal_references()
