#!/usr/bin/env python3
"""
Simple comparison between the old and new embedding systems
"""

def test_old_vs_new_embeddings():
    print("🆚 Comparing Old TF-IDF vs New Sentence Transformer Embeddings")
    print("=" * 70)
    
    # Test queries
    test_queries = [
        "show vehicle information",
        "fuel consumption report", 
        "driver assignments",
        "trip analysis data",
        "GPS tracking records"
    ]
    
    try:
        # Test new sentence transformer system
        print("\n🚀 NEW: Sentence Transformer Embeddings")
        print("-" * 50)
        
        from sentence_embeddings import initialize_sentence_embeddings
        manager = initialize_sentence_embeddings()
        
        if manager:
            for query in test_queries:
                print(f"\n🔍 Query: '{query}'")
                relevant_tables = manager.find_relevant_tables(query, top_k=3)
                for i, (table, similarity, desc) in enumerate(relevant_tables, 1):
                    print(f"  {i}. {table} (similarity: {similarity:.3f})")
        else:
            print("❌ Could not initialize sentence transformer embeddings")
    
    except Exception as e:
        print(f"❌ Error testing sentence transformers: {e}")
    
    try:
        # Test old lightweight system if available
        print(f"\n🔄 OLD: TF-IDF Lightweight Embeddings")
        print("-" * 50)
        
        from create_lightweight_embeddings import LightweightEmbeddingManager
        import pickle
        import os
        
        if os.path.exists('embeddings_cache.pkl'):
            # Load old system
            with open('embeddings_cache.pkl', 'rb') as f:
                data = pickle.load(f)
            
            old_manager = LightweightEmbeddingManager()
            old_manager.schema_embeddings = data.get('schema_embeddings', {})
            old_manager.table_descriptions = data.get('table_descriptions', {})
            old_manager.fitted_vectorizer = data.get('vectorizer', None)
            
            if old_manager.fitted_vectorizer:
                for query in test_queries:
                    print(f"\n🔍 Query: '{query}'")
                    relevant_tables = old_manager.find_relevant_tables(query, top_k=3)
                    for i, (table, similarity, desc) in enumerate(relevant_tables, 1):
                        print(f"  {i}. {table} (similarity: {similarity:.3f})")
            else:
                print("❌ Old vectorizer not available")
        else:
            print("❌ Old embeddings cache not found")
            
    except Exception as e:
        print(f"❌ Error testing old system: {e}")
    
    print("\n" + "=" * 70)
    print("🎯 SUMMARY:")
    print("• NEW system uses sentence transformers for better semantic understanding")
    print("• NEW system stores embeddings in PostgreSQL (with pgvector fallback)")  
    print("• OLD system used TF-IDF with keyword matching boosts")
    print("• NEW system should show better relevance for semantic queries")

if __name__ == "__main__":
    test_old_vs_new_embeddings()
