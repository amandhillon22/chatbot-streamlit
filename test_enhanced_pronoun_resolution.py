#!/usr/bin/env python3
"""
Test script for enhanced pronoun resolution functionality
Demonstrates how the chatbot now handles follow-up questions with pronouns
"""

from query_agent import ChatContext, english_to_sql, generate_final_response

def test_enhanced_pronoun_resolution():
    """Test the enhanced pronoun resolution system"""
    
    print("🧪 Testing Enhanced Pronoun Resolution System")
    print("=" * 60)
    
    # Create a chat context
    context = ChatContext()
    
    print("\n1️⃣ STEP 1: Initial Query - Show vehicles")
    print("-" * 40)
    
    # Simulate an initial query that returns vehicle data
    initial_query = "show me all vehicles"
    result1 = english_to_sql(initial_query, chat_context=context)
    print(f"Query: '{initial_query}'")
    print(f"SQL Generated: {result1.get('sql', 'None')[:100]}...")
    
    # Simulate storing results from the initial query
    mock_columns = ["reg_no", "vehicle_type", "plant_id", "region"]
    mock_rows = [
        ["UP16GT8409", "Truck", 460, "North"],
        ["KA01AK6654", "Car", 461, "South"], 
        ["KA01AM3985", "Van", 462, "West"],
        ["KA51AH2981", "Truck", 463, "East"],
        ["MH43BX5200", "Car", 464, "Central"]
    ]
    
    # Store results in context
    context.store_displayed_results(mock_columns, mock_rows, initial_query, result1.get('sql'))
    print(f"✅ Stored {len(mock_rows)} vehicles in context")
    
    print("\n2️⃣ STEP 2: Testing Pronoun Resolution Follow-ups")
    print("-" * 40)
    
    # Test various pronoun-based follow-up queries
    test_queries = [
        "show their details",
        "what are their plant names", 
        "tell me more about them",
        "show me their complete information",
        "list their registration numbers",
        "what is their region information",
        "display all their details",
        "show me information about those vehicles",
        "give me more details about them"
    ]
    
    successful_resolutions = 0
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Testing: '{query}'")
        
        try:
            result = english_to_sql(query, chat_context=context)
            
            if result.get('context_resolution_applied'):
                print(f"   ✅ PRONOUN RESOLVED! Generated SQL")
                print(f"   🎯 Reasoning: {result.get('reasoning', 'N/A')}")
                print(f"   🔧 SQL: {result.get('sql', 'None')[:100]}...")
                print(f"   💬 Response: {result.get('response', 'N/A')[:80]}...")
                successful_resolutions += 1
            elif result.get('sql') and 'clarify' not in result.get('response', '').lower():
                print(f"   ✅ NORMAL SQL: {result.get('sql', 'None')[:100]}...")
                successful_resolutions += 1
            else:
                print(f"   ❌ Asked for clarification or no SQL generated")
                if result.get('response'):
                    print(f"      Response: {result.get('response')[:80]}...")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print(f"\n📊 RESULTS SUMMARY:")
    print(f"   • Total queries tested: {len(test_queries)}")
    print(f"   • Successfully resolved: {successful_resolutions}")
    print(f"   • Success rate: {(successful_resolutions/len(test_queries)*100):.1f}%")
    
    print("\n3️⃣ STEP 3: Testing Different Entity Types")
    print("-" * 40)
    
    # Test with plant data
    plant_columns = ["id_no", "name", "address", "region"]
    plant_rows = [
        [460, "PB-Mohali", "123 Industrial Area", "Punjab"],
        [461, "PB-Ludhiana", "456 Factory Street", "Punjab"]
    ]
    
    context.store_displayed_results(plant_columns, plant_rows, "show all plants", "SELECT * FROM hosp_master")
    print("✅ Stored plant data in context")
    
    plant_queries = [
        "show their addresses",
        "what are their regions",
        "tell me more about those plants"
    ]
    
    plant_resolutions = 0
    
    for query in plant_queries:
        print(f"\nTesting plant query: '{query}'")
        try:
            result = english_to_sql(query, chat_context=context)
            if result.get('context_resolution_applied') or (result.get('sql') and 'clarify' not in result.get('response', '').lower()):
                print(f"   ✅ Resolved successfully")
                plant_resolutions += 1
            else:
                print(f"   ❌ Failed to resolve")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print(f"\n📊 Plant Query Results: {plant_resolutions}/{len(plant_queries)} successful")
    
    print("\n4️⃣ STEP 4: Testing Edge Cases")
    print("-" * 40)
    
    edge_cases = [
        "show details",  # Generic - should work with context
        "more information",  # Vague - should work with context  
        "tell me about it",  # Singular pronoun
        "what about those?",  # Vague demonstrative
    ]
    
    edge_resolutions = 0
    
    for query in edge_cases:
        print(f"\nTesting edge case: '{query}'")
        try:
            result = english_to_sql(query, chat_context=context)
            if result.get('context_resolution_applied') or (result.get('sql') and 'clarify' not in result.get('response', '').lower()):
                print(f"   ✅ Handled appropriately")
                edge_resolutions += 1
            else:
                print(f"   ⚠️ Asked for clarification (may be appropriate)")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print(f"\n📊 Edge Case Results: {edge_resolutions}/{len(edge_cases)} resolved")
    
    print(f"\n🎉 OVERALL RESULTS:")
    print(f"   • Vehicle pronouns: {successful_resolutions}/{len(test_queries)}")
    print(f"   • Plant pronouns: {plant_resolutions}/{len(plant_queries)}")
    print(f"   • Edge cases: {edge_resolutions}/{len(edge_cases)}")
    
    total_tested = len(test_queries) + len(plant_queries) + len(edge_cases)
    total_resolved = successful_resolutions + plant_resolutions + edge_resolutions
    overall_rate = (total_resolved / total_tested * 100) if total_tested > 0 else 0
    
    print(f"   • Overall success rate: {overall_rate:.1f}%")
    
    if overall_rate >= 70:
        print("   ✅ EXCELLENT: Pronoun resolution working well!")
    elif overall_rate >= 50:
        print("   ⚠️  GOOD: Some improvement needed")
    else:
        print("   ❌ NEEDS WORK: Significant improvements required")
    
    print("\n✅ Enhanced Pronoun Resolution Test Complete!")

if __name__ == "__main__":
    test_enhanced_pronoun_resolution()
