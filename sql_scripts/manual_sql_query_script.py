# Script ideal to run queries manually from both folders sql_queries and views
import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv

# 1. Load environment variables (PostgreSQL credentials)
load_dotenv()

PG_HOST = os.getenv("PG_HOST", "localhost")
PG_PORT = os.getenv("PG_PORT", "5432")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_DATABASE = os.getenv("PG_DATABASE")
PG_SCHEMA = os.getenv("PG_SCHEMA", "public")

# 2. Define your project structure
BASE_DIR = r"C:\Users\admin\.cursor\retail-sales-analytics-kaggle"
SQL_QUERIES_DIR = os.path.join(BASE_DIR, "sql", "sql_queries")
VIEWS_DIR = os.path.join(BASE_DIR, "sql", "views")

# 3. Create a helper function to read SQL files
def read_sql_file(folder_path, filename):
    """Reads and returns the SQL content from a file."""
    file_path = os.path.join(folder_path, filename)
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

# 4. Helper: turn filename into readable title
def format_sql_filename(filename):
    """Turns '25_bi_category_performance_by_gender.sql' → 'Category Performance By Gender'"""
    name = os.path.splitext(filename)[0]  # remove .sql
    # Remove any prefix like numbers or 'bi_'
    parts = name.split("_")
    # Filter out numeric and technical prefixes
    clean_parts = [p for p in parts if not p.isdigit() and p.lower() not in ("bi", "view")]
    # Join words and capitalize
    return " ".join(clean_parts).title()

# 5. Assign your SQL queries to easy variable names
file_query_1 = "05_bi_dataset_quick_sample.sql"

# Optional: you can change BASE_DIR to "sql_queries" if needed
file_query_2 = "01_view_dataset_totals.sql"

# variable names assigned
sql_query_1 = read_sql_file(SQL_QUERIES_DIR, file_query_1)

# Optional: you can change BASE_DIR to "sql_queries" if needed
sql_query_2 = read_sql_file(VIEWS_DIR, file_query_2)

# 6. Connect to PostgreSQL ONCE (best practice)
conn = psycopg2.connect(
    host=PG_HOST,
    port=PG_PORT,
    user=PG_USER,
    password=PG_PASSWORD,
    dbname=PG_DATABASE
)

# 7. Run your queries — and store results in DataFrames
df_query_1 = pd.read_sql(sql_query_1, conn)
df_query_2 = pd.read_sql(sql_query_2, conn)

# 8. Preview and verify results — now includes filenames
print(f"\n📄 Running File: {file_query_1}")
print(f"📊 Query 1 Title: {format_sql_filename(file_query_1)}")
print(df_query_1.head())

print(f"\n📄 Running File: {file_query_2}")
print(f"📊 Query 2 Title: {format_sql_filename(file_query_2)}")
print(df_query_2.head())


# ========================================================================================================
# 9. Optional — Save to CSV for later use (now stores in data_outputs/sql_manual_runs)
OUTPUT_DIR = os.path.join(BASE_DIR, "data_outputs", "sql_manual_runs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

df_query_1.to_csv(os.path.join(OUTPUT_DIR, f"{os.path.splitext(file_query_1)[0]}.csv"), index=False)
df_query_2.to_csv(os.path.join(OUTPUT_DIR, f"{os.path.splitext(file_query_2)[0]}.csv"), index=False)

# ========================================================================================================

# 10. Close the connection
conn.close()

print("\n✅ SQL queries executed, previewed, and saved successfully!")
