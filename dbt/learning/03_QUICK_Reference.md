# Part 3: Quick Reference

**Use this for:** Daily lookups, interview prep, troubleshooting.

---

## Essential dbt Commands

```bash
#Core Commands
dbt run                # Build all models
dbt test               # Run all tests
dbt build              # Run models + tests (recommended)
dbt debug              # Test connection

# Documentation
dbt docs generate      # Create docs
dbt docs serve         # View docs at localhost:8080

# Selective Runs
dbt run --select my_model              # Specific model
dbt run --select staging.*             # All in folder
dbt run --select +my_model             # Model + upstream
dbt run --select my_model+             # Model + downstream
dbt run --select +my_model+            # Full lineage
dbt run --exclude staging.*            # Exclude folder

# Other
dbt seed               # Load CSVs from seeds/
dbt snapshot           # Run snapshots (SCD Type 2)
dbt compile            # See compiled SQL (in target/)
dbt clean              # Delete target/ folder
dbt deps               # Install packages
```

---

## SQL → dbt Pattern Library

### Pattern 1: CREATE TABLE AS

**SQL:**
```sql
CREATE TABLE analytics.customer_summary AS
SELECT customer_id, COUNT(*) AS orders
FROM orders
GROUP BY 1;
```

**dbt:**
```sql
-- models/customer_summary.sql
{{ config(materialized='table') }}

SELECT customer_id, COUNT(*) AS orders
FROM {{ ref('orders') }}
GROUP BY 1
```

### Pattern 2: CREATE VIEW AS

**SQL:**
```sql
CREATE VIEW analytics.active_customers AS
SELECT * FROM customers
WHERE status = 'active';
```

**dbt:**
```sql
-- models/active_customers.sql
-- Default materialization is 'view'

SELECT * FROM {{ source('raw', 'customers') }}
WHERE status = 'active'
```

### Pattern 3: Hard-Coded Dependencies

**SQL:**
```sql
SELECT c.*, o.total
FROM analytics.customers c
JOIN analytics.orders_summary o ON c.id = o.customer_id
```

**dbt:**
```sql
SELECT c.*, o.total
FROM {{ ref('customers') }} c
JOIN {{ ref('orders_summary') }} o ON c.id = o.customer_id
```

### Pattern 4: Manual Testing

**SQL:**
```sql
-- Hope customer_id is unique 🤞
SELECT COUNT(*), COUNT(DISTINCT customer_id)
FROM customers;
```

**dbt:**
```yaml
# models/schema.yml
models:
  - name: customers
    columns:
      - name: customer_id
        tests:
          - unique
          - not_null
```

### Pattern 5: Incremental Load

**SQL:**
```sql
INSERT INTO fact_orders
SELECT * FROM staging_orders
WHERE order_date > (SELECT MAX(order_date) FROM fact_orders);
```

**dbt:**
```sql
-- models/fact_orders.sql
{{ config(materialized='incremental', unique_key='order_id') }}

SELECT * FROM {{ ref('staging_orders') }}
{% if is_incremental() %}
WHERE order_date > (SELECT MAX(order_date) FROM {{ this }})
{% endif %}
```

---

## Common Configurations

### Model Materialization

```sql
{{ config(materialized='table') }}      -- Physical table
{{ config(materialized='view') }}       -- SQL view
{{ config(materialized='incremental') }} -- Append new rows
{{ config(materialized='ephemeral') }}  -- CTE only
```

### In dbt_project.yml

```yaml
models:
  my_project:
    staging:
      +materialized: view    # All staging as views
    marts:
      +materialized: table   # All marts as tables
```

---

## Testing Cheatsheet

### Built-in Tests

```yaml
tests:
  - unique              # Column values are unique
  - not_null            # No NULL values
  - accepted_values:    # Only specific values
      values: ['A', 'B']
  - relationships:      # Foreign key check
      to: ref('other_table')
      field: other_id
```

### Custom Test

```sql
-- tests/no_future_dates.sql
SELECT * FROM {{ ref('orders') }}
WHERE order_date > CURRENT_DATE
```

---

## Troubleshooting Guide

### "Compilation Error: depends on a source named..."

**Problem:** Source not defined in YAML.

**Fix:**
```yaml
# models/schema.yml
sources:
  - name: raw
    tables:
      - name: orders  # Must match source('raw', 'orders')
```

### "Database Error: relation does not exist"

**Problem:** Model not built yet or wrong schema.

**Fix:**
1. Run `dbt run` to build all models
2. Check `profiles.yml` schema config
3. Verify `{{ ref('model_name') }}` spelling

### "Compilation Error: Model 'X' depends on a node named 'Y'"

**Problem:** Circular dependency or typo in `ref()`.

**Fix:** Check DAG with `dbt docs generate`, look for cycles.

### Incremental Model Not Updating

**Fix:**
```bash
dbt run --select my_model --full-refresh
```

---

## Interview Cheatsheet

### Q: What is dbt?

**A:** "dbt is an open-source transformation framework that lets you build data pipelines using SQL. It handles dependency management, testing, and documentation automatically. It's essentially SQL + Git + testing + docs."

### Q: dbt vs. traditional ETL?

**A:** "Traditional ETL extracts and transforms data **outside** the warehouse (e.g., Python scripts). dbt transforms data **inside** the warehouse using SQL. It's the 'T' in ELT (Extract, Load, Transform)."

### Q: What's the difference between ref() and source()?

**A:**
- `source()` - References **raw tables** (defined in YAML)
- `ref()` - References **dbt models** (other .sql files)

### Q: What are the materialization types?

**A:**
1. **view** - SQL view (fast to build, slow to query)
2. **table** - Physical table (slow to build, fast to query)
3. **incremental** - Appends new data only
4. **ephemeral** - CTE only, not materialized

### Q: How does dbt handle dependencies?

**A:** "dbt automatically builds models in the correct order based on `ref()` calls. It creates a DAG (directed acyclic graph) and runs parent models before child models."

### Q: How do you test data quality in dbt?

**A:** "Two ways: (1) Schema tests in YAML (unique, not_null, etc), and (2) Custom SQL tests that return failing rows."

---

## Best Practices

✅ **Naming:** `<type>_<source>_<entity>` (e.g., `stg_stripe_payments`)  
✅ **Staging:** Light transforms only (rename, cast, filter)  
✅ **Marts:** Business logic, joins, aggregations  
✅ **Test PKs:** Every primary key should have unique + not_null  
✅ **Document:** At minimum, one-line description per model  
✅ **Git:** Use feature branches and pull requests  
✅ **CI/CD:** Run `dbt build` on every PR  

---

## Useful Jinja

### Variables

```sql
{{ var('start_date', '2024-01-01') }}  -- Default value
```

Pass at runtime:
```bash
dbt run --vars '{"start_date": "2024-02-01"}'
```

### Conditionals

```sql
{% if target.name == 'prod' %}
    WHERE is_deleted = FALSE
{% endif %}
```

### Loops

```sql
{% for status in ['pending', 'shipped', 'completed'] %}
    SUM(CASE WHEN status = '{{status}}' THEN 1 ELSE 0 END) AS {{status}}_count
    {{ "," if not loop.last }}
{% endfor %}
```

---

## Package: dbt_utils

Install:
```yaml
# packages.yml
packages:
  - package: dbt-labs/dbt_utils
    version: 1.1.1
```

```bash
dbt deps
```

Useful macros:
```sql
{{ dbt_utils.surrogate_key(['customer_id', 'order_id']) }}
{{ dbt_utils.generate_series(1, 10) }}
{{ dbt_utils.date_trunc('month', 'order_date') }}
```

---

## Quick Win: Migrate Existing SQL

1. Copy your SQL query
2. Create `models/my_model.sql`
3. Replace table names with `{{ ref() }}` or `{{ source() }}`
4. Run `dbt run --select my_model`
5. Done!

Example:
```sql
-- Before
SELECT * FROM analytics.customers
JOIN analytics.orders ON customers.id = orders.customer_id

-- After (in dbt)
SELECT * FROM {{ ref('customers') }}
JOIN {{ ref('orders') }} ON customers.id = orders.customer_id
```

---

**You're now a dbt expert!** 🚀
