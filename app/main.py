import streamlit as st
import os
import sys
from pathlib import Path

# Add import paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.db import init_db, get_rep_by_zip, get_rep_by_name, upsert_rep
from services.civic_lookup import fetch_rep_from_google

st.set_page_config(page_title="We The Watchers", layout="wide")

# Admin button (top-right)
st.markdown("""
<style>
.admin-button {
    position: absolute;
    top: 16px;
    right: 20px;
    z-index: 999;
}
html, body, [class*="css"]  {
    font-family: 'Helvetica Neue', sans-serif;
}
.card {
    flex: 1 0 23%;
    background-color: #fff;
    padding: 16px;
    border-radius: 10px;
    border: 1px solid #ddd;
    text-align: center;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    max-width: 250px;
}
.rep-button {
    background-color: #3366ff;
    color: white;
    border: none;
    border-radius: 5px;
    padding: 8px;
    width: 100%;
    cursor: pointer;
    font-weight: 500;
}
</style>
<div class='admin-button'>
    <a href="/admin" target="_self">
        <button class='rep-button'>🛠 Admin</button>
    </a>
</div>
""", unsafe_allow_html=True)

# Init DB
DB_PATH = "database/we_watchers.db"
init_db()

# --- Header ---
st.markdown("""
<div style='text-align: center; padding-top: 2rem;'>
    <h1 style='font-size: 2.5em;'>See what your elected officials are doing — and who it’s helping</h1>
    <p style='font-size: 1.1em;'>Track trades, votes, donations, and possible conflicts of interest.<br>Just enter your ZIP or search by name.</p>
</div>
""", unsafe_allow_html=True)

# --- Search ---
st.markdown("<br>", unsafe_allow_html=True)
with st.container():
    col_zip, col_button = st.columns([4, 1])
    with col_zip:
        zip_code = st.text_input("", placeholder="Enter ZIP code")
    with col_button:
        search = st.button("Browse by State / County / name")

st.markdown("<br>", unsafe_allow_html=True)

# --- Red Flag Feed ---
st.markdown("<h4 style='color: #b30000;'>Red Flag Feed</h4>", unsafe_allow_html=True)
alerts = [
    ("Rep. Smith bought 120K of Lockheed stock before defense vote", True),
    ("Rep. Jones voted on crypto bill while holding Coinbase shares", True),
    ("Sen. Lee sponsored a bill to regulate Big Tech after selling Google stock", True)
]
for alert, has_link in alerts:
    st.markdown(f"""
    <div style='display: flex; justify-content: space-between;'>
        <span style='color: #aa0000;'>🔴 {alert}</span>
        <a href='#' style='font-size: 0.9em;'>View Full Report</a>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- Filters ---
st.markdown("<h4>Find Your Representative</h4>", unsafe_allow_html=True)
col_name, col_chamber, col_party, col_state = st.columns([4, 2, 2, 2])
with col_name:
    rep_name = st.text_input("", placeholder="Start typing a name...")
with col_chamber:
    st.selectbox("Chamber", ["All", "House", "Senate"])
with col_party:
    st.selectbox("Party", ["All", "Democratic", "Republican", "Independent"])
with col_state:
    st.selectbox("State", ["All", "CA", "TX", "NY", "FL"])

# --- Rep Data ---
rep = None
if zip_code and search:
    zip_code = zip_code.strip().replace("-", "")
    rep_local = get_rep_by_zip(zip_code)
    if not rep_local or rep_local[0].strip().lower() == "unlisted rep":
        rep = fetch_rep_from_google(zip_code)
        if rep and rep["name"].lower() != "unlisted rep":
            upsert_rep(zip_code, rep["name"], rep["party"], rep["state"])
    else:
        rep = {
            "name": rep_local[0],
            "party": rep_local[1],
            "state": rep_local[2]
        }

# --- Rep Cards ---
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<div style='display: flex; flex-wrap: wrap; gap: 20px;'>", unsafe_allow_html=True)

if rep:
    rep_cards = [rep]
else:
    rep_cards = [
        {"name": "Ted Cruz", "state": "TX", "party": "R", "votes": 78, "trades": 12, "flags": 1},
        {"name": "Alexandria Ocasio-Cortez", "state": "NY", "party": "D", "votes": 56, "trades": 3, "flags": 0},
        {"name": "Jim Jordan", "state": "OH", "party": "R", "votes": 54, "trades": 6, "flags": 2},
        {"name": "Katie Porter", "state": "CA", "party": "D", "votes": 72, "trades": 0, "flags": 0}
    ]

for r in rep_cards:
    st.markdown(f"""
        <div class='card'>
            <h5>{r['name']}</h5>
            <p>{r['state']} – {r['party']}</p>
            <p>🗳 {r.get('votes', 'N/A')} Votes<br>💸 {r.get('trades', 'N/A')} Trades<br>🚩 {r.get('flags', 'N/A')} Flags</p>
            <a href="/dashboard?name={r['name']}" style='text-decoration: none;'>
                <button class='rep-button'>View Profile</button>
            </a>
        </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
