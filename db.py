import sqlite3
import pandas as pd

DB_PATH = "noc.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_conn() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS captures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT UNIQUE,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS calls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            capture_id INTEGER,
            call_id TEXT,
            invite_ts TEXT,
            final_ts TEXT,
            final_status TEXT,
            pdd REAL,
            duration REAL
        );

        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            capture_id INTEGER,
            rule_name TEXT,
            severity TEXT,
            message TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """)

def insert_capture(filename):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO captures (filename) VALUES (?)", (filename,))
    cur.execute("SELECT id FROM captures WHERE filename = ?", (filename,))
    cid = cur.fetchone()["id"]
    conn.commit()
    conn.close()
    return cid

def insert_calls(cid, calls):
    conn = get_conn()
    cur = conn.cursor()
    for c in calls:
        cur.execute("""
            INSERT INTO calls
            (capture_id, call_id, invite_ts, final_ts, final_status, pdd, duration)
            VALUES (?,?,?,?,?,?,?)
        """, (
            cid,
            c["call_id"],
            c["invite_ts"],
            c["final_ts"],
            c["final_status"],
            c["pdd"],
            c["duration"]
        ))
    conn.commit()
    conn.close()

def get_recent(limit=200):
    conn = get_conn()
    calls = pd.read_sql_query(
        "SELECT * FROM calls ORDER BY invite_ts DESC LIMIT ?", 
        conn, params=(limit,)
    )
    alerts = pd.read_sql_query(
        "SELECT * FROM alerts ORDER BY created_at DESC LIMIT 30",
        conn
    )
    captures = pd.read_sql_query(
        "SELECT * FROM captures ORDER BY created_at DESC LIMIT 10",
        conn
    )
    conn.close()
    return calls, alerts, captures
