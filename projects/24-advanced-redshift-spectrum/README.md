# Advanced Project 24: Redshift Spectrum (Data Virtualization)

## 🎯 Goal
Master **Hybrid Warehousing**. We will use **Redshift Spectrum** to join "Hot" data stored on high-performance SSDs (Redshift Nodes) with "Cold" data stored cheaply on S3, *without loading the cold data*.

## 🛑 The "Storage Cost" Problem
*   **Scenario:** You have 1 Petabyte of historical logs (10 years). Access is rare.
*   **Problem:** Storing 1PB on Redshift `ra3.xlplus` nodes costs a fortune ($$$$). Loading it takes days.
*   **Solution (Spectrum):** Keep the 1PB on S3 ($). Define an "External Table" in Redshift. Query it using standard SQL. Redshift spins up thousands of ephemeral "Spectrum Writers" to scan S3 in parallel during the query.

## 🛠️ The Solution: External Schemas
We don't use `CREATE TABLE`. We use `CREATE EXTERNAL SCHEMA` which points to the **AWS Glue Data Catalog** (Project 13).
*   Redshift becomes a query engine over your Data Lake.

## 🏗️ Architecture
1.  **Local Table:** `recent_sales` (Last 3 months, on SSD).
2.  **External Table:** `spectrum.historical_sales_archive` (Last 10 years, on S3 Parquet).
3.  **Query:** `JOIN` them together seamlessly.

## 🚀 How to Run (Simulation)
1.  **Code:** `spectrum_query.sql`.
2.  **Execution:** Run in Redshift Query Editor v2.
    *   *Note: This requires an IAM Role with `AmazonRedshiftAllCommandsFullAccess` and `AmazonS3ReadOnlyAccess`.*
