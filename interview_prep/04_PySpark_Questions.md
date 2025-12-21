# PySpark Interview Questions Master List (100+)

**Ratio:** ~20% Simple | ~40% Medium | ~40% Hard

---

## 🟢 Simple (Basics - 20 Questions)

1.  **What is Apache Spark?**
    *   Unified analytics engine for big data processing (Speed, Ease of use).
2.  **What is PySpark?**
    *   Python API for Spark.
3.  **What is an RDD?**
    *   Resilient Distributed Dataset. Immutable, Partitioned collection.
4.  **What is a DataFrame?**
    *   Distributed collection with named columns (Schema).
5.  **Difference: RDD vs DataFrame?**
    *   DF has Optimization (Catalyst) and Schema. RDD is low level.
6.  **What is Lazy Evaluation?**
    *   Execution is delayed until an Action is called.
7.  **What is a Transformation?**
    *   Operation returning a new RDD/DF (Map, Filter). Lazy.
8.  **What is an Action?**
    *   Operation triggering execution (Collect, Count, Write).
9.  **What is the Driver?**
    *   Master process. Runs `main()`, creates SparkContext.
10. **What is an Executor?**
    *   Worker process. Runs tasks, stores data.
11. **What is a Partition?**
    *   Atomic chunk of data distribution.
12. **What is `spark-submit`?**
    *   CLI script to launch applications.
13. **What is `SparkSession`?**
    *   Entry point to programming Spark with DataFrames (Spark 2.0+).
14. **What is `SparkContext`?**
    *   Main entry point for RDD API.
15. **What formats does Spark support?**
    *   CSV, JSON, Parquet, ORC, Avro, Text, JDBC.
16. **What is Filter?**
    *   Transformation to select rows.
17. **What is Select?**
    *   Transformation to pick columns.
18. **What is `printSchema()`?**
    *   Prints tree view of structure.
19. **What is `show()`?**
    *   Action to print top N rows to console.
20. **Can Spark modify a file in place?**
    *   No. HDFS/S3 are immutable. Writes new files.

---

## 🟡 Medium (Optimization & API - 40 Questions)

21. **Explain `Narrow` vs `Wide` dependencies.**
    *   **Narrow:** No shuffle (Map, Filter). Partition -> Partition.
    *   **Wide:** Shuffle (Group By, Join). Partition -> Many Partitions.
22. **What is a Shuffle?**
    *   Redistribution of data across cluster. Costly (Disk/Network).
23. **What is Broadcasting?**
    *   Sending small table to all nodes to convert Join to Map-Side lookups.
24. **When does a Broadcast Join fail?**
    *   If table > Driver Memory or > Torrent Limit.
25. **What is `repartition()`?**
    *   Full shuffle to target N partitions. Balances data.
26. **What is `coalesce()`?**
    *   Decreases partitions without full shuffle (merges local).
27. **What is Caching?**
    *   `df.cache()` stores data in memory for reuse.
28. **Storage Levels explained.**
    *   Memory_Only, Memory_And_Disk, Disk_Only.
29. **What is `catalog` in Spark?**
    *   Interface to metastore (list tables, drop views).
30. **Explain `withColumn`.**
    *   Adds or replaces a column.
31. **How to rename a column?**
    *   `withColumnRenamed`.
32. **What is a UDF?**
    *   User Defined Function (Python function wrapped for Spark).
33. **Why are Python UDFs slow?**
    *   Serialization between JVM and Python process (Pickling).
34. **What is a Pandas UDF (Vectorized UDF)?**
    *   Uses Apache Arrow for low-overhead transfer. Much faster.
35. **What is Schema Evolution?**
    *   Ability to handle changing file structures (adding cols).
36. **Explain `explain()` method.**
    *   Shows the Logical and Physical plans.
37. **What represents `null` in PySpark?**
    *   `None` (Python) or `null` (SQL/Column).
38. **How to handle NULLs?**
    *   `df.fillna()`, `df.dropna()`.
39. **What is `groupBy`?**
    *   Wide transformation causing Shuffle.
40. **Difference: `count()` vs `approx_distinct_count()`?**
    *   Precision vs Speed.
41. **What is `spark.sql.shuffle.partitions`?**
    *   Config controlling number of partitions for joins/aggs (Default 200).
42. **What are Accumulators used for?**
    *   Global counters (Write-only for executors). Debugging.
43. **What are Broadcast Variables?**
    *   Read-only shared variables cached on workers (Lookup maps).
44. **What is Structured Streaming?**
    *   Stream processing API based on DataFrames (Micro-batch).
45. **What is a Window Function?**
    *   `Window.partitionBy().orderBy()`.
46. **How to remove duplicates?**
    *   `dropDuplicates()`.
47. **What is `explode`?**
    *   Converts Array column into multiple rows.
48. **Difference: `sort` vs `orderBy`?**
    *   Synonyms in PySpark.
49. **What is `limit`?**
    *   Returns new DataFrame with N rows. Transformation.
50. **What is `collect`?**
    *   Returns *all* data to Driver as a list. (Danger: OOM).
51. **How to write code to read JDBC?**
    *   `spark.read.format("jdbc").option(...)`.
52. **What is Data Skew?**
    *   Uneven distribution of keys. One task takes forever.
53. **How to detect Skew?**
    *   Spark UI -> Executor tab (Task duration variance).
54. **What is Salting?**
    *   Adding random prefix to keys to split skewed partitions.
55. **Dynamic Allocation?**
    *   Scaling executors up/down based on load.
56. **What is `persist` vs `cache`?**
    *   Cache is shorthand for Persist(Memory_Only). persist takes args.
57. **How does Spark handle JSON?**
    *   Scans whole file to infer schema (Expensive) or specify schema.
58. **Explain Aggregate `agg()` function.**
    *   Computes summaries (min, max, avg) after groupBy.
59. **Pivot in Spark?**
    *   `groupBy().pivot().agg()`. Expensive.
60. **Reading complex XML?**
    *   Databricks/spark-xml library usage.

---

## 🔴 Hard (Internals & Tuning - 40 Questions)

61. **Explain the Catalyst Optimizer.**
    *   Logical Plan -> Optimized Logical -> Physical Plans -> Cost Model -> Selected Plan.
62. **What is Tungsten?**
    *   Backend engine dealing with Memory Management (Off-heap) and Code Gen (WSCG).
63. **Whole-Stage Code Generation (WSCG)?**
    *   Collapsing multiple operators (filter + map) into single Java function loop.
64. **Explain Adaptive Query Execution (AQE).**
    *   Optimizes plan at runtime based on finished stage stats. Coalesces partitions, fixes skew, converts SortMerge to Broadcast.
65. **Memory Management (Unified Memory Manager).**
    *   Execution vs Storage Memory regions.
66. **What is `spark.driver.memory`?**
    *   Heap size for Driver.
67. **Garbage Collection (GC) Tuning.**
    *   G1GC usage. Issues with full GC stopping the world.
68. **Barrier Execution Mode?**
    *   For ML (Deep Learning). All tasks must start together.
69. **Optimizing SortMergeJoin.**
    *   Bucketing (`bucketBy`). Sorts data once on write. Joins skip shuffle/sort.
70. **Handling Small Files Problem.**
    *   `coalesce` before write. `maxRecordsPerFile`. Use Delta `OPTIMIZE`.
71. **Speculative Execution.**
    *   Relaunching slow tasks.
72. **Connect vs Standard Architecture (Spark Connect).**
    *   Decoupled client-server API (Spark 3.4). Allows thin client.
73. **Resource Managers (YARN vs K8s).**
    *   YARN (Container allocation). K8s (Pods).
74. **Serialization: Java vs Kyro.**
    *   Kyro is faster/compact. Default in modern Spark.
75. **Partition Pruning.**
    *   Skipping file reads based on Filter values matching Partition keys.
76. **Predicate Pushdown.**
    *   Pushing filter to the source (Parquet/JDBC) to reduce I/O.
77. **Vectorized Reader.**
    *   Reading batches of column values (Parquet/ORC) directly into memory.
78. **Handling OOM on Driver.**
    *   Reduce `collect`. Increase broadcast threshold? No, decrease it. Increase driver memory.
79. **Handling OOM on Executor.**
    *   Skew? Partition too big? Increase `s.sql.shuffle.partitions`. Increase `executor.memoryOverhead`.
80. **Spark Streaming vs Flink.**
    *   Micro-batch (High latency) vs Native Streaming (Low latency).
81. **Window Functions on massive data.**
    *   Risk of OOM if PartitionBy key is skewed.
82. **Explain `mapPartitions`.**
    *   Iterates per partition (Iterator). Good for expensive init (DB conn).
83. **Output Committer issues (S3).**
    *   Rename operation is slow/not atomic on S3. Use Magic Committer.
84. **Data Lineage usage.**
    *   Fault tolerance. Recomputing lost RDDs.
85. **DAG Visualization.**
    *   Reading the DAG in UI. Stages boundaries defined by Shuffles.
86. **Checkpointing.**
    *   Truncating lineage. Saving to disk. Crucial for Streaming / Deep Iteration.
87. **Difference: Checkpoint vs Cache.**
    *   Checkpoint breaks lineage. Cache keeps lineage.
88. **What is `spark.excutor.cores`?**
    *   Threads per executor. 3-5 is sweet spot.
89. **ThinExecutor vs FatExecutor.**
    *   Fat (Many cores) hits GC issues. Thin (1 core) creates HDFS overhead. Medium is best.
90. **Spark History Server.**
    *   Viewing logs of finished apps.
91. **Debugging "Task not serializable".**
    *   Class instance variables not serializable. Make static or transient.
92. **Arrow optimization config.**
    *   `spark.sql.execution.arrow.pyspark.enabled`.
93. **Job vs Stage vs Task.**
    *   Job (Action) -> Stages (Shuffle boundary) -> Task (Partition).
94. **Explain "Spill to Disk".**
    *   Memory full. Writes temp data to disk. Slow.
95. **Fair Scheduler (Pools).**
    *   Sharing cluster resources between users.
96. **Bloom Filters in Joins.**
    *   Probabilistic pruning.
97. **Dynamic Partition Pruning (DPP).**
    *   Runtime pruning for Star Schema joins.
98. **Writing Unit Tests for PySpark.**
    *   `pyspark.testing`. Creating small local sessions.
99. **What is GraphFrames?**
    *   Graph processing API on DataFrames.
100. **Pandas API on Spark.**
    *   `pyspark.pandas`. Drop-in replacement for pandas scaling.
