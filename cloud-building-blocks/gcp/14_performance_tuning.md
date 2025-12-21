# Performance Tuning 🚀

[← Back to Main](README.md)

Optimize GCP data pipelines for speed and efficiency.

---

## BigQuery Performance Tuning

### 1. Partitioning (Query Pruning)

**Impact:** 10-100x faster queries

```sql
-- Slow: Full table scan
SELECT COUNT(*) FROM logs WHERE date = '2024-01-01';
-- Scans: 10TB, Time: 60s

-- Fast: Partition pruning
SELECT COUNT(*) FROM logs_partitioned 
WHERE DATE(timestamp) = '2024-01-01';
-- Scans: 10GB, Time: 2s
```

### 2. Clustering (Filter Optimization)

```sql
CREATE TABLE dataset.events
PARTITION BY DATE(timestamp)
CLUSTER BY user_id, event_type;

-- Highly optimized query
SELECT * FROM dataset.events
WHERE DATE(timestamp) = '2024-01-01'
  AND user_id IN (1, 2, 3)
  AND event_type = 'purchase';
```

**Best Practices:**
- Cluster by high-cardinality columns
- Order: most filtered → least filtered
- Max 4 clustering columns

### 3. Avoid SELECT * in Production

```sql
-- Slow: Reads all 100 columns
SELECT * FROM large_table WHERE id = 123;

-- Fast: Reads only 3 columns
SELECT id, name, email FROM large_table WHERE id = 123;
```

**Impact:** 10-50x faster for wide tables

### 4. Use Appropriate JOIN Strategy

```sql
-- Slow: Large × Large
SELECT * FROM big_table_1 
JOIN big_table_2 ON b1.id = b2.id;

-- Fast: Pre-filter before join
SELECT * FROM (
  SELECT * FROM big_table_1 WHERE date = '2024-01-01'
) b1
JOIN (
  SELECT * FROM big_table_2 WHERE date = '2024-01-01'  
) b2 ON b1.id = b2.id;
```

### 5. Materialize Common Subqueries

```sql
-- Create intermediate table (run once)
CREATE TABLE dataset.daily_aggregates AS
SELECT date, user_id, SUM(amount) as total
FROM dataset.transactions
GROUP BY date, user_id;

-- Query the aggregated table (fast, cheap)
SELECT * FROM dataset.daily_aggregates
WHERE user_id = 123;
```

### 6. Monitor with INFORMATION_SCHEMA

```sql
-- Find slow queries
SELECT 
  query,
  total_slot_ms,
  total_bytes_processed,
  TIMESTAMP_DIFF(end_time, start_time, SECOND) as duration_sec
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
ORDER BY total_slot_ms DESC
LIMIT 10;
```

---

## Dataflow Performance Tuning

### 1. Right-Size Workers

```python
# Too small: Slow processing
options = PipelineOptions(
    machine_type='n1-standard-1'  # 1 vCPU
)

# Optimal: Balance cost/speed
options = PipelineOptions(
    machine_type='n1-standard-4'  # 4 vCPU
)
```

**Tuning:** Monitor CPU/memory utilization

### 2. Optimize Parallelism

```python
# Good: Automatic parallelism
input_data | beam.Map(process_fn)

# Better: Explicit parallelization
input_data | beam.Reshuffle() | beam.Map(heavy_process_fn)
```

### 3. Batch BigQuery Writes

```python
# Slow: Write one row at a time
rows | beam.io.WriteToBigQuery(...)

# Fast: Batch writes
rows | beam.BatchElements(min_batch_size=1000) \
     | beam.io.WriteToBigQuery(...)
```

**Impact:** 10-100x faster

### 4. Use Dataflow Shuffle Service

```python
options = PipelineOptions(
    dataflow_service_options=['shuffle_mode=service']
)
```

**Benefit:** Faster shuffles, lower cost

### 5. Monitor Dataflow Metrics

- **System Lag:** How far behind real-time
- **Data Freshness:** Age of oldest unprocessed element
- **Throughput:** Elements/second

**Action:** Scale workers if lag increasing

---

## Cloud Storage Performance

### 1. Parallel Uploads

```bash
# Slow: Sequential
gsutil cp file1.csv gs://bucket/
gsutil cp file2.csv gs://bucket/

# Fast: Parallel
gsutil -m cp *.csv gs://bucket/
```

### 2. Composite Objects (Large Files)

```bash
# For files >5GB
gsutil -o GSUtil:parallel_composite_upload_threshold=150M \
  cp large_file.csv gs://bucket/
```

### 3. Regional Colocation

**Fast:** Cloud Storage + BigQuery in same region (us-central1)
**Slow:** Cross-region transfers

---

## Dataproc Performance

### 1. Optimize Spark Configuration

```bash
gcloud dataproc clusters create my-cluster \
  --properties spark:spark.sql.shuffle.partitions=200,\
spark:spark.default.parallelism=200
```

### 2. Use SSD Instead of HDD

```bash
--worker-boot-disk-type=pd-ssd  # 10x faster I/O
```

**Trade-off:** 2-3x cost increase

### 3. Choose Right Machine Type

- **CPU-bound:** n1-highcpu
- **Memory-bound:** n1-highmem
- **Balanced:** n1-standard

---

## Performance Monitoring Tools

### 1. Cloud Profiler
- **For:** Dataflow, custom code
- **Shows:** CPU/memory hotspots

### 2. Cloud Trace
- **For:** Request latency
- **Shows:** Where time is spent

### 3. BigQuery Execution Plan
```sql
-- View query execution details
SELECT * FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE job_id = 'your-query-id';
```

---

## Quick Performance Checklist

**BigQuery:**
- [ ] Tables partitioned by date
- [ ] Clustered on filter columns
- [ ] SELECT specific columns
- [ ] Joins pre-filtered
- [ ] Expensive queries materialized

**Dataflow:**
- [ ] Right-sized machine types
- [ ] Autoscaling enabled
- [ ] Batch writes to BigQuery
- [ ] Shuffle service enabled
- [ ] Reshuffle before expensive operations

**Cloud Storage:**
- [ ] Parallel uploads (gsutil -m)
- [ ] Regional colocation
- [ ] Composite uploads for large files

**Dataproc:**
- [ ] Spark configs tuned
- [ ] Appropriate machine types
- [ ] SSD for I/O-heavy workloads

---

[← Back to Main](README.md)
