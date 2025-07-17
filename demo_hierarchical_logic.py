#!/usr/bin/env python3
"""
Demo script showing the hierarchical logic in action

This demonstrates how the chatbot now handles zone-region-plant-vehicle relationships
using the proper hierarchical structure:
zone_master ← district_master ← hosp_master ← vehicle_master
"""

from query_agent import english_to_sql, ChatContext

def demo_hierarchical_queries():
    """Demonstrate hierarchical query handling"""
    print("🎯 Hierarchical Logic Demo")
    print("=" * 60)
    print("Demonstrating zone → region → plant → vehicle relationships")
    print("=" * 60)
    
    context = ChatContext()
    
    # Demo queries that showcase the hierarchical logic
    demo_queries = [
        {
            'query': "What zone does vehicle MH12AB1234 belong to?",
            'explanation': "Find zone for specific vehicle (4-level hierarchy)"
        },
        {
            'query': "Which region is vehicle KA05CD5678 in?", 
            'explanation': "Find region/district for specific vehicle (3-level hierarchy)"
        },
        {
            'query': "What plant does vehicle TN09EF9012 belong to?",
            'explanation': "Find plant/hospital for specific vehicle (2-level hierarchy)"
        },
        {
            'query': "Show me all vehicles in North zone",
            'explanation': "List vehicles by zone (reverse hierarchy lookup)"
        },
        {
            'query': "List vehicles in Mumbai region",
            'explanation': "List vehicles by region (reverse hierarchy lookup)"
        },
        {
            'query': "Show vehicles in Bangalore plant",
            'explanation': "List vehicles by plant (direct hierarchy lookup)"
        },
        {
            'query': "Give me the complete hierarchy for vehicle DL01GH2345",
            'explanation': "Show full zone→region→plant→vehicle chain"
        }
    ]
    
    for i, demo in enumerate(demo_queries, 1):
        print(f"\n{i}. {demo['explanation']}")
        print(f"Query: '{demo['query']}'")
        print("-" * 50)
        
        try:
            result = english_to_sql(demo['query'], context)
            
            if result.get('reasoning_applied'):
                print("🧠 Intelligent reasoning applied!")
                print(f"   Intent: {result.get('reasoning_type', 'hierarchical')}")
                if result.get('sql'):
                    sql_preview = result['sql'].strip()
                    # Show the key parts of the SQL
                    if 'zone_master' in sql_preview:
                        print("   🌍 Uses zone_master table")
                    if 'district_master' in sql_preview:
                        print("   🏢 Uses district_master table") 
                    if 'hosp_master' in sql_preview:
                        print("   🏭 Uses hosp_master table")
                    if 'vehicle_master' in sql_preview:
                        print("   🚛 Uses vehicle_master table")
                    
                    # Show JOIN logic
                    join_count = sql_preview.count('JOIN')
                    if join_count > 0:
                        print(f"   🔗 Uses {join_count} hierarchical JOINs")
                        
                    print(f"   📝 SQL: {sql_preview[:120]}...")
            else:
                print("🔧 Standard query processing")
                if result.get('sql'):
                    print(f"   📝 SQL: {result['sql'][:120]}...")
                    
            if result.get('response'):
                print(f"   💬 Response: {result['response']}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Hierarchical Logic Demo Complete!")
    print("The chatbot now understands and properly handles:")
    print("• Zone → Region → Plant → Vehicle relationships")
    print("• Proper JOIN logic across hierarchical tables")
    print("• Intelligent intent detection for hierarchical queries")
    print("• Enhanced table mapping for domain-specific keywords")
    print("=" * 60)

if __name__ == "__main__":
    demo_hierarchical_queries()
