# Complete Troubleshooting Guide

**Problem Solved:** You're stuck and need quick answers to common dbt errors.

This guide covers error messages, edge cases, and debugging strategies.

---

## Common Error Messages & Fixes

### 1. "Compilation Error: depends on a node named..."

**Full Error:**
```
Compilation Error in model stg_customers
  depends on a node named 'source.my_project.raw.customers' 
  which was not found
```

**Cause:** Source not defined in YAML

**Fix:**
```yaml
# models/staging/schema.yml
version: 2

sources:
  - name: raw
    tables:
      - name: customers  # ← Must match source('raw', 'customers')
```

---

### 2. "Database Error: relation does not exist"

**Full Error:**
```
Database Error in model dim_customers
  relation "dbt_dev.stg_customers" does not exist
```

**Causes & Fixes:**

**Cause 1:** Model not built yet
```bash
# Fix: Run dependencies first
dbt run --select +dim_customers  # + includes upstream
```

**Cause 2:** Wrong schema
```sql
-- Check your profiles.yml schema matches
SELECT * FROM dbt_dev.stg_customers;  -- vs dbt_prod.stg_customers
```

**Cause 3:** Typo in ref()
```sql
SELECT * FROM {{ ref('stg_customer') }}  -- ❌ Missing 's'
SELECT * FROM {{ ref('stg_customers') }}  -- ✅
```

---

### 3. "Circular dependency detected"

**Full Error:**
```
Compilation Error
  dbt found a cycle in your DAG
  model_a → model_b → model_a
```

**Visual:**
```
model_a.sql: SELECT * FROM {{ ref('model_b') }}
model_b.sql: SELECT * FROM {{ ref('model_a') }}  ← Circular!
```

**Fix:** Break the cycle
```sql
-- Create intermediate model
-- int_base_data.sql
SELECT * FROM {{ source('raw', 'data') }}

-- model_a.sql
SELECT * FROM {{ ref('int_base_data') }}

-- model_b.sql
SELECT * FROM {{ ref('int_base_data') }}
```

---

### 4. "Incremental model not updating"

**Problem:** New data exists but model doesn't have it

**Causes:**

**Cause 1:** Incremental logic wrong
```sql
-- ❌ Bad: Will miss data
{% if is_incremental() %}
WHERE created_at > (SELECT MAX(created_at) FROM {{ this }})
{% endif %}

-- ✅ Good: Use updated_at or lookback window
{% if is_incremental() %}
WHERE updated_at > (SELECT MAX(updated_at) - INTERVAL '1 day' FROM {{ this }})
{% endif %}
```

**Cause 2:** Need full refresh
```bash
dbt run --select my_model --full-refresh
```

---

### 5. "Permission denied for schema"

**Full Error:**
```
Database Error
  permission denied for schema dbt_prod
```

**Fix:** Check warehouse role permissions
```sql
-- Snowflake
GRANT USAGE ON SCHEMA dbt_prod TO ROLE transformer;
GRANT CREATE TABLE ON SCHEMA dbt_prod TO ROLE transformer;

-- BigQuery: Update IAM permissions in GCP Console

-- Redshift
GRANT USAGE ON SCHEMA dbt_prod TO analyst;
```

---

### 6. "Connection refused" or "Connection timeout"

**Causes & Fixes:**

**Check 1: Network issues**
```bash
# Test connection
ping your-warehouse-host.com
telnet your-warehouse.com 5432
```

**Check 2: Firewall blocking**
- Add dbt Cloud IPs to warehouse whitelist
- Check VPN connection

**Check 3: Wrong credentials**
```bash
dbt debug  # Will show which part of connection fails
```

---

### 7. "Jinja compilation error: unexpected token"

**Full Error:**
```
Jinja Compilation Error
  unexpected '}' at line 5
```

**Common Causes:**

**Unclosed bracket:**
```sql
-- ❌ Bad
SELECT {{ ref('model') }  -- Missing }

-- ✅ Good
SELECT {{ ref('model') }}
```

**Wrong quote type:**
```sql
-- ❌ Bad
SELECT * FROM {{ ref("model') }}  -- Mixed quotes

-- ✅ Good
SELECT * FROM {{ ref('model') }}
```

---

### 8. "Could not find profile named..."

**Full Error:**
```
Could not find profile named 'my_project'
```

**Fix:** Check `profiles.yml` matches `dbt_project.yml`

**dbt_project.yml:**
```yaml
profile: 'my_project'  # Must match profiles.yml
```

**~/.dbt/profiles.yml:**
```yaml
my_project:  # ← Must match exactly
  target: dev
```

---

## Edge Cases & Advanced Issues

### Late-Arriving Data in Incrementals

**Problem:** Yesterday's data arrives today

**Solution: Lookback window**
```sql
{{ config(materialized='incremental') }}

SELECT * FROM {{ source('raw', 'events') }}
{% if is_incremental() %}
  -- Look back 3 days to catch late arrivals
  WHERE event_date > (
    SELECT DATE_TRUNC('day', MAX(event_date)) - INTERVAL '3 days' 
    FROM {{ this }}
  )
{% endif %}
```

---

### Handling Timezone Differences

**Problem:** Source in EST, warehouse in UTC

**Solution:**
```sql
SELECT
    id,
    created_at AT TIME ZONE 'EST' AS created_at_est,
    created_at AT TIME ZONE 'UTC' AS created_at_utc
FROM {{ source('raw', 'events') }}
```

---

### Memory Issues (Out of Memory)

**Symptoms:**
- Query killed mid-execution
- Slow warming

**Fixes:**

**1. Break into smaller models**
```sql
-- Instead of one giant model with 10 CTEs
-- Create intermediate models
```

**2. Use incremental materialization**
```sql
{{ config(materialized='incremental') }}
```

**3. Increase warehouse size**
```yaml
# profiles.yml (Snowflake)
warehouse: XLARGE_WH  # Instead of SMALL_WH
```

---

### Snapshot Not Creating dbt_valid_to

**Problem:** `dbt_valid_to` is always NULL

**Cause:** No changes detected

**Debug:**
```sql
-- Check if data actually changed
SELECT *, updated_at
FROM raw.customers
WHERE id = 123
ORDER BY updated_at DESC;
```

**Ensure `updated_at` field updates:**
```yaml
{% snapshot customers_snapshot %}
{{
    config(
      unique_key='id',
      strategy='timestamp',
      updated_at='updated_at'  # ← This field must change!
    )
}}
{% endsnapshot %}
```

---

### Test Failures You Don't Understand

**Strategy: Debug the test**

```bash
# 1. Compile the test to see SQL
dbt compile --select test:unique_customer_id

# 2. Check compiled SQL
cat target/compiled/.../tests/unique_customer_id.sql

# 3. Run in warehouse to see failing rows
-- Copy SQL from step 2
-- Run in Snowflake/BigQuery UI
```

---

## Debugging Strategies

### 1. Use `dbt debug`

```bash
dbt debug
```

Checks:
- ✅ profiles.yml exists
- ✅ Connection to warehouse
- ✅ Required permissions
- ✅ dbt version

### 2. Compile First, Run Later

```bash
# See what SQL dbt will run
dbt compile --select my_model

# Check target/compiled/my_project/models/my_model.sql
```

### 3. Use `--print` Flag

```bash
dbt run --select my_model --print
```

Prints compiled SQL to console before running.

### 4. Check Logs

```bash
# Logs are in logs/dbt.log
cat logs/dbt.log | grep ERROR
```

### 5. Use `limit 0` for Syntax Checks

```sql
{{ config(materialized='view') }}

{% if var('check_syntax', false) %}
SELECT * FROM (
{% endif %}

-- Your actual query
SELECT * FROM {{ ref('base_table') }}

{% if var('check_syntax', false) %}
) LIMIT 0
{% endif %}
```

Run:
```bash
dbt run --vars '{"check_syntax": true}'  # Fast syntax check
```

---

## Performance Troubleshooting

### Slow Model Diagnosis

**Step 1: Time it**
```bash
dbt run --select my_slow_model --debug 2>&1 | grep "Timing"
```

**Step 2: Check row count**
```sql
dbt show --select my_slow_model --limit 1  # May include row count
```

**Step 3: EXPLAIN the query**
```sql
-- Copy compiled SQL from target/compiled/
EXPLAIN SELECT ... -- Run in warehouse
```

**Step 4: Check CTEs**
- Are you nesting 10+ CTEs?
- Break into intermediate models

**Step 5: Warehouse-specific**
- **Snowflake:** Check clustering
- **BigQuery:** Check partitioning
- **Redshift:** Check distribution keys

---

## Package Issues

### Package Not Found

**Error:**
```
Package 'dbt-labs/dbt_utils' was not found in the package registry
```

**Fix:**
```yaml
# packages.yml
packages:
  - package: dbt-labs/dbt_utils
    version: 1.1.1  # Specify exact version
```

```bash
dbt deps  # Install packages
```

### Package Version Conflicts

**Error:**
```
Package version conflict
```

**Fix:** Pin all package versions explicitly
```yaml
packages:
  - package: dbt-labs/dbt_utils
    version: 1.1.1  # Not latest, specific version
  - package: dbt-labs/codegen
    version: 0.12.1
```

---

## Git Issues in dbt Cloud

### "Your branch is behind"

**Fix in IDE:**
1. Commit your changes
2. Click "Pull from main"
3. Resolve conflicts if any
4. Push

### "Detached HEAD state"

**Fix:**
```bash
# In dbt Cloud terminal
git checkout main
git pull
```

---

## When All Else Fails

### 1. Check dbt Community

- [dbt Discourse](https://discourse.getdbt.com/)
- [dbt Slack](https://www.getdbt.com/community/)

### 2. Search Error Message

```
site:discourse.getdbt.com "your error message"
```

### 3. Enable Debug Logs

```bash
dbt run --debug --log-level debug
```

### 4. Check dbt Docs

- [docs.getdbt.com](https://docs.getdbt.com/)
- Usually has exact error message solutions

### 5. Minimal Reproducible Example

Strip down to:
```sql
-- Simplest possible version that reproduces error
SELECT 1 AS id
```

Add complexity until error appears.

---

## Quick Checklist When Stuck

- [ ] Run `dbt debug` - connection OK?
- [ ] Run `dbt deps` - packages installed?
- [ ] Check `profiles.yml` - correct schema?
- [ ] Check `schema.yml` - sources defined?
- [ ] Compile model - SQL syntax valid?
- [ ] Check logs - specific error message?
- [ ] Google error - known issue?
- [ ] Check dbt Slack - others had this?

---

**99% of issues are covered above!** 💪
