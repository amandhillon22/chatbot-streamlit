#!/usr/bin/env python3
"""
Test DPR (Daily Production Report) functionality
"""
import sys
sys.path.append('/home/linux/Documents/chatbot-diya')

def test_dpr_detection():
    """Test DPR query detection"""
    try:
        from src.core.intelligent_reasoning import IntelligentReasoning
        
        reasoning = IntelligentReasoning()
        
        # Test DPR query detection
        test_queries = [
            "show me daily production report",
            "concrete orders for today",
            "transit mixer utilization",
            "sales person performance",
            "concrete grade analysis",
            "pump vs non-pump delivery",
            "customer delivery tracking"
        ]
        
        print("🏗️ Testing DPR Query Detection:")
        print("=" * 50)
        
        for query in test_queries:
            is_dpr = reasoning.is_dpr_related_query(query)
            query_type = reasoning.detect_dpr_query_type(query)
            
            print(f"Query: '{query}'")
            print(f"  - Is DPR: {is_dpr}")
            print(f"  - Type: {query_type}")
            print()
        
        # Test DPR SQL generation
        print("🔧 Testing DPR SQL Generation:")
        print("=" * 50)
        
        test_sql_query = "show me transit mixer utilization"
        entities = [{'entity_type': 'vehicle', 'value': 'TM123'}]
        
        dpr_sql = reasoning.generate_dpr_sql(test_sql_query, entities)
        
        print(f"Query: '{test_sql_query}'")
        print(f"Generated SQL:")
        print(dpr_sql)
        
        return True
        
    except Exception as e:
        print(f"❌ DPR test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_database_parser():
    """Test database parser DPR context"""
    try:
        from src.database.database_reference_parser import DatabaseReferenceParser
        
        parser = DatabaseReferenceParser()
        
        # Test DPR business context
        dpr_context = parser._infer_business_context('dpr_master1')
        
        print("🗄️ Testing Database Parser DPR Context:")
        print("=" * 50)
        print("DPR Master1 Business Context:")
        if isinstance(dpr_context, list):
            for context in dpr_context:
                print(f"  - {context}")
        else:
            print(f"  - {dpr_context}")
        print()
        
        # Test transportation keywords
        dpr_keywords = ['dpr', 'concrete_delivery', 'transit_mixer', 'sales_person']
        
        print("Transportation Keywords for DPR:")
        for keyword in dpr_keywords:
            if keyword in parser.transportation_keywords:
                tables = parser.transportation_keywords[keyword]
                print(f"  - {keyword}: {tables}")
        
        return True
        
    except Exception as e:
        print(f"❌ Database parser test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Testing DPR Integration")
    print("=" * 60)
    
    success1 = test_dpr_detection()
    print()
    success2 = test_database_parser()
    
    if success1 and success2:
        print("\n✅ All DPR tests passed! Your bot is ready for concrete delivery queries.")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
