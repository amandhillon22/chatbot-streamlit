#!/usr/bin/env python3
"""
sys.path.append('/home/linux/Documents/chatbot-diya')

Test script for the new sentence transformer embedding system
"""

import sys
import os

# Suppress streamlit warnings
import warnings
warnings.filterwarnings("ignore")

print("🧪 Testing the new sentence transformer embedding system...")

try:
    print("1. Testing sentence embeddings import...")
    from src.nlp.sentence_embeddings import initialize_sentence_embeddings
    print("✅ Sentence embeddings import successful")
    
    print("2. Initializing sentence embedding manager...")
    manager = initialize_sentence_embeddings()
    if manager:
        print("✅ Sentence embedding manager initialized")
        
        # Get stats
        stats = manager.get_embedding_stats()
        print(f"📊 Embeddings loaded: {stats.get('schema_embeddings', 0)} tables")
        print(f"📊 Query patterns: {stats.get('query_patterns', 0)}")
        print(f"📊 Embedding dimension: {stats.get('embedding_dimension', 'unknown')}")
        print(f"📊 pgvector enabled: {stats.get('pgvector_enabled', False)}")
        
        # Test similarity search
        print("3. Testing similarity search...")
        test_query = "show vehicle trip data"
        relevant_tables = manager.find_relevant_tables(test_query, top_k=3)
        
        print(f"🔍 Query: '{test_query}'")
        print("🎯 Most relevant tables:")
        for table, similarity, description in relevant_tables:
            print(f"  • {table} (similarity: {similarity:.3f})")
        
        print("✅ All tests passed! The sentence transformer system is working.")
    else:
        print("❌ Failed to initialize embedding manager")
        
except Exception as e:
    print(f"❌ Test failed: {e}")
    import traceback
    traceback.print_exc()

print("🏁 Test completed.")
