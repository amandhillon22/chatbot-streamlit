#!/usr/bin/env python3
"""
import sys
sys.path.append('/home/linux/Documents/chatbot-diya')

Simple test to check basic functionality without model loading
"""

print("🧪 Testing basic imports...")

try:
    print("1. Testing sql module...")
    from src.core.sql import get_full_schema
    print("✅ SQL module imported")
    
    print("2. Testing basic query_agent components...")
    import google.generativeai as genai
    print("✅ Google AI imported")
    
    print("3. Testing dotenv...")
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Environment loaded")
    
    print("4. Testing distance units (this might load database analysis)...")
    from src.database.distance_units import DistanceUnitManager
    print("✅ Distance units imported")
    
    print("5. Testing intelligent reasoning...")
    from src.core.intelligent_reasoning import IntelligentReasoning
    print("✅ Intelligent reasoning imported")
    
    print("🎉 All basic imports successful!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
