#!/usr/bin/env python3
"""
Test script to debug drum trip report queries
"""
import sys
import os
sys.path.append('.')

from src.core.query_agent import generate_sql_with_llm

def test_drum_trip_query():
    print("🧪 Testing AI-first drum trip query generation...")
    
    # Test simple drum trip query
    test_queries = [
        "show me 10 drum trip reports",
        "drum trip details for 5 vehicles",
        "loading time data"
    ]
    
    for query in test_queries:
        print(f"\n📝 Testing query: '{query}'")
        print("-" * 60)
        
        try:
            result = generate_sql_with_llm(query, "", None)
            
            if result:
                print(f"✅ Schema: {result.get('schema')}")
                print(f"📊 SQL: {result.get('sql')}")
                print(f"💬 Response: {result.get('response')}")
                print(f"🔄 Follow-up: {result.get('follow_up')}")
            else:
                print("❌ No result returned")
                
        except Exception as e:
            print(f"⚠️ Error: {e}")
    
    print("\n" + "="*80)

if __name__ == "__main__":
    test_drum_trip_query()
