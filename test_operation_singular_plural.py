#!/usr/bin/env python3
"""
Test script to check operation vs operations query handling
"""

import sys
sys.path.append('.')

from intelligent_reasoning import IntelligentReasoning

def test_operation_variations():
    """Test how the system handles operation vs operations"""
    
    print("🔍 TESTING OPERATION vs OPERATIONS QUERY HANDLING")
    print("=" * 60)
    
    # Initialize intelligent reasoning
    ir = IntelligentReasoning()
    
    # Test queries
    test_queries = [
        "how many complaints of operation",
        "how many complaints of operations", 
        "show complaints of operation",
        "show complaints of operations",
        "list operation complaints",
        "list operations complaints",
        "complaints in operation category",
        "complaints in operations category"
    ]
    
    print("🧪 Testing Query Variations:")
    print("-" * 40)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Query: '{query}'")
        print("-" * 30)
        
        # Analyze the query
        result = ir.analyze_query_intent(query, {})
        
        if result:
            print(f"   ✅ Intent: {result.get('intent', 'None')}")
            print(f"   📊 Extracted: {result.get('extracted_data', {})}")
        else:
            print("   ❌ No intelligent reasoning applied")

if __name__ == "__main__":
    test_operation_variations()
