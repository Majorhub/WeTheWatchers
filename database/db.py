import sqlite3
from pathlib import Path

# Path to your SQLite DB
DB_PATH = "database/we_watchers.db"

def init_db():
    """Ensure reps table exists."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS reps (
            zip TEXT PRIMARY KEY,
            name TEXT,
            party TEXT,
            state TEXT
        )
    """)
    conn.commit()
    conn.close()

def get_rep_by_zip(zip_code):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT name, party, state FROM reps WHERE zip = ?", (zip_code,))
    row = c.fetchone()
    conn.close()
    if row:
        return row
    return ("Unlisted Rep", "NA", "NA")

def get_rep_by_name(name):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT name, party, state FROM reps WHERE LOWER(name) = LOWER(?)", (name,))
    row = c.fetchone()
    conn.close()
    return row

def get_all_reps():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT zip, name, party, state FROM reps ORDER BY zip")
    rows = c.fetchall()
    conn.close()
    return rows

def upsert_rep(zip_code, name, party, state):
    """Insert or update a rep based on ZIP code."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO reps (zip, name, party, state)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(zip) DO UPDATE SET
            name = excluded.name,
            party = excluded.party,
            state = excluded.state
    """, (zip_code, name, party, state))
    conn.commit()
    conn.close()