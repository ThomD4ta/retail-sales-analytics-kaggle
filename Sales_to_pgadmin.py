# load_csv_to_postgres.py
import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql
import pandas as pd
from io import StringIO
from datetime import datetime
from kaggle_dataset import main as fetch_kaggle_data # ✅ Including kaggle_dataset.py into the pipeline

load_dotenv()

PG_HOST = os.getenv("PG_HOST", "localhost")
PG_PORT = os.getenv("PG_PORT", "5432")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_DATABASE = os.getenv("PG_DATABASE")
PG_SCHEMA = os.getenv("PG_SCHEMA", "public")
TABLE = "retail_sales"
CSV_PATH = fetch_kaggle_data()

# 1. Read CSV from kaggle_dataset.py
df = pd.read_csv(CSV_PATH)

# Normalize CSV column names
df.columns = (
    df.columns
      .str.strip()
      .str.lower()
      .str.replace(" ", "_")
      .str.replace(r"[^\w_]", "", regex=True)
)

# 2. Ensure columns and types to post in pgadmin4
# Example mapping: adapt to your actual data
col_defs = {
    "transaction_id": "text",
    "date": "date",
    "customer_id": "text",
    "gender": "text",
    "age": "integer",
    "product_category": "text",
    "quantity": "integer",
    "price_per_unit": "numeric",
    "total_amount": "numeric",
    "ds": "date"
}

# 3. Create Data template for SQL table: Reconcile col_defs with actual df columns
#   keep only columns present in df
final_columns = [c for c in df.columns if c in col_defs]
column_sql_parts = [f"{c} {col_defs[c]}" for c in final_columns]


# 4. Create SQL table function, using psycopg2.sql
create_table_sql = sql.SQL(
    "CREATE TABLE IF NOT EXISTS {}.{} ({});"
).format(
    sql.Identifier(PG_SCHEMA),
    sql.Identifier(TABLE),
    sql.SQL(", ").join(sql.SQL(part) for part in column_sql_parts)
)

# 5. Connect to PostgresSQL, open the tunnel between python and the DB
conn = psycopg2.connect(
    host=PG_HOST,
    port=PG_PORT,
    dbname=PG_DATABASE,
    user=PG_USER,
    password=PG_PASSWORD
)

# 6. Create Schema and SQL Table if missing, commit
try:
    with conn:
        with conn.cursor() as cur:
            # Create schema if not exists
            cur.execute(
                sql.SQL("CREATE SCHEMA IF NOT EXISTS {}").format(sql.Identifier(PG_SCHEMA))
            )
            # Create table if not exists
            cur.execute(create_table_sql)
            conn.commit()

            # 7. CSV data to postgreSQL: Prepare CSV buffer only with final_columns in the right order
            buf = StringIO()
            df[final_columns].to_csv(buf, index=False, header=True)
            buf.seek(0)

            # Optional: truncate or append. Here we append. To replace data and has the DS data updated, use TRUNCATE first.
            cur.execute(sql.SQL("TRUNCATE TABLE {}.{}").format(sql.Identifier(PG_SCHEMA), sql.Identifier(TABLE)))
            copy_sql = sql.SQL("COPY {}.{} ({}) FROM STDIN WITH CSV HEADER").format(
                sql.Identifier(PG_SCHEMA),
                sql.Identifier(TABLE),
                sql.SQL(", ").join(sql.Identifier(c) for c in final_columns)
            )
            cur.copy_expert(copy_sql, buf)

            # Insert a run log (optional)
            # Create run_log table if not exists
            cur.execute(sql.SQL("""
                CREATE TABLE IF NOT EXISTS {}.run_log (
                    id serial PRIMARY KEY,
                    run_ts timestamptz DEFAULT now(),
                    ds date,
                    rows_loaded integer,
                    source_file text
                );
            """).format(sql.Identifier(PG_SCHEMA)))

            cur.execute(
                sql.SQL("INSERT INTO {}.run_log (ds, rows_loaded, source_file) VALUES (%s, %s, %s)")
                   .format(sql.Identifier(PG_SCHEMA)),
                (datetime.now().date(), len(df), os.path.basename(CSV_PATH))
            )

    print(f"✅ Loaded {len(df)} rows into {PG_SCHEMA}.{TABLE} on pgadmin4")
finally:
    conn.close()