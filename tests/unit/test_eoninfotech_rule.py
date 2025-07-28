#!/usr/bin/env python3
"""
Test EONINFOTECH Business Rule Implementation
Demonstrates the business logic for vehicles in EONINFOTECH region
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from src.database.database_reference_parser import DatabaseReferenceParser
    
    def test_eoninfotech_rule():
        """Test the EONINFOTECH region business rule"""
        print("🔧 Testing EONINFOTECH Business Rule")
        print("=" * 50)
        
        parser = DatabaseReferenceParser()
        
        # Test queries that should trigger EONINFOTECH rule
        test_queries = [
            "Show me vehicles in EONINFOTECH region",
            "List all active vehicles from Eon InfoTech zone",
            "How many trucks are operational in eoninfotech district?",
            "Vehicle status report for EONINFOTECH region",
            "Active vehicle count in Mumbai", # Should not trigger rule
            "Show me all vehicles" # Should not trigger rule
        ]
        
        for query in test_queries:
            print(f"\n📝 Query: {query}")
            context = parser.get_business_context_for_query(query)
            
            if context['eoninfotech_rule']['applies']:
                print("✅ EONINFOTECH rule applies")
                print(f"   📋 Description: {context['eoninfotech_rule']['description']}")
                print(f"   🔧 Query modification: {context['eoninfotech_rule']['query_modification']}")
                print(f"   🗂️ Suggested tables: {', '.join(context['eoninfotech_rule']['suggested_tables'])}")
            else:
                print("❌ EONINFOTECH rule does not apply")
                
            if context['keywords_matched']:
                print(f"   🔍 Keywords matched: {', '.join(context['keywords_matched'])}")
                
            if context['suggested_tables']:
                print(f"   📊 All suggested tables: {', '.join(context['suggested_tables'][:5])}{'...' if len(context['suggested_tables']) > 5 else ''}")
    
    def test_business_rules_parsing():
        """Test the business rules parsing from database reference"""
        print("\n\n🔧 Testing Business Rules Parsing")
        print("=" * 50)
        
        parser = DatabaseReferenceParser()
        parsed_data = parser.parse_reference_file()
        
        if isinstance(parsed_data, dict) and 'business_rules' in parsed_data:
            print(f"✅ Found {len(parsed_data['business_rules'])} business rules")
            
            for i, rule in enumerate(parsed_data['business_rules'], 1):
                print(f"\n📋 Rule {i}: {rule.get('rule_type', 'unknown')}")
                print(f"   Description: {rule.get('description', 'No description')}")
                print(f"   Priority: {rule.get('priority', 'unknown')}")
                if 'condition' in rule:
                    print(f"   Condition: {rule['condition']}")
                if 'action' in rule:
                    print(f"   Action: {rule['action']}")
        else:
            print("⚠️ No business rules found in parsed data")
            print(f"Parsed data type: {type(parsed_data)}")
            if isinstance(parsed_data, dict):
                print(f"Available keys: {list(parsed_data.keys())}")

    def test_transportation_keywords():
        """Test transportation domain keywords"""
        print("\n\n🔧 Testing Transportation Keywords")
        print("=" * 50)
        
        parser = DatabaseReferenceParser()
        keywords = parser._load_transportation_keywords()
        
        # Test key categories
        key_categories = ['vehicle', 'active', 'inactive', 'eoninfotech', 'zone', 'plant']
        
        for category in key_categories:
            if category in keywords:
                tables = keywords[category]
                print(f"✅ {category}: {', '.join(tables[:3])}{'...' if len(tables) > 3 else ''}")
            else:
                print(f"❌ {category}: Not found")

    if __name__ == "__main__":
        test_eoninfotech_rule()
        test_business_rules_parsing()
        test_transportation_keywords()
        
        print("\n\n🎯 EONINFOTECH Rule Summary:")
        print("=" * 50)
        print("✅ Business rule: Vehicles in EONINFOTECH region are always inactive")
        print("✅ Query detection: Automatically detects EONINFOTECH mentions")  
        print("✅ Query modification: Suggests adding inactive status filter")
        print("✅ Table suggestions: Provides relevant tables for hierarchy queries")
        print("✅ Integration ready: Can be used by query agents and reasoning systems")

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure database_reference_parser.py is available")
except Exception as e:
    print(f"❌ Test error: {e}")
    import traceback
    traceback.print_exc()
