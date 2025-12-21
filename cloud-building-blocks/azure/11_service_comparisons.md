# Service Comparisons 🔍

[← Back to Main](README.md)

Clear comparisons to help you pick the right Azure service.

---

## Synapse Dedicated SQL vs Serverless SQL

| Factor | Dedicated SQL | Serverless SQL |
|--------|---------------|----------------|
| **Model** | Always-on warehouse | Pay-per-query |
| **Pricing** | DW100c ≈ $1.20/hr | $5/TB scanned |
| **Baseline** | $876/month minimum | $0 when idle |
| **Crossover** | >175TB/month queries | <175TB/month |
| **Performance** | Predictable, scalable | Variable |
| **Use Case** | Production warehouse | Ad-hoc exploration |

**Decision:** Start serverless → Move to dedicated when consistent >$876/month

---

## Data Factory vs Databricks

| Factor | Data Factory | Databricks |
|--------|--------------|------------|
| **Approach** | Visual, low-code | Code-first (Spark) |
| **Pricing** | $1/1K activities + DIU | ~$0.40/hr (DBU + VM) |
| **Best For** | Simple ETL, orchestration | Complex transformations, ML |
| **Learning Curve** | Low | High (Spark) |
| **Team** | Analysts, engineers | Data scientists, engineers |

**Decision:** ADF for pipelines, Databricks for complex Spark/ML

---

## Event Hubs vs Service Bus

| Factor | Event Hubs | Service Bus |
|--------|------------|-------------|
| **Use Case** | High-throughput streaming | Enterprise messaging |
| **Throughput** | Millions of events/sec | Lower volume |
| **Features** | Simple pub/sub | Transactions, sessions, FIFO |
| **Pricing** | $0.015/hr/unit (Standard) | $10/month + operations |

**Decision:** Event Hubs for big data streaming, Service Bus for reliable messaging

---

## Azure vs AWS vs GCP

| Azure | AWS | GCP | Use Case |
|-------|-----|-----|----------|
| Blob Storage | S3 | Cloud Storage | Object storage |
| Synapse dedicated | Redshift | BigQuery dedicated | Data warehouse |
| Synapse serverless | Athena | BigQuery on-demand | Serverless SQL |
| Databricks | EMR | Dataproc | Spark |
| Data Factory | Glue | Dataflow | ETL |
| Event Hubs | Kinesis | Pub/Sub | Streaming |
| SQL Database | RDS | Cloud SQL | Relational DB |
| Purview | Lake Formation | Data Catalog | Governance |

[← Back to Main](README.md)
