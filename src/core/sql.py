import psycopg2
from psycopg2 import pool
from psycopg2.pool import ThreadedConnectionPool
import os
import sys
import time
import threading
import logging
import logging.handlers
from contextlib import contextmanager
from typing import Optional, Any, Dict, List, Tuple
from enum import Enum
from dataclasses import dataclass
from datetime import datetime

# Optional Redis import
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    redis = None

import hashlib
import json
from decimal import Decimal
from concurrent.futures import ThreadPoolExecutor
from functools import wraps
sys.path.append('/home/linux/Documents/chatbot-diya')

from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# Custom JSON encoder to handle Decimal objects from PostgreSQL
class DecimalEncoder(json.JSONEncoder):
    """Custom JSON encoder that converts Decimal objects to float for JSON serialization"""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

# Enhanced Error Handling System
class ErrorType(Enum):
    DATABASE_CONNECTION = "db_connection"
    SQL_SYNTAX = "sql_syntax"
    PERMISSION_DENIED = "permission"
    TABLE_NOT_FOUND = "table_missing"
    TIMEOUT = "timeout"
    NETWORK = "network"
    POOL_EXHAUSTED = "pool_exhausted"
    UNKNOWN = "unknown"

@dataclass
class DatabaseError:
    error_type: ErrorType
    message: str
    user_message: str
    query: Optional[str] = None
    suggestion: Optional[str] = None
    can_retry: bool = False

class ErrorClassifier:
    @staticmethod
    def classify_error(exception: Exception, query: str = None) -> DatabaseError:
        error_str = str(exception).lower()
        
        if "connection" in error_str or "connect" in error_str or "could not connect" in error_str:
            return DatabaseError(
                error_type=ErrorType.DATABASE_CONNECTION,
                message=str(exception),
                user_message="Database is temporarily unavailable. Please try again in a moment.",
                query=query,
                suggestion="Check database connection or try again in a moment",
                can_retry=True
            )
        elif "syntax error" in error_str or "invalid sql" in error_str:
            return DatabaseError(
                error_type=ErrorType.SQL_SYNTAX,
                message=str(exception),
                user_message="There was an issue with your request. Please try rephrasing it.",
                query=query,
                suggestion="Try asking in simpler terms or check query syntax"
            )
        elif "permission denied" in error_str or "access denied" in error_str:
            return DatabaseError(
                error_type=ErrorType.PERMISSION_DENIED,
                message=str(exception),
                user_message="Access denied. Please contact your administrator.",
                query=query,
                suggestion="User needs proper database permissions"
            )
        elif "does not exist" in error_str or "relation" in error_str and "does not exist" in error_str:
            return DatabaseError(
                error_type=ErrorType.TABLE_NOT_FOUND,
                message=str(exception),
                user_message="The requested data is not available in the system.",
                query=query,
                suggestion="Check if the table/column exists in database"
            )
        elif "timeout" in error_str or "timed out" in error_str:
            return DatabaseError(
                error_type=ErrorType.TIMEOUT,
                message=str(exception),
                user_message="Your query is taking too long. Please try a more specific request.",
                query=query,
                suggestion="Optimize query or add more filters",
                can_retry=True
            )
        elif "pool" in error_str and "exhausted" in error_str:
            return DatabaseError(
                error_type=ErrorType.POOL_EXHAUSTED,
                message=str(exception),
                user_message="System is busy. Please try again in a moment.",
                query=query,
                suggestion="Connection pool is exhausted, consider increasing pool size",
                can_retry=True
            )
        else:
            return DatabaseError(
                error_type=ErrorType.UNKNOWN,
                message=str(exception),
                user_message="Something went wrong. Please try again or contact support.",
                query=query,
                suggestion="Unknown error - may need investigation"
            )

class ChatbotLogger:
    def __init__(self):
        # Create logs directory if it doesn't exist
        log_dir = '/home/linux/Documents/chatbot-diya/logs'
        os.makedirs(log_dir, exist_ok=True)
        
        # Configure main logger
        self.logger = logging.getLogger('chatbot_diya')
        self.logger.setLevel(logging.INFO)
        
        # Remove existing handlers to avoid duplicates
        if self.logger.handlers:
            self.logger.handlers.clear()
        
        # File handler with rotation (keeps 10 files of 10MB each)
        file_handler = logging.handlers.RotatingFileHandler(
            f'{log_dir}/chatbot.log',
            maxBytes=10*1024*1024,  # 10MB
            backupCount=10
        )
        
        # Console handler for immediate feedback
        console_handler = logging.StreamHandler()
        
        # Detailed formatter for files
        file_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(name)s | %(funcName)s:%(lineno)d | %(message)s'
        )
        
        # Simple formatter for console
        console_formatter = logging.Formatter(
            '%(levelname)s: %(message)s'
        )
        
        file_handler.setFormatter(file_formatter)
        console_handler.setFormatter(console_formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        # Error-specific logger
        self.error_logger = logging.getLogger('chatbot_errors')
        self.error_logger.setLevel(logging.ERROR)
        error_handler = logging.handlers.RotatingFileHandler(
            f'{log_dir}/errors.log',
            maxBytes=5*1024*1024,  # 5MB
            backupCount=5
        )
        error_handler.setFormatter(file_formatter)
        self.error_logger.addHandler(error_handler)
    
    def log_query(self, query: str, execution_time: float, row_count: int):
        """Log successful query execution"""
        self.logger.info(f"QUERY_SUCCESS | Time: {execution_time:.3f}s | Rows: {row_count} | SQL: {query[:100]}...")
    
    def log_error(self, error: DatabaseError, user_id: str = "anonymous"):
        """Log detailed error information"""
        self.error_logger.error(
            f"ERROR_TYPE: {error.error_type.value} | USER: {user_id} | "
            f"MESSAGE: {error.message} | QUERY: {error.query}"
        )
        self.logger.warning(f"User error: {error.user_message}")
    
    def log_performance(self, operation: str, duration: float, details: str = ""):
        """Log performance metrics"""
        self.logger.info(f"PERFORMANCE | {operation} | {duration:.3f}s | {details}")
    
    def log_pool_status(self, status: dict):
        """Log connection pool health"""
        self.logger.info(f"POOL_STATUS | {status}")

class SystemMonitor:
    def __init__(self):
        self.metrics = {
            'total_queries': 0,
            'successful_queries': 0,
            'failed_queries': 0,
            'avg_response_time': 0,
            'error_counts': {},
            'last_health_check': None
        }
        self.connection_stats = {
            'total_acquired': 0,
            'total_returned': 0,
            'failed_acquisitions': 0
        }
        self.performance_stats = {
            'total_execution_time': 0,
            'total_rows_returned': 0,
            'fastest_query': float('inf'),
            'slowest_query': 0
        }
        self.alert_thresholds = {
            'error_rate': 0.1,  # 10% error rate triggers alert
            'response_time': 5.0,  # 5 second response time threshold
            'failed_connections': 5  # 5 failed connections in a row
        }
    
    def record_query(self, success: bool, response_time: float, error_type: str = None):
        """Record query metrics"""
        self.metrics['total_queries'] += 1
        
        if success:
            self.metrics['successful_queries'] += 1
        else:
            self.metrics['failed_queries'] += 1
            if error_type:
                self.metrics['error_counts'][error_type] = self.metrics['error_counts'].get(error_type, 0) + 1
        
        # Update average response time
        if self.metrics['total_queries'] > 0:
            total_time = self.metrics['avg_response_time'] * (self.metrics['total_queries'] - 1) + response_time
            self.metrics['avg_response_time'] = total_time / self.metrics['total_queries']
        
        # Check for alerts
        self._check_alerts()
    
    def update_performance_metrics(self, execution_time: float, rows_returned: int):
        """Update performance tracking metrics"""
        self.performance_stats['total_execution_time'] += execution_time
        self.performance_stats['total_rows_returned'] += rows_returned
        
        # Track fastest and slowest queries
        if execution_time < self.performance_stats['fastest_query']:
            self.performance_stats['fastest_query'] = execution_time
        if execution_time > self.performance_stats['slowest_query']:
            self.performance_stats['slowest_query'] = execution_time
    
    def _check_alerts(self):
        """Check if any metrics exceed thresholds"""
        if self.metrics['total_queries'] > 10:  # Only check after some queries
            error_rate = self.metrics['failed_queries'] / self.metrics['total_queries']
            
            if error_rate > self.alert_thresholds['error_rate']:
                chatbot_logger.logger.error(f"HIGH ERROR RATE ALERT: {error_rate:.2%} (threshold: {self.alert_thresholds['error_rate']:.1%})")
            
            if self.metrics['avg_response_time'] > self.alert_thresholds['response_time']:
                chatbot_logger.logger.warning(f"SLOW RESPONSE ALERT: {self.metrics['avg_response_time']:.2f}s average")
    
    def get_health_report(self) -> dict:
        """Generate system health report"""
        if self.metrics['total_queries'] == 0:
            return {"status": "no_data", "message": "No queries processed yet"}
        
        error_rate = self.metrics['failed_queries'] / self.metrics['total_queries']
        
        if error_rate < 0.05:  # Less than 5% errors
            status = "healthy"
        elif error_rate < 0.15:  # Less than 15% errors
            status = "warning"
        else:
            status = "critical"
        
        return {
            "status": status,
            "total_queries": self.metrics['total_queries'],
            "success_rate": f"{((self.metrics['successful_queries'] / self.metrics['total_queries']) * 100):.1f}%",
            "avg_response_time": f"{self.metrics['avg_response_time']:.2f}s",
            "top_errors": sorted(self.metrics['error_counts'].items(), key=lambda x: x[1], reverse=True)[:3],
            "connection_stats": self.connection_stats,
            "performance_stats": self.performance_stats
        }

class DatabaseRecoveryManager:
    def __init__(self):
        self.retry_counts = {}
        self.max_retries = 3
        self.retry_delay_base = 0.5
    
    def should_retry(self, error_type: ErrorType, query_hash: str) -> bool:
        """Determine if we should retry this type of error"""
        if error_type in [ErrorType.DATABASE_CONNECTION, ErrorType.TIMEOUT, ErrorType.POOL_EXHAUSTED]:
            retry_count = self.retry_counts.get(query_hash, 0)
            return retry_count < self.max_retries
        return False
    
    def is_retryable_error(self, error_type: ErrorType) -> bool:
        """Check if this error type can be retried"""
        retryable_errors = [
            ErrorType.DATABASE_CONNECTION,
            ErrorType.TIMEOUT,
            ErrorType.POOL_EXHAUSTED,
            ErrorType.NETWORK
        ]
        return error_type in retryable_errors
    
    def get_retry_delay(self, attempt: int) -> float:
        """Get delay time for retry attempt with exponential backoff"""
        return self.retry_delay_base * (2 ** attempt)
    
    def increment_retry_count(self, query_hash: str):
        """Increment retry count for a query"""
        self.retry_counts[query_hash] = self.retry_counts.get(query_hash, 0) + 1
    
    def clear_retry_count(self, query_hash: str):
        """Clear retry count for successful query"""
        if query_hash in self.retry_counts:
            del self.retry_counts[query_hash]

# Global instances
chatbot_logger = ChatbotLogger()
system_monitor = SystemMonitor()
recovery_manager = DatabaseRecoveryManager()

class DatabaseConnectionManager:
    """Enhanced database connection manager with connection pooling and error handling"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, '_initialized'):
            return
            
        self._pool = None
        self._pool_lock = threading.Lock()
        self.db_config = {
            'host': os.getenv('hostname', 'localhost'),
            'database': os.getenv('dbname', 'rdc_dump'),
            'user': os.getenv('user_name', 'postgres'),
            'password': os.getenv('password', 'Akshit@123'),
            'port': int(os.getenv('port', 5432))
        }
        self.pool_config = {
            'minconn': int(os.getenv('DB_MIN_CONNECTIONS', 5)),
            'maxconn': int(os.getenv('DB_MAX_CONNECTIONS', 50)),  # Increased from 20 to 50
            'timeout': int(os.getenv('DB_CONNECTION_TIMEOUT', 10))  # Reduced from 30 to 10
        }
        self._initialize_pool()
        self._initialized = True
    
    def _initialize_pool(self):
        """Initialize the connection pool with comprehensive error handling"""
        try:
            with self._pool_lock:
                if self._pool:
                    self._pool.closeall()
                
                self._pool = ThreadedConnectionPool(
                    minconn=self.pool_config['minconn'],
                    maxconn=self.pool_config['maxconn'],
                    **self.db_config
                )
            
            chatbot_logger.logger.info(f"Database connection pool initialized successfully (min: {self.pool_config['minconn']}, max: {self.pool_config['maxconn']})")
            print(f"✅ Database connection pool initialized (min: {self.pool_config['minconn']}, max: {self.pool_config['maxconn']})")
        except Exception as e:
            error_msg = f"Failed to initialize connection pool: {e}"
            chatbot_logger.logger.error(error_msg)
            print(f"❌ {error_msg}")
            raise
    
    @contextmanager
    def get_connection_context(self):
        """
        Context manager for safe connection handling - ALWAYS use this for new code
        
        Usage:
            with db_manager.get_connection_context() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                result = cursor.fetchall()
        """
        conn = None
        try:
            conn = self.get_connection()
            yield conn
        finally:
            if conn:
                self.return_connection(conn)
    
    def get_connection(self):
        """Get a connection from the pool with comprehensive monitoring"""
        if not self._pool:
            self._initialize_pool()
        
        start_time = time.time()
        try:
            with self._pool_lock:
                conn = self._pool.getconn()
            wait_time = time.time() - start_time
            
            # Monitor connection acquisition performance
            system_monitor.connection_stats['total_acquired'] += 1
            if wait_time > 1:  # Log slow connection acquisition
                chatbot_logger.logger.warning(f"Slow connection acquisition: {wait_time:.2f}s")
                print(f"⚠️ Connection acquired in {wait_time:.2f}s (slower than expected)")
            
            return conn
            
        except Exception as e:
            wait_time = time.time() - start_time
            system_monitor.connection_stats['failed_acquisitions'] += 1
            
            # Auto-cleanup if too many failures
            if system_monitor.connection_stats['failed_acquisitions'] >= 10:
                chatbot_logger.logger.warning("🚨 High connection failure rate detected, triggering cleanup")
                print("🚨 Auto-triggering connection cleanup due to failures")
                try:
                    self.cleanup_stale_connections()
                    # Reset failure counter after cleanup
                    system_monitor.connection_stats['failed_acquisitions'] = 0
                except Exception as cleanup_error:
                    chatbot_logger.logger.error(f"Auto-cleanup failed: {cleanup_error}")
            
            error_msg = f"Failed to get connection after {wait_time:.2f}s: {e}"
            chatbot_logger.logger.error(error_msg)
            print(f"❌ {error_msg}")
            raise
    
    def return_connection(self, conn):
        """Return a connection to the pool with error handling"""
        if self._pool and conn:
            try:
                with self._pool_lock:
                    self._pool.putconn(conn)
                system_monitor.connection_stats['total_returned'] += 1
            except Exception as e:
                chatbot_logger.logger.error(f"Failed to return connection to pool: {e}")
                # If we can't return it, close it
                try:
                    conn.close()
                except:
                    pass
    
    def execute_query_with_retry(self, query, max_retries=3):
        """
        Execute query with intelligent retry mechanism and comprehensive monitoring
        Uses context manager to ensure connections are properly returned
        
        Args:
            query: SQL query to execute
            max_retries: Maximum number of retry attempts
            
        Returns:
            Tuple of (column_names, rows)
        """
        last_exception = None
        query_start = time.time()
        
        for attempt in range(max_retries + 1):
            attempt_start = time.time()
            
            try:
                # Use context manager to ensure connection is always returned
                with self.get_connection_context() as conn:
                    with conn.cursor() as cursor:
                        # Execute query with timing
                        exec_start = time.time()
                        cursor.execute(query)
                        execution_time = time.time() - exec_start
                        
                        # Fetch results
                        if cursor.description:
                            column_names = [desc[0] for desc in cursor.description]
                            rows = cursor.fetchall()
                        else:
                            column_names = []
                            rows = []
                        
                        # Update performance metrics
                        system_monitor.update_performance_metrics(execution_time, len(rows))
                        
                        # Log performance insights
                        if execution_time > 5.0:
                            chatbot_logger.logger.warning(f"Very slow query detected: {execution_time:.3f}s - Query: {query[:100]}...")
                        elif execution_time > 1.0:
                            chatbot_logger.logger.info(f"Slow query detected: {execution_time:.3f}s")
                        elif execution_time < 0.001:
                            chatbot_logger.logger.debug(f"Fast query execution: {execution_time:.6f}s")
                        
                        return column_names, rows
                
            except Exception as e:
                last_exception = e
                attempt_time = time.time() - attempt_start
                
                # Classify error for intelligent retry decision
                db_error = ErrorClassifier.classify_error(e, query)
                
                chatbot_logger.logger.error(f"Query execution failed (attempt {attempt + 1}/{max_retries + 1}) after {attempt_time:.3f}s: {db_error.error_type.value}")
                
                # Check if this error type should be retried
                if attempt < max_retries and recovery_manager.is_retryable_error(db_error.error_type):
                    wait_time = recovery_manager.get_retry_delay(attempt)
                    chatbot_logger.logger.info(f"Retrying after {wait_time}s (error type: {db_error.error_type.value})")
                    time.sleep(wait_time)
                    
                    # Continue to next attempt (connection will be cleaned up by context manager)
                    continue
                else:
                    # Non-retryable error or max retries reached
                    break
        
        # All retries exhausted or non-retryable error
        total_query_time = time.time() - query_start
        chatbot_logger.logger.error(f"Query failed after {total_query_time:.3f}s and {max_retries + 1} attempts")
        raise last_exception
    
    def get_pool_status(self):
        """Get current connection pool status for monitoring"""
        if not self._pool:
            return {"status": "not_initialized"}
        
        try:
            # This is a simplified status - actual implementation may vary based on psycopg2 version
            return {
                "status": "active",
                "min_connections": self.pool_config['minconn'],
                "max_connections": self.pool_config['maxconn'],
                "stats": system_monitor.connection_stats
            }
        except Exception as e:
            chatbot_logger.logger.error(f"Failed to get pool status: {e}")
            return {"status": "error", "error": str(e)}
    
    def cleanup_stale_connections(self):
        """Emergency cleanup of stale connections to prevent pool exhaustion"""
        if not self._pool:
            return
        
        try:
            with self._pool_lock:
                # Force close any potentially stale connections
                chatbot_logger.logger.info("🧹 Starting emergency connection cleanup")
                
                # Get current stats before cleanup
                stats_before = system_monitor.connection_stats.copy()
                
                # This will force cleanup of idle/stale connections
                # Note: psycopg2's pool doesn't have direct cleanup, but we can reset
                old_pool = self._pool
                self._pool = None
                
                # Close old pool
                try:
                    old_pool.closeall()
                except Exception as e:
                    chatbot_logger.logger.warning(f"Error closing old pool: {e}")
                
                # Reinitialize with same config
                self._pool = psycopg2.pool.ThreadedConnectionPool(**self.pool_config)
                
                chatbot_logger.logger.info("✅ Emergency connection cleanup completed")
                print("🧹 Connection pool cleanup completed")
                
        except Exception as e:
            chatbot_logger.logger.error(f"❌ Emergency cleanup failed: {e}")
            print(f"❌ Connection cleanup failed: {e}")

    def close_pool(self):
        """Close all connections in the pool with logging"""
        if self._pool:
            try:
                with self._pool_lock:
                    self._pool.closeall()
                    self._pool = None
                chatbot_logger.logger.info("Database connection pool closed successfully")
                print("🔒 Database connection pool closed")
            except Exception as e:
                chatbot_logger.logger.error(f"Error closing connection pool: {e}")
                print(f"❌ Error closing connection pool: {e}")


# Performance Optimization Classes
class IntelligentQueryCache:
    """Redis-based intelligent caching system for database queries"""
    
    def __init__(self):
        if not REDIS_AVAILABLE:
            chatbot_logger.logger.warning("⚠️ Redis not available - cache disabled")
            self.cache_available = False
            self.redis_client = None
        else:
            try:
                self.redis_client = redis.Redis(
                    host=os.getenv('REDIS_HOST', 'localhost'),
                    port=int(os.getenv('REDIS_PORT', 6379)),
                    decode_responses=True,
                    socket_timeout=5,
                    socket_connect_timeout=5,
                    db=0
                )
                # Test connection
                self.redis_client.ping()
                self.cache_available = True
                chatbot_logger.logger.info("✅ Redis cache connected successfully")
            except Exception as e:
                if REDIS_AVAILABLE and redis and hasattr(e, '__class__') and 'redis' in str(type(e)).lower():
                    chatbot_logger.logger.warning(f"⚠️ Redis cache unavailable: {e}")
                else:
                    chatbot_logger.logger.warning(f"⚠️ Redis cache unavailable: {e}")
                self.cache_available = False
                self.redis_client = None
        
        # Cache TTL strategies by query type (in seconds)
        self.cache_strategies = {
            'stoppage_report': 300,    # 5 minutes - moderate updates
            'vehicle_master': 3600,    # 1 hour - rarely changes
            'real_time_data': 30,      # 30 seconds - frequent updates
            'historical_data': 7200,   # 2 hours - historical data stable
            'analytics': 1800,         # 30 minutes - analytical queries
            'default': 600             # 10 minutes - default caching
        }
    
    def get_cache_key(self, query: str, params: dict = None) -> str:
        """Generate unique cache key for query"""
        combined = f"{query}:{json.dumps(params, sort_keys=True, cls=DecimalEncoder) if params else ''}"
        return f"chatbot_query:{hashlib.md5(combined.encode()).hexdigest()}"
    
    def determine_cache_strategy(self, query: str) -> int:
        """Determine appropriate cache TTL based on query type"""
        query_lower = query.lower()
        
        if 'util_report' in query_lower and any(x in query_lower for x in ['stoppage', 'trip']):
            return self.cache_strategies['stoppage_report']
        elif any(x in query_lower for x in ['master', 'vehicle_master', 'hosp_master']):
            return self.cache_strategies['vehicle_master']
        elif any(x in query_lower for x in ['real_time', 'current', 'now']):
            return self.cache_strategies['real_time_data']
        elif any(x in query_lower for x in ['history', 'archive', 'past']):
            return self.cache_strategies['historical_data']
        elif any(x in query_lower for x in ['count', 'sum', 'avg', 'analytics']):
            return self.cache_strategies['analytics']
        else:
            return self.cache_strategies['default']
    
    def get_cached_result(self, cache_key: str):
        """Retrieve cached result if available"""
        if not self.cache_available:
            return None
            
        try:
            cached_result = self.redis_client.get(cache_key)
            if cached_result:
                return json.loads(cached_result)
        except (json.JSONDecodeError, Exception) as e:
            chatbot_logger.logger.warning(f"Cache retrieval error: {e}")
        return None
    
    def cache_result(self, cache_key: str, result_data: dict, ttl: int):
        """Cache query result with specified TTL"""
        if not self.cache_available:
            return False
            
        try:
            # Use custom encoder to handle Decimal objects
            self.redis_client.setex(cache_key, ttl, json.dumps(result_data, cls=DecimalEncoder))
            return True
        except Exception as e:
            chatbot_logger.logger.warning(f"Cache storage error: {e}")
            return False


class QueryPerformanceOptimizer:
    """Query performance analysis and optimization suggestions"""
    
    def __init__(self):
        self.slow_query_threshold = 2.0  # 2 seconds
        self.query_stats = {}
        
    def analyze_query_performance(self, query: str, execution_time: float):
        """Analyze query performance and suggest optimizations"""
        query_hash = hashlib.md5(query.encode()).hexdigest()[:8]
        
        if query_hash not in self.query_stats:
            self.query_stats[query_hash] = {
                'query': query[:100] + '...' if len(query) > 100 else query,
                'executions': 0,
                'total_time': 0,
                'avg_time': 0,
                'max_time': 0,
                'optimizations_suggested': []
            }
        
        stats = self.query_stats[query_hash]
        stats['executions'] += 1
        stats['total_time'] += execution_time
        stats['avg_time'] = stats['total_time'] / stats['executions']
        stats['max_time'] = max(stats['max_time'], execution_time)
        
        # Suggest optimizations for slow queries
        if execution_time > self.slow_query_threshold:
            optimizations = self._suggest_optimizations(query, execution_time)
            for opt in optimizations:
                if opt not in stats['optimizations_suggested']:
                    stats['optimizations_suggested'].append(opt)
            
            chatbot_logger.logger.warning(
                f"🐌 SLOW QUERY: {execution_time:.3f}s | "
                f"Suggestions: {', '.join(optimizations[:2])}"
            )
    
    def _suggest_optimizations(self, query: str, execution_time: float) -> list:
        """Suggest query optimizations based on query pattern"""
        suggestions = []
        query_lower = query.lower()
        
        if 'select *' in query_lower:
            suggestions.append("Use specific columns instead of SELECT *")
        
        if 'like' in query_lower and not any(x in query_lower for x in ['limit', 'offset']):
            suggestions.append("Add LIMIT clause to LIKE queries")
            
        if 'where' not in query_lower and 'util_report' in query_lower:
            suggestions.append("Add WHERE clause with date/vehicle filters")
            
        if execution_time > 5.0:
            suggestions.append("Consider adding database indexes")
            
        if 'order by' in query_lower and 'limit' not in query_lower:
            suggestions.append("Add LIMIT to ORDER BY queries")
            
        return suggestions
    
    def get_performance_report(self) -> dict:
        """Generate performance analysis report"""
        if not self.query_stats:
            return {"message": "No queries analyzed yet"}
        
        sorted_stats = sorted(
            self.query_stats.values(),
            key=lambda x: x['avg_time'],
            reverse=True
        )
        
        slow_queries = [q for q in sorted_stats if q['avg_time'] > self.slow_query_threshold]
        
        return {
            "total_unique_queries": len(self.query_stats),
            "slow_queries_count": len(slow_queries),
            "top_slow_queries": slow_queries[:5],
            "average_query_time": sum(q['avg_time'] for q in sorted_stats) / len(sorted_stats),
            "total_optimizations_suggested": sum(len(q['optimizations_suggested']) for q in sorted_stats)
        }


class MemoryOptimizedResultHandler:
    """Memory optimization and result compression for large datasets"""
    
    def __init__(self):
        self.max_rows_in_memory = 1000
        self.compression_threshold = 100  # rows
        
    def optimize_large_result(self, columns, rows):
        """Optimize memory usage for large result sets"""
        row_count = len(rows)
        
        if row_count <= self.compression_threshold:
            return columns, rows  # Small result, no optimization needed
        
        chatbot_logger.logger.info(f"📊 Optimizing large result set: {row_count} rows")
        
        # For very large results, implement pagination
        if row_count > self.max_rows_in_memory:
            paginated_rows = rows[:self.max_rows_in_memory]
            truncation_msg = f"[Showing first {self.max_rows_in_memory} of {row_count} total rows]"
            
            # Add truncation info as a special row
            if paginated_rows and columns:
                truncation_row = ["..." for _ in columns]
                truncation_row[0] = truncation_msg
                paginated_rows.append(truncation_row)
            
            chatbot_logger.logger.info(f"📄 Result paginated: {len(paginated_rows)} rows returned")
            return columns, paginated_rows
        
        # For medium results, optimize data types
        optimized_rows = []
        for row in rows:
            optimized_row = []
            for value in row:
                if isinstance(value, float) and value.is_integer():
                    optimized_row.append(int(value))  # Convert float to int if possible
                elif isinstance(value, str) and value.strip() == "":
                    optimized_row.append(None)  # Convert empty strings to None
                else:
                    optimized_row.append(value)
            optimized_rows.append(optimized_row)
        
        memory_saved = (row_count * len(columns) * 8) - (len(optimized_rows) * len(columns) * 4)
        chatbot_logger.logger.info(f"💾 Memory optimized: ~{memory_saved/1024:.1f}KB saved")
        
        return columns, optimized_rows


class BackgroundProcessingManager:
    """Background processing for precomputation and async operations"""
    
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=2, thread_name_prefix="bg_processor")
        
    def schedule_background_task(self, task_func, *args, **kwargs):
        """Schedule a task to run in the background"""
        try:
            future = self.executor.submit(task_func, *args, **kwargs)
            return future
        except Exception as e:
            chatbot_logger.logger.error(f"Background task scheduling failed: {e}")
            return None
    
    def precompute_common_queries(self):
        """Pre-compute and cache common queries in background"""
        common_queries = [
            "SELECT COUNT(*) FROM util_report WHERE from_tm >= CURRENT_DATE - INTERVAL '7 days'",
            "SELECT DISTINCT reg_no FROM util_report ORDER BY reg_no LIMIT 100",
            "SELECT COUNT(*) FROM hosp_master",
            "SELECT COUNT(*) FROM util_report WHERE from_tm >= CURRENT_DATE - INTERVAL '1 day'"
        ]
        
        for query in common_queries:
            self.schedule_background_task(self._precompute_query, query)
    
    def _precompute_query(self, query):
        """Execute query and cache result"""
        try:
            columns, rows = db_manager.execute_query_with_retry(query)
            # Cache the result using the cache manager
            if hasattr(cache_manager, 'cache_available') and cache_manager.cache_available:
                cache_key = f"precomputed:{hashlib.md5(query.encode()).hexdigest()}"
                result_data = {'columns': columns, 'rows': rows}
                cache_manager.cache_result(cache_key, result_data, 3600)  # 1 hour TTL
                chatbot_logger.logger.info(f"✅ Precomputed query cached: {query[:50]}...")
        except Exception as e:
            chatbot_logger.logger.error(f"❌ Precomputation failed: {e}")


# Initialize performance optimization components
try:
    cache_manager = IntelligentQueryCache()
    performance_optimizer = QueryPerformanceOptimizer()
    result_optimizer = MemoryOptimizedResultHandler()
    background_manager = BackgroundProcessingManager()
    
    chatbot_logger.logger.info("🚀 Performance optimization suite initialized")
    
    # Start background precomputation
    background_manager.precompute_common_queries()
    
except Exception as e:
    chatbot_logger.logger.warning(f"⚠️ Performance optimization partially unavailable: {e}")
    # Create dummy objects for fallback
    cache_manager = None
    performance_optimizer = None
    result_optimizer = None
    background_manager = None


def cached_query(func):
    """Decorator for intelligent query caching"""
    @wraps(func)
    def wrapper(query, *args, **kwargs):
        if not cache_manager or not cache_manager.cache_available:
            return func(query, *args, **kwargs)
        
        # Generate cache key
        cache_key = cache_manager.get_cache_key(query, kwargs)
        
        # Try to get from cache first
        cached_result = cache_manager.get_cached_result(cache_key)
        if cached_result:
            chatbot_logger.logger.info(f"🚀 CACHE HIT: Query served from cache in 0.001s")
            return cached_result['columns'], cached_result['rows']
        
        # Execute original query
        start_time = time.time()
        columns, rows = func(query, *args, **kwargs)
        execution_time = time.time() - start_time
        
        # Cache the result
        cache_ttl = cache_manager.determine_cache_strategy(query)
        result_data = {'columns': columns, 'rows': rows}
        if cache_manager.cache_result(cache_key, result_data, cache_ttl):
            chatbot_logger.logger.info(f"💾 CACHED: Query result cached for {cache_ttl}s")
        
        return columns, rows
    return wrapper


# Global instance of the database manager
db_manager = DatabaseConnectionManager()

# Add persistent debug log to Streamlit sidebar
if 'debug_log' not in st.session_state:
    st.session_state['debug_log'] = []

@cached_query
def run_query(query, user_id="anonymous"):
    """
    Performance-optimized query execution with caching, monitoring, and optimization
    
    Args:
        query: SQL query to execute
        user_id: User identifier for logging (optional)
        
    Returns:
        Tuple of (column_names, rows)
    """
    start_time = time.time()
    query_hash = str(hash(query))
    
    try:
        # Log query start
        debug_msg = f"[DEBUG] SQL Query: {query}"
        print(f"\n{debug_msg}\n", flush=True)
        
        # Add to Streamlit debug log if available
        if 'debug_log' in st.session_state:
            st.session_state['debug_log'].append(debug_msg)
        
        # Use the enhanced connection manager with retry mechanism
        columns, rows = db_manager.execute_query_with_retry(query)
        
        # Calculate execution time
        execution_time = time.time() - start_time
        
        # Performance analysis
        if performance_optimizer:
            performance_optimizer.analyze_query_performance(query, execution_time)
        
        # Memory optimization for large results
        if result_optimizer and len(rows) > 50:
            columns, rows = result_optimizer.optimize_large_result(columns, rows)
        
        # Enhanced logging with performance metrics
        chatbot_logger.log_query(query, execution_time, len(rows))
        system_monitor.record_query(True, execution_time)
        recovery_manager.clear_retry_count(query_hash)  # Clear retry count on success
        
        # Add performance info to debug log
        cache_status = "CACHE MISS" if execution_time > 0.01 else "CACHE HIT"
        debug_msg2 = f"[{cache_status}] Query: {execution_time:.3f}s, Rows: {len(rows)}"
        print(f"{debug_msg2}\n", flush=True)
        
        if 'debug_log' in st.session_state:
            st.session_state['debug_log'].append(debug_msg2)
        
        return columns, rows
        
    except Exception as e:
        execution_time = time.time() - start_time
        
        # Classify the error for better handling
        db_error = ErrorClassifier.classify_error(e, query)
        
        # Log the error with detailed information
        chatbot_logger.log_error(db_error, user_id)
        system_monitor.record_query(False, execution_time, db_error.error_type.value)
        
        # Check if we should retry this error
        if recovery_manager.should_retry(db_error.error_type, query_hash):
            recovery_manager.increment_retry_count(query_hash)
            retry_count = recovery_manager.retry_counts[query_hash]
            retry_delay = recovery_manager.get_retry_delay(retry_count - 1)
            
            chatbot_logger.logger.info(f"Retrying query (attempt {retry_count}/{recovery_manager.max_retries}) after {retry_delay}s delay")
            time.sleep(retry_delay)
            
            return run_query(query, user_id)  # Recursive retry
        
        # Add user-friendly error to debug log
        error_msg = f"[ERROR] {db_error.user_message}"
        print(error_msg, flush=True)
        
        if 'debug_log' in st.session_state:
            st.session_state['debug_log'].append(error_msg)
            if db_error.suggestion:
                st.session_state['debug_log'].append(f"[SUGGESTION] {db_error.suggestion}")
        
        # For non-retryable errors or exhausted retries, provide graceful response
        if db_error.error_type in [ErrorType.SQL_SYNTAX, ErrorType.TABLE_NOT_FOUND, ErrorType.PERMISSION_DENIED]:
            # Return empty result instead of crashing the application
            chatbot_logger.logger.info(f"Returning empty result for non-retryable error: {db_error.error_type.value}")
            return [], []
        
        # For critical errors that should still raise exceptions (after retries)
        chatbot_logger.logger.error(f"All retry attempts exhausted for query: {query[:100]}...")
        raise Exception(db_error.user_message) from e


def get_performance_metrics():
    """Get current performance metrics for monitoring"""
    metrics = {
        'cache_status': 'available' if cache_manager and cache_manager.cache_available else 'unavailable',
        'connection_pool_health': db_manager.get_pool_status() if db_manager else {},
        'system_monitor_stats': system_monitor.get_health_report() if system_monitor else {},
    }
    
    if performance_optimizer:
        metrics['query_performance'] = performance_optimizer.get_performance_report()
    
    return metrics


def get_text_columns(schema=None, table=None):
    """Return all text/varchar columns in the database or filtered by schema/table."""
    query = """
        SELECT table_schema, table_name, column_name
        FROM information_schema.columns
        WHERE data_type IN ('text', 'character varying', 'character')
        AND table_schema NOT IN ('information_schema', 'pg_catalog')
    """
    if schema:
        query += f" AND table_schema = '{schema}'"
    if table:
        query += f" AND table_name = '{table}'"

    try:
        with db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()
                return rows
    except Exception as e:
        print("❌ Failed to fetch text columns:", e)
        return []

def get_primary_key_column(schema, table):
    """Returns the primary key column of a table if available, otherwise None."""
    try:
        with db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                query = """
                    SELECT kcu.column_name
                    FROM information_schema.table_constraints tc
                    JOIN information_schema.key_column_usage kcu
                      ON tc.constraint_name = kcu.constraint_name
                     AND tc.table_schema = kcu.table_schema
                    WHERE tc.constraint_type = 'PRIMARY KEY'
                      AND tc.table_schema = %s
                      AND tc.table_name = %s;
                """
                cur.execute(query, (schema, table))
                result = cur.fetchone()
                return result[0] if result else None
    except Exception as e:
        print(f"❌ Failed to get primary key for {schema}.{table}:", e)
        return None

def fix_encoding_for_column(schema, table, column, id_column="id", corruption_regex=None):
    """
    Fix encoding issues in a single column.
    If corruption_regex is provided, it will filter values using it.
    """
    fixed_count = 0
    try:
        with db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                full_table = f'"{schema}"."{table}"'
                corruption_clause = f"WHERE {column} ~ '{corruption_regex}'" if corruption_regex else ""

                query = f"""
                    SELECT {id_column}, {column}
                    FROM {full_table}
                    {corruption_clause};
                """

                cur.execute(query)
                rows = cur.fetchall()

                for row_id, bad_value in rows:
                    if not isinstance(bad_value, str):
                        continue
                    try:
                        fixed_value = bad_value.encode('latin1').decode('utf-8')
                        if fixed_value != bad_value:
                            cur.execute(
                                f"UPDATE {full_table} SET {column} = %s WHERE {id_column} = %s",
                                (fixed_value, row_id)
                            )
                            fixed_count += 1
                    except UnicodeDecodeError:
                        continue 

                conn.commit()
                print(f"✅ Fixed {fixed_count} entries in {schema}.{table}.{column}")
    except Exception as e:
        print(f"❌ Error processing {schema}.{table}.{column}:", e)

def fix_all_encoding_issues(corruption_regex="Ã|â€™|â€“|â€œ|â€|Ãƒ"):
    """
    Run fix_encoding_for_column on all text/varchar/char columns in all tables.
    `corruption_regex` can be changed or set to None for full scan.
    """
    columns_info = get_text_columns()
    for schema, table, column in columns_info:
        id_column = get_primary_key_column(schema, table)
        if id_column:
            fix_encoding_for_column(schema, table, column, id_column, corruption_regex)
        else:
            print(f"Skipping {schema}.{table} - no suitable primary key found.")

def get_full_schema():
    """
    Returns a dictionary of all tables and their columns for all user schemas.
    Example: { 'public': { 'film': ['film_id', 'title', ...], ... }, ... }
    """
    try:
        with db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT table_schema, table_name, column_name
                    FROM information_schema.columns
                    WHERE table_schema NOT IN ('information_schema', 'pg_catalog')
                    ORDER BY table_schema, table_name, ordinal_position
                """)
                schema = {}
                for table_schema, table_name, column_name in cur.fetchall():
                    if table_schema not in schema:
                        schema[table_schema] = {}
                    if table_name not in schema[table_schema]:
                        schema[table_schema][table_name] = []
                    schema[table_schema][table_name].append(column_name)
                return schema
    except Exception as e:
        print("❌ Failed to fetch schema:", e)
        return {}

def print_schema(schema):
    for schema_name, tables in schema.items():
        print(f"Schema: {schema_name}")
        for table, columns in tables.items():
            print(f"  Table: {table} (" + ", ".join(columns) + ")")

def get_column_types(schema=None, table=None):
    """
    Returns column data types for validation.
    Returns dict: {schema.table.column: data_type}
    """
    query = """
        SELECT table_schema, table_name, column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_schema NOT IN ('information_schema', 'pg_catalog')
    """
    
    if schema:
        query += f" AND table_schema = '{schema}'"
    if table:
        query += f" AND table_name = '{table}'"
    
    try:
        with db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()
                
                # Return dictionary with full column path and data type
                return {f"{row[0]}.{row[1]}.{row[2]}": row[3] for row in rows}
    except Exception as e:
        print("❌ Failed to fetch column types:", e)
        return {}

def get_numeric_columns(schema=None, table=None):
    """Return all numeric columns in the database."""
    query = """
        SELECT table_schema, table_name, column_name
        FROM information_schema.columns
        WHERE data_type IN ('integer', 'bigint', 'smallint', 'decimal', 'numeric', 'real', 'double precision', 'money')
        AND table_schema NOT IN ('information_schema', 'pg_catalog')
    """
    
    if schema:
        query += f" AND table_schema = '{schema}'"
    if table:
        query += f" AND table_name = '{table}'"

    try:
        with db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()
                return rows
    except Exception as e:
        print("❌ Failed to fetch numeric columns:", e)
        return []

if __name__ == "__main__":
    schema = get_full_schema()
    print_schema(schema)
