# Foundation Project 13: Serverless ETL (AWS Glue)

## 🎯 Goal
Master **AWS Native ETL**. We will write a PySpark script that uses the proprietary **AWS Glue Libraries** (`awsglue`) to transform data. This is different from "just running Spark on EMR."

## 🛑 The "Cluster Management" Problem
*   **Legacy (EMR/Databricks):** You have to provision EC2 instances, configure YARN, pick instance types (m5.xlarge), and handle auto-scaling.
*   **Serverless (Glue):** You just provide the Python script. AWS allows you to bill by the second (DPU - Data Processing Unit).

## 🛠️ The Solution: AWS Glue DynamicFrames
Glue adds a wrapper around Spark DataFrames called `DynamicFrame`.
1.  **Schema Flexibility:** DynamicFrames don't enforce a schema as strictly as Spark. A column can have both `int` and `string` values without crashing immediately.
2.  **ApplyMapping:** A powerful logical transformation method unique to Glue for renaming/casting columns.
3.  **Governance:** Native integration with the Glue Data Catalog.

## 🏗️ Architecture
1.  **Source:** Glue Data Catalog Table (`raw_customers`).
2.  **Transform:** `ApplyMapping` to rename/cast fields.
3.  **Sink:** S3 (Parquet).

## 🚀 How to Run (Simulation)
This script is designed to run in the **AWS Glue Console**.
To inspect it locally:
1.  Read `glue_job.py`.
2.  Notice the imports: `from awsglue.dynamicframe import DynamicFrame`. These only exist in the AWS environment.
