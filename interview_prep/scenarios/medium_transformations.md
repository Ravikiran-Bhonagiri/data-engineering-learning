# 🟡 Medium Scenarios 21-30

**Transformations & Optimization Patterns**

---

## Scenario 21: Window Function Memory Pressure

**🏷️ Technologies:** `PySpark`

### Interview Question
*"`Window.partitionBy(user_id)` on 1 billion users causes OOM. One user has 10GB of events. How do you handle this?"*

### What's Happening
Window functions require all data for a partition to fit in single executor memory.

### Solution
```python
# Pre-aggregate to reduce volume
df.groupBy("user_id", "date").agg(sum("amount"))\
  .withColumn("running_total", 
    sum("amount").over(Window.partitionBy("user_id").orderBy("date")))

# Or accept limitation and redesign
# Use batch processing for heavy users separately
```

---

## Scenario 22: Bucketing for Join Optimization

**🏷️ Technologies:** `PySpark` `Delta`

### Interview Question
*"You join the same two large tables multiple times per day. Each join triggers a full shuffle. How do you optimize this?"*

### Solution
```python
# Write with bucketing
df.write.format("delta")\
  .bucketBy(100, "join_key")\
  .sortBy("join_key")\
  .saveAsTable("bucketed_table")

# Subsequent joins skip shuffle entirely
sales.join(products, "product_id")  # No shuffle!
```

---

## Scenario 23-30: Additional Optimization Scenarios

### Scenario 23: Billion-Scale Deduplication (Shuffle Optimization)
**Question:** *"You have 10B rows with 2B duplicates. A simple `ROW_NUMBER()` causes a 5TB shuffle and crashes. How do you optimize this?"*
**Answer:**
1. **Reduce Shuffle Volume:** Group by key first to count duplicates. Filter only keys with `count > 1` (small dataset) to run expensive window function.
2. **Salting:** If one key has 1M duplicates, salt the key before repartitioning.
3. **Approximation:** Use Bloom Filter to filter out distinct keys early.

### Scenario 24: Handling Late Data (Without Watermarks)
**Question:** *"You cannot use Spark Watermarks because you need to join with a static table that updates daily. How do you handle events arriving 3 days late?"*
**Answer:**
- **Double-Write Pattern:** Write late data (detected by event_time vs processing_time) to a separate "Late Landing" path.
- **Batch Backfill:** Scheduled job processes the "Late Landing" path nightly and merges into the Gold table.

### Scenario 25: Spill to Disk
**Question:** *"Logs show 'Spilling to disk'. Query slow. Why?"*
**Answer:** Executors ran out of memory. Increase shuffle partitions or executor memory.

### Scenario 26: DLT vs Standard Streaming
**Question:** *"When to use Delta Live Tables vs standard Structured Streaming?"*
**Answer:** DLT for declarative pipelines with data quality. Standard for complex stateful logic.

### Scenario 27: Managing 1000s of DLT Tables
**Question:** *"DLT pipeline graph too big. How to manage?"*
**Answer:** Split into multiple pipelines. Use `dlt.read_stream("LIVE.other_pipeline_table")`.

### Scenario 28: Semi-Structured JSON
**Question:** *"Query varying JSON schema efficiently?"*
**Answer:** Use variant type: `SELECT json_col:field.nested`.

### Scenario 29: Multi-Cloud Replication  
**Question:** *"Replicate Delta tables from AWS to Azure?"*
**Answer:** `DEEP CLONE` across clouds or use Delta Sharing.

### Scenario 30: Data Contracts Implementation
**Question:** *"Upstream team keeps changing schema, breaking your ETL. 'Talk to them' failed. Implement a hard technical block."*
**Answer:**
- **CI/CD Gate:** Upstream PRs run your contract tests (Great Expectations) in CI.
- **Schema Registry:** Protobuf/Avro with strict forward compatibility.
- **Dead Letter Queue:** Ingestion job validates schema on write; invalid rows go to DLQ, alerting producers immediately.

---

**Previous:** [Complex Scheduling](./medium_complex_scheduling.md) | **Next:** [Integration & Edge Cases](./medium_integration_streaming.md)
