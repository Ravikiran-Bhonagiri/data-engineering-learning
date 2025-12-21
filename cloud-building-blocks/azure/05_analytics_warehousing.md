# Analytics & Warehousing 📊

[← Back to Main](README.md)

Azure Synapse Analytics - unified data warehouse and big data analytics.

---

## [Synapse Dedicated SQL Pools](https://azure.microsoft.com/services/synapse-analytics/)

Data warehouse with dedicated compute resources (formerly SQL Data Warehouse).

- **Why it matters:** Azure's answer to AWS Redshift / GCP BigQuery
- **Common Task:** Enterprise data warehouse for BI and analytics
- **Pricing:** DWU-based; DW100c (Gen2) ≈ $1.20/hour when running

### ✅ When to Use (Dedicated Warehouse)

1. **24/7 Data Warehouse (Predictable workloads)**
   - **Start:** DW100c = $1.20/hr × 730 hrs = $876/month
   - **Scale:** DW500c = $6/hr = $4,380/month
   - **Pause/Resume:** Stop when not in use (nights/weekends) to save 60-70%
   - **When:** Consistent heavy query load

2. **Large Data Volumes (>1TB)**
   - **ColumnStore:** Optimized for analytics queries
   - **Partitioning:** Distribute large tables across nodes
   - **Performance:** Predictable query times
   - **vs Serverless:** Better for regular heavy use

3. **Complex Workloads (Concurrent users)**
   - **Concurrency:** Handle 20+ simultaneous queries
   - **Resource Classes:** Allocate memory per query
   - **When:** BI tools with many users

### ❌ When NOT to Use

- **Sporadic queries:** Synapse serverless cheaper for ad-hoc
- **Small datasets (<100GB):** SQL Database simpler
- **Cost-sensitive with variable load:** Serverless pay-per-query better

---

## [Synapse Serverless SQL](https://azure.microsoft.com/services/synapse-analytics/)

On-demand SQL queries on data lake without provisioning resources.

- **Why it matters:** Query data without managing infrastructure (like AWS Athena/GCP BigQuery)
- **Common Task:** Ad-hoc queries on Parquet/CSV in Data Lake
- **Pricing:** $5/TB processed

### ✅ When to Use (Serverless Queries)

1. **Ad-Hoc Data Exploration**
   - **Pay-per-query:** 10TB/month = $50/month  
   - **No baseline cost:** vs DW100c $876/month minimum
   - **Crossover:** When queries >175TB/month, dedicated cheaper
   - **When:** Sporadic, unpredictable workloads

2. **External Tables on Data Lake**
   - **Query:** Parquet/CSV directly in Blob/Data Lake
   - **No loading:** Data stays in storage
   - **Cost:** Storage ($0.018/GB) + query ($5/TB)
   - **When:** Infrequently queried data

3. **Fast Prototyping**
   - **Zero setup:** Start querying immediately
   - **Iterate:** Test queries, then move to dedicated if needed
   - **Graduate:** Load into dedicated pool for production

### ❌ When NOT to Use

- **Heavy consistent use:** >175TB/month queries = dedicated cheaper
- **Need materialized views:** Dedicated SQL pools only
- **SLA requirements:** Dedicated provides predictable performance

---

## Decision: Dedicated vs Serverless

| Factor | Dedicated SQL | Serverless SQL |
|--------|---------------|----------------|
| **Cost Model** | DWU-hour (~$1.20/hr min) | $5/TB scanned |
| **Baseline** | $876/month (DW100c) | $0 when idle |
| **Crossover** | >175TB/month queries | <175TB/month |
| **Performance** | Predictable, tunable | Variable |
| **Use Case** | Production warehouse | Ad-hoc exploration |

**Recommendation:** Start serverless → Move to dedicated when consistent >$876/month

---

[← Back to Main](README.md)
