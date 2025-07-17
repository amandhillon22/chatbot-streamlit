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
    
    EMBEDDINGS_AVAILABLE = True
    print("✅ Lightweight embeddings module loaded successfully")
except ImportError as e:
    print(f"⚠️ Embeddings not available: {e}")
    EMBEDDINGS_AVAILABLE = False

# Initialize enhanced table mapper
try:
    enhanced_table_mapper = EnhancedTableMapper()
    print("✅ Enhanced table mapper initialized")
except Exception as e:
    print(f"⚠️ Enhanced table mapper not available: {e}")
    enhanced_table_mapper = None

# Import intelligent reasoning
try:
    from intelligent_reasoning import IntelligentReasoning
    intelligent_reasoning = IntelligentReasoning()
    print("✅ Intelligent reasoning initialized")
except ImportError as e:
    print(f"⚠️ Intelligent reasoning not available: {e}")
    intelligent_reasoning = None

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

    # 🏭 ENHANCED PLANT-VEHICLE QUERY HANDLING
    if re.search(r'\b(plant|site|customer|location)\b', prompt, re.IGNORECASE):
        plant_guidance = """
🏭 **PLANT-VEHICLE RELATIONSHIP GUIDANCE:**
For plant/site/customer queries related to vehicles:
1. Use JOIN between mega_trips and plant_schedule tables
2. mega_trips.plant_id = plant_schedule.plant_id (both are integers)
3. Available plant fields: plant_code, cust_name, site_name, fse_name, etc.
4. NEVER use vehicle registration number as plant_id

Examples:
- "What plant does vehicle X belong to?" → SELECT ps.plant_code, ps.cust_name FROM mega_trips mt JOIN plant_schedule ps ON mt.plant_id = ps.plant_id WHERE mt.reg_no = 'X'
- "Tell me about the plant for the 7th vehicle" → Use ordinal reference to get vehicle reg_no, then JOIN
"""
    else:
        plant_guidance = ""

    # 🚀 ENHANCED REGION QUERY HANDLING
    if re.search(r'\b(region|location|area|zone)\b', prompt, re.IGNORECASE):
        # For region queries, prioritize vehicle_master.regional_name first, then vehicle_location_shifting.region
        region_guidance = """
🌍 **REGION DATA GUIDANCE:**
For region/location queries:
1. PRIMARY SOURCE: Use vehicle_master.regional_name (available for most vehicles)
2. SECONDARY SOURCE: Use vehicle_location_shifting.region (limited data)
3. ALWAYS prefer vehicle_master table for region information unless specifically asking about location shifting

Examples:
- "What region does vehicle X belong to?" → SELECT regional_name FROM vehicle_master WHERE reg_no = 'X'
- "Show all vehicles and their regions" → SELECT reg_no, regional_name FROM vehicle_master WHERE regional_name IS NOT NULL
"""
    else:
        region_guidance = ""

    # 🚀 ENHANCED EMBEDDING PROCESSING with Advanced Table Mapping
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
                print(f"📊 Using embeddings only: {len(embedding_results)} tables")
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
                            reason = "embedding"
                        
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

    full_prompt = f"""
You are an intelligent SQL assistant for multiple PostgreSQL schemas with advanced conversation memory.

{schema_text}

{context_info}

{plant_guidance}

{region_guidance}

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

{schema_text}

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
- **STEP 3**: **CRITICAL: NEVER use SUM() or AVG() on TEXT columns** (marked as TEXT in schema).
- **STEP 4**: Only use SUM() or AVG() on NUMERIC columns (marked as NUMERIC in schema).
- **STEP 5**: If you need to join tables, ensure the join columns exist in BOTH tables.
- **STEP 6**: If a user asks for data that requires non-existent columns, explain the limitation.

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

def validate_sql_query(sql_query):
    """
    Validates SQL query for column existence and suggests type casting for numeric text columns.
    Returns (is_valid, error_message, suggested_sql)
    """
    if not sql_query or sql_query.strip() == "":
        return True, None, None
        
    try:
        # Get all column types for validation
        column_types = get_column_types()
        
        # Extract column references from SQL (simplified regex approach)
        import re
        
        # Also check for SUM, AVG, etc. on columns
        aggregate_patterns = re.findall(r'\b(SUM|AVG|MAX|MIN|COUNT)\s*\(\s*([^)]+)\s*\)', sql_query, re.IGNORECASE)
        
        suggested_sql = sql_query
        has_suggestions = False
        
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
