# PySpark Foundation

**For:** Python developers who want to process big data  
**Goal:** Understand what PySpark is, why it matters, and how Spark works.

---

## 🤔 The Problem: Python's Single-Machine Limitation

### Before PySpark: Pandas on One Machine

```python
import pandas as pd

# Works great for small data
df = pd.read_csv("sales_data.csv")  # 100 MB file
result = df.groupby("region").agg({"revenue": "sum"})
print(result)
```

**But what happens with 100 GB or 1 TB of data?**

```python
# This will crash your laptop!
df = pd.read_csv("massive_sales_data.csv")  # 100 GB file
# MemoryError: Unable to allocate 95.4 GiB
```

### Problems with Single-Machine Python:
1. **Memory limits:** Data must fit in RAM
2. **No parallelism:** Single CPU core processing
3. **No fault tolerance:** Crash = start over
4. **No scalability:** Can't add more machines

---

## ✅ The Solution: Apache Spark + PySpark

**PySpark** is the Python API for Apache Spark, a distributed computing engine that:
- Processes data **across clusters** of machines
- Runs **in-memory** for speed (100x faster than Hadoop MapReduce)
- Provides **fault tolerance** (recovers from failures automatically)
- Scales from **laptop to thousands of nodes**

### Same analysis in PySpark:

```python
from pyspark.sql import SparkSession
import pyspark.sql.functions as F

# Create Spark session
spark = SparkSession.builder.appName("sales_analysis").getOrCreate()

# Read 100 GB file distributed across cluster
df = spark.read.csv("s3://data/massive_sales_data.csv", header=True)

# Process across 100+ machines in parallel
result = df.groupBy("region").agg(F.sum("revenue").alias("total_revenue"))

result.show()
```

**What changed:**
- ✅ **No memory limit:** Data distributed across cluster
- ✅ **Parallel processing:** Uses all CPU cores across all machines
- ✅ **Fault tolerance:** Automatic recovery from failures
- ✅ **Scalable:** Add machines to handle more data

---

## 🏗️ Spark Architecture

```
┌─────────────────────────────────────────────────────┐
│                    DRIVER PROGRAM                    │
│  (Your Python code runs here - SparkSession)        │
└─────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────┐
│                  CLUSTER MANAGER                     │
│        (YARN, Kubernetes, Mesos, Standalone)        │
└─────────────────────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│   EXECUTOR 1  │ │   EXECUTOR 2  │ │   EXECUTOR 3  │
│  ┌─────────┐  │ │  ┌─────────┐  │ │  ┌─────────┐  │
│  │ Task 1  │  │ │  │ Task 3  │  │ │  │ Task 5  │  │
│  │ Task 2  │  │ │  │ Task 4  │  │ │  │ Task 6  │  │
│  └─────────┘  │ │  └─────────┘  │ │  └─────────┘  │
│   [Cache]     │ │   [Cache]     │ │   [Cache]     │
└───────────────┘ └───────────────┘ └───────────────┘
```

### Components:

| Component | Role |
|-----------|------|
| **Driver** | Your code; coordinates execution |
| **Cluster Manager** | Allocates resources (YARN, K8s) |
| **Executors** | JVM processes that run tasks |
| **Tasks** | Units of work on data partitions |
| **Cache** | In-memory storage for speed |

---

## 📦 PySpark Ecosystem

| Module | Purpose | Use Case |
|--------|---------|----------|
| **Spark SQL & DataFrames** | Structured data processing | ETL, analytics, SQL queries |
| **Structured Streaming** | Real-time data processing | IoT, logs, event streams |
| **MLlib** | Machine learning at scale | Training models on big data |
| **Spark Core (RDDs)** | Low-level API | Custom transformations |
| **Pandas API on Spark** | Pandas-like syntax | Easy migration from pandas |

---

## 🆚 When to Use/Not Use PySpark

### ✅ Use PySpark For:

| Use Case | Why PySpark? |
|----------|--------------|
| **Big data ETL** | Process TB/PB of data |
| **Data lake analytics** | Query Parquet, Delta Lake |
| **ML on large datasets** | Train models on billions of rows |
| **Real-time streaming** | Process Kafka, Kinesis streams |
| **Data warehouse queries** | Replace expensive cloud DW |

### ❌ Don't Use PySpark For:

| Use Case | Why Not? | Alternative |
|----------|----------|-------------|
| **Small data (<10 GB)** | Overkill, slow startup | Pandas, Polars |
| **Real-time (<100ms)** | Latency too high | Flink, Kafka Streams |
| **Simple scripts** | Too complex | Python + pandas |
| **Interactive notebooks** | Slow iteration | Pandas, DuckDB |

**Rule of thumb:** If data fits in memory → use pandas. If not → use PySpark.

---

## 📊 PySpark vs. Alternatives

| Tool | Best For | Distributed? |
|------|----------|--------------|
| **Pandas** | Small data, quick analysis | ❌ Single machine |
| **Polars** | Medium data, fast | ❌ Single machine |
| **DuckDB** | Analytics, SQL | ❌ Single machine |
| **Dask** | Pandas at scale | ✅ Limited |
| **PySpark** | Big data, production | ✅ Full cluster |
| **Snowflake/BigQuery** | Managed analytics | ✅ Cloud only |

---

## 🎓 Key Concepts

### RDD (Resilient Distributed Dataset)
- Low-level API (foundational)
- Immutable, partitioned collection
- Fault-tolerant via lineage

### DataFrame
- High-level API (recommended)
- Schema-based like SQL table
- Optimized by Catalyst query optimizer

### Transformations vs Actions
```python
# Transformations (lazy - don't execute immediately)
df.filter(df.age > 21)      # Returns new DataFrame
df.select("name", "age")    # Returns new DataFrame

# Actions (trigger execution)
df.count()                  # Returns number
df.show()                   # Prints rows
df.collect()                # Returns all rows to driver
```

### Lazy Evaluation
```python
# Nothing happens yet (just builds plan)
df2 = df.filter(df.age > 21)
df3 = df2.select("name")

# NOW Spark executes the entire plan
df3.show()  # Triggers execution
```

---

## 🚀 What You'll Build

By the end of this course:
- ✅ Set up PySpark locally and on clusters
- ✅ Process large datasets with DataFrames
- ✅ Write SQL queries on Spark
- ✅ Build streaming applications
- ✅ Train ML models at scale
- ✅ Optimize Spark jobs for performance
- ✅ Deploy to production (Databricks, EMR)

**Next Step:** Open `02_Day_00.md` to start! 🎯
