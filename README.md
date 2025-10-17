# retail-sales-analytics-kaggle
Case Study: API/html Request + Exploratory Data Analysis + Report + Power BI Dashboard

Main ETL Script: master_report_pipeline.py

1. Run sales_to_pgadmin logic (Kaggle API Request)
2. Run all BI SQL queries (CSV export)
3. Run report builder (Excel)
4. PowerBI Dashboard

[Kaggle Dataset] --> [Sales_to_pgadmin.py] --> [Postgres DB]
                                            \
                                             -> [run_all_bi_sql.py] --> [CSV outputs]
                                                                            \
                                                                             -> [Kaggle_ecom_report.py] --> [Excel]


**TL;DR:** Request downloads a retail sales dataset from Kaggle, normalizes the CSV, 
and bulk loads the data into a PostgreSQL table (`retail_sales`) using Python + `psycopg2`. 
It also writes a small `run_log` entry in the DB on each run.

---

## Features
- Download dataset via `kaggle_dataset.py` (Kaggle helper).
- Normalize column names and select mapped columns.
- Create schema and table if missing.
- Bulk load CSV into PostgreSQL via `COPY` for speed.
- Insert run metadata into `run_log`.
- Safe environment-based credentials (no plaintext secrets).


