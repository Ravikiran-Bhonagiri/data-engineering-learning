# 🟢 Easy Scenarios 01-10

**Foundational Concepts & Common Patterns**

---

## Scenario 1: The Small Files Disaster

**🏷️ Technologies:** `Databricks` `PySpark` `Delta Lake`

### Interview Question
*"Your team maintains a critical real-time inventory dashboard powered by Spark Structured Streaming. The job ingests events from Kafka and writes to S3/Delta Lake every 5 seconds.
**The Incident:** After running smoothly for 3 months, the system performance has degraded severely. Queries that executed in 10 seconds now take 15 minutes. You check the Spark UI and notice the driver is spending 90% of its time in 'Listing Files'.
**Question:** Diagnose the root cause of this performance cliff. What specifically happened in the storage layer, and what is your step-by-step remediation plan?"*

---

## Scenario 2: Duplicate Records from Webhooks

**🏷️ Technologies:** `PySpark` `Delta Lake`

### Interview Question
*"You are building a financial reconciliation pipeline. Your upstream payment provider sends data via Webhooks.
**The Problem:** The provider's system uses 'at-least-once' delivery. During network blips, they retry sending the same transaction payload multiple times. As a result, your `revenue_report` table shows duplicate charges, inflating daily revenue by 5%.
**Question:** How do you architect an ingestion pipeline that guarantees **exactly-once** processing for these webhook events, ensuring downstream reports are accurate even if the provider sends the same ID five times?"*

---

## Scenario 3: Schema Evolution Failure

**🏷️ Technologies:** `PySpark` `Databricks` `Auto Loader`

### Interview Question
*"It is 3 AM. You get paged because the primary ingestion pipeline has crashed.
**Investigation:** The logs show an `AnalysisException`. You discover that the mobile app team released a new version an hour ago that added a new field, `user_tier`, to the JSON event payload. Your pipeline was strictly typed and rejected the new schema.
**Question:** How would you modify your pipeline to automatically adapt to such non-breaking schema changes (like new columns) without crashing, while still protecting against breaking changes (like column type changes)?"*

### Context
Streaming pipeline reading user activity events from S3 with pre-defined schema.

### Solution
```python
spark.readStream.format("cloudFiles")\
  .option("cloudFiles.format", "json")\
  .option("cloudFiles.schemaEvolutionMode", "addNewColumns")\
  .option("cloudFiles.schemaLocation", "/schemas/users")\
  .load ("/raw/")\
  .writeStream\
  .option("mergeSchema", "true")\
  .start("/bronze/users")
```

### Follow-Up
1. **"What if they changed user_id from INT to STRING instead of adding a column?"**
   - Type changes are incompatible. Requires manual migration with backfill.

2. **"What's the risk of always allowing schema evolution?"**
   - Schema explosion: buggy code could add 1000s of unwanted columns.

---

## Scenario 4: PII Data Leak

**🏷️ Technologies:** `Databricks` `Delta Lake`

### Interview Question
*"A junior engineer accidentally wrote customer email addresses to the 'public_analytics' schema that's accessible to all marketing analysts. Your compliance team just flagged this in an audit. How do you immediately purge this PII data?"*

### Context
GDPR compliance requirement for immediate and permanent deletion of PII.

### Solution
```sql
-- 1. Stop all pipelines writing to this table
-- 2. Delete the rows
DELETE FROM public.users WHERE email IS NOT NULL;

-- 3. CRITICAL: Physical deletion (bypasses Time Travel)
SET spark.databricks.delta.retentionDurationCheck.enabled = false;
VACUUM public.users RETAIN 0 HOURS;
```

**Prevention:**
```python
df.withColumn("email_hash", sha2(col("email"), 256)).drop("email")
```

### Follow-Up
1. **"What if analysts already cached the table in their notebooks?"**
   - Must restart clusters or run `REFRESH TABLE public.users`.

2. **"How do you handle downstream tables that joined against these rows?"**
   - Use Unity Catalog lineage to trace dependencies and re-run with `--full-refresh`.

---

## Scenario 5: Python Dependency Conflict

**🏷️ Technologies:** `Airflow` `Docker`

### Interview Question
*"You have an Airflow DAG with two tasks: Task A runs a legacy ML model requiring pandas==1.0, and Task B uses a new forecasting library requiring pandas>=2.0. Both run on the same worker. Task B fails with `ImportError: cannot import name 'DataFrame'`. How do you fix this?"*

### Context
Shared Airflow worker environment where tasks overwrite each other's dependencies.

### Solution
```python
# Docker isolation (best practice)
from airflow.providers.docker.operators.docker import DockerOperator

task_a = DockerOperator(
    image='ml-legacy:pandas1.0',
    command='python train.py'
)

task_b = DockerOperator(
    image='forecast:pandas2.0',
    command='python forecast.py'
)
```

### Follow-Up
1. **"What's the startup overhead for Docker containers?"**
   - Image pull: ~10-30s (cached). Container spin-up: ~2-5s.

---

## Scenario 6-10: Additional Interview Questions

### Scenario 6: NULL Handling in JOINs
**Question:** *"You joined 10M orders with customers table. Only 7M rows returned but you expected all 10M. What happened?"*
**Answer:** NULL = NULL evaluates to NULL (not TRUE), excluding 3M guest checkouts. Use LEFT JOIN.

### Scenario 7: Cost Explosion
**Question:** *"Your Databricks bill jumped from $5K to $25K. How do you diagnose and fix?"*
**Answer:** Clusters running 24/7. Enable autotermination (30 mins) and use Job clusters for scheduled work.

### Scenario 8: Incremental Loading
**Question:** *"Your dbt full refresh takes 8 hours on 5 years of data. How do you optimize?"*
**Answer:** Convert to incremental materialization with `WHERE event_date > MAX(event_date)`.

### Scenario 9: Nested JSON
**Question:** *"API returns nested arrays in JSON. How do you flatten for SQL analysis?"*
**Answer:** Use `explode()` function layer by layer.

### Scenario 10: Timezone Issues
**Question:** *"Global sales aggregations are wrong because Tokyo's 2024-01-15 overlaps US 2024-01-14. How do you fix?"*
**Answer:** Always store timestamps in UTC, convert to local timezone only at presentation layer.

---

**Next:** [Operational Reliability](./easy_operational.md) | [Medium: Performance Debug](./medium_performance_debug.md)
