#!/usr/bin/env python3
"""
report_builder.py
Place this file under report_scripts/ in your project.

Purpose:
- Load selected CSVs from data_outputs/bi/ (or all when MANUAL_CSV_LIST is empty)
- Create outputs under report_scripts_outcome/:
    - reports/report_ecom_kaggle.xlsx         (Excel workbook with each dataset as a sheet)
    - report_charts_and_images/   (PNG images for generated charts)
- No HTML is produced (per request)
- Each helper function includes detailed notes explaining purpose and usage

How to use:
- Edit MANUAL_CSV_LIST to list the CSV stem names you want (no .csv), or leave [] to include all.
- Run: python report_scripts/kaggle_ecom_report.py
"""

# =========================================================
# 0️⃣ Imports
# =========================================================
from pathlib import Path
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

# =========================================================
# 1. Configuration — Edit these
# =========================================================
BASE_DIR = Path(__file__).resolve().parents[1]      # project/
BI_CSV_DIR = BASE_DIR / "data_outputs" / "bi"       # where CSVs are stored

OUTCOME_ROOT = BASE_DIR / "report_scripts_outcome"
REPORTS_DIR = OUTCOME_ROOT / "reports"
CHARTS_DIR = OUTCOME_ROOT / "report_charts_and_images"

# Ensure output folders exist
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
CHARTS_DIR.mkdir(parents=True, exist_ok=True)

# MANUAL_CSV_LIST: list the CSV filenames you want in the report (without extension)
# If empty list -> include all CSVs found in BI_CSV_DIR
MANUAL_CSV_LIST = [
    # e.g. "25_bi_category_performance_by_gender"
    # leave empty [] to include all available CSVs
"01_view_dataset_totals.csv",
"02_view_monthly_transactions.csv",
"24_bi_total_count_by_category_desc.csv",
"03_view_product_category_performance.csv",
"18_bi_top_5_max_orders_by_total_amount.csv",
"19_bi_top_5_min_orders_by_total_amount.csv",
"17_bi_percentiles_outliers_total_amount.csv",
"04_view_monthly_mom",
"05_view_monthly_ytd_performance",
"06_view_sales_and_customers_mom_ytd",
"07_view_product_category_sales_by_month",
"08_view_sales_and_customers_mom_ytd",
"09_view_percentiles_by_order_amount"
]

# =========================================================
# 2. Helper functions — detailed notes for each function
# =========================================================

def safe_read_csv(path: Path) -> pd.DataFrame:
    """
    Read CSV into a pandas DataFrame safely.

    Notes:
    - Input: path (Path object) pointing to a .csv file.
    - Returns: DataFrame on success, or None on failure.
    - Why: CSVs can be malformed or locked; catching exceptions prevents the whole script from crashing.
    - Implementation details: uses pandas.read_csv with default options.
      You can customize with dtype, parse_dates, or chunksize for very large files.
    """
    try:
        df = pd.read_csv(path)
        return df
    except Exception as e:
        # Print to stderr so logs/CI can separate error messages
        print(f"⚠️ Failed to read {path.name}: {e}", file=sys.stderr)
        return None


def safe_save_png(fig, out_path: Path):
    """
    Save a matplotlib Figure to disk and close it to free memory.

    Notes:
    - Input: fig (matplotlib.figure.Figure), out_path (Path)
    - Ensures the figure is written with bbox_inches='tight' to avoid cropped labels.
    - After saving, closes the figure via plt.close(fig) to avoid memory leaks when generating many charts.
    - If saving fails (e.g., permission issue), exception will propagate to caller (not swallowed).
    """
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)


def try_parse_date_column(df: pd.DataFrame):
    """
    Attempt to find a sensible date-like column in the DataFrame.

    Strategy:
    1. Look for common column names (case-insensitive): date, ds, order_date, sale_date, transaction_date.
       For each candidate, attempt pd.to_datetime() with errors='coerce' and check whether any values parsed.
    2. If none of the candidates worked, inspect dtypes and return the first datetime64-like column found.
    3. If still nothing, return None.

    Returns:
    - column name string if found, else None.

    Why:
    - Many CSVs use different date column names. This function tries practical heuristics so downstream
      plotting code can choose a date axis automatically.
    """
    candidates = [c for c in df.columns if c.lower() in ("date", "ds", "order_date", "sale_date", "transaction_date")]
    for c in candidates:
        try:
            parsed = pd.to_datetime(df[c], errors="coerce")
            if parsed.notna().sum() > 0:
                return c
        except Exception:
            # If parsing raises, ignore this candidate and continue
            continue
    # fallback: check actual dtype for datetime64
    for c in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[c]):
            return c
    return None


def numeric_columns(df: pd.DataFrame):
    """
    Return a list of numeric column names.

    Notes:
    - Uses pandas' is_numeric_dtype for robust numeric-type detection.
    - Useful to pick default metrics (e.g., totals, amounts) for charts or KPIs.
    - Returns an empty list if none found.
    """
    return [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]


def timeseries_plot(df: pd.DataFrame, date_col: str, value_col: str):
    """
    Create a daily time-series matplotlib Figure for the specified date and value columns.

    Inputs:
    - df: DataFrame containing date_col and value_col
    - date_col: column name containing dates (will be coerced to datetime)
    - value_col: numeric column to aggregate (sum) by day

    Behavior:
    - Coerces date_col to datetime (errors -> NaT)
    - Drops rows where either date_col or value_col is missing
    - Aggregates by day (resample 'D') using sum
    - If aggregated series is empty, returns a figure with a short message

    Returns:
    - matplotlib Figure object (caller should save and close using safe_save_png)
    """
    tmp = df.copy()
    tmp[date_col] = pd.to_datetime(tmp[date_col], errors="coerce")
    tmp = tmp.dropna(subset=[date_col, value_col])
    fig, ax = plt.subplots(figsize=(10, 4))
    if tmp.empty:
        ax.text(0.5, 0.5, "No data for time series", ha="center")
        return fig
    series = tmp.set_index(date_col).sort_index()[value_col].resample("D").sum()
    ax.plot(series.index, series.values)
    ax.set_title(f"Daily {value_col}")
    ax.set_xlabel("Date")
    ax.set_ylabel(value_col)
    ax.grid(True)
    plt.tight_layout()
    return fig


def top_n_barplot(df: pd.DataFrame, group_col: str, value_col: str, n: int = 10):
    """
    Create a top-n bar chart (matplotlib Figure) aggregating value_col by group_col.

    Inputs:
    - df: DataFrame
    - group_col: categorical/string column to group by
    - value_col: numeric column to aggregate (sum)
    - n: number of top groups to keep

    Behavior:
    - Groups df by group_col, sums value_col, sorts descending and keeps top n
    - Builds a bar chart with rotated x labels for readability

    Returns:
    - matplotlib Figure object (caller should save and close using safe_save_png)

    Notes:
    - group_col should be suitable as a category (not extremely high cardinality).
    - If aggregation yields fewer than n groups, it will plot whatever exists.
    """
    agg = df.groupby(group_col)[value_col].sum().sort_values(ascending=False).head(n)
    fig, ax = plt.subplots(figsize=(8, 4))
    agg.plot(kind="bar", ax=ax)
    ax.set_title(f"Top {n} {group_col} by sum({value_col})")
    ax.set_xlabel(group_col)
    ax.set_ylabel(value_col)
    ax.tick_params(axis="x", rotation=45)
    plt.tight_layout()
    return fig


# =========================================================
# 3. Gather CSVs (manual list or all)
# =========================================================
def gather_datasets(bi_csv_dir: Path, manual_list):
    """
    Collects CSV files and returns a dict: {stem: DataFrame}.

    Parameters:
    - bi_csv_dir: Path to folder containing CSVs
    - manual_list: list of stems (no .csv) or filenames; when empty -> include all CSVs

    Returns:
    - dict mapping file stem -> pandas DataFrame for each successfully read file

    Behavior details:
    - Normalizes manual_list to lowercase stems for matching against available files.
    - Warns if a requested file is missing, but continues.
    - Reads each CSV with safe_read_csv and reports shape (rows x cols) on success.
    """
    datasets = {}
    if not bi_csv_dir.exists():
        print(f"❌ CSV folder not found: {bi_csv_dir}", file=sys.stderr)
        return datasets

    manual_stems = [str(x).lower().replace(".csv", "") for x in manual_list] if manual_list else []

    files = sorted(bi_csv_dir.glob("*.csv"))
    if manual_stems:
        wanted = []
        available_stems = [f.stem.lower() for f in files]
        for s in manual_stems:
            if s in available_stems:
                f = next(f for f in files if f.stem.lower() == s)
                wanted.append(f)
            else:
                print(f"⚠️ Requested CSV not found: {s}.csv", file=sys.stderr)
        files = wanted

    for f in files:
        df = safe_read_csv(f)
        if df is not None:
            datasets[f.stem] = df
            print(f"✅ Loaded {f.name} ({df.shape[0]} rows, {df.shape[1]} cols)")
    return datasets


# =========================================================
# 4. Build the report (no HTML, Excel + charts only)
# =========================================================
    # base_dir and manual_csv_list addtion
def build_report(  
    base_dir: Path = None,
    manual_csv_list: list = None
):
    """
    Main entry point to build the Excel report and save charts.

    Steps:
    1. Gather datasets (respect MANUAL_CSV_LIST)
    2. Create an Excel workbook in REPORTS_DIR/report_ecom_kaggle.xlsx with one sheet per dataset
    3. For each dataset:
         - Detect simple KPIs (candidate columns like total_amount/revenue)
         - Generate timeseries PNG if date + numeric metric exist
         - Generate top-N barplot PNG if a categorical column exists
    4. Save images to CHARTS_DIR and Excel workbook to REPORTS_DIR
    """
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n🔧 Building report at {now_str}")

    datasets = gather_datasets(BI_CSV_DIR, MANUAL_CSV_LIST)
    if not datasets:
        print("⚠️ No datasets to report on. Exiting.")
        return

    excel_path = REPORTS_DIR / "report_ecom_kaggle.xlsx"

    # ===== IMPROVEMENT NOTE =====
    # Using a single 'with pd.ExcelWriter' context to write all datasets to separate sheets.
    # This prevents overwriting, ensures proper file closure, and avoids PermissionError on Windows.
    with pd.ExcelWriter(excel_path, engine="openpyxl") as excel_writer:
        for name, df in datasets.items():
            sheet_name = name[:31]  # Excel sheet name limit
            try:
                df.to_excel(excel_writer, sheet_name=sheet_name, index=False)
                print(f"📄 Sheet added: {sheet_name}")
            except Exception as e:
                print(f"⚠️ Could not write {sheet_name}: {e}", file=sys.stderr)

    print(f"✅ Excel report saved to: {excel_path}")

# =========================================================
# 5. Script entry point
# =========================================================
if __name__ == "__main__":
    build_report()
