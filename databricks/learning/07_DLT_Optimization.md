# Supplemental: DLT Optimization Guide

**Advanced patterns for making Delta Live Tables run fast and cheap.**

---

## 1. Enhanced Autoscaling

DLT uses a specialized autoscaling algorithm designed for streaming workloads.
- **Legacy Autoscaling:** Waits for CPU to spike. Slow start-up.
- **Enhanced Autoscaling:** Looks at backlog metrics (Kafka/DeltaLog). Proactively scales up *before* the cluster chokes.

**Config:**
```json
"configuration": {
    "spark.databricks.cluster.profile": "serverless" (or standard)
}
```

---

## 2. Partitioning in DLT

Use `partition_cols` only for large tables (>1TB).
Over-partitioning kills DLT performance because of small files.
```python
@dlt.table(
    partition_cols=["date"]
)
```
**Better:** Use Liquid Clustering (if available in DLT runtime).

---

## 3. Incremental vs Complete

- **Streaming Live Table:** Incremental. Keeps state.
    - Good for: Fact tables, Append-only logs.
- **Live Table (Materialized View):** Recomputes from scratch every run.
    - Good for: Small dimension tables (<10M rows), complex joins where history changes.

**Antipattern:**
Using a Streaming Live Table for a small lookup table that updates frequently. You will deal with complex state management. Just recompute it.

---

## 4. SCD Type 2 Optimization

`dlt.apply_changes` is magic, but can be slow if keys are skewed.

**Optimization:**
Ensure the `keys` used in `apply_changes` are high-cardinality and evenly distributed.
If you have a hotspot (e.g., Key="Unknown"), filter it out before the apply_changes logic.

---

## 5. Observability

Query the event log to find bottlenecks.

```sql
SELECT 
    timestamp,
    details:flow_progress.metrics.num_output_rows as rows,
    details:flow_progress.status as status
FROM event_log_raw
WHERE event_type = 'flow_progress'
ORDER BY timestamp DESC
```

**Interview Tip:**
If asked "How do you monitor DLT?", mention the **Event Log**. It's a hidden Delta table that stores every metric. You can build a Dashboard on top of it to track "Rows Processed Per Second" or "Quality Failure Rate".
