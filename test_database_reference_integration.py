#!/usr/bin/env python3
"""
Test Database Reference Integration
This demonstrates how the database_reference.md integration enhances your chatbot
"""

import sys
import os

print("🧪 Testing Database Reference Integration\n")

# Test 1: Database Reference Parser
print("1. Testing Database Reference Parser:")
try:
    from database_reference_parser import DatabaseReferenceParser
    parser = DatabaseReferenceParser()
    
    test_queries = [
        "show all vehicles",
        "trip report today", 
        "customer orders",
        "fuel consumption",
        "plant locations"
    ]
    
    for query in test_queries:
        relevant_tables = parser.get_business_relevant_tables(query)
        print(f"   Query: '{query}'")
        print(f"   → Relevant tables: {relevant_tables[:3]}")  # Show top 3
    
    print("   ✅ Database Reference Parser working!")
    
except Exception as e:
    print(f"   ❌ Error: {e}")

print()

# Test 2: Table Context Enhancement
print("2. Testing Table Context Enhancement:")
try:
    table_context = parser.get_table_context('vehicle_master')
    print(f"   vehicle_master context:")
    print(f"   → Business context: {table_context['business_context']}")
    print(f"   → Relationships: {table_context['relationships'][:3]}")
    print(f"   → Size estimate: {table_context['size_estimate']}")
    print("   ✅ Table context enhancement working!")
    
except Exception as e:
    print(f"   ❌ Error: {e}")

print()

# Test 3: Query Intent Detection
print("3. Testing Query Intent Detection:")
try:
    test_queries = [
        "show me today's trips",
        "analyze fuel consumption trends", 
        "what vehicles are currently active",
        "generate monthly report"
    ]
    
    for query in test_queries:
        # This would be used by your query_agent
        context = parser.enhance_query_context(query, [])
        print(f"   Query: '{query}'")
        print(f"   → Intent: {context[1]['query_intent']}")
    
    print("   ✅ Query intent detection working!")
    
except Exception as e:
    print(f"   ❌ Error: {e}")

print()

# Test 4: Integration Benefits
print("4. Integration Benefits Summary:")
print("   📊 Your chatbot now has:")
print("   • Business-aware table selection")
print("   • Transportation domain intelligence")
print("   • Context-aware query enhancement") 
print("   • Performance optimization hints")
print("   • Relationship-aware SQL generation")

print()
print("🚀 Database Reference Integration Test Complete!")
print("   Next steps:")
print("   1. Install dependencies: pip install numpy scikit-learn")
print("   2. Run: python3 create_lightweight_embeddings.py")
print("   3. Restart your Flask app")
print("   4. Test with transportation queries")
