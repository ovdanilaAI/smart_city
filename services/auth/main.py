import sqlite3
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Auth Service")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
DB_NAME = "auth.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] == 0:
        cur.executemany("INSERT INTO users (email, password_hash, full_name) VALUES (?, ?, ?)", [
            ("admin@smartcity.ru", "hash123", "Иван Иванов"),
            ("user@smartcity.ru", "hash456", "Петр Петров")
        ])
    conn.commit()
    conn.close()

init_db()

@app.get("/users")
def list_users():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT id, email, full_name FROM users")
    rows = cur.fetchall()
    conn.close()
    return [{"id": r[0], "email": r[1], "full_name": r[2]} for r in rows]
