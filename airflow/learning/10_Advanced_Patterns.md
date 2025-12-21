# Advanced Airflow Patterns

**Goal:** Master advanced DAG patterns for complex workflows.

---

## Pattern 1: Task Groups

**Use Case:** Organize related tasks visually

```python
from airflow.decorators import dag, task, task_group
from datetime import datetime

@dag(start_date=datetime(2025, 12, 1), schedule='@daily')
def grouped_pipeline():
    
    @task_group
    def data_extraction():
        @task
        def extract_from_api():
            return "api_data"
        
        @task
        def extract_from_db():
            return "db_data"
        
        # Both run in parallel
        extract_from_api()
        extract_from_db()
    
    @task_group
    def data_validation():
        @task
        def validate_schema():
            print("Schema OK")
        
        @task
        def validate_quality():
            print("Quality OK")
        
        validate_schema()
        validate_quality()
    
    @task
    def final_load():
        print("Loading...")
    
    # Task groups link like regular tasks
    extraction = data_extraction()
    validation = data_validation()
    load = final_load()
    
    extraction >> validation >> load

dag = grouped_pipeline()
```

**UI View:**
```
[data_extraction]
  ├─ extract_from_api
  └─ extract_from_db
       ↓
[data_validation]
  ├─ validate_schema
  └─ validate_quality
       ↓
[final_load]
```

---

## Pattern 2: Dynamic DAG Generation

**Use Case:** Create DAGs programmatically from config

```python
# dags/dynamic_etl_dags.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

# Config (could be from JSON file or database)
TABLES = ['users', 'orders', 'products']

def create_etl_dag(table_name):
    dag = DAG(
        dag_id=f'etl_{table_name}',
        start_date=datetime(2025, 12, 1),
        schedule='@daily',
        catchup=False,
    )
    
    with dag:
        extract = PythonOperator(
            task_id='extract',
            python_callable=lambda: print(f"Extracting {table_name}")
        )
        
        transform = PythonOperator(
            task_id='transform',
            python_callable=lambda: print(f"Transforming {table_name}")
        )
        
        load = PythonOperator(
            task_id='load',
            python_callable=lambda: print(f"Loading {table_name}")
        )
        
        extract >> transform >> load
    
    return dag

# Generate 3 DAGs (etl_users, etl_orders, etl_products)
for table in TABLES:
    globals()[f'etl_{table}'] = create_etl_dag(table)
```

---

## Pattern 3: Custom Operators

**Use Case:** Reusable complex logic

```python
# plugins/custom_operators.py
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
import requests

class SlackNotificationOperator(BaseOperator):
    """Send custom Slack notification"""
    
    @apply_defaults
    def __init__(
        self,
        webhook_url: str,
        message: str,
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.webhook_url = webhook_url
        self.message = message
    
    def execute(self, context):
        # Access context for dynamic data
        dag_id = context['dag'].dag_id
        task_id = context['task_instance'].task_id
        execution_date = context['execution_date']
        
        payload = {
            'text': f"{self.message}\n"
                   f"DAG: {dag_id}\n"
                   f"Task: {task_id}\n"
                   f"Date: {execution_date}"
        }
        
        response = requests.post(self.webhook_url, json=payload)
        response.raise_for_status()
        
        self.log.info("Slack notification sent")

# Usage in DAG:
from custom_operators import SlackNotificationOperator

notify = SlackNotificationOperator(
    task_id='send_slack',
    webhook_url='https://hooks.slack.com/...',
    message='Pipeline completed successfully!',
)
```

---

## Pattern 4: Cross-DAG Dependencies (Datasets)

**Use Case:** Trigger DAG when data is ready (Airflow 2.4+)

```python
from airflow import Dataset

# Producer DAG
@dag(start_date=datetime(2025, 12, 1), schedule='@hourly')
def data_producer():
    @task(outlets=[Dataset('s3://bucket/data/sales.parquet')])
    def produce_data():
        # Write data to S3
        print("Data written to S3")
        return "s3://bucket/data/sales.parquet"
    
    produce_data()

# Consumer DAG (triggers when dataset updated)
@dag(
    start_date=datetime(2025, 12, 1),
    schedule=[Dataset('s3://bucket/data/sales.parquet')],  # ← Dataset-based trigger
)
def data_consumer():
    @task
    def consume_data():
        # Read from S3
        print("Processing S3 data")
    
    consume_data()

producer = data_producer()
consumer = data_consumer()
```

---

## Pattern 5: Conditional Task Execution

**Use Case:** Skip tasks based on runtime conditions

```python
from airflow.decorators import dag, task
from airflow.exceptions import AirflowSkipException

@dag(start_date=datetime(2025, 12, 1), schedule='@daily')
def conditional_pipeline():
    
    @task
    def check_if_weekend():
        from datetime import datetime
        if datetime.now().weekday() >= 5:  # Saturday or Sunday
            raise AirflowSkipException("Skipping on weekends")
        return "weekday"
    
    @task
    def process_data(day_type):
        print(f"Processing {day_type} data")
    
    day = check_if_weekend()
    process_data(day)

dag = conditional_pipeline()
```

---

## Pattern 6: Parallel Processing with Retries

**Use Case:** Process items in parallel with individual retries

```python
@dag(start_date=datetime(2025, 12, 1), schedule=None)
def parallel_with_retries():
    
    @task
    def get_items():
        return ['item1', 'item2', 'item3', 'item4', 'item5']
    
    @task(retries=3, retry_delay=timedelta(minutes=1))
    def process_item(item):
        import random
        
        # Simulate random failures
        if random.random() < 0.3:
            raise ValueError(f"Failed to process {item}")
        
        print(f"Successfully processed {item}")
        return item
    
    @task
    def summarize(results):
        print(f"Processed {len(results)} items")
    
    items = get_items()
    # Each item processed independently with own retries
    processed = process_item.expand(item=items)
    summarize(processed)

dag = parallel_with_retries()
```

---

## Pattern 7: Incremental Processing with State

**Use Case:** Track what's already processed

```python
from airflow.models import Variable

@dag(start_date=datetime(2025, 12, 1), schedule='@daily')
def incremental_load():
    
    @task
    def get_last_processed_id():
        # Get from Airflow Variable
        last_id = Variable.get('last_processed_id', default_var=0)
        return int(last_id)
    
    @task
    def extract_new_records(last_id):
        # Simulate DB query
        new_records = [
            {'id': last_id + 1, 'data': 'record1'},
            {'id': last_id + 2, 'data': 'record2'},
        ]
        return new_records
    
    @task
    def update_state(records):
        if records:
            max_id = max(r['id'] for r in records)
            Variable.set('last_processed_id', max_id)
            print(f"Updated state to ID {max_id}")
    
    last_id = get_last_processed_id()
    records = extract_new_records(last_id)
    update_state(records)

dag = incremental_load()
```

---

## Pattern 8: Fan-Out/Fan-In with Aggregation

**Use Case:** Process in parallel, then aggregate results

```python
@dag(start_date=datetime(2025, 12, 1), schedule='@daily')
def fan_out_fan_in():
    
    @task
    def split_data():
        return {
            'region_1': [1, 2, 3],
            'region_2': [4, 5, 6],
            'region_3': [7, 8, 9],
        }
    
    @task
    def process_region(region_name, data):
        total = sum(data)
        return {region_name: total}
    
    @task
    def aggregate_results(results):
        # results = [{'region_1': 6}, {'region_2': 15}, {'region_3': 24}]
        grand_total = sum(list(r.values())[0] for r in results)
        print(f"Grand total: {grand_total}")
    
    data = split_data()
    
    # Fan out: Process each region in parallel
    region_results = [] 
    for region, values in data.items():
        result = process_region(region, values)
        region_results.append(result)
    
    # Fan in: Aggregate all results
    aggregate_results(region_results)

dag = fan_out_fan_in()
```

---

## Pattern 9: Human-in-the-Loop (Coming in Airflow 3.0)

**Use Case:** Wait for manual approval

```python
from airflow.sensors.python import PythonSensor

@dag(start_date=datetime(2025, 12, 1), schedule=None)
def approval_workflow():
    
    @task
    def prepare_report():
        print("Report prepared")
        return "report.pdf"
    
    def check_approval():
        # Check external system or database for approval flag
        approval_status = Variable.get('deployment_approved', default_var='false')
        return approval_status == 'true'
    
    wait_for_approval = PythonSensor(
        task_id='wait_for_approval',
        python_callable=check_approval,
        poke_interval=60,
        timeout=3600,
    )
    
    @task
    def deploy():
        print("Deploying to production")
    
    report = prepare_report()
    report >> wait_for_approval >> deploy()

dag = approval_workflow()
```

---

## Pattern 10: Error Handling with Callbacks

**Use Case:** Custom actions on success/failure

```python
def task_success_callback(context):
    print(f"✅ Task {context['task_instance'].task_id} succeeded!")
    # Could send Slack message, update dashboard, etc.

def task_failure_callback(context):
    print(f"❌ Task {context['task_instance'].task_id} failed!")
    # Could create PagerDuty alert, rollback changes, etc.

@dag(
    start_date=datetime(2025, 12, 1),
    schedule='@daily',
    default_args={
        'on_success_callback': task_success_callback,
        'on_failure_callback': task_failure_callback,
    },
)
def callback_example():
    @task
    def risky_task():
        import random
        if random.random() < 0.5:
            raise ValueError("Random failure!")
        return "success"
    
    risky_task()

dag = callback_example()
```

---

## 🎯 Pattern Selection Guide

| Pattern | Use When |
|---------|----------|
| **Task Groups** | Organizing visually |
| **Dynamic DAGs** | Many similar DAGs |
| **Custom Operators** | Reusable logic |
| **Datasets** | Cross-DAG triggers |
| **Conditional** | Skip based on logic |
| **Parallel + Retries** | Independent items |
| **Incremental** | Large tables |
| **Fan-Out/Fan-In** | Parallel + aggregate |
| **Approval** | Manual intervention |
| **Callbacks** | Custom notifications |

---

**Master these patterns for production-grade DAGs!** 🚀
