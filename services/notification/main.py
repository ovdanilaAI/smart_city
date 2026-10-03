import sqlite3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Notification Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_NAME = "services/notification/notification.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INT,
            message TEXT,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cur.execute("SELECT COUNT(*) FROM notifications")
    if cur.fetchone()[0] == 0:
        cur.execute(
            "INSERT INTO notifications (user_id, message, status) VALUES (?, ?, ?)",
            (1, "Добро пожаловать в систему Умный Город!", "sent")
        )
    conn.commit()
    conn.close()

init_db()

@app.get("/notifications")
def get_notifications():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT id, user_id, message, status, created_at FROM notifications ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return [{"id": r[0], "user_id": r[1], "message": r[2], "status": r[3], "created_at": r[4]} for r in rows]

@app.post("/notifications")
def send_notification(data: dict):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO notifications (user_id, message, status) VALUES (?, ?, 'sent')",
        (data.get("user_id", 1), data.get("message", "Новое уведомление"))
    )
    conn.commit()
    conn.close()
    return {"status": "sent"}
