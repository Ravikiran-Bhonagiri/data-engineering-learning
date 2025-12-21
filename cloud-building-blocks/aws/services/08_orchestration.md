# Orchestration 🎼

[← Back to Main](../README.md)

A pipeline is usually a series of steps. You need someone to manage the order and handle failures.

---

## [Amazon MWAA (Managed Workflows for Apache Airflow)](https://aws.amazon.com/managed-workflows-for-apache-airflow/)

A managed service for Apache Airflow that makes it easier to run open-source versions of Airflow on AWS.

- **Why it matters:** Airflow is the industry standard for orchestration. MWAA removes the pain of managing the servers/databases required to run it.
- **Common Task:** Scheduling daily ETL jobs with dependency management
- **Pricing:** Starts at ~$350/month for smallest environment

### ✅ When to Use (Complexity Justifies $350/month)

1. **Complex DAG Dependencies (Worth the cost)**
   - **Use Case:** 20+ ETL jobs with intricate dependencies
   - **Cost Math:** $350/month vs engineer months building custom scheduler
   - **Why MWAA:** Visual DAG UI, built-in retry logic, monitoring
   - **vs Cron:** MWAA for complex workflows, cron for simple schedules

2. **Team Collaboration (Multiple data engineers)**
   - **Benefit:** Web UI for all team members to view/trigger DAGs
   - **Version control:** Git integration for DAG code
   - **Cost per engineer:** $350÷5 engineers = $70/month/person
   - **Complexity:** Centralized vs scattered cron jobs

3. **Start with Open Source, Migrate When Ready**
   - **Start:** Self-hosted Airflow on EC2 (save $350/month initially)
   - **Pain points:** Upgrades, scaling, monitoring overhead
   - **Trigger:** When operational overhead > $350/month engineer time
   - **Philosophy:** Justify managed service with actual pain

4. **Built-in AWS Integrations**
   - **Operators:** GlueJobOperator, EMROperator, LambdaOperator ready
   - **vs DIY:** Write custom code to interact with AWS APIs
   - **Velocity:** Hours to setup vs days building integrations
   - **Example:** Orchestrate Glue → EMR → Redshift in minutes

5. **When Simplicity (EventBridge) Isn't Enough**
   - **EventBridge:** Simple triggers (S3 event → Lambda)
   - **Airflow:** Complex logic, retries, backfills, dependencies
   - **Decision:** EventBridge for 1-2 steps, Airflow for 5+ steps
   - **Cost:** EventBridge $1/M events vs MWAA $350 baseline

### ❌ When NOT to Use

- **Simple schedules:** Cron on EC2 or EventBridge cheaper for basic workflows
- **1-3 step workflows:** Step Functions simpler for basic orchestration
- **Cost-sensitive startup:** Self-host Airflow initially, migrate later
- **No complex dependencies:** If just "run job daily" use EventBridge
- **Small team (<3 people):** Hard to justify $350/month for 1-2 engineers

### Code Example - Simple Airflow DAG

```python
from airflow import DAG
from airflow.providers.amazon.aws.operators.glue import GlueJobOperator
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from datetime import datetime, timedelta

default_args = {
    'owner': 'data-team',
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    'daily_etl',
    default_args=default_args,
    schedule_interval='0 2 * * *',  # 2 AM daily
    start_date=datetime(2024, 1, 1),
    catchup=False
) as dag:
    
    # Wait for file to arrive
    wait_for_file = S3KeySensor(
        task_id='wait_for_file',
        bucket_name='my-data-lake',
        bucket_key='raw/2024/*/data.csv',
        timeout=3600
    )
    
    # Run Glue job
    run_glue = GlueJobOperator(
        task_id='transform_data',
        job_name='csv_to_parquet',
        script_location='s3://my-scripts/etl.py'
    )
    
    wait_for_file >> run_glue
```

---

## [AWS Step Functions](https://aws.amazon.com/step-functions/)

A visual workflow service that helps developers use AWS services to build distributed applications and automate processes.

- **Why it matters:** Great for serverless orchestration of Lambda functions and Glue jobs.
- **Common Task:** Building complex workflows with branching logic and error handling
- **Pricing:** $25 per million state transitions

### ✅ When to Use (Simple Workflows, Pay-per-Use)

1. **Serverless Orchestration (Start: $0 free tier)**
   - **Free tier:** 4,000 state transitions/month forever
   - **Cost:** 1,000 executions/day (30K transitions) = $0.75/month
   - **vs MWAA:** $350/month minimum; Step Functions for light usage
   - **Complexity:** Visual designer, no servers

2. **Lambda-centric Workflows (Native integration)**
   - **Use Case:** Lambda → Lambda → Lambda (data validation pipeline)
   - **Why:** Built for serverless, automatic retries
   - **Example:** Process S3 file → Validate → Transform → Store
   - **Cost:** Pennies for thousands of executions

3. **Simple Linear Workflows (2-5 steps)**
   - **Pattern:** Step A → Step B → Step C
   - **vs Airflow:** Overkill to deploy $350 MWAA for simple chains
   - **Visual editor:** Define workflows without code
   - **When:** No complex branching or hundreds of dependencies

4. **Event-Driven Automation**
   - **Trigger:** S3 event starts Step Functions
   - **Workflow:** Validate file → Run Glue → Notify SNS
   - **Cost:** Pay only when triggered (not 24/7 like MWAA)
   - **vs MWAA:** Step Functions for sporadic,MWAA for scheduled

5. **Rapid Prototyping (No infrastructure)**
   - **Setup time:** Minutes vs hours for Airflow
   - **Iterate:** Change workflow without redeploying
   - **Complexity:** Start here, graduate to MWAA if needs grow
   - **Philosophy:** Simplest tool that works

### ❌ When NOT to Use

- **Complex dependencies:** 50+ tasks with intricate relationships; use Airflow
- **Need DAG visualization:** Step Functions basic UI; Airflow has rich DAG views
- **Python custom logic:** Step Functions JSON-based; Airflow full Python
- **Backfills/reruns:** Limited historical execution handling; Airflow excels
- **Team collaboration:** No shared UI for data team; MWAA better for teams

---

## Related Topics

- **[Daily Workflow](16_daily_workflow.md)**: See how orchestration fits into pipelines
- **[Compute & Processing](02_compute_processing.md)**: Services to orchestrate
- **[Monitoring & Logging](09_monitoring_logging.md)**: Monitor workflows

[← Back to Main](../README.md)
