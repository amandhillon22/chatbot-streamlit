#!/usr/bin/env python3
"""
Minimal Emergency Connection Pool Test
Tests the database connection pool with minimal dependencies.
"""

import sys
import os
import time
import threading
import psycopg2
import psycopg2.pool
from concurrent.futures import ThreadPoolExecutor, as_completed

# Simple logging for this test
def log(message):
    timestamp = time.strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")

def test_direct_pool():
    """Test direct psycopg2 pool without our wrapper"""
    log("🔍 Testing direct psycopg2 pool...")
    
    # Database configuration (update as needed)
    db_config = {
        'host': os.getenv('hostname', 'localhost'),
        'database': os.getenv('dbname', 'rdc_dump'),
        'user': os.getenv('user_name', 'postgres'),
        'password': os.getenv('password', 'Akshit@123'),
        'port': int(os.getenv('port', 5432))
    }
    
    try:
        # Create pool with emergency settings
        pool = psycopg2.pool.ThreadedConnectionPool(
            minconn=5,
            maxconn=50,
            **db_config
        )
        
        log("✅ Pool created successfully")
        
        # Test getting connections
        connections = []
        for i in range(10):
            try:
                conn = pool.getconn()
                connections.append(conn)
                log(f"✅ Got connection {i+1}")
            except Exception as e:
                log(f"❌ Failed to get connection {i+1}: {e}")
                break
        
        # Test simple queries
        success_count = 0
        for i, conn in enumerate(connections):
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT current_timestamp, pg_backend_pid()")
                    result = cursor.fetchone()
                    success_count += 1
                    log(f"✅ Query {i+1} successful: PID {result[1]}")
            except Exception as e:
                log(f"❌ Query {i+1} failed: {e}")
        
        # Return connections
        for i, conn in enumerate(connections):
            try:
                pool.putconn(conn)
                log(f"✅ Returned connection {i+1}")
            except Exception as e:
                log(f"❌ Failed to return connection {i+1}: {e}")
        
        # Clean up
        pool.closeall()
        log("✅ Pool closed")
        
        log(f"📊 Results: {success_count}/{len(connections)} queries successful")
        return success_count == len(connections)
        
    except Exception as e:
        log(f"❌ Direct pool test failed: {e}")
        return False

def test_concurrent_direct(num_threads=15, queries_per_thread=3):
    """Test concurrent access to direct pool"""
    log(f"🔍 Testing {num_threads} concurrent threads with direct pool...")
    
    # Database configuration
    db_config = {
        'host': os.getenv('hostname', 'localhost'),
        'database': os.getenv('dbname', 'rdc_dump'),
        'user': os.getenv('user_name', 'postgres'),
        'password': os.getenv('password', 'Akshit@123'),
        'port': int(os.getenv('port', 5432))
    }
    
    try:
        # Create pool
        pool = psycopg2.pool.ThreadedConnectionPool(
            minconn=5,
            maxconn=50,
            **db_config
        )
        
        results = {'success': 0, 'failures': 0, 'errors': []}
        results_lock = threading.Lock()
        
        def worker_task(worker_id):
            """Worker function for concurrent testing"""
            for i in range(queries_per_thread):
                conn = None
                try:
                    start_time = time.time()
                    conn = pool.getconn()
                    
                    with conn.cursor() as cursor:
                        cursor.execute("SELECT current_timestamp, pg_backend_pid(), %s as worker_id", (worker_id,))
                        result = cursor.fetchone()
                    
                    pool.putconn(conn)
                    conn = None
                    
                    query_time = time.time() - start_time
                    
                    with results_lock:
                        results['success'] += 1
                        if query_time > 2.0:
                            log(f"⚠️ Worker {worker_id} query {i+1} took {query_time:.3f}s")
                            
                except Exception as e:
                    with results_lock:
                        results['failures'] += 1
                        results['errors'].append(f"Worker {worker_id}: {str(e)}")
                        log(f"❌ Worker {worker_id} query {i+1} failed: {e}")
                finally:
                    # Ensure connection is returned even on error
                    if conn:
                        try:
                            pool.putconn(conn)
                        except:
                            pass
        
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
        
        # Clean up pool
        pool.closeall()
        
        log(f"\n📊 Concurrent Test Results:")
        log(f"   Total Queries: {total_queries}")
        log(f"   Successful: {results['success']}")
        log(f"   Failed: {results['failures']}")
        log(f"   Success Rate: {(results['success']/total_queries)*100:.1f}%")
        log(f"   Total Time: {total_time:.3f}s")
        log(f"   Avg Query Time: {total_time/total_queries:.3f}s")
        
        if results['errors']:
            log(f"\n❌ First 3 Error Examples:")
            for error in results['errors'][:3]:
                log(f"   - {error}")
        
        return results['failures'] < (total_queries * 0.1)  # Allow 10% failure rate
        
    except Exception as e:
        log(f"❌ Concurrent test failed: {e}")
        return False

def main():
    """Run minimal emergency tests"""
    log("🚨 MINIMAL EMERGENCY CONNECTION POOL TEST")
    log("=" * 50)
    
    tests = [
        ("Direct Pool Basic", test_direct_pool),
        ("Direct Pool Concurrent", test_concurrent_direct)
    ]
    
    results = {}
    for test_name, test_func in tests:
        log(f"\n🧪 Running: {test_name}")
        log("-" * 30)
        try:
            results[test_name] = test_func()
        except Exception as e:
            log(f"❌ {test_name} crashed: {e}")
            results[test_name] = False
    
    # Summary
    log("\n" + "=" * 50)
    log("� MINIMAL TEST SUMMARY")
    log("=" * 50)
    
    passed = sum(1 for success in results.values() if success)
    total = len(results)
    
    for test_name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        log(f"{status} {test_name}")
    
    log(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        log("✅ 🎉 CONNECTION POOL STABLE!")
        return True
    else:
        log("❌ ⚠️ Connection pool needs attention")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
