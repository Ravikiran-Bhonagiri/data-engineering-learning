# Foundation Project 5: Open Table Formats (Apache Iceberg)

## 🎯 Goal
Master the **Open Table Format** standard that competes with Delta Lake. We will use **AWS Glue** and **Amazon Athena** to manage an Apache Iceberg table, performing ACID transactions and Time Travel queries.

## 🛑 The "Parquet" Problem
Standard Data Lakes use plain parquet files.
*   **No ACID:** If a job fails halfway through writing, you have 500 partial files. Readers see broken data.
*   **No Updates:** To change one row, you have to rewrite the entire partition.
*   **Performance:** Partitioning is physical (`/dates=2024-01-01/`). If you want to query by month, the engine has to scan everything.

## 🛠️ The Solution: Apache Iceberg
Iceberg adds a metadata layer over Parquet:
1.  **ACID Transactions:** Writes are atomic. Readers never see partial data.
2.  **Hidden Partitioning:** You can partition by `days(timestamp)`, but query by `hours(timestamp)`. Iceberg handles the math. Partitioning is logical, not just physical.
3.  **Time Travel:** Query `FOR SYSTEM_TIME AS OF ...`.

## 🏗️ Architecture
1.  **Catalog:** AWS Glue Data Catalog.
2.  **Storage:** AWS S3.
3.  **Engine:** Amazon Athena (Serverless SQL).
4.  **Client:** Python (`awswrangler`) to trigger DDL/DML.

## 🚀 How to Run
*Prerequisites: Logged into AWS CLI.*

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Script
```bash
python manage_iceberg.py
```
This script will:
1.  Create an Iceberg table in Glue.
2.  Insert records.
3.  Perform an **Upsert** (Merge) operation.
4.  Run a Time Travel query to see the data before the update.
