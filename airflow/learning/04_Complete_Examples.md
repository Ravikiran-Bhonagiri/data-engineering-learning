# Complete Airflow Examples

**Goal:** Learn by studying 3 complete, production-ready DAG examples.  
**Each includes:** Full code, setup instructions, and explanation.

---

## Example 1: E-commerce Sales Pipeline

**Scenario:** Daily ETL pipeline that extracts yesterday's sales from an API, transforms the data, and loads it to PostgreSQL.

### Complete Code

```python
from datetime import datetime, timedelta
from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.http.hooks.http import HttpHook
import pandas as pd

@dag(
    dag_id='ecommerce_sales_pipeline',
    start_date=datetime(2025, 12, 1),
    schedule='0 6 * * *',  # Daily at 6 AM
    catchup=False,
    default_args={
        'retries': 3,
        'retry_delay': timedelta(minutes=5),
        'email_on_failure': True,
        'email': ['data-team@company.com'],
    },
    tags=['production', 'sales', 'etl'],
    description='Daily sales data ETL from API to Postgres',
)
def sales_pipeline():
    
    @task
    def extract_sales_data():
        """Extract yesterday's sales from REST API"""
        from datetime import date
        
        yesterday = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
        
        hook = HttpHook(http_conn_id='sales_api', method='GET')
        response = hook.run(f'sales?date={yesterday}')
        
        data = response.json()
        print(f"✓ Extracted {len(data['sales'])} sales records for {yesterday}")
        
        return data['sales']
    
    @task
    def transform_sales(raw_sales):
        """Clean and enrich sales data"""
        df = pd.DataFrame(raw_sales)
        
        # Data quality checks
        initial_count = len(df)
        df = df.dropna(subset=['order_id', 'customer_id', 'amount'])
        df = df[df['amount'] > 0]
        
        print(f"✓ Cleaned data: {initial_count} → {len(df)} records")
        
        # Calculate metrics
        df['tax'] = df['amount'] * 0.08
        df['total'] = df['amount'] + df['tax']
        df['order_date'] = pd.to_datetime(df['order_date'])
        
        # Add derived fields
        df['year'] = df['order_date'].dt.year
        df['month'] = df['order_date'].dt.month
        df['day_of_week'] = df['order_date'].dt.dayofweek
        
        return df.to_dict('records')
    
    @task
    def load_to_postgres(sales_data):
        """Load transformed data to PostgreSQL"""
        hook = PostgresHook(postgres_conn_id='postgres_warehouse')
        
        # Prepare insert statement
        for record in sales_data:
            hook.run(
                """
                INSERT INTO sales_fact (
                    order_id, customer_id, product_id, 
                    amount, tax, total, order_date,
                    year, month, day_of_week
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (order_id) DO UPDATE SET
                    amount = EXCLUDED.amount,
                    tax = EXCLUDED.tax,
                    total = EXCLUDED.total;
                """,
                parameters=(
                    record['order_id'],
                    record['customer_id'],
                    record['product_id'],
                    record['amount'],
                    record['tax'],
                    record['total'],
                    record['order_date'],
                    record['year'],
                    record['month'],
                    record['day_of_week'],
                )
            )
        
        print(f"✓ Loaded {len(sales_data)} records to sales_fact table")
        return len(sales_data)
    
    @task
    def validate_load(record_count):
        """Validate data was loaded correctly"""
        hook = PostgresHook(postgres_conn_id='postgres_warehouse')
        
        # Check today's load
        result = hook.get_first(
            "SELECT COUNT(*) FROM sales_fact WHERE DATE(order_date) = CURRENT_DATE - 1"
        )
        
        loaded_count = result[0]
        
        if loaded_count != record_count:
            raise ValueError(f"Validation failed: Expected {record_count}, found {loaded_count}")
        
        print(f"✓ Validation passed: {loaded_count} records")
    
    # Build the pipeline
    raw = extract_sales_data()
    transformed = transform_sales(raw)
    count = load_to_postgres(transformed)
    validate_load(count)

dag = sales_pipeline()
```

### Setup Instructions

1. **Create Connections in Airflow UI:**
   - `sales_api`: HTTP connection to API
   - `postgres_warehouse`: PostgreSQL connection

2. **Create Database Table:**
```sql
CREATE TABLE sales_fact (
    order_id VARCHAR(50) PRIMARY KEY,
    customer_id INT NOT NULL,
    product_id INT NOT NULL,
    amount DECIMAL(10,2),
    tax DECIMAL(10,2),
    total DECIMAL(10,2),
    order_date DATE,
    year INT,
    month INT,
    day_of_week INT,
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

3. **Deploy DAG:**
   - Save to `$AIRFLOW_HOME/dags/sales_pipeline.py`
   - Verify in UI
   - Test run

---

## Example 2: ML Model Training Pipeline

**Scenario:** Weekly pipeline that prepares data, trains a model, evaluates it, and deploys if accuracy improves.

### Complete Code

```python
from datetime import datetime, timedelta
from airflow.decorators import dag, task
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.operators.python import BranchPythonOperator
import pandas as pd
import pickle

@dag(
    dag_id='ml_training_pipeline',
    start_date=datetime(2025, 12, 1),
    schedule='0 2 * * 0',  # Weekly on Sunday at 2 AM
    catchup=False,
    default_args={'retries': 2},
    tags=['ml', 'production'],
)
def ml_pipeline():
    
    @task
    def fetch_training_data():
        """Fetch last week's data from S3"""
        s3 = S3Hook(aws_conn_id='aws_default')
        
        # Download CSV from S3
        data = s3.read_key(
            key='data/training/features.csv',
            bucket_name='ml-bucket'
        )
        
        df = pd.read_csv(pd.io.common.BytesIO(data.encode()))
        print(f"✓ Fetched {len(df)} training samples")
        
        return df.to_json()
    
    @task
    def prepare_features(data_json):
        """Feature engineering"""
        df = pd.read_json(data_json)
        
        # Feature engineering
        df['feature_1_squared'] = df['feature_1'] ** 2
        df['interaction'] = df['feature_1'] * df['feature_2']
        
        # Split features and target
        X = df.drop('target', axis=1)
        y = df['target']
        
        return {
            'X': X.to_json(),
            'y': y.to_json()
        }
    
    @task
    def train_model(data):
        """Train ML model"""
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.model_selection import train_test_split
        
        X = pd.read_json(data['X'])
        y = pd.read_json(data['y'], typ='series')
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Evaluate
        accuracy = model.score(X_test, y_test)
        print(f"✓ Model trained. Accuracy: {accuracy:.4f}")
        
        # Serialize model
        model_bytes = pickle.dumps(model)
        
        return {
            'model': model_bytes.hex(),
            'accuracy': accuracy
        }
    
    def should_deploy(**context):
        """Decide if model should be deployed"""
        ti = context['ti']
        result = ti.xcom_pull(task_ids='train_model')
        
        accuracy = result['accuracy']
        threshold = 0.85
        
        if accuracy >= threshold:
            print(f"✓ Accuracy {accuracy:.4f} >= {threshold}. Deploying.")
            return 'deploy_model'
        else:
            print(f"✗ Accuracy {accuracy:.4f} < {threshold}. Skipping deploy.")
            return 'skip_deploy'
    
    @task
    def deploy_model(**context):
        """Deploy model to S3"""
        ti = context['ti']
        result = ti.xcom_pull(task_ids='train_model')
        
        model_bytes = bytes.fromhex(result['model'])
        
        s3 = S3Hook(aws_conn_id='aws_default')
        s3.load_bytes(
            bytes_data=model_bytes,
            key='models/production/model.pkl',
            bucket_name='ml-bucket',
            replace=True
        )
        
        print(f"✓ Model deployed to S3")
    
    @task
    def skip_deploy():
        print("Skipping deployment due to low accuracy")
    
    # Build pipeline
    data = fetch_training_data()
    features = prepare_features(data)
    model_result = train_model(features)
    
    branch = BranchPythonOperator(
        task_id='decide_deploy',
        python_callable=should_deploy
    )
    
    deploy = deploy_model()
    skip = skip_deploy()
    
    model_result >> branch >> [deploy, skip]

dag = ml_pipeline()
```

---

## Example 3: Data Quality Monitor with Alerts

**Scenario:** Hourly pipeline that checks data quality metrics and sends Slack alerts if issues are found.

### Complete Code

```python
from datetime import datetime, timedelta
from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator

@dag(
    dag_id='data_quality_monitor',
    start_date=datetime(2025, 12, 1),
    schedule='0 * * * *',  # Hourly
    catchup=False,
    tags=['monitoring', 'data-quality'],
)
def quality_monitor():
    
    @task
    def check_null_rates():
        """Check for excessive NULL values"""
        hook = PostgresHook(postgres_conn_id='postgres_warehouse')
        
        query = """
        SELECT 
            column_name,
            COUNT(*) FILTER (WHERE value IS NULL) * 100.0 / COUNT(*) as null_pct
        FROM information_schema.columns
        CROSS JOIN LATERAL (
            SELECT column_name as value FROM users
        ) data
        GROUP BY column_name
        HAVING COUNT(*) FILTER (WHERE value IS NULL) * 100.0 / COUNT(*) > 10
        """
        
        results = hook.get_pandas_df(query)
        
        if len(results) > 0:
            return {
                'status': 'FAIL',
                'issue': f"High NULL rates in columns: {results['column_name'].tolist()}"
            }
        
        return {'status': 'PASS'}
    
    @task
    def check_row_counts():
        """Check for unexpected row count changes"""
        hook = PostgresHook(postgres_conn_id='postgres_warehouse')
        
        today_count = hook.get_first("SELECT COUNT(*) FROM sales_fact WHERE DATE(order_date) = CURRENT_DATE")[0]
        avg_count = hook.get_first("SELECT AVG(cnt) FROM (SELECT COUNT(*) as cnt FROM sales_fact GROUP BY DATE(order_date)) t")[0]
        
        if today_count < avg_count * 0.5:
            return {
                'status': 'FAIL',
                'issue': f"Row count too low: {today_count} vs avg {avg_count:.0f}"
            }
        
        return {'status': 'PASS'}
    
    @task
    def check_duplicates():
        """Check for duplicate primary keys"""
        hook = PostgresHook(postgres_conn_id='postgres_warehouse')
        
        dup_count = hook.get_first(
            "SELECT COUNT(*) FROM (SELECT order_id, COUNT(*) FROM sales_fact GROUP BY order_id HAVING COUNT(*) > 1) t"
        )[0]
        
        if dup_count > 0:
            return {
                'status': 'FAIL',
                'issue': f"Found {dup_count} duplicate order_ids"
            }
        
        return {'status': 'PASS'}
    
    @task
    def compile_report(null_check, row_check, dup_check):
        """Compile all checks into a report"""
        all_checks = [null_check, row_check, dup_check]
        failures = [c for c in all_checks if c['status'] == 'FAIL']
        
        if failures:
            issues = '\n'.join([f"• {f['issue']}" for f in failures])
            return {
                'alert_needed': True,
                'message': f"⚠️ Data Quality Issues Detected:\n{issues}"
            }
        
        return {
            'alert_needed': False,
            'message': "✅ All data quality checks passed"
        }
    
    # Run checks in parallel
    nulls = check_null_rates()
    rows = check_row_counts()
    dups = check_duplicates()
    
    report = compile_report(nulls, rows, dups)
    
    # Send Slack alert if needed
    alert = SlackWebhookOperator(
        task_id='send_slack_alert',
        slack_webhook_conn_id='slack_webhook',
        message="{{ ti.xcom_pull(task_ids='compile_report')['message'] }}",
    )
    
    report >> alert

dag = quality_monitor()
```

---

## 🎯 Key Takeaways from Examples

✅ **Example 1:** Full ETL with validation  
✅ **Example 2:** Branching based on model performance  
✅ **Example 3:** Parallel checks with alerting  

All examples are **production-ready** and can be adapted to your use cases!
