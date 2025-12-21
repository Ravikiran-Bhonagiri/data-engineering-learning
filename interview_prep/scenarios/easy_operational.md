# 🟢 Easy Scenarios 11-20

**Operational Reliability & Testing**

---

## Scenario 11: Streaming File Not Found

**🏷️ Technologies:** `PySpark` `Delta Lake`

### Interview Question
*"Your Spark Structured Streaming job occasionally fails with `FileNotFoundException: partition_0001.parquet`. The file existed when the job started. What's causing this and how do you prevent it?"*

### What's Happening
File deleted mid-read by concurrent VACUUM or OPTIMIZE operations.

### Solution
```sql
-- Increase file retention
ALTER TABLE events SET TBLPROPERTIES (
  'delta.deletedFileRetentionDuration' = 'interval 14 days'
);
```

**Rule:** Never run VACUUM on actively streamed tables during business hours.

---

## Scenario 12: API Rate Limiting

**🏷️ Technologies:** `Airflow` `Python`

### Interview Question
*"Your ETL pipeline calls an external API 1000 times in parallel and receives `429 Too Many Requests` errors. How do you handle rate limiting in Airflow?"*

### Solution
```python
# Airflow Pool approach
@task(pool='api_pool')  # Create pool with slots=5
def fetch(customer_id):
    return requests.get(f"/api/customers/{customer_id}").json()

# Or code-level throttling
import time
for id in customer_ids:
    fetch(id)
    time.sleep(0.1)  # 10 requests/second max
```

---

## Scenario 13: View vs Materialized View

**🏷️ Technologies:** `SQL` `Databricks`

### Interview Question
*"Your dashboard queries a view that joins 5 tables and aggregates 1 billion rows. Every refresh takes 3 minutes. What's your optimization strategy?"*

### Solution
```sql
-- Materialized View (compute once, query many times)
CREATE MATERIALIZED VIEW sales_summary AS
SELECT region, SUM(amount) as total
FROM sales
GROUP BY region;

-- Refresh periodically
REFRESH MATERIALIZED VIEW sales_summary;
```

**Tradeoff:** Storage cost + staleness vs query performance.

---

## Scenario 14: Lost Update Problem

**🏷️ Technologies:** `SQL` Databases

### Interview Question
*"Two concurrent sessions both read inventory stock=10, then each decrements by their order amount. Final stock shows 5 instead of 2. What's the problem and solution?"*

### What's Happening
Classic "lost update" - both sessions read same value, last write wins.

### Solution
```sql
-- Row-level locking
BEGIN;
SELECT stock FROM inventory WHERE product_id = 1 FOR UPDATE;
UPDATE inventory SET stock = stock - 3 WHERE product_id = 1;
COMMIT;
```

Or use SERIALIZABLE isolation level.

---

## Scenario 15: Slow GROUP BY

**🏷️ Technologies:** `PySpark`

### Interview Question
*"`SELECT department, COUNT(*) FROM employees GROUP BY department` takes 20 minutes on 10M rows. You discover one department has 9M employees (extreme skew). How do you optimize?"*

### Solution
```python
# Salting technique
from pyspark.sql.functions import rand, concat, lit

df.withColumn("dept_salt", 
    concat(col("department"), lit("_"), (rand()*10).cast("int"))
).groupBy("dept_salt").count()
```

Distributes the skewed key across 10 partitions.

---

## Scenario 16: Watermarking for Late Data

**🏷️ Technologies:** `PySpark` `Streaming`

### Interview Question
*"Events arrive out of order - an event timestamped 10:00 AM arrives at 10:05 AM. How do you handle this in streaming aggregations?"*

### Solution
```python
df.withWatermark("event_time", "5 minutes")\
  .groupBy(window("event_time", "1 hour"), "user_id")\
  .count()
```

**Tradeoff:** Late tolerance (5 min) vs state store memory size.

---

## Scenario 17: Character Encoding Issues

**🏷️ Technologies:** `Python` `PySpark`

### Interview Question
*"Reading a CSV from international suppliers. Special characters (é, ñ, 中文) display as . How do you fix encoding issues?"*

### Solution
```python
df = spark.read\
    .option("encoding", "UTF-8")\
    .option("multiLine", "true")\
    .csv("/data/international.csv")
```

Always specify UTF-8 explicitly, don't rely on defaults.

---

## Scenario 18: Disk Space Exhaustion

**🏷️ Technologies:** `PySpark`

### Interview Question
*"Spark job fails: `No space left on device` even though your data is only 100GB. Executors have 200GB disks. What's happening?"*

### What's Happening
Shuffle operations spill intermediate data to `/tmp`, filling the disk.

### Solution
```python
# Increase shuffle partitions (smaller chunks per partition)
spark.conf.set("spark.sql.shuffle.partitions", 400)  # Default 200

# Or increase executor memory to reduce spill
# spark.executor.memory = 16g
```

---

## Scenario 19: Local dbt Testing

**🏷️ Technologies:** `dbt`

### Interview Question
*"How do you test a dbt model locally before deploying to production to avoid breaking the production schema?"*

### Solution
```bash
# Run in development schema
dbt run --select my_model --target dev

# With dependencies
dbt run --select +my_model+

# Test
dbt test --select my_model
```

**profiles.yml:**
```yaml
outputs:
  dev:
    schema: dbt_dev_yourname
  prod:
    schema: analytics_prod
```

---

## Scenario 20: Job Failure Monitoring

**🏷️ Technologies:** `Airflow` `Databricks`

### Interview Question
*"Jobs are failing silently and you're discovering failures days later. How do you implement real-time failure alerting?"*

### Solution
**Airflow:**
```python
def slack_alert(context):
    send_slack(f"FAILED: {context['task_instance'].task_id}")

dag = DAG(on_failure_callback=slack_alert)
```

**Databricks:**
```json
{
  "email_notifications": {
    "on_failure": ["team@company.com"],
    "on_success": [],
    "no_alert_for_skipped_runs": true
  }
}
```

---

**Previous:** [Fundamentals](./easy_fundamentals.md) | **Next:** [Medium: Performance Debug](./medium_performance_debug.md)
