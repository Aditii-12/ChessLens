import sqlite3

def init_db(db_path="data/users.db"):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        password TEXT
    )""")
    conn.commit()
    conn.close()

def add_user(u, p, db_path="data/users.db"):
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("INSERT INTO users VALUES(NULL,?,?)",(u,p))
        conn.commit()
        conn.close()
        return "User added"
    except:
        return "User exists"

def login_user(u, p, db_path="data/users.db"):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (u,p))
    r = c.fetchone()
    conn.close()
    return r
