from flask import Flask, request, jsonify, send_from_directory
from query_agent import english_to_sql, generate_final_response, gemini_direct_answer
from sql import run_query
from decimal import Decimal
import os

app = Flask(__name__)

# --- Serve the React or static frontend from frontend_new directory ---
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    if path != "" and os.path.exists(os.path.join('frontend_new', path)):
        return send_from_directory('frontend_new', path)
    else:
        return send_from_directory('frontend_new', 'index.html')

# --- Chat API endpoint (preserve your logic, but use context object for state) ---
from query_agent import ChatContext
user_contexts = {}

def get_user_context(session_id):
    if session_id not in user_contexts:
        user_contexts[session_id] = ChatContext()
    return user_contexts[session_id]

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('message', '')
    chat_history = data.get('history', [])
    session_id = data.get('session_id', 'default')
    context = get_user_context(session_id)
    if chat_history:
        context.history = chat_history
    else:
        if not hasattr(context, 'history'):
            context.history = []
        context.history.append({'user': user_input, 'response': None})
    if chat_history and chat_history[-1].get('follow_up'):
        enriched_prompt = f"{chat_history[-1]['follow_up']}. The user clarifies: {user_input}"
        parsed = english_to_sql(enriched_prompt, chat_context=context)
    else:
        parsed = english_to_sql(user_input, chat_context=context)
    sql_query = parsed.get("sql")
    follow_up = parsed.get("follow_up")
    latest_follow_up = follow_up or ""
    columns = rows = None
    if sql_query and sql_query.strip().lower() != "null":
        try:
            columns, results = run_query(sql_query)
            results = [
                [float(cell) if isinstance(cell, Decimal) else cell for cell in row]
                for row in results
            ]
            context.last_result = {
                "columns": columns,
                "rows": results,
                "question": user_input
            }
            final_answer = generate_final_response(user_input, columns, results, chat_context=context)
        except Exception as e:
            final_answer = f"❌ Failed to run your query: {e}"
    elif parsed.get("force_format_response"):
        payload = parsed["force_format_response"]
        if isinstance(payload, dict):
            question = payload["question"]
            columns = payload["columns"]
            rows = payload["rows"]
            final_answer = generate_final_response(f"{question} ({user_input})", columns, rows, chat_context=context)
        else:
            final_answer = str(payload)
    else:
        final_answer = gemini_direct_answer(user_input, chat_context=context)
    if hasattr(context, 'history') and context.history:
        context.history[-1]['response'] = final_answer
    return jsonify({
        'response': final_answer,
        'follow_up': latest_follow_up,
        'columns': columns,
        'rows': rows
    })

if __name__ == '__main__':
    app.run(debug=True, port=8501)
