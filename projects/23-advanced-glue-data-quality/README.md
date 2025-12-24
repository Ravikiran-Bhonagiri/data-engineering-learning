# Advanced Project 23: Glue Data Quality (DQDL)

## 🎯 Goal
Master **Automated Data Contracts**. We will implement a Glue ETL job that defines explicit expectations (e.g., "column `email` must be unique", "`age` must be > 18") using **Data Quality Definition Language (DQDL)** and fails if they are violated.

## 🛑 The "Garbage In, Garbage Out" Problem
*   **Standard ETL:** Reads CSV -> Writes Parquet.
*   **Safety Gap:** If the source CSV contains `age = -5`, the ETL happily writes `-5` to the Data Lake.
*   **Result:** Downstream dashboards break, or worse, ML models hallucinate.
*   **Solution:** **Circuit Breakers**. Stop the pipeline *before* the bad data lands.

## 🛠️ The Solution: Glue Data Quality
AWS provides a native evaluation engine inside Glue based on Deequ.
1.  **Ruleset:** Defined in DQDL (Data Quality Definition Language).
2.  **Actions:** `Fail` (Stop job) or `Warn` (Log metric).
3.  **Result:** A Data Quality Score (e.g., 95%).

## 🏗️ Architecture
1.  **Source:** `dynamic_frame` (Raw Data).
2.  **Evaluation:** Apply `EvaluateDataQuality` transform.
3.  **Decision:** If `Outcome == Failed` -> Stop. Else -> Write to S3.

## 🚀 How to Run (Simulation)
1.  **Code:** `glue_quality_job.py`.
2.  **Rules:** Embedded in the script (DQDL string).
    *   `IsComplete "email"`
    *   `ColumnValues "age" > 0`
