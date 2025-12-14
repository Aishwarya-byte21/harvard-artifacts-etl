import streamlit as st
import pandas as pd
from etl import fetch_artifacts, create_tables, insert_data
from db import get_connection
from queries import queries

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Harvard Artifacts Collection",
    page_icon="🏛️",
    layout="wide"
)

# ---------- HEADER ----------
st.title("🏛️ Harvard Artifacts Collection")
st.caption("ETL • SQL Analytics • Streamlit Dashboard")

st.divider()

# ---------- SESSION STATE ----------
if "data" not in st.session_state:
    st.session_state["data"] = []

# ---------- DATA INGESTION ----------
st.subheader("📥 Data Ingestion")

classification = st.selectbox(
    "Select Classification",
    ["Coins", "Sculpture", "Paintings", "Jewelry", "Drawings"]
)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🛠️ Create Tables"):
        create_tables()
        st.success("Tables created")

with col2:
    if st.button("🌐 Fetch Data"):
        with st.spinner("Fetching data from Harvard API..."):
            st.session_state["data"] = fetch_artifacts(classification)
        st.success(f"Fetched {len(st.session_state['data'])} records")

with col3:
    if st.button("💾 Insert into SQL"):
        if len(st.session_state["data"]) == 0:
            st.error("Fetch data first")
        else:
            insert_data(st.session_state["data"])
            st.success("Data inserted into SQL")

st.divider()

# ---------- SQL QUERY SECTION ----------
st.subheader("🔍 SQL Query Explorer")

selected_query = st.selectbox(
    "Choose a SQL Query",
    list(queries.keys())
)

if st.button("▶ Run Query"):
    conn = get_connection()
    df = pd.read_sql(queries[selected_query], conn)
    st.dataframe(df, use_container_width=True)
