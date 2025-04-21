import streamlit as st
import os
import sys

# Ensure local imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.db import get_all_reps, get_rep_by_zip

st.set_page_config(page_title="Admin Panel", layout="wide")

st.title("🛠 Admin Dashboard")
st.markdown("Use this panel to manage representative data and monitor application behavior.")

st.divider()

# 🔍 View all known ZIP-to-Rep mappings
st.subheader("📬 Known ZIP Code Mappings")
if st.button("Load ZIP → Rep Mappings"):
    try:
        all_reps = get_all_reps()
        if all_reps:
            for row in all_reps:
                st.write(f"**ZIP:** {row[0]} → **{row[1]}** ({row[2]}) [{row[3]}]")
        else:
            st.info("No reps found in the database.")
    except Exception as e:
        st.error(f"Error fetching reps: {e}")

st.divider()

# 🧪 Manual rep lookup
st.subheader("🔍 Manual Rep Lookup by ZIP")
manual_zip = st.text_input("Enter ZIP Code")
if manual_zip:
    rep = get_rep_by_zip(manual_zip.strip())
    if rep:
        st.success(f"{rep[0]} – {rep[1]} ({rep[2]})")
    else:
        st.warning("No rep found for that ZIP.")