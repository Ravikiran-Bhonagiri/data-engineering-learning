# Storage Services 🗄️

[← Back to Main](README.md)

Azure's foundation for data storage - from hot data to long-term archives.

---

## [Azure Blob Storage](https://azure.microsoft.com/services/storage/blobs/)

Massively scalable object storage for unstructured data.

- **Why it matters:** Foundation of Azure data lakes, like AWS S3 or GCP Cloud Storage
- **Common Task:** Store raw data files, processed Parquet, backups
- **Pricing:** $0.0184/GB/month (Hot) to $0.002/GB/month (Archive)

### ✅ When to Use (Start: GB → Scale: PB)

1. **Multi-Tier Cost Optimization (94% savings)**
   - **Hot:** $0.0184/GB/month - frequent access
   - **Cool:** $0.01/GB/month - <30 day access
   - **Archive:** $0.002/GB/month - rarely accessed
   - **Savings:** Hot→Archive = 89% reduction

2. **Data Lake Foundation**
   - **Start:** 100GB raw files = $1.84/month
   - **Scale:** Petabytes without re-architecting
   - **Integration:** Synapse, Databricks, Data Factory all read directly
   - **Why:** Pay only for storage used

3. **Lifecycle Management (Automated)**
   - **Rules:** Hot (30d) → Cool (90d) → Archive (1yr) → Delete
   - **Cost:** Automatic tiering without manual intervention
   - **Example:** Keep current month hot, archive older data

### ❌ When NOT to Use

- **Frequent small updates:** Not a database; use Cosmos DB or SQL
- **<10ms latency:** Use Redis or Cosmos DB
- **POSIX filesystem:** Use Azure Files for NFS/SMB

---

## [Data Lake Storage Gen2](https://azure.microsoft.com/services/storage/data-lake-storage/)

Hadoop-compatible hierarchical namespace on top of Blob Storage.

- **Why it matters:** Optimized for big data analytics with file/directory operations
- **Common Task:** Store data for Spark, Synapse, Databricks with folder structure
- **Pricing:** Blob Storage + $0.001-0.01/GB for hierarchical namespace

### ✅ When to Use

1. **Hadoop/Spark Workloads**
   - **Feature:** HDFS-compatible API
   - **Performance:** Atomic directory operations
   - **Cost:** Blob price + small premium for features
   - **When:** Using Databricks, Synapse Spark

2. **Fine-Grained Security (ACLs)**
   - **POSIX ACLs:** Directory/file level permissions
   - **vs Blob:** Blob only has container-level
   - **Example:** Data engineers access /raw, analysts only /curated
   - **When:** Need folder-level security

### ❌ When NOT to Use

- **Simple blob storage:** Standard Blob cheaper if no hierarchical namespace needed
- **No big data:** Overkill for simple file storage

---

## [Azure Files](https://azure.microsoft.com/services/storage/files/)

Fully managed file shares using SMB/NFS protocols.

- **Why it matters:** Shared file system for VMs and applications
- **Common Task:** Shared config files, legacy app migrations
- **Pricing:** ~$0.06/GB/month (Standard), ~$0.15/GB/month (Premium)

### ✅ When to Use

- **Shared filesystem needed:** Multiple VMs access same files
- **Lift-and-shift:** Migrate on-prem file shares
- **Windows compatibility:** SMB protocol required

### ❌ When NOT to Use

- **Object storage sufficient:** Blob cheaper ($0.018 vs $0.06/GB)
- **Big data workloads:** Use Data Lake Gen2

---

## Related Topics

- **[Synapse Analytics](05_analytics_warehousing.md)**: Query Blob/Data Lake directly
- **[Data Factory](04_data_integration.md)**: Move data to/from storage
- **[Cost Optimization](12_cost_optimization.md)**: Lifecycle policies

[← Back to Main](README.md)
