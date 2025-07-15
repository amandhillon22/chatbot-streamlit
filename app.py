import streamlit as st
from query_agent import english_to_sql, generate_final_response, gemini_direct_answer, validate_sql_query
from sql import run_query
from decimal import Decimal
import markdown
from markdown.extensions.tables import TableExtension
import re

def sanitize_results(results):
    return [
        [float(cell) if isinstance(cell, Decimal) else cell for cell in row]
        for row in results
    ]

def markdown_to_html_table(md):
    return markdown.markdown(md, extensions=[TableExtension()])

st.sidebar.title("🌓 Theme")
theme = st.sidebar.radio("Choose theme:", ["Light", "Dark"])

if theme == "Dark":
    st.markdown("""
        <style>
            body, .stApp {
                background-color: #0e1117;
                color: white;
            }
            input, textarea, .sttextInput input, .sttextArea textarea {
                color: white !important;
                background-color: #1e1e1e !important;
                caret-color: white !important;
                border: 1px solid #555 !important;
            }
            .follow-up-box {
                background-color: #263238;
                padding: 10px;
                border-radius: 8px;
                color: #80cbc4;
                margin-top: 10px;
            }
            button {
                background-color: #80cbc4 !important;
                color: black !important;
            }
            .user-bubble {
                text-align: right;
                background-color: #2c2f36;
                color: #e0e0e0;
                padding: 8px 12px;
                margin-bottom: 6px;
                border-radius: 10px;
                max-width: 80%;
                margin-left: auto;
            }
            .bot-bubble {
                text-align: left;
                background-color: #1a1a1a;
                color: white;
                padding: 10px 14px;
                margin-bottom: 8px;
                border-radius: 10px;
                max-width: 80%;
                white-space: pre-wrap;
                line-height: 1.4;
                overflow-x: auto;
            }
            .bot-bubble table {
                border-collapse: collapse;
                width: 100%;
                margin-top: 5px;
            }
            .bot-bubble th, .bot-bubble td {
                border: 1px solid #90caf9;
                padding: 6px 10px;
                text-align: left;
                color: white;
            }
            .bot-bubble th {
                background-color: #2c3e50;
                font-weight: bold;
            }
            .bot-bubble p {
                margin: 0;
            }
            .bot-bubble ul {
                margin: 0;
                padding-left: 20px;
            }
            .bot-bubble li {
                margin: 0;
                padding: 0;
                line-height: 1.2;
                list-style-position: inside;
            }
            .st-expanderHeader, .st-expanderContent {
                background-color: #121212 !important;
                color: white !important;
            }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
            body, .stApp {
                background-color: white;
                color: #1e1e1e;
            }
            input, textarea, .sttextInput input, .stTextArea textarea {
                color: #1e1e1e !important;
                background-color: white !important;
                caret-color: black !important;
                border: 1px solid #ccc !important;
            }
            ::placeholder {
                color: #999 !important;
            }
            .follow-up-box {
                background-color: #e0f7fa;
                padding: 10px;
                border-radius: 8px;
                color: #00796b;
                margin-top: 10px;
            }
            button {
                background-color: #00796b !important;
                color: white !important;
            }
            .user-bubble {
                text-align: right;
                background-color: #f0f0f0;
                color: #1e1e1e;
                padding: 8px 12px;
                margin-bottom: 6px;
                border-radius: 10px;
                max-width: 80%;
                margin-left: auto;
            }
            .bot-bubble {
                text-align: left;
                background-color: #e3f2fd;
                color: #1e1e1e;
                padding: 10px 14px;
                margin-bottom: 8px;
                border-radius: 10px;
                max-widht: 80%;
                white-space: pre-wrap;
                line-height: 1.4;
                overflow-x: auto;
            }
        </style>
    """, unsafe_allow_html=True)

# state initialisation
for var in ["chat_history", "awaiting_refinement", "pending_prompt", "user_input", "latest_follow_up", "last_result"]:
    if var not in st.session_state:
        st.session_state[var] = [] if var == "chat_history" else ""

st.sidebar.title("🕘 Chat Chat")
if st.sidebar.button("🗑️ Clear Chat"):
    for key in ["chat_history", "awaiting_refinement", "pending_prompt", "latest_follow_up", "last_result"]:
        st.session_state[key] = [] if key == "chat_history" else ""

st.title("🎙️ Gemini- Database Chatbot")

st.markdown("""
<div class='chat-input-container'>
<form method='POST'>
""", unsafe_allow_html=True)

for entry in st.session_state.chat_history:
    st.markdown(f"<div class='user-bubble'><b>You:</b> {entry['user']}</div>", unsafe_allow_html=True)
    bot_response = entry["response"]
    line_count = bot_response.count('\n')
    char_count = len(bot_response)

    def contains_markdown_table(text):
        return text.strip().startswith("|") and "\n|---" in text

    if contains_markdown_table(bot_response):
        table_html = markdown_to_html_table(bot_response)
        with st.expander("📊 Result (click to expand/ minimize)", expanded=False):
            st.markdown(f"<div class='bot-bubble'>{table_html}</div>", unsafe_allow_html=True)
    elif line_count > 10 or char_count > 600:
        with st.expander("🤖 Response (click to expand/ minimize)", expanded=False):
            st.markdown(f"<div class='bot-bubble'>{bot_response}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-bubble'>{bot_response}</div>", unsafe_allow_html=True)

st.markdown("</form></div>", unsafe_allow_html=True)

with st.form("chat_input_form", clear_on_submit=True):
    user_input = st.text_input("Your question:", placeholder="Type your question here...", label_visibility="collapsed")
    submitted = st.form_submit_button(" Submit ")

    if submitted and user_input.strip():
        st.session_state.chat_history.append({"user": user_input, "response": "🤖 Thinking..."})
        st.rerun()

if st.session_state.latest_follow_up:
    st.markdown(f"<div class='follow-up-box'><b>🤖 Suggested follow-up:</b> {st.session_state.latest_follow_up}</div>", unsafe_allow_html=True)

if st.session_state.chat_history and st.session_state.chat_history[-1]['response'] == "🤖 Thinking...":
    user_input = st.session_state.chat_history[-1]['user']

    if st.session_state.awaiting_refinement and st.session_state.pending_prompt:
        enriched_prompt = f"{st.session_state.pending_prompt}. The user clarifies: {user_input}"
        parsed = english_to_sql(enriched_prompt, chat_context=st.session_state.chat_history[:-1])
    else:
        parsed = english_to_sql(user_input, chat_context=st.session_state.chat_history[:-1])

    sql_query = parsed.get("sql")
    follow_up = parsed.get("follow_up")
    st.session_state.latest_follow_up = follow_up or ""

    if sql_query and sql_query.strip().lower() != "null":
        # Validate SQL query and get suggestions for type casting
        is_valid, validation_error, suggested_sql = validate_sql_query(sql_query)
        
        # Use suggested SQL if available (for type casting)
        final_sql = suggested_sql if suggested_sql else sql_query
        
        if not is_valid:
            final_answer = f"❌ **Query Validation Error:** {validation_error}\n\n💡 **Suggestion:** Please rephrase your question or specify which columns you'd like to analyze."
        else:
            try:
                columns, results = run_query(final_sql)
                results = sanitize_results(results)
                st.session_state.last_result = {
                    "columns": columns,
                    "rows": results,
                    "question": user_input
                }
                final_answer = generate_final_response(user_input, columns, results)
            except Exception as e:
                final_answer = f"❌ Failed to run your query: {e}"
    elif parsed.get("force_format_response"):
        payload = parsed["force_format_response"]
        if isinstance(payload, dict):
            question = payload["question"]
            columns = payload["columns"]
            rows = payload["rows"]
            final_answer = generate_final_response(f"{question} ({user_input})", columns, rows)
        else:
            # If payload is a string, use it directly as the answer
            final_answer = str(payload)
    else:
        final_answer = gemini_direct_answer(user_input, chat_context=st.session_state.chat_history[:-1])

    st.session_state.chat_history[-1]['response'] = final_answer
    st.session_state.awaiting_refinement = bool(follow_up)
    st.session_state.pending_prompt = follow_up or ""
    st.rerun()

# Show debug log in sidebar
if 'debug_log' in st.session_state and st.session_state['debug_log']:
    st.sidebar.markdown('---')
    st.sidebar.subheader('Debug Log')
    for msg in st.session_state['debug_log'][-10:]:  # Show last 10 messages
        st.sidebar.write(msg)

st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)

