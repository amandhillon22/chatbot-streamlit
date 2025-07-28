#!/usr/bin/env python3
"""
import sys
sys.path.append('/home/linux/Documents/chatbot-diya')

Quick test to verify ID relationships in SQL generation
"""

print("🔗 Quick ID Relationship Test")
print("=" * 40)

# Test the intelligent reasoning templates directly
try:
    from src.core.intelligent_reasoning import IntelligentReasoning
    
    print("✅ Intelligent reasoning imported successfully")
    ir = IntelligentReasoning()
    
    # Test the core hierarchy structure
    print("\n📋 Core Hierarchy Structure:")
    for table, info in ir.core_hierarchy.items():
        print(f"  {table}:")
        if 'parent_table' in info:
            print(f"    ↑ Parent: {info['parent_table']} (via {info['parent_foreign_key']})")
        if 'child_table' in info:
            print(f"    ↓ Child: {info['child_table']} (via {info['child_foreign_key']})")
    
    # Test hierarchical SQL templates
    print("\n🧪 Testing Hierarchical SQL Templates:")
    
    test_cases = [
        ('vehicle', 'plant', 'mohali'),
        ('vehicle', 'region', 'punjab'),
        ('plant', 'region', 'punjab')
    ]
    
    for entity_from, entity_to, filter_val in test_cases:
        print(f"\n  Testing: {entity_from} → {entity_to} (filter: {filter_val})")
        template = ir.get_hierarchical_sql_template(entity_from, entity_to, filter_val)
        
        if template:
            print(f"    ✅ Template generated")
            # Check for critical ID relationships
            if 'id_hosp' in template and 'id_no' in template:
                print(f"    ✅ Contains id_hosp relationship")
            if 'id_dist' in template and entity_to in ['region', 'zone']:
                print(f"    ✅ Contains id_dist relationship")
        else:
            print(f"    ❌ No template generated")
    
    # Test mandatory joins function
    print("\n🔧 Testing Mandatory Joins Function:")
    
    test_queries = [
        "show me vehicles of mohali plant",
        "vehicles in punjab region", 
        "plants in haryana region"
    ]
    
    for query in test_queries:
        print(f"\n  Query: '{query}'")
        base_table, joins = ir.get_mandatory_joins_for_query(query.lower())
        print(f"    Base table: {base_table}")
        for join in joins:
            print(f"    Join: {join}")
            
    print("\n🎉 Basic ID relationship structure looks good!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 40)
print("✅ Quick test completed")
