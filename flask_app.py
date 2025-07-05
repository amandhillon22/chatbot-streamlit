from flask import Flask, request, jsonify, send_from_directory
from query_agent import english_to_sql, generate_final_response, gemini_direct_answer
from sql import run_query
from decimal import Decimal
import os

app = Flask(__name__)

# Serve the frontend
@app.route('/')
def serve_frontend():
    return send_from_directory('.', 'frontend_new.html')

# Serve static files (e.g., CSS, JS, icons)
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

# Chat API endpoint
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('message', '')
    chat_history = data.get('history', [])
    # Use your existing logic to process the message
    if not user_input.strip():
        return jsonify({'response': "Please enter a message."})

    # Simulate session state for follow-up
    awaiting_refinement = False
    pending_prompt = ''
    latest_follow_up = ''
    last_result = None

    # If the last message was a follow-up
    if chat_history and chat_history[-1].get('follow_up'):
        enriched_prompt = f"{chat_history[-1]['follow_up']}. The user clarifies: {user_input}"
        parsed = english_to_sql(enriched_prompt, chat_context=chat_history[:-1])
    else:
        parsed = english_to_sql(user_input, chat_context=chat_history)

    sql_query = parsed.get("sql")
    follow_up = parsed.get("follow_up")
    latest_follow_up = follow_up or ""

    if sql_query and sql_query.strip().lower() != "null":
        try:
            columns, results = run_query(sql_query)
            results = [
                [float(cell) if isinstance(cell, Decimal) else cell for cell in row]
                for row in results
            ]
            last_result = {
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
            final_answer = str(payload)
    else:
        final_answer = gemini_direct_answer(user_input, chat_context=chat_history)

    return jsonify({
        'response': final_answer,
        'follow_up': latest_follow_up
    })

if __name__ == '__main__':
    app.run(debug=True, port=8501)
