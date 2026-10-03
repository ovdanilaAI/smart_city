import sqlite3
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Utility Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_NAME = "services/utility/utility.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS issues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INT,
            category TEXT,
            description TEXT,
            status TEXT
        )
    """)
    cur.execute("SELECT COUNT(*) FROM issues")
    if cur.fetchone()[0] == 0:
        cur.execute(
            "INSERT INTO issues (user_id, category, description, status) VALUES (?, ?, ?, ?)",
            (1, "Водоснабжение", "Прорыв трубы во дворе", "in_progress")
        )
    conn.commit()
    conn.close()

init_db()

@app.get("/issues")
def get_issues():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT id, user_id, category, description, status FROM issues ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return [{"id": r[0], "user_id": r[1], "category": r[2], "description": r[3], "status": r[4]} for r in rows]

@app.post("/issues")
def create_issue(data: dict):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO issues (user_id, category, description, status) VALUES (?, ?, ?, 'pending')",
        (data.get("user_id", 1), data.get("category", "Общее"), data["description"])
    )
    issue_id = cur.lastrowid
    conn.commit()
    conn.close()

    # Синхронное фоновое уведомление в Notification Service (порт 8006)
    try:
        requests.post(
            "http://127.0.0.1:8006/notifications",
            json={
                "user_id": data.get("user_id", 1),
                "message": f"Заявка ЖКХ #{issue_id} '{data['description']}' создана!"
            },
            timeout=2
        )
    except Exception as e:
        print(f"Ошибка отправки уведомления: {e}")

    return {"status": "created", "issue_id": issue_id}
