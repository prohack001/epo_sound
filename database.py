import sqlite3

DB_PATH = "chat_sessions.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Table pour les utilisateurs
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    # Table pour les sessions
    c.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        session_name TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    # Table pour les messages
    c.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id INTEGER NOT NULL,
        sender TEXT NOT NULL,
        message TEXT NOT NULL,
        FOREIGN KEY (session_id) REFERENCES sessions(id)
    )
    """)

    conn.commit()
    conn.close()

def get_user_by_credentials(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, username FROM users WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()
    conn.close()
    return user

def get_user_sessions(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, session_name FROM sessions WHERE user_id = ?", (user_id,))
    sessions = c.fetchall()
    conn.close()
    return sessions

def get_session_messages(session_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT sender, message FROM messages WHERE session_id = ?", (session_id,))
    messages = c.fetchall()
    conn.close()
    return messages

def add_message(session_id, sender, message):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO messages (session_id, sender, message) VALUES (?, ?, ?)", (session_id, sender, message))
    conn.commit()
    conn.close()

def create_new_session(user_id, session_name):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO sessions (user_id, session_name) VALUES (?, ?)", (user_id, session_name))
    conn.commit()
    conn.close()
