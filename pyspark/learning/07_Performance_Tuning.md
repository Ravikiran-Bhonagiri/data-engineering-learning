# Performance Tuning Guide

**Optimize your Spark jobs for speed and efficiency.**

---

## 📊 Understanding Spark Execution

```
Job → Stages → Tasks
     ↓
 [Shuffle Boundaries]
```

- **Job:** Triggered by action (count, write)
- **Stage:** Separated by shuffles
- **Task:** Unit of work on one partition

---

## ⚡ Key Optimization Areas

### 1. Partitioning

```python
# Check current partitions
df.rdd.getNumPartitions()

# Increase partitions (before heavy operations)
df = df.repartition(200)

# Decrease partitions (before write)
df = df.coalesce(10)

# Partition by column (for writes)
df.repartition("date")
```

**Rules:**
- 2-4 tasks per CPU core
- Each partition: 100-200 MB
- Too few = underutilization
- Too many = overhead

### 2. Caching

```python
from pyspark import StorageLevel

# Cache frequently used DataFrames
df.cache()  # MEMORY_AND_DISK
df.persist(StorageLevel.MEMORY_ONLY)
df.persist(StorageLevel.DISK_ONLY)

# Unpersist when done
df.unpersist()
```

**When to cache:**
- Used multiple times in job
- After expensive transformations
- Before iterative operations

### 3. Broadcast Joins

```python
from pyspark.sql.functions import broadcast

# Small table (<10MB) should be broadcast
result = large_df.join(broadcast(small_df), "key")

# Configure broadcast threshold
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", 10 * 1024 * 1024)  # 10MB
```

---

## 🚫 Avoid UDFs When Possible

```python
# ❌ SLOW: Python UDF
from pyspark.sql.functions import udf
from pyspark.sql.types import IntegerType

@udf(returnType=IntegerType())
def slow_square(x):
    return x * x

df.withColumn("squared", slow_square(col("value")))

# ✅ FAST: Built-in function
from pyspark.sql.functions import pow

df.withColumn("squared", pow(col("value"), 2))
```

**If you must use UDF:**
```python
# Use Pandas UDF (vectorized)
from pyspark.sql.functions import pandas_udf
import pandas as pd

@pandas_udf("double")
def fast_square(s: pd.Series) -> pd.Series:
    return s * s

df.withColumn("squared", fast_square(col("value")))
```

---

## 🔀 Reduce Shuffles

Shuffles are expensive (network I/O):

```python
# ❌ Multiple shuffles
df.groupBy("a").count().groupBy("b").count()

# ✅ Single shuffle
df.groupBy("a", "b").count()
```

**Shuffle-causing operations:**
- `groupBy`
- `join` (without broadcast)
- `distinct`
- `repartition`
- `sort`

---

## ⚙️ Configuration Tuning

```python
spark = SparkSession.builder \
    .config("spark.sql.shuffle.partitions", 200) \
    .config("spark.default.parallelism", 100) \
    .config("spark.executor.memory", "4g") \
    .config("spark.executor.cores", 4) \
    .config("spark.memory.fraction", 0.8) \
    .getOrCreate()
```

| Config | Description | Default |
|--------|-------------|---------|
| `spark.sql.shuffle.partitions` | Partitions for shuffles | 200 |
| `spark.default.parallelism` | RDD partitions | Total cores |
| `spark.executor.memory` | Memory per executor | 1g |
| `spark.memory.fraction` | Fraction for execution | 0.6 |

---

## 🔍 Reading Explain Plans

```python
df = spark.sql("SELECT dept, SUM(salary) FROM employees GROUP BY dept")
df.explain(True)
```

**Look for:**
- `BroadcastHashJoin` (good) vs `SortMergeJoin` (expensive)
- `Exchange` = shuffle (minimize these)
- `Filter` pushed down (good)

---

## 📈 Handling Data Skew

```python
# Problem: One key has millions of rows

# Solution 1: Salting
from pyspark.sql.functions import concat, lit, rand

salt_range = 10
df_salted = df.withColumn("salted_key", 
    concat(col("key"), lit("_"), (rand() * salt_range).cast("int"))
)

# Solution 2: Broadcast smaller side
result = skewed_df.join(broadcast(small_df), "key")

# Solution 3: Enable AQE
spark.conf.set("spark.sql.adaptive.enabled", True)
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", True)
```

---

## 🧪 Benchmarking

```python
import time

def benchmark(name, df_func):
    start = time.time()
    result = df_func()
    result.count()  # Force execution
    elapsed = time.time() - start
    print(f"{name}: {elapsed:.2f}s")

benchmark("With cache", lambda: cached_df.filter(col("x") > 0))
benchmark("Without cache", lambda: df.filter(col("x") > 0))
```

---

## 🎯 Optimization Checklist

- [ ] Appropriate number of partitions
- [ ] Cache reused DataFrames
- [ ] Broadcast small tables
- [ ] Avoid Python UDFs (use built-ins)
- [ ] Minimize shuffles
- [ ] Enable AQE (`spark.sql.adaptive.enabled=true`)
- [ ] Check explain plans for issues
- [ ] Handle data skew
- [ ] Use Parquet/Delta (columnar)
- [ ] Filter early, select only needed columns

---

**Master these techniques for 10x faster Spark jobs!** 🚀
