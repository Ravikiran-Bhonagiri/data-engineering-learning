# Databricks Quick Reference

**The ultimate cheat sheet for daily work and interview whiteboard questions.**

---

## 🏗 Architecture & Compute

| Type | Use Case | Startup | Cost |
|------|----------|---------|------|
| **All-Purpose** | Interactive Dev | 5-10m | $$$ |
| **Job Cluster** | Scheduled Tasks | 5-10m | $$ |
| **SQL Warehouse** | BI / Dashboards | <10s | $$ |
| **Pools** | Keep VMs warm | Instant | $$$$ |

---

## 🔄 Transformations Map

**95% of Databricks work is standard PySpark.**

| Type | Examples | Where to Learn? |
|------|----------|-----------------|
| **Standard** | `filter`, `select`, `join`, `groupBy` | [PySpark Day 3](../pyspark/02_Day_03.md) |
| **SQL** | `SELECT`, `WHERE`, `CTAS` | [PySpark Day 4](../pyspark/02_Day_04.md) |
| **Delta** | `MERGE`, `DELETE`, `UPDATE`, `Reference` | [Databricks Day 2](./02_Day_02.md) |
| **Physical** | `OPTIMIZE`, `ZORDER`, `VACUUM` | [Databricks Day 2](./02_Day_02.md) |
| **Declarative**| `dlt.table`, `dlt.expect` | [Databricks Day 6](./02_Day_06.md) |

---

**Cluster Mode:**
- **Standard:** Python/Scala/R/SQL.
- **Single Node:** Driver only (no workers). Good for small data / single-threaded libs.
- **High Concurrency:** Deprecated (use Shared access mode).

---

## 💾 Delta Lake Commands

### Check History
```sql
DESCRIBE HISTORY my_table;
```

### Time Travel
```sql
-- Select older version
SELECT * FROM my_table VERSION AS OF 3;
SELECT * FROM my_table TIMESTAMP AS OF '2024-01-01';

-- Restore (Rollback)
RESTORE TABLE my_table TO VERSION AS OF 2;
```

### Optimization (Interview Gold!)
```sql
-- Compact small files
OPTIMIZE my_table;

-- Compact + Co-locate data (Skip data scanning)
OPTIMIZE my_table ZORDER BY (user_id, event_time);
```

### Cleanup
```sql
-- Remove old files (Default > 7 days)
VACUUM my_table;

-- Remove files > 1 hour (Dangerous!)
SET spark.databricks.delta.retentionDurationCheck.enabled = false;
VACUUM my_table RETAIN 0 HOURS;
```

---

## 🔐 Unity Catalog (SQL)

### 3-Level Namespace
`catalog.schema.table`

### Permissions
```sql
-- Grant creation
GRANT CREATE TABLE ON SCHEMA main.default TO `data_eng_group`;

-- Grant read
GRANT SELECT ON TABLE main.default.users TO `analysts`;

-- Check access
SHOW GRANTS ON TABLE main.default.users;
```

### Metadata
```sql
COMMENT ON TABLE main.default.users IS 'Contains PII data';
ALTER TABLE main.default.users SET TBLPROPERTIES ('quality' = 'silver');
```

---

## 🌊 Delta Live Tables (Python)

```python
import dlt

@dlt.table(
    comment="Raw data",
    partition_cols=["date"]
)
@dlt.expect("valid_id", "id IS NOT NULL")
@dlt.expect_or_drop("valid_amount", "amount > 0")
def clean_orders():
    return spark.readStream.format("cloudFiles").load("/path")
```

---

## 🔧 Performance Tuning Cheat Sheet

**1. Slow Shuffle?**
- Check `spark.sql.shuffle.partitions` (Default 200).
- Enable AQE: `spark.sql.adaptive.enabled = true`

**2. Skewed Join?**
- Symptom: 199 tasks finish fast, 1 task takes forever.
- Fix: `spark.sql.adaptive.skewJoin.enabled = true` OR Salt keys.

**3. Broadcast Timeout?**
- Symptom: `Timeout waiting for build`
- Fix: `spark.conf.set("spark.sql.broadcastTimeout", 3600)`

**4. Small Files?**
- Read: `OPTIMIZE ... ZORDER BY`
- Write: `spark.databricks.delta.optimizeWrite.enabled = true`

---

## 📋 Common CLI Commands

**Databricks CLI (v2)**

```bash
# Configure
databricks configure

# Secrets
databricks secrets list-scopes
databricks secrets put-secret --scope my-scope --key my-key

# Jobs
databricks jobs list
databricks jobs run-now --job-id 123

# Workspace
databricks workspace export_dir /Shared/Project ./local_project
```

---

## 🧠 Interview: "Explain this Code"

**Scenario:** You see this in a notebook. What does it do?

```python
(deltaTable.alias("t")
  .merge(updatesDF.alias("s"), "t.id = s.id")
  .whenMatchedUpdate(condition="s.seq > t.seq", set={"val": "s.val", "seq": "s.seq"})
  .whenNotMatchedInsertAll()
  .execute())
```
**Answer:** This is a **CDC (Change Data Capture) Merge**.
- It merges `updatesDF` into `deltaTable`.
- Key: It handles **out-of-order data** using the condition `s.seq > t.seq`. It only updates the target if the source record is *newer* (higher sequence number) than what we already have.
- If it's a new ID, it just inserts.

---

**Keep this open during your coding rounds!** 🚀
