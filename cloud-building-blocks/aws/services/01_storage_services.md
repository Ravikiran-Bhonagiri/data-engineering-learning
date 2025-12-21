# Storage Services 🏗️

[← Back to Main](README.md)

Every data pipeline starts and ends with storage. In AWS, the "Data Lake" architecture is built on top of these services.

---

## [Amazon S3 (Simple Storage Service)](https://aws.amazon.com/s3/)

The "Super Glue" of AWS. It's an object storage service offering industry-leading scalability, data availability, security, and performance.

- **Why it matters:** It is the primary storage for Data Lakes. Almost every other service integrates with it.
- **Common Task:** Storing raw landing data, transformed Parquet files, and final curated datasets.
- **Pricing:** ~$0.023/GB/month for Standard storage, with cheaper tiers for infrequent access

### ✅ When to Use (Start Simple → Scale Up)

1. **Any Size Data Lake (Start: 100GB → Scale: 500PB)**
   - **Start Simple:** Store daily CSV reports (100GB) - $2.30/month
   - **Scale Up:** Grow to petabyte data lake as business grows
   - **Why:** Pay only for what you use, no upfront commitment
   - **Velocity:** Batch ingestion (hourly/daily), not real-time

2. **Cost-Effective Archival (Any volume, infrequent access)**
   - **Start Simple:** Archive last year's data (1TB) to Glacier - $4/month
   - **Complexity:** Set lifecycle policy in 5 minutes, fully automated
   - **Why:** 80% cost savings vs keeping in standard storage
   - **When:** Access data <1x per month

3. **Decouple Storage from Compute**
   - **Start Simple:** Store 10TB Parquet files, query with Athena as needed
   - **Cost:** Pay $5 per TB scanned vs $1,000+/month for Redshift cluster
   - **Complexity:** No servers to manage, instant scalability
   - **When:** Sporadic analytics (not daily dashboard queries)

4. **Multi-Tool Integration Hub**
   - **Start Simple:** Land all data in S3, process with different tools later
   - **Why:** S3 integrates with 100+ AWS services (Athena, Glue, EMR, Redshift)
   - **Flexibility:** Change analytics tools without migrating data
   - **Future-proof:** Start with Athena, add Redshift if query frequency grows

5. **Velocity-Based Tiering (Right-size for access patterns)**
   - **Hot Data:** Standard storage for last 30 days - frequent access
   - **Warm Data:** Intelligent-Tiering for 31-90 days - occasional access
   - **Cold Data:** Glacier for 90+ days - rare access
   - **Cost Impact:** $23/TB/month → $4/TB/month as data ages

### ❌ When NOT to Use

- **Millisecond latency needed:** S3 GET ~100ms; use DynamoDB for <10ms
- **Frequent small writes (<1KB):** Minimum charge per request; use database for frequent tiny updates
- **POSIX file locking:** Applications needing shared write access; use EFS
- **Transactional updates:** S3 is object store, not database; use RDS for ACID
- **Cost for tiny datasets (<10GB):** S3 minimum billing can exceed database costs for very small data

### Code Example - Upload and Download with boto3

```python
import boto3

s3 = boto3.client('s3')

# Upload a file
s3.upload_file('local_data.csv', 'my-data-lake', 'raw/2024/data.csv')

# Download a file
s3.download_file('my-data-lake', 'raw/2024/data.csv', 'downloaded_data.csv')

# List objects in a bucket
response = s3.list_objects_v2(Bucket='my-data-lake', Prefix='raw/')
for obj in response.get('Contents', []):
    print(obj['Key'])
```

### Best Practices

- Use **S3 Lifecycle Policies** to automatically move older data to cheaper storage tiers (Glacier)
- Organize data using a clear prefix structure: `s3://bucket/environment/layer/domain/year/month/day/`
- Enable **versioning** for critical datasets to prevent accidental deletions
- Use **S3 Event Notifications** to trigger Lambda functions or send messages to SNS/SQS
- Partition data by date or logical keys for better query performance with Athena

---

## [Amazon S3 Glacier](https://aws.amazon.com/s3/glacier/)

Low-cost storage for data archiving and long-term backup.

- **Why it matters:** Perfect for regulatory data that you must keep for years but rarely access.
- **Common Task:** Archiving "Cold" data from your S3 buckets.
- **Pricing:** ~$0.004/GB/month (5x cheaper than S3 Standard)

---

## [Amazon EFS (Elastic File System)](https://aws.amazon.com/efs/)

A simple, serverless, set-and-forget elastic file system.

- **Why it matters:** Useful when you need a shared file system across multiple EC2 instances or Lambda functions (e.g., sharing a library or model).
- **Pricing:** ~$0.30/GB/month, autoscaling based on usage

---

## Related Topics

- **[Cost Optimization](13_cost_optimization.md)**: S3 lifecycle policies and storage tiering strategies
- **[Analytics & Querying](05_analytics_querying.md)**: Query S3 data with Athena
- **[Compute & Processing](02_compute_processing.md)**: Process files from S3 with Glue/Lambda

[← Back to Main](README.md)
