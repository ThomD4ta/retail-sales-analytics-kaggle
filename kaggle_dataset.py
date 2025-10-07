import os
import csv
import pandas as pd
import kagglehub
from datetime import datetime


def main():
    # 1. Download kaggle dataset with the latest version
    path = kagglehub.dataset_download("mohammadtalib786/retail-sales-dataset")
    print("Path to dataset files:", path)

    # 2. List the files in the dataset folder after downloading, listdir
    files = os.listdir(path)
    print("Files in dataset folder:", files)

    # 3. Find and load the CSV file (loop)
    csv_file = None
    for f in files:
        if f.endswith(".csv"):
            csv_file = os.path.join(path, f)
            break

    if csv_file is None:
        raise FileNotFoundError("❌ No CSV file found in the dataset folder.")
    else:
        print(f"✅ Loading CSV file: {csv_file}")

    # 4. Inspect the CSV file headers with csv
    with open(csv_file, newline='', encoding='utf-8') as fh:
        reader = csv.reader(fh)
        header = next(reader)
    print("Columns:", header)

    # 5. Load the CSV file into a DataFrame
    df = pd.read_csv(csv_file)
    # print(df.info()) # to inspect data types

    # 6. Add a DS column to the DataFrame with today's date in YYYY-MM-DD format
    df['DS'] = datetime.now().strftime('%Y-%m-%d')

    # 7. Print the first 5 rows of the CSV file
    print("First 5 rows of the dataset:")
    print(df.head())  # shows top 5 rows

    # 8. Use the output_file variable to create a .csv file
    output_file = "retail_sales.csv"

    # 9. Save the DataFrame to CSV, overwriting if it exists
    df.to_csv(output_file, index=False)
    print(f"✅ Output file saved successfully: {output_file}")
    # print(df.describe()) # to inspect summary statistics

    # 10 New addition to be imported to Sales_to_pgadmin.py
    return output_file   # 👈 Now the function explicitly hands back the file path when called from another script.

# Optional: allow standalone run
if __name__ == "__main__":
    main()