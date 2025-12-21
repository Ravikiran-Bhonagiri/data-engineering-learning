# 🔴 Hard Scenarios 11-20

**Advanced Patterns & Edge Cases**

---

## Scenario 11: Zombie Kafka Offsets

**🏷️ Technologies:** `PySpark` `Kafka` `Streaming`

### Interview Question
*"Your Spark Streaming job crashes. When you restart, it fails with `OffsetOutOfRangeException`. Checkpoint says offset 500, but Kafka's earliest offset is now 1000. What happened and how do you handle this safely?"*

### What's Happening
Kafka retention policy deleted old messages while job was down (offset 500-999).

### Solution
```python
df = spark.readStream.format("kafka")\
  .option("failOnDataLoss", "false")\  # Accept data loss
  .option("startingOffsets", "earliest")\  # Reset to 1000
  .load()

# Alert: Data lost (offsets 500-999)
```

---

## Scenario 12: Backfilling Stateful Streaming

**🏷️ Technologies:** `PySpark` `Streaming`

### Interview Question
*"Your stateful streaming job (`mapGroupsWithState`) crashed and you need to backfill 1 week of data. How do you do this without replaying the entire history from day 1?"*

### Hard Truth
**You can't.** Stateful streaming requires full history replay.

### Solution (Lambda Architecture)
```
- Speed Layer: Resume streaming from "now"
- Batch Layer: Separate Spark batch job for backfill period
- Serving: Application merges batch + stream results
```

---

## Scenario 13-20: Advanced Architecture Patterns

### Scenario 13: High-Cardinality Window Functions
**Question:** *"Window partition by 1B users, one user has 10GB events. OOM. Solutions?"*
**Answer:** Pre-aggregate or accept limitation (window needs all partition data in memory).

### Scenario 14: Semantic Layer
**Question:** *"'Revenue' defined differently in Tableau vs ML models. How to standardize?"*
**Answer:** dbt MetricFlow. Define metric once, all tools consume via API.

### Scenario 15: Write-Audit-Publish
**Question:** *"Data quality checks must pass BEFORE consumers see data. Pattern?"*
**Answer:** Write to staging → quality checks → if pass, swap/publish.

### Scenario 16: Feature Store
**Question:** *"Why not just use a table for ML features?"*
**Answer:** Point-in-time correctness + online/offline sync. Feature Store handles both.

### Scenario 17: Skewed Window Management
**Question:** *"Window partition won't fit in memory (50GB). Solutions?"*
**Answer:** Pre-aggregate, custom `mapGroups` with iterative processing, or redesign.

### Scenario 18: Dynamic DAG Generation
**Question:** *"500 tables to ingest. Can't hand-code 500 DAGs. Solution?"*
**Answer:** Config-driven: `for table in config: globals()[f"dag_{table}"] = create_dag (table)`.

### Scenario 19: Data Mesh
**Question:** *"Implement Data Mesh architecture with Unity Catalog?"*
**Answer:** Domains own catalogs. Cross-domain via GRANT. Contracts published as schemas.

### Scenario 20: Ultimate Architecture
**Question:** *"Design platform to ingest 1PB/day, transform, ML train, dashboards. Components?"*
**Answer:** Kafka → Auto Loader → Bronze → dbt → Silver/Gold → Feature Store + MLflow + BI.

---

**Previous:** [System Architecture](./hard_system_architecture.md) | **Next:** [Governance & Security](./hard_governance_security.md)
