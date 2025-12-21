# Advanced Troubleshooting Guide

**Goal:** Diagnose and fix complex Airflow issues.

---

## 🔍 Diagnostic Commands

```bash
# Check Airflow health
airflow db check

# List all DAGs (check for import errors)
airflow dags list

# Show import errors
airflow dags list-import-errors

# Check connections
airflow connections list

# View task state
airflow tasks state my_dag my_task 2025-12-20

# Clear task state (for re-run)
airflow tasks clear my_dag --start-date 2025-12-20 --end-date 2025-12-20
```

---

## 🐛 Common Issues & Fixes

### Issue 1: High Scheduler Lag

**Symptom:** Tasks don't start on time  
**Diagnosis:**
```bash
# Check scheduler logs
tail -f $AIRFLOW_HOME/logs/scheduler/*.log

# Look for "DagFileProcessorProcess"
```

**Causes:**
1. Too many DAG files
2. Complex DAG parsing
3. Database slow

**Fixes:**
```python
# In airflow.cfg
[scheduler]
min_file_process_interval = 30  # Reduce if too high
dag_dir_list_interval = 300     # How often to scan for new files

[core]
parallelism = 32                # Increase if needed
max_active_runs_per_dag = 16    # Limit concurrent runs
```

---

### Issue 2: Tasks Stuck in "Queued"

**Symptom:** Tasks never move to "Running"  
**Diagnosis:**
```bash
# Check if workers are running
ps aux | grep "airflow celery worker"  # For Celery
ps aux | grep "airflow scheduler"       # For Local
```

**Fixes:**

**For LocalExecutor:**
```bash
# Restart scheduler
pkill -f "airflow scheduler"
airflow scheduler
```

**For CeleryExecutor:**
```bash
# Check worker status
airflow celery worker --concurrency 16

# Check queue
redis-cli LLEN celery
```

---

### Issue 3: XCom Serialization Error

**Error:** `Object of type 'DataFrame' is not JSON serializable`

**Fix:**
```python
# DON'T do this:
@task
def bad_example():
    import pandas as pd
    return pd.DataFrame({'a': [1,2,3]})  # ❌ Won't serialize

# DO this instead:
@task
def good_example():
    import pandas as pd
    df = pd.DataFrame({'a': [1,2,3]})
    return df.to_json()  # ✅ Serialized

@task
def use_data(json_data):
    import pandas as pd
    df = pd.read_json(json_data)  # ✅ Deserialize
```

---

### Issue 4: Task Timeout

**Error:** Task killed after running too long

**Fix:**
```python
# Option 1: Increase timeout per task
@task(execution_timeout=timedelta(hours=2))
def long_task():
    # Takes 90 minutes
    pass

#Option 2: Global default
# airflow.cfg
[operators]
default_task_execution_timeout = 7200  # 2 hours
```

---

### Issue 5: Database Deadlock

**Error:** `(psycopg2.OperationalError) FATAL: remaining connection slots`

**Cause:** Too many connections

**Fix:**
```python
# airflow.cfg
[core]
sql_alchemy_pool_size = 5
sql_alchemy_max_overflow = 10
sql_alchemy_pool_recycle = 1800

# Also increase PostgreSQL max_connections
# In postgresql.conf:
max_connections = 200
```

---

### Issue 6: Memory Leak

**Symptom:** Scheduler/Worker memory grows infinitely

**Diagnosis:**
```bash
# Monitor memory
watch -n 1 'ps aux | grep airflow'
```

**Fixes:**
```python
# airflow.cfg
[celery]
worker_max_tasks_per_child = 1000  # Restart worker after 1000 tasks

# In DAG:
@task
def task_with_cleanup():
    import gc
    
    # Your task code
    result = process_data()
    
    # Force garbage collection
    gc.collect()
    
    return result
```

---

### Issue 7: File Permission Errors

**Error:** `Permission denied: '/opt/airflow/logs'`

**Fix:**
```bash
# Set correct ownership
chown -R airflow:airflow $AIRFLOW_HOME/logs
chown -R airflow:airflow $AIRFLOW_HOME/dags

# Or use chmod (less secure)
chmod -R 777 $AIRFLOW_HOME/logs
```

---

## 🔬 Advanced Debugging

### Enable Debug Logging

```python
# airflow.cfg
[logging]
logging_level = DEBUG
fab_logging_level = DEBUG

# Or per DAG:
import logging
logging.getLogger("airflow.processors").setLevel(logging.DEBUG)
```

### Profile Slow DAGs

```python
from airflow.decorators import task
import cProfile

@task
def profile_me():
    profiler = cProfile.Profile()
    profiler.enable()
    
    # Your slow code
    result = expensive_operation()
    
    profiler.disable()
    profiler.print_stats(sort='cumtime')
    
    return result
```

### Trace SQL Queries

```python
# airflow.cfg
[core]
sql_alchemy_echo = True  # Log all SQL queries
```

---

## 📊 Monitoring Queries

### Check Running Tasks

```sql
SELECT 
    dag_id,
    task_id,
    state,
    start_date,
    EXTRACT(EPOCH FROM (NOW() - start_date))/60 as runtime_minutes
FROM task_instance
WHERE state = 'running'
ORDER BY runtime_minutes DESC;
```

### Find Slow DAGs

```sql
SELECT
    dag_id,
    AVG(EXTRACT(EPOCH FROM (end_date - start_date))/60) as avg_duration_minutes
FROM dag_run
WHERE state = 'success'
GROUP BY dag_id
ORDER BY avg_duration_minutes DESC
LIMIT 10;
```

### Identify Failed Tasks

```sql
SELECT
    dag_id,
    task_id,
    COUNT(*) as failure_count
FROM task_instance
WHERE state = 'failed'
    AND execution_date > NOW() - INTERVAL '7 days'
GROUP BY dag_id, task_id
ORDER BY failure_count DESC;
```

---

## 🚨 Emergency Procedures

### Kill Stuck Task

```bash
# Find process ID
ps aux | grep "my_task"

# Kill it
kill -9 <PID>

# Clear in Airflow
airflow tasks clear my_dag --task-regex my_task --start-date 2025-12-20
```

### Reset Entire DAG

```bash
# Nuclear option: clear all task instances
airflow dags delete my_dag

# Re-trigger
airflow dags trigger my_dag
```

### Database Cleanup

```bash
# Clean old task instances (older than 30 days)
airflow db clean --clean-before-timestamp $(date -d '30 days ago' +%Y-%m-%d) --yes
```

---

## 🎯 Preventive Measures

1. **Set resource limits:**
```python
default_args = {
    'execution_timeout': timedelta(hours=1),
    'retries': 2,
    'pool': 'database_pool',  # Limit concurrent DB tasks
}
```

2. **Use pools to prevent overload:**
```bash
# Create pool
airflow pools set database_pool 5 "Limit DB connections"
```

3. **Monitor scheduler health:**
```bash
# Set up alerting on this metric
airflow scheduler-health-check
```

4. **Regular maintenance:**
```bash
# Weekly cleanup
airflow db clean --clean-before-timestamp $(date -d '90 days ago' +%Y-%m-%d)
```

---

**Prevention > Cure when it comes to Airflow!** 🔧
