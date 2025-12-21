# Storage Services 🗄️

[← Back to Main](README.md)

GCP's foundation for data storage - object storage and file systems.

---

## [Cloud Storage](https://cloud.google.com/storage)

Object storage service for storing and accessing data on Google Cloud (equivalent to AWS S3).

- **Why it matters:** Foundation of GCP data lakes. BigQuery, Dataflow, Dataproc all read/write here.
- **Common Task:** Storing raw data, processed Parquet files, exports from BigQuery
- **Pricing:** $0.020/GB/month (Standard), cheaper tiers for infrequent access

### ✅ When to Use (Start Simple → Scale Up)

1. **Data Lake Foundation (Start: 10GB → Scale: Petabytes)**
   - **Start Simple:** Store daily CSVs (100GB) = $2/month
   - **Scale:** Grow to petabytes as needed
   - **Why:** Pay only for storage used, no provisioning
   - **Integration:** BigQuery external tables, Dataflow I/O

2. **Cost-Optimized Storage Tiers**
   - **Standard:** $0.020/GB/month - frequently accessed data
   - **Nearline:** $0.010/GB/month - access <1x/month
   - **Coldline:** $0.004/GB/month - access <1x/quarter
   - **Archive:** $0.0012/GB/month - access <1x/year
   - **Decision:** Move old data to save 94% (Standard → Archive)

3. **BigQuery Integration (Decouple storage/compute)**
   - **External Tables:** Query Cloud Storage files directly
   - **Cost:** Storage $0.020/GB + query $6.25/TB vs loading into BigQuery
   - **When:** Infrequently queried data or mixed formats
   - **Flexibility:** Change query tools without moving data

4. **Multi-Regional for HA (Global access)**
   - **Multi-Region:** $0.026/GB/month for 99.95% SLA
   - **Dual-Region:** $0.026/GB/month for specific region pairs
   - **Single-Region:** $0.020/GB/month for local access
   - **Decision:** Multi-region for critical data, single for cost

5. **Lifecycle Management (Automated tiering)**
   - **Auto-transition:** Standard (30d) → Nearline (90d) → Archive
   - **Cost savings:** 50-94% for aging data
   - **Complexity:** Set once, fully automated
   - **Example:** Keep hot data 30 days, archive rest

### ❌ When NOT to Use

- **Millisecond latency:** Cloud Storage has ~50-100ms latency; use Bigtable for <10ms
- **Frequent small updates:** Not a database; use Firestore or Cloud SQL for transactional updates
- **POSIX filesystem:** For NFS/file locking needs, use Filestore
- **Structured analytics:** Load into BigQuery for better performance than external tables
- **Strong transactional guarantees:** Use Cloud SQL or Firestore for ACID compliance

### Code Example - Upload and Download

```python
from google.cloud import storage

client = storage.Client()

# Upload file
bucket = client.bucket('my-data-lake')
blob = bucket.blob('raw/2024/data.csv')
blob.upload_from_filename('local_data.csv')

# Download file
blob.download_to_filename('downloaded_data.csv')

# List objects
for blob in bucket.list_blobs(prefix='raw/'):
    print(f"{blob.name}: {blob.size} bytes")

# Set lifecycle rule
bucket.add_lifecycle_delete_rule(age=365)  # Delete after 1 year
bucket.patch()
```

### Best Practices

- **Use regional buckets** for compute in same region (free egress)
- **Organize with prefixes:** `gs://bucket/env/layer/domain/date/`
- **Enable versioning** for critical datasets
- **Use signed URLs** for temporary access (no auth needed)
- **Parallel uploads** for large files (gsutil -m or parallel composite uploads)
- **Monitor with Cloud Monitoring** for access patterns

---

## [Filestore](https://cloud.google.com/filestore)

Managed NFS file storage for applications requiring a filesystem interface.

- **Why it matters:** When you need shared file access across VMs (unlike Cloud Storage)
- **Common Task:** Shared storage for machine learning training data, legacy app migrations
- **Pricing:** ~$0.20/GB/month (Basic tier)

### ✅ When to Use

- **Shared filesystem needed:** Multiple VMs accessing same files
- **POSIX compliance required:** Applications needing file locking, permissions
- **Legacy app migration:** Lift-and-shift apps expecting NFS
- **ML training:** Shared dataset access across training nodes

### ❌ When NOT to Use

- **Object storage sufficient:** Use Cloud Storage ($0.020/GB vs $0.20/GB)
- **Structured data:** Use BigQuery or Databases
- **Serverless workloads:** Cloud Storage integrates better with Cloud Functions, Dataflow

---

## Related Topics

- **[BigQuery](05_analytics_warehousing.md)**: External tables on Cloud Storage
- **[Dataflow](02_compute_processing.md)**: Read/write Cloud Storage
- **[Cost Optimization](13_cost_optimization.md)**: Lifecycle policies, storage classes

[← Back to Main](README.md)
