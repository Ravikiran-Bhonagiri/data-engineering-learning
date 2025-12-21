# Architecture Patterns 🏗️

[← Back to Main](README.md)

Common GCP data engineering architecture patterns and best practices.

---

## Pattern 1: Batch Analytics (Classic Data Lake)

```
Cloud Storage (Raw Data)
    ↓
Dataflow (Batch Processing)
    ↓
BigQuery (Data Warehouse)
    ↓
Looker/Data Studio (BI)
```

**When:** Daily/hourly data processing
**Cost:** Low (pay per job)
**Complexity:** Low
**Example:** Daily sales reports

---

## Pattern 2: Streaming Analytics (Real-Time)

```
Application
    ↓
Pub/Sub (Message Queue)
    ↓
Dataflow Streaming (Processing)
    ↓
BigQuery (Storage + Analytics)
    ↓
BI Engine (Sub-second queries)
```

**When:** <1 minute latency required
**Cost:** Medium (persistent workers)
**Complexity:** Medium
**Example:** Real-time user activity dashboard

---

## Pattern 3: Lambda Architecture (Batch + Streaming)

```
         Application
         ↙          ↘
    Pub/Sub      Cloud Storage
    (Real-time)   (Batch)
         ↓            ↓
    Dataflow      Dataflow
    Streaming     Batch
         ↘          ↙
         BigQuery
```

**When:** Need both real-time and batch processing
**Cost:** High (runs both pipelines)
**Complexity:** High
**Example:** E-commerce (real-time inventory + daily reports)

---

## Pattern 4: Database Replication (CDC)

```
Cloud SQL (OLTP)
    ↓
Datastream (CDC)
    ↓
BigQuery (OLAP)
    ↓
Analytics
```

**When:** Keep analytics in sync with operational DB
**Cost:** ~$0.04/GB processed
**Complexity:** Low
**Example:** Customer 360 view

---

## Pattern 5: Data Lake with Governance

```
Cloud Storage (Data Lake)
    ↓
Data Catalog (Discovery)
    ↓
DLP (PII Detection)
    ↓
BigQuery (with Policy Tags)
    ↓
IAM (Access Control)
```

**When:** Compliance requirements (GDPR, HIPAA)
**Cost:** DLP scan costs (~$0.15/GB one-time)
**Complexity:** Medium
**Example:** Healthcare data platform

---

## Pattern 6: ML Pipeline

```
BigQuery (Feature Store)
    ↓
Vertex AI (Train Model)
    ↓
Vertex Endpoints (Serve Predictions)
    ↓
BigQuery ML (or) API
```

**When:** Production ML workflows
**Cost:** Training + inference costs
**Complexity:** High
**Example:** Customer churn prediction

---

## Pattern 7: Multi-Cloud Data Sharing

```
BigQuery Omni
    ↓
Query AWS S3 / Azure Blob
    ↓
Results in BigQuery
```

**When:** Data in multiple clouds
**Cost:** Query costs + cross-cloud egress
**Complexity:** Medium
**Example:** Acquisitions, multi-cloud strategy

---

## Pattern 8: Event-Driven Automation

```
Cloud Storage Upload
    ↓
Cloud Functions (Trigger)
    ↓
Dataflow Job (Start)
    ↓
BigQuery (Load)
    ↓
Workflows (Notify)
```

**When:** Automated, event-driven pipelines
**Cost:** Low (serverless, pay-per-use)
**Complexity:** Low
**Example:** Process uploaded CSV files automatically

---

## Best Practices

### 1. Data Organization

**Cloud Storage:**
```
gs://bucket/
├── raw/            # As-is data
├── staging/        # Cleaned/validated
├── curated/        # Analytics-ready
└── archive/        # Old data (Archive tier)
```

**BigQuery:**
```
project/
├── raw_data/       # Loaded from sources
├── staging/        # Transformations
├── analytics/      # Final models
└── backups/        # Historical snapshots
```

### 2. Security Layers

1. **Network:** VPC, Private Google Access
2. **IAM:** Least privilege, service accounts
3. **Data:** Encryption at rest (default), DLP
4. **Audit:** Cloud Logging, Data Catalog

### 3. Cost Management

- **Start:** On-demand pricing
- **Scale:** Committed use discounts
- **Optimize:** Partitioning, lifecycle policies
- **Monitor:** Budget alerts, cost breakdowns

### 4. Monitoring Strategy

1. **Data Freshness:** Alert if data >30min old
2. **Pipeline Health:** Dataflow lag, job failures
3. **Cost Alerts:** Daily spend thresholds
4. **Data Quality:** Row counts, null checks

---

## Anti-Patterns to Avoid

❌ **Storing everything in BigQuery**
→ Use Cloud Storage for raw files

❌ **No partitioning on large tables**
→ Always partition by date/timestamp

❌ **24/7 Dataproc clusters**
→ Use ephemeral clusters or Dataflow

❌ **SELECT * in production queries**
→ Select only needed columns

❌ **No data governance**
→ Implement IAM, DLP, Data Catalog early

❌ **Over-engineering for small data**
→ Start simple (BigQuery SQL), add complexity as needed

---

## Recommended Architecture Evolution

**Phase 1: Start Simple (0-100GB)**
- Cloud Storage + BigQuery + BigQuery SQL
- Cost: ~$50/month

**Phase 2: Add Processing (100GB-1TB)**
- Add Dataflow for complex ETL
- Cost: ~$200/month

**Phase 3: Add Streaming (Real-time needs)**
- Add Pub/Sub + Dataflow Streaming
- Cost: ~$500/month

**Phase 4: Add Governance (Compliance)**
- Add Data Catalog + DLP + IAM policies
- Cost: +$100/month one-time DLP scans

**Phase 5: Scale & Optimize (>1TB)**
- Flat-rate slots, committed use, advanced tuning
- Cost: $2,000-5,000/month

---

[← Back to Main](README.md)
