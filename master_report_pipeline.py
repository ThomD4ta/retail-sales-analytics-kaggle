import os
import sys
import traceback
from datetime import datetime
from pathlib import Path

# =========================================================
# Imports from your modular scripts
# =========================================================
try:
    from Sales_to_pgadmin import run_sales_to_pgadmin
except ImportError:
    def run_sales_to_pgadmin():
        raise ImportError("Could not import 'run_sales_to_pgadmin' from sales_to_pgadmin.py")

try:
    from sql_scripts.run_all_bi_sql import run_all_bi_queries
except ImportError:
    def run_all_bi_queries():
        raise ImportError("Could not import 'run_all_bi_queries' from run_all_bi_sql.py")

try:
    from report_scripts.kaggle_ecom_report import build_report
except ImportError:
    def build_report():
        raise ImportError("Could not import 'build_report' from kaggle_ecom_report.py")

# =========================================================
# Logging utilities
# =========================================================
def log(msg: str, level: str = "INFO"):
    """Simple color-coded console logger."""
    colors = {
        "INFO": "\033[94m",     # Blue
        "SUCCESS": "\033[92m",  # Green
        "ERROR": "\033[91m",    # Red
        "STEP": "\033[96m",     # Cyan
        "ENDC": "\033[0m",      # Reset
    }
    prefix = f"[{level}]"
    print(f"{colors.get(level, '')}{prefix} {msg}{colors['ENDC']}")


# =========================================================
# Main Orchestration Logic
# =========================================================
def run_pipeline():
    start_time = datetime.now()
    log("Starting Full BI Orchestration Pipeline", "STEP")
    log(f"Start Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}", "INFO")

    try:
        # ---------------------------------------------
        # 1️⃣ Extract & Load to Postgres
        # ---------------------------------------------
        log("Step 1: Loading Kaggle data → PostgreSQL", "STEP")
        run_sales_to_pgadmin()
        log("✅ Step 1 Completed Successfully", "SUCCESS")

        # ---------------------------------------------
        # 2️⃣ Run SQL Transformations (BI Views)
        # ---------------------------------------------
        log("Step 2: Running BI SQL transformations", "STEP")
        run_all_bi_queries()
        log("✅ Step 2 Completed Successfully", "SUCCESS")

        # ---------------------------------------------
        # 3️⃣ Generate Report
        # ---------------------------------------------
        log("Step 3: Building Excel Report and Charts", "STEP")
        build_report()
        log("✅ Step 3 Completed Successfully", "SUCCESS")

    except Exception as e:
        log("❌ Pipeline failed!", "ERROR")
        log(str(e), "ERROR")
        traceback.print_exc()
        sys.exit(1)

    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    log(f"🎉 Pipeline completed successfully in {duration:.2f} seconds", "SUCCESS")


# =========================================================
# Entry Point
# =========================================================
if __name__ == "__main__":
    run_pipeline()