# Advanced Project 27: Athena CTAS (SQL ETL)

## 🎯 Goal
Master **SQL-Based ETL**. We will use **CTAS (Create Table As Select)** to transform raw, messy JSON/CSV data into optimized **Parquet/Snappy** tables fully managed by Athena, skipping Glue Jobs entirely for simpler transformations.

## 🛑 The "Glue Job Overkill" Problem
*   **Scenario:** You just need to convert CSV to Parquet and rename a column.
*   **Overkill:** Writing a PySpark script, provisioning DPUs, waiting for spin-up (3 mins).
*   **Solution (CTAS):** Run a standard SQL query. Athena reads the CSV, writes the Parquet files to S3, and registers the new table. Cost: $5/TB scanned. Time: Seconds.

## 🛠️ The Solution: WITH Parameters
CTAS allows specifying storage formats:
```sql
WITH (
     format = 'PARQUET',
     parquet_compression = 'SNAPPY',
     external_location = 's3://...'
)
```

## 🏗️ Architecture
1.  **Source:** `raw_logs` (JSON, GZIP, unsorted).
2.  **Transformation:** SQL (`SELECT upper(name)...`).
3.  **Target:** `clean_logs` (Parquet, Snappy, Partitioned).

## 🚀 How to Run (Simulation)
1.  **Code:** `run_ctas.sql`.
2.  **Run:** Paste into Athena Console.
