# 🟡 Medium Scenarios 01-10

**Performance Debugging & Optimization**

---

## Scenario 1: The Skewed Join

**🏷️ Technologies:** `PySpark` `Databricks`

### Interview Question
*"You are optimizing a slow Spark job that joins a 10TB `Transactions` table with a 500GB `Merchants` table.
**Observation:** In the Spark UI, you see that the stage has 200 tasks. 199 of these tasks finish in under 2 minutes. However, the final task (Task #200) runs for 90 minutes and eventually crashes with an OutOfMemory error.
**Question:** This is a classic symptom. What is technically happening in Task #200? How would you confirm your hypothesis using the UI, and what are two specific code changes to fix it?"*

---

## Scenario 2: Driver OutOfMemory

**🏷️ Technologies:** `PySpark`

### Interview Question
*"Your nightly batch ETL job crashes consistently at 3:00 AM.
**Error Log:** `java.lang.OutOfMemoryError: Java heap space`.
**Diagnostics:** You check the Ganglia metrics and notice the **Driver** node's memory usage spiked to 100% just before the crash, while the Worker nodes were idle at 10% utilization.
**Question:** What specific anti-patterns in Spark code cause the Driver to OOM while Executors are idle? Provide two examples of code that would cause this."*

---

## Scenario 3: ConcurrentAppendException

**🏷️ Technologies:** `Databricks` `Delta Lake` `Airflow`

### Interview Question
*"You have two separate Airflow DAGs: `Ingest_Marketing_Data` and `Ingest_Sales_Data`. Both DAGs run at 8:00 AM and attempt to write to the same `Gold_Revenue` Delta table.
**The Error:** One of the DAGs fails intermittently with `ConcurrentAppendException: Files were added to partition [date=2024-01-15] by a concurrent update`.
**Question:** Explain how Delta Lake's ACID concurrency control works here. Why did it block the write, and how can you architect your pipeline to allow safe concurrent writes?"*

---

## Scenario 4: Airflow Scheduler CPU 100%

**🏷️ Technologies:** `Airflow`

### Interview Question
*"Your Airflow environment is sluggish. The Web UI takes forever to load, and tasks are staying in 'Queued' state for 10-15 minutes before running, even though you have free worker capacity.
**Metric:** The **Scheduler** process is pinned at 100% CPU utilization.
**Investigation:** You have 2,000 DAG files in your repo.
**Question:** What common coding mistake in the DAG definition files causes the Scheduler to burn CPU? How does the Scheduler parsing loop work, and how do you fix this?"*

### What's Happening
Scheduler re-parses all DAG files every 30 seconds. Files have expensive operations at module level (DB calls, API requests).

### Solution
```python
# ❌ BAD: Top-level code executed every parse
customers = requests.get("api/customers").json()
for c in customers:
    dag = DAG(...)

# ✅ GOOD: Move to task execution
@task
def get_customers():
    return requests.get("api/customers").json()

@task
def process(customer):
    ...

process.expand(customer=get_customers())
```

Enable DAG serialization:
```ini
[core]
store_serialized_dags = True
```

---

## Scenario 5-10: Additional Medium Questions

**Scenario 5: Broadcast Timeout**
*Question:* "Query fails with `Timeout waiting for build`. What's happening?"
*Answer:* Forced broadcast of table larger than timeout allows. Increase `spark.sql.broadcastTimeout` or disable broadcast.

**Scenario 6: Gaps & Islands (SQL Pattern)**
*Question:* "Find consecutive login day streaks per user."
*Answer:* `grp = date - ROW_NUMBER()`. Group by `(user_id, grp)`.

**Scenario 7: Point-in-Time Join (SCD Type 2)**
*Question:* "Join fact to dimension as it was at fact timestamp."
*Answer:* `ON f.date BETWEEN d.valid_from AND d.valid_to`

**Scenario 8: Approximate COUNT DISTINCT**
*Question:* "`COUNT(DISTINCT)` on 10B rows takes 20 mins. Alternative?"
*Answer:* `approx_count_distinct()` (HyperLogLog) - 99% accurate, 100× faster.

**Scenario 9: Distributed API Rate Limiting**
*Question:* "100 Spark executors hitting API. IP banned. Fix?"
*Answer:* `repartition(5)` to limit concurrency + rate limiter in `mapPartitions`.

**Scenario 10: Streaming Backpressure**
*Question:* "Kafka burst 10M events. Spark OOMs. Solution?"
*Answer:* `.option("maxOffsetsPerTrigger", 100000)` to cap batch size.

---

**Previous:** [Easy: Operational](./easy_operational.md) | **Next:** [Complex Scheduling](./medium_complex_scheduling.md)
