import sqlite3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Transport Service")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
DB_NAME = "transport.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS vehicles (id INTEGER PRIMARY KEY, name TEXT, lat REAL, lon REAL, status TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS parkings (id INTEGER PRIMARY KEY, address TEXT, total_spots INT, available_spots INT)")
    
    cur.execute("SELECT COUNT(*) FROM vehicles")
    if cur.fetchone()[0] == 0:
        cur.executemany("INSERT INTO vehicles (name, lat, lon, status) VALUES (?, ?, ?, ?)", [
            ("Автобус #101", 55.7558, 37.6173, "active"),
            ("Электросамокат #42", 55.7522, 37.6155, "available")
        ])
        cur.executemany("INSERT INTO parkings (address, total_spots, available_spots) VALUES (?, ?, ?)", [
            ("ул. Ленина, д. 10", 50, 12),
            ("Парк Горького", 100, 45)
        ])
    conn.commit()
    conn.close()

init_db()

@app.get("/vehicles")
def get_vehicles():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM vehicles")
    rows = cur.fetchall()
    conn.close()
    return [{"id": r[0], "name": r[1], "lat": r[2], "lon": r[3], "status": r[4]} for r in rows]

@app.get("/parking")
def get_parkings():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM parkings")
    rows = cur.fetchall()
    conn.close()
    return [{"id": r[0], "address": r[1], "total_spots": r[2], "available_spots": r[3]} for r in rows]
