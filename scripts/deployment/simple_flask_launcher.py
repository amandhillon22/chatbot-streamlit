#!/usr/bin/env python3
"""
Simple Flask App Launcher for Localhost
This script starts the Diya Chatbot Flask application with minimal dependencies
"""

import os
import sys

def setup_environment():
    """Set up environment variables for localhost deployment"""
    # Database configuration
    os.environ['hostname'] = os.getenv('hostname', 'localhost')
    os.environ['dbname'] = os.getenv('dbname', 'rdc_dump')
    os.environ['user_name'] = os.getenv('user_name', 'postgres')
    os.environ['password'] = os.getenv('password', 'Akshit@123')
    
    # Flask configuration
    os.environ['FLASK_ENV'] = os.getenv('FLASK_ENV', 'development')
    os.environ['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-localhost')
    
    print("🔧 Environment configured for localhost")

def test_basic_imports():
    """Test if basic required modules can be imported"""
    try:
        import flask
        print("✅ Flask available")
    except ImportError:
        print("❌ Flask not available. Please install: pip install flask")
        return False
    
    try:
        import psycopg2
        print("✅ PostgreSQL adapter available")
    except ImportError:
        print("❌ psycopg2 not available. Please install: pip install psycopg2-binary")
        return False
    
    return True

def test_database_connection():
    """Test database connection"""
    try:
        import psycopg2
        conn = psycopg2.connect(
            host=os.getenv('hostname', 'localhost'),
            dbname=os.getenv('dbname', 'rdc_dump'),
            user=os.getenv('user_name', 'postgres'),
            password=os.getenv('password', 'Akshit@123'),
            port=5432
        )
        cursor = conn.cursor()
        cursor.execute('SELECT 1;')
        cursor.fetchone()
        cursor.close()
        conn.close()
        print("✅ Database connection successful")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def start_basic_flask_app():
    """Start a basic Flask application"""
    from flask import Flask, jsonify, request, render_template_string
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # Basic HTML template
    HTML_TEMPLATE = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Diya Chatbot - Localhost</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #2c5aa0; }
            .status { padding: 10px; margin: 10px 0; border-radius: 5px; }
            .success { background: #d4edda; border: 1px solid #c3e6cb; color: #155724; }
            .error { background: #f8d7da; border: 1px solid #f5c6cb; color: #721c24; }
            .info { background: #d1ecf1; border: 1px solid #bee5eb; color: #0c5460; }
            .chat-box { border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }
            input[type="text"] { width: 70%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
            button { padding: 10px 20px; background: #2c5aa0; color: white; border: none; border-radius: 5px; cursor: pointer; }
            button:hover { background: #1d4084; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 Diya Chatbot - Localhost</h1>
            <div class="status info">
                <strong>Status:</strong> Running on localhost:5000<br>
                <strong>Database:</strong> {{ db_status }}<br>
                <strong>Environment:</strong> Development
            </div>
            
            <h2>Quick Test</h2>
            <div class="chat-box">
                <input type="text" id="queryInput" placeholder="Ask a question about your database..." />
                <button onclick="sendQuery()">Send</button>
                <div id="response" style="margin-top: 10px; padding: 10px; background: #f8f9fa; border-radius: 5px;"></div>
            </div>
            
            <h2>API Endpoints</h2>
            <ul>
                <li><code>/</code> - This home page</li>
                <li><code>/health</code> - Health check endpoint</li>
                <li><code>/query</code> - Chat query endpoint (POST)</li>
                <li><code>/admin/metrics</code> - System metrics</li>
            </ul>
            
            <div class="status success">
                ✅ Flask application is running successfully!
            </div>
        </div>
        
        <script>
            function sendQuery() {
                const query = document.getElementById('queryInput').value;
                if (!query) return;
                
                document.getElementById('response').innerHTML = 'Processing...';
                
                fetch('/query', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query: query })
                })
                .then(response => response.json())
                .then(data => {
                    document.getElementById('response').innerHTML = 
                        '<strong>Response:</strong> ' + (data.response || data.error || 'No response');
                })
                .catch(error => {
                    document.getElementById('response').innerHTML = 
                        '<strong>Error:</strong> ' + error.message;
                });
            }
        </script>
    </body>
    </html>
    """
    
    @app.route('/')
    def home():
        # Test database connection for status
        try:
            test_database_connection()
            db_status = "✅ Connected"
        except:
            db_status = "❌ Connection issues"
        
        return render_template_string(HTML_TEMPLATE, db_status=db_status)
    
    @app.route('/health')
    def health():
        return jsonify({
            'status': 'healthy',
            'database': 'connected' if test_database_connection() else 'disconnected',
            'environment': os.getenv('FLASK_ENV', 'development')
        })
    
    @app.route('/query', methods=['POST'])
    def query():
        try:
            data = request.get_json()
            query = data.get('query', '')
            
            # Simple response for now
            return jsonify({
                'response': f"Received your query: '{query}'. Full chatbot functionality requires all dependencies to be installed.",
                'query': query,
                'status': 'partial'
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/admin/metrics')
    def metrics():
        return jsonify({
            'system': 'Diya Chatbot',
            'status': 'running',
            'mode': 'localhost-development',
            'database': os.getenv('dbname', 'rdc_dump'),
            'host': os.getenv('hostname', 'localhost')
        })
    
    return app

def main():
    print("🚀 Diya Chatbot - Simple Localhost Launcher")
    print("=" * 45)
    
    # Step 1: Setup environment
    setup_environment()
    
    # Step 2: Test basic imports
    if not test_basic_imports():
        print("\n❌ Missing required dependencies. Please install them first.")
        return
    
    # Step 3: Test database connection
    db_ok = test_database_connection()
    if not db_ok:
        print("\n⚠️  Database connection issues detected, but continuing...")
    
    # Step 4: Start Flask app
    print("\n🚀 Starting Flask application...")
    try:
        # Try to import the full application first
        try:
            import sys
            sys.path.append('/home/linux/Documents/chatbot-diya')
            from src.api.flask_app import app
            print("✅ Full application loaded")
            flask_app = app
        except Exception as e:
            print(f"⚠️  Full application failed to load: {e}")
            print("🔧 Starting with basic Flask app...")
            flask_app = start_basic_flask_app()
        
        print("\n🌐 Application URLs:")
        print("   • Main Interface: http://localhost:5000")
        print("   • Health Check:   http://localhost:5000/health")
        print("   • API Metrics:    http://localhost:5000/admin/metrics")
        print("\n💡 Press Ctrl+C to stop the server")
        print("=" * 45)
        
        flask_app.run(
            host='0.0.0.0',
            port=5000,
            debug=True if os.getenv('FLASK_ENV') == 'development' else False
        )
    
    except KeyboardInterrupt:
        print("\n👋 Shutting down gracefully...")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")

if __name__ == '__main__':
    main()
