# Foundation Project 4: The Lakehouse Ingestion (Autoloader)

## 🎯 Goal
Master the **"Set it and Forget it"** ingestion pattern. We will build a pipeline that ingests millions of small JSON files from S3 into Delta Lake without writing complex Lambda functions or managing SQS queues.

## 🛑 The "Small Files" Problem
When thousands of devices send logs, you get millions of tiny (KB-sized) files in S3.
*   **Legacy Approach:** A Spark job runs `spark.read.json("s3://bucket/")`. It has to "List" (enumerate) all 1 million files every time it runs to find the new ones. This takes hours and eventually crashes.
*   **Schema Drift:** If a device sends a new field `cpu_temp`, the legacy pipeline fails because the schema doesn't match.

## 🛠️ The Solution: Databricks Autoloader
Autoloader (`format("cloudFiles")`) solves this:
1.  **Scalable Discovery:** It keeps a persistent state (RocksDB) of what files it has seen, preventing expensive S3 listing.
2.  **Schema Evolution:** It detects new columns and adds them to the target Delta table automatically (`mergeSchema`).
3.  **Resilience:** If a file is corrupt, it goes to a "Rescue Data" column instead of crashing the job.

## 🏗️ Architecture
1.  **Source:** S3 Bucket (simulated path).
2.  **Stream:** Spark Structured Streaming using `cloudFiles`.
3.  **Sink:** Delta Table (Bronze Layer).
4.  **Checkpoint:** Stores the state so we can restart exactly where we left off.

## 🚀 How to Run (on Databricks)
1.  Create a cluster (Single Node is fine).
2.  Create a Notebook.
3.  Paste the code from `ingestion.py`.
4.  Run the cell. It will start a stream.
5.  Drop invalid JSON files into the source path and watch them appear in the table.
