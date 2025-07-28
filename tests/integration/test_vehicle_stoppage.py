#!/usr/bin/env python3
"""
Test script for vehicle stoppage report functionality
"""

import sys
sys.path.append('/home/linux/Documents/chatbot-diya')

def test_stoppage_imports():
    """Test if all required modules can be imported"""
    try:
        from src.database.database_reference_parser import DatabaseReferenceParser
        print("✅ DatabaseReferenceParser imported successfully")
        
        from src.nlp.enhanced_table_mapper import EnhancedTableMapper
        print("✅ EnhancedTableMapper imported successfully")
        
        # Test direct function imports instead of class
        from src.core.query_agent import english_to_sql, generate_final_response
        print("✅ Query agent functions imported successfully")
        
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_stoppage_keywords():
    """Test if stoppage keywords are properly configured"""
    try:
        from src.database.database_reference_parser import DatabaseReferenceParser
        
        parser = DatabaseReferenceParser()
        
        # Test stoppage-related keywords
        test_queries = [
            "vehicle stoppage report",
            "show vehicle stops", 
            "vehicle tracking",
            "overspeeding report",
            "distance report"
        ]
        
        for query in test_queries:
            # Use the correct method name
            result = parser.get_business_relevant_tables(query)
            print(f"Query: '{query}'")
            print(f"Business relevant tables: {result}")
            print("-" * 50)
            
    except Exception as e:
        print(f"❌ Keyword test error: {e}")
        import traceback
        traceback.print_exc()

def test_table_mapping():
    """Test if util_report table is properly mapped"""
    try:
        from src.nlp.enhanced_table_mapper import EnhancedTableMapper
        
        mapper = EnhancedTableMapper()
        
        # Test queries that should map to util_report
        test_queries = [
            "show vehicle stoppage reports",
            "get vehicle tracking data",
            "overspeeding vehicles"
        ]
        
        for query in test_queries:
            # Use the correct method name
            priority_tables = mapper.get_priority_tables(query)
            print(f"Query: '{query}'")
            print(f"Priority tables: {priority_tables}")
            print("-" * 50)
            
    except Exception as e:
        print(f"❌ Table mapping test error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚗 Testing Vehicle Stoppage Report System")
    print("=" * 60)
    
    # Test imports
    print("\n1. Testing Imports...")
    if not test_stoppage_imports():
        sys.exit(1)
    
    # Test keywords
    print("\n2. Testing Stoppage Keywords...")
    test_stoppage_keywords()
    
    # Test table mapping
    print("\n3. Testing Table Mapping...")
    test_table_mapping()
    
    print("\n✅ All tests completed!")
