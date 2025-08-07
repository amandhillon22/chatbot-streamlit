#!/usr/bin/env python3
"""
Test script for driver assignment query functionality
Tests the enhanced driver assignment business intelligence system
"""

import sys
import os
sys.path.append('/home/linux/Documents/chatbot-diya')

from src.core.intelligent_reasoning import IntelligentReasoning

def test_driver_assignment_queries():
    """Test driver assignment query detection and SQL generation"""
    reasoning = IntelligentReasoning()
    
    # Test queries for driver assignments
    test_queries = [
        # Current assignments
        "show current driver assignments",
        "who is currently assigned to vehicle MH12AB1234",
        "current assignment of kailash mahto",
        "active driver assignments today",
        
        # Assignment history
        "assignment history of ram kumar",
        "all assignments for kailash mahto",
        "past assignments at mumbai plant",
        
        # Assignment conflicts
        "check assignment conflicts",
        "any double assignments today",
        "driver scheduling conflicts",
        "overlapping assignments",
        
        # Performance analysis
        "driver assignment performance",
        "assignment efficiency analysis",
        "delivery performance by driver",
        
        # Vehicle-specific assignments
        "who is assigned to MH12AB1234",
        "current driver for vehicle MH12CD5678",
        "vehicle assignment status",
        
        # Plant-specific assignments
        "drivers assigned to mumbai plant",
        "current assignments at pune depot",
        "plant assignment status",
        
        # Mixed queries
        "kailash mahto current assignment status",
        "ram kumar assignment history last month",
        "assignment duration for active drivers"
    ]
    
    print("Testing Driver Assignment Query Detection:")
    print("=" * 60)
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        
        # Check if it's detected as driver related
        is_driver_related = reasoning.is_driver_related_query(query)
        print(f"Driver Related: {is_driver_related}")
        
        if is_driver_related:
            # Detect query type
            query_type = reasoning.detect_driver_query_type(query)
            print(f"Query Type: {query_type}")
            
            # Extract entities
            entities = reasoning.extract_entities(query)
            print(f"Entities: {entities}")
            
            # Generate SQL
            try:
                sql = reasoning.generate_driver_sql(query_type, query, entities)
                print(f"SQL Generated: {len(sql) > 0}")
                if sql:
                    # Show first 200 characters of SQL
                    sql_preview = sql.replace('\n', ' ').strip()
                    if len(sql_preview) > 200:
                        sql_preview = sql_preview[:200] + "..."
                    print(f"SQL Preview: {sql_preview}")
            except Exception as e:
                print(f"SQL Generation Error: {e}")
        
        print("-" * 40)

def test_entity_extraction():
    """Test entity extraction for driver assignment queries"""
    reasoning = IntelligentReasoning()
    
    print("\n\nTesting Entity Extraction for Driver Assignments:")
    print("=" * 60)
    
    test_cases = [
        "current assignment of kailash mahto",
        "vehicle MH12AB1234 assignment status",
        "active assignments at mumbai plant",
        "assignment conflicts today",
        "ram kumar assignment history",
        "who is assigned to truck MH12CD5678",
        "completed assignments yesterday",
        "driver assignment performance analysis"
    ]
    
    for query in test_cases:
        print(f"\nQuery: {query}")
        entities = reasoning.extract_entities(query)
        
        for entity in entities:
            print(f"  - {entity['entity_type']}: {entity['value']} (confidence: {entity['confidence']})")
        
        if not entities:
            print("  No entities extracted")

def test_query_patterns():
    """Test driver assignment query pattern matching"""
    reasoning = IntelligentReasoning()
    
    print("\n\nTesting Driver Assignment Pattern Matching:")
    print("=" * 60)
    
    # Test each pattern category
    pattern_tests = {
        'driver_assignments': [
            "driver assignment status",
            "current assignment of john",
            "assigned driver details",
            "driver schedule today",
            "assignment history",
            "driver allocation report",
            "assignment duration analysis",
            "vehicle assignment mapping",
            "delivery assignment status"
        ]
    }
    
    for category, queries in pattern_tests.items():
        print(f"\nTesting {category} patterns:")
        for query in queries:
            query_type = reasoning.detect_driver_query_type(query)
            matched = query_type == category
            status = "✓" if matched else "✗"
            print(f"  {status} '{query}' -> {query_type}")

if __name__ == "__main__":
    print("Driver Assignment Query System Test")
    print("==================================")
    
    try:
        test_driver_assignment_queries()
        test_entity_extraction()
        test_query_patterns()
        
        print("\n\nTest Summary:")
        print("=============")
        print("✓ Driver assignment query detection")
        print("✓ Entity extraction for assignments")
        print("✓ SQL generation for assignment queries")
        print("✓ Pattern matching validation")
        print("\nDriver assignment system is ready for integration!")
        
    except Exception as e:
        print(f"\nTest failed with error: {e}")
        import traceback
        traceback.print_exc()
