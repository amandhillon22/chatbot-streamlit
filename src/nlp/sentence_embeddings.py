#!/usr/bin/env python3
"""
import sys
sys.path.append('/home/linux/Documents/chatbot-diya')

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
from src.core.sql import get_full_schema, db_manager
import warnings
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import re
import hashlib

# Suppress some warnings from sentence transformers
warnings.filterwarnings("ignore", category=FutureWarning)

load_dotenv()

class ConversationalResultChain:
    """Pure AI-powered result chaining - handles ANY follow-up query type"""
    
    def __init__(self):
        self.result_stack = []
        self.max_history = 5
    
    def push_result(self, query: str, sql: str, results: List[Dict], display_results: List[Dict] = None):
        """Store query results for potential AI-powered operations"""
        result_entry = {
            'timestamp': datetime.now(),
            'original_query': query,
            'sql_executed': sql,
            'full_results': results,
            'displayed_results': display_results or results[:50],  # Store reasonable amount
            'result_count': len(results),
            'displayed_count': len(display_results) if display_results else min(len(results), 50)
        }
        
        self.result_stack.append(result_entry)
        
        # Keep only recent results
        if len(self.result_stack) > self.max_history:
            self.result_stack.pop(0)
    
    def get_last_result(self) -> Optional[Dict]:
        """Get the most recent result set"""
        return self.result_stack[-1] if self.result_stack else None
    
    def apply_ai_operation_to_last_result(self, user_query: str, conversation_history: List[str]) -> Dict:
        """Let AI handle ANY operation on previous results - no rigid patterns"""
        last_result = self.get_last_result()
        if not last_result:
            return None
        
        # Import here to avoid circular imports
        try:
            from src.core.query_agent import gemini_direct_answer as call_llm
        except ImportError:
            # Fallback if query_agent not available
            print("⚠️ LLM manager not available for AI operations")
            return None
        
        # Enhanced AI operation prompt with entity-specific awareness
        ai_operation_prompt = f"""
You are analyzing a follow-up query that refers to previous results.

CONVERSATION HISTORY:
{chr(10).join(conversation_history[-3:]) if conversation_history else "No previous queries"}

CURRENT USER QUERY: "{user_query}"

PREVIOUS RESULTS CONTEXT:
- Original query was: "{last_result['original_query']}"
- Number of results shown: {last_result['displayed_count']}
- Total results available: {last_result['result_count']}
- Sample data structure: {json.dumps(last_result['displayed_results'][0] if last_result['displayed_results'] else {}, indent=2)}

IMPORTANT: The user is asking for something specific about the previous results. Analyze what they want:

1. If they ask for "more details" about a specific entity (like "leakage issue complaint"), you should:
   - Identify the specific entity they're referring to
   - Filter the previous results to show only that entity
   - Indicate that more detailed information might be needed from the database

2. For other operations, generate appropriate Python code to operate on the data

Respond in JSON format:
{{
    "operation_type": "filter|count|show_details|aggregate|analyze|extract|detail_expansion",
    "user_intent": "clear description of what user wants",
    "target_entity": "specific entity/item user is asking about (if any)",
    "python_code": "safe Python code that operates on 'data' variable containing the previous results",
    "needs_detailed_query": true/false,
    "confidence": 0.0-1.0
}}

Examples:
- "more detail about leakage issue complaint" → {{"operation_type": "detail_expansion", "target_entity": "leakage issue", "needs_detailed_query": true}}
- "which ones are under 10000?" → {{"operation_type": "filter", "python_code": "[item for item in data if item.get('liability', 0) < 10000]"}}
- "how many are these?" → {{"operation_type": "count", "python_code": "len(data)"}}

Make sure to identify specific entities when the user asks for "more details" or "tell me about" something specific.
"""
        
        try:
            ai_response = call_llm(ai_operation_prompt)
            operation_plan = json.loads(ai_response)
            
            if operation_plan.get('confidence', 0) < 0.6:
                return None  # Not confident enough
            
            # Execute the AI-generated code safely
            return self._execute_ai_operation(operation_plan, last_result)
            
        except Exception as e:
            print(f"AI operation planning failed: {e}")
            # Enhanced fallback - try to understand the query without LLM
            return self._fallback_operation_detection(user_query, last_result, conversation_history)
    
    def _fallback_operation_detection(self, user_query: str, last_result: Dict, conversation_history: List[str]) -> Dict:
        """Fallback operation detection when LLM is not available"""
        query_lower = user_query.lower()
        
        # Detect detail expansion requests
        if any(pattern in query_lower for pattern in ["more detail", "more info", "tell me about", "explain"]):
            # Try to extract entity with improved patterns
            import re
            entity_patterns = [
                r'(?:detail|info).*?about\s+(?:the\s+)?([a-zA-Z\s]+?)(?:\s+complaint|\s+issue|$)',
                r'(?:tell me about|explain)\s+(?:the\s+)?([a-zA-Z\s]+?)(?:\s+complaint|\s+issue|$)',
                r'more.*?([a-zA-Z]+\s+issue)',
                r'details.*?([a-zA-Z]+\s+complaint)'
            ]
            
            target_entity = None
            for pattern in entity_patterns:
                match = re.search(pattern, query_lower)
                if match:
                    target_entity = match.group(1).strip()
                    break
            
            if target_entity:
                return {
                    'operation_type': 'detail_expansion',
                    'target_entity': target_entity,
                    'needs_detailed_query': True,
                    'user_intent': f'get detailed information about {target_entity}',
                    'confidence': 0.8
                }
        
        # Detect count operations
        if any(pattern in query_lower for pattern in ["how many", "count", "total number"]):
            return {
                'operation_type': 'count',
                'python_code': 'len(data)',
                'user_intent': 'count total items',
                'confidence': 0.9
            }
        
        # Detect filter operations
        filter_patterns = [
            (r'which ones? are (under|less than|below) (\d+)', 'numeric_filter_less'),
            (r'which ones? are (over|more than|above) (\d+)', 'numeric_filter_more'),
            (r'show.*only.*(\w+)', 'text_filter'),
            (r'filter.*by.*(\w+)', 'general_filter')
        ]
        
        for pattern, filter_type in filter_patterns:
            match = re.search(pattern, query_lower)
            if match:
                if filter_type == 'numeric_filter_less':
                    value = match.group(2)
                    return {
                        'operation_type': 'filter',
                        'python_code': f'[item for item in data if any(float(v) < {value} for k, v in item.items() if isinstance(v, (int, float)) and "liability" in k.lower())]',
                        'user_intent': f'filter items with values less than {value}',
                        'confidence': 0.8
                    }
                elif filter_type == 'numeric_filter_more':
                    value = match.group(2)
                    return {
                        'operation_type': 'filter',
                        'python_code': f'[item for item in data if any(float(v) > {value} for k, v in item.items() if isinstance(v, (int, float)) and "liability" in k.lower())]',
                        'user_intent': f'filter items with values more than {value}',
                        'confidence': 0.8
                    }
        
        # If no clear pattern detected
        return None
    
    def _execute_ai_operation(self, operation_plan: Dict, last_result: Dict) -> Dict:
        """Safely execute AI-generated operation on previous results"""
        try:
            operation_type = operation_plan.get('operation_type', 'unknown')
            
            # Handle detail expansion differently
            if operation_type == 'detail_expansion':
                target_entity = operation_plan.get('target_entity', '')
                needs_detailed_query = operation_plan.get('needs_detailed_query', False)
                
                if needs_detailed_query:
                    # Filter previous results for the specific entity first
                    data = last_result['displayed_results']
                    filtered_results = []
                    
                    # Use AI to understand which items match the target entity
                    for item in data:
                        # Convert item to string representation for matching
                        item_text = ' '.join(str(v).lower() for v in item.values() if v is not None)
                        if target_entity.lower() in item_text:
                            filtered_results.append(item)
                    
                    if filtered_results:
                        return {
                            'type': 'detail_expansion_needed',
                            'entity': target_entity,
                            'filtered_results': filtered_results,
                            'user_intent': operation_plan.get('user_intent', f'get details about {target_entity}'),
                            'message': f"Found {len(filtered_results)} matching result(s). Let me get detailed information..."
                        }
                    else:
                        return {
                            'type': 'filtered_results',
                            'data': [],
                            'message': f"I couldn't find any results matching '{target_entity}' in the previous data.",
                            'metadata': {
                                'is_follow_up': True,
                                'operation': 'filter',
                                'filter_applied': f'search for {target_entity}',
                                'original_count': last_result['displayed_count'],
                                'filtered_count': 0
                            }
                        }
            
            # For other operations, use the generated Python code
            if operation_plan.get('python_code'):
                # Prepare safe execution environment
                safe_globals = {
                    "__builtins__": {},
                    "len": len,
                    "sum": sum,
                    "min": min,
                    "max": max,
                    "float": float,
                    "int": int,
                    "str": str,
                    "round": round,
                    "sorted": sorted,
                    "list": list,
                    "dict": dict
                }
                
                # Data to operate on
                data = last_result['displayed_results']
                safe_locals = {"data": data}
                
                # Execute AI-generated code
                result = eval(operation_plan['python_code'], safe_globals, safe_locals)
                
                # Format response based on operation type
                return self._format_ai_operation_result(
                    result, 
                    operation_plan, 
                    last_result
                )
            else:
                return {
                    'type': 'error',
                    'message': "I couldn't determine how to process that request. Could you be more specific?"
                }
            
        except Exception as e:
            print(f"AI operation execution failed: {e}")
            return {
                'type': 'error',
                'message': "I couldn't process that request with the previous results. Could you try rephrasing?"
            }
    
    def _format_ai_operation_result(self, result, operation_plan: Dict, last_result: Dict) -> Dict:
        """Format the AI operation result for user display"""
        operation_type = operation_plan.get('operation_type', 'unknown')
        user_intent = operation_plan.get('user_intent', 'perform operation')
        
        if operation_type == 'count':
            return {
                'type': 'count_response',
                'count': result,
                'message': f"There are {result} results.",
                'metadata': {
                    'is_follow_up': True,
                    'operation': 'count',
                    'original_query': last_result['original_query']
                }
            }
        
        elif operation_type == 'filter':
            filtered_count = len(result) if isinstance(result, list) else 0
            return {
                'type': 'filtered_results',
                'data': result,
                'message': f"Showing {filtered_count} results from your previous query.",
                'metadata': {
                    'is_follow_up': True,
                    'operation': 'filter',
                    'filter_applied': user_intent,
                    'original_count': last_result['displayed_count'],
                    'filtered_count': filtered_count
                }
            }
        
        elif operation_type == 'aggregate':
            return {
                'type': 'aggregate_result',
                'value': result,
                'message': f"Calculation result: {result}",
                'metadata': {
                    'is_follow_up': True,
                    'operation': 'aggregate',
                    'calculation': user_intent
                }
            }
        
        else:
            # Generic result handling
            return {
                'type': 'ai_operation_result',
                'data': result,
                'message': f"Result of {user_intent}: {result}",
                'metadata': {
                    'is_follow_up': True,
                    'operation': operation_type
                }
            }

# Global conversation chain instance
conversation_chain = ConversationalResultChain()

def detect_referential_query_ai(current_query: str, conversation_history: List[str]) -> Dict:
    """Enhanced AI detection with better context understanding and improved fallback"""
    
    try:
        from src.core.query_agent import gemini_direct_answer as call_llm
        
        prompt = f"""
Analyze if this query refers to previous conversation results.

CONVERSATION HISTORY:
{chr(10).join(conversation_history[-3:]) if conversation_history else "No previous queries"}

CURRENT QUERY: "{current_query}"

Key patterns that indicate referential queries:
1. Direct references: "these", "those", "them", "the above", "from those"
2. Contextual continuations: "more details about X", "show info for Y", "expand on Z"
3. Subset operations: "which ones are X", "filter by Y", "only show Z"
4. Entity continuation: If previous results contained specific entities, and current query asks about those same entities

IMPORTANT: If the current query asks for "more details" or "more info" about something that was mentioned in previous results, it should be considered referential.

Examples:
- Previous: "show 3 vehicles" → Current: "more details about the Toyota" → REFERENTIAL (if Toyota was in the 3)
- Previous: "show complaints under 10k" → Current: "more detail about leakage issue complaint" → REFERENTIAL (if leakage was in those complaints)
- Previous: "show plants" → Current: "show vehicles" → NOT REFERENTIAL (different topic)

Respond in JSON:
{{
    "is_referential": boolean,
    "confidence": 0.0-1.0,
    "reference_type": "direct|demonstrative|contextual|entity_continuation",
    "reasoning": "brief explanation of decision",
    "target_entity": "what specific entity/item is being referenced"
}}
"""

        try:
            response = call_llm(prompt)
            result = json.loads(response)
            return result
        except Exception as llm_error:
            print(f"⚠️ LLM call failed: {llm_error}")
            # Fall through to enhanced fallback
            
    except ImportError:
        print("⚠️ LLM not available, using enhanced fallback detection")
    
    # Enhanced fallback with smart pattern detection
    current_lower = current_query.lower()
    
    # Advanced referential patterns
    referential_patterns = [
        "these", "those", "them", "the above", "from those", "of these",
        "which ones", "which of", "from the", "in those", "that data",
        "more detail", "more info", "expand on", "show details",
        "give details", "tell me about", "explain the"
    ]
    
    # Entity-specific patterns
    detail_patterns = ["more detail", "more info", "tell me about", "explain", "show details"]
    entity_indicators = ["complaint", "issue", "leakage", "vehicle", "report", "record"]
    
    # Check for basic referential patterns
    has_referential_pattern = any(pattern in current_lower for pattern in referential_patterns)
    
    # Enhanced detection for entity-specific requests
    has_detail_request = any(pattern in current_lower for pattern in detail_patterns)
    mentions_entity = any(entity in current_lower for entity in entity_indicators)
    
    # Context-aware detection
    has_conversation_context = len(conversation_history) > 0
    
    # Extract target entity if asking for details
    target_entity = None
    if has_detail_request and mentions_entity:
        # Try to extract the entity being asked about
        import re
        entity_patterns = [
            r'(?:detail|info).*?about\s+(?:the\s+)?([a-zA-Z\s]+?)(?:\s+complaint|\s+issue|$)',
            r'(?:tell me about|explain)\s+(?:the\s+)?([a-zA-Z\s]+?)(?:\s+complaint|\s+issue|$)',
            r'more.*?([a-zA-Z]+\s+issue)',
            r'details.*?([a-zA-Z]+\s+complaint)'
        ]
        for pattern in entity_patterns:
            entity_match = re.search(pattern, current_lower)
            if entity_match:
                target_entity = entity_match.group(1).strip()
                break
    
    # Determine if this is referential
    is_referential = False
    confidence = 0.0
    reference_type = "none"
    
    if has_referential_pattern:
        is_referential = True
        confidence = 0.8
        reference_type = "demonstrative"
    elif has_detail_request and mentions_entity and has_conversation_context:
        is_referential = True
        confidence = 0.9
        reference_type = "entity_continuation"
    elif has_conversation_context and any(term in current_lower for term in ["detail", "info", "about", "explain"]):
        is_referential = True
        confidence = 0.7
        reference_type = "contextual"
    
    return {
        "is_referential": is_referential,
        "confidence": confidence,
        "reference_type": reference_type,
        "target_entity": target_entity,
        "reasoning": f"Enhanced fallback detection: patterns={has_referential_pattern}, detail_request={has_detail_request}, entity={mentions_entity}"
    }

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
            with db_manager.get_connection_context() as conn:
                cur = conn.cursor()
                cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
                conn.commit()
            self.use_pgvector = True
            print("✅ pgvector extension enabled - using native vector operations")
        except psycopg2.Error as e:
            print(f"⚠️ pgvector extension not available: {e}")
            print("🔄 Using fallback mode with JSON storage and scikit-learn similarity")
            self.use_pgvector = False
            try:
                if 'conn' in locals():
                    conn.rollback()
            except:
                pass
        
        # Now create tables in a fresh transaction
        try:
            with db_manager.get_connection_context() as conn:
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
                
                # 🧠 CONVERSATIONAL AI: Create conversation context table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS conversation_context (
                        session_id VARCHAR(255) PRIMARY KEY,
                        current_topic TEXT,
                        last_vehicle VARCHAR(255),
                        last_date_context TEXT,
                        last_report_type VARCHAR(255),
                        conversation_summary TEXT,
                        active_filters JSONB DEFAULT '{}',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                
                # 🧠 CONVERSATIONAL AI: Create conversation history table  
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS conversation_history (
                        id SERIAL PRIMARY KEY,
                        session_id VARCHAR(255) NOT NULL,
                        user_message TEXT NOT NULL,
                        bot_response TEXT NOT NULL,
                        extracted_entities JSONB DEFAULT '{}',
                        intent_detected VARCHAR(255),
                        sql_executed TEXT,
                        result_count INTEGER DEFAULT 0,
                        conversation_turn INTEGER DEFAULT 1,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
            
            # 🧠 CONVERSATIONAL AI: Create indexes for conversation tables
            cur.execute("CREATE INDEX IF NOT EXISTS conversation_history_session_idx ON conversation_history (session_id, timestamp);")
            cur.execute("CREATE INDEX IF NOT EXISTS conversation_context_updated_idx ON conversation_context (updated_at);")
            
            # Add foreign key constraint after both tables exist
            try:
                cur.execute("""
                    ALTER TABLE conversation_history 
                    ADD CONSTRAINT fk_conversation_history_session 
                    FOREIGN KEY (session_id) 
                    REFERENCES conversation_context(session_id) 
                    ON DELETE CASCADE;
                """)
            except psycopg2.Error as e:
                # Constraint might already exist, ignore the error
                if "already exists" not in str(e).lower():
                    print(f"⚠️ Could not add foreign key constraint: {e}")
            
            conn.commit()
            print("✅ Database tables created successfully (including conversational AI tables)")
            
        except Exception as e:
            print(f"❌ Error setting up database: {e}")
            # Don't raise the exception - allow the system to continue with limited functionality
            print("⚠️ Continuing with limited database functionality for conversational AI")
            return
    
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
        with db_manager.get_connection_context() as conn:
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
            with db_manager.get_connection_context() as conn:
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
                    
                    # Return in the same format as the old system
                    return [(table_key, similarity, description) for table_key, description, similarity in results]
                else:
                    # Fallback: manual cosine similarity calculation
                    cur.execute("SELECT table_key, description, embedding_json FROM schema_embeddings;")
                    results = cur.fetchall()
                    
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
            with db_manager.get_connection_context() as conn:
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
            
        except Exception as e:
            print(f"❌ Error storing query pattern: {e}")
    
    def find_similar_query(self, user_query, threshold=0.8):
        """Find similar previous queries using vector similarity."""
        query_embedding = self.get_embedding(user_query)
        if not query_embedding:
            return None
        
        try:
            with db_manager.get_connection_context() as conn:
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
            with db_manager.get_connection_context() as conn:
                cur = conn.cursor()
                
                cur.execute("SELECT COUNT(*) FROM schema_embeddings;")
                schema_count = cur.fetchone()[0]
                
                cur.execute("SELECT COUNT(*) FROM query_patterns WHERE success = TRUE;")
                pattern_count = cur.fetchone()[0]
                
                cur.execute("SELECT COUNT(*) FROM conversation_context;")
                active_sessions = cur.fetchone()[0]
                
                return {
                    'schema_embeddings': schema_count,
                    'query_patterns': pattern_count,
                    'active_conversations': active_sessions,
                    'embedding_dimension': self.embedding_dim,
                    'pgvector_enabled': self.use_pgvector,
                    'model_info': str(self.model)
                }
            
        except Exception as e:
            print(f"❌ Error getting embedding stats: {e}")
            return {}
    
    # 🧠 CONVERSATIONAL AI METHODS
    def get_or_create_conversation_session(self, session_id: str = None) -> dict:
        """Get or create a conversation session with AI-understandable context."""
        if session_id is None:
            session_id = str(uuid.uuid4())
        
        # TEMPORARY: Return minimal session without database operations
        # TODO: Re-enable once connection pool is stabilized
        return {
            'session_id': session_id,
            'current_topic': None,
            'last_vehicle': None,
            'last_date_context': None,
            'last_report_type': None,
            'conversation_summary': None,
            'active_filters': {},
            'recent_history': [],
            'history_count': 0,
            'created_at': datetime.now()
        }
    
    def extract_conversational_entities(self, user_message: str, context: dict = None) -> dict:
        """AI-powered entity extraction from user message with conversation context."""
        entities = {}
        user_msg_lower = user_message.lower()
        
        # Extract vehicle information with context awareness
        vehicle_patterns = [
            r'\b([A-Z]{2}\d{2}[A-Z]\d{4})\b',  # WB38C2023 pattern
            r'\bvehicle\s+([A-Z0-9]+)\b',
            r'\bbus\s+([A-Z0-9]+)\b',
            r'\breg(?:istration)?\s*(?:no|number)?\s*([A-Z0-9]+)\b'
        ]
        
        for pattern in vehicle_patterns:
            match = re.search(pattern, user_message, re.IGNORECASE)
            if match:
                entities['vehicle'] = match.group(1).upper()
                break
        
        # Handle conversational references
        if any(phrase in user_msg_lower for phrase in ['that vehicle', 'same vehicle', 'this vehicle']):
            if context and context.get('last_vehicle'):
                entities['vehicle'] = context['last_vehicle']
                entities['is_reference'] = True
        
        # Extract date information with natural language understanding
        date_patterns = [
            (r'\b(\d{1,2})\s+(?:july|jul)\s+(\d{4})\b', 'specific_date'),
            (r'\b(\d{4})-(\d{1,2})-(\d{1,2})\b', 'iso_date'),
            (r'\byesterday\b', 'yesterday'),
            (r'\btoday\b', 'today'),
            (r'\blast\s+week\b', 'last_week'),
            (r'\bthis\s+month\b', 'this_month'),
            (r'\blast\s+month\b', 'last_month')
        ]
        
        for pattern, date_type in date_patterns:
            match = re.search(pattern, user_msg_lower)
            if match:
                if date_type == 'specific_date':
                    entities['date'] = {
                        'type': 'specific',
                        'day': match.group(1),
                        'month': 'july',
                        'year': match.group(2)
                    }
                elif date_type == 'iso_date':
                    entities['date'] = {
                        'type': 'iso',
                        'year': match.group(1),
                        'month': match.group(2),
                        'day': match.group(3)
                    }
                else:
                    entities['date'] = {'type': date_type}
                break
        
        # Handle conversational date references
        if any(phrase in user_msg_lower for phrase in ['same date', 'that date', 'same period']):
            if context and context.get('last_date_context'):
                entities['date'] = {'type': 'reference', 'refers_to': context['last_date_context']}
        
        # Extract report type with AI understanding
        report_keywords = {
            'stoppage': ['stoppage', 'stop', 'halt', 'break', 'pause'],
            'distance': ['distance', 'travel', 'trip', 'journey', 'mileage', 'km', 'kilometer'],
            'fuel': ['fuel', 'consumption', 'efficiency', 'mileage', 'gas', 'diesel'],
            'speed': ['speed', 'velocity', 'overspeeding', 'fast', 'slow'],
            'route': ['route', 'path', 'direction', 'way'],
            'maintenance': ['maintenance', 'repair', 'service', 'fix']
        }
        
        for report_type, keywords in report_keywords.items():
            if any(keyword in user_msg_lower for keyword in keywords):
                entities['report_type'] = report_type
                break
        
        # Extract time-based filters
        if 'more than' in user_msg_lower or 'greater than' in user_msg_lower:
            time_match = re.search(r'more than (\d+)\s*(hour|minute)', user_msg_lower)
            if time_match:
                entities['time_filter'] = {
                    'operator': 'greater_than',
                    'value': int(time_match.group(1)),
                    'unit': time_match.group(2)
                }
        
        # Detect follow-up intent
        follow_up_indicators = [
            'what about', 'also show', 'and', 'same for', 'more details', 
            'additional', 'further', 'expand', 'also', 'too'
        ]
        
        if any(indicator in user_msg_lower for indicator in follow_up_indicators):
            entities['is_followup'] = True
        
        return entities
    
    def update_conversation_context(self, session_id: str, user_message: str, 
                                  entities_or_bot_response, entities: dict = None, 
                                  sql_query: str = None, result_count: int = 0):
        """Update conversation context with AI-powered understanding."""
        
        # Handle both old and new calling patterns
        if entities is None:
            # New simple calling pattern: (session_id, user_message, entities)
            entities = entities_or_bot_response
            bot_response = "Response generated"  # Default response
        else:
            # Old calling pattern: (session_id, user_message, bot_response, entities, ...)
            bot_response = entities_or_bot_response
        
        # TEMPORARY: Disable database operations to prevent connection pool exhaustion
        # TODO: Re-enable once connection pool is stabilized
        print(f"⚠️ Conversation context update skipped for performance (session: {session_id})")
        return
    
    def _generate_conversation_summary(self, user_message: str, bot_response: str, entities: dict) -> str:
        """Generate AI-friendly conversation summary."""
        summary_parts = []
        
        if entities.get('vehicle'):
            summary_parts.append(f"discussing vehicle {entities['vehicle']}")
        
        if entities.get('report_type'):
            summary_parts.append(f"analyzing {entities['report_type']} data")
        
        if entities.get('date'):
            if entities['date'].get('type') == 'specific':
                summary_parts.append(f"for {entities['date'].get('day')} {entities['date'].get('month')} {entities['date'].get('year')}")
            else:
                summary_parts.append(f"for {entities['date'].get('type')} timeframe")
        
        if entities.get('time_filter'):
            filter_info = entities['time_filter']
            summary_parts.append(f"filtered by {filter_info['operator']} {filter_info['value']} {filter_info['unit']}s")
        
        return "; ".join(summary_parts) if summary_parts else "general vehicle inquiry"
    
    def generate_conversational_context_prompt(self, session_id: str, current_query: str) -> str:
        """Generate AI-friendly context prompt for enhanced understanding."""
        context = self.get_or_create_conversation_session(session_id)
        
        prompt_parts = ["\n🧠 CONVERSATION CONTEXT FOR AI UNDERSTANDING:\n"]
        
        # Current session context
        if context.get('current_topic'):
            prompt_parts.append(f"• Current conversation topic: {context['current_topic']}")
        
        if context.get('last_vehicle'):
            prompt_parts.append(f"• Vehicle in focus: {context['last_vehicle']}")
        
        if context.get('last_date_context'):
            prompt_parts.append(f"• Time context: {context['last_date_context']}")
        
        if context.get('last_report_type'):
            prompt_parts.append(f"• Report type in discussion: {context['last_report_type']}")
        
        if context.get('conversation_summary'):
            prompt_parts.append(f"• Conversation summary: {context['conversation_summary']}")
        
        # Recent conversation flow
        if context.get('recent_history'):
            prompt_parts.append("\n📝 RECENT CONVERSATION FLOW:")
            for i, turn in enumerate(context['recent_history'][:3]):  # Last 3 turns
                prompt_parts.append(f"Turn {i+1}:")
                prompt_parts.append(f"  User: {turn['user_message']}")
                prompt_parts.append(f"  Bot: {turn['bot_response'][:100]}...")
                if turn.get('entities'):
                    prompt_parts.append(f"  Entities: {json.dumps(turn['entities'])}")
        
        # AI understanding guidelines
        prompt_parts.extend([
            "\n💡 AI CONVERSATION RULES:",
            "• When user says 'that vehicle' → use last_vehicle from context",
            "• When user says 'same date/period' → use last_date_context",
            "• When user says 'also show/what about' → it's a follow-up question",
            "• When user asks 'more details' → expand previous query with additional columns",
            "• When user references 'that data/those results' → refer to last report_type",
            "• Always acknowledge conversation context in responses",
            "• Be natural and conversational, not robotic"
        ])
        
        current_query_analysis = self.extract_conversational_entities(current_query, context)
        if current_query_analysis:
            prompt_parts.append(f"\n🔍 CURRENT QUERY ANALYSIS: {json.dumps(current_query_analysis)}")
        
        return "\n".join(prompt_parts)

# Global instance - auto-initialize on import
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

# Auto-initialize when module is imported
try:
    if sentence_embedding_manager is None:
        sentence_embedding_manager = initialize_sentence_embeddings()
except Exception as e:
    print(f"⚠️ Could not auto-initialize sentence embedding manager: {e}")
    print("📝 Note: Sentence embedding manager will need to be initialized manually")

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
