# Databricks Interview Questions Master List (100+)

**Ratio:** ~20% Simple | ~40% Medium | ~40% Hard

---

## 🟢 Simple (Basics - 20 Questions)

1.  **What is Databricks?**
    *   Unified data platform built on Spark by Spark founders.
2.  **What is the Lakehouse?**
    *   Architecture combining Warehouse (Reliability) and Lake (Flexibility).
3.  **What is Delta Lake?**
    *   Open storage layer bringing ACID transactions to Parquet data.
4.  **What is a Databricks Notebook?**
    *   Collaborative code editor (multi-language support).
5.  **What is the "Control Plane" vs "Data Plane"?**
    *   Control (UI, Notebooks) managed by Databricks (Backend). Data (Clusters, S3) in your AWS/Azure account.
6.  **What kind of clusters exist?**
    *   All-Purpose (Interactive), Job (Automated), SQL Warehouse (Serverless).
7.  **What is DBFS?**
    *   Databricks File System. Abstraction over S3/Blob.
8.  **What are "Widgets"?**
    *   Notebook parameters (inputs).
9.  **What is `dbutils`?**
    *   Utility library (fs, secrets, widgets, notebook callbacks).
10. **What is a "Job"?**
    *   Workflow orchestrator for running tasks.
11. **What is Unity Catalog?**
    *   Centralized governance (ACLs) across workspaces.
12. **What is the `hive_metastore` (legacy)?**
    *   Old workspace-local catalog.
13. **What is Parquet?**
    *   Columnar file format used under the hood by Delta.
14. **What is a "Mount Point"?**
    *   Attaching S3 bucket to DBFS (Deprecated for External Locations).
15. **What is DBU?**
    *   Databricks Unit. The billing currency.
16. **What is Databricks SQL?**
    *   Serverless warehouse service for BI/Analysts.
17. **What is the "Catalog Explorer"?**
    *   UI to browse data assets.
18. **What is a Repository (Databricks Git Folder)?**
    *   Syncing code with GitHub/GitLab.
19. **What is MLflow?**
    *   Machine Learning lifecycle tool (Tracking, Registry).
20. **Can you install Python Libraries?**
    *   Yes, via PyPI, Maven, or CRAN.

---

## 🟡 Medium (Development & Delta - 40 Questions)

21. **Explain the functionality of `OPTIMIZE`.**
    *   Compacts small files into larger ones (1GB).
22. **Explain the functionality of `ZORDER`.**
    *   Co-locates related data in same files to skip efficient data skipping.
23. **What is Time Travel?**
    *   Querying older snapshots of data. `VERSION AS OF`.
24. **How does `VACUUM` work?**
    *   Permanently deletes old data files no longer referenced by recent logs. Note: breaks Time Travel.
25. **What is Auto Loader (`cloudFiles`)?**
    *   Scaling file ingestion using file notification service (SQS).
26. **What is Schema Evolution in Auto Loader?**
    *   `cloudFiles.inferColumnTypes`, `addNewColumns` mode.
27. **Explain `COPY INTO`.**
    *   SQL command for idempotent batch loading.
28. **Delta Lake: Merge-On-Read vs Copy-On-Write.**
    *   CoW: Rewrite file on update. MoR: Write deletion vector.
29. **What is Photon?**
    *   C++ High performance engine rewrote from scratch.
30. **What is a "Secret Scope"?**
    *   Vault for API keys. `dbutils.secrets.get()`.
31. **Job Cluster vs Interactive Cluster costs?**
    *   Jobs are significantly cheaper (~50%). Always use Job clusters for prod.
32. **What allows ACID in Delta?**
    *   The `_delta_log`. Atomic commit protocol.
33. **Explain `MERGE` statement.**
    *   SQL Upsert. `WHEN MATCHED UPDATE... WHEN NOT MATCHED INSERT`.
34. **What is `dlt` (Delta Live Tables)?**
    *   Declarative Pipeline Framework (Python/SQL).
35. **DLT: Expectation vs Expectation or Drop?**
    *   Expectation: Alert only. Drop: Remove bad row.
36. **Explain "Identity Federation".**
    *   Account-level users assigned to workspaces.
37. **What is an "External Location" (UC)?**
    *   Secure definition of Storage credential + S3 path.
38. **What acts as a "Volume" in UC?**
    *   Object for unstructured data (images, PDFs).
39. **What is Cluster Policy?**
    *   Governance to enforce cost controls (e.g., set Max DBU, enforce Tags).
40. **How does Databricks handle PII?**
    *   Dynamic Views or Row Filters/Column Masks in UC.
41. **What is Databricks Connect?**
    *   Dev tool. Run IDE code locally, execute on Cluster.
42. **What is a "Service Principal"?**
    *   Robot identity for running Jobs securely.
43. **How to share data externally?**
    *   Delta Sharing. Open protocol.
44. **What is a "Table Constraint" in Delta?**
    *   `CHECK` constraint or `NOT NULL`.
45. **What is the "Partner Connect"?**
    *   Quick integrations (Fivetran, Tableau).
46. **What is "Liquid Clustering"?**
    *   New replacement for ZORDER. Dynamic clustering without rewriting entire table.
47. **Serverless Compute availability?**
    *   SQL Warehouses, DLT, and Model Serving are Serverless.
48. **How to optimize a Slow Join?**
    *   Broadcast, Skew Hint, or ZORDER by Join Keys.
49. **What is "Data Skipping"?**
    *   Using Min/Max stats in Parquet footer to ignore non-relevant files.
50. **What describes Delta History?**
    *   `DESCRIBE HISTORY table`.
51. **Can you read Delta tables with other engines?**
    *   Yes, native readers in Trino, Snowflake, Athena.
52. **Difference between `managed` and `external` table?**
    *   Managed: DB owns storage cycle. External: You own storage.
53. **What is `CREATE TABLE AS SELECT` (CTAS)?**
    *   Infers schema and writes data in one go.
54. **Handling "Small Files Problem"?**
    *    auto-optimize (write), OPTIMIZE (read).
55. **What is "Change Data Feed" (CDF)?**
    *   Delta feature recording row-level changes (insert/update/delete) for downstream consumption.
56. **DLT Continuous vs Triggered?**
    *   Continuous: Always running (low latency). Triggered: Batch.
57. **How to parameterize a Job?**
    *   Task parameters passed to `dbutils.widgets`.
58. **What is `run_if` in Jobs?**
    *   Conditional execution (only run if previous succeeded).
59. **Is Databricks Open Source?**
    *   No. Spark/Delta are, Databricks "Platform" is proprietary.
60. **Difference: Standard vs Premium Workspace?**
    *   Premium needed for RBAC, Security, SQL Warehouses.

---

## 🔴 Hard (Architecture & Scenario - 40 Questions)

61. **Scenario: Job fails with "ConcurrentAppendException".**
    *   Multiple writers adding to same partition. Fix: Partition data or retry logic.
62. **Optimization: "Cloud Fetch" (Databricks SQL).**
    *   Large results fetched directly from S3 via presigned URLs (High throughput) instead of thru Driver.
63. **Explain the 3-level Namespace.**
    *   `catalog.schema.table`. Required for Unity Catalog.
64. **Disaster Recovery (DR) Strategy?**
    *   Clone tables to secondary region. Sync Metastore.
65. **Networking: What is Private Link?**
    *   Secure connectivity without Public Internet between Control Plane and Data Plane.
66. **Troubleshooting Slowness: "Driver is overloaded".**
    *   Too much `collect()`. Single threaded code. Move logic to UDF/Pandas UDF.
67. **Explain cost optimization with "Spot Instances".**
    *   Use Spot for Executors (stateless). On-Demand on Driver (stateful).
68. **How to implement CI/CD for Databricks?**
    *   Databricks Asset Bundles (DABs) or Terraform.
69. **DLT: Implementing SCD Type 2.**
    *   `dlt.apply_changes(stored_as_scd_type=2)`.
70. **Handling "Schema Drift" in Production pipelines.**
    *   Auto Loader `schemaEvolutionMode`.
71. **What is the "Isolation Level" of Delta?**
    *   Serializable (Write). Snapshot (Read).
72. **Explain "V-Order".**
    *   Write-time optimization in Photon (sorting for compression).
73. **Migration: Hive to Unity Catalog strategy.**
    *   `SYNC` command or `Deep Clone` or `Upgrade` wizard.
74. **Vector Search?**
    *   New feature storing embeddings for LLM RAG apps.
75. **How does Databricks handle "Eventually Consistent" S3?**
    *   S3 is now strong consistent. Before, used DynamoDB lock (Delta).
76. **Explain "Materialized Views" in Databricks SQL.**
    *   Precomputed results managed by DLT engine under the hood. Incremental updates.
77. **Lakehouse Federation?**
    *   Querying external DBs (Postgres, Snowflake) without moving data. `CREATE FOREIGN CATALOG`.
78. **What is "Clean Rooms"?**
    *   Secure data sharing environment without exposing PII.
79. **Implementing "Quality Gates" (WAP pattern).**
    *   Write-Audit-Publish. Write to stage branch, verify, merge to prod.
80. **Feature Store Integration.**
    *   Versioning ML features. Point-in-time correctness joins.
81. **GraphFrames usage.**
    *   Network analysis (PageRank) on DF.
82. **Explain `spark.databricks.io.cache.enabled`.**
    *   Delta Cache (Disk Caching on NVMe SSDs). Local copy of remote data.
83. **Difference: Spark Cache vs Delta Cache.**
    *   Spark Cache: RAM/Heap (Row format). Delta Cache: SSD (Blob format).
84. **Debugging "Executor Lost".**
    *   OOM? Spot Interruption? Network error? Check Instance logs.
85. **What is "Predictive Optimization"?**
    *   AI enabling `OPTIMIZE`/`VACUUM` automatically.
86. **Streaming deduplication strategy.**
    *   `dropDuplicates(["id"])` with Watermark.
87. **Explain "Bloom Filter Indexes" in Delta.**
    *   File skipping for high cardinality not-sorted columns (UUID).
88. **How to monitor Costs by Tag?**
    *   Cluster tags propagate to Cloud Bill (AWS Cost Explorer).
89. **Cluster Init Scripts vs Docker Container?**
    *   Docker is immutable/faster startup. Init scripts flexible but brittle.
90. **Can you modify the Delta Log manually?**
    *   No. Corrupts the table.
91. **What is "Deep Learning" distributor?**
    *   running TorchDistributor to parallelize PyTorch on Spark.
92. **Handling small file explosion in Streaming.**
    *   `Trigger.AvailableNow` (Batching) or `optimizeWrite`.
93. **What is the "System Tables" catalog?**
    *   `system.billing`, `system.access`. Metadata analysis.
94. **Explain "Volumes" vs "Mounts".**
    *   Volumes = UC Governed. Mounts = Workspace Legacy.
95. **Using "File Format" options.**
    *   `maxRecordsPerFile` used for splitting output.
96. **Explain "Reprocess Data" in DLT.**
    *   Full Refresh.
97. **Model Serving Architecture.**
    *   Serverless containers exposing REST endpoint.
98. **LLM Integration (Dolly/Mosaic).**
    *   Training foundation models on Databricks.
99. **Databricks Assistant.**
    *   AI coding companion in notebook.
100. **Future of Databricks?**
    *   Data Intelligence Platform (DI Platform).
