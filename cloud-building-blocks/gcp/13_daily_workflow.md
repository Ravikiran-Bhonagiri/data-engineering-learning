# Daily Workflow & Best Practices 📅

[← Back to Main](README.md)

How GCP services fit together in real-world data engineering workflows.

---

## The Standard GCP Data Engineering Pattern

Most GCP data pipelines follow this architecture:

### Phase 1: Ingestion (Get Data In)

**Batch Data:**
- Files uploaded to **Cloud Storage** (raw layer)
- Databases replicated via custom scripts or partner tools
- *Decision:* Cloud Storage is always the landing zone

**Streaming Data:**
- Real-time events → **Pub/Sub**
- *Decision:* Use Pub/Sub if latency <1 min; otherwise batch to Cloud Storage

### Phase 2: Processing (Transform)

**Batch Processing:**
- **Option A:** BigQuery SQL transformations (simple, cheapest)
  - *When:* SQL-only logic, <100GB/day
- **Option B:** Dataflow batch jobs (complex transformations)
  - *When:* Need custom code, >100GB/day, complex logic
- **Option C:** Dataproc (Spark-specific needs)
  - *When:* Need Spark ML, existing Spark code

**Streaming Processing:**
- **Pub/Sub → Dataflow → BigQuery**
  - Classic GCP streaming pattern
  - Sub-minute end-to-end latency

### Phase 3: Storage (Organize)

**Data Lake Layers:**
```
gs://my-bucket/
├── raw/              # As-is data (CSV, JSON)
├── staging/          # Cleaned, validated
└── curated/          # Analytics-ready (Parquet, denormalized)
```

**BigQuery Datasets:**
```
project/
├── raw_data/         # Loaded from Cloud Storage
├── staging/          # Intermediate transformations
└── analytics/        # Final dimensional models
```

### Phase 4: Analytics (Serve Value)

- **Ad-Hoc:** Analysts query BigQuery directly (serverless SQL)
- **BI Dashboards:** Looker, Data Studio, Tableau connected to BigQuery
- **ML:** BigQuery ML or Vertex AI on curated data

### Phase 5: Orchestration (Coordinate)

- **Simple workflows (<10 steps):** Workflows
  - *Example:* Cloud Storage event → Workflows → Dataflow
- **Complex pipelines (20+ tasks):** Cloud Composer (Airflow)
  - *Example:* Daily orchestration of BigQuery → Dataflow → Export

### Phase 6: Monitoring (Stay Reliable)

- **Cloud Monitoring:** Alert on pipeline failures, costs
- **Cloud Logging:** Debug with centralized logs
- **Export logs to BigQuery:** Query logs with SQL

---

## Sample End-to-End Pipeline

**Use Case:** Daily clickstream analytics

```
1. APPLICATION
   ↓ (real-time)
2. PUB/SUB (streaming ingestion)
   ↓
3. DATAFLOW (streaming processing)
   - Parse JSON
   - Enrich with reference data
   - Window aggregations
   ↓
4. BIGQUERY (data warehouse)
   - Streaming inserts
   - Partitioned by date
   ↓
5. LOOKER DASHBOARDS (BI)
   - Real-time charts
   - <10 second freshness
```

**Costs (100GB/day streaming):**
-Pub/Sub: $4/month (ingestion) + $8/month (delivery) = $12/month
- Dataflow: ~$80/month (continuous workers)
- BigQuery: $180/month (storage) + query costs
- **Total: ~$280/month** for real-time analytics

---

## Decision Tree for Common Scenarios

### "I need to query data..."

**Data in Cloud Storage?**
- Yes → BigQuery external table or load to BigQuery
- No → Where is it?
  - Cloud SQL → Query directly or export to BigQuery for analytics
  - Firestore → Export to Cloud Storage → BigQuery

**How often query?**
- Ad-hoc (<10/month) → BigQuery on-demand
- Daily reports (100+ queries/day) → Consider BigQuery slots

### "I need to transform data..."

**What's the data size?**
- <1GB → BigQuery SQL or Cloud Functions
- 1GB-100GB → BigQuery SQL first; Dataflow if needed
- >100GB → Dataflow or Dataproc

**Batch or streaming?**
- Hourly+ → Dataflow batch or BigQuery scheduled queries
- <1 min → Dataflow streaming from Pub/Sub

**Complexity?**
- SQL logic → BigQuery
- Python/Java logic → Dataflow
- Spark-specific → Dataproc

### "I need to orchestrate..."

**How many steps?**
- 1-2 steps → Cloud Scheduler (cron)
- 3-10 steps → Workflows
- 10steps → Cloud Composer

**Team size?**
- 1-2 people → Workflows (avoid $300/month)
- 3+ people → Cloud Composer (shared UI)

---

## GCP Best Practices

1. **Start with BigQuery** - It's the center of most GCP architectures
2. **Use Cloud Storage** - Decouple storage from compute
3. **Partition tables** - By date for cost optimization
4. **Monitor from day 1** - Set up alerts before production
5. **Use IAM properly** - Principle of least privilege
6. **Tag resources** - For cost tracking and organization
7. **Start serverless** - BigQuery, Dataflow before Dataproc
8. **Export logs to BigQuery** - Query your logs with SQL!

---

## Cost Optimization Quick Wins

1. **BigQuery:**
   - Partition tables by date
   - Cluster on frequently filtered columns
   - Use `SELECT columns` not `SELECT *`
   - Materialize expensive queries as tables

2. **Cloud Storage:**
   - Lifecycle policies (Standard → Nearline → Archive)
   - Regional buckets (avoid egress)

3. **Dataflow:**
   - Use Flex RS for batch (30% cheaper)
   - Enable autoscaling
   - Shut down streaming jobs when not needed

4. **General:**
   - Delete unused resources
   - Use committed use discounts (37-55% off)
   - Monitor with budget alerts

---

## Learning Path for GCP Data Engineering

**Week 1-2:** Cloud Storage + BigQuery
- Create buckets, load CSV, query with SQL
- **Hands-on:** Build a simple data warehouse

**Week 3-4:** Dataflow or Dataproc
- Choose based on your needs (Beam vs Spark)
- **Hands-on:** Build ETL pipeline

**Week 5-6:** Pub/Sub + Streaming
- Real-time ingestion patterns
- **Hands-on:** Streaming pipeline to BigQuery

**Week 7-8:** Orchestration + Monitoring
- Cloud Composer or Workflows
- **Hands-on:** End-to-end orchestrated pipeline

---

[← Back to Main](README.md)
