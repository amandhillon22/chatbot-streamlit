import psycopg2
import hashlib
import uuid
import sys
sys.path.append('/home/linux/Documents/chatbot-diya')

from datetime import datetime
from src.core.sql import db_manager

class UserManager:
    def __init__(self):
        pass
    
    def get_connection(self):
        """Get database connection using the new context manager"""
        return db_manager.get_connection_context()
    
    def hash_password(self, password):
        """Simple MD5 hash for password (in production, use bcrypt)"""
        return hashlib.md5(password.encode()).hexdigest()
    
    def authenticate_user(self, username, password):
        """Authenticate user with username and password"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                password_hash = self.hash_password(password)
                cursor.execute(
                    "SELECT id, username FROM users WHERE username = %s AND password_hash = %s",
                    (username, password_hash)
                )
                
                user = cursor.fetchone()
                
                if user:
                    # Update last login
                    cursor.execute(
                        "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = %s",
                        (user[0],)
                    )
                    conn.commit()
                    
                    return {
                        'id': user[0],
                        'username': user[1],
                        'authenticated': True
                    }
                
                return {'authenticated': False}
                
        except Exception as e:
            print(f"Authentication error: {e}")
            return {'authenticated': False}
    
    def create_user(self, username, password):
        """Create a new user"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                password_hash = self.hash_password(password)
                cursor.execute(
                    "INSERT INTO users (username, password_hash) VALUES (%s, %s) RETURNING id",
                    (username, password_hash)
                )
                
                user_id = cursor.fetchone()[0]
                conn.commit()
            
            return {
                'id': user_id,
                'username': username,
                'created': True
            }
            
        except psycopg2.IntegrityError:
            return {'created': False, 'error': 'Username already exists'}
        except Exception as e:
            print(f"User creation error: {e}")
            return {'created': False, 'error': str(e)}

class ChatHistoryManager:
    def __init__(self):
        pass
    
    def get_connection(self):
        """Get database connection using the new manager"""
        return db_manager.get_connection()
    
    def create_chat_session(self, user_id, title=None):
        """Create a new chat session"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            session_id = str(uuid.uuid4())
            if not title:
                title = f"Chat {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            
            cursor.execute(
                """INSERT INTO chat_sessions (user_id, session_id, title) 
                   VALUES (%s, %s, %s) RETURNING id""",
                (user_id, session_id, title)
            )
            
            chat_session_id = cursor.fetchone()[0]
            conn.commit()
            
            return {
                'session_db_id': chat_session_id,
                'session_id': session_id,
                'title': title,
                'created': True
            }
            
        except Exception as e:
            print(f"Chat session creation error: {e}")
            return {'created': False, 'error': str(e)}
    
    def save_message(self, session_id, message_type, content, sql_query=None):
        """Save a message to chat history"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Get session database ID
            cursor.execute(
                "SELECT id, title FROM chat_sessions WHERE session_id = %s",
                (session_id,)
            )
            session_data = cursor.fetchone()
            
            if not session_data:
                print(f"Session not found: {session_id}")
                return {'saved': False, 'error': 'Session not found'}
            
            session_db_id, current_title = session_data
            
            cursor.execute(
                """INSERT INTO chat_messages (session_id, message_type, content, sql_query) 
                   VALUES (%s, %s, %s, %s)""",
                (session_db_id, message_type, content, sql_query)
            )
            
            # Auto-update session title if it's the first user message and title is generic
            if message_type == 'user' and current_title == 'New Chat':
                # Create a meaningful title from the user's first message
                title_words = content.strip().split()[:4]  # First 4 words
                new_title = ' '.join(title_words)
                if len(content) > 30:
                    new_title += '...'
                
                cursor.execute(
                    "UPDATE chat_sessions SET title = %s WHERE id = %s",
                    (new_title, session_db_id)
                )
            
            # Update session timestamp
            cursor.execute(
                "UPDATE chat_sessions SET updated_at = CURRENT_TIMESTAMP WHERE id = %s",
                (session_db_id,)
            )
            
            conn.commit()
            return {'saved': True}
            
        except Exception as e:
            print(f"Message save error: {e}")
            return {'saved': False, 'error': str(e)}
    
    def get_user_chat_sessions(self, user_id, limit=20):
        """Get recent chat sessions for a user"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                """SELECT session_id, title, created_at, updated_at 
                   FROM chat_sessions 
                   WHERE user_id = %s 
                   ORDER BY updated_at DESC 
                   LIMIT %s""",
                (user_id, limit)
            )
            
            sessions = []
            for row in cursor.fetchall():
                sessions.append({
                    'session_id': row[0],
                    'title': row[1],
                    'created_at': row[2].isoformat() if row[2] else None,
                    'updated_at': row[3].isoformat() if row[3] else None
                })
            
            return {'sessions': sessions}
            
        except Exception as e:
            print(f"Get sessions error: {e}")
            return {'sessions': [], 'error': str(e)}
    
    def get_chat_history(self, session_id):
        """Get chat history for a specific session"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                """SELECT cm.message_type, cm.content, cm.sql_query, cm.created_at 
                   FROM chat_messages cm
                   JOIN chat_sessions cs ON cm.session_id = cs.id
                   WHERE cs.session_id = %s 
                   ORDER BY cm.created_at ASC""",
                (session_id,)
            )
            
            messages = []
            for row in cursor.fetchall():
                messages.append({
                    'type': row[0],
                    'content': row[1],
                    'sql_query': row[2],
                    'timestamp': row[3].isoformat() if row[3] else None
                })
            
            return {'messages': messages}
            
        except Exception as e:
            print(f"Get chat history error: {e}")
            return {'messages': [], 'error': str(e)}
    
    def update_session_title(self, session_id, title):
        """Update chat session title"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                "UPDATE chat_sessions SET title = %s WHERE session_id = %s",
                (title, session_id)
            )
            
            conn.commit()
            return {'updated': True}
            
        except Exception as e:
            print(f"Update session title error: {e}")
            return {'updated': False, 'error': str(e)}
    
    def delete_chat_session(self, session_id, user_id):
        """Delete a chat session (with user verification)"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                "DELETE FROM chat_sessions WHERE session_id = %s AND user_id = %s",
                (session_id, user_id)
            )
            
            conn.commit()
            return {'deleted': True}
            
        except Exception as e:
            print(f"Delete session error: {e}")
            return {'deleted': False, 'error': str(e)}

# Global instances
user_manager = UserManager()
chat_history_manager = ChatHistoryManager()
