# Warehouse-Specific dbt Guide

**Problem Solved:** Different warehouses have different SQL syntax and features.

This guide shows you how to adapt generic dbt code for Snowflake, BigQuery, and Redshift.

---

## Quick Comparison Table

| Feature | Postgres | Snowflake | BigQuery | Redshift |
|---------|----------|-----------|----------|----------|
| **Date Trunc** | `DATE_TRUNC('month', date)` | `DATE_TRUNC('month', date)` | `DATE_TRUNC(date, MONTH)` | `DATE_TRUNC('month', date)` |
| **String Concat** | `||` or `CONCAT()` | `||` or `CONCAT()` | `||` or `CONCAT()` | `||` or `CONCAT()` |
| **Current Date** | `CURRENT_DATE` | `CURRENT_DATE` | `CURRENT_DATE()` | `CURRENT_DATE` |
| **Window Anti-Pattern** | Subquery | `QUALIFY` | No `QUALIFY` | No `QUALIFY` |
| **JSON** | `jsonb` | `VARIANT` | `JSON` | `SUPER` |
| **Array** | `ARRAY[]` | `ARRAY_CONSTRUCT()` | `[]` | No native arrays |

---

## 1. Snowflake-Specific Features

### Installation

```bash
pip install dbt-snowflake
```

### profiles.yml

```yaml
my_project:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: abc12345.us-east-1  # Your account locator
      user: your_username
      password: your_password
      role: TRANSFORMER
      database: ANALYTICS
      warehouse: TRANSFORMING
      schema: dbt_dev
      threads: 4
```

### Snowflake-Specific SQL

**QUALIFY Clause (Window Function Filter):**
```sql
-- Generic dbt (subquery)
WITH ranked AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC) AS rn
    FROM {{ ref('orders') }}
)
SELECT *  FROM ranked WHERE rn = 1

-- Snowflake (QUALIFY)
SELECT *
FROM {{ ref('orders') }}
QUALIFY ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC) = 1
```

**Variant/JSON Handling:**
```sql
-- Parse JSON in Snowflake
SELECT
    user_id,
    metadata:email::STRING AS email,
    metadata:preferences.language::STRING AS language
FROM {{ ref('user_events') }}
```

**Snowflake-Specific Config:**
```sql
{{ config(
    materialized='incremental',
    unique_key='id',
    cluster_by=['order_date'],  -- Snowflake clustering
    snowflake_warehouse='LARGE_WH'  -- Override warehouse
) }}
```

---

## 2. BigQuery-Specific Features

### Installation

```bash
pip install dbt-bigquery
```

### profiles.yml

```yaml
my_project:
  target: dev
  outputs:
    dev:
      type: bigquery
      method: service-account
      project: your-gcp-project
      dataset: dbt_dev
      threads: 4
      keyfile: /path/to/service-account.json
      location: US
```

### BigQuery-Specific SQL

**Date Functions:**
```sql
-- Generic
DATE_TRUNC('month', order_date)

-- BigQuery
DATE_TRUNC(order_date, MONTH)
```

**Partitioning:**
```sql
{{ config(
    materialized='table',
    partition_by={
      "field": "order_date",
      "data_type": "date",
      "granularity": "day"
    },
    cluster_by=['customer_id', 'status']
) }}

SELECT * FROM {{ ref('orders') }}
```

**Nested/Repeated Fields:**
```sql
-- Unnest arrays in BigQuery
SELECT
    order_id,
    item.product_id,
    item.quantity
FROM {{ ref('orders') }},
UNNEST(items) AS item
```

**Wildcard Tables:**
```sql
-- Query multiple sharded tables
SELECT *
FROM `project.dataset.table_*`
WHERE _TABLE_SUFFIX BETWEEN '20240101' AND '20240131'
```

**Legacy SQL vs Standard SQL:**
```sql
-- BigQuery uses Standard SQL by default in dbt
-- But if you need legacy:
{{ config(use_legacy_sql=true) }}
```

---

## 3. Redshift-Specific Features

### Installation

```bash
pip install dbt-redshift
```

### profiles.yml

```yaml
my_project:
  target: dev
  outputs:
    dev:
      type: redshift
      host: your-cluster.region.redshift.amazonaws.com
      port: 5439
      user: your_username
      password: your_password
      dbname: analytics
      schema: dbt_dev
      threads: 4
```

### Redshift-Specific SQL

**Distribution Keys:**
```sql
{{ config(
    materialized='table',
    dist='customer_id',  -- Distribution key
    sort=['order_date', 'customer_id']  -- Sort keys
) }}

SELECT * FROM {{ ref('orders') }}
```

**Date Diff:**
```sql
-- Redshift DATEDIFF
SELECT
    DATEDIFF(day, first_order, last_order) AS days_between
FROM {{ ref('customer_summary') }}
```

**INSERT Performance:**
```sql
-- Use APPEND for better performance on incremental models
{{ config(
    materialized='incremental',
    unique_key='id',
    incremental_strategy='append'
) }}
```

**SUPER Data Type (JSON):**
```sql
-- Redshift SUPER type
SELECT
    user_id,
    metadata.email::VARCHAR AS email
FROM {{ ref('user_events') }}
WHERE JSON_TYPEOF(metadata.email) = 'string'
```

---

## 4. Cross-Warehouse Macros

Write warehouse-agnostic code using `target.type`:

```sql
-- macros/date_trunc_month.sql
{% macro date_trunc_month(column_name) %}
    {% if target.type == 'bigquery' %}
        DATE_TRUNC({{ column_name }}, MONTH)
    {% else %}
        DATE_TRUNC('month', {{ column_name }})
    {% endif %}
{% endmacro %}
```

**Usage:**
```sql
SELECT
    {{ date_trunc_month('order_date') }} AS order_month,
    COUNT(*) AS orders
FROM {{ ref('orders') }}
GROUP BY 1
```

---

## 5. Incremental Strategies by Warehouse

| Strategy | Postgres | Snowflake | BigQuery | Redshift |
|----------|----------|-----------|----------|----------|
| **append** | ✅ | ✅ | ✅ | ✅ |
| **delete+insert** | ✅ | ✅ | ✅ | ✅ |
| **merge** | ❌ | ✅ | ✅ | ❌ |

**Example for Snowflake (merge):**
```sql
{{ config(
    materialized='incremental',
    unique_key='order_id',
    incremental_strategy='merge',
    merge_update_columns=['status', 'updated_at']
) }}

SELECT * FROM {{ source('raw', 'orders') }}
{% if is_incremental() %}
WHERE updated_at > (SELECT MAX(updated_at) FROM {{ this }})
{% endif %}
```

---

## 6. Adapter-Specific dbt Packages

### dbt_utils (Cross-warehouse)
```yaml
# packages.yml
packages:
  - package: dbt-labs/dbt_utils
    version: 1.1.1
```

Handles cross-warehouse differences automatically:
```sql
-- Works on all warehouses
{{ dbt_utils.date_trunc('month', 'order_date') }}
{{ dbt_utils.generate_surrogate_key(['customer_id', 'order_id']) }}
```

### Snowflake Utils
```yaml
packages:
  - package: dbt-labs/snowflake_utils
    version: 0.3.0
```

### BigQuery Specific
```yaml
packages:
  - package: dbt-labs/metrics
    version: 1.6.0  # Works best with BigQuery
```

---

## 7. Common Migration Patterns

### From Postgres to Snowflake

```sql
-- Postgres
SELECT id::TEXT AS id_string

-- Snowflake
SELECT id::VARCHAR AS id_string
-- OR
SELECT TO_VARCHAR(id) AS id_string
```

### From Redshift to BigQuery

```sql
-- Redshift DATEDIFF
DATEDIFF(day, start_date, end_date)

-- BigQuery DATE_DIFF
DATE_DIFF(end_date, start_date, DAY)
```

---

## 8. Performance Optimization by Warehouse

### Snowflake
- Use clustering on high-cardinality columns
- Leverage result caching (automatic)
- Use `TRANSIENT` tables for temp data

```sql
{{ config(
    transient=true,
    cluster_by=['customer_id']
) }}
```

### BigQuery
- Partition by date for large tables
- Cluster after partitioning
- Use `_PARTITIONTIME` for partition pruning

```sql
WHERE _PARTITIONTIME >= TIMESTAMP('2024-01-01')
```

### Redshift
- Choose proper distribution keys (avoid skew)
- Sort keys for frequently filtered columns
- Vacuum and analyze regularly

---

## 9. Testing Across Warehouses

Use dbt's `target.type` in tests:

```sql
-- tests/cross_warehouse_test.sql
{% if target.type == 'bigquery' %}
    -- BigQuery-specific test
    SELECT * FROM {{ ref('orders') }}
    WHERE DATE_TRUNC(order_date, DAY) > CURRENT_DATE()
{% else %}
    -- Generic test
    SELECT * FROM {{ ref('orders') }}
    WHERE order_date > CURRENT_DATE
{% endif %}
```

---

## Quick Reference

**When migrating dbt projects:**
1. Update `profiles.yml` with new warehouse
2. Search for warehouse-specific syntax (QUALIFY, UNNEST, etc.)
3. Update materialization configs (dist, cluster, partition)
4. Test incremental strategy compatibility
5. Update date/time functions
6. Check JSON/array handling

**Use dbt_utils for most cross-warehouse compatibility!**

---

**Now you can use dbt on any warehouse!** 🚀
