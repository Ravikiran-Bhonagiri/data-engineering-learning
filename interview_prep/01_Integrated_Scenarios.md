# The Data Engineering Scenario Masterclass

**100+ Real-World Scenarios integrating SQL, dbt, PySpark, Databricks, and Airflow.**

This guide moves beyond "What is X?" to "How do you solve Y using X, Z, and W?".

---

## 🏗 Section 1: Architecture & System Design (Scenarios 1-20)

### Scenario 1: The "Small Files" Disaster
**Context:** Your Airflow DAG triggers a Spark job every 10 minutes to ingest Kafka data into Databricks Delta Lake. After 2 months, query performance has dropped by 10x.
**Tech Stack:** Airflow, PySpark, Databricks.
**Diagnosis:** You created millions of tiny KB-sized files (The Small Files Problem), overloading the Delta Log and listing operations.
**Solution:**
1.  **Immediate Fix:** Run `OPTIMIZE table_name ZORDER BY (date)` on Databricks to compact files.
2.  **Root Cause Fix:** Adjust the Spark Structured Streaming trigger to `Trigger.AvailableNow` (batch) instead of Continuous, or enable `spark.databricks.delta.autoOptimize.optimizeWrite = true`.
3.  **Architecture:** Introduce a "Bronze" (Raw) to "Silver" (Clean) compaction job in Airflow that runs hourly, separate from the 10-min ingestion.

### Scenario 2: Late Arriving Data in Financial Reporting
**Context:** You are building a dbt Data Warehouse. Financial transactions often arrive 3 days late. Your daily incremental model misses them because it only looks at `date = current_date`.
**Tech Stack:** dbt, SQL.
**Solution:**
1.  **dbt Logic:** Update the incremental strategy.
    ```sql
    {% if is_incremental() %}
      WHERE transaction_date >= (select max(transaction_date) - interval 3 days from {{ this }})
    {% endif %}
    ```
2.  **Design:** This is a "Lookback Window". It forces the MERGE statement to scan the last 3 days of target data to catch updates/inserts for late rows.

### Scenario 3: The "Zombie" Airflow Tasks
**Context:** Users report that tasks are stuck in "Running" state for hours but no logs are generating. The underlying Spark cluster shows the driver died.
**Tech Stack:** Airflow, Kubernetes/Databricks.
**Diagnosis:** The Airflow Worker lost connection to the Task (Zombie). The Scheduler thinks it's running; the reality is it's dead.
**Solution:**
1.  **Config:** Decrease `scheduler_zombie_task_threshold`.
2.  **Resiliency:** Use `CeleryExecutor` or `KubernetesExecutor`. Ensure the worker node has enough memory (OOM often kills the worker process but leaves the task state 'Running').
3.  **Alerting:** Set `sla_miss_callback` to alert Slack when tasks overrun their expected duration.

### Scenario 4: PII leakage in Bronze Layer
**Context:** A developer accidentally pushed a raw JSON dump containing Credit Card numbers to the Bronze Delta table. 5 downstream dbt models read from this.
**Tech Stack:** Databricks, dbt, SQL.
**Solution:**
1.  **Containment:** Stop all Airflow DAGs.
2.  **Purge:**
    - `DELETE FROM bronze_table WHERE ...`
    - **Crucial:** Run `VACUUM bronze_table RETAIN 0 HOURS` to remove the physical parquet files immediately. (Standard Delete keeps them for Time Travel).
3.  **Fix:** Update the Ingestion PySpark job to apply a hashing mask `sha2(col("cc_num"), 256)` *before* writing to Delta.
4.  **Propagate:** Rerun upstream dbt models with `--full-refresh` to scrub the cache.

### Scenario 5: Migrating Logic from Stored Procedures to dbt/Spark
**Context:** Legacy system uses 5000-line SQL Stored Procedures. Nightly run takes 12 hours. You need to move to Databricks/dbt.
**Tech Stack:** SQL, dbt, PySpark.
**Strategy:**
1.  **Categorize:**
    - **Row-by-row cursors:** Rewrite in PySpark (Set based manipulation is 100x faster).
    - **Complex Joins:** Rewrite in dbt (Modularize into Staging -> Intermediate -> Marts).
2.  **Testing:** Use dbt `audit_helper` package to compare Legacy Output vs New Output row-by-row to guarantee parity.

... [Scenarios continue] ...

---

## 🚒 Section 2: Troubleshooting & Optimization (Scenarios 21-50)

### Scenario 21: The Skewed Join (99% Complete Hang)
**Context:** A PySpark job joining `Transactions` (10TB) and `Customers` (50GB) hangs at the last task.
**Tech Stack:** PySpark.
**Diagnosis:** Data Skew. One "Null" or generic Customer ID matches 100M transactions, overloading one executor.
**Solution:**
1.  **Salting:** Add a random integer (0-199) to the join key on the "Big" side, and explode the "Small" side records 200 times. Join on `(id, salt)`.
2.  **AQE:** Enable `spark.sql.adaptive.skewJoin.enabled = true`. Spark will auto-split the skewed partition.

### Scenario 22: dbt Model Timeout
**Context:** A dbt model implementing a complex `distinct` logic over 5 Billion rows times out after 2 hours.
**Tech Stack:** dbt, SQL (Snowflake/Databricks).
**Solution:**
1.  **Materialization:** Switch from `view` to `incremental` table.
2.  **Logic:** Move the deduplication logic to the upstream (Silver) layer.
3.  **Partitioning:** Ensure the target table is partitioned by Date. Filter `WHERE date > ...` in the dbt model to leverage Partition Pruning.

### Scenario 23: Airflow Scheduler Overload
**Context:** You have 10,000 DAGs. The Scheduler heartbeat lags, and tasks don't start for minutes.
**Tech Stack:** Airflow.
**Diagnosis:** Parsing overhead. The scheduler parses every `.py` file continuously.
**Solution:**
1.  **Fix Code:** Remove specific "Top Level Code" (e.g., `db_conn = get_connection()` called at global scope). Wrap it in tasks.
2.  **Architecture:** Split into multiple Schedulers (High Availability).
3.  **Serialization:** Ensure "DAG Serialization" is writing JSON to the DB effectively.

### Scenario 24: Databricks Driver OOM
**Context:** `spark.driver.memory` is 16GB. Job fails with `OutOfMemoryError` during a `collect()`.
**Tech Stack:** PySpark.
**Solution:**
1.  **Anti-Pattern:** Never call `collect()` on big data. It pulls everything to the single Driver node.
2.  **Fix:** Use `.toPandas()` only on aggregated small data, or write to S3/DBFS and read just the tail.
3.  **Broadcast:** Check if you are broadcasting a table > 8GB. Increase `spark.sql.autoBroadcastJoinThreshold` or disable broadcast.

### Scenario 25: Schema Drift breaking Pipelines
**Context:** Source API added a new column `user_rating`. The PySpark ingestion job failed because the Delta table didn't expect it.
**Tech Stack:** Databricks, PySpark.
**Solution:**
1.  **Enable Evolution:** Set `.option("mergeSchema", "true")` on the writer.
2.  **Auto Loader:** If using `cloudFiles`, set `cloudFiles.schemaEvolutionMode = "addNewColumns"`. It updates the target schema automatically without downtime.

... [Scenarios continue] ...

---

## 🔄 Section 3: Orchestration & Dependencies (Scenarios 51-70)

### Scenario 51: Handling Cross-DAG Dependencies
**Context:** DAG A (Ingestion) must finish before DAG B (Transformation) starts. They are on different schedules.
**Tech Stack:** Airflow.
**Solution:**
1.  **Dataset (Airflow 2.4+):** DAG A updates `Dataset("s3://bucket/raw")`. DAG B schedules on `[Dataset("s3://bucket/raw")]`. Event-driven.
2.  **ExternalTaskSensor:** DAG B has a sensor task waiting for DAG A execution_date. (Fragile if schedules misalign).
3.  **TriggerDagRunOperator:** DAG A pushes a trigger to DAG B at the end. (Best for tight coupling).

### Scenario 52: Idempotency in Backfills
**Context:** You need to re-run transformations for Jan 2023. The dbt model does a standard `INSERT`. Rerunning it creates duplicates.
**Tech Stack:** dbt, SQL.
**Solution:**
1.  **Delete+Insert Pattern:**
    ```sql
    {% if is_incremental() %}
    DELETE FROM {{ this }} WHERE date = '{{ var("date") }}';
    INSERT INTO {{ this }} ...
    {% endif %}
    ```
2.  **Design:** Always build pipelines that can run twice without side effects. Use `MERGE` or `OVERWRITE` partition for the specific date active.

... [Scenarios continue] ...

---

## 🧪 Section 4: Data Quality & Tests (Scenarios 71-85)

### Scenario 71: Silent Data Corruption
**Context:** A currency conversion Join failed silently (inner join dropped rows), causing Revenue to report 50% lower. No error was thrown.
**Tech Stack:** dbt, Airflow.
**Solution:**
1.  **Source Test:** `dbt test` on source tables (check row counts).
2.  **Relationship Test:** Add `relationships` test in dbt ensuring `fact_sales.currency_id` exists in `dim_currency`.
3.  **Recency Test:** Airflow `check_operator` to verify row count > 0 before proceeding to report generation.

### Scenario 72: CI/CD for Data Pipelines
**Context:** A developer changed a column name `c_id` to `customer_id` and broke production.
**Tech Stack:** dbt, GitHub Actions, Databricks.
**Solution:**
1.  **Slim CI:** On PR, GitHub Action triggers `dbt run --select state:modified+ --defer --state prod_artifacts`.
2.  **What it does:** It runs only the modified model and its children in a sandbox schema, comparing against Production state. Immediate failure if column rename isn't propagated.

... [Scenarios continue] ...

---

## 🔐 Section 5: Governance & Security (Scenarios 86-100)

### Scenario 86: Row-Level Security (RLS) Implementation
**Context:** Germany users should only see Germany data. US users see all.
**Tech Stack:** Databricks Unity Catalog.
**Solution:**
1.  **Function:** Create a UDF `check_access(region)`.
    ```sql
    CREATE FUNCTION check_access(region STRING) RETURN
    IF(is_account_group_member('admin'), TRUE, region = 'DE');
    ```
2.  **Apply:** `ALTER TABLE sales SET ROW FILTER check_access ON (region)`.
3.  **Benefit:** This applies to SQL queries, PySpark jobs, and BI dashboards automatically.

### Scenario 87: Secrets Management
**Context:** Developers are hardcoding AWS Keys in Airflow Variables.
**Tech Stack:** Airflow.
**Solution:**
1.  **Backend:** Configure `secrets_backend = Airflow.providers.amazon.aws.secrets.secrets_manager.SecretsManagerBackend`.
2.  **Workflow:** Store keys in AWS Secrets Manager. Airflow retrieves them at runtime. Keys never exist in Airflow Metadata DB or UI.

... [Scenarios continue] ...

---
**Summary:**
This integrated approach tests your ability to connect the dots:
*   Spark writes the data (Optimization).
*   Databricks stores it (Governance).
*   dbt transforms it (Modeling/Testing).
*   Airflow coordinates it all (Reliability).
