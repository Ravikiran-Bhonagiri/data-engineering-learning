import pandas as pd
import sys
from datetime import datetime

def run_etl():
    print(f"[{datetime.now()}] Starting ETL Job...")
    
    # 1. Simulate Extraction
    data = {
        "id": [1, 2, 3],
        "name": ["Alice", "Bob", "Charlie"],
        "amount": [100.50, 200.00, 50.25]
    }
    df = pd.DataFrame(data)
    print("Extracted Data:")
    print(df)
    
    # 2. Simulate Transformation
    # Apply a 10% tax
    df['tax'] = df['amount'] * 0.10
    df['total'] = df['amount'] + df['tax']
    
    print("\nTransformed Data:")
    print(df)
    
    # 3. Simulate Load
    print(f"\nLoaded {len(df)} records to Data Warehouse.")
    print(f"[{datetime.now()}] Job Finished Successfully.")

if __name__ == "__main__":
    print(f"Python Version: {sys.version}")
    run_etl()
