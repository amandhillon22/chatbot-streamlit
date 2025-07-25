import google.generativeai as genai
import os
import json
import re
from dotenv import load_dotenv
import datetime
from decimal import Decimal
from sql import get_full_schema, get_column_types, get_numeric_columns

# Import embeddings functionality
try:
    from create_lightweight_embeddings import LightweightEmbeddingManager
    from enhanced_table_mapper import EnhancedTableMapper
    EMBEDDINGS_AVAILABLE = True
except ImportError:
    EMBEDDINGS_AVAILABLE = False

# Import distance unit conversion functionality
try:
    from distance_units import get_distance_conversion_info, get_distance_columns_info
    DISTANCE_CONVERSION_AVAILABLE = True
    print("✅ Distance unit conversion system loaded successfully")
except ImportError as e:
    print(f"⚠️ Distance unit conversion not available: {e}")
    DISTANCE_CONVERSION_AVAILABLE = False

def initialize_embeddings():
    """Initialize the lightweight embedding manager"""
    try:
        if os.path.exists('embeddings_cache.pkl'):
            import pickle
            with open('embeddings_cache.pkl', 'rb') as f:
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
    from intelligent_reasoning import IntelligentReasoning
    intelligent_reasoning = IntelligentReasoning()
    print("✅ Intelligent reasoning initialized")
except ImportError as e:
    print(f"⚠️ Intelligent reasoning not available: {e}")
    intelligent_reasoning = None

# Import enhanced pronoun resolver
try:
    from enhanced_pronoun_resolver import EnhancedPronounResolver
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
            return json.loads(match.group())
        return {}
    except json.JSONDecodeError:
        return {}

def english_to_sql(prompt, chat_context=None):
    # 🎯 ENHANCED PRONOUN RESOLUTION CHECK
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
    
    # 🧠 INTELLIGENT CONTEXTUAL REASONING CHECK
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
                
                return {
                    "sql": intelligent_sql,
                    "response": intelligent_response,
                    "follow_up": None,
                    "reasoning_applied": True,
                    "reasoning_type": reasoning_result['reasoning_type']
                }
    
    # Continue with existing logic if no intelligent reasoning needed
    if re.search(r'\b(format|clean|style|tabular|bullets|rewrite|shorter|rephrase|reword|simplify|again|visual|text-based|in text|as table|re-display)\b', prompt, re.IGNORECASE):
        last_data = chat_context.last_result if chat_context else None
        if not last_data:
            return {
                "sql": None,
                "follow_up": None,
                "force_format_response": "I'm sorry, I can't reformat because there is no recent data available. Can you please restate your original question?"
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

    # Get enhanced conversation context with ordinal reference handling
    context_info = ""
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

🎯 **PLANT QUERY EXAMPLES:**
- "Show all plants" → SELECT hm.name, hm.id_no FROM hosp_master hm WHERE hm.name IS NOT NULL
- "Plant name for ID 460" → SELECT hm.name, hm.address FROM hosp_master hm WHERE hm.id_no = 460
- "Plants in Punjab" → SELECT hm.name FROM hosp_master hm JOIN district_master dm ON hm.id_dist = dm.id_no WHERE dm.name ILIKE '%Punjab%'
- "Vehicles in Mohali plant" → SELECT vm.reg_no FROM vehicle_master vm JOIN hosp_master hm ON vm.id_hosp = hm.id_no WHERE hm.name ILIKE '%mohali%'

🚛 **VEHICLES OF PLANT QUERIES - CRITICAL:**
- "Vehicles of Mohali plant" → SELECT vm.reg_no FROM vehicle_master vm JOIN hosp_master hm ON vm.id_hosp = hm.id_no WHERE hm.name ILIKE '%mohali%'
- "Show vehicles of [plant name]" → SELECT vm.reg_no, vm.bus_id FROM vehicle_master vm JOIN hosp_master hm ON vm.id_hosp = hm.id_no WHERE hm.name ILIKE '%[plant name]%'
- "Vehicles in plant ID X" → SELECT vm.reg_no FROM vehicle_master vm WHERE vm.id_hosp = X

⚠️ **CRITICAL**: When user asks for "vehicles of [plant name]", ALWAYS:
1. Use vehicle_master table for vehicles
2. JOIN with hosp_master to find plant by name
3. Use ILIKE '%plant_name%' for flexible name matching
4. Show reg_no (registration number) as primary vehicle identifier
5. **REMEMBER**: hosp_master = plant data, NOT medical data

❌ **NEVER USE**: plant_schedule, plant_master, or any other table for plant data
❌ **NEVER ASSUME**: hosp_master contains medical data - it's PLANT data!
"""
    else:
        plant_guidance = ""

    # 🚀 CRITICAL ID RELATIONSHIP ENFORCEMENT
    id_relationship_guide = """
🔗 **MANDATORY ID RELATIONSHIPS - NEVER MISS THESE:**

**CORE HIERARCHICAL CHAIN (ALWAYS USE THESE EXACT JOINS):**
zone_master.id_no ← district_master.id_zone ← hosp_master.id_dist ← vehicle_master.id_hosp

**EXACT JOIN SYNTAX:**
```sql
-- Complete hierarchy from vehicle to zone:
FROM vehicle_master vm
LEFT JOIN hosp_master hm ON vm.id_hosp = hm.id_no        -- CRITICAL: id_hosp relationship
LEFT JOIN district_master dm ON hm.id_dist = dm.id_no    -- CRITICAL: id_dist relationship  
LEFT JOIN zone_master zm ON dm.id_zone = zm.id_no        -- CRITICAL: id_zone relationship
```

🔑 **CRITICAL COLUMN NAMES - USE EXACTLY THESE:**
- **zone_master**: Use `zone_name` (NOT `name`)
- **district_master**: Use `name` (for region names) 
- **hosp_master**: Use `name` (for plant names)
- **vehicle_master**: Use `reg_no` (for registration numbers)

🎯 **SMART LOCATION DETECTION - CRITICAL LOGIC:**
When user mentions a location (e.g., "Gujarat", "Maharashtra", "West Bengal"):
1. **FIRST**: Check if it's a DISTRICT/STATE name → Use district_master.name
2. **SECOND**: Only if not found, check if it's a ZONE name → Use zone_master.zone_name
3. **AVOID**: Unnecessary joins to zone_master if the location is actually a district

**LOCATION QUERY EXAMPLES:**
```sql
-- For "Plants in Gujarat" - Check district first:
SELECT hm.name 
FROM hosp_master hm 
JOIN district_master dm ON hm.id_dist = dm.id_no 
WHERE dm.name ILIKE '%Gujarat%'

-- Only use zone_master if specifically asking for zone or if district search fails:
SELECT hm.name 
FROM hosp_master hm 
JOIN district_master dm ON hm.id_dist = dm.id_no 
JOIN zone_master zm ON dm.id_zone = zm.id_no 
WHERE zm.zone_name ILIKE '%Gujarat%'
```

⚠️ **MANDATORY RULES:**
1. **vehicle_master.id_hosp** MUST link to **hosp_master.id_no**
2. **hosp_master.id_dist** MUST link to **district_master.id_no**
3. **district_master.id_zone** MUST link to **zone_master.id_no**
4. NEVER skip these relationships - they ensure complete data integrity
5. ALWAYS use correct column names: zm.zone_name, dm.name, hm.name, vm.reg_no
6. **SMART LOCATION**: Start with district_master for location names, only use zone_master when needed

**COMMON QUERY PATTERNS:**
- Vehicle → Plant: JOIN hosp_master hm ON vm.id_hosp = hm.id_no
- Plant → Region: JOIN district_master dm ON hm.id_dist = dm.id_no
- Region → Zone: JOIN zone_master zm ON dm.id_zone = zm.id_no
- Vehicle → Full Hierarchy: Use all three joins above

**EXAMPLE: Plants in a Location (SMART DETECTION)**
```sql
-- PREFERRED: Try district_master first (most locations are districts/states)
SELECT hm.name 
FROM hosp_master hm 
JOIN district_master dm ON hm.id_dist = dm.id_no 
WHERE dm.name ILIKE '%Gujarat%'

-- FALLBACK: Only if district fails, try zone_master
SELECT hm.name 
FROM hosp_master hm 
JOIN district_master dm ON hm.id_dist = dm.id_no 
JOIN zone_master zm ON dm.id_zone = zm.id_no 
WHERE zm.zone_name ILIKE '%Gujarat%'
```

⚠️ **CRITICAL**: If asking for vehicles of a plant/region/zone, ALWAYS include the complete join chain to ensure NO vehicles are missed!
"""

    # 🚀 ABSOLUTE HIERARCHICAL ENFORCEMENT
    hierarchy_guidance = ""
    
    # Zone queries - ONLY zone_master
    if re.search(r'\b(zone)\b', prompt, re.IGNORECASE):
        hierarchy_guidance += """
🌐 **ZONE QUERIES - ABSOLUTE RULE:**
⚠️ **CRITICAL**: ALWAYS and ONLY use zone_master table for zone queries
❌ **NEVER USE**: Any other table for zone data
🔑 **ZONE COLUMN NAME**: Use `zone_name` NOT `name` for zone_master table

Examples:
- "Show all zones" → SELECT DISTINCT zone_name FROM zone_master WHERE zone_name IS NOT NULL
- "What zone does vehicle X belong to?" → 
  SELECT zm.zone_name FROM zone_master zm 
  JOIN district_master dm ON zm.id_no = dm.id_zone 
  JOIN hosp_master hm ON dm.id_no = hm.id_dist 
  JOIN vehicle_master vm ON hm.id_no = vm.id_hosp 
  WHERE vm.reg_no = 'X'
- "Plants in Gujarat zone" → 
  SELECT hm.name FROM hosp_master hm 
  JOIN district_master dm ON hm.id_dist = dm.id_no 
  JOIN zone_master zm ON dm.id_zone = zm.id_no 
  WHERE zm.zone_name = 'Gujarat'
"""

    # Region/District queries - Smart location detection
    if re.search(r'\b(region|district|state|gujarat|maharashtra|bengal|punjab|haryana|rajasthan|karnataka|tamil|andhra|kerala|odisha|bihar|uttar|madhya|jharkhand|chhattisgarh|assam|himachal|uttarakhand|goa|tripura|meghalaya|manipur|nagaland|mizoram|arunachal|sikkim|delhi|mumbai|bangalore|chennai|kolkata|hyderabad|pune|ahmedabad|surat|jaipur|lucknow|kanpur|bhopal|indore|agra|patna|vadodara|coimbatore|ludhiana|kochi|visakhapatnam|nashik|meerut|aurangabad|ranchi|howrah|gwalior|jabalpur|vijayawada|jodhpur|madurai|raipur|kota|chandigarh|guwahati|solapur|hubli|tiruchirappalli|belgaum|bhubaneswar|thiruvananthapuram)\b', prompt, re.IGNORECASE):
        hierarchy_guidance += """
🏢 **REGION/DISTRICT/STATE QUERIES - SMART APPROACH:**
⚠️ **CRITICAL**: For location names (Gujarat, Maharashtra, etc.), FIRST try district_master
🎯 **SMART DETECTION**: Most Indian state/region names are in district_master.name, NOT zone_master
❌ **DON'T**: Automatically use zone_master for all geographic queries

🔑 **LOCATION QUERY LOGIC:**
1. **PRIMARY**: Use district_master.name for state/region/district names
2. **SECONDARY**: Only use zone_master.zone_name if specifically asking for zones

Examples:
- "Plants in Gujarat" → SELECT hm.name FROM hosp_master hm JOIN district_master dm ON hm.id_dist = dm.id_no WHERE dm.name ILIKE '%Gujarat%'
- "Vehicles in Maharashtra" → SELECT vm.reg_no FROM vehicle_master vm JOIN hosp_master hm ON vm.id_hosp = hm.id_no JOIN district_master dm ON hm.id_dist = dm.id_no WHERE dm.name ILIKE '%Maharashtra%'
- "Show all regions" → SELECT DISTINCT name FROM district_master WHERE name IS NOT NULL
- "What region does vehicle X belong to?" → SELECT dm.name as region_name FROM district_master dm JOIN hosp_master hm ON dm.id_no = hm.id_dist JOIN vehicle_master vm ON hm.id_no = vm.id_hosp WHERE vm.reg_no = 'X'

⚠️ **CRITICAL**: States like Gujarat, Maharashtra, West Bengal are typically in district_master.name, not zone_master.zone_name
"""

    # Plant/Facility queries - ONLY hosp_master
    if re.search(r'\b(plant|facility)\b', prompt, re.IGNORECASE):
        hierarchy_guidance += """
🏭 **PLANT QUERIES - ABSOLUTE RULE:**
⚠️ **CRITICAL**: ALWAYS and ONLY use hosp_master table for plant queries
⚠️ **IMPORTANT**: hosp_master contains PLANT DATA, not medical data!
❌ **NEVER USE**: plant_schedule, plant_master, or any other table for plant data
🔑 **PLANT COLUMN NAME**: Use `name` (NOT `plant_name`) for hosp_master table

Examples:
- "Show all plants" → SELECT DISTINCT name FROM hosp_master WHERE name IS NOT NULL
- "What plant does vehicle X belong to?" → 
  SELECT hm.name as plant_name FROM hosp_master hm 
  JOIN vehicle_master vm ON hm.id_no = vm.id_hosp 
  WHERE vm.reg_no = 'X'
- "Plants in Punjab region" →
  SELECT hm.name FROM hosp_master hm 
  JOIN district_master dm ON hm.id_dist = dm.id_no 
  WHERE dm.name ILIKE '%Punjab%'
- "Vehicles in Mohali plant" →
  SELECT vm.reg_no FROM vehicle_master vm 
  JOIN hosp_master hm ON vm.id_hosp = hm.id_no 
  WHERE hm.name ILIKE '%Mohali%'

🔑 **REMEMBER**: hosp_master = PLANT/FACTORY data (NOT medical facilities)
"""

    # Vehicle hierarchy queries - ONLY vehicle_master
    if re.search(r'\b(vehicle|truck|fleet)\b', prompt, re.IGNORECASE):
        hierarchy_guidance += """
🚛 **VEHICLE QUERIES - ABSOLUTE RULE:**
⚠️ **CRITICAL**: ALWAYS and ONLY use vehicle_master table for vehicle queries
❌ **NEVER USE**: mega_trips, drv_veh_qr_assign, or any other table for vehicle data unless specifically joining

Examples:
- "Show all vehicles" → SELECT DISTINCT reg_no FROM vehicle_master WHERE reg_no IS NOT NULL
- "Show vehicle X with full hierarchy" → 
  SELECT vm.reg_no, hm.name as plant, dm.name as district, zm.zone_name 
  FROM vehicle_master vm 
  LEFT JOIN hosp_master hm ON vm.id_hosp = hm.id_no 
  LEFT JOIN district_master dm ON hm.id_dist = dm.id_no 
  LEFT JOIN zone_master zm ON dm.id_zone = zm.id_no 
  WHERE vm.reg_no = 'X'
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
- **NEVER** assume hosp_master contains medical information

{id_relationship_guide}

{distance_info}

{context_info}

{plant_guidance}

{hierarchy_guidance}

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

- **Do not return actual DB results.**
- **Return only a valid JSON object — no markdown or commentary outside the JSON.**
- **SQL must always use schema-qualified table names.**
- **Never use unqualified table or column names.**
- **CRITICAL: ONLY use columns that are explicitly listed in the schema above. If a column is not listed, DO NOT use it.**
- **CRITICAL: Before generating any SQL, verify that ALL columns referenced exist in the provided schema.**
- **If you need a column that doesn't exist, return an error in the 'response' field explaining the limitation.**
- **For potentially large datasets, always add LIMIT 50 to prevent performance issues.**
- **If user asks for "all" records from large tables, suggest aggregations instead.**
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
    rows_json = []
    for r in rows:
        row_dict = {}
        for col, val in zip(columns, r):
            if isinstance(val, datetime.timedelta):
                days = val.days
                hours = val.seconds // 3600
                minutes = (val.seconds % 3600) // 60
                text = f"{days} days"
                if hours:
                    text += f", {hours} hours"
                if minutes:
                    text += f", {minutes} minutes"
                row_dict[col] = text
            elif isinstance(val, (datetime.datetime, datetime.date)):
                row_dict[col] = val.isoformat()
            elif isinstance(val, (float, Decimal)):
                row_dict[col] = round(float(val), 2)
            else:
                row_dict[col] = val
        rows_json.append(row_dict)

    formatted_data = json.dumps(rows_json, separators=(',', ':'))

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
- Suggest alternative queries when appropriate (e.g., "Would you like to see other available information about this vehicle?")
- Do not mention table or column names in your explanation or answer.
- Be concise, friendly, and clear.
- If the user asks for a table, always present the data as a markdown table, even if it was previously shown in another format.
- Handle tricky questions and counter-questions by referencing the conversation context

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
                "columns": columns,
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
