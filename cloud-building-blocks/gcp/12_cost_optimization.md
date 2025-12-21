# Cost Optimization 💰

[← Back to Main](README.md)

Strategies to reduce GCP data engineering costs without sacrificing performance.

---

## BigQuery Cost Optimization

### 1. Partitioning (Save 90%+ on queries)

**The Problem:** Querying entire table scans all data
**The Solution:** Partition by date/timestamp

```sql
-- BAD: Scans entire 10TB table = $62.50
SELECT * FROM dataset.logs
WHERE date = '2024-01-01';

-- GOOD: Scans only 1 day partition (10GB) = $0.06
CREATE TABLE `dataset.logs_partitioned`
PARTITION BY DATE(timestamp)
AS SELECT * FROM `dataset.logs`;

SELECT * FROM `dataset.logs_partitioned`
WHERE DATE(timestamp) = '2024-01-01';
```

**Savings:** 99.9% reduction in scanned data

### 2. Clustering (Additional 50% savings)

**Combine with partitioning:**

```sql
CREATE TABLE `dataset.logs_optimized`
PARTITION BY DATE(timestamp)
CLUSTER BY user_id, region
AS SELECT * FROM `dataset.logs`;

-- Now queries filtered by user_id/region scan even less
SELECT * FROM `dataset.logs_optimized`
WHERE DATE(timestamp) = '2024-01-01'
  AND user_id = 12345;
```

**Best For:** Columns frequently used in WHERE/GROUP BY

### 3. Select Only Columns Needed

```sql
-- BAD: Scans all 50 columns
SELECT * FROM dataset.large_table;

-- GOOD: Only scans 2 columns
SELECT user_id, revenue FROM dataset.large_table;
```

**Savings:** Columns stored separately; pay only for what you query

### 4. Materialize Expensive Queries

```sql
-- Run expensive query once, save results
CREATE TABLE `dataset.daily_aggregate` AS
SELECT date, SUM(revenue) as total
FROM `dataset.transactions`
GROUP BY date;

-- Query the small table repeatedly (cheap)
SELECT * FROM `dataset.daily_aggregate`;
```

**When:** Same complex query run 10+ times

### 5. On-Demand vs Flat-Rate Slots

**Decision Matrix:**
- **<$2,000/month scanned:** Stay on-demand ($6.25/TB)
- **>$2,000/month consistent:** Buy slots ($2,920/month for 100 slots)
- **Calculation:** $2,000 ÷ $6.25 = 320TB/month crossover

---

## Cloud Storage Cost Optimization

### 1. Lifecycle Policies (Save 94%)

```
Standard (30 days): $0.020/GB
↓ Auto-transition
Nearline (60 days): $0.010/GB
↓ Auto-transition  
Coldline (90 days): $0.004/GB
↓ Auto-transition
Archive (1 year): $0.0012/GB
```

**Setup:**
```bash
gsutil lifecycle set lifecycle-config.json gs://my-bucket
```

### 2. Regional vs Multi-Regional

- **Multi-Region:** $0.026/GB (99.95% SLA)
- **Single-Region:** $0.020/GB
- **Savings:** 23% for non-critical data

### 3. Avoid Egress Charges

- **Free:** Same region (Cloud Storage → BigQuery in us-central1)
- **Expensive:** Cross-region or internet egress
- **Strategy:** Colocate compute and storage

---

## Dataflow Cost Optimization

### 1. Use FlexRS (30% cheaper)

```python
options = PipelineOptions(
    flexrsgoal='COST_OPTIMIZED'  # 30% discount
)
```

**Trade-off:** May be delayed if resources unavailable
**Best For:** Non-time-sensitive batch jobs

### 2. Autoscaling

```python
options = PipelineOptions(
    autoscaling_algorithm='THROUGHPUT_BASED',
    max_num_workers=50,
    num_workers=2  # Start small, scale up
)
```

**Savings:** Don't over-provision workers

### 3. Use Appropriate Machine Types

- **Default:** n1-standard-1 (1 vCPU, 3.75GB)
- **Memory-intensive:** n1-highmem-2
- **CPU-intensive:** n1-highcpu-4

**Right-sizing saves 30-50%**

---

## Dataproc Cost Optimization

### 1. Ephemeral Clusters

```bash
# Create cluster, run job, delete cluster
gcloud dataproc clusters create temp-cluster --max-idle=10m

# Auto-deletes after 10 min idle
```

**vs 24/7 cluster:** Save 80%+ for sporadic jobs

### 2. Preemptible Workers (70% cheaper)

```bash
gcloud dataproc clusters create my-cluster \
  --num-workers=10 \
  --num-preemptible-workers=20  # 70% cheaper
```

**Trade-off:** Can be terminated; use for non-critical processing

### 3. Committed Use Discounts

- **1 year:** 37% off
- **3 years:** 55% off
- **When:** Predictable 24/7 workloads

---

## General GCP Cost Optimization

### 1. Budget Alerts

```bash
# Alert when spend > $100/day
gcloud billing budgets create --billing-account=XXXXX \
  --display-name="Daily Budget" \
  --budget-amount=100
```

### 2. Cost Breakdown Reports

- **BigQuery Queries:** INFORMATION_SCHEMA.JOBS
- **Cloud Storage:** Storage class reports
- **Dataflow:** Job metrics in Cloud Monitoring

### 3. Clean Up Unused Resources

**Common Waste:**
- Snapshots never deleted
- Old BigQuery tables
- Orphaned Cloud Storage buckets
- Idle Dataproc clusters

---

## Cost Comparison Examples

### ETL Pipeline Costs

| Approach | Monthly Cost |
|----------|--------------|
| BigQuery SQL transforms | $50 (query costs) |
| Dataflow batch (daily) | $85 (sporadic) |
| Dataproc 24/7 | $300 (always on) |
| Data Fusion | $250+ (instance + compute) |

**Recommendation:** Start with BigQuery SQL

### Storage Costs (1TB)

| Tier | Monthly Cost | Retrieval | Use When |
|------|--------------|-----------|----------|
| Standard | $20 | Free | Frequent access |
| Nearline | $10 | $0.01/GB | Monthly access |
| Coldline | $4 | $0.02/GB | Quarterly |
| Archive | $1.20 | $0.05/GB | Yearly |

---

## Quick Wins Checklist

- [ ] Partition BigQuery tables by date
- [ ] Cluster frequently filtered columns
- [ ] Use SELECT columns (not SELECT *)
- [ ] Set Cloud Storage lifecycle policies
- [ ] Use FlexRS for Dataflow batch
- [ ] Delete old BigQuery tables (>90 days unused)
- [ ] Use preemptible workers in Dataproc
- [ ] Set budget alerts
- [ ] Review INFORMATION_SCHEMA for expensive queries

**Potential Savings:** 30-70% reduction

---

[← Back to Main](README.md)
