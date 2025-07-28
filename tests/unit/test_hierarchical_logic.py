#!/usr/bin/env python3
"""
import sys
sys.path.append('/home/linux/Documents/chatbot-diya')

Test script for hierarchical zone-region-plant-vehicle relationships

This script validates the new hierarchical logic implementation:
- zone_master ← district_master ← hosp_master ← vehicle_master
"""

import sys
import os
from src.core.sql import run_sql_query

def test_hierarchical_structure():
    """Test the basic hierarchical structure and relationships"""
    print("🏗️ Testing Hierarchical Structure")
    print("=" * 50)
    
    # Test 1: Check zone_master table
    print("\n1. Testing zone_master table:")
    try:
        columns, rows = run_sql_query("SELECT id_no, zone_name FROM public.zone_master LIMIT 5")
        if rows:
            print(f"✅ Found {len(rows)} zones:")
            for row in rows:
                print(f"   Zone ID: {row[0]}, Name: {row[1]}")
        else:
            print("❌ No zones found")
    except Exception as e:
        print(f"❌ Error querying zones: {e}")
    
    # Test 2: Check district_master table and its relationship to zones
    print("\n2. Testing district_master table and zone relationship:")
    try:
        query = """
        SELECT dm.id_no, dm.name, dm.id_zone, zm.zone_name 
        FROM public.district_master dm 
        LEFT JOIN public.zone_master zm ON dm.id_zone = zm.id_no 
        LIMIT 5
        """
        columns, rows = run_sql_query(query)
        if rows:
            print(f"✅ Found {len(rows)} districts:")
            for row in rows:
                print(f"   District ID: {row[0]}, Name: {row[1]}, Zone ID: {row[2]}, Zone Name: {row[3]}")
        else:
            print("❌ No districts found")
    except Exception as e:
        print(f"❌ Error querying districts: {e}")
    
    # Test 3: Check hosp_master table and its relationship to districts
    print("\n3. Testing hosp_master table and district relationship:")
    try:
        query = """
        SELECT hm.id_no, hm.name, hm.id_dist, dm.name as district_name 
        FROM public.hosp_master hm 
        LEFT JOIN public.district_master dm ON hm.id_dist = dm.id_no 
        LIMIT 5
        """
        columns, rows = run_sql_query(query)
        if rows:
            print(f"✅ Found {len(rows)} plants/hospitals:")
            for row in rows:
                print(f"   Plant ID: {row[0]}, Name: {row[1]}, District ID: {row[2]}, District Name: {row[3]}")
        else:
            print("❌ No plants found")
    except Exception as e:
        print(f"❌ Error querying plants: {e}")
    
    # Test 4: Check vehicle_master table and its relationship to plants
    print("\n4. Testing vehicle_master table and plant relationship:")
    try:
        query = """
        SELECT vm.reg_no, vm.id_hosp, hm.name as plant_name 
        FROM public.vehicle_master vm 
        LEFT JOIN public.hosp_master hm ON vm.id_hosp = hm.id_no 
        WHERE vm.id_hosp IS NOT NULL 
        LIMIT 5
        """
        columns, rows = run_sql_query(query)
        if rows:
            print(f"✅ Found {len(rows)} vehicles with plant assignments:")
            for row in rows:
                print(f"   Vehicle: {row[0]}, Plant ID: {row[1]}, Plant Name: {row[2]}")
        else:
            print("❌ No vehicles with plant assignments found")
    except Exception as e:
        print(f"❌ Error querying vehicles: {e}")

def test_complete_hierarchy():
    """Test the complete hierarchical chain from vehicle to zone"""
    print("\n🔗 Testing Complete Hierarchical Chain")
    print("=" * 50)
    
    try:
        query = """
        SELECT 
            vm.reg_no,
            hm.name as plant_name,
            dm.name as district_name,
            zm.zone_name
        FROM public.vehicle_master vm 
        LEFT JOIN public.hosp_master hm ON vm.id_hosp = hm.id_no 
        LEFT JOIN public.district_master dm ON hm.id_dist = dm.id_no 
        LEFT JOIN public.zone_master zm ON dm.id_zone = zm.id_no 
        WHERE vm.id_hosp IS NOT NULL 
        AND hm.id_dist IS NOT NULL 
        AND dm.id_zone IS NOT NULL
        LIMIT 5
        """
        columns, rows = run_sql_query(query)
        if rows:
            print(f"✅ Found {len(rows)} vehicles with complete hierarchy:")
            for row in rows:
                print(f"   🚛 Vehicle: {row[0]}")
                print(f"   🏭 Plant: {row[1]}")
                print(f"   🏢 District: {row[2]}")
                print(f"   🌍 Zone: {row[3]}")
                print("   " + "-" * 40)
        else:
            print("❌ No vehicles with complete hierarchy found")
    except Exception as e:
        print(f"❌ Error querying complete hierarchy: {e}")

def test_hierarchical_queries():
    """Test specific hierarchical queries that the chatbot should handle"""
    print("\n🎯 Testing Hierarchical Query Patterns")
    print("=" * 50)
    
    # Test queries that should work with the new logic
    test_queries = [
        {
            'description': 'Get zone for a specific vehicle',
            'query': """
                SELECT zm.zone_name, vm.reg_no
                FROM public.zone_master zm 
                JOIN public.district_master dm ON zm.id_no = dm.id_zone 
                JOIN public.hosp_master hm ON dm.id_no = hm.id_dist 
                JOIN public.vehicle_master vm ON hm.id_no = vm.id_hosp 
                WHERE vm.reg_no IS NOT NULL
                LIMIT 1
            """
        },
        {
            'description': 'Get region for a specific vehicle',
            'query': """
                SELECT dm.name as region_name, vm.reg_no
                FROM public.district_master dm 
                JOIN public.hosp_master hm ON dm.id_no = hm.id_dist 
                JOIN public.vehicle_master vm ON hm.id_no = vm.id_hosp 
                WHERE vm.reg_no IS NOT NULL
                LIMIT 1
            """
        },
        {
            'description': 'Get plant for a specific vehicle',
            'query': """
                SELECT hm.name as plant_name, vm.reg_no
                FROM public.hosp_master hm 
                JOIN public.vehicle_master vm ON hm.id_no = vm.id_hosp 
                WHERE vm.reg_no IS NOT NULL
                LIMIT 1
            """
        },
        {
            'description': 'Get all vehicles in a zone',
            'query': """
                SELECT vm.reg_no, zm.zone_name
                FROM public.vehicle_master vm 
                JOIN public.hosp_master hm ON vm.id_hosp = hm.id_no 
                JOIN public.district_master dm ON hm.id_dist = dm.id_no 
                JOIN public.zone_master zm ON dm.id_zone = zm.id_no 
                WHERE zm.zone_name IS NOT NULL
                LIMIT 3
            """
        }
    ]
    
    for i, test in enumerate(test_queries, 1):
        print(f"\n{i}. {test['description']}:")
        try:
            columns, rows = run_sql_query(test['query'])
            if rows:
                print(f"✅ Query successful, found {len(rows)} results:")
                for row in rows:
                    print(f"   {dict(zip(columns, row))}")
            else:
                print("⚠️ Query successful but no results found")
        except Exception as e:
            print(f"❌ Query failed: {e}")

def test_enhanced_table_mapper():
    """Test the enhanced table mapper with hierarchical keywords"""
    print("\n🗺️ Testing Enhanced Table Mapper with Hierarchical Keywords")
    print("=" * 50)
    
    try:
        from src.nlp.enhanced_table_mapper import EnhancedTableMapper
        mapper = EnhancedTableMapper()
        
        test_queries = [
            "What zone does vehicle MH12AB1234 belong to?",
            "Show me all vehicles in zone North",
            "Which region is vehicle KA05CD5678 in?",
            "List all vehicles in Bangalore plant",
            "Show the complete hierarchy for vehicle TN09EF9012"
        ]
        
        for query in test_queries:
            print(f"\n📝 Query: '{query}'")
            try:
                priority_tables = mapper.get_priority_tables(query)
                print(f"   🎯 Priority tables: {priority_tables}")
                
                # Check for hierarchical pattern matches
                for pattern, tables in mapper.hierarchical_patterns.items():
                    import re
                    if re.search(pattern, query, re.IGNORECASE):
                        print(f"   ✅ Hierarchical pattern matched: {tables}")
                        break
                else:
                    print("   ⚠️ No hierarchical pattern matched")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
                
    except ImportError as e:
        print(f"❌ Could not import enhanced table mapper: {e}")

def test_intelligent_reasoning():
    """Test the intelligent reasoning with hierarchical patterns"""
    print("\n🧠 Testing Intelligent Reasoning with Hierarchical Patterns")
    print("=" * 50)
    
    try:
        from src.core.intelligent_reasoning import IntelligentReasoning
        reasoning = IntelligentReasoning()
        
        # Mock chat context
        class MockChatContext:
            def __init__(self):
                self.last_displayed_items = []
                self.history = []
        
        context = MockChatContext()
        
        test_queries = [
            "What zone does vehicle MH12AB1234 belong to?",
            "Show me the region for vehicle KA05CD5678",
            "Which plant does vehicle TN09EF9012 belong to?",
            "List vehicles in North zone",
            "Show vehicles in Mumbai region",
            "Give me the complete hierarchy for vehicle DL01GH2345"
        ]
        
        for query in test_queries:
            print(f"\n📝 Query: '{query}'")
            try:
                result = reasoning.analyze_query_intent(query, context)
                if result:
                    print(f"   ✅ Intent: {result['intent']}")
                    print(f"   📊 Extracted: {result['extracted_data']}")
                    
                    sql = reasoning.generate_intelligent_query(result)
                    if sql:
                        print(f"   🔧 SQL: {sql.strip()[:100]}...")
                    else:
                        print("   ⚠️ No SQL generated")
                else:
                    print("   ⚠️ No intelligent reasoning applied")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
                
    except ImportError as e:
        print(f"❌ Could not import intelligent reasoning: {e}")

def main():
    """Run all hierarchical tests"""
    print("🧪 Hierarchical Logic Test Suite")
    print("=" * 60)
    print("Testing zone → district → hosp_master → vehicle_master relationships")
    print("=" * 60)
    
    # Run all test suites
    test_hierarchical_structure()
    test_complete_hierarchy()
    test_hierarchical_queries()
    test_enhanced_table_mapper()
    test_intelligent_reasoning()
    
    print("\n" + "=" * 60)
    print("🎉 Hierarchical Logic Test Suite Complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
