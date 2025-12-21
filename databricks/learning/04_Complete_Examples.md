# Complete Databricks Examples

**Production-ready code patterns for key interview scenarios.**

---

## Example 1: DLT Pipeline with Auto Loader (CDC)

**Scenario:** Ingest JSON files from S3, handle schema evolution, and apply CDC updates.

```python
import dlt
from pyspark.sql.functions import *

# 1. Bronze: Incremental Ingestion
@dlt.table(
    comment="Raw JSON ingestion with Schema Evolution",
    table_properties={"quality": "bronze"}
)
def bronze_users():
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "json")
        .option("cloudFiles.schemaLocation", "/tmp/schema/users")
        .option("cloudFiles.inferColumnTypes", "true")
        .load("/mnt/landing/users")
        .withColumn("ingestion_time", current_timestamp())
    )

# 2. Silver: Type 1 CDC (Overwrite old state)
dlt.create_streaming_table("silver_users")

dlt.apply_changes(
    target = "silver_users",
    source = "bronze_users",
    keys = ["user_id"],
    sequence_by = col("updated_at"), # Use latest timestamp
    stored_as_scd_type = 1 # Keep only current state
)

# 3. Gold: Aggregates
@dlt.table(
    comment="Daily user signup counts"
)
def gold_daily_signups():
    return (
        dlt.read("silver_users")
        .groupBy(to_date("created_at").alias("date"))
        .count()
    )
```

**Interview Note:** Mention `apply_changes()` API. It abstracts the complex `MERGE` logic required for deduplication and ordering updates.

---

## Example 2: Unity Catalog Setup Script

**Scenario:** You are the Admin. Set up a new project structure securely.

```sql
-- 1. Create Catalog
CREATE CATALOG IF NOT EXISTS marketing_prod
MANAGED LOCATION 's3://my-datalake/marketing_prod';

-- 2. Create Schema
USE CATALOG marketing_prod;
CREATE SCHEMA IF NOT EXISTS campaigns;

-- 3. Create Managed Table
CREATE TABLE campaigns.email_stats (
    campaign_id INT,
    sent INT,
    opened INT
);

-- 4. Create External Volume for Images
CREATE VOLUME campaigns.creative_assets
LOCATION 's3://my-datalake/marketing_assets';

-- 5. Set Permissions (Principle of Least Privilege)
-- Data Engineers own the structure
GRANT ALL PRIVILEGES ON SCHEMA campaigns TO `data_engineers`;

-- Analysts can only read
GRANT SELECT ON TABLE campaigns.email_stats TO `marketing_analysts`;

-- 6. PII Masking (Dynamic View)
CREATE VIEW campaigns.secure_stats AS
SELECT 
    campaign_id,
    sent,
    CASE 
        WHEN is_account_group_member('managers') THEN opened 
        ELSE NULL 
    END as opened_count
FROM campaigns.email_stats;
```

---

## Example 3: Structured Streaming with ForeachBatch

**Scenario:** Write streaming data to a sink that doesn't support streaming (e.g., calling an external API or complex Delta merge).

```python
def process_batch(df, batch_id):
    # This runs on the Driver
    print(f"Processing batch {batch_id} with {df.count()} records")
    
    # 1. De-dupe the micro-batch
    batch_deduped = df.dropDuplicates(["id"])
    
    # 2. Complex Merge Logic
    from delta.tables import DeltaTable
    deltaTable = DeltaTable.forName(spark, "target_table")
    
    (deltaTable.alias("t")
      .merge(batch_deduped.alias("s"), "t.id = s.id")
      .whenMatchedUpdateAll()
      .whenNotMatchedInsertAll()
      .execute())
      
    # 3. Optimize every 10 batches (Optional pattern)
    if batch_id % 10 == 0:
        spark.sql("OPTIMIZE target_table")

# Start Stream
stream_query = (spark.readStream
    .table("source_table")
    .writeStream
    .foreachBatch(process_batch)
    .option("checkpointLocation", "/tmp/checkpoints/custom_merge")
    .start())
```

**Interview Note:** `foreachBatch` is the escape hatch. Use it when standard sinks aren't enough or when you need to run specific logic (like `OPTIMIZE` or API calls) per batch.

---

## Example 4: MLflow Training with Signature

**Scenario:** Train a model and enforce input schema (Signature).

```python
import mlflow
from mlflow.models.signature import infer_signature

# Load Data
df = spark.table("silver_churn").toPandas()
X = df.drop("churn", axis=1)
y = df["churn"]

with mlflow.start_run():
    # Train
    model = RandomForestClassifier()
    model.fit(X, y)
    
    # Infer Signature (Crucial for Serving!)
    signature = infer_signature(X, model.predict(X))
    
    # Log Model with Signature
    mlflow.sklearn.log_model(
        model, 
        "model",
        signature=signature,
        registered_model_name="dev.ml.churn_model"
    )
    
    # Log Metrics
    mlflow.log_metric("accuracy", 0.95)
```

**Interview Note:** Mentioning "Signatures" shows you think about production serving, not just training. It prevents type mismatch errors when deploying the model.
