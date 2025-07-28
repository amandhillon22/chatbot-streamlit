#!/usr/bin/env python3
"""
Test vehicle stoppage report SQL generation
"""

import sys
import os
sys.path.append('/home/linux/Documents/chatbot-diya')

def test_stoppage_sql_generation():
    """Test SQL generation for vehicle stoppage reports"""
    try:
        from src.core.query_agent import english_to_sql
        
        # Test various stoppage-related queries
        test_queries = [
            "Show me vehicle stoppage reports",
            "Get vehicle tracking data for today",
            "Show vehicles with long stoppages",
            "Display overspeeding vehicles",
            "Vehicle stoppage details with location"
        ]
        
        print("🚗 Testing Vehicle Stoppage SQL Generation")
        print("=" * 60)
        
        for query in test_queries:
            print(f"\n📝 Query: '{query}'")
            print("-" * 40)
            
            try:
                result = english_to_sql(query)
                
                if result and isinstance(result, dict):
                    if 'sql' in result:
                        sql = result['sql']
                        if sql:  # Check if SQL is not None
                            print(f"✅ Generated SQL:")
                            print(f"   {sql}")
                            
                            # Check if util_report is mentioned
                            if 'util_report' in sql.lower():
                                print("✅ util_report table correctly used")
                            else:
                                print("⚠️ util_report table not found in query")
                        else:
                            print("❌ SQL is None")
                            
                    else:
                        print(f"❌ No SQL in result. Result keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
                else:
                    print(f"❌ Unexpected result format: {result}")
                    
            except Exception as e:
                print(f"❌ Error generating SQL: {e}")
                import traceback
                traceback.print_exc()
                
    except Exception as e:
        print(f"❌ Setup error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_stoppage_sql_generation()
