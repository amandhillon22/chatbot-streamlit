import google.generativeai as genai
import os
import json
import re
import sys
sys.path.append('/home/linux/Documents/chatbot-diya')

from dotenv import load_dotenv
import datetime
from decimal import Decimal
from src.core.sql import get_full_schema

# Import embeddings functionality
try:
    from src.nlp.sentence_embeddings import sentence_embedding_manager, initialize_sentence_embeddings
    EMBEDDINGS_AVAILABLE = True
    print("✅ Sentence transformer embeddings module loaded successfully")
except ImportError as e:
    print(f"⚠️ Sentence transformer embeddings not available: {e}")
    EMBEDDINGS_AVAILABLE = False

# Import distance unit conversion functionality
try:
    from src.database.distance_units import get_distance_conversion_info, get_distance_columns_info
    DISTANCE_CONVERSION_AVAILABLE = True
    print("✅ Distance unit conversion system loaded successfully")
except ImportError as e:
    print(f"⚠️ Distance unit conversion not available: {e}")
    DISTANCE_CONVERSION_AVAILABLE = False

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

def schema_dict_to_prompt(schema_dict):
    """
    Converts the schema dictionary to a readable string for LLM prompt.
    """
    lines = []
    for schema_name, tables in schema_dict.items():
        lines.append(f"Schema: {schema_name}")
        for table, columns in tables.items():
            lines.append(f"- {schema_name}.{table}({', '.join(columns)})")
    return '\n'.join(lines)

# Dynamically fetch schema at import time
SCHEMA_DICT = get_full_schema()
SCHEMA_PROMPT = schema_dict_to_prompt(SCHEMA_DICT)

# Initialize embeddings if available
if EMBEDDINGS_AVAILABLE:
    try:
        embedding_manager = initialize_sentence_embeddings()
        print("🚀 Sentence transformer embeddings system initialized")
    except Exception as e:
        print(f"⚠️ Failed to initialize sentence transformer embeddings: {e}")
        EMBEDDINGS_AVAILABLE = False

# Import enhanced pronoun resolver
try:
    from src.nlp.enhanced_pronoun_resolver import EnhancedPronounResolver
    pronoun_resolver = EnhancedPronounResolver()
    print("✅ Enhanced pronoun resolver initialized")
except ImportError as e:
    print(f"⚠️ Enhanced pronoun resolver not available: {e}")
    pronoun_resolver = None

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

    # 🚀 SENTENCE TRANSFORMER EMBEDDING-ENHANCED PROCESSING
    relevant_schema_text = SCHEMA_PROMPT  # Default fallback
    
    if EMBEDDINGS_AVAILABLE and embedding_manager:
        try:
            # Check for similar previous queries first
            similar_query = embedding_manager.find_similar_query(prompt)
            if similar_query:
                print(f"🎯 Found similar query pattern: {similar_query['query'][:50]}...")
                print(f"    Similarity: {similar_query.get('similarity', 0):.3f}")
                # Could return the similar SQL with modifications, but for now, continue with normal flow
            
            # Find most relevant tables for this query using sentence transformers
            relevant_tables = embedding_manager.find_relevant_tables(prompt, top_k=8)
            
            if relevant_tables:
                print(f"📊 Using sentence transformer embeddings: Found {len(relevant_tables)} relevant tables")
                
                # Build focused schema text with only relevant tables
                focused_schema = []
                for table_key, similarity, description in relevant_tables:
                    schema_name, table_name = table_key.split('.', 1)
                    if schema_name in SCHEMA_DICT and table_name in SCHEMA_DICT[schema_name]:
                        columns = SCHEMA_DICT[schema_name][table_name]
                        focused_schema.append(f"- {table_key}({', '.join(columns)}) # {description[:100]}")
                        print(f"  • {table_key} (relevance: {similarity:.3f})")
                
                if focused_schema:
                    relevant_schema_text = "Relevant tables for your query (selected using sentence transformer embeddings):\n" + "\n".join(focused_schema)
                    
        except Exception as e:
            print(f"⚠️ Sentence transformer embedding error: {e}, falling back to full schema")

    history_text = ""
    if chat_context:
        for entry in reversed(chat_context.history):
            history_text += f"User: {entry['user']}\nBot: {entry.get('response', '')}\n"

    # Get distance conversion information
    distance_info = ""
    if DISTANCE_CONVERSION_AVAILABLE:
        try:
            distance_info = get_distance_conversion_info()
        except Exception as e:
            print(f"⚠️ Error getting distance conversion info: {e}")
            distance_info = ""

    full_prompt = f"""
You are an intelligent SQL assistant for multiple PostgreSQL schemas.

{relevant_schema_text}

{distance_info}

Always use PostgreSQL-compatible datetime functions like EXTRACT(), DATE_TRUNC(), and TO_CHAR() instead of SQLite functions like strftime().

Your task:
1. Analyze the user's question.
2. Identify which schema it belongs to.
3. Use the MOST RELEVANT tables shown above (they are pre-selected for this query).
4. Return ONLY a JSON with:
   - schema
   - sql
   - response (a *placeholder* natural language answer for user)
   - follow_up (suggested question or null)

🔁 **Handling Follow-up Questions and Contextual Scope**

If the user asks a question that appears to follow from a previous result, list, or subset (e.g., "these 10 vehicles", "that result", "total distance covered"), you **must determine the correct scope**.

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
  - A user-provided group (e.g., "top 5 most used vehicles")
  - Any manually listed items (e.g., reg_nos just displayed)

---

❗ Strict instructions:

- **Do not return actual DB results.**
- **Return only a valid JSON object — no markdown or commentary outside the JSON.**
- **SQL must always use schema-qualified table names.**
- **Never use unqualified table or column names.**
- **For potentially large datasets, always add LIMIT 50 to prevent performance issues.**
- **If user asks for "all" records from large tables, suggest aggregations instead.**
- **PRIORITIZE the tables shown above - they are the most relevant for this query.**
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

🚩 **DISTANCE UNIT CONVERSION - CRITICAL INSTRUCTIONS**:

**⚠️ IMPORTANT**: Most distance columns in this database store values in METERS by default. When users ask for distances in kilometers, you MUST convert them.

**Auto-Detection Rules**:
1. When user mentions "km", "kilometers", "kilometer" → Convert meters to km using: `ROUND((column_name::NUMERIC / 1000), 2)`
2. When user mentions "meters", "metres", "m" → Use raw values if already in meters
3. For vehicle mileage/odometer → Usually already in kilometers

**Conversion SQL Examples**:
- User asks: "total distance in km" → Use: `ROUND((distance_column::NUMERIC / 1000), 2) AS distance_km`
- User asks: "show mileage" → Use column as-is (usually already km)
- User asks: "distance in meters" → Use raw column if stored in meters

**Smart Response**: Always mention the conversion in your response.
- ✅ "Here's the total distance in kilometers (converted from meters):"
- ✅ "Vehicle mileage is already stored in kilometers:"
- ✅ "Distance values converted from meters to kilometers as requested:"

---

🏭 **PLANT & HIERARCHY QUERY GUIDANCE - CRITICAL:**

**⚠️ STRICT RULES - ALWAYS FOLLOW:**

**For PLANT queries:**
- **ALWAYS use `hosp_master` table** for plant data
- **Plant ID**: `hm.id_no`
- **Plant Name**: `hm.name` (NOT plant_code)
- **Plant Address**: `hm.address`
- **Region Link**: `hm.id_dist` (connects to district_master)

**For REGION queries:**
- **ALWAYS use `district_master` table** for regions
- **Region Name**: `dm.name`
- **Zone Link**: `dm.id_zone` (connects to zone_master)

**For ZONE queries:**
- **ALWAYS use `zone_master` table** for zones
- **Zone Name**: `zm.zone_name`

**HIERARCHY SQL Examples:**
```sql
-- Plants in Punjab region:
SELECT hm.name as plant_name, hm.address 
FROM hosp_master hm 
JOIN district_master dm ON hm.id_dist = dm.id_no 
WHERE dm.name ILIKE '%punjab%' 
LIMIT 50;

-- Plant for specific ID:
SELECT hm.name, hm.address 
FROM hosp_master hm 
WHERE hm.id_no = 460;

-- All plants:
SELECT hm.name, hm.id_no, hm.address 
FROM hosp_master hm 
WHERE hm.name IS NOT NULL 
LIMIT 50;
```

**❌ NEVER USE:**
- `plant_schedule`, `plant_master` for plant data
- `vehicle_location_shifting` for region data
- Always use the hierarchical tables listed above

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

{{
  "schema": "schema_name or null",
  "sql": "SQL query string or null",
  "response": "Short natural-language placeholder answer (e.g. 'Sure, let me get that for you.')",
  "follow_up": "suggested helpful follow-up question"
}}

Conversation so far:
{history_text}
User: {prompt}
"""

    try:
        response = model.generate_content(full_prompt).text
        result = extract_json(response)
        
        # Store successful query patterns for future use with sentence transformers
        if EMBEDDINGS_AVAILABLE and embedding_manager and result.get("sql"):
            try:
                embedding_manager.add_query_pattern(prompt, result["sql"], success=True)
            except Exception as e:
                print(f"⚠️ Failed to store query pattern in sentence transformer embeddings: {e}")
        
        return result
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

    formatting_prompt = f"""
You are a helpful assistant. Given the user's question and the database results in JSON, generate the most natural, clear, and helpful answer for the user.

Instructions:
- If the user asks to reformat, summarize, or present the previous data in a different way (such as 'show as table', 'show as list', 'summarize', etc.), always use the most recent data/results available, not just the new user question.
- If the answer can be given in natural language, do so.
- Only use a markdown table if it is truly necessary for clarity (e.g., multiple rows or columns that cannot be summarized naturally).
- If the answer is a single value or can be summarized in a sentence, prefer natural language.
- If there is no data, politely state that no relevant data was found.
- Do not mention table or column names in your explanation or answer.
- Be concise, friendly, and clear.
- If the user asks for a table, always present the data as a markdown table, even if it was previously shown in another format.

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
        # If chat_context is a list (from streamlit session state)
        if isinstance(chat_context, list):
            recent_history = []
            for entry in chat_context[-3:]:  # Last 3 interactions
                recent_history.append(f"User: {entry.get('user', '')}")
                recent_history.append(f"Bot: {entry.get('response', '')}")
            context_info = f"\nCONVERSATION CONTEXT:\n" + "\n".join(recent_history) + "\n"
    
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
        return answer
    except Exception as e:
        return f"I'm sorry, I encountered an error: {e}"

def validate_sql_query(sql_query):
    """
    Simple validation for SQL query - enhanced version just validates basic structure.
    Returns (is_valid, error_message, suggested_sql)
    """
    if not sql_query or sql_query.strip() == "":
        return True, None, None
    
    # Basic SQL structure validation
    sql_lower = sql_query.lower().strip()
    
    # Check for dangerous operations
    dangerous_keywords = ['drop', 'delete', 'truncate', 'alter', 'create', 'insert', 'update']
    if any(keyword in sql_lower for keyword in dangerous_keywords):
        return False, "Query contains potentially dangerous operations", None
    
    # Must start with SELECT
    if not sql_lower.startswith('select'):
        return False, "Query must start with SELECT", None
    
    return True, None, None

# Add ChatContext class for Flask integration
class ChatContext:
    def __init__(self):
        self.last_result = None
        self.last_result_summary = None
        self.last_result_entities = None
        self.last_displayed_items = None
        self.history = []
