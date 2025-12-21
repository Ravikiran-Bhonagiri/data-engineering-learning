# Cost Optimization 💰

[← Back to Main](README.md)

Reduce Azure costs without sacrificing performance.

---

## Synapse Cost Optimization

### 1. Pause/Resume Dedicated SQL Pools (Save 60-70%)

**The Problem:** DW100c running 24/7 = $876/month
**The Solution:** Pause when not in use

- **Business hours only:** 8hrs × 5 days = 160 hrs/month = $192/month
- **Savings:** $684/month (78%)
- **Automation:** Use Azure Automation to pause/resume on schedule

### 2. Use Serverless for Ad-Hoc Queries

- **Dedicated:** $876/month minimum
- **Serverless:** $5/TB scanned
- **Decision:** Serverless until >175TB/month

### 3. Partition Tables (90% savings on queries)

```sql
-- Partitioned table scans only relevant data
CREATE TABLE Sales
WITH (
    DISTRIBUTION = HASH(OrderID),
    PARTITION (OrderDate RANGE RIGHT FOR VALUES ('2024-01-01', '2024-02-01'))
) AS SELECT * FROM SourceTable;
```

---

## Blob Storage Optimization

### 1. Lifecycle Management (89% savings)

- **Hot:** $0.0184/GB → **Archive:** $0.002/GB
- **Automated:** Hot (30d) → Cool (90d) → Archive (1yr)
- **Savings:** For 1TB archived = $18.40 → $2/month

### 2. Reserved Capacity (30-40% off)

- **1 year:** 20-37% discount
- **3 years:** Up to 55% discount
- **When:** Predictable storage needs

---

## Databricks Optimization

### 1. Spot Instances (60-80% savings)

- **Regular VM:** $0.30/hr
- **Spot VM:** $0.06-0.12/hr
- **Risk:** Can be terminated; good for fault-tolerant workloads

### 2. Auto-Termination

- **Set idle timeout:** Terminate after 10 min idle
- **Savings:** Avoid paying for forgotten clusters

---

## Data Factory Optimization

### 1. Use Self-Hosted Integration Runtime

- **Avoid DIU costs:** Run on your own VMs for on-prem connectivity
- **When:** Frequent on-prem data movement

### 2. Batch Activities

- **Reduce execution count:** Combine multiple small copies into one

---

## Quick Wins

- [ ] Pause Synapse dedicated pools when not in use
- [ ] Set Blob Storage lifecycle policies
- [ ] Enable Databricks auto-termination
- [ ] Use reserved capacity for predictable workloads
- [ ] Set budget alerts in Azure Cost Management

**Potential Savings:** 40-70% reduction

[← Back to Main](README.md)
