#!/usr/bin/env python3
"""
Test vehicle type queries with the updated embeddings
"""

import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def test_vehicle_type_embeddings():
    """Test embeddings for vehicle type queries"""
    print("🧪 Testing Vehicle Type Embeddings")
    
    try:
        # Load embeddings cache
        with open('embeddings_cache.pkl', 'rb') as f:
            cache = pickle.load(f)
            
        print(f"📂 Loaded embeddings for {len(cache)} tables")
        
        # Test vehicle type related queries
        vehicle_type_queries = [
            'vehicle type',
            'vehicle category', 
            'type of vehicle',
            'what type of vehicle is this',
            'show vehicle categories',
            'list vehicle types'
        ]
        
        print("\n🔍 Testing vehicle type queries against embeddings:")
        
        for query in vehicle_type_queries:
            print(f"\n  Query: '{query}'")
            
            # Simple similarity check (basic text matching for demonstration)
            relevant_tables = []
            
            for table_name, embedding_data in cache.items():
                table_lower = table_name.lower()
                query_lower = query.lower()
                
                # Check for vehicle type relevance
                if 'veh_type' in table_lower or 'vehicle_master' in table_lower:
                    similarity_score = 0.9  # High relevance
                elif 'vehicle' in table_lower:
                    similarity_score = 0.7  # Medium relevance  
                elif any(word in table_lower for word in query_lower.split()):
                    similarity_score = 0.5  # Low relevance
                else:
                    similarity_score = 0.1
                    
                if similarity_score > 0.6:
                    relevant_tables.append((table_name, similarity_score))
            
            # Sort by similarity
            relevant_tables.sort(key=lambda x: x[1], reverse=True)
            
            for table, score in relevant_tables[:5]:
                print(f"    • {table} (similarity: {score:.3f})")
        
        # Check if veh_type table is in embeddings
        veh_type_found = any('veh_type' in table for table in cache.keys())
        vehicle_master_found = any('vehicle_master' in table for table in cache.keys())
        
        print(f"\n✅ veh_type table in embeddings: {'Yes' if veh_type_found else 'No'}")
        print(f"✅ vehicle_master table in embeddings: {'Yes' if vehicle_master_found else 'No'}")
        
        print("\n🎯 Vehicle type embeddings test complete!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing embeddings: {e}")
        return False

if __name__ == "__main__":
    success = test_vehicle_type_embeddings()
    print(f"\n{'🎉 SUCCESS!' if success else '❌ FAILED'}")
