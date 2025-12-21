# Complete PySpark Examples

**Production-ready examples with full code.**

---

## Example 1: ETL Pipeline (CSV → Transform → Parquet)

### Scenario
Process daily sales data: clean, enrich, aggregate, store in Parquet.

### Complete Code

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, sum, avg, count, current_date, datediff
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType, DateType

# Initialize
spark = SparkSession.builder \
    .appName("Sales ETL Pipeline") \
    .config("spark.sql.shuffle.partitions", 200) \
    .getOrCreate()

# Define schema (better than inferSchema for production)
schema = StructType([
    StructField("transaction_id", StringType(), False),
    StructField("customer_id", IntegerType(), True),
    StructField("product_id", StringType(), True),
    StructField("quantity", IntegerType(), True),
    StructField("unit_price", DoubleType(), True),
    StructField("transaction_date", DateType(), True),
    StructField("store_id", StringType(), True),
])

# EXTRACT
print("Extracting data...")
raw_df = spark.read \
    .option("header", True) \
    .schema(schema) \
    .csv("/data/raw/sales_*.csv")

print(f"Raw records: {raw_df.count()}")

# TRANSFORM
print("Transforming...")

# 1. Remove nulls in critical columns
clean_df = raw_df.dropna(subset=["transaction_id", "customer_id", "quantity"])

# 2. Filter invalid quantities
clean_df = clean_df.filter(col("quantity") > 0)

# 3. Calculate total amount
enriched_df = clean_df.withColumn(
    "total_amount", col("quantity") * col("unit_price")
)

# 4. Add customer segment
enriched_df = enriched_df.withColumn(
    "customer_segment",
    when(col("total_amount") > 1000, "Premium")
    .when(col("total_amount") > 100, "Standard")
    .otherwise("Basic")
)

# 5. Add days since transaction
enriched_df = enriched_df.withColumn(
    "days_ago", datediff(current_date(), col("transaction_date"))
)

# Aggregate by store
store_summary = enriched_df.groupBy("store_id", "transaction_date").agg(
    sum("total_amount").alias("daily_revenue"),
    count("transaction_id").alias("transaction_count"),
    avg("total_amount").alias("avg_transaction_value")
)

# LOAD
print("Loading to Parquet...")
enriched_df.write \
    .mode("overwrite") \
    .partitionBy("transaction_date") \
    .parquet("/data/processed/sales")

store_summary.write \
    .mode("overwrite") \
    .parquet("/data/processed/store_summary")

print("ETL Complete!")
spark.stop()
```

---

## Example 2: Real-Time Analytics (Streaming)

### Scenario
Process Kafka events: user clicks on a website.

### Complete Code

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    from_json, col, window, count, avg, to_timestamp
)
from pyspark.sql.types import StructType, StructField, StringType, LongType

spark = SparkSession.builder \
    .appName("Real-Time Click Analytics") \
    .getOrCreate()

# Define event schema
event_schema = StructType([
    StructField("user_id", StringType(), True),
    StructField("page", StringType(), True),
    StructField("action", StringType(), True),
    StructField("timestamp", LongType(), True),
])

# Read from Kafka
kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "user_clicks") \
    .option("startingOffsets", "latest") \
    .load()

# Parse JSON events
events = kafka_df \
    .select(from_json(col("value").cast("string"), event_schema).alias("event")) \
    .select("event.*") \
    .withColumn("event_time", to_timestamp(col("timestamp") / 1000))

# Windowed aggregation: clicks per page every 5 minutes
page_stats = events \
    .withWatermark("event_time", "10 minutes") \
    .groupBy(
        window(col("event_time"), "5 minutes"),
        col("page")
    ).agg(
        count("*").alias("click_count"),
        count("user_id").alias("unique_users")
    )

# Output to console (for demo) or Delta table
query = page_stats.writeStream \
    .outputMode("update") \
    .format("console") \
    .option("truncate", False) \
    .start()

# For production: write to Delta
# query = page_stats.writeStream \
#     .format("delta") \
#     .outputMode("append") \
#     .option("checkpointLocation", "/checkpoints/clicks") \
#     .start("/data/click_analytics")

query.awaitTermination()
```

---

## Example 3: ML Classification Pipeline

### Scenario
Predict customer churn using historical data.

### Complete Code

```python
from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.feature import (
    VectorAssembler, StringIndexer, StandardScaler, Imputer
)
from pyspark.ml.classification import GBTClassifier
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder

spark = SparkSession.builder.appName("Churn Prediction").getOrCreate()

# Load data
data = spark.read.parquet("/data/customers")
print(f"Records: {data.count()}")
data.printSchema()

# Define feature columns
numeric_cols = ["tenure", "monthly_charges", "total_charges"]
categorical_cols = ["contract_type", "payment_method"]
label_col = "churned"

# Build pipeline stages
stages = []

# 1. Impute missing numeric values
imputer = Imputer(
    inputCols=numeric_cols,
    outputCols=[f"{c}_imputed" for c in numeric_cols],
    strategy="median"
)
stages.append(imputer)

# 2. Index categorical columns
for cat_col in categorical_cols:
    indexer = StringIndexer(
        inputCol=cat_col,
        outputCol=f"{cat_col}_indexed",
        handleInvalid="keep"
    )
    stages.append(indexer)

# 3. Assemble features
feature_cols = (
    [f"{c}_imputed" for c in numeric_cols] +
    [f"{c}_indexed" for c in categorical_cols]
)
assembler = VectorAssembler(
    inputCols=feature_cols,
    outputCol="features_raw"
)
stages.append(assembler)

# 4. Scale features
scaler = StandardScaler(
    inputCol="features_raw",
    outputCol="features"
)
stages.append(scaler)

# 5. Classifier
gbt = GBTClassifier(
    featuresCol="features",
    labelCol=label_col,
    maxIter=20
)
stages.append(gbt)

# Build pipeline
pipeline = Pipeline(stages=stages)

# Split data
train, test = data.randomSplit([0.8, 0.2], seed=42)
print(f"Train: {train.count()}, Test: {test.count()}")

# Hyperparameter tuning
paramGrid = ParamGridBuilder() \
    .addGrid(gbt.maxDepth, [3, 5, 7]) \
    .addGrid(gbt.stepSize, [0.1, 0.01]) \
    .build()

evaluator = BinaryClassificationEvaluator(
    labelCol=label_col,
    metricName="areaUnderROC"
)

cv = CrossValidator(
    estimator=pipeline,
    estimatorParamMaps=paramGrid,
    evaluator=evaluator,
    numFolds=3
)

# Train
print("Training model...")
cv_model = cv.fit(train)
best_model = cv_model.bestModel

# Evaluate
predictions = best_model.transform(test)
auc = evaluator.evaluate(predictions)
print(f"Test AUC: {auc:.4f}")

# Feature importance (from GBT stage)
gbt_model = best_model.stages[-1]
print(f"Feature Importances: {gbt_model.featureImportances}")

# Save model
best_model.save("/models/churn_model_v1")
print("Model saved!")

# Predict on new data
# loaded_model = PipelineModel.load("/models/churn_model_v1")
# new_predictions = loaded_model.transform(new_customers)

spark.stop()
```

---

## 🎯 Key Patterns in These Examples

| Pattern | Where Used |
|---------|------------|
| **Schema definition** | Example 1 (production-grade) |
| **Null handling** | Example 1 (dropna, filter) |
| **Window aggregation** | Example 2 (streaming) |
| **Watermarking** | Example 2 (late data) |
| **Pipeline** | Example 3 (ML) |
| **CrossValidator** | Example 3 (tuning) |
| **Save/Load models** | Example 3 (production) |

---

**Use these as templates for your own projects!** 🚀
