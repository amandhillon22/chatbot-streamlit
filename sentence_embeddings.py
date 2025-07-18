#!/usr/bin/env python3
"""
Advanced Embedding System using Sentence Transformers and PostgreSQL with pgvector
This replaces the previous TF-IDF approach with proper semantic embeddings.
"""

import os
import json
import numpy as np
import psycopg2
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv
from sql import get_full_schema, get_connection
import warnings

# Suppress some warnings from sentence transformers
warnings.filterwarnings("ignore", category=FutureWarning)

load_dotenv()

class SentenceEmbeddingManager:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        """
        Initialize the sentence embedding manager.
        
        Args:
            model_name: SentenceTransformer model to use. 
                       'all-MiniLM-L6-v2' is fast and efficient (384 dimensions)
                       'all-mpnet-base-v2' is more accurate but slower (768 dimensions)
        """
        print(f"🤖 Loading SentenceTransformer model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.embedding_dim = self.model.get_sentence_embedding_dimension()
        print(f"✅ Model loaded. Embedding dimension: {self.embedding_dim}")
        
        self.table_descriptions = {}
        self.query_patterns = {}
        
        # Initialize pgvector extension and create tables
        self._setup_pgvector_database()
        
    def _setup_pgvector_database(self):
        """Setup PostgreSQL database with vector support (pgvector if available, otherwise fallback)."""
        self.use_pgvector = False
        
        # First, try to enable pgvector extension
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            conn.commit()
            cur.close()
            conn.close()
            self.use_pgvector = True
            print("✅ pgvector extension enabled - using native vector operations")
        except psycopg2.Error as e:
            print(f"⚠️ pgvector extension not available: {e}")
            print("🔄 Using fallback mode with JSON storage and scikit-learn similarity")
            self.use_pgvector = False
            try:
                if 'conn' in locals():
                    conn.rollback()
                    cur.close()
                    conn.close()
            except:
                pass
        
        # Now create tables in a fresh transaction
        try:
            conn = get_connection()
            cur = conn.cursor()
            
            # Create schema embeddings table
            if self.use_pgvector:
                cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS schema_embeddings (
                        id SERIAL PRIMARY KEY,
                        table_key VARCHAR(255) UNIQUE NOT NULL,
                        description TEXT NOT NULL,
                        embedding vector({self.embedding_dim}),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
            else:
                # Fallback: store embeddings as JSON
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS schema_embeddings (
                        id SERIAL PRIMARY KEY,
                        table_key VARCHAR(255) UNIQUE NOT NULL,
                        description TEXT NOT NULL,
                        embedding_json TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
            
            # Create query patterns table
            if self.use_pgvector:
                cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS query_patterns (
                        id SERIAL PRIMARY KEY,
                        user_query TEXT NOT NULL,
                        sql_query TEXT NOT NULL,
                        embedding vector({self.embedding_dim}),
                        success BOOLEAN DEFAULT TRUE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
            else:
                # Fallback: store embeddings as JSON
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS query_patterns (
                        id SERIAL PRIMARY KEY,
                        user_query TEXT NOT NULL,
                        sql_query TEXT NOT NULL,
                        embedding_json TEXT NOT NULL,
                        success BOOLEAN DEFAULT TRUE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
            
            # Create indexes for efficient search
            if self.use_pgvector:
                try:
                    cur.execute("""
                        CREATE INDEX IF NOT EXISTS schema_embeddings_vector_idx 
                        ON schema_embeddings USING ivfflat (embedding vector_cosine_ops) 
                        WITH (lists = 100);
                    """)
                    cur.execute("""
                        CREATE INDEX IF NOT EXISTS query_patterns_vector_idx 
                        ON query_patterns USING ivfflat (embedding vector_cosine_ops) 
                        WITH (lists = 100);
                    """)
                    print("✅ Vector indexes created for efficient similarity search")
                except psycopg2.Error as e:
                    print(f"⚠️ Could not create vector indexes: {e}")
            else:
                # Create regular indexes for fallback mode
                cur.execute("CREATE INDEX IF NOT EXISTS schema_embeddings_table_key_idx ON schema_embeddings (table_key);")
                cur.execute("CREATE INDEX IF NOT EXISTS query_patterns_created_idx ON query_patterns (created_at);")
                print("✅ Regular indexes created for fallback mode")
            
            conn.commit()
            cur.close()
            conn.close()
            print("✅ Database tables created successfully")
            
        except Exception as e:
            print(f"❌ Error setting up database: {e}")
            raise
    
    def _create_table_description(self, table_name, columns):
        """Create a comprehensive description of a table for embedding."""
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
        description = f"Database table named {table_name} "
        
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
        
        # Add column information with semantic context
        description += f"Contains data columns: {', '.join(columns)}. "
        
        # Add column-based semantic context with distance unit detection
        semantic_context = []
        distance_columns = []
        
        for col in columns:
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in ['id', 'key']):
                semantic_context.append("identifier")
            elif any(keyword in col_lower for keyword in ['name', 'title', 'description']):
                semantic_context.append("name or description")
            elif any(keyword in col_lower for keyword in ['date', 'time', 'timestamp']):
                semantic_context.append("temporal data")
            elif any(keyword in col_lower for keyword in ['distance', 'km', 'mile', 'meter', 'metre']):
                # Enhanced distance detection with unit hints
                if 'km' in col_lower or 'kilometer' in col_lower:
                    distance_columns.append(f"{col} (likely kilometers)")
                    semantic_context.append("distance in kilometers")
                elif any(word in col_lower for word in ['meter', 'metre', 'm_', '_m']):
                    distance_columns.append(f"{col} (likely meters)")
                    semantic_context.append("distance in meters")
                else:
                    distance_columns.append(f"{col} (distance - unit detection needed)")
                    semantic_context.append("distance measurement")
            elif 'fuel' in col_lower:
                semantic_context.append("fuel consumption")
            elif any(keyword in col_lower for keyword in ['status', 'state']):
                semantic_context.append("status information")
            elif any(keyword in col_lower for keyword in ['speed', 'velocity']):
                semantic_context.append("speed measurement")
            elif any(keyword in col_lower for keyword in ['lat', 'lng', 'longitude', 'latitude', 'location']):
                semantic_context.append("geographic coordinates")
            elif any(keyword in col_lower for keyword in ['count', 'total', 'sum', 'amount']):
                semantic_context.append("numerical aggregate")
                
        if semantic_context:
            description += f"This table stores {', '.join(set(semantic_context))}."
            
        # Add specific distance column information
        if distance_columns:
            description += f" Distance columns: {', '.join(distance_columns)}."
            
        return description
    
    def create_schema_embeddings(self):
        """Generate and store embeddings for all database tables."""
        print("🔄 Creating sentence transformer embeddings for database schema...")
        
        schema_dict = get_full_schema()
        
        # Clear existing embeddings
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM schema_embeddings;")
        
        embeddings_created = 0
        
        for schema_name, tables in schema_dict.items():
            for table_name, columns in tables.items():
                table_key = f"{schema_name}.{table_name}"
                
                # Create descriptive text for the table
                description = self._create_table_description(table_name, columns)
                self.table_descriptions[table_key] = description
                
                # Generate embedding using sentence transformer
                embedding = self.model.encode(description, convert_to_tensor=False)
                embedding_list = embedding.tolist()
                
                # Store in database (pgvector or fallback mode)
                if self.use_pgvector:
                    cur.execute("""
                        INSERT INTO schema_embeddings (table_key, description, embedding)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (table_key) DO UPDATE SET
                            description = EXCLUDED.description,
                            embedding = EXCLUDED.embedding,
                            updated_at = CURRENT_TIMESTAMP;
                    """, (table_key, description, embedding_list))
                else:
                    # Fallback: store as JSON
                    embedding_json = json.dumps(embedding_list)
                    cur.execute("""
                        INSERT INTO schema_embeddings (table_key, description, embedding_json)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (table_key) DO UPDATE SET
                            description = EXCLUDED.description,
                            embedding_json = EXCLUDED.embedding_json,
                            updated_at = CURRENT_TIMESTAMP;
                    """, (table_key, description, embedding_json))
                
                embeddings_created += 1
                
        conn.commit()
        cur.close()
        conn.close()
        
        mode = "pgvector" if self.use_pgvector else "fallback JSON"
        print(f"✅ Created {embeddings_created} sentence transformer embeddings and stored in PostgreSQL ({mode} mode)")
    
    def get_embedding(self, text):
        """Generate embedding for given text using sentence transformer."""
        try:
            embedding = self.model.encode(text, convert_to_tensor=False)
            return embedding.tolist()
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return None
        
    def find_relevant_tables(self, user_query, top_k=5):
        """Find the most relevant tables using vector similarity search."""
        # Generate embedding for user query
        query_embedding = self.get_embedding(user_query)
        if not query_embedding:
            return []
        
        try:
            conn = get_connection()
            cur = conn.cursor()
            
            if self.use_pgvector:
                # Use pgvector's cosine similarity for efficient search
                cur.execute("""
                    SELECT 
                        table_key, 
                        description,
                        1 - (embedding <=> %s::vector) as similarity
                    FROM schema_embeddings
                    ORDER BY similarity DESC
                    LIMIT %s;
                """, (query_embedding, top_k))
                
                results = cur.fetchall()
                cur.close()
                conn.close()
                
                # Return in the same format as the old system
                return [(table_key, similarity, description) for table_key, description, similarity in results]
            else:
                # Fallback: manual cosine similarity calculation
                cur.execute("SELECT table_key, description, embedding_json FROM schema_embeddings;")
                results = cur.fetchall()
                cur.close()
                conn.close()
                
                similarities = []
                for table_key, description, embedding_json in results:
                    try:
                        embedding = json.loads(embedding_json)
                        similarity = cosine_similarity([query_embedding], [embedding])[0][0]
                        similarities.append((table_key, similarity, description))
                    except (json.JSONDecodeError, ValueError) as e:
                        print(f"⚠️ Error parsing embedding for {table_key}: {e}")
                        continue
                
                # Sort by similarity and return top matches
                similarities.sort(key=lambda x: x[1], reverse=True)
                return similarities[:top_k]
                
        except Exception as e:
            print(f"❌ Error in similarity search: {e}")
            return []
    
    def add_query_pattern(self, user_query, sql_query, success=True):
        """Store successful query patterns for future matching."""
        if not success:
            return
            
        query_embedding = self.get_embedding(user_query)
        if not query_embedding:
            return
        
        try:
            conn = get_connection()
            cur = conn.cursor()
            
            if self.use_pgvector:
                cur.execute("""
                    INSERT INTO query_patterns (user_query, sql_query, embedding, success)
                    VALUES (%s, %s, %s, %s);
                """, (user_query, sql_query, query_embedding, success))
            else:
                # Fallback: store as JSON
                embedding_json = json.dumps(query_embedding)
                cur.execute("""
                    INSERT INTO query_patterns (user_query, sql_query, embedding_json, success)
                    VALUES (%s, %s, %s, %s);
                """, (user_query, sql_query, embedding_json, success))
            
            conn.commit()
            cur.close()
            conn.close()
            
        except Exception as e:
            print(f"❌ Error storing query pattern: {e}")
    
    def find_similar_query(self, user_query, threshold=0.8):
        """Find similar previous queries using vector similarity."""
        query_embedding = self.get_embedding(user_query)
        if not query_embedding:
            return None
        
        try:
            conn = get_connection()
            cur = conn.cursor()
            
            if self.use_pgvector:
                # Find most similar successful query using pgvector
                cur.execute("""
                    SELECT 
                        user_query,
                        sql_query,
                        1 - (embedding <=> %s::vector) as similarity
                    FROM query_patterns
                    WHERE success = TRUE
                    ORDER BY similarity DESC
                    LIMIT 1;
                """, (query_embedding,))
                
                result = cur.fetchone()
                cur.close()
                conn.close()
                
                if result and result[2] > threshold:
                    return {
                        'query': result[0],
                        'sql': result[1],
                        'similarity': result[2]
                    }
            else:
                # Fallback: manual similarity calculation
                cur.execute("SELECT user_query, sql_query, embedding_json FROM query_patterns WHERE success = TRUE;")
                results = cur.fetchall()
                cur.close()
                conn.close()
                
                best_match = None
                best_similarity = 0
                
                for user_q, sql_q, embedding_json in results:
                    try:
                        embedding = json.loads(embedding_json)
                        similarity = cosine_similarity([query_embedding], [embedding])[0][0]
                        if similarity > best_similarity and similarity > threshold:
                            best_similarity = similarity
                            best_match = {
                                'query': user_q,
                                'sql': sql_q,
                                'similarity': similarity
                            }
                    except (json.JSONDecodeError, ValueError):
                        continue
                
                return best_match
            
            return None
            
        except Exception as e:
            print(f"❌ Error finding similar query: {e}")
            return None
    
    def get_embedding_stats(self):
        """Get statistics about stored embeddings."""
        try:
            conn = get_connection()
            cur = conn.cursor()
            
            cur.execute("SELECT COUNT(*) FROM schema_embeddings;")
            schema_count = cur.fetchone()[0]
            
            cur.execute("SELECT COUNT(*) FROM query_patterns WHERE success = TRUE;")
            pattern_count = cur.fetchone()[0]
            
            cur.close()
            conn.close()
            
            return {
                'schema_embeddings': schema_count,
                'query_patterns': pattern_count,
                'embedding_dimension': self.embedding_dim,
                'pgvector_enabled': self.use_pgvector,
                'model_info': str(self.model)
            }
            
        except Exception as e:
            print(f"❌ Error getting embedding stats: {e}")
            return {}

# Global instance
sentence_embedding_manager = None

def initialize_sentence_embeddings():
    """Initialize the sentence embedding system."""
    global sentence_embedding_manager
    
    if sentence_embedding_manager is None:
        try:
            sentence_embedding_manager = SentenceEmbeddingManager()
            print("🚀 Sentence embedding system initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize sentence embedding system: {e}")
            return None
    
    return sentence_embedding_manager

if __name__ == "__main__":
    print("🚀 Setting up advanced embedding system with Sentence Transformers + pgvector...")
    
    # Initialize the embedding manager
    manager = SentenceEmbeddingManager()
    
    # Create embeddings for the database schema
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
        "vehicle master data",
        "maintenance records",
        "GPS tracking data"
    ]
    
    print("\n🧪 Testing sentence transformer embeddings:")
    for query in test_queries:
        relevant = manager.find_relevant_tables(query, top_k=3)
        print(f"\n🔍 Query: '{query}'")
        for table, similarity, desc in relevant:
            print(f"  • {table} (similarity: {similarity:.3f})")
            print(f"    {desc[:80]}...")
    
    # Display statistics
    stats = manager.get_embedding_stats()
    print(f"\n📊 Embedding Statistics:")
    print(f"  • Schema embeddings: {stats.get('schema_embeddings', 0)}")
    print(f"  • Query patterns: {stats.get('query_patterns', 0)}")
    print(f"  • Embedding dimension: {stats.get('embedding_dimension', 'unknown')}")
    print(f"  • pgvector enabled: {stats.get('pgvector_enabled', False)}")
    
    print("\n✅ Advanced embedding system created successfully!")
    print("🔄 The system is ready to use with improved semantic understanding.")
