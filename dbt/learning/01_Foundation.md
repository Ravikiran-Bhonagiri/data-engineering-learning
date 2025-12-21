# Part 1: From SQL to dbt (Foundation)

**Reading time:** 30 minutes  
**Goal:** Understand what dbt is and why you need it.

---

## The Problem (You Already Know This Pain)

You write SQL. Great SQL. But you probably face these issues:

### Problem 1: Scattered Scripts
```sql
-- analytics/reports/customer_summary.sql (WHERE IS THIS?)
SELECT customer_id, SUM(amount) 
FROM prod.orders 
GROUP BY 1;
```

Your SQL lives in:
- Random folders on your laptop
- Jupyter notebooks
- BI tool custom SQL tabs
- Email threads (!?)
- That Slack message from 3 months ago

### Problem 2: Manual Dependencies
```sql
-- Run these IN ORDER or everything breaks:
-- 1. clean_customers.sql (run first!)
-- 2. aggregate_orders.sql (depends on #1)
-- 3. customer_summary.sql (depends on #1 and #2)
```

You maintain a mental (or Excel) dependency graph.

### Problem 3: Hard-Coded Hell
```sql
SELECT * FROM analytics.dim_customers  -- hope this exists!
JOIN analytics.fct_orders              -- hope this is updated!
```

Change a table name? Good luck finding all the places it's used.

### Problem 4: No Testing
```sql
-- Is customer_id unique? 🤷
-- Are there NULLs in email? 🤷
-- Is order_date ever in the future? 🤷
```

You check manually... sometimes... if you remember.

### Problem 5: Zero Documentation
Six months later: "What does this query do again?"

---

## The Solution: dbt

**dbt = Your SQL + Smart Tooling**

Same SQL you write today, but with:
- ✅ Version control (Git)
- ✅ Automatic dependencies
- ✅ Built-in testing
- ✅ Auto-generated documentation
- ✅ Runs inside your warehouse

---

## Before & After Comparison

### BEFORE: Manual SQL Script

```sql
-- analytics/manual_customer_dim.sql
-- TODO: Run this after clean_customers.sql
-- TODO: Remember to update if schema changes
-- TODO: Add email validation somehow?

CREATE TABLE analytics.dim_customers AS
SELECT 
    id AS customer_id,
    UPPER(first_name || ' ' || last_name) AS full_name,
    email,
    created_at::date AS signup_date
FROM raw.customers
WHERE status = 'active';
```

**Issues:**
- No dependency tracking
- Hard-coded table names
- No tests
- No documentation
- Run manually or via cron

### AFTER: dbt Model

**File:** `models/marts/dim_customers.sql`
```sql
{{ config(materialized='table') }}

WITH source_customers AS (
    SELECT * FROM {{ source('raw', 'customers') }}
),

active_customers AS (
    SELECT 
        id AS customer_id,
        UPPER(first_name || ' ' || last_name) AS full_name,
        email,
        created_at::date AS signup_date
    FROM source_customers
    WHERE status = 'active'
)

SELECT * FROM active_customers
```

**File:** `models/marts/schema.yml`
```yaml
models:
  - name: dim_customers
    description: "Active customer dimension"
    columns:
      - name: customer_id
        tests:
          - unique
          - not_null
      - name: email
        tests:
          - not_null
```

**Benefits:**
- ✅ `source('raw', 'customers')` - dbt tracks this
- ✅ Automatic dependency DAG
- ✅ Built-in tests (unique, not_null)
- ✅ Documentation from YAML
- ✅ Run with `dbt run`

---

## Key Concept: Models

**SQL Script:**
```sql
-- You run this manually
CREATE TABLE my_table AS
SELECT * FROM source;
```

**dbt Model:**
```sql
-- dbt runs this for you
-- Just write the SELECT
SELECT * FROM {{ source('raw', 'source') }}
```

**That's it.** A dbt model is just a SELECT statement in a `.sql` file.

---

## Installation & Setup

### Step 1: Install dbt

```bash
# Choose your warehouse
pip install dbt-postgres    # PostgreSQL
pip install dbt-snowflake   # Snowflake  
pip install dbt-bigquery    # BigQuery
pip install dbt-redshift    # Redshift
```

### Step 2: Configure Connection

Create `~/.dbt/profiles.yml`:

```yaml
my_project:
  target: dev
  outputs:
    dev:
      type: postgres
      host: localhost
      user: your_username
      password: your_password
      port: 5432
      dbname: analytics
      schema: dbt_dev
      threads: 4
```

### Step 3: Initialize Project

```bash
dbt init my_first_project
cd my_first_project
```

This creates:
```
my_first_project/
├── dbt_project.yml      # Project config
├── models/              # Your SQL goes here
├── tests/               # Custom tests
├── macros/              # Reusable functions
└── seeds/               # CSV reference data
```

### Step 4: Test Connection

```bash
dbt debug
```

You should see: `Connection test: [OK connection ok]`

---

## Your First dbt Model

### Create the Model

**File:** `models/my_first_model.sql`
```sql
-- This is just a SELECT statement
-- dbt handles the CREATE TABLE part

SELECT
    1 AS id,
    'Hello dbt!' AS message,
    CURRENT_TIMESTAMP AS created_at
```

### Run It

```bash
dbt run
```

**Output:**
```
Running with dbt=1.7.0
Found 1 model
  
1 of 1 START sql view model dbt_dev.my_first_model ..... [RUN]
1 of 1 OK created sql view model dbt_dev.my_first_model  [SUCCESS in 0.12s]

Finished running 1 view model in 0.15s.
```

### Query the Result

```sql
SELECT * FROM dbt_dev.my_first_model;
```

```
id | message      | created_at
---+--------------+----------------------------
 1 | Hello dbt!   | 2024-03-20 14:23:45.123456
```

**Congratulations!** You just created your first dbt model.

---

## SQL → dbt Translation Guide

| SQL Pattern | dbt Pattern |
|-------------|-------------|
| `CREATE TABLE x AS SELECT...` | `{{ config(materialized='table') }}` + `SELECT...` |
| `CREATE VIEW x AS SELECT...` | `SELECT...` (default is view) |
| `FROM analytics.customers` | `FROM {{ ref('customers') }}` |
| `FROM raw.orders` | `FROM {{ source('raw', 'orders') }}` |
| Manually track dependencies | Auto-tracked via `ref()` |
| Cron job | `dbt run` |
| Manual testing | `dbt test` |

---

## dbt Commands (The Basics)

```bash
dbt run          # Build all models
dbt test         # Run all tests
dbt docs generate # Create documentation
dbt docs serve    # View docs at localhost:8080
```

That's 90% of what you'll use daily.

---

## The "Aha!" Moment

**Old way:**
1. Write SQL script
2. Manually run it
3. Hope dependencies are current
4. Manually check for bugs
5. Update some wiki somewhere
6. Repeat tomorrow

**dbt way:**
1. Write SELECT statement
2. Run `dbt run`
3. Dependencies handled automatically
4. Tests run automatically
5. Docs generated automatically
6. Done.

---

## What You've Learned

✅ dbt solves SQL workflow problems you already have  
✅ dbt models are just SELECT statements  
✅ `ref()` and `source()` replace hard-coded table names  
✅ Dependencies are automatic  
✅ Testing and docs are built-in  

---

**Next Step:** Open `02_Seven_Day_Course.md` for hands-on practice →
