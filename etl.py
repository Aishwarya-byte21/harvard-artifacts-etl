import requests
import time
import mysql.connector
from db import get_connection

API_KEY = "5f2b0854-29dc-4775-ba56-1c3b66a34f46"


# ---------------- CREATE TABLES ----------------
def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS artifact_metadata (
        id INT PRIMARY KEY,
        title TEXT,
        culture TEXT,
        period TEXT,
        century TEXT,
        medium TEXT,
        dimensions TEXT,
        description TEXT,
        department TEXT,
        classification TEXT,
        accessionyear INT,
        accessionmethod TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS artifact_media (
        objectid INT,
        imagecount INT,
        mediacount INT,
        colorcount INT,
        media_rank INT,
        datebegin INT,
        dateend INT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS artifact_colors (
        objectid INT,
        color TEXT,
        spectrum TEXT,
        hue TEXT,
        percent FLOAT,
        css3 TEXT
    )
    """)

    conn.commit()
    conn.close()


# ---------------- FETCH ARTIFACTS ----------------
def fetch_artifacts(classification, limit=2500):
    records = []
    page = 1
    retries = 3

    while len(records) < limit:
        url = "https://api.harvardartmuseums.org/object"
        params = {
            "apikey": API_KEY,
            "classification": classification,
            "size": 100,
            "page": page
        }

        try:
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json().get("records", [])

            if not data:
                break

            records.extend(data)
            page += 1
            time.sleep(0.3)

        except requests.exceptions.RequestException:
            if retries > 0:
                retries -= 1
                time.sleep(2)
                continue
            else:
                break

    return records[:limit]


# ---------------- INSERT DATA ----------------
def insert_data(records):
    conn = get_connection()
    cur = conn.cursor()

    for r in records:
        # ---- METADATA ----
        cur.execute("""
        INSERT IGNORE INTO artifact_metadata (
            id, title, culture, period, century, medium,
            dimensions, description, department,
            classification, accessionyear, accessionmethod
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            r.get("id"),
            r.get("title"),
            r.get("culture"),
            r.get("period"),
            r.get("century"),
            r.get("medium"),
            r.get("dimensions"),
            r.get("description"),
            r.get("department"),
            r.get("classification"),
            r.get("accessionyear"),
            r.get("accessionmethod")
        ))

        # ---- MEDIA ----
        cur.execute("""
        INSERT INTO artifact_media (
            objectid, imagecount, mediacount,
            colorcount, media_rank, datebegin, dateend
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (
            r.get("id"),
            r.get("imagecount"),
            r.get("mediacount"),
            r.get("colorcount"),
            r.get("rank"),
            r.get("datebegin"),
            r.get("dateend")
        ))

        # ---- COLORS ----
        for c in r.get("colors", []):
            cur.execute("""
            INSERT INTO artifact_colors (
                objectid, color, spectrum, hue, percent, css3
            )
            VALUES (%s,%s,%s,%s,%s,%s)
            """, (
                r.get("id"),
                c.get("color"),
                c.get("spectrum"),
                c.get("hue"),
                c.get("percent"),
                c.get("css3")
            ))

    conn.commit()
    conn.close()
