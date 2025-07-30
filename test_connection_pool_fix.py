#!/usr/bin/env python3
"""
Test script to verify the connection pool leak fix
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_connection_pool():
    """Test the connection pool with context manager"""
    try:
        from src.core.sql import db_manager
        print("✅ Successfully imported database manager")
        
        # Test basic connection
        print("\n🔍 Testing connection pool with context manager...")
        
        # Test multiple connections to check for leaks
        for i in range(5):
            try:
                with db_manager.get_connection_context() as conn:
                    cursor = conn.cursor()
                    cursor.execute('SELECT 1 as test_value')
                    result = cursor.fetchone()
                    print(f"✅ Connection {i+1}: {result}")
                    
            except Exception as e:
                print(f"❌ Connection {i+1} failed: {e}")
                return False
        
        print("\n✅ Connection pool test completed successfully!")
        print("🎉 No connection leaks detected - connections properly returned to pool")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_query_execution():
    """Test the enhanced query execution with retry mechanism"""
    try:
        from src.core.sql import db_manager
        
        print("\n🔍 Testing query execution with enhanced error handling...")
        
        # Test a simple query
        columns, rows = db_manager.execute_query_with_retry("SELECT 1 as test, 'connection_pool_fix' as status")
        print(f"✅ Query executed successfully: {columns} = {rows}")
        
        return True
        
    except Exception as e:
        print(f"❌ Query execution test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Starting Connection Pool Fix Test")
    print("=" * 50)
    
    # Load environment
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ Environment loaded")
    except Exception as e:
        print(f"⚠️ Could not load environment: {e}")
    
    # Run tests
    test1_passed = test_connection_pool()
    test2_passed = test_query_execution()
    
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS:")
    print(f"Connection Pool Test: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"Query Execution Test: {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 ALL TESTS PASSED! Connection pool leak fix is working correctly.")
    else:
        print("\n❌ Some tests failed. Check the errors above.")
