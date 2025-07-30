#!/usr/bin/env python3
"""
Emergency Connection Pool Test
Tests the stabilized database connection pool after emergency fixes.
"""

import sys
import os
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import the stabilized components
from src.core.sql import DatabaseManager, system_monitor, chatbot_logger

def test_single_connection():
    """Test single connection acquisition and release"""
    print("🔍 Testing single connection...")
    try:
        db_manager = DatabaseManager()
        
        # Test connection acquisition
        start_time = time.time()
        with db_manager.get_connection_context() as conn:
            acquisition_time = time.time() - start_time
            print(f"✅ Connection acquired in {acquisition_time:.3f}s")
            
            # Test simple query
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1 as test")
                result = cursor.fetchone()
                print(f"✅ Query executed successfully: {result}")
        
        print("✅ Connection returned to pool successfully")
        return True
        
    except Exception as e:
        print(f"❌ Single connection test failed: {e}")
        return False

def test_concurrent_connections(num_threads=20, queries_per_thread=5):
    """Test concurrent connection usage"""
    print(f"🔍 Testing {num_threads} concurrent connections...")
    
    db_manager = DatabaseManager()
    results = {'success': 0, 'failures': 0, 'errors': []}
    results_lock = threading.Lock()
    
    def worker_task(worker_id):
        """Worker function for concurrent testing"""
        for i in range(queries_per_thread):
            try:
                start_time = time.time()
                with db_manager.get_connection_context() as conn:
                    with conn.cursor() as cursor:
                        cursor.execute("SELECT current_timestamp, pg_backend_pid()")
                        result = cursor.fetchone()
                        
                query_time = time.time() - start_time
                
                with results_lock:
                    results['success'] += 1
                    if query_time > 2.0:
                        print(f"⚠️ Worker {worker_id} query {i+1} took {query_time:.3f}s")
                        
            except Exception as e:
                with results_lock:
                    results['failures'] += 1
                    results['errors'].append(f"Worker {worker_id}: {str(e)}")
                    print(f"❌ Worker {worker_id} query {i+1} failed: {e}")
    
    # Execute concurrent tasks
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(worker_task, i) for i in range(num_threads)]
        
        # Wait for all tasks to complete
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                with results_lock:
                    results['failures'] += 1
                    results['errors'].append(f"Thread execution error: {str(e)}")
    
    total_time = time.time() - start_time
    total_queries = num_threads * queries_per_thread
    
    print(f"\n📊 Concurrent Test Results:")
    print(f"   Total Queries: {total_queries}")
    print(f"   Successful: {results['success']}")
    print(f"   Failed: {results['failures']}")
    print(f"   Success Rate: {(results['success']/total_queries)*100:.1f}%")
    print(f"   Total Time: {total_time:.3f}s")
    print(f"   Avg Query Time: {total_time/total_queries:.3f}s")
    
    if results['errors']:
        print(f"\n❌ First 3 Error Examples:")
        for error in results['errors'][:3]:
            print(f"   - {error}")
    
    return results['failures'] == 0

def test_pool_status():
    """Test pool status monitoring"""
    print("🔍 Testing pool status monitoring...")
    try:
        db_manager = DatabaseManager()
        status = db_manager.get_pool_status()
        
        print(f"📊 Pool Status: {status}")
        print(f"📊 Connection Stats: {system_monitor.connection_stats}")
        
        return True
    except Exception as e:
        print(f"❌ Pool status test failed: {e}")
        return False

def test_cleanup_mechanism():
    """Test emergency cleanup mechanism"""
    print("🔍 Testing emergency cleanup mechanism...")
    try:
        db_manager = DatabaseManager()
        
        # Get initial stats
        initial_stats = system_monitor.connection_stats.copy()
        print(f"📊 Initial Stats: {initial_stats}")
        
        # Trigger cleanup
        db_manager.cleanup_stale_connections()
        print("✅ Emergency cleanup executed successfully")
        
        # Verify pool still works after cleanup
        with db_manager.get_connection_context() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 'cleanup_test' as test")
                result = cursor.fetchone()
                print(f"✅ Post-cleanup query successful: {result}")
        
        return True
    except Exception as e:
        print(f"❌ Cleanup test failed: {e}")
        return False

def main():
    """Run all emergency tests"""
    print("🚨 EMERGENCY CONNECTION POOL STABILITY TEST")
    print("=" * 50)
    
    tests = [
        ("Single Connection", test_single_connection),
        ("Pool Status", test_pool_status),
        ("Emergency Cleanup", test_cleanup_mechanism),
        ("Concurrent Connections", lambda: test_concurrent_connections(15, 3))
    ]
    
    results = {}
    for test_name, test_func in tests:
        print(f"\n🧪 Running: {test_name}")
        print("-" * 30)
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 EMERGENCY TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for success in results.values() if success)
    total = len(results)
    
    for test_name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ 🎉 ALL EMERGENCY TESTS PASSED - System Stable!")
        return True
    else:
        print("❌ ⚠️ Some tests failed - System needs attention")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
