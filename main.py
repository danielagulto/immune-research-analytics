from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import sqlite3, random, json
from datetime import date, timedelta

BASE = Path(__file__).resolve().parent
DB_PATH = BASE / "immune_research.db"
app = FastAPI(title="Immune Research Analytics API", version="1.0.0")
app.mount("/static", StaticFiles(directory=BASE / "static"), name="static")

def connect():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    con = connect()
    con.execute("""CREATE TABLE IF NOT EXISTS samples (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sample_code TEXT UNIQUE NOT NULL,
        cohort TEXT NOT NULL,
        collection_date TEXT NOT NULL,
        cd4_count REAL NOT NULL,
        cd8_count REAL NOT NULL,
        b_cell_pct REAL NOT NULL,
        inflammation_score REAL NOT NULL,
        response_group TEXT NOT NULL
    )""")
    count = con.execute("SELECT COUNT(*) FROM samples").fetchone()[0]
    if count == 0:
        rng = random.Random(2026)
        cohorts = ["Cohort A", "Cohort B", "Cohort C"]
        groups = ["Responder", "Partial response", "Non-responder"]
        today = date.today()
        rows = []
        for i in range(1, 91):
            group = rng.choices(groups, weights=[0.42, 0.33, 0.25])[0]
            inflammation = max(0.2, min(9.8, rng.gauss(3.2 if group == "Responder" else 5.6, 1.35)))
            rows.append((
                f"IM-{i:04d}", rng.choice(cohorts),
                (today - timedelta(days=rng.randint(0, 180))).isoformat(),
                round(max(150, rng.gauss(850 if group == "Responder" else 650, 150)), 1),
                round(max(80, rng.gauss(520 if group == "Responder" else 680, 140)), 1),
                round(max(2, min(35, rng.gauss(14, 4))), 1),
                round(inflammation, 2), group
            ))
        con.executemany("""INSERT INTO samples
            (sample_code, cohort, collection_date, cd4_count, cd8_count, b_cell_pct, inflammation_score, response_group)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", rows)
    con.commit()
    con.close()

@app.on_event("startup")
def startup():
    init_db()

@app.get("/", response_class=HTMLResponse)
def home():
    return (BASE / "static" / "index.html").read_text(encoding="utf-8")

@app.get("/api/summary")
def summary():
    con = connect()
    total = con.execute("SELECT COUNT(*) FROM samples").fetchone()[0]
    averages = con.execute("""SELECT AVG(cd4_count) cd4, AVG(cd8_count) cd8,
        AVG(b_cell_pct) bcell, AVG(inflammation_score) inflammation FROM samples""").fetchone()
    groups = con.execute("SELECT response_group label, COUNT(*) value FROM samples GROUP BY response_group").fetchall()
    cohorts = con.execute("SELECT cohort label, COUNT(*) value FROM samples GROUP BY cohort ORDER BY cohort").fetchall()
    trend = con.execute("""SELECT substr(collection_date,1,7) month,
        ROUND(AVG(inflammation_score),2) inflammation, COUNT(*) samples
        FROM samples GROUP BY month ORDER BY month""").fetchall()
    con.close()
    return {
        "total_samples": total,
        "averages": {k: round(averages[k], 2) for k in averages.keys()},
        "response_groups": [dict(r) for r in groups],
        "cohorts": [dict(r) for r in cohorts],
        "monthly_trend": [dict(r) for r in trend],
        "notice": "Synthetic demo data only. Not for clinical use."
    }

@app.get("/api/samples")
def samples(q: str = Query(default="", max_length=80), cohort: str = "", response_group: str = ""):
    sql = "SELECT * FROM samples WHERE 1=1"
    params = []
    if q:
        sql += " AND sample_code LIKE ?"
        params.append(f"%{q}%")
    if cohort:
        sql += " AND cohort = ?"
        params.append(cohort)
    if response_group:
        sql += " AND response_group = ?"
        params.append(response_group)
    sql += " ORDER BY collection_date DESC LIMIT 200"
    con = connect()
    rows = con.execute(sql, params).fetchall()
    con.close()
    return {"items": [dict(r) for r in rows], "count": len(rows)}

@app.get("/api/health")
def health():
    return {"status": "ok", "database": "sqlite", "data": "synthetic"}
