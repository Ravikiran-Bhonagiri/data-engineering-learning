# Service Comparison Guide 🤔

[← Back to Main](../README.md)

Making the right choice is half the battle. Here's when to use what.

---

## Glue vs EMR: When to use what?

| Factor | AWS Glue | Amazon EMR |
|--------|----------|------------|
| **Use When** | Simple ETL, serverless needs | Complex Spark tuning, custom libraries |
| **Complexity** | Low - fully managed | Medium - you manage cluster |
| **Cost Model** | Pay per job (DPU-hours) | Pay per cluster uptime |
| **Flexibility** | Limited Spark config | Full control over Spark/Hadoop |
| **Best For** | Standard transformations | ML pipelines, iterative algorithms |

**Decision Guide:**
- Start with Glue for most ETL workloads
- Move to EMR if you need custom Spark jars or deep configuration control

---

## Athena vs Redshift: When to use what?

| Factor | Amazon Athena | Amazon Redshift |
|--------|---------------|-----------------|
| **Use When** | Ad-hoc queries, exploration | Repeated queries, BI dashboards |
| **Storage** | Data stays in S3 | Data loaded into Redshift |
| **Performance** | Good for infrequent queries | Optimized for frequent queries |
| **Cost Model** | Pay per TB scanned | Pay for cluster (even when idle) |
| **Best For** | Data scientists, analysts | Production BI workloads |

**Decision Guide:**
- Use Athena for exploratory work and ad-hoc analysis
- Use Redshift when you have predictable, frequent query patterns

---

## Kinesis Streams vs Firehose

| Factor | Kinesis Data Streams | Kinesis Data Firehose |
|--------|---------------------|----------------------|
| **Use When** | Need custom processing | Simple S3/Redshift delivery |
| **Consumers** | Multiple custom consumers | Pre-built destinations only |
| **Latency** | Real-time(milliseconds) | Near real-time (60s+ buffering) |
| **Complexity** | Higher - you write consumers | Lower - fully managed |

**Decision Guide:**
- Use Firehose for simple "ingest to S3" workloads
- Use Streams when you need real-time processing or multiple consumers

---

## Related Topics

- **[Cost Optimization](13_cost_optimization.md)**: Make cost-effective choices
- **[Architecture Patterns](11_architecture_patterns.md)**: See services in context
- **[Daily Workflow](16_daily_workflow.md)**: Quick reference table

[← Back to Main](../README.md)
