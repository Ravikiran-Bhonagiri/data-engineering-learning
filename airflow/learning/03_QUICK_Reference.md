# Airflow Quick Reference Guide

**For:** Interview prep and daily use  
**Contains:** Commands, patterns, troubleshooting, and interview Q&A

---

## ⚡ Essential Commands

### DAG Management
```bash
# List all DAGs
airflow dags list

# Trigger a DAG
airflow dags trigger my_dag

# Pause/unpause DAG
airflow dags pause my_dag
airflow dags unpause my_dag

# Check DAG structure
airflow dags show my_dag

# Test DAG for errors
airflow dags list-import-errors
```

### Task Management
```bash
# Run a specific task
airflow tasks run my_dag my_task 2025-12-20

# Test task (doesn't save state)
airflow tasks test my_dag my_task 2025-12-20

# View task logs
airflow tasks logs my_dag my_task 2025-12-20

# List tasks in DAG
airflow tasks list my_dag
```

### Backfilling
```bash
# Backfill past dates
airflow dags backfill my_dag \
    --start-date 2025-12-01 \
    --end-date 2025-12-20

# Clear task state (for re-run)
airflow tasks clear my_dag --start-date 2025-12-20
```

### Database & Users
```bash
# Initialize database
airflow db init

# Upgrade database
airflow db upgrade

# Create admin user
airflow users create \
    --username admin \
    --password admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com
```

---

## 🎨 Common DAG Patterns

### Pattern 1: Simple Linear ETL
```python
@dag(start_date=datetime(2025, 12, 1), schedule='@daily')
def etl():
    extract() >> transform() >> load()
```

### Pattern 2: Parallel Processing
```python
@dag(...)
def parallel():
    start = dummy_task()
    end = dummy_task()
    
    start >> [task1(), task2(), task3()] >> end
```

### Pattern 3: Conditional Branching
```python
def choose_path():
    return 'task_a' if condition else 'task_b'

branch = BranchPythonOperator(...)
branch >> [task_a, task_b]
```

### Pattern 4: Dynamic Task Mapping
```python
@task
def get_items():
    return ['item1', 'item2', 'item3']

@task
def process(item):
    print(f"Processing {item}")

process.expand(item=get_items())
```

### Pattern 5: Sensor + Process
```python
wait = FileSensor(filepath='/tmp/data.csv', ...)
wait >> process_file()
```

---

## 🐛 Troubleshooting Guide

### Error: "DAG not found"
**Cause:** Scheduler hasn't scanned yet  
**Fix:** Wait 30s or restart scheduler

### Error: "Task stuck in queued"
**Cause:** No workers running  
**Fix:** `airflow celery worker` or check executor config

### Error: "Import error in DAG"
**Cause:** Syntax error in Python file  
**Fix:** `airflow dags list-import-errors`

### Error: "Task fails but no logs"
**Cause:** Exception swallowed  
**Fix:** Always `raise` exceptions, never just `pass`

### Error: "Circular dependency detected"
**Cause:** Task A depends on B, B depends on A  
**Fix:** Refactor DAG structure

### Error: "XCom value too large"
**Cause:** Trying to pass >48KB via XCom  
**Fix:** Store in S3/GCS, pass path instead

---

## 📚 Schedule Expressions

| Expression | Meaning | Runs |
|------------|---------|------|
| `@once` | Run once | Never again |
| `@hourly` | Every hour | `0 * * * *` |
| `@daily` | Every day midnight | `0 0 * * *` |
| `@weekly` | Every Sunday | `0 0 * * 0` |
| `@monthly` | First of month | `0 0 1 * *` |
| `@yearly` | Jan 1st | `0 0 1 1 *` |
| `None` | Manual only | Never |
| `0 6 * * *` | 6 AM daily | Custom cron |
| `*/15 * * * *` | Every 15 min | Custom cron |

---

## 🎓 Interview Questions & Answers

### Q: What is Airflow?
**A:** Airflow is an open-source workflow orchestration platform that lets you programmatically author, schedule, and monitor data pipelines. Workflows are defined as DAGs (Directed Acyclic Graphs) using Python code.

### Q: What is a DAG?
**A:** A Directed Acyclic Graph - a collection of tasks with defined dependencies. "Directed" means tasks run in a specific order, "Acyclic" means no loops.

### Q: Explain Airflow architecture.
**A:** Airflow has 4 main components:
1. **Webserver:** UI for monitoring
2. **Scheduler:** Triggers tasks when ready
3. **Executor:** Runs tasks (Local, Celery, K8s)
4. **Metadata Database:** Stores DAG/task state

### Q: What's the difference between operators and hooks?
**A:** 
- **Operators:** Templates for tasks (BashOperator, PythonOperator)
- **Hooks:** Interfaces to external systems (PostgresHook, S3Hook)

### Q: What is XCom?
**A:** Cross-communication - a mechanism for tasks to exchange small amounts of data (<48KB). Data is stored in the metadata database.

### Q: When would you NOT use Airflow?
**A:** 
- Real-time streaming (use Kafka/Flink)
- Sub-second latency requirements
- Simple single-task cron jobs
- When you need to process data (Airflow orchestrates, doesn't process)

### Q: How do you handle failures?
A: Multiple strategies:
- **Retries:** `retries=3` in default_args
- **Alerts:** Email/Slack on failure
- **Branches:** Conditional execution paths
- **Sensors:** Wait for conditions before proceeding

### Q: What's the difference between `schedule_interval` and `start_date`?
**A:** 
- `start_date`: When DAG becomes active
- `schedule_interval`: How often it runs after start_date

### Q: What is `catchup`?
**A:** If `True`, Airflow backfills all missed runs between `start_date` and now. Usually set to `False` in production.

### Q: How do you deploy DAGs to production?
**A:** Common methods:
1. Git sync (DAGs in version control)
2. CI/CD pipeline (test → deploy)
3. DAG bundling (package DAGs with dependencies)

---

## 🔐 Security Best Practices

✅ Use secrets backend (AWS Secrets Manager, Vault)  
✅ Enable RBAC in webserver  
✅ Encrypt connections with Fernet key  
✅ Don't hardcode credentials in DAG files  
✅ Use service accounts, not personal credentials  
✅ Rotate secrets regularly  

---

## 📊 Performance Tips

1. **Use pools** to limit concurrent tasks
2. **Set priority_weight** for critical tasks
3. **Use deferrable operators** for sensors
4. **Optimize `concurrency`** and `parallelism`
5. **Enable remote logging** (S3/GCS)
6. **Use KubernetesExecutor** for auto-scaling

---

## 🎯 Production Checklist

- [ ] PostgreSQL/MySQL database (not SQLite)
- [ ] CeleryExecutor or KubernetesExecutor
- [ ] Remote logging configured
- [ ] Email/Slack alerts set up
- [ ] Secrets backend configured
- [ ] RBAC enabled
- [ ] Monitoring (Prometheus/Grafana)
- [ ] Unit tests for DAGs
- [ ] Documentation in DAG description
- [ ] `catchup=False` on new DAGs

---

## 💡 Pro Tips

1. **Always use TaskFlow API** for new DAGs (cleaner code)
2. **Tag your DAGs** for better organization
3. **Use Variables** for configuration, not hardcoded values
4. **Test DAGs locally** before deploying
5. **Monitor scheduler lag** in production
6. **Use SLAs** to catch slow tasks
7. **Document dependencies** in DAG description
8. **Version control** your DAG files

---

## 📖 Resources

- Official Docs: [airflow.apache.org](https://airflow.apache.org)
- Community: [Airflow Slack](https://apache-airflow-slack.herokuapp.com/)
- Best Practices: [Astronomer Guides](https://www.astronomer.io/guides/)

---

**You're now ready to ace Airflow interviews and build production pipelines!** 🚀
