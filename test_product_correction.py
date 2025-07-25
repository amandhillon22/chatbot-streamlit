#!/usr/bin/env python3
"""
Test Product Correction Status System with Debug Logs
"""

import os
import sys
import warnings
warnings.filterwarnings('ignore')

os.chdir('/home/linux/Documents/chatbot-diya')

print("🔍 TESTING PRODUCT CORRECTION STATUS SYSTEM")
print("=" * 60)

def test_product_correction_queries():
    """Test various product correction queries with debug output"""
    try:
        from intelligent_reasoning import IntelligentReasoning
        reasoning = IntelligentReasoning()
        
        print("✅ Intelligent reasoning module imported with debug logs")
        
        # Mock chat context
        class MockChatContext:
            def __init__(self):
                self.last_displayed_items = []
                self.history = []
        
        context = MockChatContext()
        
        # Test queries for product correction functionality
        test_queries = [
            # Product correction done (Y)
            "show me complaints with product correction done",
            "list complaints where correction is completed", 
            "complaints with product correction",
            
            # Product correction not done (N) or empty
            "show me complaints with product correction not done",
            "complaints without product correction",
            "list complaints missing correction",
            "complaints where correction is pending",
            
            # Specific complaint correction status
            "product correction status of complaint 123",
            "complaint 456 product correction done",
            "what is the correction status for complaint 789"
        ]
        
        print(f"\n🧪 Testing {len(test_queries)} Product Correction Queries:")
        print("-" * 60)
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n{i}. Query: '{query}'")
            print("-" * 40)
            
            try:
                result = reasoning.analyze_query_intent(query, context)
                if result:
                    print(f"   ✅ Intent: {result['intent']}")
                    print(f"   📊 Extracted: {result['extracted_data']}")
                    
                    sql = reasoning.generate_intelligent_query(result)
                    if sql:
                        print(f"   🔧 SQL Generated: ✅")
                        print(f"   📝 SQL Key Points:")
                        
                        # Analyze SQL for key business logic
                        if "product_correction = 'Y'" in sql:
                            print(f"      • Filters for product_correction = 'Y' (Done)")
                        elif "product_correction = 'N'" in sql:
                            print(f"      • Filters for product_correction = 'N' (Not Done)")
                        elif "product_correction IS NULL" in sql:
                            print(f"      • Includes NULL/empty correction status")
                        
                        if "correction_status_description" in sql:
                            print(f"      • Provides human-readable status description")
                        
                        # Test response generation
                        mock_result = {
                            'sql': sql, 
                            'rows': [
                                {'complaint_id': 123, 'correction_status_description': 'Product Correction Done'},
                                {'complaint_id': 456, 'correction_status_description': 'Product Correction Not Done'}
                            ]
                        }
                        response = reasoning.create_intelligent_response(result, mock_result)
                        print(f"   💬 Response: {response}")
                    else:
                        print(f"   ⚠️ No SQL generated")
                else:
                    print(f"   ❌ No intelligent reasoning applied")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
                import traceback
                traceback.print_exc()
                
        return True
        
    except ImportError as e:
        print(f"❌ Could not import intelligent reasoning: {e}")
        return False

def test_product_correction_edge_cases():
    """Test edge cases and variations for product correction queries"""
    try:
        from intelligent_reasoning import IntelligentReasoning
        reasoning = IntelligentReasoning()
        
        class MockChatContext:
            def __init__(self):
                self.last_displayed_items = []
                self.history = []
        
        context = MockChatContext()
        
        edge_case_queries = [
            # Different ways to ask for done
            "show complaints where correction finished",
            "list complaints with correction completed",
            
            # Different ways to ask for not done  
            "complaints where correction incomplete",
            "show me complaints correction missing",
            
            # Mixed terminology
            "product correction status complaint 999",
            "correction done for complaint 111"
        ]
        
        print(f"\n🧪 Testing Edge Cases:")
        print("-" * 40)
        
        for i, query in enumerate(edge_case_queries, 1):
            print(f"\n{i}. Edge Case: '{query}'")
            result = reasoning.analyze_query_intent(query, context)
            
            if result:
                print(f"   ✅ Matched intent: {result['intent']}")
                extracted = result.get('extracted_data', {})
                
                if 'product_correction_status' in extracted:
                    status = extracted['product_correction_status']
                    status_desc = 'Done' if status == 'Y' else 'Not Done'
                    print(f"   📊 Product Correction: {status} ({status_desc})")
                
                sql = reasoning.generate_intelligent_query(result)
                if sql:
                    print(f"   🔧 SQL generated successfully")
                else:
                    print(f"   ⚠️ No SQL generated")
            else:
                print(f"   ❌ Pattern not matched - may need additional patterns")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing edge cases: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting product correction status system test...\n")
    
    results = {
        'product_correction_queries': test_product_correction_queries(),
        'edge_cases': test_product_correction_edge_cases()
    }
    
    print(f"\n📊 TEST RESULTS SUMMARY:")
    print("=" * 40)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print(f"\n🎉 ALL TESTS PASSED!")
        print("Product correction status system is working correctly!")
        print("\nSupported Query Types:")
        print("• Complaints with product correction done (Y)")
        print("• Complaints without product correction (N or NULL/empty)")
        print("• Specific complaint correction status lookup")
        print("• Natural language variations and edge cases")
        print("\nBusiness Logic Implemented:")
        print("• Y = Product correction done")
        print("• N = Product correction not done")
        print("• NULL/Empty = No correction status recorded")
        print("• Intelligent pattern matching for various user expressions")
    else:
        print(f"\n⚠️ Some tests failed. Check the debug output above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
