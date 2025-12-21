# Analytics & Warehousing 📊

[← Back to Main](README.md)

BigQuery is the heart of GCP data engineering - a serverless, highly scalable data warehouse.

---

## [BigQuery](https://cloud.google.com/bigquery)

Serverless, petabyte-scale analytics data warehouse with built-in machine learning.

- **Why it matters:** BigQuery is GCP's flagship data service. Most GCP data architectures center around it.
- **Common Task:** Running SQL queries on terabytes of data without managing infrastructure
- **Pricing:** $6.25 per TB scanned (on-demand) OR $0.04/slot-hour (flat-rate)

### ✅ When to Use (Start Simple → Scale Smart)

1. **Any Size Analytics (Start: 1GB → Scale: Petabytes)**
   - **Start Simple:** Query 10GB dataset = $0.06 (practically free)
   - **Scale:** Handle 100TB queries without infrastructure changes
   - **Cost Model:** Pay only for data scanned ($5/TB with good partitioning)
   - **Velocity:** Sub-second to minute query times

2. **Serverless Data Warehouse (Zero management)**
   - **Start:** CREATE TABLE, load CSV = operational in minutes
   - **No Clusters:** Unlike Redshift, zero infrastructure to manage
   - **Auto-scaling:** Handles 1 query/day or 10,000 queries/day automatically
   - **Cost:** No baseline cost when idle (vs Redshift $180/month minimum)

3. **Cost-Effective for Variable Workloads**
   - **On-Demand Example:** 10TB scanned/month = $62.50/month
   - **Flat-Rate Trigger:** When monthly > $2,000 (≈320TB), buy slots
   - **Slots:** 100 slots @ $0.04/slot/hr = ~$2,920/month for predictable costs
   - **Decision:** On-demand until usage is consistent

4. **Built-in ML & Advanced Analytics**
   - **BigQuery ML:** Train ML models with SQL (no Python needed)
   - **GIS Functions:** Analyze geospatial data natively
   - **BI Engine:** In-memory acceleration for dashboards
   - **When:** Need advanced analytics without external tools

5. **Multi-Cloud & External Data**
   - **Query:** Cloud Storage, Google Drive, Bigtable without loading
   - **Federated:** Query Cloud SQL tables directly
   - **Export:** Results to Cloud Storage, Sheets, Data Studio
   - **Flexibility:** Mix internal and external data

### ❌ When NOT to Use

- **Transactional workloads (OLTP):** For row-level updates/deletes, use Cloud SQL or Spanner
- **Small datasets (<1GB) with many updates:** BigQuery optimized for append, not frequent updates
- **Sub-second latency required:** Query startup ~1-3s; use Bigtable or Spanner for <100ms
- **Streaming inserts at high volume:** $0.010/200MB can add up; use batch loading when possible
- **Need fine-grained DML control:** BigQuery best for bulk operations, not row-by-row

### Code Example - Querying BigQuery

```python
from google.cloud import bigquery

client = bigquery.Client()

# Query public dataset
query = """
    SELECT name, SUM(number) as total
    FROM `bigquery-public-data.usa_names.usa_1910_current`
    WHERE year >= 2000
    GROUP BY name
    ORDER BY total DESC
    LIMIT 10
"""

# Dry run to estimate cost
job_config = bigquery.QueryJobConfig(dry_run=True)
dry_run = client.query(query, job_config=job_config)
print(f"Est. cost: ${(dry_run.total_bytes_processed / 1e12) * 6.25:.4f}")

# Execute query
query_job = client.query(query)
results = query_job.result()

for row in results:
    print(f"{row.name}: {row.total}")
```

### Best Practices

- **Partition tables by date** to reduce scan costs (use `_PARTITIONTIME` or column-based)
- **Cluster tables** on frequently filtered columns (e.g., user_id, region)
- **Use `SELECT *` sparingly** - only query columns you need
- **Materialize complex queries** as tables for repeated access
- **Monitor with INFORMATION_SCHEMA** to track costs per query
- **Use BI Engine** for sub-second dashboard queries ($0.355/GB/month)

### Cost Optimization Examples

```sql
-- BAD: Scans entire table (expensive)
SELECT * FROM dataset.large_table WHERE date = '2024-01-01';

-- GOOD: Uses partition pruning (cheap)
SELECT customer_id, amount 
FROM dataset.large_table
WHERE DATE(_PARTITIONTIME) = '2024-01-01';

-- Check bytes scanned before running
SELECT SUM(size_bytes) / 1e12 as TB
FROM dataset.INFORMATION_SCHEMA.PARTITIONS
WHERE table_name = 'large_table'
AND partition_id = '20240101';
```

---

## Related Topics

- **[Storage Services](01_storage_services.md)**: Cloud Storage for BigQuery external tables
- **[Dataflow](02_compute_processing.md)**: Stream processing results into BigQuery
- **[Pub/Sub](06_streaming_messaging.md)**: Real-time ingestion to BigQuery
- **[Cost Optimization](13_cost_optimization.md)**: Partition/cluster strategies

[← Back to Main](README.md)
