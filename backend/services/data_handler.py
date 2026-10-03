import sys
import pandas as pd

if len(sys.argv) < 2:
    print("No file path provided")
    sys.exit(1)

file_path = sys.argv[1]

try:
    df = pd.read_csv(file_path)
    print(f"Columns: {list(df.columns)}")
    print(f"Number of rows: {len(df)}")
except Exception as e:
    print(f"Error reading CSV: {e}")
