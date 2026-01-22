import sqlite3
import os

DB_PATH = "data/users.db"


def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

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


def add_user(username, password, profile="standard"):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        c.execute(
            "INSERT INTO users (username, password, profile) VALUES (?, ?, ?)",
            (username, password, profile)
        )

        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def login_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = c.fetchone()
    conn.close()
    return user
