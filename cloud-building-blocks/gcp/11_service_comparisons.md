# Service Comparisons 🔍

[← Back to Main](README.md)

Clear, grounded comparisons to help you pick the right GCP service for your needs.

---

## BigQuery vs Cloud SQL

**The Golden Rule:** BigQuery for analytics (OLAP), Cloud SQL for transactions (OLTP).

| Factor | BigQuery | Cloud SQL |
|--------|----------|-----------|
| **Use Case** | Analytics, reporting, data warehouse | Application backend, transactions |
| **Model** | Serverless, columnar storage | Managed instances, row storage |
| **Pricing** | $6.25/TB scanned (on-demand) | $23-820/month (instance-based) |
| **Scale** | Petabytes automatically | Up to ~10TB (migrate to Spanner after) |
| **Query Pattern** | Ad-hoc SELECT, aggregations | INSERT/UPDATE/DELETE, point queries |
| **Latency** | 1-30 seconds | <100ms |
| **Ideal for** | Business intelligence, ML, reporting | E-commerce, user accounts, orders |

**Decision:**
- Cloud SQL if your app needs ACID transactions
- BigQuery if you're running SELECT queries on large datasets

---

## Dataflow vs Dataproc

**The Golden Rule:** Dataflow for serverless/streaming, Dataproc for Spark ecosystem.

| Factor | Dataflow | Dataproc |
|--------|----------|----------|
| **Framework** | Apache Beam (unified) | Spark, Hadoop, Hive, Presto |
| **Management** | Fully serverless | Managed clusters |
| **Pricing** | $0.056/vCPU-hr (pay per job) | Compute + $0.010/vCPU-hr |
| **Startup Time** | 2-5 minutes | 90 seconds - 5 minutes |
| **Best For** | Variable workloads, streaming | 24/7 workloads, Spark ML |
| **Learning Curve** | Beam API (moderate) | Spark (steep) |
| **Ideal for** | ETL, streaming Pub/Sub→BQ | Interactive notebooks, SparkML |

**Decision:**
- Dataflow for sporadic jobs (<8 hrs/day)
- Dataproc for persistent clusters or Spark-specific features
- Dataflow for streaming (<1 min latency)

**Cost Example:**
- Daily 1-hour ETL job: Dataflow $2/day vs Dataproc $10/day (24/7)
- 24/7 streaming: Dataproc with committed use < Dataflow

---

## Cloud Composer vs Workflows

**The Golden Rule:** Workflows for simple chains, Composer for complex DAGs.

| Factor | Workflows | Cloud Composer |
|--------|-----------|----------------|
| **Complexity** | Simple, linear (2-10 steps) | Complex DAGs (50+ tasks) |
| **Language** | YAML | Python (Airflow) |
| **Pricing** | $0.01/1000 steps (pennies) | ~$300/month minimum |
| **UI** | Basic | Full Airflow web UI |
| **Team Collab** | Limited | Full team dashboard |
| **Use Case** | Event-driven automation | Multi-team orchestration |

**Decision:**
- Workflows if workflow < 10 steps and cost-sensitive
- Composer when team needs Airflow UI and complex dependencies
- **Crossover:** When workflows hit 20+ steps or need team visibility

---

## Cloud Storage vs Filestore

**The Golden Rule:** Cloud Storage for 99% of cases, Filestore only for NFS needs.

| Factor | Cloud Storage | Filestore |
|--------|---------------|-----------|
| **Type** | Object storage | NFS file storage |
| **Pricing** | $0.020/GB/month | $0.20/GB/month (10x more) |
| **Access** | HTTP APIs, gsutil | NFS mount |
| **Use Case** | Data lakes, BigQuery source | VM shared storage |
| **POSIX** | No | Yes (file locking) |

**Decision:**
- Cloud Storage unless you specifically need NFS/POSIX
- FileStore only for legacy apps requiring filesystem

---

## On-Demand vs Flat-Rate BigQuery

**The Golden Rule:** On-demand until monthly spend > $2,000.

| Factor | On-Demand | Flat-Rate (Slots) |
|--------|-----------|-------------------|
| **Pricing** | $6.25/TB scanned | $0.04/slot-hour (~$2,880/month for 100 slots) |
| **Best For** | Variable, unpredictable queries | Consistent, heavy usage |
| **Trigger** | <320TB/month scanned | >320TB/month scanned |
| **Pros** | No commitment, true pay-per-use | Predictable cost, faster queries |
| **Cons** | Can spike unexpectedly | Minimum $2,880 commitment |

**Decision:**
- Start on-demand
- Monitor monthly scanned data
- Switch to slots when consistently > $2,000/month

---

## GCP vs AWS (Quick Reference)

| GCP Service | AWS Equivalent | Key Difference |
|-------------|----------------|----------------|
| Cloud Storage | S3 | Similar pricing, same features |
| BigQuery | Redshift | BQ serverless, Redshift cluster-based |
| Dataflow | Glue | Dataflow uses Beam, Glue uses Spark |
| Dataproc | EMR | Very similar (Spark/Hadoop) |
| Pub/Sub | Kinesis + SNS | Pub/Sub combines both |
| Cloud SQL | RDS | Very similar pricing/features |
| Composer | MWAA | Both managed Airflow ($300/mo) |
| Cloud Functions | Lambda | Similar serverless functions |

**Philosophy Difference:**
- **GCP:** Serverless-first (BigQuery, Dataflow push this hard)
- **AWS:** More options, more complexity
- **Pricing:** GCP often simpler/clearer

---

[← Back to Main](README.md)
