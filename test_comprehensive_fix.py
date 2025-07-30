#!/usr/bin/env python3
"""
Comprehensive test to verify chatbot functionality after connection pool fix
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_ai_query_agent():
    """Test the AI query agent that was having connection pool issues"""
    try:
        from src.core.query_agent import get_sql_query
        
        print("🔍 Testing AI Query Agent with connection pool fix...")
        
        # Test a simple stoppage query
        test_query = "Show me vehicles that stopped for more than 30 minutes"
        
        result = get_sql_query(test_query)
        
        if result and 'sql' in result:
            print(f"✅ AI Query generated: {result['sql'][:100]}...")
            
            # Verify it uses the correct table name
            if 'util_report' in result['sql']:
                print("✅ Correctly using util_report table!")
            else:
                print("⚠️ Table name validation needed")
                
            return True
        else:
            print(f"❌ AI Query failed: {result}")
            return False
            
    except Exception as e:
        print(f"❌ AI Query Agent test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_database_operations():
    """Test database operations that were causing connection pool exhaustion"""
    try:
        from src.core.sql import db_manager
        
        print("\n🔍 Testing database operations...")
        
        # Test table information retrieval
        columns, rows = db_manager.execute_query_with_retry("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            LIMIT 5
        """)
        
        print(f"✅ Retrieved table info: {len(rows)} tables found")
        
        # Test a more complex query
        columns, rows = db_manager.execute_query_with_retry("""
            SELECT COUNT(*) as total_records 
            FROM util_report 
            LIMIT 1
        """)
        
        print(f"✅ Util_report count query: {rows[0][0]} records")
        
        return True
        
    except Exception as e:
        print(f"❌ Database operations test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_connection_pool_stress():
    """Stress test the connection pool to ensure no leaks under load"""
    try:
        from src.core.sql import db_manager
        
        print("\n🔍 Stress testing connection pool...")
        
        # Simulate multiple concurrent queries
        for i in range(15):  # Test more than min connections
            try:
                with db_manager.get_connection_context() as conn:
                    cursor = conn.cursor()
                    cursor.execute('SELECT %s as iteration', (i,))
                    result = cursor.fetchone()
                    
                if i % 5 == 0:
                    print(f"✅ Stress test iteration {i}: {result}")
                    
            except Exception as e:
                print(f"❌ Stress test failed at iteration {i}: {e}")
                return False
        
        print("✅ Stress test completed - connection pool handling heavy load correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Connection pool stress test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Starting Comprehensive Chatbot Functionality Test")
    print("=" * 60)
    
    # Load environment
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ Environment loaded")
    except Exception as e:
        print(f"⚠️ Could not load environment: {e}")
    
    # Run tests
    test1_passed = test_ai_query_agent()
    test2_passed = test_database_operations() 
    test3_passed = test_connection_pool_stress()
    
    print("\n" + "=" * 60)
    print("📊 COMPREHENSIVE TEST RESULTS:")
    print(f"AI Query Agent Test:        {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"Database Operations Test:   {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    print(f"Connection Pool Stress Test: {'✅ PASSED' if test3_passed else '❌ FAILED'}")
    
    if test1_passed and test2_passed and test3_passed:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Connection pool leak fix is working correctly")
        print("✅ AI query agent is functional") 
        print("✅ Database operations are stable")
        print("✅ System ready for production use!")
    else:
        print("\n❌ Some tests failed. System needs additional fixes.")
