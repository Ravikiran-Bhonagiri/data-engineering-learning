# GCP Data Engineering Services Guide 🔵

A comprehensive, practical guide to Google Cloud Platform services for data engineering.

## 📚 Service Categories

### 1. [Storage Services](01_storage_services.md) 🗄️
- **Cloud Storage** - Object storage (like AWS S3)
- **Filestore** - Managed NFS file storage

### 2. [Compute & Processing](02_compute_processing.md) ⚙️
- **Dataflow** - Serverless Apache Beam (streaming & batch)
- **Dataproc** - Managed Spark & Hadoop clusters
- **Cloud Functions** - Event-driven serverless compute

### 3. [Databases](03_databases.md) 💾
- **Cloud SQL** - Managed MySQL, PostgreSQL, SQL Server
- **Cloud Spanner** - Globally distributed relational DB
- **Firestore** - Document database

### 4. [Data Integration](04_data_integration.md) 🔄
- **Data Fusion** - Visual ETL pipeline builder
- **Datastream** - Serverless CDC and replication

### 5. [Analytics & Warehousing](05_analytics_warehousing.md) 📊
- **BigQuery** - Serverless data warehouse (STAR SERVICE)

### 6. [Streaming & Messaging](06_streaming_messaging.md) 🌊
- **Pub/Sub** - Streaming message bus
- **Dataflow Streaming** - Real-time processing

### 7. [Governance & Catalog](07_governance_catalog.md) 🛡️
- **Data Catalog** - Metadata management
- **DLP (Data Loss Prevention)** - Sensitive data protection
- **IAM** - Identity and Access Management

### 8. [Orchestration](08_orchestration.md) 🎼
- **Cloud Composer** - Managed Apache Airflow
- **Workflows** - Serverless orchestration

### 9. [Monitoring & Logging](09_monitoring_logging.md) 🕵️
- **Cloud Monitoring** - Metrics & alerts
- **Cloud Logging** - Centralized logging

### 10. [ML & AI Services](10_ml_ai_services.md) 🤖
- **Vertex AI** - Unified ML platform
- **BigQuery ML** - SQL-based machine learning

### 11. [Service Comparisons](11_service_comparisons.md) 🔍
- BigQuery vs Cloud SQL, Dataflow vs Dataproc, and more

### 12. [Cost Optimization](12_cost_optimization.md) 💰
- Partitioning strategies, lifecycle policies, committed use discounts

### 13. [Daily Workflow](13_daily_workflow.md) 📅
- End-to-end pipeline patterns and best practices

### 14. [Performance Tuning](14_performance_tuning.md) 🚀
- BigQuery optimization, Dataflow tuning, monitoring

### 15. [Architecture Patterns](15_architecture_patterns.md) 🏗️
- Reference architectures and design patterns

---

## 🎯 Quick Decision Guide

| Your Need | GCP Service | AWS Equivalent |
|-----------|-------------|----------------|
| Object Storage | Cloud Storage | S3 |
| Data Warehouse | BigQuery | Redshift |
| Serverless ETL | Dataflow | Glue |
| Managed Spark | Dataproc | EMR |
| Real-time Messaging | Pub/Sub | Kinesis |
| Transactional DB | Cloud SQL | RDS |
| Orchestration | Cloud Composer | MWAA |
| Serverless Functions | Cloud Functions | Lambda |

---

## 💡 GCP Philosophy

**Key Differences from AWS:**
- **Serverless-First:** GCP emphasizes serverless (BigQuery, Dataflow)
- **BigQuery is King:** Central to most GCP data architectures
- **Simpler Pricing:** Often more straightforward than AWS
- **Pay-per-Use:** Less emphasis on committed/reserved instances

---

## 🚀 Getting Started Path

1. **Week 1-2:** Master Cloud Storage + BigQuery
2. **Week 3-4:** Learn Dataflow or Dataproc
3. **Week 5-6:** Add Pub/Sub for streaming
4. **Week 7-8:** Orchestrate with Cloud Composer

---

## 📖 Additional Resources

- [Architecture Patterns](11_architecture_patterns.md)
- [Service Comparisons](12_service_comparisons.md)
- [Cost Optimization](13_cost_optimization.md)
- [Daily Workflow](14_daily_workflow.md)

---

**Note:** All pricing and examples in this guide are grounded in actual GCP pricing and real-world usage patterns. No exaggerations!

[Official GCP Documentation](https://cloud.google.com/docs) | [GCP Pricing Calculator](https://cloud.google.com/products/calculator)
