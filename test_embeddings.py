#!/usr/bin/env python3

# Simple test for embeddings
import os
import sys
sys.path.append('/home/linux/Documents/chatbot-diya')

print("🔄 Testing embeddings system...")

try:
    from sql import get_full_schema
    print("✅ SQL module imported")
    
    schema = get_full_schema()
    print(f"✅ Schema loaded: {len(schema)} schemas found")
    
    from embeddings import EmbeddingManager
    print("✅ EmbeddingManager imported")
    
    manager = EmbeddingManager()
    print("✅ EmbeddingManager created")
    
    # Create embeddings for the first few tables only (for testing)
    print("🔄 Creating sample embeddings...")
    
    # Get first schema and first table for testing
    first_schema = list(schema.keys())[0]
    first_table = list(schema[first_schema].keys())[0]
    table_key = f"{first_schema}.{first_table}"
    columns = schema[first_schema][first_table]
    
    description = manager._create_table_description(first_table, columns)
    print(f"📝 Description for {table_key}: {description[:100]}...")
    
    embedding = manager.get_embedding(description)
    if embedding:
        print(f"✅ Embedding created: {len(embedding)} dimensions")
        manager.schema_embeddings[table_key] = embedding
        manager.table_descriptions[table_key] = description
        print("✅ Test embeddings stored")
    else:
        print("❌ Failed to create embedding")
        
    # Test finding relevant tables
    test_query = "show vehicle data"
    print(f"\n🔍 Testing query: '{test_query}'")
    
    relevant = manager.find_relevant_tables(test_query, top_k=3)
    if relevant:
        print("📊 Found relevant tables:")
        for table, similarity, desc in relevant:
            print(f"  • {table} (similarity: {similarity:.3f})")
    else:
        print("⚠️ No relevant tables found")
        
    print("\n🎉 Embeddings test completed successfully!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
