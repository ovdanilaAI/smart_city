import sqlite3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Billing Service")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
DB_NAME = "billing.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS invoices (id INTEGER PRIMARY KEY, user_id INT, amount REAL, status TEXT)")
    cur.execute("SELECT COUNT(*) FROM invoices")
    if cur.fetchone()[0] == 0:
        cur.executemany("INSERT INTO invoices (user_id, amount, status) VALUES (?, ?, ?)", [
            (1, 1500.50, "pending"),
            (1, 3200.00, "paid")
        ])
    conn.commit()
    conn.close()

init_db()

@app.get("/accounts/{user_id}/invoices")
def get_invoices(user_id: int):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM invoices WHERE user_id=?", (user_id,))
    rows = cur.fetchall()
    conn.close()
    return [{"id": r[0], "user_id": r[1], "amount": r[2], "status": r[3]} for r in rows]
