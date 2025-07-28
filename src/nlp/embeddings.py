import google.generativeai as genai
import os
import json
import numpy as np
import sys
sys.path.append('/home/linux/Documents/chatbot-diya')

from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
import pickle
from src.core.sql import get_full_schema

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class EmbeddingManager:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-2.5-pro")
        self.schema_embeddings = {}
        self.table_descriptions = {}
        self.query_patterns = {}
        
    def get_embedding(self, text):
        """Get embedding for a given text using Google's embedding model."""
        try:
            # Use Gemini to generate text embedding
            # Note: We'll simulate embeddings using text similarity for now
            # In production, you'd use Google's dedicated embedding API
            response = self.model.generate_content(
                f"Generate a numerical representation for: {text}. "
                f"Return only a simple hash-like number that represents the semantic meaning."
            )
            
            # For now, we'll create a simple hash-based embedding
            # This is a placeholder - in production use proper embedding API
            text_hash = hash(text.lower().strip()) % (10**8)
            
            # Create a pseudo-embedding vector
            np.random.seed(text_hash)
            embedding = np.random.normal(0, 1, 384)  # 384-dimensional vector
            return embedding.tolist()
            
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return None
    
    def create_schema_embeddings(self):
        """Create embeddings for all tables and columns in the database."""
        print("🔄 Creating schema embeddings...")
        
        schema_dict = get_full_schema()
        
        for schema_name, tables in schema_dict.items():
            for table_name, columns in tables.items():
                table_key = f"{schema_name}.{table_name}"
                
                # Create descriptive text for the table
                description = self._create_table_description(table_name, columns)
                self.table_descriptions[table_key] = description
                
                # Generate embedding for the table
                embedding = self.get_embedding(description)
                if embedding:
                    self.schema_embeddings[table_key] = embedding
                    
        print(f"✅ Created embeddings for {len(self.schema_embeddings)} tables")
        self.save_embeddings()
        
    def _create_table_description(self, table_name, columns):
        """Create a human-readable description of a table for embedding."""
        # Transportation domain specific descriptions
        transportation_keywords = {
            'trip': 'vehicle journey travel route distance',
            'vehicle': 'bus car truck fleet transportation',
            'driver': 'operator person staff employee',
            'route': 'path direction destination stops',
            'fuel': 'gas diesel consumption efficiency',
            'maintenance': 'repair service fix schedule',
            'alert': 'notification warning event issue',
            'gps': 'location tracking position coordinates',
            'report': 'summary data analysis statistics'
        }
        
        # Generate contextual description
        context_words = []
        table_lower = table_name.lower()
        
        for keyword, description in transportation_keywords.items():
            if keyword in table_lower:
                context_words.append(description)
        
        # Combine table name, columns, and context
        description = f"Table {table_name} contains data about {' '.join(context_words)}. "
        description += f"Columns: {', '.join(columns)}. "
        
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
                
        if column_context:
            description += f"Contains {', '.join(set(column_context))} data."
            
        return description
    
    def find_relevant_tables(self, user_query, top_k=5):
        """Find the most relevant tables for a user query."""
        if not self.schema_embeddings:
            self.load_embeddings()
            
        if not self.schema_embeddings:
            print("⚠️ No embeddings found. Creating new ones...")
            self.create_schema_embeddings()
            
        query_embedding = self.get_embedding(user_query)
        if not query_embedding:
            return []
            
        similarities = []
        
        for table_key, table_embedding in self.schema_embeddings.items():
            similarity = cosine_similarity(
                [query_embedding], 
                [table_embedding]
            )[0][0]
            similarities.append((table_key, similarity, self.table_descriptions[table_key]))
            
        # Sort by similarity and return top matches
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]
    
    def save_embeddings(self):
        """Save embeddings to disk for faster loading."""
        data = {
            'schema_embeddings': self.schema_embeddings,
            'table_descriptions': self.table_descriptions,
            'query_patterns': self.query_patterns
        }
        
        # Use absolute path for embeddings cache
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        cache_path = os.path.join(project_root, 'embeddings_cache.pkl')
        
        with open(cache_path, 'wb') as f:
            pickle.dump(data, f)
        print("💾 Embeddings saved to cache")
    
    def load_embeddings(self):
        """Load embeddings from disk."""
        try:
            # Use absolute path for embeddings cache
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            cache_path = os.path.join(project_root, 'embeddings_cache.pkl')
            
            with open(cache_path, 'rb') as f:
                data = pickle.load(f)
                self.schema_embeddings = data.get('schema_embeddings', {})
                self.table_descriptions = data.get('table_descriptions', {})
                self.query_patterns = data.get('query_patterns', {})
            print(f"📂 Loaded embeddings for {len(self.schema_embeddings)} tables")
            return True
        except FileNotFoundError:
            print("📂 No embedding cache found")
            return False
    
    def add_query_pattern(self, user_query, sql_query, success=True):
        """Store successful query patterns for future matching."""
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
    
    def find_similar_query(self, user_query, threshold=0.8):
        """Find similar previous queries."""
        if not self.query_patterns:
            return None
            
        query_embedding = self.get_embedding(user_query)
        if not query_embedding:
            return None
            
        best_match = None
        best_similarity = 0
        
        for pattern_key, pattern_data in self.query_patterns.items():
            similarity = cosine_similarity(
                [query_embedding],
                [pattern_data['embedding']]
            )[0][0]
            
            if similarity > best_similarity and similarity > threshold:
                best_similarity = similarity
                best_match = pattern_data
                
        return best_match if best_match else None

# Global instance
embedding_manager = EmbeddingManager()

def initialize_embeddings():
    """Initialize embeddings system - load from cache only, don't create new ones."""
    if embedding_manager.load_embeddings():
        print("🚀 Embeddings loaded from cache successfully")
        return embedding_manager
    else:
        print("⚠️ No embeddings cache found. Running without embeddings for now.")
        print("💡 You can create embeddings later by running: python create_embeddings.py")
        return None

if __name__ == "__main__":
    # Test the embedding system
    manager = initialize_embeddings()
    
    # Test query
    test_query = "show me vehicle trip data"
    relevant_tables = manager.find_relevant_tables(test_query)
    
    print(f"\n🔍 For query: '{test_query}'")
    print("📊 Most relevant tables:")
    for table, similarity, description in relevant_tables:
        print(f"  • {table} (similarity: {similarity:.3f})")
        print(f"    {description[:100]}...")
