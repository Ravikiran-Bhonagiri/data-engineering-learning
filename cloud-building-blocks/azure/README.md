# Azure Data Engineering Services Guide 🔷

A comprehensive, practical guide to Microsoft Azure services for data engineering.

## 📚 Service Categories

### 1. [Storage Services](01_storage_services.md) 🗄️
- **Azure Blob Storage** - Object storage (Hot, Cool, Archive tiers)
- **Data Lake Storage Gen2** - Hadoop-compatible data lake
- **Azure Files** - Managed file shares

### 2. [Compute & Processing](02_compute_processing.md) ⚙️
- **Synapse Spark Pools** - Serverless Spark
- **Azure Databricks** - Collaborative Spark platform
- **Azure Functions** - Event-driven serverless compute

### 3. [Databases](03_databases.md) 💾
- **Azure SQL Database** - Managed SQL Server
- **Cosmos DB** - Globally distributed NoSQL
- **PostgreSQL/MySQL** - Managed open-source databases

### 4. [Data Integration](04_data_integration.md) 🔄
- **Azure Data Factory** - Visual ETL/ELT orchestration
- **Event Hubs** - Big data streaming ingestion

### 5. [Analytics & Warehousing](05_analytics_warehousing.md) 📊
- **Synapse Dedicated SQL Pools** - Dedicated data warehouse
- **Synapse Serverless SQL** - On-demand querying

### 6. [Streaming & Messaging](06_streaming_messaging.md) 🌊
- **Event Hubs** - High-throughput event streaming
- **Service Bus** - Enterprise messaging

### 7. [Governance & Catalog](07_governance_catalog.md) 🛡️
- **Microsoft Purview** - Unified data governance
- **Azure Policy** - Resource compliance

### 8. [Orchestration](08_orchestration.md) 🎼
- **Azure Data Factory** - Data pipeline orchestration
- **Logic Apps** - Workflow automation

### 9. [Monitoring & Logging](09_monitoring_logging.md) 🕵️
- **Azure Monitor** - Metrics and alerts
- **Log Analytics** - Centralized logging

### 10. [ML & AI Services](10_ml_ai_services.md) 🤖
- **Azure Machine Learning** - End-to-end ML platform
- **Cognitive Services** - Pre-built AI models

### 11. [Service Comparisons](11_service_comparisons.md) 🔍
- Synapse vs SQL Database, ADF vs Databricks, and more

### 12. [Cost Optimization](12_cost_optimization.md) 💰
- Reserved capacity, pause/resume, partitioning strategies

### 13. [Daily Workflow](13_daily_workflow.md) 📅
- End-to-end pipeline patterns and best practices

### 14. [Performance Tuning](14_performance_tuning.md) 🚀
- Synapse optimization, ADF tuning, Databricks configuration

### 15. [Architecture Patterns](15_architecture_patterns.md) 🏗️
- Modern data warehouse, lakehouse, streaming architectures

---

## 🎯 Quick Decision Guide

| Your Need | Azure Service | AWS Equivalent | GCP Equivalent |
|-----------|---------------|----------------|----------------|
| Object Storage | Blob Storage | S3 | Cloud Storage |
| Data Warehouse | Synapse dedicated SQL | Redshift | BigQuery |
| Serverless SQL | Synapse serverless | Athena | BigQuery |
| Spark Processing | Databricks/Synapse Spark | EMR | Dataproc |
| ETL Orchestration | Data Factory | Glue | Dataflow |
| Streaming | Event Hubs | Kinesis | Pub/Sub |
| Relational DB | SQL Database | RDS | Cloud SQL |
| NoSQL | Cosmos DB | DynamoDB | Firestore |
| Governance | Purview | Lake Formation | Data Catalog |
| Monitoring | Azure Monitor | CloudWatch | Cloud Monitoring |

---

## 💡 Azure Philosophy

**Key Characteristics:**
- **Hybrid-First:** Strong integration with on-premises (Azure Arc, Synapse Link)
- **Unified Platform:** Synapse Analytics combines warehouse, Spark, pipelines
- **Pay-as-you-go:** Flexible pricing with pause/resume capabilities
- **Enterprise Focus:** Deep Microsoft ecosystem integration (Power BI, Office 365)

---

## 🚀 Getting Started Path

1. **Week 1-2:** Blob Storage + Synapse serverless SQL
2. **Week 3-4:** Data Factory for ETL
3. **Week 5-6:** Synapse dedicated SQL or Databricks
4. **Week 7-8:** Event Hubs + advanced orchestration

---

## 📖 Additional Resources

- [Architecture Patterns](15_architecture_patterns.md)
- [Service Comparisons](11_service_comparisons.md)
- [Cost Optimization](12_cost_optimization.md)
- [Daily Workflow](13_daily_workflow.md)

---

**Note:** All pricing and examples are grounded in actual Azure pricing and real-world usage patterns.

[Official Azure Documentation](https://docs.microsoft.com/azure) | [Azure Pricing Calculator](https://azure.microsoft.com/pricing/calculator/)
