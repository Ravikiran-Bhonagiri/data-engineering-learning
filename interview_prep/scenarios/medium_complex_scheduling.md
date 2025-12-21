# 🟡 Medium Scenarios 11-20

**Complex State, Scheduling & Integration**

---

## Scenario 11: Executor OutOfMemory

**🏷️ Technologies:** `PySpark`

### Interview Question
*"Your Spark job's executors keep dying with 'Container killed by YARN'. The Driver is fine. Logs show GC thrashing before the crash. How do you diagnose and fix this?"*

### What's Happening
Executor running out of memory due to:
- Wide rows (large JSON/XML columns in single rows)
- Heavy Pandas UDFs using off-heap memory
- Insufficient memory overhead allocation

### Solution
```python
# Increase memory overhead (for off-heap usage)
spark.conf.set("spark.executor.memoryOverhead", "4g")

# Or increase total executor memory
# spark.executor.memory = 16g

# Increase shuffle partitions to reduce task size
spark.conf.set("spark.sql.shuffle.partitions", 400)
```

### Follow-Up
**"How do you distinguish Executor OOM from Driver OOM?"**
- Executor: Logs show "Container killed", multiple executors affected
- Driver: Error says "Driver stacktrace", only one failure

---

## Scenario 12: S3 List Performance

**🏷️ Technologies:** `Delta Lake` `PySpark`

### Interview Question
*"Your query takes 20 minutes and the Spark UI shows most time is spent in 'list files at s3://...' before any actual data processing. What's the bottleneck and how do you fix it?"*

### Solution
```python
# Use Delta Lake (maintains manifest in _delta_log)
df = spark.read.format("delta").load("s3://bucket/table")

# Reduce partition granularity
# Instead of: partitionBy("year", "month", "day", "hour")
# Use: partitionBy("year", "month", "day")
```

**Why Delta helps:** Metadata in transaction log eliminates recursive S3 listing.

---

## Scenario 13: Task Not Serializable

**🏷️ Technologies:** `PySpark`

### Interview Question
*"Your Spark job fails immediately with `Task not serializable: java.io.NotSerializableException: connection`. What caused this and how do you fix it?"*

### What's Happening
You created a database connection on the Driver and tried to use it in a distributed operation (map, filter).

### Solution
```python
# ❌ BAD: Connection created on driver
conn = create_db_connection()
def process(row):
    conn.insert(row)  # Tries to serialize connection
df.foreach(process)

# ✅ GOOD: Create connection in executor
def process_partition(iterator):
    conn = create_db_connection()  # Each executor creates own connection
    for row in iterator:
        conn.insert(row)
    conn.close()

df.foreachPartition(process_partition)
```

---

## Scenario 14: Cross-DAG Dependencies

**🏷️ Technologies:** `Airflow`

### Interview Question
*"DAG A processes raw data and DAG B transforms it. Both run at midnight. Sometimes DAG B starts before DAG A finishes, causing failures. What are 3 ways to handle this dependency?"*

### Solutions
**1. ExternalTaskSensor (brittle):**
```python
wait_for_dag_a = ExternalTaskSensor(
    task_id='wait',
    external_dag_id='dag_a',
    external_task_id='final_task'
)
```

**2. TriggerDagRunOperator (active trigger):**
```python
# End of DAG A
trigger_dag_b = TriggerDagRunOperator(
    task_id='trigger_b',
    trigger_dag_id='dag_b'
)
```

**3. Datasets (Airflow 2.4+, best):**
```python
# DAG A
@dag(schedule="@daily")
def dag_a():
    @task(outlets=[Dataset("s3://bucket/processed/")])
    def process():
        ...

# DAG B
@dag(schedule=[Dataset("s3://bucket/processed/")])
def dag_b():
    ...
```

---

## Scenario 15: Idempotency in S3 Writes

**🏷️ Technologies:** `PySpark` `Airflow`

### Interview Question
*"Your job writes Parquet files to S3. It crashes halfway through. You restart it and now have duplicate data. How do you make this idempotent?"*

### Solution
```python
# Overwrite partition strategy
df.write\
  .mode("overwrite")\
  .partitionBy("date")\
  .parquet("s3://bucket/data/")

# Or use Delta Lake MERGE
from delta.tables import DeltaTable

DeltaTable.forPath(spark, "s3://bucket/delta_table")\
  .alias("t").merge(df.alias("s"), "t.id = s.id")\
  .whenMatchedUpdateAll()\
  .whenNotMatchedInsertAll()\
  .execute()
```

---

## Scenario 16-20: Additional Medium Scenarios

### Scenario 16: dbt Snapshot Strategy
**Question:** *"Need to track history for a table without updated_at column. How?"*
**Answer:** Use `strategy='check'` and `check_cols='all'`. dbt hashes entire row.

### Scenario 17: Zombie Airflow Tasks
**Question:** *"Tasks stuck in 'Running' state but nothing happening. Logs empty. Why?"*
**Answer:** Worker died (OOM) but didn't notify Scheduler. Tune `scheduler_zombie_task_threshold`.

### Scenario 18: Dynamic Task Mapping
**Question:** *"Need to create 500 tasks dynamically (one per customer). How in Airflow?"*
**Answer:** Use `expand()` with Airflow 2.3+ dynamic task mapping.

### Scenario 19: Unit Testing dbt
**Question:** *"How do you unit test dbt SQL logic with mock data?"*
**Answer:** Use `dbt-unit-tests` package. Define mock inputs/outputs in YAML.

### Scenario 20: Cloud Fetch Optimization
**Question:** *"Tableau pulling 10GB result from Databricks SQL is slow. How to optimize?"*
**Answer:** Enable Cloud Fetch. Result writes to S3, BI downloads via presigned URL (parallel).

---

**Previous:** [Performance Debug](./medium_performance_debug.md) | **Next:** [Transformations](./medium_transformations.md)
