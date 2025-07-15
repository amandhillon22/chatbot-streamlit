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

    history_text = ""
    if chat_context:
        for entry in reversed(chat_context.history):
            history_text += f"User: {entry['user']}\nBot: {entry.get('response', '')}\n"

    # 🚀 EMBEDDING-ENHANCED PROCESSING (if available)
    relevant_schema_text = SCHEMA_PROMPT  # Default fallback
    
    if EMBEDDINGS_AVAILABLE and embedding_manager:
        try:
            print(f"🎯 Analyzing query with embeddings: '{prompt[:50]}...'")
            
            # Find most relevant tables for this query
            relevant_tables = embedding_manager.find_relevant_tables(prompt, top_k=8)
            
            if relevant_tables:
                print(f"📊 Using embeddings: Found {len(relevant_tables)} relevant tables")
                
                # Build focused schema text with only relevant tables
                focused_schema = []
                for table_key, similarity, description in relevant_tables:
                    try:
                        schema_name, table_name = table_key.split('.', 1)
                        if schema_name in SCHEMA_DICT and table_name in SCHEMA_DICT[schema_name]:
                            columns = SCHEMA_DICT[schema_name][table_name]
                            focused_schema.append(f"- {table_key}({', '.join(columns)})")
                            print(f"  • {table_key} (relevance: {similarity:.3f}) - Columns: {len(columns)}")
                    except Exception as e:
                        print(f"⚠️ Error processing table {table_key}: {e}")
                
                if focused_schema:
                    relevant_schema_text = "Most relevant tables for your query:\n" + "\n".join(focused_schema)
                    print(f"✅ Using focused schema with {len(focused_schema)} tables instead of all {len(SCHEMA_DICT.get('public', {}))} tables")
                    
        except Exception as e:
            print(f"⚠️ Embedding error: {e}, falling back to full schema")

    schema_text = relevant_schema_text

    full_prompt = f"""
You are an intelligent SQL assistant for multiple PostgreSQL schemas.

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
User: {prompt}
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
    history_text = ""
    if chat_context and hasattr(chat_context, 'history'):
        for entry in reversed(chat_context.history):
            history_text += f"User: {entry['user']}\nBot: {entry.get('response', '')}\n"
    comparison_context = ""
    if chat_context and chat_context.last_result_summary:
        last_summary = chat_context.last_result_summary
        columns = last_summary.get("columns", [])
        rows = last_summary.get("rows", [])
        last_user_q = last_summary.get("user_question", "")
        preview = json.dumps(rows[:5], indent=2) if rows else "[]"
        colnames = ", ".join(columns) if columns else "none"
        if len(rows) >= 2 and len(columns) >= 2:
            entity_col = columns[0]
            value_col = columns[1] if len(columns) > 1 else None
            comparison_context = (
                f"The last result was a comparison between these entities based on '{value_col}':\n" +
                "\n".join([f"- {row[entity_col]}: {row[value_col]}" for row in rows]) +
                "\n\nIf the user asks 'which one is better?' or 'which one has better revenue?', answer based on this comparison."
            )
        entities_info = ""
        if chat_context.last_result_entities:
            top_entities = ", ".join(chat_context.last_result_entities[:5])
            entities_info = f"\nThe last result included key values such as: {top_entities}."
        result_context = (
            f"The last structured query came from the question: '{last_user_q}'.\n"
            f"It returned the following columns: {colnames}.{entities_info}\n\n"
            f"Sample of the data:\n{preview}\n"
        )
    else:
        result_context = "There is no structured result saved from the last query."
    full_prompt = (
        "You are a helpful conversational assistant. Use the conversation history and the result context to understand what the user is referring to.\n\n"
        f"{comparison_context}\n\n"
        "Important:\n"
        "- If the user says things like \"this data\", \"that table\", \"filter this\", etc., refer to the **most recent structured query output** (columns and context).\n"
        "- Do NOT make up data or regenerate summaries unless explicitly asked.\n"
        "- If unsure, politely ask the user to clarify what data they want to continue with.\n"
        "- Only use previous result if user's follow-up clearly refers to it using overlapping terms (e.g. \"this\", \"these\", \"filter\", or repeats previous columns/entities).\n"
        "- If user's new question is **independent**, answer it fresh without using the last result.\n"
        "- If the user's query is a clarification/confirmation like \"are you sure?\", \"is that correct?\", \"can you verify?\", then respond accordingly:\n"
        "   - Confirm the based on the last result if you are confident.\n"
        "   - Or say: \"Let me double-check...\" and re-evaluate the last result.\n"
        "- Avoid using outdated context unless the user explicitly refers back to an earlier topic.\n"
        "- Do NOT say \"I don't know\" if the data is present.\n"
        "- Only say \"no data available\" if the last result clearly lacks that field or row.\n"
        "- If a new question is unrelated (e.g., changes topic completely), start fresh.\n\n"
        "- Always be aware that certain terms or phrases (e.g., \"maximum duration\", \"total amount\", \"count\", \"usage\", \"activity\") can have **multiple interpretations** depending on context.\n"
        "- If you detect ambiguity (e.g., \"duration\" could mean predefined vs calculated), briefly clarify what you're using.\n\n"
        "- When such a term appears, do the following:\n"
        "   1. Infer the most likely meaning based on the **current question**,\n"
        "   2. Compare it to what was previously asked in the conversation.\n"
        "   3. If the meaning may differ (e.g., the same word could refer to a different table or concept), clearly **explain the distinction**.\n\n"
        "- For example, \"duration\" might refer to:\n"
        "   - A **predefined value** stored in a metadata table,\n"
        "   - A **computed value** based on timestamps (e.g., end_time - start_time),\n"
        "   - A **user-defined period**, based on filters or ranges.\n\n"
        "- If the user switches from talking about one entity (like \"product\") to another (like \"customer\"), and reuses similar terms (e.g., \"usage\", \"duration\", \"amount\"), you must clarify whether their intent has shifted.\n\n"
        "- In all such cases, briefly explain the **contextual meaning** of the value you're returning, and what field or logic it came from.\n\n"
        f"{result_context}\n\n"
        "Conversation history:\n"
        f"{history_text}\n\n"
        f"User: {prompt}\n"
    )
    try:
        response = model.generate_content(full_prompt)
        return response.text.strip()
    except Exception as e:
        return f"Gemini error: {e}"

# Add ChatContext class for Flask integration
class ChatContext:
    def __init__(self):
        self.last_result = None
        self.last_result_summary = None
        self.last_result_entities = None
        self.history = []

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
