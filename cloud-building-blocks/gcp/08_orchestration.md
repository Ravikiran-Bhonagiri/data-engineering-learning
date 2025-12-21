# Orchestration 🎼

[← Back to Main](README.md)

Schedule and coordinate data pipelines in GCP.

---

## [Cloud Composer](https://cloud.google.com/composer)

Fully managed Apache Airflow service for workflow orchestration.

- **Why it matters:** Industry-standard orchestration. Same Apache Airflow as AWS MWAA.
- **Common Task:** Schedule daily big Query refreshes, coordinate multi-step ETL
- **Pricing:** Starting at ~$300/month (small environment) + worker/compute costs

### ✅ When to Use (Complex Workflows Justify Cost)

1. **Complex DAG Dependencies (Worth $300+/month)**
   - **Use Case:** 50+ interdependent tasks across services
   - **Cost Justification:** $300/month vs engineer-months building scheduler
   - **Why Composer:** Managed Airflow, no infrastructure
   - **Team Size:** Makes sense for teams of 3+ data engineers

2. **Integrating Multiple GCP Services**
   - **Operators:** Built-in for BigQuery, Dataflow, Dataproc, Cloud Storage
   - **Example:** Cloud Storage → Dataflow → BigQuery → Cloud SQL
   - **No Custom Code:** Pre-built operators vs writing glue code
   - **Velocity:** Days to setup vs weeks custom orchestration

3. **Existing Airflow Experience (Portability)**
   - **Same Airflow:** DAGs written for on-prem/AWS work unchanged
   - **Ecosystem:** 1000+ community operators
   - **Migration:** Lift-and-shift from self-hosted Airflow
   - **Future:** Not locked into GCP (can move DAGs elsewhere)

4. **Team Collaboration (Shared UI)**
   - **Web UI:** All team members view/trigger DAGs
   - **Git Integration:** Version control for DAG code
   - **per-Engineer:** $300÷5 = $60/month/person
   - **Complexity:** Centralized vs scattered scripts

5. **Dynamic/Programmatic Pipelines**
   - **Dynamic DAGs:** Generate tasks programmatically
   - **Parameters:** Pass runtime arguments to tasks
   - **Sensors:** Wait for conditions (file exists, table ready)
   - **When:** Need more than simple schedules

### ❌ When NOT to Use

- **Simple schedules (single task):** Cloud Scheduler cheaper ($0.10/job/month)
- **Linear workflows (<5 steps):** Workflows simpler for basic chains
- **Cost-sensitive startups:** $300 baseline too high; use Workflows
- **Serverless-only:** Composer requires understanding Airflow/workers
- **Small team (1-2 people):** Hard to justify $300/month

### Code Example - Cloud Composer DAG

```python
from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.providers.google.cloud.sensors.gcs import GCSObjectExistenceSensor
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
    
    # Wait for file
    wait_for_file = GCSObjectExistenceSensor(
        task_id='wait_for_file',
        bucket='my-bucket',
        object='raw/{{ ds }}/data.csv',
        timeout=3600
    )
    
    # Load to BigQuery
    load_bq = BigQueryInsertJobOperator(
        task_id='load_bigquery',
        configuration={
            'load': {
                'sourceUris': ['gs://my-bucket/raw/{{ ds }}/data.csv'],
                'destinationTable': {
                    'projectId': 'my-project',
                    'datasetId': 'staging',
                    'tableId': 'raw_data'
                }
            }
        }
    )
    
    wait_for_file >> load_bq
```

### Best Practices

- **Use environment variables** for config (not hardcode)
- **Enable auto-scaling** for workers (cost optimization)
- **Monitor with Cloud Monitoring** for DAG failures
- **Use Composer v2** (better performance, cheaper)
- **Separate envs** for dev/prod
- **Use XComs sparingly** (can cause memory issues)

---

## [Workflows](https://cloud.google.com/workflows)

Serverless orchestration for simple, linear workflows.

- **Why it matters:** Simpler and cheaper than Composer for basic orchestration
- **Common Task:** Chain Cloud Functions, BigQuery jobs, API calls
- **Pricing:** $0.01 per 1,000 internal steps (nearly free)

### ✅ When to Use (Simple Workflows)

1. **Serverless Orchestration (Start: Free tier)**
   - **Free:** 5,000 executions/month, 500 steps/execution
   - **Cost:** 1,000 daily executions (10 steps each) = ~$3/month
   - **vs Composer:** $300 minimum; Workflows for light usage
   - **Complexity:** YAML definition, no Python

2. **Linear Chains (2-10 steps)**
   - **Pattern:** Step A → Step B → Step C
   - **No Branching Complexity:** Simple conditional logic only
   - **Example:** Trigger Dataflow → Wait → Load BigQuery
   - **When:** Don't need full Airflow power

3. **Event-Driven (Triggered by events)**
   - **Triggers:** Pub/Sub message, HTTP request, Schedule
   - **Pay-per-Execution:** No baseline costs
   - **Scale:** Handles 1/day to 10,000/day automatically
   - **Cost Efficiency:** Pennies for most use cases

4. **Rapid Prototyping (No infrastructure)**
   - **Setup:** Minutes vs hours for Composer
   - **Iterate:** Edit YAML, deploy immediately
   - **Graduate:** Move to Composer if workflow outgrows Workflows
   - **Philosophy:** Start simple, add complexity when needed

### ❌ When NOT to Use

- **Complex DAGs (50+ tasks):** Workflows gets unwieldy; use Composer
- **Need Python logic:** Workflows is YAML/expressions; Composer for code
- **Team collaboration:** No shared UI like Airflow; Composer better
- **Backfills:** Limited historical execution handling
- **Dynamic workflows:** Can't generate tasks programmatically

### Code Example - Workflows

```yaml
# Deploy with: gcloud workflows deploy my-workflow --source=workflow.yaml
main:
  steps:
    - check_file:
        call: googleapis.storage.v1.objects.get
        args:
          bucket: my-bucket
          object: raw/data.csv
        result: file_exists
    
    - run_query:
        call: googleapis.bigquery.v2.jobs.query
        args:
          projectId: my-project
          body:
            query: SELECT COUNT(*) FROM dataset.table
            useLegacySql: false
        result: query_result
    
    - return_result:
        return: ${query_result}
```

---

## Related Topics

- **[Dataflow](02_compute_processing.md)**: Orchestrate Dataflow jobs
- **[BigQuery](05_analytics_warehousing.md)**: Schedule BigQuery refreshes
- **[Service Comparisons](11_service_comparisons.md)**: Composer vs Workflows

[← Back to Main](README.md)
