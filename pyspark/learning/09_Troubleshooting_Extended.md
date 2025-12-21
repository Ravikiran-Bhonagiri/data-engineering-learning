# Troubleshooting Guide

**Diagnose and fix common PySpark issues.**

---

## 🐛 Common Errors & Fixes

### OutOfMemoryError

**Error:**
```
java.lang.OutOfMemoryError: Java heap space
```

**Causes:**
- Driver OOM: Collecting too much data
- Executor OOM: Data skew or large partitions

**Fixes:**
```python
# Increase driver memory
spark = SparkSession.builder \
    .config("spark.driver.memory", "4g") \
    .getOrCreate()

# Increase executor memory
# In spark-submit: --executor-memory 8g

# Avoid collect() on large data
# ❌ df.collect()
# ✅ df.take(100)

# Reduce partition size
df = df.repartition(500)
```

---

### Task Not Serializable

**Error:**
```
org.apache.spark.SparkException: Task not serializable
```

**Cause:** Non-serializable object in transformation

**Fixes:**
```python
# ❌ Using class method
class MyClass:
    def process(self, x):
        return x * 2

obj = MyClass()
rdd.map(obj.process)  # Fails!

# ✅ Use static method or function
def process(x):
    return x * 2

rdd.map(process)

# ✅ Or use broadcast
bc_obj = spark.sparkContext.broadcast(my_data)
rdd.map(lambda x: x + bc_obj.value)
```

---

### AnalysisException: Column Not Found

**Error:**
```
AnalysisException: cannot resolve 'column_name'
```

**Fixes:**
```python
# Check column names
df.columns
df.printSchema()

# Case sensitivity
spark.conf.set("spark.sql.caseSensitive", False)

# Use backticks for special characters
df.select("`column-with-dash`")
```

---

### Py4JJavaError

**Error:**
```
py4j.protocol.Py4JJavaError: An error occurred while calling ...
```

**Common causes:**
1. Java version mismatch
2. Missing dependencies
3. Configuration issues

**Fixes:**
```bash
# Check Java version (need 8 or 11)
java -version

# Check Spark/PySpark compatibility
python -c "import pyspark; print(pyspark.__version__)"
```

---

### Shuffle Fetch Failed

**Error:**
```
FetchFailedException: Shuffle block failed
```

**Causes:**
- Executor died during shuffle
- Network timeout
- Disk full

**Fixes:**
```python
# Increase shuffle partitions
spark.conf.set("spark.sql.shuffle.partitions", 500)

# Increase memory fraction for shuffle
spark.conf.set("spark.shuffle.memoryFraction", 0.4)

# Add retries
spark.conf.set("spark.shuffle.fetch.retryWait", "30s")
spark.conf.set("spark.shuffle.fetch.maxRetries", "5")
```

---

### Slow Performance

**Symptoms:** Jobs take hours instead of minutes

**Diagnostic Steps:**
```python
# 1. Check explain plan
df.explain(True)

# 2. Check partitions
print(df.rdd.getNumPartitions())

# 3. Check for skew
df.groupBy("key").count().orderBy("count", ascending=False).show()
```

**Common Fixes:**
```python
# 1. Enable AQE
spark.conf.set("spark.sql.adaptive.enabled", True)

# 2. Broadcast small tables
df1.join(broadcast(small_df), "key")

# 3. Cache reused DataFrames
df.cache()

# 4. Repartition skewed data
df.repartition(200, "key")
```

---

### UDF Errors

**Error:**
```
PythonException: An exception was thrown from a UDF
```

**Debugging:**
```python
# Add try-except in UDF
@udf(returnType=StringType())
def safe_udf(x):
    try:
        return process(x)
    except Exception as e:
        return f"ERROR: {str(e)}"

# Check for nulls
df.filter(col("input").isNull()).count()
```

---

### Streaming Job Stuck

**Symptoms:** No progress in streaming query

**Diagnostic:**
```python
# Check query status
query.status
query.lastProgress
query.exception()
```

**Fixes:**
```python
# Add trigger interval
query = df.writeStream \
    .trigger(processingTime="10 seconds") \
    .start()

# Check Kafka connectivity
# Verify checkpoint location is writable
# Ensure source has new data
```

---

## 🔍 Debugging Tools

### Spark UI

Access at `http://driver:4040`:
- **Jobs:** Overall progress
- **Stages:** Shuffle details
- **Storage:** Cached data
- **SQL:** Query plans

### Logging

```python
# Set log level
spark.sparkContext.setLogLevel("DEBUG")

# View logs
# Check executor logs in cluster manager (YARN, K8s)
```

### Explain Plans

```python
# Physical plan
df.explain()

# Full plans (parsed, analyzed, optimized, physical)
df.explain(True)

# Cost-based optimization stats
df.explain("cost")
```

---

## 📋 Troubleshooting Checklist

**Before running:**
- [ ] Java 8/11 installed?
- [ ] JAVA_HOME set?
- [ ] PySpark version compatible?
- [ ] Cluster has enough resources?

**After failure:**
- [ ] Check Spark UI for failed stages
- [ ] Look for skew in data
- [ ] Check executor logs
- [ ] Verify data source accessible
- [ ] Check memory settings

**Performance issues:**
- [ ] Caching appropriate DataFrames?
- [ ] Broadcasting small tables?
- [ ] Partition count reasonable?
- [ ] Avoiding Python UDFs?
- [ ] AQE enabled?

---

**Debug systematically and check the Spark UI first!** 🔧
