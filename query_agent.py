import google.generativeai as genai
import os
import json
import re
from dotenv import load_dotenv
import datetime
import streamlit as st
from decimal import Decimal

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

SCHEMAS = {
    "public": """
    Tables in Pagila:

    - public.actor(actor_id, first_name, last_name, last_update)
    - public.address(address_id, address, address2, district, city_id, postal_code, phone, last_update)
    - public.category(category_id, name, last_update)
    - public.city(city_id, city, country_id, last_update)
    - public.country(country_id, country, last_update)
    - public.customer(customer_id, store_id, first_name, last_name, email, address_id, activebool, create_date, last_update, active)
    - public.film(film_id, title, description, release_year, language_id, rental_duration, rental_rate, length, replacement_cost, rating, last_update, special_features, fulltext)
    - public.film_actor(actor_id, film_id, last_update)
    - public.film_category(film_id, category_id, last_update)
    - public.inventory(inventory_id, film_id, store_id, last_update)
    - public.language(language_id, name, last_update)
    - public.payment(payment_id, customer_id, staff_id, rental_id, amount, payment_date)
    - public.rental(rental_id, rental_date, inventory_id, customer_id, return_date, staff_id, last_update)
    - public.staff(staff_id, first_name, last_name, address_id, email, store_id, active, username, password, last_update, picture)
    - public.store(store_id, manager_staff_id, address_id, last_update)
    """
}

def extract_json(response):
    try:
        match = re.search(r"{[\s\S]+}", response)
        if match:
            return json.loads(match.group())
        return {}
    except json.JSONDecodeError:
        return {}

def english_to_sql(prompt, chat_context=None):
    if re.search(r'\b(format|clean|style|table|tabular|list|bullets|rewrite|shorter|rephrase|reword|simplify|again|visual|text-based|in text|as table|re-display)\b', prompt, re.IGNORECASE):
        last_data = st.session_state.get("last_result")
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
        for entry in reversed(chat_context):
            history_text += f"User: {entry['user']}\nBot: {entry.get('response', '')}\n"

    schema_text = "\n\n".join([f"Schema ({name}):\n{definition}" for name, definition in SCHEMAS.items()])

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

def generate_final_response(user_question, columns, rows):
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
You are a helpful assistant. Given the user's question and the database results in JSON, return a clean, readable answer.

IMPORTANT:
- You must base your answer strictly on the exact keys and values provided in the JSON.
- Do not assume missing data or exclude fields unless they are truly absent.
- If 'first_name' and 'last_name' are present, use both.
- Do not generalize based on partial values.
- Do not say “no data available” unless you're sure the previous result had no relevant entity.

If the user question includes words like pie chart, bar chart, line chart, plot, or visualize:
- Do NOT attempt to convert or assume chart data.
- Instead, politely respond that visual/chart-based outputs are not available here.

- If the user explicity mentions 'table', 'tabular' then make a table of the data and represent it.
Correct format:
| Title | Value |
|       |       |
|       |       |

- If the user does not mention any format particularly, then THINK YOURSELF ABOUT THE MOST SUITABLE FORMAT AND RESPOND WITH THAT.

- If the user refers to "that customer", "her", or "him", assume it refers to the most recent person or entity mentioned in the previous result.

If user asks to reformat previously given data:
- Do NOT reinterpret or regenerate data from scratch. Instead, reuse exactly what was shown before.

Ensure the result:
- Has minimal vertical whitespace.
- Avoids blank lines before tables.
- Avoids guessing unrelated summaries.
- Avoid having unnecessary extra spaces between your answers or line breaks between words.
- Make sure that the answers always have a proper structure. Do NOT give an unstructured answer.
- Is structured consistently based on result size:
  - If only 1 row and ≤3 columns → summary sentence.
  - If 2-4 columns and ≤20 rows → markdown table.
  - If >20 rows or 1 column → bullet list or expander if long.

User Question:
{user_question}

Database Results:
{formatted_data}

If the result has exactly one row and 3 or fewer columns, you MUST respond with a summary sentence.

Return the cleaned, user-friendly answer only:
"""

    try:
        response = model.generate_content(formatting_prompt)
        raw_response = response.text.strip()

        # Cleanup extra line breaks
        cleaned_response = re.sub(r'\n{3,}', '\n\n', raw_response)
        cleaned_response = re.sub(r'(\n\s*)+\Z', '', cleaned_response)
        cleaned_response = re.sub(r' +\n', '\n', cleaned_response)

        # Save structured result for follow-up
        st.session_state["last_result_summary"] = {
            "columns": columns,
            "rows": rows_json,
            "user_question": user_question
        }

        # Extract relevant row labels like film titles, names, etc.
        named_entities = []
        for row in rows_json:
            for key in ['title', 'name', 'film_title']:  # extendable
                val = row.get(key)
                if isinstance(val, str) and val.strip():
                    named_entities.append(val.strip())
                    break  # only take the first matching key per row

        st.session_state["last_result_entities"] = named_entities

        return cleaned_response

    except Exception as e:
        return f"Error formatting response: {e}"


def gemini_direct_answer(prompt, chat_context=None):

    history_text = ""
    if chat_context:
        for entry in reversed(chat_context):
            history_text += f"User: {entry['user']}\nBot: {entry.get('response', '')}\n"

    if "last_result_summary" in st.session_state:
        last_summary = st.session_state["last_result_summary"]
        columns = last_summary.get("columns", [])
        rows = last_summary.get("rows", [])
        last_user_q = last_summary.get("user_question", "")
        preview = json.dumps(rows[:5], indent=2) if rows else "[]"
        colnames = ", ".join(columns) if columns else "none"

        entities_info = ""
    if "last_result_entities" in st.session_state and st.session_state["last_result_entities"]:
        top_entities = ", ".join(st.session_state["last_result_entities"][:5])
        entities_info = f"\nThe last result compared the following entities: {top_entities}."

        result_context = f"""
        The last structured query came from the question: '{last_user_q}'.
        It returned the following columns: {colnames}.{entities_info}

Sample of the data:
{preview}
"""
    else:
        result_context = "There is no structured result saved from the last query."

    full_prompt = f"""
You are a helpful conversational assistant. Use the conversation history and the result context to understand what the user is referring to.
If the user asks “which one is better?”, refer to the **last comparison** of named rows (such as films or products).
If multiple entities were shown (like two film titles), compare them using the available metric (e.g., revenue, rental count).
Do not answer using unrelated records like top-grossing items unless explicitly asked.

Always use the most recent structured result as anchor unless the new question starts a new topic.

Important:
- If the user says things like "this data", "that table", "filter this", etc., refer to the **most recent structured query output** (columns and context).
- Do NOT make up data or regenerate summaries unless explicitly asked.
- If unsure, politely ask the user to clarify what data they want to continue with.
- Only use previous result if user's follow-up clearly refers to it using overlapping terms (e.g. "this", "these", "filter", or repeats previous columns/entities).
- If user's new question is **independent**, answer it fresh without using the last result.
- If the user's query is a clarification/confirmation like "are you sure?", "is that correct?", "can you verify?", then respond accordingly:
   - Confirm the based on the last result if you are confident.
   - Or say: "Let me double-check..." and re-evaluate the last result.
- Avoid using outdated context unless the user explicitly refers back to an earlier topic.
- Do NOT say "I don't know" if the data is present.
- Only say "no data available" if the last result clearly lacks that field or row.
- If a new question is unrelated (e.g., changes topic completely), start fresh.


- Always be aware that certain terms or phrases (e.g., "maximum duration", "total amount", "count", "usage", "activity") can have **multiple interpretations** depending on context.
- If you detect ambiguity (e.g., "duration" could mean predefined vs calculated), briefly clarify what you're using.

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

{result_context}


Conversation history:
{history_text}

User: {prompt}
"""

    try:
        response = model.generate_content(full_prompt)
        return response.text.strip()
    except Exception as e:
        return f"Gemini error: {e}"
