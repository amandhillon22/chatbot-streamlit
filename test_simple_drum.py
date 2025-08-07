#!/usr/bin/env python3
"""
Simple test for drum trip report integration
"""
import sys
sys.path.append('/home/linux/Documents/chatbot-diya')

def test_simple_query():
    """Test a simple drum trip report query"""
    print("🚀 Testing Simple Drum Trip Report Query")
    print("=" * 50)
    
    try:
        from src.core.query_agent import process_user_query
        
        # Test a very simple query
        test_query = "show me 5 drum trip reports"
        print(f"Testing query: '{test_query}'")
        
        result = process_user_query(test_query)
        
        if result.get('success'):
            print("✅ Query executed successfully!")
            print(f"📊 Returned {len(result.get('data', []))} results")
            
            # Show first result
            if result.get('data'):
                first_result = result['data'][0]
                print("📝 Sample result keys:", list(first_result.keys()))
                
                # Check if we have drum-specific data
                drum_keys = [k for k in first_result.keys() if 'loading' in k.lower() or 'plant' in k.lower() or 'site' in k.lower()]
                if drum_keys:
                    print("✅ Drum-specific data found:", drum_keys)
                else:
                    print("⚠️ No drum-specific data in results")
        else:
            print(f"❌ Query failed: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_simple_query()
