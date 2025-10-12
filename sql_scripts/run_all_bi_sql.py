#!/usr/bin/env python3
"""
Run all SQL files that contain "_bi_" in their filename from two folders:
 - sql/sql_queries
 - sql/views

Behavior:
 - Runs all BI SQL files automatically.
 - SELECT/WITH queries → Fetch results → Save as CSV in data_outputs/bi/
 - CREATE/INSERT/UPDATE → Executes and commits changes.
 - Errors are caught per file so execution continues.
"""

# ============================================================
# 1️⃣ Import libraries and load environment variables
# ============================================================
import os
from pathlib import Path
import psycopg2
import pandas as pd
from dotenv import load_dotenv
import traceback

load_dotenv()

# ============================================================
# 2️⃣ Load PostgreSQL credentials from .env
# ============================================================
PG_HOST = os.getenv("PG_HOST", "localhost")
PG_PORT = os.getenv("PG_PORT", "5432")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_DATABASE = os.getenv("PG_DATABASE")
PG_SCHEMA = os.getenv("PG_SCHEMA", "public")

# ============================================================
# 3️⃣ Define project paths
# ============================================================
BASE_DIR = Path(r"C:\Users\admin\.cursor\retail-sales-analytics-kaggle")
SQL_QUERIES_DIR = BASE_DIR / "sql" / "sql_queries"
VIEWS_DIR = BASE_DIR / "sql" / "views"
OUTPUT_DIR = BASE_DIR / "data_outputs" / "bi"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# 4️⃣ Helper functions
# ============================================================

def read_sql_file(path: Path) -> str:
    """Read and return SQL file content."""
    return path.read_text(encoding="utf-8")

def format_sql_filename(filename: str) -> str:
    """Convert '25_bi_sales_summary.sql' → 'Sales Summary'."""
    name = Path(filename).stem
    parts = name.split("_")
    clean_parts = [p for p in parts if not p.isdigit() and p.lower() not in ("bi", "view")]
    return " ".join(clean_parts).title() or name

def first_keyword(sql_text: str) -> str:
    """Identify the first SQL keyword (e.g., SELECT, CREATE, INSERT)."""
    for line in sql_text.splitlines():
        s = line.strip()
        if not s or s.startswith("--") or s.startswith("/*"):
            continue
        return s.split()[0].upper()
    return ""

def find_bi_and_view_sql_files(*folders):
    """Search given folders for files containing '_bi_' or '_view_'."""
    files = []
    for folder in folders:
        if not folder.exists():
            continue
        for f in sorted(folder.iterdir()):
            if (
                f.is_file()
                and f.suffix.lower() == ".sql"
                and ("_bi_" in f.name.lower() or "_view_" in f.name.lower())
            ):
                files.append(f)
    return files

# ============================================================
# 5️⃣ Main function to run BI SQL files
# ============================================================
def run_all_bi_queries():
     # Step 5.1 — Find all _bi_ and _view_ SQL files
    sql_files = find_bi_and_view_sql_files(SQL_QUERIES_DIR, VIEWS_DIR)
    if not sql_files:
        print("⚠️ No _bi_ or _view_ SQL files found in folders.")
        return

    print(f"📁 Found {len(sql_files)} BI/VIEW SQL files. Running them...\n")

    # Step 5.2 — Open PostgreSQL connection once
    conn = psycopg2.connect(
        host=PG_HOST, 
        port=PG_PORT, 
        user=PG_USER, 
        password=PG_PASSWORD, 
        dbname=PG_DATABASE
    )

    try:
        # Step 5.3 — Loop through each SQL file
        for sql_path in sql_files:
            try:
                sql_text = read_sql_file(sql_path)
                title = format_sql_filename(sql_path.name)
                print(f"\n---\n📄 File: {sql_path.name}\n📌 Title: {title}")

                kw = first_keyword(sql_text)

                # Step 5.4 — If it's a SELECT/WITH query → fetch results
                if kw in ("SELECT", "WITH"):
                    df = pd.read_sql(sql_text, conn)
                    print(f"▶ Rows fetched: {len(df)}")
                    print(df.head(5).to_string(index=False))
                    out_csv = OUTPUT_DIR / f"{sql_path.stem}.csv"
                    df.to_csv(out_csv, index=False)
                    print(f"✅ Saved CSV: {out_csv}")

                # Step 5.5 — If it's DDL/DML → execute and commit
                else:
                    with conn.cursor() as cur:
                        cur.execute(sql_text)
                    conn.commit()
                    print(f"✅ Executed DDL/DML (keyword: {kw})")

            except Exception as e:
                print(f"❌ Error in {sql_path.name}: {e}")
                traceback.print_exc()

    finally:
        # Step 5.6 — Close DB connection
        conn.close()
        print("\n🔒 Connection closed.")

# ============================================================
# 6️⃣ Run script
# ============================================================
if __name__ == "__main__":
    run_all_bi_queries()