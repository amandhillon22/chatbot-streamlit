#!/usr/bin/env python3
"""
import sys
sys.path.append('/home/linux/Documents/chatbot-diya')

Test script for conversation context functionality
"""

from src.core.query_agent import ChatContext, english_to_sql, generate_final_response

def test_conversation_context():
    """Test the enhanced conversation context functionality"""
    
    print("🧪 Testing Enhanced Conversation Context")
    print("=" * 50)
    
    # Create a chat context
    context = ChatContext()
    
    # Simulate a conversation
    print("\n1️⃣ First Question: Show me all vehicles")
    result1 = english_to_sql("Show me all vehicles", chat_context=context)
    print(f"SQL: {result1.get('sql', 'None')}")
    
    # Add interaction manually for testing
    context.add_interaction(
        "Show me all vehicles",
        "Here are all the vehicles in the fleet",
        sql_query="SELECT * FROM vehicles LIMIT 10",
        columns=["id", "registration_number", "model"],
        rows=[["1", "ABC123", "Toyota Camry"], ["2", "XYZ789", "Ford Transit"]]
    )
    
    print(f"Topics extracted: {context.key_topics}")
    print(f"Conversation summary: {context.conversation_summary}")
    
    print("\n2️⃣ Follow-up Question: What about their fuel consumption?")
    result2 = english_to_sql("What about their fuel consumption?", chat_context=context)
    print(f"SQL: {result2.get('sql', 'None')}")
    
    context.add_interaction(
        "What about their fuel consumption?",
        "Here's the fuel consumption data for those vehicles",
        sql_query="SELECT registration_number, avg_fuel_consumption FROM vehicles",
        columns=["registration_number", "avg_fuel_consumption"],
        rows=[["ABC123", "8.5"], ["XYZ789", "12.3"]]
    )
    
    print(f"Updated topics: {context.key_topics}")
    print(f"Updated summary: {context.conversation_summary}")
    
    print("\n3️⃣ Tricky Question: Which one is more efficient?")
    context_for_llm = context.get_context_for_llm("Which one is more efficient?")
    print(f"Context for LLM: {context_for_llm}")
    
    result3 = english_to_sql("Which one is more efficient?", chat_context=context)
    print(f"SQL: {result3.get('sql', 'None')}")
    print(f"Response: {result3.get('response', 'None')}")
    
    print("\n4️⃣ Counter Question: But I thought you said XYZ789 was better?")
    result4 = english_to_sql("But I thought you said XYZ789 was better?", chat_context=context)
    print(f"Response: {result4.get('response', 'None')}")
    
    print("\n5️⃣ Test Error Handling: Empty context")
    empty_context = ChatContext()
    result5 = english_to_sql("Hello", chat_context=empty_context)
    print(f"Response with empty context: {result5.get('response', 'None')}")
    
    print("\n✅ Conversation Context Test Complete!")
    print(f"Final conversation summary: {context.conversation_summary}")
    print(f"Key topics tracked: {context.key_topics}")
    print(f"Last SQL queries: {context.last_sql_queries}")
    print(f"Total interactions: {len(context.history)}")

if __name__ == "__main__":
    test_conversation_context()
