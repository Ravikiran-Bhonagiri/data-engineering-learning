# Compute & Processing ⚙️

[← Back to Main](README.md)

GCP's powerful processing engines for transforming data at scale.

---

## [Dataflow](https://cloud.google.com/dataflow)

Fully managed service for executing Apache Beam pipelines (batch and streaming).

- **Why it matters:** GCP's serverless alternative to Spark. No cluster management.
- **Common Task:** ETL pipelines, real-time stream processing from Pub/Sub
- **Pricing:** $0.056/vCPU-hour + $0.003557/GB-hour (billed per second)

### ✅ When to Use (Serverless Processing)

1. **Serverless ETL (Start: Small → Scale Automatically)**
   - **Start Simple:** Process 1GB file = ~$0.10 (2 workers × 5 min)
   - **Auto-scaling:** Scales from 1 to 1000+ workers automatically
   - **No Management:** Zero infrastructure to maintain
   - **Cost:** Pay only for actual worker time (vs Dataproc 24/7)

2. **Real-time Streaming (Sub-minute latency)**
   - **Pub/Sub → Dataflow → BigQuery:** Classic GCP streaming pattern
   - **Latency:** Seconds to process messages
   - **Cost:** Workers run continuously for streaming jobs
   - **When:** Need <1 minute end-to-end processing

3. **Apache Beam Pipelines (Portability)**
   - **Write Once:** Beam code runs on Dataflow, Spark, Flink
   - **Unified API:** Same code for batch and streaming
   - **Complexity:** Steeper learning curve than SQL
   - **Benefit:** Not locked into GCP

4. **Variable Workloads (Cost efficiency)**
   - **Daily ETL:** Run job, auto-shutdown when complete
   - **Example:** 100GB daily: 10 workers × 30min = $2.80/day
   - **vs Dataproc:** No idle cluster costs (vs $10-20/day minimum)
   - **Decision:** Dataflow for sporadic, Dataproc for 24/7

5. **Complex Transformations (Beyond SQL)**
   - **Custom Logic:** Python/Java for complex business logic
   - **Windows & Sessions:** Advanced time-based aggregations
   - **Side Inputs:** Enrich streaming data with reference data
   - **When:** SQL insufficient for transformation needs

### ❌ When NOT to Use

- **Simple SQL transformations:** BigQuery SQL cheaper and simpler
- **Spark-specific features needed:** Use Dataproc for Spark MLlib, GraphX
- **Very small files (<100MB):** Cloud Functions cheaper for simple tasks
- **Persistent clusters for development:** Dataproc better for interactive work
- **Cost-sensitive with predictable load:** Dataproc with committed use cheaper for 24/7

### Code Example - Simple Beam Pipeline

```python
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

options = PipelineOptions(
    project='my-project',
    runner='DataflowRunner',
    region='us-central1',
    temp_location='gs://my-bucket/temp'
)

with beam.Pipeline(options=options) as pipeline:
    (pipeline
     | 'Read' >> beam.io.ReadFromText('gs://my-bucket/input.csv')
     | 'Parse' >> beam.Map(lambda line: line.split(','))
     | 'Filter' >> beam.Filter(lambda row: int(row[2]) > 100)
     | 'Format' >> beam.Map(lambda row: f"{row[0]},{row[1]}")
     | 'Write' >> beam.io.WriteToText('gs://my-bucket/output'))
```

### Best Practices

- **Use Streaming Engine** for streaming jobs (better resource management)
- **Enable auto-scaling** for batch jobs (max_num_workers)
- **Use Flex RS** for non-time-sensitive batch (30% cheaper)
- **Monitor with Cloud Monitoring** for job performance
- **Partition BigQuery writes** to avoid small file issues

---

## [Dataproc](https://cloud.google.com/dataproc)

Managed Apache Spark and Hadoop service (like AWS EMR).

- **Why it matters:** When you need Spark/Hadoop ecosystem or want cluster control
- **Common Task:** Spark ML, PySpark notebooks, migrating from on-prem Hadoop
- **Pricing:** Compute Engine price + $0.010/vCPU-hour Dataproc fee

### ✅ When to Use (When You Need Spark Ecosystem)

1. **Spark-Specific Features**
   - **SparkML:** Machine learning on Spark
   - **GraphX:** Graph processing algorithms
   - **Custom Libraries:** JAR files, specific Spark versions
   - **When:** Dataflow doesn't support your use case

2. **Interactive Development (Jupyter/Zeppelin)**
   - **Notebooks:** Data scientists need interactive Spark
   - **Cost:** Cluster runs while you develop (~$0.50/hour small cluster)
   - **Ephemeral Clusters:** Spin up for session, delete after
   - **Workflow Orchestration:** Use Cloud Composer to manage

3. **Predictable 24/7 Workloads**
   - **Long-Running:** Streaming jobs or always-on clusters
   - **Committed Use:** 1yr = 37% off, 3yr = 55% off
   - **vs Dataflow:** Cheaper for continuous processing
   - **Example:** $10/day cluster with committed = $6.30/day

4. **Migrating from On-Prem**
   - **Lift-and-Shift:** Existing Spark jobs run unchanged
   - **Gradual Migration:** Modernize to Dataflow over time
   - **Compatibility:** Full Spark/Hadoop ecosystem
   - **Time-to-Value:** Immediate migration vs rewriting

### ❌ When NOT to Use

- **Simple ETL:** BigQuery SQL or Dataflow simpler
- **Sporadic jobs:** Dataflow avoids idle cluster costs
- **No Spark expertise:** Steep learning curve vs Dataflow/BigQuery
- **Serverless preference:** Dataproc requires cluster management

---

## [Cloud Functions](https://cloud.google.com/functions)

Event-driven serverless compute platform (like AWS Lambda).

- **Why it matters:** Lightweight data transformations triggered by events
- **Common Task:** Process files when uploaded to Cloud Storage
- **Pricing:** $0.40/million invocations + $0.0000025/GB-sec

### ✅ When to Use

- **Event-Driven:** Trigger on Cloud Storage, Pub/Sub, HTTP
- **Small transformations:** <10MB files, simple logic
- **Cost:** First 2 million free, then pennies per million
- **Velocity:** Millisecond startup

### ❌ When NOT to Use

- **Large files (>10MB):** Use Dataflow or Dataproc
- **Long processing (>60 min):** Cloud Functions gen2 has 60min timeout; use Dataflow for longer jobs
- **Complex pipelines:** Use Dataflow for multi-step ETL

---

## Related Topics

- **[BigQuery](05_analytics_warehousing.md)**: Dataflow writes results here
- **[Pub/Sub](06_streaming_messaging.md)**: Dataflow streaming source
- **[Cloud Storage](01_storage_services.md)**: Input/output for all processing
- **[Service Comparisons](12_service_comparisons.md)**: Dataflow vs Dataproc

[← Back to Main](README.md)
