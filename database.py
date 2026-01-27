import sqlite3

def init_db(db_path="data/users.db"):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Create users table if not exists
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            profile TEXT DEFAULT 'standard'
        )
    """)
    conn.commit()
    conn.close()


def add_user(username, password, profile="standard", db_path="data/users.db"):
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password, profile) VALUES (?, ?, ?)",
                  (username, password, profile))
        conn.commit()
        conn.close()
        return "User added successfully ✅"
    except sqlite3.IntegrityError:
        return "Username already exists ❌"


def login_user(username, password, db_path="data/users.db"):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    return user