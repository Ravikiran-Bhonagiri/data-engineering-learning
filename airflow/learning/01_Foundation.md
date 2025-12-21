# Apache Airflow Foundation

**For:** Data Engineers with SQL & Python experience  
**Goal:** Understand what Airflow is, why it matters, and when to use it.

---

## 🤔 The Problem: Manual Workflow Hell

### Before Airflow

Many data engineers start with individual scripts:

```python
# extract_data.py
import requests
data = requests.get('https://api.example.com/data').json()
with open('/tmp/data.json', 'w') as f:
    f.write(json.dumps(data))
```

```python
# transform_data.py
import pandas as pd
df = pd.read_json('/tmp/data.json')
df_clean = df.dropna()
df_clean.to_csv('/tmp/data_clean.csv')
```

```python
# load_data.py
import psycopg2
# Load CSV to database...
```

### Scheduled with cron:

```bash
0 6 * * * python /scripts/extract_data.py
10 6 * * * python /scripts/transform_data.py
20 6 * * * python /scripts/load_data.py
```

### What breaks:

1. **No dependency management:** If `extract` fails, `transform` still runs on stale data
2. **No retry logic:** One failure = manual intervention
3. **No monitoring:** Did it work? Check logs manually
4. **No backfilling:** Need to reprocess last week? Write custom scripts
5. **Hard to scale:** Adding new tasks means more cron entries

**This works until it doesn't.**

---

## ✅ The Solution: Apache Airflow

Airflow is a **workflow orchestration platform** that:
- Defines workflows as **DAGs** (Directed Acyclic Graphs)
- Manages **dependencies** automatically
- Provides **monitoring, retries, and logging**
- Scales from laptop to production clusters

### Same pipeline in Airflow:

```python
from datetime import datetime
from airflow.decorators import dag, task

@dag(
    dag_id="etl_pipeline",
    schedule="@daily",
    start_date=datetime(2025, 12, 1),
    catchup=False,
)
def pipeline():
    @task
    def extract():
        import requests
        data = requests.get('https://api.example.com/data').json()
        return data
    
    @task
    def transform(data):
        import pandas as pd
        df = pd.DataFrame(data)
        return df.dropna().to_dict('records')
    
    @task
    def load(data):
        # Load to database
        print(f"Loaded {len(data)} records")
    
    # Define dependencies
    raw = extract()
    clean = transform(raw)
    load(clean)

pipeline_dag = pipeline()
```

**What changed:**
- ✅ Dependencies: `transform` won't run if `extract` fails
- ✅ Retries: Automatic (configured in DAG)
- ✅ Monitoring: Web UI shows status
- ✅ Backfilling: `airflow dags backfill` command
- ✅ Scalable: Add more tasks = same code structure

---

## 🏗️ Airflow Architecture

### Core Components

```
┌─────────────┐
│  Web Server │  ← UI (http://localhost:8080)
└─────────────┘
       ↓
┌─────────────┐
│  Scheduler  │  ← Decides when tasks run
└─────────────┘
       ↓
┌─────────────┐
│   Executor  │  ← Runs tasks (Local/Celery/Kubernetes)
└─────────────┘
       ↓
┌─────────────┐
│   Workers   │  ← Execute the actual code
└─────────────┘
       ↓
┌─────────────┐
│  Metadata   │  ← PostgreSQL/MySQL (stores DAG runs, logs)
│  Database   │
└─────────────┘
```

### Workflow:

1. **Scheduler** parses DAG files from `$AIRFLOW_HOME/dags/`
2. **Scheduler** checks if tasks are ready (dependencies met)
3. **Executor** assigns ready tasks to **Workers**
4. **Workers** run the task code
5. **Metadata DB** records status (success/failure/retry)
6. **Web Server** displays everything in the UI

---

## 🆚 When to Use/Not Use Airflow

### ✅ Use Airflow For:

| Use Case | Why Airflow? |
|----------|--------------|
| **Batch ETL** | Schedule daily/hourly data pipelines |
| **ML Training** | Orchestrate feature extraction → training → deployment |
| **Report Generation** | Run analytics queries on schedule |
| **Data Quality Checks** | Run tests after data loads |
| **Multi-system workflows** | Coordinate tasks across DBs, APIs, cloud services |

### ❌ Don't Use Airflow For:

| Use Case | Why Not? | Alternative |
|----------|----------|-------------|
| **Real-time streaming** | Airflow is batch-oriented | Apache Kafka, Flink |
| **Event processing (<1s)** | Scheduler overhead too high | AWS Lambda, Cloud Functions |
| **Simple cron job** | Overkill for single tasks | Just use cron |
| **Data storage** | Airflow orchestrates, doesn't store | Use S3, databases |
| **Complex transformations** | Airflow orchestrates, doesn't process | Use Spark, dbt, pandas |

**Key principle:** Airflow **orchestrates**. It tells other tools when to run, not how to process data.

---

## 📊 Airflow vs. Alternatives

| Tool | Purpose | When to Use |
|------|---------|-------------|
| **Airflow** | Workflow orchestration | Complex DAGs with dependencies |
| **Cron** | Simple scheduling | Single independent tasks |
| **Prefect** | Workflow orchestration | Python-first, simpler than Airflow |
| **Dagster** | Data orchestration | Data-aware pipelines, ML |
| **Luigi** | Workflow orchestration | Legacy; Airflow is more popular |
| **Argo Workflows** | Kubernetes-native | If already on K8s |

**Airflow wins:** Battle-tested, huge community, extensive integrations.

---

## 🎓 Key Concepts (Quick Reference)

### DAG (Directed Acyclic Graph)
- **Directed:** Tasks have a specific order
- **Acyclic:** No loops (task A → B → A is not allowed)
- **Graph:** Visual representation of workflow

### Task
- Smallest unit of work in a DAG
- Example: `extract()`, `transform()`, `load()`

### Operator
- Template for a task
- Examples: `BashOperator`, `PythonOperator`, `PostgresOperator`

### Dependencies
```python
# Classic syntax
task1 >> task2 >> task3  # task1, then task2, then task3

# TaskFlow API (automatic)
result = transform(extract())  # extract() before transform()
```

### Scheduling
```python
schedule="@daily"        # Every day at midnight
schedule="0 6 * * *"     # Every day at 6 AM (cron syntax)
schedule="@hourly"       # Every hour
schedule=None            # Manual trigger only
```

---

## 🚀 What You'll Build

By the end of this course:
- ✅ Install Airflow locally
- ✅ Create production-ready DAGs
- ✅ Use operators, sensors, hooks
- ✅ Handle XComs, branching, dynamic tasks
- ✅ Build real ETL pipelines
- ✅ Debug and monitor workflows
- ✅ Deploy to production

**Next Step:** Open `02_Day_00.md` to start the hands-on course! 🎯
