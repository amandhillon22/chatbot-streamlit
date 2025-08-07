import google.generativeai as genai
import os
import json
import re
import sys
sys.path.append('/home/linux/Documents/chatbot-diya')

from dotenv import load_dotenv
import datetime
from decimal import Decimal
from src.core.sql import get_full_schema, get_column_types, get_numeric_columns, DecimalEncoder

# Enhanced JSON encoder to handle datetime and decimal objects
class SafeJSONEncoder(DecimalEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.date, datetime.time, datetime.timedelta)):
            return obj.isoformat()
        return super().default(obj)

def safe_json_dumps(obj, **kwargs):
    """Safely serialize objects to JSON, handling datetime and Decimal objects"""
    return json.dumps(obj, cls=SafeJSONEncoder, **kwargs)

# Import embeddings functionality
try:
    from src.nlp.create_lightweight_embeddings import LightweightEmbeddingManager
    from src.nlp.enhanced_table_mapper import EnhancedTableMapper
    from src.nlp.sentence_embeddings import sentence_embedding_manager, initialize_sentence_embeddings
    EMBEDDINGS_AVAILABLE = True
    CONVERSATIONAL_AI_AVAILABLE = True
except ImportError:
    EMBEDDINGS_AVAILABLE = False
    CONVERSATIONAL_AI_AVAILABLE = False

# Import distance unit conversion functionality
try:
    from src.database.distance_units import get_distance_conversion_info, get_distance_columns_info
    DISTANCE_CONVERSION_AVAILABLE = True
    print("✅ Distance unit conversion system loaded successfully")
except ImportError as e:
    print(f"⚠️ Distance unit conversion not available: {e}")
    DISTANCE_CONVERSION_AVAILABLE = False

# Import location converter for coordinate conversion
try:
    from src.utils.location_converter import convert_location_string_to_readable
    LOCATION_CONVERSION_AVAILABLE = True
    print("✅ Location conversion system loaded successfully")
except ImportError as e:
    print(f"⚠️ Location conversion not available: {e}")
    LOCATION_CONVERSION_AVAILABLE = False

def initialize_embeddings():
    """Initialize the lightweight embedding manager"""
    try:
        # Use absolute path for embeddings cache
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        embeddings_cache_path = os.path.join(project_root, 'embeddings_cache.pkl')
        
        if os.path.exists(embeddings_cache_path):
            import pickle
            with open(embeddings_cache_path, 'rb') as f:
                data = pickle.load(f)
            manager = LightweightEmbeddingManager()
            manager.schema_embeddings = data.get('schema_embeddings', {})
            manager.table_descriptions = data.get('table_descriptions', {})
            manager.query_patterns = data.get('query_patterns', {})
            manager.fitted_vectorizer = data.get('vectorizer', None)
            print(f"📂 Loaded embeddings for {len(manager.schema_embeddings)} tables")
            return manager
        else:
            print("⚠️ No embeddings cache found")
            return None
    except Exception as e:
        print(f"⚠️ Error loading embeddings: {e}")
        return None

# Initialize enhanced table mapper for embeddings
if EMBEDDINGS_AVAILABLE:
    try:
        enhanced_table_mapper = EnhancedTableMapper()
        print("✅ Enhanced table mapper initialized")
    except Exception as e:
        print(f"⚠️ Enhanced table mapper not available: {e}")
        enhanced_table_mapper = None
        EMBEDDINGS_AVAILABLE = False
else:
    enhanced_table_mapper = None

# Import intelligent reasoning
try:
    from src.core.intelligent_reasoning import IntelligentReasoning
    intelligent_reasoning = IntelligentReasoning()
    print("✅ Intelligent reasoning initialized")
except ImportError as e:
    print(f"⚠️ Intelligent reasoning not available: {e}")
    intelligent_reasoning = None

# Import enhanced pronoun resolver
try:
    from src.nlp.enhanced_pronoun_resolver import EnhancedPronounResolver
    pronoun_resolver = EnhancedPronounResolver()
    print("✅ Enhanced pronoun resolver initialized")
except ImportError as e:
    print(f"⚠️ Enhanced pronoun resolver not available: {e}")
    pronoun_resolver = None

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

def schema_dict_to_prompt(schema_dict):
    """
    Converts the schema dictionary to a readable string for LLM prompt.
    Now includes explicit column validation instructions and data type warnings.
    """
    lines = []
    
    # Get column types for validation hints
    try:
        column_types = get_column_types()
    except:
        column_types = {}
    
    for schema_name, tables in schema_dict.items():
        lines.append(f"Schema: {schema_name}")
        for table, columns in tables.items():
            lines.append(f"- {schema_name}.{table}")
            
            # Add column information with type hints where available
            column_details = []
            for col in columns:
                col_path = f"{schema_name}.{table}.{col}"
                col_type = column_types.get(col_path, "unknown")
                
                # Add type warnings for common mistakes
                if col_type in ['character varying', 'text', 'character']:
                    column_details.append(f"{col} (TEXT - use COUNT/MAX/MIN only, NOT SUM/AVG)")
                elif col_type in ['integer', 'bigint', 'smallint', 'decimal', 'numeric', 'real', 'double precision', 'money']:
                    column_details.append(f"{col} (NUMERIC - can use SUM/AVG/COUNT/MAX/MIN)")
                else:
                    column_details.append(col)
            
            lines.append(f"  Columns: {', '.join(column_details)}")
            lines.append(f"  ⚠️  ONLY these {len(columns)} columns exist - do not reference any others!")
            lines.append(f"  ⚠️  Use SUM/AVG ONLY on NUMERIC columns, never on TEXT columns!")
    return '\n'.join(lines)

# Dynamically fetch schema at import time
SCHEMA_DICT = get_full_schema()
SCHEMA_PROMPT = schema_dict_to_prompt(SCHEMA_DICT)

# Initialize embeddings if available
if EMBEDDINGS_AVAILABLE:
    try:
        embedding_manager = initialize_embeddings()
        if embedding_manager:
            print("🚀 Embeddings system initialized")
        else:
            print("⚠️ Running without embeddings (faster startup)")
            EMBEDDINGS_AVAILABLE = False
    except Exception as e:
        print(f"⚠️ Failed to initialize embeddings: {e}")
        EMBEDDINGS_AVAILABLE = False

def extract_json(response):
    try:
        match = re.search(r"{[\s\S]+}", response)
        if match:
            result = json.loads(match.group())
            # Validate and fix common table name errors
            result = validate_and_fix_sql(result)
            return result
        return {}
    except json.JSONDecodeError:
        return {}

def validate_and_fix_sql(result):
    """Validate and fix common SQL errors before execution"""
    if result and 'sql' in result and result['sql']:
        sql = result['sql']
        
        # Critical fix: Replace stoppage_report with util_report
        if 'stoppage_report' in sql.lower():
            print("🚨 CRITICAL FIX: Replacing 'stoppage_report' with 'util_report' in SQL")
            sql = re.sub(r'\bstoppage_report\b', 'util_report', sql, flags=re.IGNORECASE)
            result['sql'] = sql
            
            # Add debug warning
            if 'response' in result:
                result['response'] += " [Fixed: Used util_report table for stoppage data]"
        
        # Additional validation could be added here
        
    return result

def english_to_sql(prompt, chat_context=None, session_id=None):
    """
    🧠 CONVERSATIONAL AI-FIRST APPROACH: Enhanced with conversation memory and context understanding
    """
    
    # 🚀 AI-FIRST: Check if this is a referential query to previous results
    from src.nlp.sentence_embeddings import conversation_chain, detect_referential_query_ai
    
    # Build conversation history for AI analysis
    conversation_history = []
    if session_id and CONVERSATIONAL_AI_AVAILABLE and sentence_embedding_manager:
        try:
            history = sentence_embedding_manager.get_conversation_history(session_id, limit=3)
            conversation_history = [h['user_message'] for h in history if h.get('user_message')]
        except:
            pass
    
    # Use AI to detect referential intent (NO rigid patterns)
    referential_analysis = detect_referential_query_ai(prompt, conversation_history)
    
    if referential_analysis.get('is_referential', False) and referential_analysis.get('confidence', 0) > 0.7:
        print(f"🧠 [AI-REFERENTIAL] Detected follow-up query with confidence {referential_analysis.get('confidence', 0):.2f}")
        print(f"🧠 [AI-REFERENTIAL] Reference type: {referential_analysis.get('reference_type', 'unknown')}")
        
        # This is a follow-up query referring to previous results
        ai_result = conversation_chain.apply_ai_operation_to_last_result(
            prompt, 
            conversation_history
        )
        
        if ai_result:
            print(f"✅ [AI-REFERENTIAL] Successfully processed follow-up query")
            
            # Store this follow-up interaction
            if CONVERSATIONAL_AI_AVAILABLE and sentence_embedding_manager and session_id:
                try:
                    sentence_embedding_manager.update_conversation_context_simple(
                        session_id, prompt, safe_json_dumps(ai_result)
                    )
                except Exception as e:
                    print(f"⚠️ Failed to store follow-up interaction: {e}")
            
            # Format AI result to match expected response structure
            formatted_result = {
                "sql": None,  # No SQL needed for referential queries
                "response": ai_result.get('message', 'Processed successfully'),
                "data": ai_result.get('data', []),
                "follow_up": None,
                "conversational_context": f"Processed {ai_result.get('metadata', {}).get('operation', 'operation')} on previous results",
                "entities": {"is_referential": True, "operation_type": ai_result.get('metadata', {}).get('operation')},
                "metadata": ai_result.get('metadata', {}),
                "type": ai_result.get('type', 'ai_referential_response')
            }
            
            # Handle different AI operation types
            if ai_result.get('type') == 'count_response':
                formatted_result["response"] = f"There are {ai_result.get('count', 0)} results."
                formatted_result["data"] = [{"count": ai_result.get('count', 0)}]
            elif ai_result.get('type') == 'filtered_results':
                formatted_result["data"] = ai_result.get('data', [])
                formatted_result["response"] = ai_result.get('message', f"Showing {len(ai_result.get('data', []))} filtered results.")
            elif ai_result.get('type') == 'aggregate_result':
                formatted_result["response"] = ai_result.get('message', f"Calculation result: {ai_result.get('value', 'N/A')}")
                formatted_result["data"] = [{"result": ai_result.get('value', 'N/A')}]
            
            return formatted_result
    
    # 🧠 CONVERSATIONAL AI: Initialize conversation context
    conversation_context = ""
    entities_extracted = {}
    is_followup = False
    
    if CONVERSATIONAL_AI_AVAILABLE and sentence_embedding_manager and session_id:
        try:
            # Get conversational context
            conversation_context = sentence_embedding_manager.generate_conversational_context_prompt(session_id, prompt)
            entities_extracted = sentence_embedding_manager.extract_conversational_entities(prompt, 
                sentence_embedding_manager.get_or_create_conversation_session(session_id))
            is_followup = entities_extracted.get('is_followup', False)
            
            print(f"🧠 [CONVERSATIONAL] Session: {session_id}")
            print(f"🧠 [CONVERSATIONAL] Entities extracted: {entities_extracted}")
            print(f"🧠 [CONVERSATIONAL] Is follow-up: {is_followup}")
            
        except Exception as e:
            print(f"⚠️ [CONVERSATIONAL] Error in conversational analysis: {e}")
    
    # 🔄 FORMAT/DISPLAY REQUESTS - Handle immediately 
    if re.search(r'\b(format|clean|style|tabular|bullets|rewrite|shorter|rephrase|reword|simplify|again|visual|text-based|in text|as table|re-display)\b', prompt, re.IGNORECASE):
        last_data = chat_context.last_result if chat_context else None
        if not last_data:
            return {
                "sql": None,
                "response": "I don't have any recent data to reformat. Please ask me a question first.",
                "follow_up": None,
                "conversational_context": conversation_context,
                "entities": entities_extracted
            }
        
        try:
            # Get the last SQL query and result for reformatting
            result = handle_formatting_request(prompt, chat_context)
            result["conversational_context"] = conversation_context
            result["entities"] = entities_extracted
            return result
        except Exception as e:
            return {
                "sql": None,
                "response": f"Error formatting data: {str(e)}",
                "follow_up": None,
                "conversational_context": conversation_context,
                "entities": entities_extracted
            }
    
    # 🎯 CONVERSATIONAL AI-FIRST INTENT ANALYSIS
    # Let the LLM understand what the user wants with full conversation context
    try:
        print(f"🧠 [AI-FIRST] Analyzing user intent with conversational context: '{prompt}'")
        
        # Build enhanced context for LLM with conversation awareness
        context_info = conversation_context if conversation_context else ""
        enhanced_prompt = prompt
        
        # 🧠 CONVERSATIONAL ENHANCEMENT: Modify prompt based on entities and context
        if is_followup and entities_extracted:
            # Handle follow-up queries by inheriting context
            inherited_context = []
            
            if entities_extracted.get('vehicle'):
                inherited_context.append(f"Vehicle: {entities_extracted['vehicle']}")
            elif entities_extracted.get('is_reference', False):
                inherited_context.append("Vehicle: (reference to previous vehicle)")
            
            if entities_extracted.get('date'):
                if entities_extracted['date'].get('type') == 'reference':
                    inherited_context.append("Date: (reference to previous date)")
                else:
                    inherited_context.append(f"Date: {json.dumps(entities_extracted['date'])}")
            
            if entities_extracted.get('report_type'):
                inherited_context.append(f"Report type: {entities_extracted['report_type']}")
            
            if inherited_context:
                enhanced_prompt = f"{prompt} [CONTEXT: {'; '.join(inherited_context)}]"
                print(f"🧠 [CONVERSATIONAL] Enhanced prompt: {enhanced_prompt}")
        
        if chat_context:
            context_info = chat_context.get_context_for_llm(prompt)
            
            # Handle ordinal references like "1st", "2nd", etc.
            ordinal_match = re.search(r'\b(\d+)(?:st|nd|rd|th)\b', prompt, re.IGNORECASE)
            if ordinal_match and chat_context.last_displayed_items:
                ordinal_num = int(ordinal_match.group(1))
                if 1 <= ordinal_num <= len(chat_context.last_displayed_items):
                    target_item = chat_context.last_displayed_items[ordinal_num - 1]
                    entity = "item"
                    
                    # Find primary identifier
                    primary_id = None
                    for key in ['registration_number', 'reg_no', 'vehicle_id', 'id', 'name']:
                        if key in target_item:
                            primary_id = target_item[key]
                            break
                    
                    if primary_id:
                        enhanced_prompt = f"{prompt} (specifically for {entity} with identifier: {primary_id})"
                        print(f"🎯 Enhanced prompt with ordinal reference: {enhanced_prompt}")
        
        # Get the actual LLM analysis
        llm_result = generate_sql_with_llm(enhanced_prompt, context_info, chat_context)
        
        # ✅ If LLM successfully understands and generates SQL, use it
        if llm_result and llm_result.get('sql'):
            print(f"✅ [AI-FIRST] LLM successfully generated SQL")
            
            # 🚀 STORE RESULTS IN CONVERSATION CHAIN for follow-up queries
            try:
                if llm_result.get('data') and isinstance(llm_result['data'], list):
                    conversation_chain.push_result(
                        query=prompt,
                        sql=llm_result.get('sql', ''),
                        results=llm_result['data'],
                        display_results=llm_result['data'][:50] if len(llm_result['data']) > 50 else llm_result['data']
                    )
                    print(f"📊 [CONVERSATION-CHAIN] Stored {len(llm_result['data'])} results for follow-up queries")
            except Exception as e:
                print(f"⚠️ Failed to store results in conversation chain: {e}")
            
            # Update conversational context for successful queries
            if session_id and sentence_embedding_manager:
                entities = sentence_embedding_manager.extract_conversational_entities(prompt)
                sentence_embedding_manager.update_conversation_context(session_id, prompt, entities)
            
            return llm_result
        
        print(f"⚠️ [AI-FIRST] LLM failed to generate SQL, trying intelligent reasoning fallback")
        
    except Exception as e:
        print(f"❌ [AI-FIRST] LLM analysis failed: {e}")
    
    # 🏗️ DPR (Daily Production Report) Query Detection
    if intelligent_reasoning and intelligent_reasoning.is_dpr_related_query(prompt):
        print(f"🏗️ [DPR] Daily Production Report query detected")
        
        # Extract entities for DPR context
        entities = intelligent_reasoning.extract_entities(prompt, conversation_context)
        
        # Generate DPR-specific SQL
        dpr_sql = intelligent_reasoning.generate_dpr_sql(prompt, entities)
        
        if dpr_sql:
            print(f"🏗️ [DPR] Generated DPR-specific SQL")
            
            # Update conversational context for DPR queries
            if session_id and sentence_embedding_manager:
                sentence_embedding_manager.update_conversation_context(session_id, prompt, entities)
            
            return {
                "sql": dpr_sql,
                "response": "I'll get the daily production report information for you.",
                "follow_up": "Would you like to see more details about any specific delivery or customer?",
                "reasoning_applied": True,
                "reasoning_type": "DPR Query Processing",
                "entities": entities
            }
    
    # 🚛 Driver Management Query Detection
    if intelligent_reasoning and intelligent_reasoning.is_driver_related_query(prompt):
        print(f"🚛 [DRIVER] Driver management query detected")
        
        # Detect specific driver query type
        driver_query_type = intelligent_reasoning.detect_driver_query_type(prompt)
        
        if driver_query_type:
            print(f"🚛 [DRIVER] Query type: {driver_query_type}")
            
            # Extract entities for driver context
            entities = intelligent_reasoning.extract_entities(prompt, conversation_context)
            
            # Generate driver-specific SQL
            driver_sql = intelligent_reasoning.generate_driver_sql(driver_query_type, prompt, entities)
            
            if driver_sql:
                print(f"🚛 [DRIVER] Generated driver-specific SQL")
                
                # Create appropriate response based on query type
                response_map = {
                    'driver_lookup': "I'll find the driver information for you.",
                    'license_management': "I'll check the license status and renewal information.",
                    'plant_assignment': "I'll show you the driver assignments by plant.",
                    'contact_info': "I'll get the driver contact information.",
                    'demographics': "I'll analyze the driver demographic information.",
                    'service_duration': "I'll calculate the service duration for drivers.",
                    'uniform_management': "I'll show the uniform size distribution.",
                    'driver_codes': "I'll find drivers by their codes."
                }
                
                response = response_map.get(driver_query_type, "I'll get the driver information for you.")
                
                # Update conversational context for driver queries
                if session_id and sentence_embedding_manager:
                    sentence_embedding_manager.update_conversation_context(session_id, prompt, entities)
                
                return {
                    "sql": driver_sql,
                    "response": response,
                    "follow_up": "Would you like to see additional driver details or analyze specific aspects?",
                    "reasoning_applied": True,
                    "reasoning_type": f"Driver Query Processing - {driver_query_type}",
                    "entities": entities
                }
    
    # 🧠 INTELLIGENT CONTEXTUAL REASONING FALLBACK
    if intelligent_reasoning and chat_context:
        reasoning_result = intelligent_reasoning.analyze_query_intent(prompt, chat_context)
        if reasoning_result:
            print(f"🧠 Intelligent reasoning detected: {reasoning_result['intent']}")
            print(f"📊 Extracted data: {reasoning_result['extracted_data']}")
            
            # Generate intelligent SQL query
            intelligent_sql = intelligent_reasoning.generate_intelligent_query(reasoning_result)
            if intelligent_sql:
                print(f"🎯 Generated intelligent SQL: {intelligent_sql.strip()}")
                
                # Create intelligent response
                intelligent_response = intelligent_reasoning.create_intelligent_response(
                    reasoning_result, {'sql': intelligent_sql}
                )
                
                # Update conversational context for successful queries
                if session_id and sentence_embedding_manager:
                    entities = sentence_embedding_manager.extract_conversational_entities(prompt)
                    sentence_embedding_manager.update_conversation_context(session_id, prompt, entities)
                
                return {
                    "sql": intelligent_sql,
                    "response": intelligent_response,
                    "follow_up": None,
                    "reasoning_applied": True,
                    "reasoning_type": reasoning_result['reasoning_type']
                }
    
    # 🎯 ENHANCED PRONOUN RESOLUTION FALLBACK
    if pronoun_resolver and chat_context:
        pronoun_detection = pronoun_resolver.detect_pronoun_reference(prompt)
        
        if pronoun_detection['needs_context_resolution']:
            print(f"🎯 Pronoun reference detected: {pronoun_detection['pronoun_type']}")
            
            # Check if we should avoid asking for clarification
            should_avoid_clarification = pronoun_resolver.should_avoid_clarification(prompt, chat_context)
            
            if should_avoid_clarification:
                print("🚫 Avoiding clarification - resolving with context")
                
                # Resolve using context
                context_resolution = pronoun_resolver.resolve_context_reference(
                    prompt, chat_context, pronoun_detection
                )
                
                if context_resolution:
                    return {
                        "sql": context_resolution['sql'],
                        "response": f"Here are the {context_resolution['requested_field']} for the {context_resolution['entity_type']} from our previous results:",
                        "follow_up": f"Would you like to see any other information about these {context_resolution['entity_type']}?",
                        "context_resolution_applied": True,
                        "reasoning": context_resolution['reasoning']
                    }
                else:
                    print("❌ Context resolution failed, continuing with normal processing")
    
    # � CONVERSATIONAL CONTEXT UPDATES
    if session_id:
        # Extract and store conversational entities for future reference
        entities = sentence_embedding_manager.extract_conversational_entities(prompt)
        sentence_embedding_manager.update_conversation_context(session_id, prompt, entities)
    
    # �🚫 FINAL FALLBACK - Simple error handling
    return {
        "sql": None,
        "response": "I couldn't understand your request. Could you please rephrase it or be more specific about what information you're looking for?",
        "follow_up": "For example, you could ask about vehicle details, plant information, or specific reports."
    }


def generate_sql_with_llm(prompt, context_info, chat_context=None):
    """
    🚀 TWO-STAGE APPROACH: Generate simple SQL, then apply formatting in post-processing
    Stage 1: Simple, raw SQL generation (avoid complex formatting in SQL)
    Stage 2: Python-based post-processing for user-friendly display
    """
    
    # Check if this is a drum_trip_report query - use two-stage approach
    if 'drum_trip_report' in prompt.lower() or 'drum trip' in prompt.lower():
        print("🎯 Using TWO-STAGE approach for drum_trip_report query")
        return generate_simple_drum_trip_sql(prompt, context_info, chat_context)
    
    # For other queries, continue with existing approach but simplified
    enhanced_prompt = prompt
    
    if chat_context:
        # Check for ordinal references and enhance the prompt
        position, entity = chat_context.extract_ordinal_reference(prompt)
        if position and chat_context.last_displayed_items:
            target_item = chat_context.get_item_by_ordinal(position)
            if target_item:
                # Find the primary identifier
                primary_id = None
                for key in ['registration_number', 'reg_no', 'vehicle_id', 'id', 'name']:
                    if key in target_item:
                        primary_id = target_item[key]
                        break
                
                if primary_id:
                    # Enhance the prompt with specific identifier
                    enhanced_prompt = f"{prompt} (specifically for {entity} with identifier: {primary_id})"
                    print(f"🎯 Enhanced prompt with ordinal reference: {enhanced_prompt}")
        
        context_info = chat_context.get_context_for_llm(enhanced_prompt)
        
        # Build detailed history with focus on recent interactions
        history_parts = []
        recent_interactions = chat_context.history[-3:] if chat_context.history else []
        
        for interaction in recent_interactions:
            user_q = interaction.get('user', '')
            bot_response = interaction.get('response') or ''  # Handle None case
            bot_response = bot_response[:200] if bot_response else ''  # Safe truncation
            sql_q = interaction.get('sql_query', '')
            
            history_parts.append(f"User: {user_q}")
            if sql_q:
                history_parts.append(f"SQL: {sql_q}")
            history_parts.append(f"Bot: {bot_response}...")
            history_parts.append("---")
        
        history_text = "\n".join(history_parts) if history_parts else ""
    else:
        history_text = ""

    # 🏭 STRICT HIERARCHICAL PLANT GUIDANCE 
    if re.search(r'\b(plant|site|facility|factory|location|mohali|ludhiana|derabassi|punjab|gujarat|maharashtra)\b', prompt, re.IGNORECASE):
        plant_guidance = """
🏭 **PLANT QUERY GUIDANCE - CRITICAL CLARIFICATION:**

⚠️ **MOST IMPORTANT**: hosp_master table is **PLANT MASTER**, NOT medical facility master!
- Despite the name "hosp_master", this table contains **PLANT/FACILITY DATA**
- Contains: Plant names, plant locations, factory information, site details
- **NEVER** interpret as medical facilities or healthcare institutions

✅ **ALWAYS USE hosp_master for ALL plant/facility queries**
- Plant ID: hm.id_no
- Plant Name: hm.name (e.g., "PB-Mohali", "PB-Ludhiana", "PB-Derabassi")
- Plant Address: hm.address
- District Link: hm.id_dist (links to district_master.id_no)

🎯 **CRITICAL: FLEXIBLE NAME MATCHING FOR ALL PLANT QUERIES:**

⚠️ **NEVER USE EXACT EQUALITY (=) FOR NAME MATCHING** - Database values may have:
- Extra spaces ("Nagpur- Hingna" vs "Nagpur-Hingna")
- Different capitalization ("mohali" vs "Mohali")
- Special characters variations
- Leading/trailing spaces

✅ **ALWAYS USE FLEXIBLE MATCHING PATTERNS:**
- **ILIKE '%name%'** for case-insensitive partial matching
- **TRIM()** functions to handle spaces
- **Multiple ILIKE conditions** for better coverage

🎯 **PLANT QUERY EXAMPLES WITH FLEXIBLE MATCHING:**
- "Show all plants" → SELECT hm.name, hm.id_no FROM hosp_master hm WHERE hm.name IS NOT NULL
- "Plant name for ID 460" → SELECT hm.name, hm.address FROM hosp_master hm WHERE hm.id_no = 460
- "Plants in Punjab" → SELECT hm.name FROM hosp_master hm JOIN district_master dm ON hm.id_dist = dm.id_no WHERE dm.name ILIKE '%Punjab%'
- "Vehicles in Mohali plant" → SELECT vm.reg_no FROM vehicle_master vm JOIN hosp_master hm ON vm.id_hosp = hm.id_no WHERE hm.name ILIKE '%mohali%'
- "Vehicles in Nagpur-Hingna plant" → SELECT vm.reg_no FROM vehicle_master vm JOIN hosp_master hm ON vm.id_hosp = hm.id_no WHERE (hm.name ILIKE '%nagpur%' AND hm.name ILIKE '%hingna%')

🚛 **VEHICLES OF PLANT QUERIES - FLEXIBLE MATCHING RULES:**
- "Vehicles of Mohali plant" → SELECT vm.reg_no FROM vehicle_master vm JOIN hosp_master hm ON vm.id_hosp = hm.id_no WHERE hm.name ILIKE '%mohali%'
- "Show vehicles of [plant name]" → SELECT vm.reg_no, vm.bus_id FROM vehicle_master vm JOIN hosp_master hm ON vm.id_hosp = hm.id_no WHERE hm.name ILIKE '%[plant name]%'
- "Vehicles in Nagpur-Hingna" → SELECT vm.reg_no FROM vehicle_master vm JOIN hosp_master hm ON vm.id_hosp = hm.id_no WHERE (hm.name ILIKE '%nagpur%' AND hm.name ILIKE '%hingna%')
- "Count vehicles in specific plant" → SELECT COUNT(vm.reg_no) FROM vehicle_master vm JOIN hosp_master hm ON vm.id_hosp = hm.id_no WHERE hm.name ILIKE '%plant_name%'

⚠️ **CRITICAL FLEXIBLE MATCHING STRATEGIES:**

1. **For compound names** (like "Nagpur-Hingna"):
   - Split into parts: "Nagpur" and "Hingna"
   - Use: `WHERE (hm.name ILIKE '%nagpur%' AND hm.name ILIKE '%hingna%')`
   - This handles: "Nagpur-Hingna", "Nagpur- Hingna", "Nagpur - Hingna", etc.

2. **For simple names** (like "Mohali"):
   - Use: `WHERE hm.name ILIKE '%mohali%'`
   - This handles: "Mohali", "PB-Mohali", "Mohali Plant", etc.

3. **For location-based names** (like "PB-Ludhiana"):
   - Use: `WHERE hm.name ILIKE '%ludhiana%'` (focus on location part)
   - This handles various prefixes and suffixes

4. **For numerical plant IDs**:
   - Always prefer ID-based matching when available
   - Use: `WHERE hm.id_no = X` for exact matches

⚠️ **MANDATORY FLEXIBLE MATCHING RULES:**
1. **NEVER** use exact equality (=) for text-based plant name matching
2. **ALWAYS** use ILIKE '%pattern%' for case-insensitive partial matching
3. **For compound names**: Break into keywords and use multiple ILIKE conditions with AND
4. **Handle spaces**: Use TRIM() or multiple ILIKE patterns to catch space variations
5. **Prefer ID matching**: When plant ID is known, use id_no for exact matching

❌ **NEVER USE**: plant_schedule, plant_master, or any other table for plant data
❌ **NEVER ASSUME**: hosp_master contains medical data - it's PLANT data!
❌ **NEVER USE**: Exact equality (=) for plant name matching
"""
    else:
        plant_guidance = ""

    # Build the complete LLM prompt - simplified for AI-first approach
    distance_enforcement = ""
    if re.search(r'\b(distance.*report|distance|travel|drum.*rotation|kilometers?|km|metres?|meters?)\b', enhanced_prompt, re.IGNORECASE):
        distance_enforcement = """
🚨 **SIMPLE DISTANCE QUERY ENFORCEMENT:**

**AI-FIRST PRINCIPLE**: Generate simple raw data queries. Let Python handle ALL conversions.

**SIMPLE RULES:**
- SELECT raw columns only: `distance`, `drum_rotation`, `ps_kms`, `sp_kms`
- NO SQL formatting functions: NO ROUND(), NO CONCAT(), NO complex CASE statements
- NO unit conversions in SQL - Python will handle meter→km and drum→time conversions
- Use simple aliases: `distance AS raw_distance`, `drum_rotation AS raw_drum_rotation`

**LET PYTHON HANDLE:**
- Distance conversions (meters to kilometers)
- Drum rotation to time format (HH:MM)
- All formatting and display logic
"""

    full_prompt = f"""
{SCHEMA_PROMPT}

🔍 **SIMPLE DATA TYPE VERIFICATION:**
Reference the database schema documentation at `/home/linux/Documents/chatbot-diya/docs/features/database_reference.md` for column types.

**AI-FIRST PRINCIPLE**: Generate simple queries that fetch raw data. Let Python handle ALL formatting.

**SIMPLE COLUMN HANDLING:**
- Duration/Time Columns: SELECT raw values, Python will format
- Distance/Numeric Columns: SELECT raw values, Python will convert units
- Coordinate Columns: SELECT raw lat/lng values, Python will format locations
- Text Columns: SELECT raw text, Python will handle display

**CRITICAL**: NO ROUND(), NO CONCAT(), NO complex CASE statements in SQL.
Let the AI intelligently understand data types and generate appropriate simple comparisons.
- **NEVER SELECT**: `loading_cnt` (count data not needed)
- **NEVER SELECT**: `unloading_cnt` (count data not needed)
- **USE PROPER NAMING**: `drum_in_plant` → `loading_time` (this represents concrete loading time into drum)
- **COLUMN PRIORITY**: Focus on essential delivery cycle data - times, distances, locations, speeds

**ESSENTIAL DRUM_TRIP_REPORT COLUMNS TO INCLUDE:**
- `reg_no` → registration_number (vehicle identifier)
- `plant_out`, `site_in`, `site_out`, `plant_in` → formatted timestamps  
- `ps_duration`, `sp_duration`, `cycle_time` → formatted time periods
- `ps_kms`, `sp_kms`, `cycle_km` → formatted distances with units
- `ps_max_speed`, `ps_avg_speed`, `sp_max_speed`, `sp_avg_speed` → speeds with km/h
- `plant_lat`, `plant_lng`, `site_lat`, `site_lng` → location coordinates
- `unloading_duration`, `site_waiting` → formatted waiting times
- `drum_in_plant` → `loading_time` (concrete loading time)
- `tkt_no` → ticket_number (delivery ticket reference)
- **EXCLUDE**: unloading_time, depo_id, loading_cnt, unloading_cnt (not needed for business reporting)

**AI-FIRST SIMPLE FORMATTING:**
- Select raw columns only
- Let Python handle all conversions and formatting
- No complex SQL formatting functions
- AI should intelligently handle data type mismatches by choosing appropriate comparisons

{plant_guidance}

{distance_enforcement}

{context_info}
```

**2. MANDATORY coordinate formatting with empty string validation:**
```sql
-- ❌ NEVER concatenate raw coordinates:
plant_lat || ',' || plant_lng

-- ✅ ALWAYS use NULL-safe coordinate formatting:
CASE WHEN plant_lat IS NOT NULL AND plant_lat != '' THEN ROUND(plant_lat::numeric, 4) ELSE '0' END || ',' || 
CASE WHEN plant_lng IS NOT NULL AND plant_lng != '' THEN ROUND(plant_lng::numeric, 4) ELSE '0' END
```

**3. MANDATORY time/duration handling with fallbacks:**
```sql
-- ✅ NULL-safe time formatting:
CASE WHEN ps_duration IS NOT NULL 
     THEN CASE WHEN EXTRACT(HOUR FROM ps_duration) > 0 
               THEN TO_CHAR(ps_duration, 'HH24"h "MI"m"')
               ELSE TO_CHAR(ps_duration, 'MI"m "SS"s"')
          END
     ELSE 'N/A'
END AS plant_site_duration
```

**4. SPECIAL drum_in_plant conversion with NULL safety:**
```sql
-- ✅ NULL-safe drum_in_plant conversion:
CASE WHEN drum_in_plant IS NULL OR drum_in_plant = '' OR drum_in_plant = '0'
     THEN '00h 00m 00s'
     ELSE TO_CHAR((COALESCE(drum_in_plant, '0') || ' minutes')::interval, 'HH24"h "MI"m "SS"s"')
END AS loading_time
```

**5. MANDATORY speed/distance formatting with N/A fallbacks:**
```sql
-- ✅ NULL-safe speed formatting:
CASE WHEN ps_max_speed IS NOT NULL AND ps_max_speed != ''
     THEN ROUND(ps_max_speed::numeric, 1) || ' km/h'
     ELSE 'N/A'
END AS plant_site_max_speed

-- ✅ NULL-safe distance formatting:
CASE WHEN ps_kms IS NOT NULL AND ps_kms != ''
     THEN CASE WHEN ps_kms >= 1.0
               THEN ROUND(ps_kms::numeric, 1) || ' Km'
               ELSE ROUND(ps_kms::numeric * 1000, 0) || ' m'
          END
     ELSE 'N/A'
END AS plant_site_distance_km
```

⚠️ **ABSOLUTE REQUIREMENTS:**
- **EVERY** `::numeric` cast MUST be wrapped in `IS NOT NULL AND != ''` checks
- **EVERY** coordinate display MUST validate empty strings before casting
- **EVERY** time calculation MUST handle NULL values with proper fallbacks
- **NEVER** assume data exists - always provide 'N/A' or '0' fallbacks
- **ALWAYS** use COALESCE() for interval calculations
- **MANDATORY** empty string checking for all text-to-numeric conversions

🔥 **FAILURE TO FOLLOW THESE PATTERNS WILL CAUSE "invalid input syntax for type numeric" ERRORS**

🚛 **COMPREHENSIVE DRUM_TRIP_REPORT SPECIFIC REQUIREMENTS - MANDATORY**

⚠️ **CRITICAL: For ALL drum_trip_report queries, apply these EXACT patterns:**

🔢 **IMPORTANT COLUMN TYPE INFORMATION:**
- **DOUBLE PRECISION columns**: ps_kms, sp_kms, cycle_km, ps_max_speed, ps_avg_speed, sp_max_speed, sp_avg_speed, plant_lat, plant_lng, site_lat, site_lng
- **For DOUBLE PRECISION**: Use `IS NOT NULL` only (NO empty string checks)
- **TEXT columns**: reg_no, tkt_no, drum_in_plant
- **For TEXT columns**: Use `IS NOT NULL AND != ''` (both NULL and empty string checks)

**1. MANDATORY Distance Column Formatting (NULL-safe with units):**
```sql
-- ✅ ps_kms formatting (DOUBLE PRECISION - only NULL check, no empty string check):
CASE WHEN ps_kms IS NOT NULL 
     THEN CASE WHEN ps_kms >= 1.0 
               THEN ROUND(ps_kms, 1) || ' Km' 
               ELSE ROUND(ps_kms * 1000, 0) || ' m' 
          END 
     ELSE 'N/A' 
END AS plant_site_distance_km

-- ✅ sp_kms formatting (DOUBLE PRECISION - only NULL check, no empty string check):
CASE WHEN sp_kms IS NOT NULL 
     THEN CASE WHEN sp_kms >= 1.0 
               THEN ROUND(sp_kms, 1) || ' Km' 
               ELSE ROUND(sp_kms * 1000, 0) || ' m' 
          END 
     ELSE 'N/A' 
END AS site_plant_distance_km

You are an expert PostgreSQL query generator. Convert this natural language request into a perfect SQL query.

🎯 **AI-FIRST PRINCIPLE**: Generate SIMPLE, CLEAN SQL that fetches raw data. Python will handle formatting later.

**CORE RULES:**
- Generate simple SELECT statements with raw columns
- NO formatting functions: NO ROUND(), NO CONCAT(), NO complex CASE statements  
- Let AI intelligently handle PostgreSQL data type conflicts
- Use basic aliases for readability
- Always include LIMIT 50 for performance
- Focus on accurate data retrieval, not presentation

Context:
{history_text}

User Question: {enhanced_prompt}

Generate a JSON response with this exact structure:
{{
    "sql": "SELECT ...",
    "response": "Brief explanation of what this query does"
}}
"""

    try:
        response = model.generate_content(full_prompt).text
        result = extract_json(response)
        
        # 🚨 CRITICAL: Validate and fix distance report queries
        if result and result.get('sql') and re.search(r'\b(distance.*report|distance|travel|drum.*rotation)\b', enhanced_prompt, re.IGNORECASE):
            sql = result['sql']
            
            # Check if distance_report table is being used
            if 'distance_report' in sql.lower():
                # Fix missing distance conversion
                if 'distance' in sql and 'distance / 1000' not in sql:
                    sql = re.sub(r'\bdistance\b(?!\s*/\s*1000)', 'ROUND(distance / 1000.0, 2) as distance_km', sql)
                    print("🔧 Fixed missing distance conversion formula")
                
                # Fix missing drum rotation conversion
                if 'drum_rotation' in sql and 'drum_rotation / 2' not in sql and 'CONCAT' not in sql:
                    sql = re.sub(
                        r'\bdrum_rotation\b(?!\s*/\s*2)', 
                        "CONCAT(LPAD((ROUND(drum_rotation / 2.0)::integer / 60)::text, 2, '0'), ':', LPAD((ROUND(drum_rotation / 2.0)::integer % 60)::text, 2, '0')) as drum_rotation_time", 
                        sql
                    )
                    print("🔧 Fixed missing drum rotation conversion formula")
                
                # Update the SQL in result
                result['sql'] = sql
                # Don't add technical messages to user response
        
        # ✅ AI-FIRST APPROACH: All formatting now handled by comprehensive LLM prompt
        # Previous complex regex patterns have been replaced with AI-first approach
        # The LLM now generates properly formatted SQL from the beginning
        
        # 🚨 CRITICAL: Ensure LIMIT 50 is always applied
        if result and result.get('sql'):
            sql = result['sql']
            if 'SELECT' in sql.upper() and 'LIMIT' not in sql.upper():
                # Add LIMIT 50 to SELECT queries that don't have a LIMIT
                sql += ' LIMIT 50'
                result['sql'] = sql
                print("🔧 Added LIMIT 50 to query for performance")
        
        return result
    except Exception as e:
        print(f"❌ LLM generation failed: {e}")
        return {
            "sql": None,
            "response": f"I couldn't process your request. Error: {str(e)}",
            "follow_up": None
        }


def generate_simple_drum_trip_sql(prompt, context_info, chat_context=None):
    """
    🚀 AI-FIRST APPROACH: Generate clean SQL for drum_trip_report
    Let the LLM handle all the complexity through intelligent prompting
    """
    
    # Check for simple, direct queries that should be ultra-simple
    prompt_lower = prompt.lower()
    
    # If it's a simple loading time query for a specific vehicle, generate ultra-simple SQL
    if 'loading time for' in prompt_lower:
        # Extract vehicle registration if possible
        import re
        vehicle_match = re.search(r'([A-Z]{2}\d{2}[A-Z]\d{4})', prompt, re.IGNORECASE)
        if vehicle_match:
            vehicle = vehicle_match.group(1).upper()
            return {
                "sql": f"SELECT reg_no, drum_in_plant FROM public.drum_trip_report WHERE reg_no = '{vehicle}' LIMIT 10;",
                "response": f"Fetching loading time for vehicle {vehicle}",
                "table_type": "drum_trip_report",
                "requires_formatting": True
            }
    
    # Build AI-first prompt - let LLM handle all formatting logic
    ai_prompt = f"""
You are a PostgreSQL expert specializing in drum_trip_report queries.

**TABLE: drum_trip_report (Transit Mixer Concrete Delivery Data)**

🎯 **AI-FIRST PRINCIPLE**: Generate SIMPLE, CLEAN SQL that fetches raw data. Python will handle formatting later.

**COLUMN UNDERSTANDING:**
- reg_no: Vehicle registration number  
- plant_out/site_in/site_out/plant_in: Delivery cycle timestamps
- ps_kms/sp_kms/cycle_km: Distances in kilometers (double precision)
- ps_duration/sp_duration/cycle_time: Time durations
- drum_in_plant: Loading time 
- plant_lat/plant_lng/site_lat/site_lng: Coordinates
- unloading_duration/site_waiting: Operation times
- tkt_no: Delivery ticket number

**CRITICAL RULES:**
1. Generate SIMPLE SQL - just SELECT the raw columns needed
2. NO formatting functions AT ALL - no ROUND(), no TRUNC(), no COALESCE for display
3. NO complex formatting in SQL - Python handles ALL formatting  
4. Always include LIMIT for performance
5. Use meaningful column aliases for display
6. Fetch RAW data only - let Python and LLM do ALL the formatting work

**ABSOLUTELY FORBIDDEN FUNCTIONS:** TRUNC(), ROUND(), COALESCE for display, CASE for formatting, coordinate conversion in SQL, string concatenation for units

User Request: {prompt}

Generate a JSON response:
{{
    "sql": "SELECT ... (simple, clean SQL with basic aliases)",
    "response": "Brief explanation"
}}
"""
    
    try:
        response = model.generate_content(ai_prompt).text
        result = extract_json(response)
        
        # Ensure LIMIT is present
        if result and result.get('sql'):
            sql = result['sql']
            if 'SELECT' in sql.upper() and 'LIMIT' not in sql.upper():
                sql += ' LIMIT 50'
                result['sql'] = sql
        
        # Mark that this result needs post-processing formatting
        if result:
            result['requires_formatting'] = True
            result['table_type'] = 'drum_trip_report'
        
        return result
    except Exception as e:
        print(f"❌ Simple SQL generation failed: {e}")
        return {
            "sql": "SELECT reg_no, plant_out, site_in FROM public.drum_trip_report LIMIT 20;",
            "response": f"Generated fallback query due to error: {str(e)}",
            "requires_formatting": True,
            "table_type": 'drum_trip_report'
        }


def format_raw_results(raw_results, table_type):
    """
    🎨 TWO-STAGE APPROACH - Stage 2: Format raw SQL results for user display
    Apply user-friendly formatting in Python instead of complex SQL
    """
    
    if not raw_results or not isinstance(raw_results, list):
        return []
    
    if table_type == 'drum_trip_report':
        return format_drum_trip_results(raw_results)
    elif table_type == 'distance_report':
        return format_distance_report_results(raw_results)
    else:
        # Generic formatting for other tables
        return raw_results


def format_drum_trip_results(raw_results):
    """
    🚀 AI-FIRST APPROACH: Simple, clean formatting for drum trip results
    Trust the LLM to handle complex formatting in SQL - just do basic business logic here
    """
    if not raw_results:
        return "No drum trip data found."
    
    formatted_results = []
    for row in raw_results:
        result = {}
        for column, value in row.items():
            # Simple NULL handling
            if value is None:
                result[column] = "Not available"
            # Handle key drum trip columns with business-friendly names
            elif column == 'drum_in_plant':
                result['Loading Time'] = f"{value} minutes" if isinstance(value, (int, float)) else str(value)
            elif column == 'reg_no':
                result['Vehicle'] = str(value)
            elif 'kms' in column.lower() or '_km' in column.lower():
                result[column] = f"{value} km" if isinstance(value, (int, float)) else str(value)
            elif 'duration' in column.lower() or 'time' in column.lower():
                result[column] = f"{value} mins" if isinstance(value, (int, float)) else str(value)
            else:
                result[column] = str(value)
        formatted_results.append(result)
    
    return formatted_results


def format_distance_report_results(raw_results):
    """Format distance_report raw results with user-friendly display"""
    formatted_results = []
    
    for row in raw_results:
        formatted_row = {}
        
        # Vehicle registration
        if 'reg_no' in row:
            formatted_row['registration_number'] = row['reg_no'] or 'N/A'
        
        # Distance conversion (meters to km)
        if 'distance' in row and row['distance'] is not None:
            try:
                distance_km = float(row['distance']) / 1000.0
                formatted_row['distance_km'] = f"{distance_km:.2f} Km"
            except:
                formatted_row['distance_km'] = 'N/A'
        else:
            formatted_row['distance_km'] = 'N/A'
        
        # Drum rotation conversion
        if 'drum_rotation' in row and row['drum_rotation'] is not None:
            try:
                rotation_minutes = float(row['drum_rotation']) / 2.0
                hours = int(rotation_minutes // 60)
                minutes = int(rotation_minutes % 60)
                formatted_row['drum_rotation_time'] = f"{hours:02d}:{minutes:02d}"
            except:
                formatted_row['drum_rotation_time'] = '00:00'
        else:
            formatted_row['drum_rotation_time'] = '00:00'
        
        # Format timestamps
        for ts_col, display_name in [('from_tm', 'start_time'), ('to_tm', 'end_time')]:
            if ts_col in row and row[ts_col]:
                try:
                    if isinstance(row[ts_col], str):
                        from datetime import datetime
                        dt = datetime.fromisoformat(row[ts_col].replace('Z', '+00:00'))
                        formatted_row[display_name] = dt.strftime('%d %b %Y %H:%M')
                    else:
                        formatted_row[display_name] = str(row[ts_col])
                except:
                    formatted_row[display_name] = str(row[ts_col])
            else:
                formatted_row[display_name] = 'N/A'
        
        formatted_results.append(formatted_row)
    
    return formatted_results


def handle_formatting_request(prompt, chat_context):
    """Handle formatting requests for existing data"""
    last_data = chat_context.last_result if chat_context else None
    if not last_data:
        return {
            "sql": None,
            "response": "I don't have any recent data to reformat. Please ask me a question first.",
            "follow_up": None
        }
    
    return {
        "sql": None,
        "follow_up": None,
        "force_format_response": {
            "question": last_data["question"],
            "columns": last_data["columns"],
            "rows": last_data["rows"],
            "format_hint": prompt
        }
    }


# Rest of the function continue normally below...
    if re.search(r'\b(plant|facility)\b', prompt, re.IGNORECASE):
        hierarchy_guidance += """
🏭 **PLANT QUERIES - ABSOLUTE RULE:**
⚠️ **CRITICAL**: ALWAYS and ONLY use hosp_master table for plant queries
⚠️ **IMPORTANT**: hosp_master contains PLANT DATA, not medical data!
❌ **NEVER USE**: plant_schedule, plant_master, or any other table for plant data
🔑 **PLANT COLUMN NAME**: Use `name` (NOT `plant_name`) for hosp_master table

Examples:
- "Show all plants" → SELECT DISTINCT name as plant_name FROM hosp_master WHERE name IS NOT NULL LIMIT 50
- "What plant does vehicle X belong to?" → 
  SELECT hm.name as plant_name FROM hosp_master hm 
  JOIN vehicle_master vm ON hm.id_no = vm.id_hosp 
  WHERE vm.reg_no = 'X' LIMIT 50
- "Plants in Punjab region" →
  SELECT hm.name as plant_name FROM hosp_master hm 
  JOIN district_master dm ON hm.id_dist = dm.id_no 
  WHERE dm.name ILIKE '%Punjab%' LIMIT 50
- "Vehicles in Mohali plant" →
  SELECT vm.reg_no as registration_number FROM vehicle_master vm 
  JOIN hosp_master hm ON vm.id_hosp = hm.id_no 
  WHERE hm.name ILIKE '%Mohali%' LIMIT 50

🔑 **REMEMBER**: hosp_master = PLANT/FACTORY data (NOT medical facilities)
"""

    # Vehicle hierarchy queries - ONLY vehicle_master
    if re.search(r'\b(vehicle|truck|fleet)\b', prompt, re.IGNORECASE):
        hierarchy_guidance += """
🚛 **VEHICLE QUERIES - ABSOLUTE RULE:**
⚠️ **CRITICAL**: ALWAYS and ONLY use vehicle_master table for vehicle queries
❌ **NEVER USE**: mega_trips, drv_veh_qr_assign, crm_site_visit_dtls, or any other table for vehicle data unless specifically joining

🎯 **VEHICLE HIERARCHY QUERY PATTERNS:**
- "Show all vehicles" → SELECT DISTINCT reg_no as registration_number FROM vehicle_master WHERE reg_no IS NOT NULL LIMIT 50
- "Vehicle X region and plant" → 
  SELECT vm.reg_no as registration_number, hm.name as plant_name, dm.name as region_name 
  FROM vehicle_master vm 
  LEFT JOIN hosp_master hm ON vm.id_hosp = hm.id_no 
  LEFT JOIN district_master dm ON hm.id_dist = dm.id_no 
  WHERE vm.reg_no = 'X' LIMIT 50
- "Which region does vehicle belong to" → 
  SELECT vm.reg_no, dm.name as region_name 
  FROM vehicle_master vm 
  LEFT JOIN hosp_master hm ON vm.id_hosp = hm.id_no 
  LEFT JOIN district_master dm ON hm.id_dist = dm.id_no 
  WHERE vm.reg_no = 'VEHICLE_REG'
- "Which plant does vehicle belong to" → 
  SELECT vm.reg_no, hm.name as plant_name 
  FROM vehicle_master vm 
  LEFT JOIN hosp_master hm ON vm.id_hosp = hm.id_no 
  WHERE vm.reg_no = 'VEHICLE_REG'
- "Show vehicle X with full hierarchy" → 
  SELECT vm.reg_no, hm.name as plant, dm.name as district, zm.zone_name 
  FROM vehicle_master vm 
  LEFT JOIN hosp_master hm ON vm.id_hosp = hm.id_no 
  LEFT JOIN district_master dm ON hm.id_dist = dm.id_no 
  LEFT JOIN zone_master zm ON dm.id_zone = zm.id_no 
  WHERE vm.reg_no = 'X'

⚠️ **MANDATORY RULES FOR VEHICLE QUERIES:**
1. ALWAYS start FROM vehicle_master (alias: vm) 
2. NEVER use crm_site_visit_dtls, mega_trips, or other tables as the primary table for vehicle info
3. JOIN hosp_master via vm.id_hosp = hm.id_no for plant information
4. JOIN district_master via hm.id_dist = dm.id_no for region information
5. Use vm.reg_no for vehicle registration number filtering
6. Vehicle registration number should appear only ONCE in WHERE clause, not repeated
"""

    # AI-FIRST Stoppage report queries - ONLY util_report with intelligent understanding
    if re.search(r'\b(stoppage|util_report|stop|idle|parked|journey|trip|tour|halt|pause|break|rest)\b', prompt, re.IGNORECASE):
        
        # AI-enhanced pattern recognition for better stoppage understanding
        is_vehicle_specific = bool(re.search(r'\b(?:vehicle|truck|bus)\s+([A-Z0-9\-]+)', prompt, re.IGNORECASE))
        is_duration_focused = bool(re.search(r'\b(?:long|short|extended|brief|duration|time|hours?|minutes?)\b', prompt, re.IGNORECASE))
        is_location_focused = bool(re.search(r'\b(?:where|location|place|at|in|near)\b', prompt, re.IGNORECASE))
        is_time_filtered = bool(re.search(r'\b(?:today|yesterday|this\s+week|last\s+week|(?:january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{4}|\d{4}-\d{2}-\d{2})\b', prompt, re.IGNORECASE))
        is_plant_focused = bool(re.search(r'\b(?:plant|depot|facility|mohali|chandigarh|delhi)\b', prompt, re.IGNORECASE))
        is_analysis_request = bool(re.search(r'\b(?:analyz|analis|report|summary|statistics|count|total|average|maximum)\b', prompt, re.IGNORECASE))
        
        hierarchy_guidance += """
� **AI-POWERED STOPPAGE REPORT SYSTEM - COMPREHENSIVE GUIDANCE:**
⚠️ **CRITICAL**: ALWAYS and ONLY use util_report table for ALL stoppage/utilization reports
❌ **ABSOLUTELY FORBIDDEN**: driver_stop_report, stop_report, or any other table for stoppage data

🧠 **AI STOPPAGE UNDERSTANDING:**
Current query context analysis:
- Vehicle-specific query: """ + str(is_vehicle_specific) + """
- Duration-focused query: """ + str(is_duration_focused) + """
- Location-focused query: """ + str(is_location_focused) + """
- Time-filtered query: """ + str(is_time_filtered) + """
- Plant/region-focused query: """ + str(is_plant_focused) + """
- Analysis/reporting request: """ + str(is_analysis_request) + """

🏗️ **UTIL_REPORT TABLE STRUCTURE (AI-Optimized):**
- **reg_no**: Vehicle registration number (KEY identifier - always include)
- **from_tm**: Stop start timestamp (WHEN vehicle stopped - format for users)
- **to_tm**: Stop end timestamp (WHEN vehicle resumed - format for users)  
- **location**: Combined "latitude/longitude" format (CONVERT to location names)
- **lat, long**: Separate coordinate columns (NEVER show raw to users)
- **duration**: Stop time period (FORMAT as "X hours Y minutes")
- **depo_id**: Plant hierarchy link → hosp_master.id_no (for business context)
- **report_type**: Should be 'stoppage' or NULL for stoppage queries

🎯 **AI-ENHANCED STOPPAGE QUERY PATTERNS:**

**SIMPLE STOPPAGE QUERIES (Let AI be intelligent about data types):**
- "Show stoppage report" → 
  ```sql
  SELECT ur.reg_no, ur.from_tm, ur.to_tm, ur.duration, ur.location, hm.name as plant_name
  FROM public.util_report ur
  LEFT JOIN public.hosp_master hm ON ur.depo_id = hm.id_no
  WHERE (ur.report_type = 'stoppage' OR ur.report_type IS NULL)
  ORDER BY ur.from_tm DESC LIMIT 50
  ```

**VEHICLE-SPECIFIC STOPPAGE:**
- "Vehicle stoppage details" → 
  ```sql
  SELECT ur.reg_no, ur.from_tm, ur.to_tm, ur.duration, ur.location, hm.name as plant_name
  FROM public.util_report ur
  LEFT JOIN public.hosp_master hm ON ur.depo_id = hm.id_no
  WHERE ur.reg_no ILIKE '%VEHICLE_REG%' 
    AND (ur.report_type = 'stoppage' OR ur.report_type IS NULL)
  ORDER BY ur.from_tm DESC LIMIT 50
  ```

**BASIC PATTERNS (Let AI handle complexity intelligently):**
- Always use simple SELECT with raw columns
- Let Python handle all formatting and data type conversions
- AI should be smart about numeric vs text column handling
- Use appropriate WHERE conditions based on data types
- Join with hierarchy tables when needed for context

📍 **AI-ENHANCED LOCATION HANDLING:**
⚠️ **CRITICAL USER EXPERIENCE RULE**: NEVER show raw coordinates to end users
✅ **BUSINESS-FRIENDLY DISPLAY**:
- Raw: "28.7041/77.1025" → Display: "Near Delhi NCR"
- Raw: "30.7333/76.7794" → Display: "Near Chandigarh"
- Raw: "null" → Display: "Location not available"

🕐 **INTELLIGENT TIME PROCESSING:**
- "Today" → WHERE DATE(from_tm) = CURRENT_DATE
- "Yesterday" → WHERE DATE(from_tm) = CURRENT_DATE - INTERVAL '1 day'  
- "This week" → WHERE from_tm >= DATE_TRUNC('week', CURRENT_DATE)
- "July 2025" → WHERE EXTRACT(MONTH FROM from_tm) = 7 AND EXTRACT(YEAR FROM from_tm) = 2025

🎯 **AI BUSINESS CONTEXT UNDERSTANDING:**
- "Stoppage" = Vehicle temporarily stopped during operation
- "Stop" = Same as stoppage (vehicle halt)
- "Idle" = Vehicle stopped with engine potentially running
- "Parked" = Vehicle stopped, typically longer duration
- "Journey/Trip/Tour stops" = Stops during travel (still use util_report)
- "Break/Rest/Halt" = Operational stops (still use util_report)

⚠️ **ABSOLUTE AI RULES:**
1. util_report = ONLY source for ALL stoppage data
2. ALWAYS join with hosp_master for plant context when possible
3. ALWAYS format duration in human-readable format
4. ALWAYS convert coordinates to location names for users
5. NEVER use driver_stop_report table for any stoppage query
6. Include plant hierarchy for business context unless specifically vehicle-only query
7. Order by from_tm DESC for chronological relevance"""

    # Distance report queries - ONLY distance_report
    if re.search(r'\b(distance.*report|distance|travel|drum.*rotation|kilometers?|km|metres?|meters?|plant.*to.*plant|inter.*plant)\b', prompt, re.IGNORECASE):
        hierarchy_guidance += """
🚚 **DISTANCE REPORT QUERIES - COMPREHENSIVE GUIDANCE:**
⚠️ **CRITICAL**: ALWAYS and ONLY use distance_report table for vehicle distance/travel reports
❌ **NEVER USE**: util_report, trip_report, or any other table for distance data

🛠️ **DISTANCE_REPORT TABLE STRUCTURE:**
- **reg_no**: Vehicle registration number (primary identifier) 
- **from_tm**: Journey start time (timestamp when travel began)
- **to_tm**: Journey end time (timestamp when travel ended)
- **distance**: Distance traveled in METERS (MUST convert to KM for display)
- **drum_rotation**: Raw drum rotation value (MUST apply formula and convert to HH:MM)
- **depo_id**: Links to hosp_master.id_no (for plant/region hierarchy)

🔧 **CRITICAL CONVERSION FORMULAS:**

1. **DISTANCE CONVERSION (DONE IN PYTHON):**
   - Database stores distance in METERS
   - Python will convert to KM: distance / 1000.0
   - Example: 5000 meters → Python converts to 5.00 KM

2. **DRUM ROTATION CONVERSION (DONE IN PYTHON):**
   - Raw value divided by 2 in Python: drum_rotation / 2
   - Result converted to HH:MM format in Python
   - Example: drum_rotation = 150 → Python: 150/2 = 75 minutes → "01:15"

🎯 **DISTANCE REPORT QUERY PATTERNS:**

**SIMPLE DISTANCE QUERIES (Let AI handle data types intelligently):**
- "Show distance report" → 
  ```sql
  SELECT reg_no, from_tm, to_tm, distance, drum_rotation
  FROM public.distance_report LIMIT 50
  ```

- "Distance report for vehicle X" → 
  ```sql
  SELECT reg_no, from_tm, to_tm, distance, drum_rotation
  FROM public.distance_report 
  WHERE reg_no ILIKE 'X' 
  ORDER BY from_tm LIMIT 50
  ```

**PLANT HIERARCHY JOINS (Simple patterns):**
- "Distance with plant info" → 
  ```sql
  SELECT dr.reg_no, hm.name as plant_name, dr.distance, dr.drum_rotation
  FROM public.distance_report dr 
  JOIN public.vehicle_master vm ON dr.reg_no = vm.reg_no
  JOIN public.hosp_master hm ON vm.id_hosp = hm.id_no LIMIT 50
  ```

**KEY PRINCIPLES:**
- Use simple SELECT with raw columns only
- Let Python handle all conversions (meters→KM, drum_rotation→HH:MM)
- AI should intelligently choose appropriate data type handling
- No complex CASE statements or formatting functions in SQL
- Focus on data retrieval, not presentation

⚠️ **MANDATORY CONVERSION RULES (DONE IN PYTHON, NOT SQL):**
1. **Distance conversion in Python**: Raw meters → KM with rounding
2. **Drum rotation conversion in Python**: Raw value / 2 → HH:MM format
3. **NEVER do conversions in SQL** - fetch raw data only
4. **NEVER show raw distance values in meters to users** - Python converts to KM
5. **NEVER show raw drum_rotation values to users** - Python converts to HH:MM
6. **Use JOIN with vehicle_master → hosp_master → district_master for hierarchy**
7. **SQL fetches raw data, Python handles all user-friendly formatting**

🎯 **DISTANCE REPORT CONTEXT UNDERSTANDING:**
- "Distance report" = distance_report table with conversions
- "Travel distance" = distance column converted to KM
- "Drum rotation" = drum_rotation / 2 converted to HH:MM format
- "Plant to plant distance" = JOIN with plant hierarchy
- "Vehicle travel analysis" = distance_report with vehicle/plant details
- "Inter-plant travel" = distance between different plant locations
- "Journey distance" = from_tm to to_tm with distance in KM
- "Travel time vs drum rotation" = compare journey duration with drum rotation time

🚨 **ABSOLUTE RULES:**
1. distance_report = ONLY table for vehicle travel/distance data
2. distance column = METERS (convert to KM with ROUND(distance/1000.0, 2))
3. drum_rotation = RAW value (apply formula: /2, then convert to HH:MM)
4. reg_no connects to vehicle_master for plant hierarchy
5. NEVER use util_report for distance queries!
6. ALWAYS apply both conversion formulas in every distance query
"""

    # 🚀 ENHANCED EMBEDDING PROCESSING with Advanced Table Mapping and Database Reference
    relevant_schema_text = SCHEMA_PROMPT  # Default fallback
    
    if EMBEDDINGS_AVAILABLE and embedding_manager:
        try:
            print(f"🎯 Analyzing query with enhanced mapping: '{prompt[:50]}...'")
            
            # STEP 1: Get embedding results (existing system)
            embedding_results = embedding_manager.find_relevant_tables(prompt, top_k=15)  # Get more candidates
            
            # STEP 2: Apply enhanced table mapping
            if enhanced_table_mapper and embedding_results:
                print(f"🔧 Applying enhanced table mapping...")
                
                # Extract available table names from schema
                available_tables = []
                if 'public' in SCHEMA_DICT:
                    available_tables = [f"public.{table}" for table in SCHEMA_DICT['public'].keys()]
                
                # Use enhanced mapper to re-rank tables
                enhanced_results = enhanced_table_mapper.rank_tables(prompt, embedding_results, available_tables)
                
                if enhanced_results:
                    print(f"📊 Enhanced mapping: Found {len(enhanced_results)} optimized tables")
                    relevant_tables = [(table, score, reason) for table, score, reason in enhanced_results]
                else:
                    print(f"📊 Fallback to embeddings: {len(embedding_results)} tables")
                    relevant_tables = embedding_results
            else:
                print(f"📊 Using embeddings with database reference: {len(embedding_results)} tables")
                relevant_tables = embedding_results
            
            if relevant_tables:
                # Build focused schema text with only relevant tables
                focused_schema = []
                for i, table_info in enumerate(relevant_tables):
                    try:
                        if len(table_info) >= 3:
                            table_key, similarity, reason = table_info
                        else:
                            table_key, similarity = table_info[:2]
                            reason = "embedding/reference"
                        
                        schema_name, table_name = table_key.split('.', 1)
                        if schema_name in SCHEMA_DICT and table_name in SCHEMA_DICT[schema_name]:
                            columns = SCHEMA_DICT[schema_name][table_name]
                            focused_schema.append(f"- {table_key}({', '.join(columns)})")
                            print(f"  • {table_key} (relevance: {similarity:.3f}, {reason}) - Columns: {len(columns)}")
                    except Exception as e:
                        print(f"⚠️ Error processing table {table_key}: {e}")
                
                if focused_schema:
                    relevant_schema_text = "Most relevant tables for your query:\n" + "\n".join(focused_schema)
                    print(f"✅ Using enhanced schema with {len(focused_schema)} tables instead of all {len(SCHEMA_DICT.get('public', {}))} tables")
                    
        except Exception as e:
            print(f"⚠️ Enhanced mapping error: {e}, falling back to full schema")

    schema_text = relevant_schema_text

    # Get distance conversion information
    distance_info = ""
    if DISTANCE_CONVERSION_AVAILABLE:
        try:
            distance_info = get_distance_conversion_info()
        except Exception as e:
            print(f"⚠️ Error getting distance conversion info: {e}")
            distance_info = ""

    full_prompt = f"""
You are an intelligent SQL assistant for multiple PostgreSQL schemas with advanced conversation memory.

{schema_text}

🏭 **CRITICAL TABLE CLARIFICATIONS - NEVER MISINTERPRET:**

⚠️ **MOST IMPORTANT**: `hosp_master` table contains **PLANT DATA**, NOT medical data!
- **hosp_master = PLANT MASTER TABLE** (despite the misleading name)
- Contains: Plant names, plant IDs, plant addresses, plant locations
- Use for: All plant-related queries, plant locations, facility information
- **NEVER** interpret as medical facility, healthcare data

🔑 **CORRECT TABLE MEANINGS:**
- **hosp_master**: PLANTS (factories, facilities, sites) - Use `hm.name` for plant names
- **district_master**: REGIONS/DISTRICTS/STATES - Use `dm.name` for region names  
- **zone_master**: ZONES (larger geographic areas) - Use `zm.zone_name` for zone names
- **vehicle_master**: VEHICLES/TRUCKS/FLEET - Use `vm.reg_no` for vehicle registration
- **util_report**: VEHICLE STOPPAGE/UTILIZATION REPORTS - Use for all stoppage queries (NOT driver_stop_report)
  • reg_no: Vehicle registration number
  • from_tm: Stop start time, to_tm: Stop end time  
  • location: Lat/Long formatted as "latitude/longitude" (convert to location names for users)
  • lat, long: Individual latitude/longitude columns (alternative to location)
  • duration: Time period of the stop
  • depo_id: Links to hosp_master.id_no for plant/region hierarchy

⚠️ **CRITICAL COLUMN VALUE MAPPINGS - EXACT VALUES REQUIRED:**

🚨 **MOST CRITICAL**: For status and correction columns, use **EXACT** database values:
- **active_status**: Use 'Y' for Open/Active complaints, 'N' for Closed (NEVER use 'Open'/'Closed')
- **product_correction**: Use 'Y' for Done/Completed correction, 'N' for Not Done (NEVER use 'Yes'/'No'/'Completed')
- **_action_status columns** (bh_action_status, cm_action_status, etc.): Use 'A' for Approved/Accepted, 'R' for Rejected/Refused/Declined (NEVER use 'Y'/'N')

**EXAMPLES OF CORRECT USAGE:**
- ✅ `WHERE active_status = 'Y'` (for open complaints)
- ✅ `WHERE product_correction = 'Y'` (for completed corrections)
- ✅ `WHERE bh_action_status = 'A'` (for approved actions)
- ✅ `WHERE cm_action_status = 'R'` (for rejected actions)
- ❌ `WHERE active_status = 'Open'` (WRONG!)
- ❌ `WHERE product_correction = 'Yes'` (WRONG!)
- ❌ `WHERE bh_action_status = 'Y'` (WRONG! Use 'A' instead)

🎯 **UNIVERSAL NAME MATCHING STRATEGY - HANDLE IRREGULARITIES:**

⚠️ **CRITICAL PROBLEM**: Database values often have inconsistent formatting:
- Spacing issues: "Nagpur-Hingna" vs "Nagpur- Hingna" vs "Nagpur - Hingna"
- Case variations: "mohali" vs "Mohali" vs "MOHALI"
- Special characters: "Plant-A" vs "Plant_A" vs "PlantA"
- Leading/trailing spaces: " Mumbai " vs "Mumbai"

✅ **MANDATORY FLEXIBLE MATCHING RULES FOR ALL NAME-BASED QUERIES:**

1. **NEVER USE EXACT EQUALITY (=) FOR TEXT MATCHING**
   - ❌ `WHERE name = 'Nagpur-Hingna'` (will fail if space exists)
   - ✅ `WHERE name ILIKE '%nagpur%' AND name ILIKE '%hingna%'` (handles all variations)

2. **COMPOUND NAME STRATEGY** (names with hyphens, spaces, multiple words):
   - Split compound names into keywords
   - Use multiple ILIKE conditions with AND
   - Examples:
     - "Nagpur-Hingna" → `WHERE (name ILIKE '%nagpur%' AND name ILIKE '%hingna%')`
     - "New Delhi" → `WHERE (name ILIKE '%new%' AND name ILIKE '%delhi%')`
     - "PB-Mohali" → `WHERE name ILIKE '%mohali%'` (focus on main location)

3. **SIMPLE NAME STRATEGY** (single word names):
   - Use ILIKE '%keyword%' for partial matching
   - Examples:
     - "Mohali" → `WHERE name ILIKE '%mohali%'`
     - "Mumbai" → `WHERE name ILIKE '%mumbai%'`

4. **VEHICLE REGISTRATION MATCHING**:
   - Vehicle registrations are usually more consistent but can have case issues
   - Use: `WHERE reg_no ILIKE 'MH12SX6301'` for case-insensitive matching

5. **REGIONAL NAME MATCHING**:
   - Regions/states/districts can have various representations
   - "Punjab" → `WHERE region_name ILIKE '%punjab%'`
   - "West Bengal" → `WHERE (region_name ILIKE '%west%' AND region_name ILIKE '%bengal%')`

⚠️ **EXAMPLES OF ROBUST QUERIES:**

```sql
-- Plant vehicle count (handles name variations)
SELECT COUNT(vm.reg_no) 
FROM vehicle_master vm 
JOIN hosp_master hm ON vm.id_hosp = hm.id_no 
WHERE (hm.name ILIKE '%nagpur%' AND hm.name ILIKE '%hingna%')

-- Regional plant search (handles case and spacing)
SELECT hm.name 
FROM hosp_master hm 
JOIN district_master dm ON hm.id_dist = dm.id_no 
WHERE dm.name ILIKE '%punjab%'

-- Vehicle search (case-insensitive)
SELECT vm.reg_no, hm.name as plant_name 
FROM vehicle_master vm 
JOIN hosp_master hm ON vm.id_hosp = hm.id_no 
WHERE vm.reg_no ILIKE 'mh12sx6301'
```

🚨 **MANDATORY IMPLEMENTATION RULES:**
1. **Always use ILIKE instead of = for text matching**
2. **Always use '%keyword%' pattern for partial matching**
3. **Split compound names into individual keywords**
4. **Use AND conditions for multiple keywords in same field**
5. **Make all text matching case-insensitive**
6. **Handle hyphenated names by splitting on meaningful parts**

This approach ensures queries work regardless of spacing, case, or minor formatting differences in the database.

� **CRITICAL COLUMN VALIDATION - EXACT COLUMN NAMES REQUIRED:**

**FOR CRM COMPLAINT TABLES**: Only use columns that ACTUALLY exist in the schema:
- **crm_complaint_dtls**: Use ONLY columns explicitly listed in schema (check id_no, complaint_date, complaint_category_id, active_status, cust_id, plant_id)
- **crm_site_visit_dtls**: Use ONLY columns explicitly listed in schema (check complaint_id, complaint_status, product_correction, bh_action_status, ho_qc_action_status, etc.)
- **NEVER assume columns exist** - always verify against the provided schema

**COMMON WRONG ASSUMPTIONS TO AVOID:**
- ❌ `description` (This column may NOT exist in crm_complaint_dtls)
- ❌ `title` (This column may NOT exist in crm_complaint_dtls)  
- ❌ `details` (This column may NOT exist in crm_complaint_dtls)
- ❌ `summary` (This column may NOT exist in crm_complaint_dtls)
- ❌ `complaint_description` (This column may NOT exist in crm_complaint_dtls)

**CORRECT APPROACH FOR COMPLAINT DETAILS:**
- ✅ ALWAYS check the provided schema for exact column names
- ✅ Use: `id_no, complaint_date, complaint_category_id, active_status` (if they exist in schema)
- ✅ Join with crm_site_visit_dtls for: complaint_status, product_correction, action statuses
- ✅ Join with hosp_master for plant names using plant_id relationship
- ✅ Join with crm_customer_dtls for customer information using cust_id relationship
- ✅ If needed columns don't exist, explain limitation to user

**EXAMPLES OF CORRECT COLUMN VALIDATION:**
- ✅ `SELECT cd.id_no, cd.complaint_date FROM crm_complaint_dtls cd` (verify columns exist in schema)
- ✅ `WHERE csv.ho_qc_action_status = 'R'` (for rejected by HO QC - verify column exists)
- ✅ `WHERE cd.active_status = 'Y'` (for active complaints - verify column exists)
- ❌ `SELECT cd.description FROM crm_complaint_dtls cd` (WRONG! Verify column exists first)

�📋 **QUERY INTERPRETATION RULES:**
- "Show plants" → SELECT FROM hosp_master (NOT medical facilities!)
- "Vehicles in Mohali" → JOIN vehicle_master with hosp_master WHERE plant name ILIKE '%Mohali%'
- "Plants in Punjab" → JOIN hosp_master with district_master WHERE region name ILIKE '%Punjab%'
- "Stoppage report" → SELECT FROM util_report (NOT driver_stop_report!)
- "Vehicle stoppage" → SELECT FROM util_report WHERE reg_no conditions
- "Stops during journey/trip/tour" → SELECT FROM util_report with time filters
- "Where did vehicle stop" → SELECT location/lat/long FROM util_report (convert coordinates to names)
- "How long stopped" → SELECT duration FROM util_report
- "Stop timings" → SELECT from_tm, to_tm FROM util_report
- "Plant-wise stoppages" → JOIN util_report with hosp_master via depo_id
- "Regional stoppage analysis" → JOIN util_report → hosp_master → district_master via depo_id
- "Which region does vehicle X belong to" → SELECT FROM vehicle_master vm JOIN hosp_master hm JOIN district_master dm WHERE vm.reg_no = 'X'
- "Which plant does vehicle X belong to" → SELECT FROM vehicle_master vm JOIN hosp_master hm WHERE vm.reg_no = 'X'
- "Vehicle X region and plant" → SELECT FROM vehicle_master vm JOIN hosp_master hm JOIN district_master dm WHERE vm.reg_no = 'X'

🚨 **CRITICAL TABLE NAME WARNING - NEVER USE THESE NAMES:**
- **NEVER** use table name "stoppage_report" (this table DOES NOT EXIST!)
- **ALWAYS** use "util_report" for ALL stoppage/stop-related queries
- **NEVER** assume hosp_master contains medical information
- **NEVER** use driver_stop_report for vehicle stoppage queries
- **NEVER** use crm_site_visit_dtls as primary table for vehicle hierarchy queries

⚠️ **STOPPAGE DATA TABLE MAPPING - MANDATORY:**
- "stoppage report" queries → **ALWAYS USE util_report table**
- "vehicle stoppage" queries → **ALWAYS USE util_report table**  
- "stop analysis" queries → **ALWAYS USE util_report table**
- Table name should ALWAYS be "public.util_report" in SQL (NOT stoppage_report!)

{id_relationship_guide}

{distance_info}

{context_info}

{plant_guidance}

{hierarchy_guidance}

🕐 **CRITICAL: USER-FRIENDLY DATE FORMATTING - AI-FIRST APPROACH:**

⚠️ **MANDATORY DATE FORMATTING RULES FOR ALL QUERIES:**

1. **AUTOMATIC DATE FORMATTING (REQUIRED FOR ALL DATETIME COLUMNS):**
   - **NEVER return raw ISO date formats** (e.g., "2025-07-12 19:53:05")
   - **ALWAYS format dates to be user-friendly** using PostgreSQL TO_CHAR function
   - **Apply to ALL timestamp, date, and datetime columns automatically**

2. **STANDARD DATE FORMAT PATTERNS:**
   - **Primary format (Date with Time)**: `TO_CHAR(column_name, 'DD Mon YYYY HH24:MI') as formatted_column_name` (e.g., "12 Jul 2025 19:53")
   - **Date Only**: `TO_CHAR(column_name, 'DD Mon YYYY') as formatted_column_name` (e.g., "12 Jul 2025")
   - **Alternative format**: `TO_CHAR(column_name, 'DD-MM-YYYY HH24:MI:SS') as formatted_column_name` (if seconds needed)

3. **EXAMPLES OF CORRECT DATE FORMATTING:**
   ```sql
   -- Speed violation query with formatted date
   SELECT vm.reg_no as registration_number,
          vr.max_speed as maximum_speed_kmh,
          TO_CHAR(vr.from_tm, 'DD Mon YYYY HH24:MI') as violation_start_time
   FROM public.violate_report_65 vr
   JOIN public.vehicle_master vm ON vr.id_vehicle = vm.id_no
   
   -- Distance report with formatted dates
   SELECT reg_no as registration_number,
          TO_CHAR(from_tm, 'DD Mon YYYY HH24:MI') as journey_start,
          TO_CHAR(to_tm, 'DD Mon YYYY HH24:MI') as journey_end,
          ROUND(distance / 1000.0, 2) as distance_km
   FROM public.distance_report
   
   -- Complaint report with formatted dates
   SELECT id_no as complaint_id,
          TO_CHAR(complaint_date, 'DD Mon YYYY') as complaint_date_formatted
   FROM public.crm_complaint_dtls
   ```

4. **COMPREHENSIVE DATE COLUMN IDENTIFICATION:**
   - **Timestamp columns**: from_tm, to_tm, date_time, created_at, updated_at
   - **Date columns**: complaint_date, visit_date, report_date
   - **Datetime columns**: Any column with timestamp, datetime, or date data type
   - **Apply formatting to ALL such columns automatically**

5. **DATE FORMAT PREFERENCES:**
   - **Primary format**: DD Mon YYYY HH24:MI (e.g., "12 Jul 2025 19:53")
   - **Date only**: DD Mon YYYY (e.g., "12 Jul 2025")
   - **With seconds**: DD Mon YYYY HH24:MI:SS (e.g., "12 Jul 2025 19:53:05")
   - **Choose appropriate format based on column type and user query context**

6. **CRITICAL IMPLEMENTATION RULES:**
   - **IDENTIFY every datetime column in your query**
   - **WRAP each datetime column with TO_CHAR() function**
   - **USE descriptive aliases** (e.g., violation_start_time, journey_start)
   - **NEVER leave raw datetime columns unformatted**
   - **APPLY this to ALL queries, not just specific ones**

⚠️ **THIS APPLIES TO ALL TABLES AND ALL DATETIME COLUMNS:**
- violate_report_* tables: format from_tm, to_tm, date_time columns
- distance_report: format from_tm, to_tm columns  
- util_report: format from_tm, to_tm columns
- crm_complaint_dtls: format complaint_date column
- ANY table with datetime/timestamp columns

🎯 **AI-FIRST RULE**: When generating any SQL query, automatically scan for datetime columns and apply user-friendly formatting using TO_CHAR() function with appropriate date patterns.

Always use PostgreSQL-compatible datetime functions like EXTRACT(), DATE_TRUNC(), and TO_CHAR() instead of SQLite functions like strftime().

Your task:
1. Analyze the user's question in the context of the ongoing conversation.
2. Use the conversation context and recent queries to understand follow-up questions and references.
3. If the user refers to "these", "those", "the previous results", "that data", etc., use the context to understand what they mean.
4. Identify which schema the question belongs to.
5. Return ONLY a JSON with:
   - schema
   - sql
   - response (a *placeholder* natural language answer for user)
   - follow_up (suggested question or null)

🧠 **Smart Context Handling & Ordinal References**

When processing follow-up questions:
- **"Show me more details"** → Use the last result context to understand what "more details" means
- **"What about the total?"** → Apply aggregation to the last queried dataset
- **"Which one is the best?"** → Apply ranking/filtering to the last result set
- **"Can you summarize that?"** → Summarize the last query results
- **"Show it as a table"** → Reformat the last results

**Ordinal References (CRITICAL):**
- **"7th vehicle"**, **"first item"**, **"the 3rd result"** → Use the ORDINAL REFERENCE and TARGET ITEM IDENTIFIER from context
- If context shows "TARGET ITEM IDENTIFIER: MH12SX6301", then query specifically for that identifier
- **NEVER** claim you don't have access to previously shown data if it's referenced in context
- **ALWAYS** use the specific identifier when provided in the enhanced prompt

**Consistency Rules:**
- If previous query returned data successfully, similar queries for the same data MUST also work
- If a vehicle was in a previous result set, it MUST be queryable individually
- Use the same tables and columns that worked before

Use the CONVERSATION CONTEXT and RECENT SQL QUERIES to understand:
- What data the user is referring to
- What scope they want (specific subset vs all data)
- What their follow-up question is really asking for

Always use PostgreSQL-compatible datetime functions like EXTRACT(), DATE_TRUNC(), and TO_CHAR() instead of SQLite functions like strftime().

Your task:
1. Analyze the user's question.
2. Identify which schema it belongs to.
3. Return ONLY a JSON with:
   - schema
   - sql
   - response (a *placeholder* natural language answer for user)
   - follow_up (suggested question or null)

🔁 **Handling Follow-up Questions and Contextual Scope**

If the user asks a question that appears to follow from a previous result, list, or subset (e.g., “these 10 vehicles”, “that result”, “total distance covered”), you **must determine the correct scope**.

- If the scope is **clear from recent context** (e.g., a recent list of 10 vehicles or a selected route), apply your logic to **only that subset**.
- If the scope is **not clearly defined**, or could be interpreted in multiple ways (e.g., whole DB vs subset), **do not assume**.
- Instead, **return a clarifying response** in the `response` field. Example:

  > "Just to confirm: do you want the total distance covered by all vehicles in the database, or only the 10 recently listed ones?"

- This applies to follow-ups like:
  - "What's the total cost?"
  - "Show their duration."
  - "Which one is longest?"
  - "Give a summary."
  - "Show the top 5."

📌 You must **track the last known result set**, such as:
  - Last filtered list
  - A user-provided group (e.g., “top 5 most used vehicles”)
  - Any manually listed items (e.g., reg_nos just displayed)

---

🔍 **Column Validation Rules:**

- **STEP 1**: Before writing any SQL, carefully examine the provided schema.
- **STEP 2**: For each table you want to query, verify the exact column names AND DATA TYPES listed.
- **STEP 3**: **CRITICAL: NEVER assume column names exist** - only use columns explicitly listed in the schema.
- **STEP 4**: **CRITICAL: NEVER use SUM() or AVG() on TEXT columns** (marked as TEXT in schema).
- **STEP 5**: Only use SUM() or AVG() on NUMERIC columns (marked as NUMERIC in schema).
- **STEP 6**: If you need to join tables, ensure the join columns exist in BOTH tables.
- **STEP 7**: If a user asks for data that requires non-existent columns, explain the limitation and suggest available columns.

**Critical Column Existence Check:**
- **BEFORE generating SQL**: Verify EVERY column exists in the provided schema
- **IF column not found**: Return error explaining which columns ARE available
- **COMMON MISTAKES**: Assuming 'description', 'title', 'details' columns exist without checking schema
- **CORRECT APPROACH**: Only reference columns explicitly listed in schema for each table

**Data Type Rules:**
- **TEXT columns** (character varying, text, character): 
  - Use COUNT(), MAX(), MIN() by default
  - For columns with numeric names (total_price, total_value, quantity, amount): Use CAST(column AS NUMERIC) with SUM()/AVG()
  - Example: `SUM(CAST(total_so_value AS NUMERIC))` instead of `SUM(total_so_value)`
- **NUMERIC columns** (integer, decimal, numeric, real, double precision): Can use SUM(), AVG(), COUNT(), MAX(), MIN() directly
- **When in doubt**: Use COUNT() which works on all column types

**Type Casting Examples:**
- `SUM(CAST(total_price AS NUMERIC))` - converts text to number for calculation
- `AVG(CAST(quantity AS NUMERIC))` - converts text to number for average
- `SUM(CAST(total_so_value AS NUMERIC))` - converts text to number for sum

**Example**: If user asks "show total quantity" but `quantity` is marked as TEXT, respond with:
```json
{{
  "schema": null,
  "sql": null,
  "response": "I cannot calculate the total quantity because the 'quantity' column contains text data, not numbers. I can show you the count of records or individual quantity values instead.",
  "follow_up": "Would you like to see the count of SO details records or view individual quantity values?"
}}
```

**Example**: If user asks for complaint details but references non-existent columns, respond with:
```json
{{
  "schema": null,
  "sql": null,
  "response": "I cannot retrieve the 'description' column because it doesn't exist in the crm_complaint_dtls table. Available columns include: id_no, complaint_date, complaint_category_id, active_status, cust_id, plant_id. Would you like me to show these details instead?",
  "follow_up": "Which of the available complaint details would you like to see?"
}}
```

---

❗ Strict instructions:

🚀 **AI-FIRST CORE PRINCIPLE**: Generate SIMPLE, CLEAN SQL queries that fetch RAW data ONLY. Let Python handle ALL formatting, coordinate conversion, and business logic. 

**SIMPLICITY RULES:**
- NO formatting functions in SQL AT ALL - no ROUND(), no TRUNC(), no COALESCE for display
- NO complex CASE statements or formatting in SQL
- NO coordinate-to-location conversion in SQL
- NO string concatenation with || for display units in SQL
- NO mathematical operations for display formatting
- Keep SQL focused ONLY on data retrieval, not presentation
- Let Python formatting handle ALL units, labels, rounding, and business display logic

**ABSOLUTELY FORBIDDEN FUNCTIONS IN SQL:** TRUNC(), ROUND(), COALESCE for display, complex CASE WHEN for display, coordinate conversion, string concatenation for units

- **Do not return actual DB results.**
- **Return only a valid JSON object — no markdown or commentary outside the JSON.**
- **SQL must always use schema-qualified table names.**
- **Never use unqualified table or column names.**
- **CRITICAL: ONLY use columns that are explicitly listed in the schema above. If a column is not listed, DO NOT use it.**
- **CRITICAL: Before generating any SQL, verify that ALL columns referenced exist in the provided schema.**
- **If you need a column that doesn't exist, return an error in the 'response' field explaining the limitation.**
- **For potentially large datasets, always add LIMIT 50 to prevent performance issues.**
- **If user asks for "all" records from large tables, suggest aggregations instead.**
- **ALWAYS use descriptive column aliases in SQL for user-friendly display (e.g., 'reg_no as registration_number', 'name as plant_name')**
- **Basic datetime formatting with TO_CHAR() is OK, but keep it simple**
- **NEVER include suggestions, follow-up questions, or recommendations in responses**
- For year-based filters (e.g., "deployed in 2022"), use:
  - `EXTRACT(YEAR FROM column) = 2022`, or
  - `column BETWEEN '2022-01-01' AND '2022-12-31'`
- When answering questions about time ranges (e.g., "earliest trip date", "trips in the last month"), you must:
  - Use `MIN()` and `MAX()` on timestamp columns (like `alert_ign.date_time` or relevant trip tables)
  - Mention the specific column name and its role in the `response`
  - Never say the range is unknown unless the column truly has no values

  Example:
  "To get the full range of vehicle activity, we'll look at the `alert_ign.date_time` column using MIN() and MAX()."

- If the user asks about "latest trips", you must:
  - Check the max value of the trip/alert date column
  - Use `DATE_TRUNC()` to find the most recent full month

---

🎯 **Clarity rules for ambiguous terms**:

Words like **"duration"**, **"total"**, **"usage"**, **"activity"**, **"amount"**, and **"count"** can have multiple meanings depending on context.

When such terms appear:

1. Infer the **most likely meaning** based on the **current question**.
2. Compare that to any **previous user queries** (in conversation history).
3. If ambiguity is possible:
   - Explicitly **explain the difference**.
   - Clarify **which interpretation** you're using and **why**.

📌 Examples:
- **"duration"** could mean:
  - A **fixed field** in metadata
  - A **calculated value** like `end_time - start_time`
  - A **user-defined time range**

- **"usage"** might refer to:
  - A **count of trips**
  - **Distance covered**
  - **Fuel consumption**, etc.

- **"date range"**, **"latest month"**, **"recent activity"**, or **"full timeline"** may mean:
  - The **MIN/MAX** of a datetime field (e.g., `date_time`)
  - The **most recent month** (`MAX(date_time)` then group or filter)
  - An **ongoing or rolling period** (e.g., last 30 days)

👉 In such cases, clarify:
- Which **field** is being used (e.g., `alert_ign.date_time`)
- What the **range boundaries** are (e.g., "from 2024-05-01 to 2025-07-10")
- Whether the request includes **only completed trips**, **active routes**, or **all records**

---

🧠 **Context-switch detection**:

If the user switches from one entity (e.g., *vehicle*) to another (e.g., *route*) while using overlapping terms (e.g., "amount", "usage"):

- Assume their intent **may have shifted**
- Verify which entity each term applies to now
- Clearly state which table or field the metric comes from

---

🎨 **Response formatting guidelines** (applies only to the 'response' and 'follow_up' strings):

- Use **headings** and **bullet points** to organize information
- Use **tables** when comparing or summarizing key data
- Use **bold** to highlight important terms or metrics
- Use **code blocks** (` ```sql `) to show the query clearly
- Optionally use **emojis** to enhance clarity and structure (e.g. 🧮, 📊, ⏱️)
- Avoid long-winded text — be clear, concise, and helpful

---

Use this **strict JSON structure** exactly:

```json
{{
  "schema": "schema_name or null",
  "sql": "SQL query string or null", 
  "response": "Short natural-language placeholder answer (e.g. 'Sure, let me get that for you.')",
  "follow_up": "suggested helpful follow-up question"
}}
```

Conversation so far:
{history_text}
User: {enhanced_prompt}
"""


    try:
        response = model.generate_content(full_prompt).text
        return extract_json(response)
    except Exception:
        return {
            "schema": None,
            "sql": None,
            "response": "Sorry, I couldn't process that.",
            "follow_up": None
        }

def generate_final_response(user_question, columns, rows, chat_context=None):
    # Map specific database column names to meaningful business-friendly display names
    # AI handles the rest automatically using smart snake_case to Title Case conversion
    column_display_map = {
        # Vehicle & Registration
        'reg_no': 'Vehicle Registration',
        'registration_number': 'Vehicle Registration',
        
        # Plant & Location (hosp_master = PLANT data, not medical!)
        'plant_name': 'Plant Name',
        'name': 'Plant/Location Name',  # Could be plant name from hosp_master
        
        # Time & Duration
        'from_tm': 'Start Time',
        'to_tm': 'End Time',
        'start_time': 'Start Time',
        'end_time': 'End Time',
        'drum_in_plant': 'Loading Time',  # Specific for drum trip reports
        'drum_rotation_time': 'Drum Rotation Time',
        'drum_rotation_hhmm': 'Drum Rotation (HH:MM)',
        'duration': 'Duration',
        
        # Distance & Travel
        'distance_km': 'Distance (KM)',
        'total_distance_km': 'Total Distance (KM)',
        
        # Geographic Hierarchy
        'region_name': 'Region',
        'district_name': 'District',
        'zone_name': 'Zone',
        
        # Status & Classification
        'active_status': 'Status',
        'complaint_status': 'Complaint Status',
        'product_correction': 'Correction Status',
        
        # Common Business Fields
        'complaint_date': 'Complaint Date',
        'location': 'Location',
        'id_no': 'ID Number',
        
        # AI will automatically convert other columns:
        # vehicle_plant → Vehicle Plant, stop_duration → Stop Duration, etc.
    }
    
    # Create display columns with user-friendly names
    display_columns = []
    for col in columns:
        display_name = column_display_map.get(col.lower(), col.replace('_', ' ').title())
        display_columns.append(display_name)
    
    rows_json = []
    for r in rows:
        row_dict = {}
        for i, (col, val) in enumerate(zip(columns, r)):
            display_col = display_columns[i]  # Use the user-friendly column name
            if isinstance(val, datetime.timedelta):
                days = val.days
                hours = val.seconds // 3600
                minutes = (val.seconds % 3600) // 60
                text = f"{days} days"
                if hours:
                    text += f", {hours} hours"
                if minutes:
                    text += f", {minutes} minutes"
                row_dict[display_col] = text
            elif isinstance(val, datetime.time):
                # Handle datetime.time objects (like duration columns)
                hours = val.hour
                minutes = val.minute
                seconds = val.second
                if hours > 0:
                    row_dict[display_col] = f"{hours}h {minutes}m {seconds}s"
                elif minutes > 0:
                    row_dict[display_col] = f"{minutes}m {seconds}s"
                else:
                    row_dict[display_col] = f"{seconds}s"
            elif isinstance(val, (datetime.datetime, datetime.date)):
                # Format datetime objects to user-friendly format instead of ISO format
                if hasattr(val, 'strftime'):
                    if isinstance(val, datetime.datetime):
                        # Full datetime: 09 November 2023 06:12:29 AM
                        row_dict[display_col] = val.strftime('%d %B %Y %I:%M:%S %p')
                    else:
                        # Date only: 09 November 2023  
                        row_dict[display_col] = val.strftime('%d %B %Y')
                else:
                    row_dict[display_col] = str(val)
            elif isinstance(val, (float, Decimal)):
                row_dict[display_col] = round(float(val), 2)
            elif col.lower() == 'location' and isinstance(val, str) and LOCATION_CONVERSION_AVAILABLE:
                # Convert location coordinates to readable names
                try:
                    readable_location = convert_location_string_to_readable(val)
                    row_dict[display_col] = readable_location
                    # Also store original coordinates for reference
                    row_dict[f'{display_col}_coordinates'] = val
                except Exception as e:
                    print(f"⚠️ Location conversion failed for '{val}': {e}")
                    row_dict[display_col] = val
            elif col.lower() in ['distance_km', 'distance'] and isinstance(val, (int, float, Decimal)):
                # Handle distance conversion - if it looks like raw meters, convert to KM
                distance_val = float(val)
                if distance_val > 1000:  # Likely raw meters
                    distance_km = round(distance_val / 1000.0, 2)
                    row_dict[display_col] = f"{distance_km} KM"
                else:  # Already in KM
                    row_dict[display_col] = f"{round(distance_val, 2)} KM"
            elif col.lower() in ['drum_rotation_time', 'drum_rotation_hhmm', 'drum_time'] and isinstance(val, str):
                # Format drum rotation time (already converted to HH:MM format in SQL)
                row_dict[display_col] = val
            elif col.lower() in ['drum_rotation'] and isinstance(val, (int, float, Decimal)):
                # Convert raw drum rotation to HH:MM format if not already converted in SQL
                drum_raw = float(val)
                if drum_raw > 0:
                    drum_minutes = round(drum_raw / 2.0)
                    hours = drum_minutes // 60
                    minutes = drum_minutes % 60
                    row_dict[display_col] = f"{hours:02d}:{minutes:02d}"
                else:
                    row_dict[display_col] = "00:00"
            else:
                row_dict[display_col] = val
        rows_json.append(row_dict)

    formatted_data = json.dumps(rows_json, separators=(',', ':'), cls=DecimalEncoder)

    # Add conversation context for better response generation
    context_info = ""
    if chat_context:
        context_info = chat_context.get_context_for_llm(user_question)
        if context_info:
            context_info = f"\nCONVERSATION CONTEXT:\n{context_info}\n"

    formatting_prompt = f"""
You are a helpful assistant with excellent conversation memory. Given the user's question and the database results in JSON, generate the most natural, clear, and helpful answer for the user.

{context_info}

Instructions:
- Use the conversation context to understand follow-up questions and references to previous data
- If the user asks to reformat, summarize, or present the previous data in a different way (such as 'show as table', 'show as list', 'summarize', etc.), always use the most recent data/results available, not just the new user question.
- If the user refers to "these results", "that data", "the previous query", etc., use the context to understand what they mean
- Be aware of what was just discussed and respond intelligently to follow-up questions
- If the answer can be given in natural language, do so.
- Only use a markdown table if it is truly necessary for clarity (e.g., multiple rows or columns that cannot be summarized naturally).
- If the answer is a single value or can be summarized in a sentence, prefer natural language.

**HANDLING EMPTY/NULL DATA:**
- If there is NO DATA returned (empty result set), say: "I couldn't find any information about [specific thing requested] for [specific item/vehicle]."
- If data is returned but contains NULL/empty values, say: "I found [vehicle/item] in the system, but the [specific field requested] information is not available or hasn't been recorded."
- Be specific about what was requested and what is missing
- DO NOT suggest alternative queries or ask follow-up questions

**LOCATION DATA FORMATTING:**
- NEVER show raw latitude/longitude coordinates to users (e.g., don't show "28.7041/77.1025")
- Convert coordinate data to readable location names (e.g., "Near Delhi", "Mumbai Region", "Highway Junction")
- If location column contains "lat/long" format, interpret and convert to meaningful place names
- For stoppage reports, always present locations as understandable place names, not coordinates

**DISTANCE REPORT DATA FORMATTING:**
- NEVER show raw distance values in meters to users (e.g., don't show "151515 meters")
- ALWAYS convert distance to KM with proper formatting (e.g., "151.52 KM")
- NEVER show raw drum_rotation values to users (e.g., don't show "1794")
- ALWAYS convert drum_rotation to HH:MM format (e.g., "14:57" for 1794/2 = 897 minutes)
- For distance reports, emphasize the converted, user-friendly values
- Explain that distances are inter-plant travel distances when relevant

**DISTANCE REPORT FORMATTING:**
- Distance values are automatically converted to KM with proper formatting (e.g., "15.50 KM")
- Drum rotation values are automatically converted to HH:MM format (e.g., "02:30" for 2 hours 30 minutes)
- Present distance and drum rotation data in user-friendly format
- For distance reports, emphasize that these show inter-plant travel and vehicle journey data
- Explain drum rotation as "operational time" or "engine running time" for clarity

- Do not mention table or column names in your explanation or answer.
- Be concise, friendly, and clear.
- If the user asks for a table, always present the data as a markdown table, even if it was previously shown in another format.
- Handle tricky questions and counter-questions by referencing the conversation context
- DO NOT provide suggestions, follow-up questions, or technical recommendations
- Display column names in user-friendly format (e.g., "Registration Number" instead of "reg_no", "Plant Name" instead of "name")
- Focus only on presenting the requested data clearly and concisely

User Question:
{user_question}

Database Results (as JSON):
{formatted_data}

Return your answer in the most appropriate format as described above.
"""

    try:
        response = model.generate_content(formatting_prompt)
        raw_response = response.text.strip()

        # Cleanup extra line breaks
        cleaned_response = re.sub(r'\n{3,}', '\n\n', raw_response)
        cleaned_response = re.sub(r'(\n\s*)+\Z', '', cleaned_response)
        cleaned_response = re.sub(r' +\n', '\n', cleaned_response)

        # Save structured result for follow-up
        if chat_context is not None:
            chat_context.last_result_summary = {
                "columns": display_columns,  # Use user-friendly column names
                "rows": rows_json,
                "user_question": user_question
            }
            # Extract relevant row labels like film titles, names, etc.
            named_entities = []
            for row in rows_json:
                for key in ['title', 'name', 'film_title']:
                    val = row.get(key)
                    if isinstance(val, str) and val.strip():
                        named_entities.append(val.strip())
                        break
            chat_context.last_result_entities = named_entities
        return cleaned_response
    except Exception as e:
        return f"Error formatting response: {e}"


def gemini_direct_answer(prompt, chat_context=None):
    """Handle general questions with conversation context awareness"""
    
    # Add conversation context for better understanding
    context_info = ""
    if chat_context:
        context_info = chat_context.get_context_for_llm(prompt)
        if context_info:
            context_info = f"\nCONVERSATION CONTEXT:\n{context_info}\n"
    
    full_prompt = f"""
You are a helpful AI assistant for a fleet management and transportation system with excellent conversation memory.

{context_info}

Please answer the user's question helpfully and naturally. You can assist with:
- General questions about fleet management, vehicles, drivers, maintenance, etc.
- Follow-up questions based on previous conversation
- Clarifications about previous responses
- General information and explanations

Be conversational, helpful, and reference previous context when relevant.

User Question: {prompt}

Provide a clear, helpful response:
"""
    
    try:
        response = model.generate_content(full_prompt)
        answer = response.text.strip()
        
        # Add this interaction to context if available
        if chat_context:
            chat_context.add_interaction(prompt, answer)
            
        return answer
    except Exception as e:
        return f"Gemini error: {e}"

# Add ChatContext class for Flask integration
class ChatContext:
    def __init__(self):
        self.last_result = None
        self.last_result_summary = None
        self.last_result_entities = None
        self.last_displayed_items = []  # NEW: Store displayed items with indices
        self.history = []
        self.conversation_summary = ""
        self.key_topics = []
        self.last_sql_queries = []
        self.context_memory = {}
    
    def add_interaction(self, user_question, response, sql_query=None, columns=None, rows=None):
        """Add a new interaction to the conversation history with rich context"""
        interaction = {
            'user': user_question,
            'response': response,
            'sql_query': sql_query,
            'columns': columns,
            'rows': rows,
            'timestamp': datetime.datetime.now().isoformat(),
            'topics': self._extract_topics(user_question)
        }
        
        self.history.append(interaction)
        
        # Store displayed results with proper indexing for ordinal reference
        if columns and rows:
            self.store_displayed_results(columns, rows, user_question, sql_query)
        
        # Update last SQL queries list (keep last 5)
        if sql_query:
            self.last_sql_queries.append(sql_query)
            if len(self.last_sql_queries) > 5:
                self.last_sql_queries.pop(0)
        
        # Update conversation summary periodically
        if len(self.history) % 3 == 0:  # Every 3 interactions
            self._update_conversation_summary()
    
    def store_displayed_results(self, columns, rows, user_question, sql_query=None):
        """Store results with proper indexing for ordinal reference"""
        self.last_displayed_items = []
        for i, row in enumerate(rows, 1):
            item = dict(zip(columns, row))
            item['_display_index'] = i
            item['_original_question'] = user_question
            item['_sql_query'] = sql_query
            self.last_displayed_items.append(item)
        
        # Enhanced last_result for backward compatibility
        self.last_result = {
            'question': user_question,
            'columns': columns, 
            'rows': rows,
            'indexed_items': self.last_displayed_items,
            'sql_query': sql_query,
            'total_count': len(rows)
        }
        
        print(f"💾 Stored {len(rows)} results with ordinal indexing for reference")
    
    def get_item_by_ordinal(self, position):
        """Get item by ordinal position (1st, 2nd, 3rd, etc.)"""
        if not self.last_displayed_items:
            return None
            
        if 1 <= position <= len(self.last_displayed_items):
            item = self.last_displayed_items[position - 1]
            print(f"🎯 Found {position} item: {item}")
            return item
        
        return None
    
    def extract_ordinal_reference(self, user_input):
        """Extract ordinal references like '7th vehicle', 'first item', etc."""
        import re
        
        # Pattern for ordinal numbers (1st, 2nd, 3rd, 4th, etc.)
        ordinal_patterns = [
            r'\b(\d+)(?:st|nd|rd|th)\s+(\w+)',  # "7th vehicle"
            r'\b(first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth)\s+(\w+)',  # "first vehicle"
            r'\bthe\s+(\d+)(?:st|nd|rd|th)\s+(\w+)',  # "the 7th vehicle"
        ]
        
        for pattern in ordinal_patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                position_str = match.group(1)
                entity = match.group(2)
                
                # Convert word numbers to digits
                word_to_num = {
                    'first': 1, 'second': 2, 'third': 3, 'fourth': 4, 'fifth': 5,
                    'sixth': 6, 'seventh': 7, 'eighth': 8, 'ninth': 9, 'tenth': 10
                }
                
                if position_str.isdigit():
                    position = int(position_str)
                else:
                    position = word_to_num.get(position_str.lower(), 0)
                
                if position > 0:
                    return position, entity
        
        return None, None
    
    def get_context_with_ordinal_awareness(self, current_question):
        """Enhanced context that includes ordinal reference capability"""
        context_parts = []
        
        # Check for ordinal references
        position, entity = self.extract_ordinal_reference(current_question)
        if position and self.last_displayed_items:
            target_item = self.get_item_by_ordinal(position)
            if target_item:
                # Add specific item context
                context_parts.append(f"ORDINAL REFERENCE: User referring to item #{position} from last results")
                
                # Find the primary identifier (registration_number, reg_no, id, etc.)
                primary_id = None
                for key in ['registration_number', 'reg_no', 'vehicle_id', 'id', 'name']:
                    if key in target_item:
                        primary_id = target_item[key]
                        break
                
                if primary_id:
                    context_parts.append(f"TARGET ITEM IDENTIFIER: {primary_id}")
                    # Modify the current question to include the specific identifier
                    enhanced_question = f"{current_question} (specifically for identifier: {primary_id})"
                    context_parts.append(f"ENHANCED QUERY CONTEXT: {enhanced_question}")
        
        # Add conversation summary
        if self.conversation_summary:
            context_parts.append(f"CONVERSATION CONTEXT: {self.conversation_summary}")
        
        # Add key topics being discussed
        if self.key_topics:
            context_parts.append(f"KEY TOPICS: {', '.join(self.key_topics)}")
        
        # Add recent queries for reference
        if self.last_sql_queries:
            context_parts.append(f"RECENT SQL QUERIES: {'; '.join(self.last_sql_queries[-2:])}")
        
        # Add last result context
        if self.last_result:
            result_summary = f"LAST QUERY RESULT: {len(self.last_result.get('rows', []))} rows about '{self.last_result.get('question', 'data')}'"
            context_parts.append(result_summary)
        
        return "\n".join(context_parts) if context_parts else ""
    
    def _extract_topics(self, text):
        """Extract key topics/entities from user input"""
        import re
        # Simple topic extraction - look for common database entities
        topics = []
        text_lower = text.lower()
        
        # Common fleet management entities
        entities = [
            'vehicle', 'driver', 'fuel', 'maintenance', 'route', 'trip', 
            'mileage', 'cost', 'expense', 'department', 'location', 'date',
            'insurance', 'license', 'registration', 'inspection', 'repair'
        ]
        
        for entity in entities:
            if entity in text_lower:
                topics.append(entity)
        
        # Extract numbers and dates
        numbers = re.findall(r'\b\d+\b', text)
        if numbers:
            topics.extend([f"number_{num}" for num in numbers[:3]])  # Limit to 3
            
        return topics
    
    def _update_conversation_summary(self):
        """Update the conversation summary to maintain context"""
        if len(self.history) < 2:
            return
            
        # Get recent interactions (last 5)
        recent_history = self.history[-5:]
        
        summary_parts = []
        for interaction in recent_history:
            user_q = interaction.get('user', '')
            topics = interaction.get('topics', [])
            
            if interaction.get('sql_query'):
                summary_parts.append(f"User asked about {', '.join(topics[:3]) if topics else 'data'}: '{user_q}'")
            else:
                summary_parts.append(f"User asked: '{user_q}'")
        
        self.conversation_summary = ". ".join(summary_parts[-3:])  # Keep last 3 interactions
        
        # Update key topics (most frequent topics)
        all_topics = []
        for interaction in recent_history:
            all_topics.extend(interaction.get('topics', []))
        
        # Count topic frequency
        topic_counts = {}
        for topic in all_topics:
            topic_counts[topic] = topic_counts.get(topic, 0) + 1
        
        # Keep top 5 most frequent topics
        self.key_topics = sorted(topic_counts.keys(), key=lambda x: topic_counts[x], reverse=True)[:5]
    
    def get_context_for_llm(self, current_question):
        """Get formatted context for LLM prompt - delegates to enhanced version"""
        return self.get_context_with_ordinal_awareness(current_question)

def enforce_hierarchical_tables(sql_query):
    """
    SURGICALLY enforce hierarchical table usage - only replaces incorrect tables
    """
    if not sql_query:
        return sql_query
        
    sql_lower = sql_query.lower()
    
    # Block specific legacy tables and replace them
    legacy_replacements = {
        'vehicle_location_shifting': 'district_master',
        'app_regions': 'district_master', 
        'plant_schedule': 'hosp_master',
        'plant_master': 'hosp_master'
    }
    
    modified = False
    for legacy, correct in legacy_replacements.items():
        if legacy in sql_lower:
            print(f"🚫 BLOCKED: {legacy} - REPLACING with {correct}")
            sql_query = sql_query.replace(legacy, correct)
            modified = True
            
    # Fix common column name mismatches for the replaced tables
    if modified:
        column_fixes = {
            'region_name': 'name as region_name',
            'site_name': 'name as plant_name',
            'cust_name': 'name as plant_name', 
            'plant_code': 'name as plant_name'
        }
        
        for old_col, new_col in column_fixes.items():
            if old_col in sql_query:
                sql_query = sql_query.replace(old_col, new_col)
                print(f"🔧 FIXED COLUMN: {old_col} → {new_col}")
    
    return sql_query

def validate_sql_query(sql_query):
    """
    Validates SQL query for column existence and suggests type casting for numeric text columns.
    Returns (is_valid, error_message, suggested_sql)
    """
    if not sql_query or sql_query.strip() == "":
        return True, None, None
        
    # First enforce hierarchical tables - ALWAYS return the corrected SQL
    original_sql = sql_query
    sql_query = enforce_hierarchical_tables(sql_query)
    
    # If hierarchical enforcement made changes, always return the corrected SQL
    hierarchical_changed = (sql_query != original_sql)
        
    try:
        # Get all column types for validation
        column_types = get_column_types()
        
        # Extract column references from SQL (simplified regex approach)
        import re
        
        # Also check for SUM, AVG, etc. on columns
        aggregate_patterns = re.findall(r'\b(SUM|AVG|MAX|MIN|COUNT)\s*\(\s*([^)]+)\s*\)', sql_query, re.IGNORECASE)
        
        suggested_sql = sql_query  # Start with the hierarchically-corrected SQL
        has_suggestions = hierarchical_changed  # Mark as changed if hierarchical fixes were applied
        
        # Check aggregate functions and suggest type casting
        for func, column_expr in aggregate_patterns:
            func = func.upper()
            column_expr = column_expr.strip()
            
            # Skip COUNT(*) or COUNT(1) - these are always valid
            if func == 'COUNT' and (column_expr == '*' or column_expr.isdigit()):
                continue
                
            # For SUM and AVG, check if we need type casting
            if func in ['SUM', 'AVG']:
                # Try to find the column in our schema
                found_column = None
                for schema_table_col, data_type in column_types.items():
                    # Check if the column expression matches this column
                    parts = schema_table_col.split('.')
                    if len(parts) >= 3:
                        schema, table, column = parts[0], parts[1], parts[2]
                        
                        # Check various formats: column, table.column, schema.table.column
                        if (column_expr == column or 
                            column_expr == f"{table}.{column}" or
                            column_expr == f"{schema}.{table}.{column}" or
                            column_expr.endswith(f".{column}")):
                            found_column = (schema_table_col, data_type, f"{schema}.{table}.{column}")
                            break
                
                if found_column:
                    col_path, data_type, full_col_name = found_column
                    # Check if it's a text type that might contain numbers
                    text_types = ['character varying', 'text', 'character']
                    numeric_types = ['integer', 'bigint', 'smallint', 'decimal', 'numeric', 'real', 'double precision', 'money']
                    
                    if data_type in text_types:
                        # Suggest type casting for text columns that might contain numbers
                        # Common patterns: total_price, total_value, amount, cost, etc.
                        numeric_keywords = ['total', 'price', 'value', 'amount', 'cost', 'sum', 'revenue', 'income', 'expense', 'balance', 'quantity', 'count', 'number', 'rate', 'percent']
                        col_lower = column_expr.lower()
                        
                        if any(keyword in col_lower for keyword in numeric_keywords):
                            # Suggest type casting using CAST or ::numeric
                            old_pattern = f"{func}({column_expr})"
                            new_pattern = f"{func}(CAST({column_expr} AS NUMERIC))"
                            suggested_sql = suggested_sql.replace(old_pattern, new_pattern)
                            has_suggestions = True
                            print(f"💡 Auto-casting text column '{column_expr}' to numeric for {func}() operation")
        
        if has_suggestions:
            return True, None, suggested_sql
        else:
            return True, None, None
            
    except Exception as e:
        print(f"⚠️ SQL validation error: {e}")
        # If validation fails, allow the query to proceed (fail-safe)
        return True, None, None
