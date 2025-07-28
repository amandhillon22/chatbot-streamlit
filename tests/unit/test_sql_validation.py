#!/usr/bin/env python3
"""
Test script to verify SQL validation is working correctly.
"""

import sys
import os
sys.path.append('/home/linux/Documents/chatbot-diya')

from src.core.query_agent import validate_sql_query
from src.core.sql import get_column_types

def test_validation():
    print("🧪 Testing SQL Validation System")
    print("=" * 50)
    
    # Get some column types to understand the schema
    print("\n📊 Sample column types from database:")
    column_types = get_column_types()
    sample_columns = list(column_types.items())[:10]
    for col_path, data_type in sample_columns:
        print(f"  {col_path}: {data_type}")
    
    print("\n🔍 Testing various SQL queries:")
    
    # Test cases
    test_queries = [
        # Valid queries
        ("SELECT COUNT(*) FROM public.vehicle_master", "Valid count query"),
        ("SELECT reg_no FROM public.vehicle_master LIMIT 10", "Valid text column query"),
        
        # Invalid queries that should be auto-fixed with type casting
        ("SELECT SUM(total_so_value) FROM public.so_details", "Auto-fix: SUM on text column with numeric data"),
        ("SELECT AVG(total_price) FROM public.so_details", "Auto-fix: AVG on text column with numeric data"),
        ("SELECT SUM(quantity) FROM public.so_details", "Auto-fix: SUM on text column with numeric data"),
        
        # Edge cases
        ("SELECT COUNT(reg_no) FROM public.vehicle_master", "Valid: COUNT on any column"),
        ("SELECT MAX(reg_no) FROM public.vehicle_master", "Valid: MAX on text (alphabetical)"),
        ("SELECT MIN(reg_no) FROM public.vehicle_master", "Valid: MIN on text (alphabetical)"),
    ]
    
    for sql_query, description in test_queries:
        print(f"\n📝 {description}")
        print(f"   SQL: {sql_query}")
        
        is_valid, error_msg, suggested_sql = validate_sql_query(sql_query)
        
        if suggested_sql and suggested_sql != sql_query:
            print(f"   🔄 AUTO-FIXED: {suggested_sql}")
        elif is_valid:
            print("   ✅ PASSED: Query validation successful")
        else:
            print(f"   ❌ BLOCKED: {error_msg}")
    
    print("\n" + "=" * 50)
    print("🎯 Validation test completed!")

if __name__ == "__main__":
    test_validation()
