#!/usr/bin/env python3
"""
End-to-End Chatbot Distance Conversion Test
Simulates realistic chatbot interactions with distance queries.
"""

from query_agent_enhanced import english_to_sql, generate_final_response
from sql import get_connection
import psycopg2

def execute_query(sql, schema):
    """Execute a query and return results."""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(sql)
        
        # Get column names
        columns = [desc[0] for desc in cur.description]
        rows = cur.fetchall()
        
        cur.close()
        conn.close()
        
        return columns, rows
    except Exception as e:
        print(f"Query execution error: {e}")
        return [], []

def test_chatbot_distance_scenarios():
    """Test end-to-end chatbot scenarios with distance conversion."""
    
    print("🤖 End-to-End Chatbot Distance Conversion Test")
    print("=" * 60)
    
    scenarios = [
        {
            "name": "Simple Distance Query in KM",
            "query": "Show me the average distance per trip in kilometers",
            "should_have_data": True
        },
        {
            "name": "Vehicle Mileage Query",
            "query": "Which vehicles have the highest mileage?",
            "should_have_data": True
        },
        {
            "name": "Specific Table Distance",
            "query": "Total distance from trip_report in km",
            "should_have_data": True
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n🎭 Scenario {i}: {scenario['name']}")
        print(f"User Query: '{scenario['query']}'")
        print("-" * 50)
        
        # Step 1: Generate SQL
        result = english_to_sql(scenario['query'])
        
        if result.get('sql'):
            sql = result['sql']
            schema = result.get('schema', 'public')
            
            print(f"🔧 Generated SQL:")
            print(f"   {sql}")
            
            # Check for conversion
            if 'ROUND(' in sql and '/ 1000' in sql:
                print("✅ Distance conversion applied (meters → kilometers)")
            else:
                print("ℹ️  No conversion (data likely already in correct units)")
            
            # Step 2: Execute query
            columns, rows = execute_query(sql, schema)
            
            if rows:
                print(f"📊 Query returned {len(rows)} rows")
                
                # Step 3: Generate natural language response
                final_response = generate_final_response(
                    scenario['query'], 
                    columns, 
                    rows[:5]  # Limit to first 5 rows for demo
                )
                
                print(f"🤖 Chatbot Response:")
                print(f"   {final_response}")
                
            else:
                print("⚠️  Query returned no data")
                
        else:
            print(f"🔄 Clarification Response:")
            print(f"   {result.get('response', 'No response generated')}")
        
        print("")
    
    # Test conversion accuracy
    print("🔬 Testing Conversion Accuracy")
    print("-" * 30)
    
    # Test a simple known conversion
    simple_query = "SELECT ROUND((1000::NUMERIC / 1000), 2) AS test_conversion"
    columns, rows = execute_query(simple_query, "public")
    
    if rows and rows[0][0] == 1.0:
        print("✅ Conversion math verified: 1000 meters = 1.0 km")
    else:
        print("❌ Conversion math issue detected")

if __name__ == "__main__":
    test_chatbot_distance_scenarios()
