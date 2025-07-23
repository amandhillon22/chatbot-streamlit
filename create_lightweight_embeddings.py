#!/usr/bin/env python3
"""
Lightweight embeddings creator that uses text-based similarity instead of API calls
This avoids API quota issues while still providing semantic understanding
Enhanced with database reference intelligence
"""

import os
import json
import numpy as np
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sql import get_full_schema

# Import database reference integration
try:
    from database_reference_parser import database_reference_parser
    DATABASE_REFERENCE_AVAILABLE = True
    print("✅ Database reference parser integration available")
except ImportError:
    DATABASE_REFERENCE_AVAILABLE = False
    print("⚠️ Database reference parser not available - using basic keywords")

class LightweightEmbeddingManager:
    def __init__(self):
        self.schema_embeddings = {}
        self.table_descriptions = {}
        self.query_patterns = {}
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=300)
        self.fitted_vectorizer = None
        
        # Initialize database reference enhancement
        self.db_reference_data = None
        if DATABASE_REFERENCE_AVAILABLE:
            try:
                self.db_reference_data = database_reference_parser.parse_reference_file()
                print(f"📊 Loaded reference data for {len(self.db_reference_data)} tables")
            except Exception as e:
                print(f"⚠️ Could not load database reference: {e}")

    def _create_table_description(self, table_name, columns):
        """Create a human-readable description of a table for embedding."""
        
        # Enhanced description with database reference
        if DATABASE_REFERENCE_AVAILABLE and self.db_reference_data:
            return self._create_enhanced_description(table_name, columns)
        
        # Fallback to original transportation keywords
        return self._create_basic_description(table_name, columns)
    
    def _create_enhanced_description(self, table_name, columns):
        """Create enhanced description using database reference data"""
        
        # Get business context from database reference
        table_context = database_reference_parser.get_table_context(table_name)
        
        # Start with exact table name
        description = f"Table named {table_name} "
        
        # Add business context from reference
        if table_context.get('business_context'):
            description += f"used for {table_context['business_context']}. "
        
        # Add column information
        description += f"Contains columns: {', '.join(columns)}. "
        
        # Add relationship hints
        relationships = table_context.get('relationships', [])
        if relationships:
            description += f"Commonly joins with: {', '.join(relationships[:3])}. "
        
        # Add size context for performance
        size = table_context.get('size_estimate', 'medium')
        if size == 'large':
            description += "Large table - consider using LIMIT clauses. "
        
        # Add column-based transportation context
        column_context = self._analyze_columns_for_context(columns)
        if column_context:
            description += f"Key operations: {column_context}. "
        
        return description
    
    def _create_basic_description(self, table_name, columns):
        """Original description creation method as fallback."""
        # Transportation domain specific descriptions
        transportation_keywords = {
            'trip': 'vehicle journey travel route distance',
            'vehicle': 'bus car truck fleet transportation automobile',
            'master': 'reference main primary data registry list',
            'driver': 'operator person staff employee',
            'route': 'path direction destination stops',
            'fuel': 'gas diesel consumption efficiency',
            'maintenance': 'repair service fix schedule',
            'alert': 'notification warning event issue',
            'gps': 'location tracking position coordinates',
            'report': 'summary data analysis statistics',
            'history': 'past records log archive',
            'status': 'state condition current situation',
            'ignition': 'engine start stop power',
            'location': 'position place coordinates',
            'speed': 'velocity rate movement',
            'time': 'timestamp datetime schedule',
            'count': 'total number quantity amount',
            'total': 'sum aggregate count number',
            'so': 'sales order service order work order',
            'details': 'information data records specifics'
        }
        
        # Generate contextual description starting with the exact table name
        description = f"Table named {table_name} "
        
        # Add table name parts as keywords
        table_parts = table_name.lower().split('_')
        table_keywords = []
        for part in table_parts:
            if part in transportation_keywords:
                table_keywords.extend(transportation_keywords[part].split())
            else:
                table_keywords.append(part)
        
        if table_keywords:
            description += f"relates to {' '.join(set(table_keywords))}. "
        
        # Add column information
        description += f"Contains columns: {', '.join(columns)}. "
        
        # Add column-based context
        column_context = []
        for col in columns:
            col_lower = col.lower()
            if 'id' in col_lower:
                column_context.append("identifier")
            elif 'name' in col_lower or 'title' in col_lower:
                column_context.append("name")
            elif 'date' in col_lower or 'time' in col_lower:
                column_context.append("timestamp")
            elif 'distance' in col_lower or 'km' in col_lower:
                column_context.append("distance")
            elif 'fuel' in col_lower:
                column_context.append("fuel consumption")
            elif 'status' in col_lower:
                column_context.append("status information")
            elif 'speed' in col_lower:
                column_context.append("velocity")
            elif 'lat' in col_lower or 'lng' in col_lower or 'location' in col_lower:
                column_context.append("location coordinates")
                
        if column_context:
            description += f"Stores {', '.join(set(column_context))} data."
            
        return description
    
    def _analyze_columns_for_context(self, columns):
        """Analyze columns to understand table operations"""
        context_operations = []
        
        columns_lower = [col.lower() for col in columns]
        
        # Detect common operations based on column patterns
        if any('distance' in col for col in columns_lower):
            context_operations.append('distance tracking')
        if any('fuel' in col for col in columns_lower):
            context_operations.append('fuel management')
        if any('time' in col or 'date' in col for col in columns_lower):
            context_operations.append('time-based reporting')
        if any('status' in col for col in columns_lower):
            context_operations.append('status monitoring')
        if any('amount' in col or 'cost' in col or 'price' in col for col in columns_lower):
            context_operations.append('financial tracking')
        
        return ', '.join(context_operations)
        
    def create_schema_embeddings(self):
        """Create TF-IDF based embeddings for all tables."""
        print("🔄 Creating lightweight schema embeddings...")
        
        schema_dict = get_full_schema()
        descriptions = []
        table_keys = []
        
        # Create descriptions for all tables
        for schema_name, tables in schema_dict.items():
            for table_name, columns in tables.items():
                table_key = f"{schema_name}.{table_name}"
                description = self._create_table_description(table_name, columns)
                
                table_keys.append(table_key)
                descriptions.append(description)
                self.table_descriptions[table_key] = description
        
        # Create TF-IDF embeddings
        if descriptions:
            tfidf_matrix = self.vectorizer.fit_transform(descriptions)
            self.fitted_vectorizer = self.vectorizer
            
            # Store embeddings
            for i, table_key in enumerate(table_keys):
                self.schema_embeddings[table_key] = tfidf_matrix[i].toarray()[0].tolist()
        
        print(f"✅ Created lightweight embeddings for {len(self.schema_embeddings)} tables")
        self.save_embeddings()
        
    def get_embedding(self, text):
        """Get TF-IDF embedding for text."""
        if not self.fitted_vectorizer:
            return None
        try:
            tfidf_vector = self.fitted_vectorizer.transform([text])
            return tfidf_vector.toarray()[0].tolist()
        except:
            return None
    
    def find_relevant_tables(self, user_query, top_k=10):
        """Enhanced table finding with database reference intelligence"""
        
        # Get business-relevant tables from database reference
        if DATABASE_REFERENCE_AVAILABLE:
            business_tables = database_reference_parser.get_business_relevant_tables(user_query)
            
            # Combine with existing embedding-based search
            embedding_results = self._find_tables_by_embeddings(user_query, top_k)
            
            # Merge results with business intelligence
            return self._merge_table_results(business_tables, embedding_results, user_query)
        
        # Fallback to original method
        return self._find_tables_by_embeddings(user_query, top_k)
    
    def _find_tables_by_embeddings(self, query, top_k=10):
        """Original embedding-based table search"""
        if not self.schema_embeddings:
            return []
            
        query_embedding = self.get_embedding(query)
        if not query_embedding:
            return []
            
        similarities = []
        query_lower = query.lower()
        query_words = set(query_lower.replace('_', ' ').split())
        
        for table_key, table_embedding in self.schema_embeddings.items():
            # Calculate base TF-IDF similarity
            base_similarity = cosine_similarity(
                [query_embedding], 
                [table_embedding]
            )[0][0]
            
            table_name = table_key.split('.', 1)[1] if '.' in table_key else table_key
            table_name_lower = table_name.lower()
            table_parts = table_name_lower.split('_')
            
            # Calculate name-based boost with multiple strategies
            name_boost = 0.0
            
            # Strategy 1: Exact table name match
            if table_name_lower in query_lower or query_lower.replace(' ', '_') == table_name_lower:
                name_boost = 0.8
            
            # Strategy 2: Table starts with query terms (e.g., "so" matches "so_status", "so_details")
            elif any(table_name_lower.startswith(word) for word in query_words if len(word) >= 2):
                name_boost = 0.7
            
            # Strategy 3: Query words match table parts exactly
            elif query_words.intersection(set(table_parts)):
                matched_parts = len(query_words.intersection(set(table_parts)))
                name_boost = min(0.6, matched_parts * 0.3)
            
            # Strategy 4: Partial word matches within table parts
            else:
                partial_matches = 0
                for query_word in query_words:
                    for table_part in table_parts:
                        if len(query_word) >= 3 and query_word in table_part:
                            partial_matches += 1
                        elif len(table_part) >= 3 and table_part in query_word:
                            partial_matches += 1
                if partial_matches > 0:
                    name_boost = min(0.4, partial_matches * 0.2)
            
            # Strategy 5: Prefix matching for abbreviations (so -> so_*)
            if any(table_name_lower.startswith(f"{word}_") for word in query_words if len(word) >= 2):
                name_boost = max(name_boost, 0.6)
            
            # Combine base similarity with name boost
            final_similarity = min(1.0, base_similarity * 0.3 + name_boost * 0.7)
            
            similarities.append((table_key, final_similarity, self.table_descriptions[table_key]))
            
        # Sort by similarity and return top matches
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]
    
    def _merge_table_results(self, business_tables, embedding_results, query):
        """Merge business intelligence with embedding results"""
        merged_results = []
        seen_tables = set()
        
        # First, add business-relevant tables with high priority
        for table in business_tables[:5]:  # Top 5 business relevant
            table_key = f"public.{table}"  # Assume public schema
            if table_key in self.schema_embeddings:
                # Give business-relevant tables a boost
                similarity = 0.9  # High relevance score
                description = self.table_descriptions.get(table_key, f"Business-relevant table: {table}")
                merged_results.append((table_key, similarity, description))
                seen_tables.add(table_key)
        
        # Then add embedding results that aren't already included
        for table_key, similarity, description in embedding_results:
            if table_key not in seen_tables:
                merged_results.append((table_key, similarity, description))
                seen_tables.add(table_key)
        
        # Sort by similarity and return
        merged_results.sort(key=lambda x: x[1], reverse=True)
        return merged_results[:10]  # Return top 10
    
    def save_embeddings(self):
        """Save embeddings to disk."""
        data = {
            'schema_embeddings': self.schema_embeddings,
            'table_descriptions': self.table_descriptions,
            'query_patterns': self.query_patterns,
            'vectorizer': self.fitted_vectorizer
        }
        
        with open('embeddings_cache.pkl', 'wb') as f:
            pickle.dump(data, f)
        print("💾 Lightweight embeddings saved to cache")
    
    def add_query_pattern(self, user_query, sql_query, success=True):
        """Store successful query patterns."""
        if success:
            query_embedding = self.get_embedding(user_query)
            if query_embedding:
                pattern_key = f"pattern_{len(self.query_patterns)}"
                self.query_patterns[pattern_key] = {
                    'query': user_query,
                    'sql': sql_query,
                    'embedding': query_embedding
                }
                self.save_embeddings()

if __name__ == "__main__":
    print("🚀 Creating lightweight embeddings (no API calls needed)...")
    
    manager = LightweightEmbeddingManager()
    manager.create_schema_embeddings()
    
    # Test the system
    test_queries = [
        "show vehicle information",
        "trip report data", 
        "fuel consumption",
        "driver details",
        "alert notifications",
        "so status details",
        "show so status",
        "so tables",
        "vehicle master"
    ]
    
    print("\n🧪 Testing embeddings:")
    for query in test_queries:
        relevant = manager.find_relevant_tables(query, top_k=5)
        print(f"\n🔍 Query: '{query}'")
        for table, similarity, desc in relevant:
            if 'so_' in table.lower():
                print(f"  ✅ {table} (similarity: {similarity:.3f})")
            else:
                print(f"  • {table} (similarity: {similarity:.3f})")
    
    # Special test for so_ tables
    print(f"\n🔍 Special test - All tables starting with 'so_':")
    so_tables = [key for key in manager.schema_embeddings.keys() if key.split('.', 1)[1].startswith('so_')]
    print(f"Found {len(so_tables)} tables starting with 'so_': {so_tables}")
    
    test_result = manager.find_relevant_tables("show so status", top_k=10)
    print(f"\n🎯 Results for 'show so status' (top 10):")
    for table, similarity, desc in test_result:
        marker = "✅" if 'so_' in table.lower() else "•"
        print(f"  {marker} {table} (similarity: {similarity:.3f})")
    
    print("\n✅ Lightweight embeddings created successfully!")
    print("🔄 Restart your Flask app to use the new embeddings.")
