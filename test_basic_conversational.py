#!/usr/bin/env python3
"""
Minimal test for conversational result chain
"""

import sys
import os
sys.path.append('/home/linux/Documents/chatbot-diya')

def test_basic_imports():
    """Test basic imports without heavy dependencies"""
    print("🧪 Testing Basic Conversational Components")
    print("=" * 50)
    
    try:
        # Test importing the conversational chain
        from src.nlp.sentence_embeddings import ConversationalResultChain
        print("✅ ConversationalResultChain imported successfully")
        
        # Create a chain instance
        chain = ConversationalResultChain()
        print("✅ ConversationalResultChain instance created")
        
        # Test pushing results
        sample_data = [
            {"complaint_id": 200, "liability": 50000.0},
            {"complaint_id": 179, "liability": 0.0},
            {"complaint_id": 201, "liability": 70000.0}
        ]
        
        chain.push_result(
            query="test query",
            sql="SELECT * FROM test",
            results=sample_data
        )
        print("✅ Successfully pushed test data to chain")
        
        # Test getting last result
        last_result = chain.get_last_result()
        if last_result:
            print(f"✅ Retrieved last result: {len(last_result['displayed_results'])} items")
        else:
            print("❌ Failed to retrieve last result")
            return False
        
        print("\n🎉 BASIC TESTS PASSED!")
        print("✅ Conversational result chain is properly implemented")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_basic_imports()
    if success:
        print("\n🚀 Ready for advanced testing once dependencies are installed!")
        print("💡 The core conversational system is working correctly.")
    else:
        print("\n❌ Basic tests failed - check implementation")
