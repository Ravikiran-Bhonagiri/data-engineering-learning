# Analytics & Querying 🧠

[← Back to Main](../README.md)

How we make sense of the data once it's stored and cleaned.

---

## [Amazon Athena](https://aws.amazon.com/athena/)

An interactive query service that makes it easy to analyze data in Amazon S3 using standard SQL.

- **Why it matters:** No infrastructure to manage. You simply point to your data in S3 and start writing `SELECT` statements.
- **Common Task:** Ad-hoc analysis and "tasting" the data before building a full ETL pipeline.
- **Pricing:** $5 per TB of data scanned (use Parquet/ORC to reduce costs!)

### ✅ When to Use (Cost & Query Frequency Matter Most)

1. **Sporadic Analytics (Start: $0 → Pay per query)**
   - **Start Simple:** Query 100GB dataset once/month = $0.50
   - **Cost Evolution:** Pay only for data scanned ($5/TB)
   - **Comparison:** $50/month for Athena (e.g., 10TB scanned) vs $180/month Redshift baseline
   - **Decision Point:** Athena wins for intermittent workloads
   - **Complexity:** Zero setup, SQL-ready in minutes

2. **Data Exploration (Before committing to Redshift)**
   - **Use Case:** Prototype dashboards on 10TB dataset
   - **Cost:** $50 to validate vs $500/month Redshift commitment
   - **Philosophy:** "Try before you buy" - validate use case first
   - **Velocity:** Seconds to start querying vs hours to setup Redshift

3. **Variable Query Patterns (Unpredictable load)**
   - **Monday:** 100 queries on 5TB = $25
   - **Rest of week:** 5 queries on 500GB = $0.13
   - **Vs Redshift:** Pay $500/month regardless of usage
   - **When:** Query volume unpredictable month-to-month

4. **Log Investigation (Infrequent, Large scans)**
   - **Use Case:** Query 2 years of CloudTrail logs (20TB) quarterly
   - **Cost:** $100/quarter = $33/month vs $500/month Redshift always-on
   - **Velocity:** Can wait 30-60s per query vs <1s Redshift
   - **Complexity:** No cluster to maintain

5. **Team Self-Service (Many users, few queries each)**
   - **Scenario:** 50 analysts, each 5 queries/month
   - **Cost:** $5-10/user/month vs dedicated Redshift cluster
   - **Why:** Serverless scales automatically, no capacity planning
   - **Trade-off:** ~3s query startup vs instant Redshift

### ❌ When NOT to Use

- **High query frequency (>10/min):** Each query has ~1-5s startup; Redshift <100ms for cached
- **Real-time dashboards:** Sub-second latency needed; use Redshift
- **Frequent small queries:** $0.005 minimum per query adds up; Redshift better for micro-queries
- **Complex ETL transformations:** Athena SQL-only; use Glue/EMR for Spark logic
- **Row-level updates needed:** Athena reads S3 immutably; use RDS/Redshift for updates

### Code Example - Query S3 with Athena (boto3)

```python
import boto3
import time

athena = boto3.client('athena')

# Execute query
response = athena.start_query_execution(
    QueryString='SELECT * FROM my_database.sales WHERE year=2024 LIMIT 100',
    QueryExecutionContext={'Database': 'my_database'},
    ResultConfiguration={'OutputLocation': 's3://my-athena-results/'}
)

query_execution_id = response['QueryExecutionId']

# Wait for query to complete
while True:
    status = athena.get_query_execution(QueryExecutionId=query_execution_id)
    state = status['QueryExecution']['Status']['State']
    if state in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
        break
    time.sleep(1)

# Get results
if state == 'SUCCEEDED':
    results = athena.get_query_results(QueryExecutionId=query_execution_id)
    for row in results['ResultSet']['Rows']:
        print(row['Data'])
```

### Best Practices

- Use **Parquet or ORC** formats to reduce costs by 90%+
- Partition data by common query patterns (e.g., by date)
- Use **CREATE TABLE AS SELECT (CTAS)** to materialize query results
- Enable **Query Result Reuse** to cache results for identical queries

---

## [Amazon Redshift](https://aws.amazon.com/redshift/)

A fast, fully managed data warehouse that makes it simple and cost-effective to analyze all your data using standard SQL.

- **Why it matters:** It's the destination for "Cleaned" and "Aggregated" data used by Business Intelligence (BI) tools.
- **Common Task:** Building star schemas and powering Tableau/PowerBI dashboards.
- **Pricing:** Starting at $0.25/hour for dc2.large (160GB SSD storage)

### ✅ When to Use (When Query Frequency Justifies 24/7 Cost)

1. **High-Frequency Dashboards (>100 queries/day)**
   - **Use Case:** Executive dashboard refreshes every 5 minutes
   - **Cost Math:** Redshift dc2.large node ~$180/month vs Athena
   - **Decision:** Redshift wins if consistent usage >$180/month
   - **Velocity:** <100ms cached queries vs 1-5s Athena startup

2. **Production BI (Predictable, repetitive queries)**
   - **Pattern:** Same 50 queries run 100x/day by Tableau/PowerBI
   - **Why Redshift:** Materialized views, caching, query plans optimized
   - **Cost Efficiency:** Amortize fixed cluser cost across thousands of queries
   - **Example:** $180/month ÷ 150,000 monthly queries = $0.0012/query
   - **Vs Athena:** $5/TB scan (can be expensive for frequently scanned large tables)

3. **Sub-Second Latency (Real-time applications)**
   - **Need:** Dashboard must load <1 second for good UX
   - **Redshift:** 50-200ms for hot queries
   - **Athena:** 1-5s startup even for small queries
   - **When:** User-facing apps, not batch reports

4. **Complex Star Schemas (Optimized JOINs)**
   - **Use Case:** 10-way JOIN across dimension and fact tables
   - **Why Redshift:** Distribution keys co-locate related data
   - **Performance:** Significant speedup over Athena on complex JOINs
   - **Complexity:** Worth the setup for repeated complex queries

5. **Start Cost-Effective, Migrate When Ready**
   - **Start:** Use Athena for first few months (pay-per-query)
   - **Trigger:** When monthly Athena bill exceeds ~$180 (cost of 1 Redshift node)
   - **Migrate:** Move to Redshift to cap costs and improve speed
   - **Philosophy:** Right-size based on actual usage, not predictions

### ❌ When NOT to Use

- **Infrequent queries (<10/day):** Paying $500/month for 10 queries = $1.67/query vs $0.05 Athena
- **Exploratory/Ad-hoc only:** Cluster always running even when unused; use Athena
- **Small datasets (<50GB):** RDS PostgreSQL cheaper and simpler for small data
- **Schema changes frequently:** Redshift schema changes disruptive; S3+Athena flexible
- **Don't know query patterns yet:** Start with Athena, migrate to Redshift when patterns clear

### Best Practices

- Use **Distribution Keys** to co-locate related data
- Define **Sort Keys** to optimize range-filtered queries
- Use **COPY** command to load data from S3 (parallelized)
- Enable **Automatic Workload Management (WLM)** for query prioritization

---

## [Amazon OpenSearch Service](https://aws.amazon.com/opensearch-service/)

Managed search and analytics engine for log analytics, application monitoring, and search.

- **Why it matters:** Perfect for free-text search, log analysis, and real-time dashboards.
- **Common Task:** Building search interfaces or visualizing log data with Kibana
- **Pricing:** ~$0.092/hour for t3.small.search instance

---

## Related Topics

- **[Service Comparisons](12_service_comparisons.md)**: Athena vs Redshift - when to use what
- **[Cost Optimization](13_cost_optimization.md)**: Reduce Athena costs by 95%
- **[Performance Tuning](14_performance_tuning.md)**: Optimize queries and partitions

[← Back to Main](../README.md)
