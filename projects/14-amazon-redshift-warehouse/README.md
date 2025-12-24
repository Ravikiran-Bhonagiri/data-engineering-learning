# Foundation Project 14: Data Warehousing (Amazon Redshift)

## 🎯 Goal
Master **MPP (Massively Parallel Processing) Data Warehousing**. We will efficiently load massive datasets from S3 into Redshift using the `COPY` command, the only scalable way to ingest data.

## 🛑 The "INSERT INTO" Problem
*   **Junior Mistake:** Looping through a CSV in Python and running `INSERT INTO table VALUES (...)` for every row.
*   **Result:** It takes 24 hours to load 1GB. The database locks up.
*   **The Pro Way:** The `COPY` command asks the Redshift Cluster to pull data from S3 *in parallel* across all nodes. It can load TBs in minutes.

## 🛠️ The Solution: Redshift COPY
1.  **Parallelism:** Each slice of the cluster reads a part of the file(s).
2.  **Compression:** Redshift analyzes the data on-the-fly to apply columnar compression (LZO/ZSTD).
3.  **Manifests:** Control exactly which files to load.

## 🏗️ Architecture
1.  **Source:** S3 Bucket (Parquet files).
2.  **Warehouse:** Redshift Cluster (ra3.xlplus).
3.  **DDL:** Sort Keys (for speed) and Distribution Keys (for join performance).

## 🚀 How to Run (Simulation)
This requires a running Redshift cluster.
1.  **SQL:** `load_data.sql` contains the DDL and COPY commands.
2.  **Driver:** `trigger_load.py` uses `psycopg2` (standard Postgres driver) to send the commands.
