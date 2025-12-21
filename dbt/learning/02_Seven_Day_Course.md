# Part 2: Seven-Day dbt Course

**Time:** 7 days, 1-2 hours per day  
**Prerequisites:** Completed Part 1

This hands-on course is extracted from the official dbt learning plan PDFs. Work through one day at a time.

---

## Day 0: The "Why" (Understanding the Problem)

### Before dbt: Pain Points

You're a SQL expert, but your workflow probably looks like this:

**Scenario:** Building a customer dimension table

```sql
-- Step 1: Run clean_customers.sql first (manually)
CREATE TABLE analytics.clean_customers AS
SELECT 
    id,
    LOWER(email) AS email,
    first_name,
    last_name
FROM raw.customers
WHERE email IS NOT NULL;

-- Step 2: Run customer_orders.sql second (manually, after Step 1)
CREATE TABLE analytics.customer_orders AS
SELECT 
    customer_id,
    COUNT(*) AS total_orders,
    SUM(amount) AS lifetime_value
FROM raw.orders
GROUP BY 1;

-- Step 3: Run dim_customers.sql last (manually, after Steps 1 & 2)
CREATE TABLE analytics.dim_customers AS
SELECT
    c.id AS customer_id,
    c.first_name || ' ' || c.last_name AS full_name,
    c.email,
    COALESCE(o.total_orders, 0) AS total_orders,
    COALESCE(o.lifetime_value, 0) AS lifetime_value
FROM analytics.clean_customers c
LEFT JOIN analytics.customer_orders o ON c.id = o.customer_id;
```

**Problems:**
- ❌ Run in order or everything breaks
- ❌ Hard-coded table names everywhere
- ❌ No tests (is customer_id unique? who knows!)
- ❌ No documentation
- ❌ Change `clean_customers`? Good luck finding all dependencies

### With dbt: Automatic Everything

Same logic, dbt style:

**File:** `models/staging/stg_customers.sql`
```sql
SELECT 
    id AS customer_id,
    LOWER(email) AS email,
    first_name,
    last_name
FROM {{ source('raw', 'customers') }}
WHERE email IS NOT NULL
```

**File:** `models/staging/stg_orders.sql`
```sql
SELECT 
    customer_id,
    COUNT(*) AS total_orders,
    SUM(amount) AS lifetime_value
FROM {{ source('raw', 'orders') }}
GROUP BY 1
```

**File:** `models/marts/dim_customers.sql`
```sql
SELECT
    c.customer_id,
    c.first_name || ' ' || c.last_name AS full_name,
    c.email,
    COALESCE(o.total_orders, 0) AS total_orders,
    COALESCE(o.lifetime_value, 0) AS lifetime_value
FROM {{ ref('stg_customers') }} c
LEFT JOIN {{ ref('stg_orders') }} o ON c.customer_id = o.customer_id
```

**File:** `models/schema.yml`
```yaml
models:
  - name: dim_customers
    columns:
      - name: customer_id
        tests:
          - unique
          - not_null
```

**Run:**
```bash
dbt run   # Runs in correct order automatically!
dbt test  # Tests customer_id is unique and not null
```

**Benefits:**
- ✅ `ref()` tracks dependencies - runs in correct order
- ✅ Tests built-in
- ✅ Documentation from YAML
- ✅ Change `stg_customers`? dbt knows what depends on it

---

## Day 1: Setup & First Project

### Install dbt

```bash
pip install dbt-postgres  # or dbt-snowflake, dbt-bigquery, etc.
dbt --version
```

### Configure Connection

Create `~/.dbt/profiles.yml`:

```yaml
ecommerce_project:
  target: dev
  outputs:
    dev:
      type: postgres
      host: localhost
      port: 5432
      user: your_username
      password: your_password
      dbname: ecommerce
      schema: dbt_dev
      threads: 4
```

### Initialize Project

```bash
dbt init ecommerce_project
cd ecommerce_project
```

### Test Connection

```bash
dbt debug
```

Look for: `Connection test: [OK connection ok]`

### Create First Model

**File:** `models/my_first_dbt_model.sql`
```sql
SELECT 1 AS id, 'hello dbt' AS message
```

### Run It

```bash
dbt run
```

### View Docs

```bash
dbt docs generate
dbt docs serve  # Opens localhost:8080
```

Click the graph icon to see your DAG (even for one model!).

**✅ Day 1 Complete:** You have a working dbt project.

---

## Day 2: Models, ref(), and Dependencies

### The `ref()` Function

**Bad (hard-coded):**
```sql
SELECT * FROM analytics.stg_customers  -- What if this changes?
```

**Good (dbt managed):**
```sql
SELECT * FROM {{ ref('stg_customers') }}  -- dbt tracks this!
```

### Create Staging Models

**File:** `models/staging/stg_customers.sql`
```sql
WITH source AS (
    SELECT * FROM {{ source('raw', 'customers') }}
),

cleaning AS (
    SELECT
        id AS customer_id,
        first_name,
        last_name,
        LOWER(email) AS email,
        city,
        state,
        created_at
    FROM source
    WHERE email IS NOT NULL
)

SELECT * FROM cleaning
```

**File:** `models/staging/stg_orders.sql`
```sql
SELECT
    id AS order_id,
    customer_id,
    order_date,
    status,
    amount
FROM {{ source('raw', 'orders') }}
WHERE status != 'cancelled'
```

### Create Mart Model (Uses ref())

**File:** `models/marts/dim_customers.sql`
```sql
WITH customers AS (
    SELECT * FROM {{ ref('stg_customers') }}
),

orders AS (
    SELECT
        customer_id,
        COUNT(*) AS total_orders,
        SUM(amount) AS lifetime_value
    FROM {{ ref('stg_orders') }}
    GROUP BY 1
),

final AS (
    SELECT
        c.customer_id,
        c.first_name || ' ' || c.last_name AS full_name,
        c.email,
        c.city,
        c.state,
        COALESCE(o.total_orders, 0) AS total_orders,
        COALESCE(o.lifetime_value, 0) AS lifetime_value,
        c.created_at
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
)

SELECT * FROM final
```

### Run and Check DAG

```bash
dbt run
dbt docs generate && dbt docs serve
```

In the docs, click the DAG icon. You'll see:
```
raw.customers ──► stg_customers ──┐
                                  ├──► dim_customers
raw.orders ────► stg_orders ──────┘
```

dbt figured out the build order automatically!

**✅ Day 2 Complete:** You understand dependencies and `ref()`.

---

## Day 3: Sources & Seeds

### Define Sources (YAML)

**File:** `models/staging/schema.yml`
```yaml
version: 2

sources:
  - name: raw
    database: ecommerce
    schema: raw
    tables:
      - name: customers
        description: "Raw customer data from production"
        columns:
          - name: id
            tests:
              - unique
              - not_null
      
      - name: orders
        description: "Raw order transactions"
        loaded_at_field: created_at
        freshness:
          warn_after: {count: 12, period: hour}
```

### Use Sources in Models

```sql
-- Instead of: FROM raw.customers
SELECT * FROM {{ source('raw', 'customers') }}
```

### Check Data Freshness

```bash
dbt source freshness
```

### Create a Seed (CSV Reference Data)

**File:** `seeds/product_categories.csv`
```csv
category_id,category_name,department
1,Electronics,Technology
2,Furniture,Office
3,Books,Media
```

### Load Seed

```bash
dbt seed
```

### Use Seed in Model

```sql
SELECT
    p.name AS product_name,
    pc.category_name,
    pc.department
FROM {{ ref('products') }} p
JOIN {{ ref('product_categories') }} pc 
  ON p.category_id = pc.category_id
```

**✅ Day 3 Complete:** You know sources and seeds.

---

## Day 4: Testing

### Schema Tests (YAML)

**File:** `models/marts/schema.yml`
```yaml
models:
  - name: dim_customers
    description: "Customer dimension table"
    columns:
      - name: customer_id
        tests:
          - unique
          - not_null
      
      - name: email
        tests:
          - not_null
      
      - name: state
        tests:
          - accepted_values:
              values: ['NY', 'CA', 'TX', 'IL']
```

### Custom Data Test

**File:** `tests/no_negative_amounts.sql`
```sql
-- This should return 0 rows
-- If it returns rows, the test fails
SELECT *
FROM {{ ref('stg_orders') }}
WHERE amount < 0
```

### Run Tests

```bash
dbt test                       # All tests
dbt test --select dim_customers  # Specific model
```

**✅ Day 4 Complete:** You can test your data quality.

---

## Day 5: Documentation & DAG

### Add Descriptions

**File:** `models/marts/schema.yml`
```yaml
models:
  - name: dim_customers
    description: |
      Customer dimension table with lifetime metrics.
      Updated daily. Source: raw.customers + raw.orders.
    
    columns:
      - name: customer_id
        description: "Unique identifier for each customer"
      
      - name: lifetime_value
        description: "Total revenue from this customer (all time)"
```

### Generate & View Docs

```bash
dbt docs generate
dbt docs serve
```

Navigate to `localhost:8080`:
- Browse models
- See column descriptions
- View DAG (lineage graph)
- Search everything

**✅ Day 5 Complete:** Your project is documented.

---

## Day 6: Snapshots (SCD Type 2)

Track historical changes to slowly changing dimensions.

**File:** `snapshots/customers_snapshot.sql`
```sql
{% snapshot customers_snapshot %}

{{
    config(
      target_schema='snapshots',
      unique_key='id',
      strategy='timestamp',
      updated_at='updated_at'
    )
}}

SELECT * FROM {{ source('raw', 'customers') }}

{% endsnapshot %}
```

### Run Snapshot

```bash
dbt snapshot
```

This creates a table with:
- `dbt_valid_from` - When record became active
- `dbt_valid_to` - When record was superseded (NULL = current)
- `dbt_scd_id` - Unique snapshot ID
- All original columns

**✅ Day 6 Complete:** You can track historical changes.

---

## Day 7: Macros, Incremental, CI/CD

### Create a Macro

**File:** `macros/cents_to_dollars.sql`
```sql
{% macro cents_to_dollars(column_name) %}
    ({{ column_name }} / 100.0)::decimal(10,2)
{% endmacro %}
```

**Use in model:**
```sql
SELECT
    order_id,
    {{ cents_to_dollars('amount_cents') }} AS amount_dollars
FROM {{ ref('orders') }}
```

### Incremental Model

**File:** `models/marts/fct_orders_incremental.sql`
```sql
{{
    config(
        materialized='incremental',
        unique_key='order_id'
    )
}}

SELECT
    order_id,
    customer_id,
    order_date,
    amount
FROM {{ source('raw', 'orders') }}

{% if is_incremental() %}
    WHERE order_date > (SELECT MAX(order_date) FROM {{ this }})
{% endif %}
```

First run: Loads all data  
Subsequent runs: Only new rows (faster!)

### CI/CD with GitHub Actions

**File:** `.github/workflows/dbt_ci.yml`
```yaml
name: dbt CI
on: [pull_request]

jobs:
  dbt_run:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - run: pip install dbt-postgres
      - run: dbt deps
      - run: dbt build  # Run models + tests
```

**✅ Day 7 Complete:** You know advanced dbt features.

---

## 🎓 Course Summary

You've learned:

| Day | Topic | Key Takeaway |
|-----|-------|--------------|
| 0 | Why dbt? | Solves SQL workflow problems |
| 1 | Setup | Install, configure, first model |
| 2 | Models & ref() | Automatic dependencies |
| 3 | Sources & Seeds | Reference raw data and CSVs |
| 4 | Testing | Schema + custom data tests |
| 5 | Docs | Auto-generated documentation |
| 6 | Snapshots | Historical change tracking |
| 7 | Advanced | Macros, incremental, CI/CD |

**Next:** Use `03_Quick_Reference.md` for daily lookups →
