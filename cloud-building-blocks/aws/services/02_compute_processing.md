# Compute & Processing ⚡

[← Back to Main](README.md)

Raw data is just noise until you process it. These services provide the horsepower.

---

## [AWS Glue (Spark & Python Jobs)](https://aws.amazon.com/glue/)

A serverless data integration service that makes it easy to discover, prepare, and combine data.

- **Why it matters:** It manages the underlying Spark infrastructure so you can focus on your ETL logic. It also includes a "Crawler" to automatically infer schemas.
- **Common Task:** Running daily batch jobs to transform CSVs into optimized Parquet files.
- **Pricing:** $0.44/DPU-hour (Data Processing Unit = 4 vCPUs + 16GB RAM)

### ✅ When to Use (Start Simple → Scale Smartly)

1. **Serverless ETL (Start: Small → Scale)**
   - **Start Simple:** Convert small CSV to Parquet costs pennies
   - **No Infrastructure:** Zero servers to manage, auto-scales
   - **Cost Reality:** ~$0.44 per DPU-Hour (billed per second, 1 min min)
   - **Example:** A job using 10 DPUs for 30 mins = 5 DPU-Hours = ~$2.20
   - **When:** Sporadic/scheduled jobs, not continuous processing

2. **Schema Discovery (Complexity: Low)**
   - **Start Simple:** Run Glue Crawler on new S3 data
   - **Auto-Catalog:** Automatically infers schema, creates tables
   - **Why:** Save hours of manual schema definition
   - **Cost:** $0.44 per DPU-Hour (typically small crawlers run for minutes)

3. **Cost-Conscious Processing (Variable workloads)**
   - **Daily ETL:** Pay only when job runs
   - **Vs EMR:** EMR cluster costs accrue 24/7 if not terminated
   - **Decision Point:** Glue often cheaper for jobs running <12-16 hours total/day
   - **Velocity:** 2-10min startup (great for batch, not real-time)

4. **Simple First, Complex Later**
   - **Start:** Basic CSV → Parquet with Glue Studio (visual, no code)
   - **Grow:** Add Python/Spark transformations as needs evolve
   - **Scale:** Handle terabytes without architecture changes
   - **Complexity:** Gradual learning curve, not all-or-nothing

5. **Multi-Source Integration**
   - **Use Case:** Join RDS tables with S3 files daily
   - **Why Glue:** Built-in connectors vs writing custom Spark code
   - **Benefit:** Focus on logic, not connectivity
   - **Velocity:** Daily batch (not hourly/real-time)

### ❌ When NOT to Use

- **Sub-5-minute latency:** 1-5min cold start; use EMR or Lambda
- **Complex Spark tuning needed:** Limited config; use EMR for custom Spark optimization
- **Streaming data:** Glue is primarily batch (Streaming exists but EMR/Kinesis often preferred)
- **Tiny datasets (<100MB):** DPU billing minimums might be overkill; use Lambda
- **Continuous 24/7 processing:** persistent EMR cluster often cheaper per hour

### Code Example - Basic Glue Job (PySpark)

```python
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Read from S3
datasource = glueContext.create_dynamic_frame.from_catalog(
    database = "my_database",
    table_name = "raw_data"
)

# Transform
transformed = datasource.apply_mapping([
    ("id", "int", "customer_id", "int"),
    ("name", "string", "customer_name", "string")
])

# Write to S3 as Parquet
glueContext.write_dynamic_frame.from_options(
    frame = transformed,
    connection_type = "s3",
    connection_options = {"path": "s3://my-bucket/curated/customers/"},
    format = "parquet"
)

job.commit()
```

### Best Practices

- Use **Glue Crawlers** to automatically detect schema changes
- Enable **Job Bookmarks** to process only new data in incremental loads
- Use **Glue Data Catalog** as a centralized metastore
- Monitor job metrics in CloudWatch to optimize DPU allocation

---

## [Amazon EMR (Elastic MapReduce)](https://aws.amazon.com/emr/)

The industry-leading cloud big data platform for processing vast amounts of data using open-source tools such as Apache Spark, Hive, and Presto.

- **Why it matters:** Use EMR when you need deep control over your Spark configuration or need to run massive, complex clusters at scale.
- **Common Task:** Running large-scale Spark jobs, Hive queries, or Presto analytics
- **Pricing:** ~$0.096/hour for m5.xlarge + EC2 instance cost

### ✅ When to Use (When Complexity Justifies Cost)

1. **Complex Spark Tuning Required**
   - **Need:** Custom memory management, shuffle optimization
   - **Example:** Graph algorithms needing specific executor configs
   - **Why EMR:** Full control over spark-defaults.conf, JVM settings
   - **Cost:** Worth cluster management for performance-critical workloads

2. **Long-Running/Interactive Analytics (24/7 workloads)**
   - **Use Case:** Data scientists need Jupyter notebooks on live data
   - **Cost Math (Small Cluster):** 3 nodes (m5.xlarge) ≈ $0.90/hour ≈ $21/day
   - **Comparison:** Cheaper than Glue if running essentially 24/7
   - **Complexity:** Reserved instances reduce cost further (40-60%)

3. **Custom Libraries & Dependencies**
   - **Need:** TensorFlowOnSpark, custom JAR files, specific versions
   - **Why EMR:** Install any library vs Glue's limited environment
   - **Complexity:** Must manage cluster, but worth it for custom needs
   - **Example:** Legacy Hive UDFs, proprietary analytics packages

4. **Streaming Applications (Real-time velocity)**
   - **Need:** Spark Structured Streaming for <1-minute latency
   - **Why EMR:** Continuous processing vs Glue's batch orientation
   - **Cost:** Long-running cluster avoids Glue's startup latency and minimums
   - **Example:** Process IoT sensor data continuously

5. **Migration from On-Prem Hadoop**
   - **Start Simple:** Lift-and-shift existing Hadoop jobs unchanged
   - **Why EMR:** Run existing scripts without rewriting for Glue
   - **Future:** Gradually migrate to Glue Serverless as you modernize
   - **Velocity:** Immediate migration vs months rewriting

### ❌ When NOT to Use

- **Simple ETL Glue handles:** CSV→Parquet doesn't need cluster management
- **Sporadic jobs (<4 hrs/day):** Cluster spin-up/down complexity vs Glue's simplicity
- **No Spark expertise:** Steep learning curve; start with Glue's visual tools
- **Small data (<10GB):** Cluster startup overhead not justified

---

## [AWS Lambda](https://aws.amazon.com/lambda/)

Run code without thinking about servers. Pay only for the compute time you consume.

- **Why it matters:** Ideal for event-driven data engineering (e.g., "When a file drops in S3, trigger this code").
- **Common Task:** Minor data validation, light transformations, or triggering API calls.
- **Pricing:** First 1M requests free, then $0.20/1M requests + compute time

### Code Example - Lambda Function Triggered by S3

```python
import json
import boto3

s3 = boto3.client('s3')
sns = boto3.client('sns')

def lambda_handler(event, context):
    # Triggered when file lands in S3
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    print(f"Processing file: s3://{bucket}/{key}")
    
    # Example: Validate file size
    response = s3.head_object(Bucket=bucket, Key=key)
    file_size = response['ContentLength']
    
    if file_size > 100 * 1024 * 1024:  # 100MB
        sns.publish(
            TopicArn='arn:aws:sns:us-east-1:123456789:data-alerts',
            Message=f'Large file detected: {key} ({file_size} bytes)'
        )
    
    return {'statusCode': 200, 'body': json.dumps('Processing complete')}
```

---

## [AWS Batch](https://aws.amazon.com/batch/)

Fully managed batch processing at any scale.

- **Why it matters:** When you have containerized batch jobs that need to run on a schedule or be triggered.
- **Common Task:** Running Docker containers for data processing jobs

---

## Related Topics

- **[Service Comparisons](12_service_comparisons.md)**: Glue vs EMR - when to use what
- **[Performance Tuning](14_performance_tuning.md)**: Optimize Glue and EMR performance
- **[Cost Optimization](13_cost_optimization.md)**: Reduce Glue and EMR costs by 20-70%
- **[Orchestration](08_orchestration.md)**: Schedule Glue/EMR jobs with Airflow

[← Back to Main](README.md)
