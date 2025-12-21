# Architecture Patterns 🏛️

[← Back to Main](../README.md)

Here are typical architectures you'll build using these services.

---

## Pattern 1: Modern Data Lake

```mermaid
graph LR
    A[SaaS Apps<br/>Salesforce] -->|AppFlow| B[S3 Raw Zone]
    C[RDS Database] -->|DMS CDC| B
    D[Streaming Events] -->|Kinesis<br/>Firehose| B
    B -->|Glue Crawler| E[Glue Data<br/>Catalog]
    B -->|Glue ETL Job| F[S3 Curated Zone]
    F -->|Athena Query| G[Analysts]
    F -->|COPY| H[Redshift DW]
    H --> I[BI Tools<br/>Tableau]
    J[Airflow MWAA] -.orchestrates.-> B
    J -.orchestrates.-> F
```

**Use Case:** Centralized data repository from multiple sources

**Key Services:**
- S3 for storage
- DMS/AppFlow for ingestion
- Glue for ETL and cataloging
- Athena for ad-hoc queries
- Redshift for BI workloads

---

## Pattern 2: Real-time Analytics Pipeline

```mermaid
graph LR
    A[Web/Mobile Apps] -->|PUT records| B[Kinesis Data<br/>Streams]
    B -->|Consumer 1| C[Lambda<br/>Enrichment]
    B -->|Consumer 2| D[Kinesis Data<br/>Analytics]
    C --> E[S3 Hot Data]
    D --> F[OpenSearch<br/>Dashboard]
    E -->|Athena| G[Real-time<br/>Queries]
```

**Use Case:** Process and analyze streaming events in real-time

**Key Services:**
- Kinesis Data Streams for ingestion
- Lambda for transformation
- Kinesis Data Analytics for stream processing
- OpenSearch for dashboards

---

## Pattern 3: Batch ETL with Orchestration

```mermaid
graph TD
    A[S3 Event] -->|Trigger| B[Lambda Validator]
    B -->|Valid| C[SNS Topic]
    C -->|Notify| D[Airflow DAG]
    D -->|Step 1| E[Glue Crawler]
    D -->|Step 2| F[Glue Spark Job]
    F --> G[S3 Parquet]
    G --> H[Redshift COPY]
    F -.logs.-> I[CloudWatch]
    I -.alarm.-> J[SNS Alert]
```

**Use Case:** Automated daily batch processing with error handling

**Key Services:**
- S3 Events + Lambda for triggers
- Airflow for orchestration
- Glue for processing
- CloudWatch for monitoring

---

## Related Topics

- **[Advanced Architectures](15_advanced_architectures.md)**: Production patterns (multi-region, security)
- **[Daily Workflow](16_daily_workflow.md)**: How these patterns fit into daily operations
- **[Service Comparisons](12_service_comparisons.md)**: Choose the right services

[← Back to Main](../README.md)
