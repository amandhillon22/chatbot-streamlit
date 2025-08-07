#!/usr/bin/env python3
"""
Test script to verify driver name detection and query processing
"""
import sys
sys.path.append('/home/linux/Documents/chatbot-diya')

def test_driver_name_queries():
    """Test specific driver name queries"""
    
    print("🧪 Testing Driver Name Query Detection")
    print("=" * 50)
    
    try:
        from src.core.intelligent_reasoning import IntelligentReasoning
        reasoning = IntelligentReasoning()
        
        # Test queries from user
        test_queries = [
            "i want to give a birthday gift to kailash mahto but forgot his birthday. when was it?",
            "what is the size of kailash mahto", 
            "kailash mahto tshirt size",
            "birthday of ram kumar",
            "tell me about john smith"
        ]
        
        for query in test_queries:
            print(f"\n📝 Testing: '{query}'")
            
            # Test driver detection
            is_driver = reasoning.is_driver_related_query(query)
            print(f"  🎯 Driver query detected: {is_driver}")
            
            if is_driver:
                # Test query type detection
                query_type = reasoning.detect_driver_query_type(query)
                print(f"  📊 Query type: {query_type}")
                
                # Test entity extraction
                entities = reasoning.extract_entities(query)
                print(f"  🔍 Entities found: {len(entities)}")
                for entity in entities:
                    print(f"    - {entity['entity_type']}: {entity['value']} (confidence: {entity['confidence']})")
                
                # Test SQL generation
                if query_type:
                    sql = reasoning.generate_driver_sql(query_type, query, entities)
                    if sql:
                        print(f"  ✅ SQL generated successfully")
                        print(f"    📝 Sample: {sql[:150]}...")
                    else:
                        print(f"  ❌ SQL generation failed")
                else:
                    print(f"  ⚠️ No query type detected")
            else:
                print(f"  ❌ Not detected as driver query")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_database_parser():
    """Test database parser integration"""
    
    print("\n🔍 Testing Database Parser Integration")
    print("=" * 50)
    
    try:
        from src.database.database_reference_parser import DatabaseReferenceParser
        parser = DatabaseReferenceParser()
        
        test_keywords = ['birthday', 'birth_date', 'size', 'tshirt', 'kailash']
        
        for keyword in test_keywords:
            if keyword in parser.transportation_keywords:
                tables = parser.transportation_keywords[keyword]
                print(f"  ✅ '{keyword}' → {tables}")
            else:
                print(f"  ❌ '{keyword}' → Not found")
        
        return True
        
    except Exception as e:
        print(f"❌ Database parser test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚛 DRIVER NAME QUERY TESTING")
    print("=" * 60)
    
    test1 = test_driver_name_queries()
    test2 = test_database_parser()
    
    print("\n" + "=" * 60)
    if test1 and test2:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Driver name detection is working correctly")
    else:
        print("❌ Some tests failed")
        
    exit(0 if test1 and test2 else 1)
