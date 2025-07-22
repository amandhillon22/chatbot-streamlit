from flask import Flask, request, jsonify, send_from_directory, session
from query_agent import english_to_sql, generate_final_response, gemini_direct_answer, validate_sql_query
from sql import run_query
from decimal import Decimal
import os
from dotenv import load_dotenv
import time
from functools import wraps
from user_manager import user_manager, chat_history_manager

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-change-this-in-production')

# --- Serve the React or static frontend from frontend_new directory ---
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    if path != "" and os.path.exists(os.path.join('frontend_new', path)):
        return send_from_directory('frontend_new', path)
    else:
        return send_from_directory('frontend_new', 'index.html')

# --- Rate limiting decorator ---
last_request_time = {}

def rate_limit(requests_per_minute=10):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            now = time.time()
            session_id = request.get_json().get('session_id', 'default') if request.get_json() else 'default'
            
            if session_id in last_request_time:
                time_since_last = now - last_request_time[session_id]
                min_interval = 60.0 / requests_per_minute  # seconds between requests
                
                if time_since_last < min_interval:
                    wait_time = min_interval - time_since_last
                    return jsonify({
                        'response': f"⏳ Rate limit: Please wait {wait_time:.1f} seconds before next request.",
                        'follow_up': None,
                        'columns': None,
                        'rows': None
                    }), 429
            
            last_request_time[session_id] = now
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# --- Authentication endpoints ---
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')
    
    if not username or not password:
        return jsonify({'authenticated': False, 'error': 'Username and password required'}), 400
    
    result = user_manager.authenticate_user(username, password)
    
    if result['authenticated']:
        session['user_id'] = result['id']
        session['username'] = result['username']
        return jsonify({
            'authenticated': True,
            'user': {
                'id': result['id'],
                'username': result['username']
            }
        })
    else:
        return jsonify({'authenticated': False, 'error': 'Invalid credentials'}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'logged_out': True})

@app.route('/api/user', methods=['GET'])
def get_current_user():
    if 'user_id' in session:
        return jsonify({
            'authenticated': True,
            'user': {
                'id': session['user_id'],
                'username': session['username']
            }
        })
    else:
        return jsonify({'authenticated': False})

# --- Chat history endpoints ---
@app.route('/api/chat/sessions', methods=['GET'])
def get_chat_sessions():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    result = chat_history_manager.get_user_chat_sessions(session['user_id'])
    return jsonify(result)

@app.route('/api/chat/sessions', methods=['POST'])
def create_chat_session():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.get_json()
    title = data.get('title', None)
    
    result = chat_history_manager.create_chat_session(session['user_id'], title)
    return jsonify(result)

@app.route('/api/chat/sessions/<session_id>/history', methods=['GET'])
def get_chat_history(session_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    result = chat_history_manager.get_chat_history(session_id)
    return jsonify(result)

@app.route('/api/chat/sessions/<session_id>', methods=['DELETE'])
def delete_chat_session(session_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    result = chat_history_manager.delete_chat_session(session_id, session['user_id'])
    return jsonify(result)

@app.route('/api/chat/sessions/<session_id>/title', methods=['PUT'])
def update_session_title(session_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.get_json()
    title = data.get('title', '')
    
    if not title:
        return jsonify({'error': 'Title required'}), 400
    
    result = chat_history_manager.update_session_title(session_id, title)
    return jsonify(result)

# --- Chat API endpoint (preserve your logic, but use context object for state) ---
from query_agent import ChatContext
user_contexts = {}

def get_user_context(session_id):
    if session_id not in user_contexts:
        user_contexts[session_id] = ChatContext()
    return user_contexts[session_id]

@app.route('/api/chat', methods=['POST'])
@rate_limit(requests_per_minute=8)  # Conservative rate limiting
def chat():
    # Check authentication
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
        
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
        print(f"\n🔍 USER QUERY (Follow-up): {user_input}")
        print(f"📝 ENRICHED PROMPT: {enriched_prompt}")
    else:
        parsed = english_to_sql(user_input, chat_context=context)
        print(f"\n🔍 USER QUERY: {user_input}")
    
    # 🧠 Check if intelligent reasoning was applied
    if parsed.get('reasoning_applied'):
        print(f"🧠 INTELLIGENT REASONING APPLIED: {parsed.get('reasoning_type')}")
        # For intelligent reasoning, we can return the response directly
        sql_query = parsed.get("sql")
        final_answer = parsed.get("response", "I found the information using intelligent reasoning.")
        
        # Execute the intelligent SQL to get actual data
        if sql_query and sql_query.strip().lower() != "null":
            try:
                columns, results = run_query(sql_query)
                print(f"✅ INTELLIGENT QUERY EXECUTED - Returned {len(results)} rows")
                
                # Store results in context
                context.add_interaction(
                    user_input, 
                    final_answer,
                    sql_query=sql_query, 
                    columns=columns, 
                    rows=results
                )
                
                # Generate a rich response with the actual data
                if results:
                    enhanced_response = generate_final_response(user_input, columns, results, chat_context=context)
                    final_answer = f"{final_answer}\n\n{enhanced_response}"
                
            except Exception as e:
                print(f"❌ Error executing intelligent query: {e}")
                final_answer = f"{final_answer}\n\n❌ However, I encountered an error retrieving the actual data: {str(e)}"
        
        return jsonify({
            'response': final_answer,
            'follow_up': parsed.get('follow_up'),
            'columns': columns if 'columns' in locals() else None,
            'rows': results if 'results' in locals() else None,
            'sql': sql_query,
            'reasoning_applied': True
        })
    
    sql_query = parsed.get("sql")
    print(f"🔧 GENERATED SQL: {sql_query}")
    print("-" * 80)
    follow_up = parsed.get("follow_up")
    latest_follow_up = follow_up or ""
    columns = rows = None
    if sql_query and sql_query.strip().lower() != "null":
        # Validate SQL query and get suggestions for type casting
        is_valid, validation_error, suggested_sql = validate_sql_query(sql_query)
        
        if suggested_sql and suggested_sql != sql_query:
            print(f"✨ SUGGESTED SQL (with type casting): {suggested_sql}")
        
        # Use suggested SQL if available (for type casting)
        final_sql = suggested_sql if suggested_sql else sql_query
        print(f"⚡ FINAL SQL TO EXECUTE: {final_sql}")
        
        if not is_valid:
            print(f"❌ VALIDATION ERROR: {validation_error}")
            final_answer = f"❌ **Query Validation Error:** {validation_error}\n\n💡 **Suggestion:** Please rephrase your question or specify which columns you'd like to analyze."
        else:
            try:
                print(f"🔄 EXECUTING QUERY...")
                columns, results = run_query(final_sql)
                print(f"✅ QUERY EXECUTED SUCCESSFULLY - Returned {len(results)} rows")
                results = [
                    [float(cell) if isinstance(cell, Decimal) else cell for cell in row]
                    for row in results
                ]
                
                # Handle large result sets to prevent API quota issues
                total_rows = len(results)
                MAX_ROWS = 50
                
                # Store results in context immediately for ordinal reference
                context.add_interaction(
                    user_input, 
                    None,  # Response will be set later
                    sql_query=final_sql, 
                    columns=columns, 
                    rows=results
                )
                print(f"💾 STORED {len(results)} RESULTS WITH ORDINAL INDEXING")
                
                if total_rows > MAX_ROWS:
                    # Limit to top 50 rows
                    limited_results = results[:MAX_ROWS]
                    context.last_result = {
                        "columns": columns,
                        "rows": limited_results,
                        "question": user_input,
                        "total_rows": total_rows,
                        "limited": True
                    }
                    
                    # Create a simple response for large datasets
                    final_answer = f"**Query Results (Showing top {MAX_ROWS} of {total_rows:,} total rows)**\n\n"
                    
                    # Add a simple table view
                    if columns and limited_results:
                        # Create header
                        final_answer += "| " + " | ".join(columns) + " |\n"
                        final_answer += "|" + "|".join(["---"] * len(columns)) + "|\n"
                        
                        # Add rows (limit to avoid token issues)
                        display_rows = min(20, len(limited_results))  # Show max 20 rows in table
                        for row in limited_results[:display_rows]:
                            formatted_row = []
                            for cell in row:
                                if cell is None:
                                    formatted_row.append("NULL")
                                elif isinstance(cell, (int, float)):
                                    formatted_row.append(str(cell))
                                else:
                                    # Truncate long text
                                    cell_str = str(cell)
                                    formatted_row.append(cell_str[:50] + "..." if len(cell_str) > 50 else cell_str)
                            final_answer += "| " + " | ".join(formatted_row) + " |\n"
                        
                        if display_rows < len(limited_results):
                            final_answer += f"\n*... and {len(limited_results) - display_rows} more rows shown in the limited dataset*\n"
                    
                    final_answer += f"\n📊 **Note:** This query returned {total_rows:,} rows, which is quite large! I'm showing you the top {MAX_ROWS} results to keep things manageable.\n\n"
                    final_answer += "💡 **Suggestions:**\n"
                    final_answer += "- Add `LIMIT 50` to your query for faster results\n"
                    final_answer += "- Use filters like `WHERE` conditions to narrow down the data\n"
                    final_answer += "- Ask for specific aggregations (COUNT, SUM, AVG) instead of raw data\n"
                    final_answer += "- Try queries like 'show me a summary of...' or 'count the number of...'"
                    
                else:
                    # Normal handling for smaller results
                    context.last_result = {
                        "columns": columns,
                        "rows": results,
                        "question": user_input
                    }
                    
                    # Enhanced handling for empty results
                    if len(results) == 0:
                        print(f"📭 EMPTY RESULT SET - No data found")
                        # Check if this was an ordinal reference to provide better context
                        if context and hasattr(context, 'last_displayed_items') and context.last_displayed_items:
                            position, entity = context.extract_ordinal_reference(user_input)
                            if position:
                                target_item = context.get_item_by_ordinal(position)
                                if target_item:
                                    # Extract identifier for better error message
                                    identifier = None
                                    for key in ['reg_no', 'registration_number', 'vehicle_id', 'id']:
                                        if key in target_item:
                                            identifier = target_item[key]
                                            break
                                    
                                    if identifier:
                                        final_answer = generate_final_response(f"{user_input} (for {identifier})", columns, results, chat_context=context)
                                    else:
                                        final_answer = generate_final_response(user_input, columns, results, chat_context=context)
                                else:
                                    final_answer = generate_final_response(user_input, columns, results, chat_context=context)
                            else:
                                final_answer = generate_final_response(user_input, columns, results, chat_context=context)
                        else:
                            final_answer = generate_final_response(user_input, columns, results, chat_context=context)
                    else:
                        final_answer = generate_final_response(user_input, columns, results, chat_context=context)
            except Exception as e:
                print(f"💥 QUERY EXECUTION ERROR: {e}")
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
        try:
            final_answer = gemini_direct_answer(user_input, chat_context=context)
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "quota" in error_msg.lower():
                final_answer = "⏳ **API Rate Limit Reached**\n\nPlease wait a moment and try again. The free tier has limited requests per minute.\n\n**Suggestions:**\n- Wait 1-2 minutes\n- Try a simpler question\n- Consider upgrading your API plan"
            elif "API_KEY_INVALID" in error_msg or "expired" in error_msg.lower():
                final_answer = "🔑 **API Key Issue**\n\nPlease check your API key configuration.\n\n**Steps:**\n- Verify your API key in .env file\n- Restart the application\n- Generate a new API key if needed"
            else:
                final_answer = f"❌ **Error:** {error_msg}"
    # Update chat history and context with rich information
    # Ensure we have valid columns and rows for context storage
    final_columns = columns if columns is not None else []
    final_rows = rows if rows is not None else []
    
    if hasattr(context, 'history') and context.history:
        context.history[-1]['response'] = final_answer
        # Add the interaction with full context
        context.add_interaction(
            user_input, 
            final_answer, 
            sql_query=sql_query, 
            columns=final_columns, 
            rows=final_rows
        )
    else:
        # Initialize history if not exists
        if not hasattr(context, 'history'):
            context.history = []
        context.add_interaction(
            user_input, 
            final_answer, 
            sql_query=sql_query, 
            columns=final_columns, 
            rows=final_rows
        )
        
    print(f"💬 CONVERSATION TOPICS: {', '.join(context.key_topics) if context.key_topics else 'None'}")
    print(f"📝 CONVERSATION SUMMARY: {context.conversation_summary[:100]}..." if context.conversation_summary else "")
    print(f"🔢 ORDINAL ITEMS STORED: {len(context.last_displayed_items) if hasattr(context, 'last_displayed_items') else 0}")
    if hasattr(context, 'last_displayed_items') and context.last_displayed_items:
        print(f"📊 SAMPLE STORED ITEMS: {context.last_displayed_items[:3]}")
    print("-" * 80)
    
    # Save chat messages to database if user is authenticated
    if 'user_id' in session and session_id != 'default':
        try:
            # Save user message
            chat_history_manager.save_message(session_id, 'user', user_input)
            
            # Save assistant message with SQL query
            sql_for_history = parsed.get('sql') if parsed.get('sql') and parsed.get('sql').strip().lower() != 'null' else None
            chat_history_manager.save_message(session_id, 'assistant', final_answer, sql_for_history)
            
            print(f"💾 Saved messages to database for session: {session_id}")
        except Exception as e:
            print(f"⚠️ Error saving chat history: {e}")
    
    return jsonify({
        'response': final_answer,
        'follow_up': latest_follow_up,
        'columns': columns,
        'rows': rows
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
