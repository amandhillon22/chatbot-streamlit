#!/usr/bin/env python3
"""
Edge case testing for category queries - operations, technical, singular/plural
"""

import sys
sys.path.append('.')

from intelligent_reasoning import IntelligentReasoning

def test_category_edge_cases():
    """Test edge cases and both category types"""
    
    print("🔍 CATEGORY QUERY EDGE CASE TESTING")
    print("=" * 60)
    
    # Initialize intelligent reasoning
    ir = IntelligentReasoning()
    
    # Comprehensive test queries
    test_queries = [
        # Operations variations
        "how many complaints of operation",
        "how many complaints of operations", 
        "count of operation complaints",
        "number of operations complaints",
        "show operation complaints",
        "list operations complaints",
        "complaints in operation category",
        "complaints from operations department",
        
        # Technical variations  
        "how many complaints of technical",
        "how many complaints of tech",
        "count of technical complaints", 
        "show technical complaints",
        "list tech complaints",
        "complaints in technical category",
        "complaints from tech department",
        
        # Edge cases
        "operation category complaints",
        "technical category complaints",
        "complaints operation",
        "complaints technical"
    ]
    
    print("🧪 Testing All Category Query Variations:")
    print("-" * 50)
    
    operations_count = 0
    technical_count = 0
    unmatched_count = 0
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i:2}. '{query}'")
        result = ir.analyze_query_intent(query, {})
        
        if result:
            intent = result.get('intent', 'None')
            extracted = result.get('extracted_data', {})
            category_name = extracted.get('category_name', 'None')
            category_id = extracted.get('category_id', 'None')
            
            if category_name == 'Operations':
                operations_count += 1
                print(f"    ✅ Operations (ID: {category_id}) - {intent}")
            elif category_name == 'Technical':
                technical_count += 1
                print(f"    ✅ Technical (ID: {category_id}) - {intent}")
            else:
                print(f"    ⚠️  Other: {category_name} - {intent}")
        else:
            unmatched_count += 1
            print(f"    ❌ No pattern matched")
    
    print("\n" + "=" * 60)
    print("📊 RESULTS SUMMARY:")
    print(f"• Operations queries matched: {operations_count}")
    print(f"• Technical queries matched: {technical_count}") 
    print(f"• Unmatched queries: {unmatched_count}")
    print(f"• Total queries tested: {len(test_queries)}")
    
    print("\n🎯 SUCCESS CRITERIA:")
    print(f"• Operations variations work: {'✅' if operations_count >= 8 else '❌'}")
    print(f"• Technical variations work: {'✅' if technical_count >= 6 else '❌'}")
    print(f"• No queries unmatched: {'✅' if unmatched_count == 0 else '❌'}")

if __name__ == "__main__":
    test_category_edge_cases()
