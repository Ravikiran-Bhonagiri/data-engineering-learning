# Delta Lake & Advanced Topics

**Modern data lakehouse patterns and advanced PySpark features.**

---

## 🏠 Delta Lake Deep Dive

### MERGE Patterns

```python
from delta.tables import DeltaTable

delta_table = DeltaTable.forPath(spark, "/data/customers")

# Upsert (Update existing, Insert new)
delta_table.alias("target").merge(
    updates.alias("source"),
    "target.id = source.id"
).whenMatchedUpdateAll() \
 .whenNotMatchedInsertAll() \
 .execute()

# Conditional update
delta_table.alias("t").merge(
    source.alias("s"),
    "t.id = s.id"
).whenMatchedUpdate(
    condition="s.updated_at > t.updated_at",
    set={"name": "s.name", "updated_at": "s.updated_at"}
).whenNotMatchedInsert(
    values={"id": "s.id", "name": "s.name", "updated_at": "s.updated_at"}
).execute()

# Delete matched rows
delta_table.alias("t").merge(
    deletes.alias("s"),
    "t.id = s.id"
).whenMatchedDelete().execute()
```

### Change Data Feed

```python
# Enable CDF
spark.sql("ALTER TABLE my_table SET TBLPROPERTIES (delta.enableChangeDataFeed = true)")

# Read changes
changes = spark.read.format("delta") \
    .option("readChangeDataFeed", True) \
    .option("startingVersion", 5) \
    .table("my_table")

# Change types: insert, update_preimage, update_postimage, delete
changes.filter(col("_change_type") == "update_postimage").show()
```

### Schema Enforcement & Evolution

```python
# Strict enforcement (default)
df.write.format("delta").mode("append").save("/data/table")  # Fails if schema mismatch

# Schema evolution
df.write.format("delta") \
    .option("mergeSchema", True) \
    .mode("append") \
    .save("/data/table")

# Overwrite schema
df.write.format("delta") \
    .option("overwriteSchema", True) \
    .mode("overwrite") \
    .save("/data/table")
```

---

## 🔧 Advanced DataFrame Operations

### Complex Types

```python
from pyspark.sql.functions import struct, array, map_from_arrays, explode, col

# Create struct
df.withColumn("person", struct("name", "age"))

# Create array
df.withColumn("tags", array("tag1", "tag2"))

# Create map
df.withColumn("attributes", map_from_arrays(array("key1"), array("val1")))

# Explode array
df.select(explode(col("tags")).alias("tag"))

# Access nested fields
df.select(col("person.name"))
df.select(col("attributes")["key1"])
```

### Pivot Tables

```python
# Long to wide
pivoted = df.groupBy("date").pivot("category").sum("revenue")

# Result: date | Electronics | Clothing | Food

# Limit pivot values
pivoted = df.groupBy("date") \
    .pivot("category", ["Electronics", "Clothing"]) \
    .sum("revenue")
```

### Custom Aggregations

```python
from pyspark.sql.functions import pandas_udf, PandasUDFType
import pandas as pd

@pandas_udf("double", PandasUDFType.GROUPED_AGG)
def weighted_mean(values: pd.Series, weights: pd.Series) -> float:
    return (values * weights).sum() / weights.sum()

df.groupBy("category").agg(
    weighted_mean(col("price"), col("quantity")).alias("weighted_avg_price")
)
```

---

## 🌊 Advanced Streaming

### Stateful Operations

```python
from pyspark.sql.streaming import GroupState, GroupStateTimeout

# Define state update function
def update_session_state(key, values, state: GroupState):
    if state.hasTimedOut:
        yield (key, state.get, "timeout")
        state.remove()
    else:
        events = list(values)
        total = state.getOption or 0
        new_total = total + len(events)
        state.update(new_total)
        state.setTimeoutDuration("30 minutes")
        yield (key, new_total, "active")

# Apply stateful processing
result = df.groupByKey(lambda row: row.session_id) \
    .flatMapGroupsWithState(
        outputMode="append",
        timeoutConf=GroupStateTimeout.ProcessingTimeTimeout,
        func=update_session_state
    )
```

### Kafka Sink with Exactly-Once

```python
df.writeStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("topic", "output") \
    .option("checkpointLocation", "/checkpoints/kafka-sink") \
    .outputMode("append") \
    .start()
```

---

## 📊 Spark Connect (Remote Client)

```python
# Client-side (thin client, no Spark installation needed)
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .remote("sc://spark-server:15002") \
    .getOrCreate()

# Use like normal SparkSession
df = spark.read.parquet("/data/sales")
df.show()
```

---

## 🐼 Pandas API on Spark

```python
import pyspark.pandas as ps

# Create pandas-on-Spark DataFrame
psdf = ps.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})

# Pandas operations work!
psdf["C"] = psdf["A"] + psdf["B"]
psdf.describe()
psdf.plot.bar()

# Convert from Spark DataFrame
psdf = df.pandas_api()

# Convert to Spark DataFrame
spark_df = psdf.to_spark()

# Read data
psdf = ps.read_csv("/data/file.csv")
```

---

## 📈 GraphFrames (Graph Processing)

```python
from graphframes import GraphFrame

# Create vertices and edges
vertices = spark.createDataFrame([
    ("1", "Alice", 30),
    ("2", "Bob", 35),
    ("3", "Charlie", 25),
], ["id", "name", "age"])

edges = spark.createDataFrame([
    ("1", "2", "friend"),
    ("2", "3", "colleague"),
    ("1", "3", "friend"),
], ["src", "dst", "relationship"])

# Create graph
g = GraphFrame(vertices, edges)

# PageRank
g.pageRank(resetProbability=0.15, maxIter=10).vertices.show()

# Connected components
g.connectedComponents().show()

# Shortest paths
g.shortestPaths(landmarks=["1"]).show()
```

---

## 🔌 External Integrations

### JDBC Write with Batch

```python
df.write \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://host:5432/db") \
    .option("dbtable", "public.sales") \
    .option("user", "user") \
    .option("password", "pass") \
    .option("batchsize", 10000) \
    .option("numPartitions", 10) \
    .mode("append") \
    .save()
```

### MongoDB Connector

```python
df = spark.read \
    .format("mongo") \
    .option("uri", "mongodb://host:27017/db.collection") \
    .load()
```

---

## 🎯 Best Practices Summary

| Area | Best Practice |
|------|---------------|
| **Storage** | Use Delta Lake for all tables |
| **Schema** | Define explicitly, enable evolution |
| **Partitioning** | By date/time for time-series |
| **MERGE** | For incremental updates |
| **Streaming** | Use checkpoints, watermarks |
| **Performance** | Enable AQE, avoid UDFs |
| **Pandas** | Use pandas API on Spark for migration |

---

**You've mastered advanced PySpark!** 🏆
