# Daily Workflow & Patterns 📅

[← Back to Main](README.md)

How Azure services fit together in real-world data pipelines.

---

## Standard Azure Data Pipeline

### Phase 1: Ingestion

**Batch:**
- Files → Blob Storage / Data Lake Gen2

**Streaming:**
- Events → Event Hubs

### Phase 2: Processing

**Option A:** Data Factory (Visual ETL)
- Simple transformations
- Orchestration

**Option B:** Databricks (Complex Spark)
- ML pipelines
- Advanced transformations

**Option C:** Synapse Spark
- Integrated with Synapse workspace

### Phase 3: Storage

**Data Lake Structure:**
```
/raw/           # As-is data
/staging/       # Cleaned
/curated/       # Analytics-ready
```

**Load to Warehouse:**
- Synapse Dedicated SQL (production)
- Synapse Serverless SQL (exploration)

### Phase 4: Analytics

- Power BI → Synapse/SQL Database
- Analysts → Synapse Serverless
- Applications → SQL Database

### Phase 5: Monitor

- Azure Monitor for alerts
- Data Factory monitoring
- Purview for lineage

---

## Sample End-to-End Pipeline

**Use Case:** Daily sales processing

```
1. Source System
   ↓ (nightly export)
2. BLOB STORAGE (raw/)
   ↓ (trigger)
3. DATA FACTORY Pipeline
   - Copy to staging
   - Transform with mapping data flow
   ↓
4. DATA LAKE (curated/)
   ↓ (load)
5. SYNAPSE DEDICATED SQL
   ↓
6. POWER BI Dashboards
```

**Costs (100GB/day):**
- Blob Storage: $1.84/month
- Data Factory: ~$30/month
- Synapse DW100c (8hrs/day): ~$192/month
- **Total: ~$224/month**

---

## Decision Tree

### "I need to query data..."

**Where is it?**
- Blob Storage → Synapse Serverless or load to dedicated
- SQL Database → Query directly or sync to Synapse

**How often?**
- Ad-hoc → Synapse Serverless
- Daily heavy use → Synapse Dedicated (with pause/resume)

### "I need to transform data..."

**Complexity?**
- Simple → Data Factory mapping data flows
- Complex/ML → Databricks

**Volume?**
- <1TB → Data Factory
- >1TB → Databricks or Synapse Spark

### "I need orchestration..."

**Steps?**
- <10 steps → Data Factory
- Complex dependencies → Consider Apache Airflow

---

## Best Practices

1. **Use Data Lake Gen2** for analytics workloads
2. **Partition** by date in Synapse
3. **Pause** dedicated SQL pools when not in use
4. **Start serverless** before committing to dedicated
5. **Monitor** from day 1 with Azure Monitor
6. **Tag resources** for cost tracking
7. **Use Purview** early for governance

[← Back to Main](README.md)
