# Databricks notebook receiver
import dlt
from pyspark.sql.functions import col, current_timestamp, to_date

# Define bucket paths (Production would use widgets)
LANDING_PATH = "s3://serverless-lakehouse-dev-landing-zone/app_logs/"

# ==========================================
# BRONZE LAYER (Raw Logs)
# ==========================================
# Autoloader handles the "Small Files" problem and Schema Drift automatically.

@dlt.table(
    comment="Raw application logs ingested from S3 via Autoloader",
    table_properties={
        "quality": "bronze",
        "delta.appendOnly": "true"
    }
)
def bronze_app_logs():
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "json")
        .option("cloudFiles.inferColumnTypes", "true")
        # CRITICAL: This solves the Schema Evolution problem
        .option("cloudFiles.schemaEvolutionMode", "addNewColumns") 
        .load(LANDING_PATH)
        .withColumn("_ingestion_timestamp", current_timestamp())
        .withColumn("_source_file", col("_metadata.file_path"))
    )

# ==========================================
# SILVER LAYER (Cleaned Logs)
# ==========================================
# Generic Data Quality Rules:
# 1. Must have a timestamp (otherwise we can't analyze "when")
# 2. Must have a user_id (or device_id) to verify authenticity

@dlt.table(
    comment="Cleaned logs with valid timestamps and identifiers",
    table_properties={
        "quality": "silver"
    }
)
@dlt.expect_or_drop("valid_timestamp", "timestamp IS NOT NULL")
@dlt.expect("valid_identifier", "user_id IS NOT NULL OR device_id IS NOT NULL")
def silver_app_logs():
    return (
        dlt.read("bronze_app_logs")
        .select(
            "event_id",
            "user_id",
            "device_id",
            "action_type",
            "metadata_json",
            to_date("timestamp").alias("log_date"),
            "timestamp",
            "_ingestion_timestamp"
        )
    )
