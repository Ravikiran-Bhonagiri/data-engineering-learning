# PySpark Quick Reference

**Cheat sheet for daily PySpark work.**

---

## 🚀 SparkSession

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("my_app") \
    .master("local[*]") \
    .config("spark.sql.shuffle.partitions", 200) \
    .getOrCreate()

spark.stop()  # Cleanup
```

---

## 📊 Create DataFrames

```python
# From list
df = spark.createDataFrame([(1, "a"), (2, "b")], ["id", "val"])

# From CSV/JSON/Parquet
df = spark.read.csv("path.csv", header=True, inferSchema=True)
df = spark.read.json("path.json")
df = spark.read.parquet("path.parquet")
```

---

## 🔧 DataFrame Operations

```python
import pyspark.sql.functions as F

# Select
df.select("col1", "col2")
df.select(F.col("name"), F.col("age") + 1)

# Filter
df.filter(F.col("age") > 25)
df.where("age > 25")

# Add/Modify column
df.withColumn("new_col", F.col("age") * 2)
df.withColumnRenamed("old", "new")

# Drop
df.drop("col1", "col2")

# Distinct
df.distinct()
df.dropDuplicates(["id"])
```

---

## 📈 Aggregations

```python
from pyspark.sql.functions import sum, avg, count, max, min

df.groupBy("dept").agg(
    sum("salary").alias("total"),
    avg("salary").alias("average"),
    count("*").alias("count")
)

# Multiple groupBy
df.groupBy("dept", "level").agg(sum("salary"))
```

---

## 🔗 Joins

```python
# Inner (default)
df1.join(df2, "key")
df1.join(df2, df1.id == df2.id)

# Types: left, right, outer, cross, semi, anti
df1.join(df2, "key", "left")
```

---

## 🪟 Window Functions

```python
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number, rank, lag, lead

window = Window.partitionBy("dept").orderBy("salary")

df.withColumn("rank", rank().over(window))
df.withColumn("row_num", row_number().over(window))
df.withColumn("prev_salary", lag("salary", 1).over(window))
```

---

## 📝 SQL

```python
df.createOrReplaceTempView("table")
spark.sql("SELECT * FROM table WHERE age > 25").show()
```

---

## 🛠 Common Functions

```python
from pyspark.sql.functions import (
    col, lit, when, concat, upper, lower, trim,
    split, explode, array, struct,
    year, month, day, current_date, datediff,
    sum, avg, count, max, min,
    coalesce, isnull, isnan
)

# Conditional
df.withColumn("tier", 
    when(col("age") > 30, "Senior")
    .when(col("age") > 20, "Mid")
    .otherwise("Junior")
)

# Null handling
df.fillna(0)
df.dropna()
df.withColumn("safe", coalesce(col("val"), lit(0)))

# Strings
df.withColumn("name", upper(col("name")))
df.withColumn("words", split(col("text"), " "))

# Arrays
df.withColumn("first", explode(col("items")))
```

---

## 💾 Write Data

```python
# Parquet (recommended)
df.write.parquet("output.parquet")

# CSV
df.write.csv("output.csv", header=True)

# Delta
df.write.format("delta").save("output")

# Modes: overwrite, append, ignore, error
df.write.mode("overwrite").parquet("output")

# Partitioned
df.write.partitionBy("year", "month").parquet("output")
```

---

## ⚡ Performance Tips

```python
# Cache frequently used DataFrames
df.cache()
df.persist()
df.unpersist()

# Broadcast small tables
from pyspark.sql.functions import broadcast
df1.join(broadcast(small_df), "key")

# Repartition
df.repartition(100)
df.repartition("key")
df.coalesce(10)  # Reduce partitions

# Explain plan
df.explain()
df.explain(True)
```

---

## 📊 MLlib Quick Reference

```python
from pyspark.ml.feature import VectorAssembler, StringIndexer
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml import Pipeline

# Pipeline
pipeline = Pipeline(stages=[
    StringIndexer(inputCol="cat", outputCol="cat_idx"),
    VectorAssembler(inputCols=["col1", "col2"], outputCol="features"),
    RandomForestClassifier(labelCol="label", featuresCol="features")
])

model = pipeline.fit(train)
predictions = model.transform(test)
```

---

## 🌊 Streaming Quick Reference

```python
# Read stream
df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "topic").load()

# Write stream
query = df.writeStream \
    .outputMode("append") \
    .format("parquet") \
    .option("checkpointLocation", "/checkpoint") \
    .start("/output")

query.awaitTermination()
```

---

## 🎯 Interview Q&A

**Q: RDD vs DataFrame?**  
A: DataFrames are optimized (Catalyst), have schema, easier API. RDDs for low-level control.

**Q: Transformations vs Actions?**  
A: Transformations are lazy (return new DF). Actions trigger execution (count, show, write).

**Q: How to optimize slow Spark jobs?**  
A: Cache, broadcast joins, tune partitions, avoid UDFs, check for skew.

**Q: What is shuffle?**  
A: Data redistribution across nodes (groupBy, join). Expensive - minimize it.

**Q: Explain lazy evaluation.**  
A: Spark builds execution plan without running until action is called.

**Q: What is Catalyst optimizer?**  
A: Query optimizer that rewrites, combines, and optimizes execution plans.

**Q: How to handle skewed data?**  
A: Salting keys, broadcast smaller table, increase partitions.

---

## 🐛 Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `AnalysisException` | Column not found | Check column names, case sensitivity |
| `OutOfMemoryError` | Driver/executor OOM | Increase memory, reduce collect() |
| `Task not serializable` | Non-serializable in UDF | Use broadcast or make serializable |
| `Py4JJavaError` | JVM error | Check Java version, dependencies |

---

**Keep this handy during development!** 🚀
