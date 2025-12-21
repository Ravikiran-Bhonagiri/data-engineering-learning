# Architecture Patterns 🏗️

[← Back to Main](README.md)

Common Azure data engineering architecture patterns.

---

## Pattern 1: Modern Data Warehouse

```
Source Systems
    ↓
Data Factory (Ingest)
    ↓
Data Lake Gen2 (Bronze/Silver/Gold layers)
    ↓
Synapse Dedicated SQL (Serve)
    ↓
Power BI (Consume)
```

**When:** Traditional BI and reporting
**Cost:** ~$200-500/month (small scale)

---

## Pattern 2: Lakehouse (Delta Lake)

```
Raw Data → Blob Storage
    ↓
Databricks (Process with Delta Lake)
    ↓
Delta Tables (Bronze → Silver → Gold)
    ↓
Synapse Serverless SQL OR Power BI Direct Lake
```

**When:** Need both data lake flexibility and warehouse performance
**Cost:** Variable based on compute usage

---

## Pattern 3: Real-Time Analytics

```
Applications
    ↓
Event Hubs (Ingest)
    ↓
Stream Analytics OR Databricks Streaming
    ↓
Synapse Dedicated SQL Pool
    ↓
Power BI (Real-time dashboards)
```

**When:** <1 minute analytics latency
**Cost:** ~$500-1,000/month

---

## Pattern 4: Hybrid (On-Prem + Cloud)

```
On-Premises SQL Server
    ↓
Data Factory (Self-Hosted IR)
    ↓
Azure Data Lake Gen2
    ↓
Synapse Analytics
```

**When:** Gradual cloud migration
**Cost:** On-prem + Azure costs

---

## Pattern 5: Serverless Analytics

```
Blob Storage (Data Lake)
    ↓
Synapse Serverless SQL (Ad-hoc queries)
    ↓
Power BI OR External Applications
```

**When:** Unpredictable query patterns, cost optimization
**Cost:** Pay-per-query ($5/TB)

---

## Best Practices

### Data Lake Organization

```
/raw/              # As-is from source
/staging/          # Cleaned, validated
/curated/          # Analytics-ready
/archive/          # Historical (Archive tier)
```

### Medallion Architecture (Bronze/Silver/Gold)

- **Bronze:** Raw data
- **Silver:** Cleaned, enriched
- **Gold:** Business-level aggregates

### Security Layers

1. **Network:** Private endpoints, VNet integration
2. **Identity:** Azure AD, managed identities
3. **Data:** Encryption at rest, column-level security
4. **Audit:** Purview, Azure Monitor logs

---

## Anti-Patterns to Avoid

❌ **Not pausing Synapse dedicated pools**
→ Wastes $876/month when idle

❌ **Using Synapse dedicated for ad-hoc queries**
→ Use serverless instead

❌ **No data lake organization**
→ Implement Bronze/Silver/Gold layers

❌ **Storing everything in Synapse**
→ Use Data Lake for raw files

❌ **Ignoring partitioning**
→ Always partition large tables by date

---

## Recommended Evolution

**Phase 1: Start Simple (0-100GB)**
- Blob Storage + Synapse Serverless + Power BI
- Cost: ~$50/month

**Phase 2: Add Processing (100GB-1TB)**
- Add Data Factory for ETL
- Cost: ~$200/month

**Phase 3: Add Dedicated Warehouse (>1TB, consistent load)**
- Synapse Dedicated SQL (with pause/resume)
- Cost: ~$500/month

**Phase 4: Advanced (Streaming, ML)**
- Add Event Hubs, Databricks
- Cost: $1,000-5,000/month

[← Back to Main](README.md)
