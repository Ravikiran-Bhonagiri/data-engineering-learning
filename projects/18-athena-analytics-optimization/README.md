# Foundation Project 18: Ad-Hoc Analytics (Amazon Athena)

## 🎯 Goal
Master **Serverless SQL Optimization**. We will create an Athena table using **Partition Projection**, a technique that allows you to query petabytes of S3 data instantaneously by "calculating" partition locations instead of looking them up.

## 🛑 The "Metastore" Problem
*   **Standard Hive:** unique partitions (`date=2024-01-01`) are stored in a database (Glue Catalog).
*   **The Issue:** If you have 5 years of data partitioned by hour, that's `5 * 365 * 24 = 43,800` partitions. A query like `SELECT * WHERE year > 2020` has to fetch all those partition paths from the Metastore first. This adds seconds/minutes of latency.
*   **The Solution (Projection):** You tell Athena: "My partitions follow the pattern `/date=YYYY-MM-DD/`." Athena *calculates* the S3 paths in memory and starts reading immediately. Zero metastore latency.

## 🛠️ The Solution: Partition Projection
We add `TBLPROPERTIES` to the `CREATE TABLE` statement:
1.  **projection.enabled:** `true`
2.  **projection.date.type:** `date`
3.  **projection.date.range:** `2020-01-01,NOW`

## 🏗️ Architecture
1.  **Storage:** S3 (Standard Hive Style: `/year=2024/month=10/`).
2.  **Engine:** Athena (Presto).
3.  **Optimization:** Projection Configuration.

## 🚀 How to Run (Simulation)
Copy the SQL from `create_optimized_table.sql` into the Athena Console.
*   Notice there is no `MSCK REPAIR TABLE` command needed. The partitions are instantly available.
