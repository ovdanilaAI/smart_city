import sqlite3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Environment Service")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
DB_NAME = "environment.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS sensors (id INTEGER PRIMARY KEY, location TEXT, type TEXT)")
    cur.execute("SELECT COUNT(*) FROM sensors")
    if cur.fetchone()[0] == 0:
        cur.executemany("INSERT INTO sensors (location, type) VALUES (?, ?)", [
            ("Центральный парк", "Качество воздуха (AQI)"),
            ("Промзона #3", "Уровень шума (дБ)")
        ])
    conn.commit()
    conn.close()

init_db()

@app.get("/sensors")
def get_sensors():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM sensors")
    rows = cur.fetchall()
    conn.close()
    return [{"id": r[0], "location": r[1], "type": r[2]} for r in rows]
