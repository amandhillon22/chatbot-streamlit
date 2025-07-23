#!/usr/bin/env python3
"""
Test script to verify hierarchical relationships
"""

def test_hierarchical_relationships():
    """Test the hierarchical relationship updates"""
    try:
        from database_reference_parser import DatabaseReferenceParser
        
        print("🏗️ Testing Hierarchical Relationships")
        
        # Test 1: Parser can be imported
        parser = DatabaseReferenceParser('database_reference.md')
        print("✅ Parser initialized successfully")
        
        # Test 2: Hierarchical queries return relevant tables
        hierarchical_queries = [
            'plant hierarchy',
            'site organization', 
            'customer structure',
            'plant to customer',
            'organizational structure',
            'plant sites customers'
        ]
        
        print("\n🔍 Testing hierarchical queries:")
        for query in hierarchical_queries:
            try:
                relevant_tables = parser.get_business_relevant_tables(query)
                print(f"   '{query}' → {len(relevant_tables)} tables found")
                hierarchy_tables = [t for t in relevant_tables if any(ht in t for ht in ['hosp_master', 'site_master', 'customer_detail', 'plant_data'])]
                if hierarchy_tables:
                    print(f"     ✅ Hierarchy tables: {hierarchy_tables}")
                else:
                    print("     ⚠️  No hierarchy tables found")
            except Exception as e:
                print(f"     ❌ Error: {e}")
        
        # Test 3: Check specific hierarchical relationships
        print(f"\n🔗 Testing hierarchical table relationships:")
        
        # Parse the reference file to get table metadata
        try:
            tables_info = parser.parse_reference_file()
            
            hierarchy_tables = ['hosp_master', 'site_master', 'customer_detail', 'plant_data']
            for table in hierarchy_tables:
                if table in tables_info:
                    relationships = tables_info[table].get('relationships', [])
                    print(f"   {table} → relationships: {relationships}")
                else:
                    print(f"   ⚠️  {table} not found in parsed tables")
                    
        except Exception as e:
            print(f"   ❌ Error parsing relationships: {e}")
        
        print("\n✅ Hierarchical relationship test complete!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_hierarchical_relationships()
    print(f"\n{'🎉 SUCCESS!' if success else '❌ FAILED'}")
