# ingestion.py
# This code is designed to run in a Databricks Notebook

from pyspark.sql.functions import col, current_timestamp, input_file_name

# 1. Configuration
# In a real project, these paths would come from Widgets or Secrets
SOURCE_PATH = "s3://databricks-foundations-dev-landing/raw-events/"
CHECKPOINT_PATH = "s3://databricks-foundations-dev-bronze/_checkpoints/raw_events_stream"
TARGET_TABLE = "bronze.raw_events"

def ingest_data():
    # 2. Define the Stream
    # We use format("cloudFiles") to invoke Autoloader
    stream_df = (spark.readStream
        .format("cloudFiles") 
        .option("cloudFiles.format", "json") 
        
        # KEY FEATURE 1: Schema Evolution
        # "addNewColumns" will update the Delta table schema automatically
        .option("cloudFiles.schemaEvolutionMode", "addNewColumns") 
        
        # KEY FEATURE 2: Rescue Data
        # Corrupt data (e.g. integer field containing string) goes here
        .option("cloudFiles.schemaLocation", CHECKPOINT_PATH + "/schema")
        
        .load(SOURCE_PATH)
        
        # Add metadata columns for lineage
        .withColumn("_ingestion_ts", current_timestamp())
        .withColumn("_source_file", input_file_name())
    )

    # 3. Write to Delta
    # mergeSchema=true is required to allow the write-side to update the table
    (stream_df.writeStream
        .format("delta")
        .option("checkpointLocation", CHECKPOINT_PATH)
        .option("mergeSchema", "true") 
        .outputMode("append")
        .table(TARGET_TABLE)
    )

if __name__ == "__main__":
    print("Starting Autoloader Stream...")
    ingest_data()
