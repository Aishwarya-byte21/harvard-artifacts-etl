import streamlit as st
import requests
import sqlite3
import pandas as pd
import time

# ==================================================
# CONFIG
# ==================================================
API_KEY = "5f2b0854-29dc-4775-ba56-1c3b66a34f46"
BASE_URL = "https://api.harvardartmuseums.org/object"
DB_NAME = "database.db"

st.set_page_config(page_title="Harvard’s Artifacts Collection", layout="wide")

# ==================================================
# DATABASE CONNECTION
# ==================================================
conn = sqlite3.connect(DB_NAME, check_same_thread=False)
cursor = conn.cursor()

# ==================================================
# CREATE TABLES
# ==================================================
def create_tables():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS artifact_metadata (
        id INTEGER PRIMARY KEY,
        title TEXT,
        culture TEXT,
        dated TEXT,
        period TEXT,
        division TEXT,
        medium TEXT,
        dimensions TEXT,
        department TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS artifact_media (
        objectid INTEGER,
        imagecount INTEGER,
        mediacount INTEGER,
        colorcount INTEGER,
        media_rank INTEGER,
        datebegin INTEGER,
        dateend INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS artifact_colors (
        objectid INTEGER,
        color TEXT,
        spectrum TEXT,
        hue TEXT,
        percent REAL,
        css3 TEXT
    )
    """)
    conn.commit()

create_tables()

# ==================================================
# COLLECT DATA (2500 RECORDS)
# ==================================================
def collect_data(classification, limit=2500):
    records = []
    page = 1

    while len(records) < limit:
        params = {
            "apikey": API_KEY,
            "classification": classification,
            "size": 100,
            "page": page
        }

        response = requests.get(BASE_URL, params=params)
        if response.status_code != 200:
            break

        data = response.json()
        if "records" not in data or len(data["records"]) == 0:
            break

        records.extend(data["records"])
        page += 1
        time.sleep(0.25)

    return records[:limit]

# ==================================================
# SPLIT DATA
# ==================================================
def split_data(records):
    metadata, media, colors = [], [], []

    for r in records:
        metadata.append({
            "id": r.get("id"),
            "title": r.get("title"),
            "culture": r.get("culture"),
            "dated": r.get("dated"),
            "period": r.get("period"),
            "division": r.get("division"),
            "medium": r.get("medium"),
            "dimensions": r.get("dimensions"),
            "department": r.get("department")
        })

        media.append({
            "objectid": r.get("id"),
            "imagecount": r.get("imagecount"),
            "mediacount": r.get("mediacount"),
            "colorcount": r.get("colorcount"),
            "media_rank": r.get("rank"),
            "datebegin": r.get("datebegin"),
            "dateend": r.get("dateend")
        })

        if r.get("colors"):
            for c in r["colors"]:
                colors.append({
                    "objectid": r.get("id"),
                    "color": c.get("color"),
                    "spectrum": c.get("spectrum"),
                    "hue": c.get("hue"),
                    "percent": c.get("percent"),
                    "css3": c.get("css3")
                })

    return pd.DataFrame(metadata), pd.DataFrame(media), pd.DataFrame(colors)

# ==================================================
# INSERT DATA (IGNORE DUPLICATES)
# ==================================================
def insert_into_sql(meta_df, media_df, color_df):

    # ---- METADATA (PRIMARY KEY SAFE) ----
    for _, row in meta_df.iterrows():
        cursor.execute("""
            INSERT OR IGNORE INTO artifact_metadata
            (id, title, culture, dated, period, division, medium, dimensions, department)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row["id"],
            row["title"],
            row["culture"],
            row["dated"],
            row["period"],
            row["division"],
            row["medium"],
            row["dimensions"],
            row["department"]
        ))

    # ---- MEDIA ----
    media_df.to_sql("artifact_media", conn, if_exists="append", index=False)

    # ---- COLORS ----
    color_df.to_sql("artifact_colors", conn, if_exists="append", index=False)

    conn.commit()
# ==================================================
# GET ALL CLASSIFICATIONS FROM HARVARD API
# ==================================================
def get_all_classifications():
    url = "https://api.harvardartmuseums.org/classification"
    params = {
        "apikey": API_KEY,
        "size": 100
    }

    response = requests.get(url, params=params)
    data = response.json()

    classifications = []
    for item in data.get("records", []):
        name = item.get("name")
        if name:
            classifications.append(name)

    return sorted(classifications)

# ==================================================
# STREAMLIT UI
# ==================================================
st.title("🏛️ Harvard’s Artifacts Collection")

all_classifications = get_all_classifications()

classification = st.selectbox(
    "Select a classification",
    all_classifications
)

if "records" not in st.session_state:
    st.session_state.records = []

# --------------------------------------------------
# COLLECT DATA
# --------------------------------------------------
if st.button("📥 Collect data"):
    st.session_state.records = collect_data(classification)
    st.success(f"Collected {len(st.session_state.records)} records")

# --------------------------------------------------
# SHOW METADATA | MEDIA | COLOURS
# --------------------------------------------------
if st.session_state.records:
    meta_df, media_df, color_df = split_data(st.session_state.records)

    st.subheader("Collected Data Preview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### Metadata")
        st.dataframe(meta_df.head(10), use_container_width=True)

    with col2:
        st.markdown("### Media")
        st.dataframe(media_df.head(10), use_container_width=True)

    with col3:
        st.markdown("### Colours")
        st.dataframe(color_df.head(10), use_container_width=True)

    st.markdown("---")

    # --------------------------------------------------
    # INSERT BUTTON
    # --------------------------------------------------
    st.subheader("Insert the collected data")

    if st.button("Insert"):
        insert_into_sql(meta_df, media_df, color_df)
        st.success("Data Inserted successfully")

# ==================================================
# SQL QUERIES SECTION
# ==================================================
import queries

st.markdown("---")
st.subheader("🔍 SQL Queries")

query_question = st.selectbox(
    "Select a query",
    list(queries.queries.keys())
)

if st.button("Run Query"):
    result_df = pd.read_sql_query(
        queries.queries[query_question],
        conn
    )
    st.dataframe(result_df, use_container_width=True)
