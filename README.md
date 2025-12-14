# Harvard Artifacts ETL Project

## 📌 Project Overview
This project extracts artifact data from the **Harvard Art Museums API**, transforms it, stores it in a **MySQL database**, and visualizes insights using a **Streamlit dashboard**.

---

## 🛠 Tech Stack
- Python
- MySQL
- Streamlit
- Harvard Art Museums API
- Git & GitHub

---

## 🔄 ETL Pipeline
1. **Extract** artifact data by classification (Coins, Sculpture, etc.)
2. **Transform** JSON responses into structured formats
3. **Load** data into MySQL tables:
   - `artifact_metadata`
   - `artifact_media`
   - `artifact_colors`

---

## 📊 SQL Analytics
25 SQL queries were implemented to analyze:
- Artifact counts by classification
- Medium and culture analysis
- Date range insights
- Color usage patterns
- Media availability

---

## 🖥 Streamlit Dashboard
- Interactive classification selector
- ETL control buttons (Create Tables, Fetch Data, Insert into SQL)
- SQL analytics display

---

## 🚀 How to Run
```bash
pip install -r requirements.txt
streamlit run app.py
