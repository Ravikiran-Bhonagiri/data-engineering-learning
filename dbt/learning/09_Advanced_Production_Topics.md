# Advanced dbt Topics & Production Best Practices

**Problem Solved:** You need to go beyond basics for production deployments.

This guide covers advanced patterns, optimization, and real-world challenges.

---

## 1. Advanced Materialization Strategies

### Incremental Models - Deep Dive

**Basic Incremental:**
```sql
{{ config(materialized='incremental', unique_key='id') }}

SELECT * FROM {{ source('raw', 'events') }}
{% if is_incremental() %}
WHERE created_at > (SELECT MAX(created_at) FROM {{ this }})
{% endif %}
```

**Problem:** Late-arriving data (event created yesterday but loaded today)

**Solution: Lookback Window**
```sql
{{ config(materialized='incremental', unique_key='id') }}

SELECT * FROM {{ source('raw', 'events') }}
{% if is_incremental() %}
WHERE created_at > (SELECT MAX(created_at) - INTERVAL '3 days' FROM {{ this }})
{% endif %}
```

**Advanced: Merge with Updates**
```sql
{{ config(
    materialized='incremental',
    unique_key='order_id',
    incremental_strategy='merge',
    merge_update_columns=['status', 'updated_at'],
    merge_exclude_columns=['created_at']
) }}

SELECT * FROM {{ source('raw', 'orders') }}
{% if is_incremental() %}
WHERE updated_at > (SELECT MAX(updated_at) FROM {{ this }})
{% endif %}
```

---

## 2. dbt Mesh (Multi-Project Architecture)

**Scenario:** Multiple teams, one data warehouse

### Project Structure

```
company_dbt/
├── core_data/           # Shared dimensions (owned by Platform team)
│   └── models/
│       └── dim_customers.sql
├── finance_analytics/   # Finance-specific (owned by Finance team)
│   └── models/
│       └── fct_revenue.sql  # Uses core_data.dim_customers
└── marketing_analytics/ # Marketing-specific
    └── models/
        └── fct_campaigns.sql  # Uses core_data.dim_customers
```

### Cross-Project References

**core_data `dbt_project.yml`:**
```yaml
models:
  core_data:
    +access: public  # Allow other projects to ref()
```

**finance_analytics `dependencies.yml`:**
```yaml
projects:
  - name: core_data
```

**finance_analytics model:**
```sql
-- Can reference models from core_data
SELECT * 
FROM {{ ref('core_data', 'dim_customers') }}  -- Cross-project ref!
```

**Benefits:**
- Team autonomy
- Clear ownership
- Shared dimensions
- Independent deployment

---

## 3. dbt Semantic Layer & Metrics

### Define Metrics Once

**models/metrics/revenue_metrics.yml:**
```yaml
metrics:
  - name: total_revenue
    label: Total Revenue
    model: ref('fct_orders')
    calculation_method: sum
    expression: order_amount
    timestamp: order_date
    time_grains: [day, week, month, quarter, year]
    dimensions:
      - customer_segment
      - product_category
    
  - name: avg_order_value
    label: Average Order Value
    model: ref('fct_orders')
    calculation_method: average
    expression: order_amount
```

### Query Metrics via API

```python
# From BI tool or application
import requests

response = requests.post(
    'https://semantic-layer.getdbt.com/api/graphql',
    headers={'Authorization': 'Bearer YOUR_TOKEN'},
    json={
        'query': '''
          query {
            metrics(
              metrics: ["total_revenue", "avg_order_value"]
              groupBy: ["customer_segment"]
              where: [{ sql: "order_date >= '2024-01-01'" }]
            ) {
              data
            }
          }
        '''
    }
)
```

---

## 4. Advanced Testing Patterns

### Data Anomaly Detection

**tests/data_quality/revenue_spike_detection.sql:**
```sql
WITH daily_revenue AS (
    SELECT
        DATE_TRUNC('day', order_date) AS day,
        SUM(amount) AS revenue
    FROM {{ ref('fct_orders') }}
    GROUP BY 1
),

stats AS (
    SELECT
        AVG(revenue) AS avg_revenue,
        STDDEV(revenue) AS stddev_revenue
    FROM daily_revenue
    WHERE day >= CURRENT_DATE - 30
),

anomalies AS (
    SELECT
        d.day,
        d.revenue,
        s.avg_revenue,
        s.stddev_revenue
    FROM daily_revenue d
    CROSS JOIN stats s
    WHERE d.day = CURRENT_DATE
      AND ABS(d.revenue - s.avg_revenue) > 3 * s.stddev_revenue  -- 3 sigma
)

SELECT * FROM anomalies
```

### Custom Generic Tests

**macros/tests/test_valid_email.sql:**
```sql
{% test valid_email(model, column_name) %}
    SELECT {{ column_name }}
    FROM {{ model }}
    WHERE {{ column_name }} IS NOT NULL
      AND {{ column_name }} !~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
{% endtest %}
```

**Usage:**
```yaml
columns:
  - name: email
    tests:
      - valid_email
```

---

## 5. Performance Optimization

### Diagnosis: `dbt --debug` Logs

```bash
dbt run --debug --select my_slow_model
```

Look for:
- Compile time (should be <1s)
- Execution time (warehouse-dependent)
- Row count (millions of rows?)

### Optimization Strategies

**1. Limit CTE Nesting**
```sql
-- ❌ Bad (5 CTEs)
WITH a AS (...),
b AS (SELECT * FROM a WHERE ...),
c AS (SELECT * FROM b WHERE ...),
d AS (SELECT * FROM c WHERE ...),
e AS (SELECT * FROM d WHERE ...)
SELECT * FROM e

-- ✅ Good (break into intermediate models)
-- int_model_1.sql
WITH a AS (...),
b AS (SELECT * FROM a WHERE ...)
SELECT * FROM b

-- int_model_2.sql
WITH c AS (SELECT * FROM {{ ref('int_model_1') }} WHERE ...)
SELECT * FROM c
```

**2. Use Incremental for Large Tables**
```sql
-- ✅ For tables >100M rows
{{ config(materialized='incremental') }}
```

**3. Optimize Joins**
```sql
-- ❌ Bad (large table first)
FROM {{ ref('fact_orders') }} orders  -- 100M rows
JOIN {{ ref('dim_customers') }} customers  -- 10K rows

-- ✅ Good (small table first for hash joins)
FROM {{ ref('dim_customers') }} customers  -- 10K rows
JOIN {{ ref('fact_orders') }} orders  -- 100M rows
```

**4. Warehouse-Specific Optimization**
- **Snowflake:** Add clustering
- **BigQuery:** Partition + cluster
- **Redshift:** Distribution + sort keys

---

## 6. Blue/Green Deployments

**Pattern:** Deploy to parallel schema, then swap

```sql
-- Job 1: Deploy to blue schema
dbt run --target blue  # Writes to dbt_blue schema

-- Job 2: Validate
dbt test --target blue

-- Job 3: Swap (via script)
-- ALTER SCHEMA dbt_prod RENAME TO dbt_old;
-- ALTER SCHEMA dbt_blue RENAME TO dbt_prod;
-- ALTER SCHEMA dbt_old RENAME TO dbt_blue;
```

**Benefits:**
- Zero downtime
- Rollback capability
- Validation before switching

---

## 7. Secrets Management

**Never commit passwords!**

### Option 1: Environment Variables

**profiles.yml:**
```yaml
my_project:
  target: prod
  outputs:
    prod:
      type: snowflake
      account: "{{ env_var('SNOWFLAKE_ACCOUNT') }}"
      user: "{{ env_var('SNOWFLAKE_USER') }}"
      password: "{{ env_var('SNOWFLAKE_PASSWORD') }}"
```

**Set in shell:**
```bash
export SNOWFLAKE_PASSWORD='my_secure_password'
dbt run
```

### Option 2: dbt Cloud (Managed)

Credentials stored encrypted in dbt Cloud UI.

### Option 3: Secrets Manager (AWS/GCP)

```bash
# Fetch from AWS Secrets Manager
export SNOWFLAKE_PASSWORD=$(aws secretsmanager get-secret-value \
    --secret-id prod/dbt/snowflake --query SecretString --output text)
dbt run
```

---

## 8. Data Contracts

**Enforce schema on sources:**

```yaml
# models/staging/schema.yml
sources:
  - name: raw
    tables:
      - name: customers
        columns:
          - name: id
            data_type: integer
            constraints:
              - type: not_null
              - type: unique
          - name: email
            data_type: varchar
            constraints:
              - type: not_null
```

**dbt will fail if source doesn't match contract!**

---

## 9. CI/CD Best Practices

### Slim CI (Only Test Changed Models)

```yaml
# .github/workflows/dbt_ci.yml
name: dbt CI
on: [pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      
      # Download production manifest
      - name: Download prod manifest
        run: |
          dbt run-operation stage_external_sources  # If needed
          dbt compile --target prod
      
      # Run only modified models
      - name: Test changes
        run: |
          dbt build --select state:modified+ \
            --defer --state ./target_prod
```

**Saves 90% of CI time!**

---

## 10. Monitoring & Alerts

### Slack Alerts on Failure

**dbt Cloud:**
Built-in integration (Settings → Notifications).

**dbt Core + Airflow:**
```python
from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator

def dbt_failure_callback(context):
    SlackWebhookOperator(
        task_id='slack_alert',
        webhook_token='YOUR_WEBHOOK',
        message=f"dbt run failed: {context['task_instance']}"
    ).execute(context)

dbt_task = BashOperator(
    task_id='dbt_run',
    bash_command='dbt run',
    on_failure_callback=dbt_failure_callback
)
```

### Data Quality Dashboard

Track test failures over time:
```sql
-- models/monitoring/data_quality_metrics.sql
SELECT
    DATE_TRUNC('day', created_at) AS test_date,
    test_name,
    COUNT(*) FILTER (WHERE status = 'pass') AS passes,
    COUNT(*) FILTER (WHERE status = 'fail') AS failures
FROM {{ ref('dbt_test_results') }}  -- If using artifacts
GROUP BY 1, 2
```

---

## 11. Common Production Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| **Slow incremental model** | No indexes, poor partition | Add clustering/partitioning |
| **Test failures in prod** | Data quality regression | Add `--warn-error` to catch early |
| **Circular dependency** | Model refs itself (indirectly) | Check DAG, break cycle |
| **Out of memory** | Too many CTEs, large datasets | Break into intermediate models |
| **Permission denied** | Wrong warehouse role | Update `profiles.yml` role |

---

## 12. Pro Tips

✅ **Use `--vars` for environment-specific logic**
```bash
dbt run --vars '{"is_prod": true}'
```

✅ **Tag models for selective runs**
```yaml
{{ config(tags=['daily', 'finance']) }}
```

```bash
dbt run --select tag:daily
```

✅ **Pre/Post Hooks for custom logic**
```yaml
{{ config(
    pre_hook="GRANT SELECT ON {{ this }} TO analyst_role",
    post_hook="ANALYZE {{ this }}"
) }}
```

✅ **Use `on-run-end` hooks for notifications**
```yaml
# dbt_project.yml
on-run-end:
  - "{{ log_run_results() }}"  # Custom macro
```

---

**You're now ready for production dbt!** 🚀
