import requests
import yaml
import sqlite3
from pathlib import Path

DB_PATH = "database/we_watchers.db"
GITHUB_YAML = "https://raw.githubusercontent.com/unitedstates/congress-legislators/main/legislators-current.yaml"

def create_database():
    Path("database").mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS representatives (
        id TEXT PRIMARY KEY,
        full_name TEXT,
        state TEXT,
        party TEXT,
        zip_code TEXT
    )
    """)
    conn.commit()
    conn.close()

def fetch_and_insert():
    response = requests.get(GITHUB_YAML)
    if response.status_code != 200:
        print("❌ Failed to fetch data:", response.status_code)
        return

    data = yaml.safe_load(response.text)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # 🔧 Force-assign ZIPs to specific reps (if their ID is found)
    zip_map = {
        "A000360": "92646",  # Dana Rohrabacher (example)
        "P000197": "94110",
        "S001193": "90210",
        "O000173": "10001",
        "C001075": "33101",
    }

    assigned_zips = set()

    for member in data:
        rep_id = member.get("id", {}).get("bioguide")
        name = member.get("name", {})
        terms = member.get("terms", [])
        if not rep_id or not terms:
            continue

        full_name = f"{name.get('first', '')} {name.get('last', '')}".strip()
        party = terms[-1].get("party", "Unknown")
        state = terms[-1].get("state", "N/A")
        zip_code = zip_map.get(rep_id)

        if zip_code:
            assigned_zips.add(zip_code)
            print(f"✅ Assigned ZIP {zip_code} to {full_name}")

        c.execute("""
            INSERT OR REPLACE INTO representatives (id, full_name, state, party, zip_code)
            VALUES (?, ?, ?, ?, ?)
        """, (rep_id, full_name, state, party, zip_code))

    # ✅ Ensure any ZIPs not matched still have dummy entries
    for zip_val in zip_map.values():
        if zip_val not in assigned_zips:
            print(f"⚠️  No match found for ZIP {zip_val} — inserting dummy rep.")
            c.execute("""
                INSERT OR IGNORE INTO representatives (id, full_name, state, party, zip_code)
                VALUES (?, ?, ?, ?, ?)
            """, (f"DUMMY_{zip_val}", "Unlisted Rep", "NA", "NA", zip_val))

    conn.commit()
    conn.close()
    print("✅ Representatives populated into DB")

if __name__ == "__main__":
    create_database()
    fetch_and_insert()