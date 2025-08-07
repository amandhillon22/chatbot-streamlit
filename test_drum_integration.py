#!/usr/bin/env python3
"""
Test script to verify drum trip report integration
"""
import sys
sys.path.append('/home/linux/Documents/chatbot-diya')

def test_drum_trip_queries():
    """Test various drum trip report queries"""
    
    print("🚀 Testing Drum Trip Report Integration")
    print("=" * 50)
    
    # Test queries that should detect drum_trip_report
    test_queries = [
        "show drum trip reports",
        "concrete delivery data",
        "transit mixer journeys", 
        "plant to site distance",
        "loading and unloading times",
        "concrete transport cycles",
        "drum operation reports",
        "TM delivery records",
        "site waiting times",
        "plant departure and return times"
    ]
    
    # Test with lightweight embeddings
    try:
        from src.nlp.create_lightweight_embeddings import LightweightEmbeddingManager
        import pickle
        import os
        
        cache_path = '/home/linux/Documents/chatbot-diya/embeddings_cache.pkl'
        if os.path.exists(cache_path):
            with open(cache_path, 'rb') as f:
                data = pickle.load(f)
            
            manager = LightweightEmbeddingManager()
            manager.schema_embeddings = data.get('schema_embeddings', {})
            manager.table_descriptions = data.get('table_descriptions', {})
            manager.fitted_vectorizer = data.get('vectorizer', None)
            
            print("📊 LIGHTWEIGHT EMBEDDINGS TEST:")
            print("-" * 30)
            
            for query in test_queries:
                relevant = manager.find_relevant_tables(query, top_k=3)
                print(f"\n🔍 Query: '{query}'")
                
                drum_detected = False
                for table, similarity in relevant:
                    print(f"  • {table} (similarity: {similarity:.3f})")
                    if 'drum_trip_report' in table.lower():
                        print("    ✅ DRUM TRIP REPORT DETECTED!")
                        drum_detected = True
                
                if not drum_detected:
                    print("    ⚠️ Drum trip report not in top 3 results")
        else:
            print("⚠️ Lightweight embeddings cache not found")
            
    except Exception as e:
        print(f"❌ Lightweight embeddings test failed: {e}")
    
    print("\n" + "=" * 50)
    
    # Test with sentence transformers
    try:
        from src.nlp.sentence_embeddings import sentence_embedding_manager
        if sentence_embedding_manager:
            print("🤖 SENTENCE TRANSFORMER TEST:")
            print("-" * 30)
            
            for query in test_queries[:5]:  # Test fewer queries due to processing time
                relevant = sentence_embedding_manager.find_relevant_tables(query, top_k=3)
                print(f"\n🔍 Query: '{query}'")
                
                drum_detected = False
                for table, similarity, desc in relevant:
                    print(f"  • {table} (similarity: {similarity:.3f})")
                    if 'drum_trip_report' in table.lower():
                        print("    ✅ DRUM TRIP REPORT DETECTED!")
                        drum_detected = True
                
                if not drum_detected:
                    print("    ⚠️ Drum trip report not in top 3 results")
        else:
            print("⚠️ Sentence embedding manager not available")
            
    except Exception as e:
        print(f"❌ Sentence transformer test failed: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Drum Trip Report Integration Test Complete!")

if __name__ == "__main__":
    test_drum_trip_queries()
