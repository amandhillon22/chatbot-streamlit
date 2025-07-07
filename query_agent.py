import google.generativeai as genai
import os
import json
import re
from dotenv import load_dotenv
import datetime
from decimal import Decimal
from sql import get_full_schema

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

    schema_text = SCHEMA_PROMPT

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

But DO NOT include actual DB results in this stage.

- Always be aware that certain terms or phrases (e.g., "maximum duration", "total amount", "count", "usage", "activity") can have **multiple interpretations** depending on context.

- When such a term appears, do the following:
   1. Infer the most likely meaning based on the **current question**, and
   2. Compare it to what was previously asked in the conversation.
   3. If the meaning may differ (e.g., the same word could refer to a different table or concept), clearly **explain the distinction**.

- For example, "duration" might refer to:
   - A **predefined value** stored in a metadata table,
   - A **computed value** based on timestamps (e.g., end_time - start_time),
   - A **user-defined period**, based on filters or ranges.

- If the user switches from talking about one entity (like "product") to another (like "customer"), and reuses similar terms (e.g., "usage", "duration", "amount"), you must clarify whether their intent has shifted.

- In all such cases, briefly explain the **contextual meaning** of the value you're returning, and what field or logic it came from.


Strict rules:
- Use schema-qualified table names.
- No unqualified names.
- No markdown or explanations outside JSON.
- For year-based filters (e.g., customers who joined in 2022), use EXTRACT(YEAR FROM column) = 2022 or BETWEEN '2022-01-01' AND '2022-12-31'.
- Use this JSON structure exactly:

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
- If the answer can be given in natural language, do so.
- Only use a markdown table if it is truly necessary for clarity (e.g., multiple rows or columns that cannot be summarized naturally).
- If the answer is a single value or can be summarized in a sentence, prefer natural language.
- If there is no data, politely state that no relevant data was found.
- Do not mention table or column names in your explanation or answer.
- Be concise, friendly, and clear.

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
