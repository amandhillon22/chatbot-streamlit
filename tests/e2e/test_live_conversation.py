#!/usr/bin/env python3
"""
import sys
sys.path.append('/home/linux/Documents/chatbot-diya')

Test script to simulate the exact live conversation that failed
"""

import requests
import json

def test_live_conversation():
    """Test the exact conversation that failed in the live chatbot"""
    
    print("🧪 Testing Live Conversation Simulation")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:5000"
    
    # Test 1: Show me all vehicles
    print("\n1️⃣ Testing: 'show me all the vehicles'")
    response1 = requests.post(f"{base_url}/chat", json={
        "message": "show me all the vehicles",
        "history": []
    })
    
    if response1.status_code == 200:
        data1 = response1.json()
        print(f"✅ Response received")
        print(f"📊 Response preview: {data1.get('response', '')[:100]}...")
        
        # Extract vehicle list to identify the 7th vehicle
        response_text = data1.get('response', '')
        if 'registration' in response_text.lower() or 'vehicle' in response_text.lower():
            print("✅ Vehicle list detected in response")
        
        # Test 2: Ask about 7th vehicle
        print("\n2️⃣ Testing: 'What region does the 7th vehicle belong to?'")
        
        history = [{
            "user": "show me all the vehicles",
            "response": data1.get('response', '')
        }]
        
        response2 = requests.post(f"{base_url}/chat", json={
            "message": "What region does the 7th vehicle belong to?",
            "history": history
        })
        
        if response2.status_code == 200:
            data2 = response2.json()
            print(f"📊 Response: {data2.get('response', '')}")
            
            if "couldn't find" in data2.get('response', '').lower():
                print("❌ ORDINAL REFERENCE FAILED - Bot claims no data found")
            else:
                print("✅ ORDINAL REFERENCE WORKING")
        else:
            print(f"❌ Request failed: {response2.status_code}")
    else:
        print(f"❌ Request failed: {response1.status_code}")
    
    # Test 3: Direct vehicle query
    print("\n3️⃣ Testing: 'Tell me about vehicle MH12UM0524' (7th from actual list)")
    response3 = requests.post(f"{base_url}/chat", json={
        "message": "Tell me about vehicle MH12UM0524",
        "history": []
    })
    
    if response3.status_code == 200:
        data3 = response3.json()
        print(f"📊 Response: {data3.get('response', '')[:200]}...")
    else:
        print(f"❌ Request failed: {response3.status_code}")

if __name__ == "__main__":
    test_live_conversation()
