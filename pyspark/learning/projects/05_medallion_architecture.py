"""
Project 5: Medallion Architecture
=================================
Implement Bronze → Silver → Gold data lakehouse pattern.

Skills: Delta Lake, MERGE, Data layers, Schema evolution

Run: spark-submit --packages io.delta:delta-core_2.12:2.4.0 05_medallion_architecture.py
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, current_timestamp, lit, when, sum, avg, count,
    year, month, dayofmonth, to_date, row_number
)
from pyspark.sql.window import Window
from pyspark.sql.types import (
    StructType, StructField,
    StringType, IntegerType, DoubleType, TimestampType
)


def create_spark_session():
    """Create Spark session with Delta Lake support."""
    return SparkSession.builder \
        .appName("Medallion Architecture") \
        .config("spark.jars.packages", "io.delta:delta-core_2.12:2.4.0") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .getOrCreate()


def create_raw_data(spark):
    """Simulate raw data from source systems."""
    
    # Batch 1: Initial data
    batch1 = [
        ("2025-01-15 10:00:00", "ORD001", "CUST001", "PROD001", 2, 29.99, "COMPLETED"),
        ("2025-01-15 11:30:00", "ORD002", "CUST002", "PROD002", 1, 149.99, "COMPLETED"),
        ("2025-01-15 14:00:00", "ORD003", "CUST001", "PROD003", 3, 9.99, "PENDING"),
        ("2025-01-16 09:00:00", "ORD004", "CUST003", "PROD001", 1, 29.99, "COMPLETED"),
        ("2025-01-16 12:00:00", "ORD005", "CUST002", "PROD004", 2, 79.99, "CANCELLED"),
        # Duplicates and errors
        ("2025-01-15 10:00:00", "ORD001", "CUST001", "PROD001", 2, 29.99, "COMPLETED"),  # Duplicate
        ("2025-01-16 15:00:00", "ORD006", None, "PROD002", 1, 149.99, "COMPLETED"),  # Null customer
    ]
    
    schema = StructType([
        StructField("event_time", StringType(), True),
        StructField("order_id", StringType(), True),
        StructField("customer_id", StringType(), True),
        StructField("product_id", StringType(), True),
        StructField("quantity", IntegerType(), True),
        StructField("unit_price", DoubleType(), True),
        StructField("status", StringType(), True),
    ])
    
    return spark.createDataFrame(batch1, schema)


def process_bronze_layer(spark, raw_df, bronze_path):
    """
    BRONZE LAYER: Raw data ingestion with minimal transformation.
    - Add ingestion metadata
    - Store as-is (append only)
    """
    print("\n" + "=" * 60)
    print("BRONZE LAYER: Raw Ingestion")
    print("=" * 60)
    
    # Add metadata
    bronze_df = raw_df \
        .withColumn("_ingested_at", current_timestamp()) \
        .withColumn("_source", lit("order_system")) \
        .withColumn("_batch_id", lit(1))
    
    print(f"Records to ingest: {bronze_df.count()}")
    
    # Write as Delta (append mode for incremental loads)
    bronze_df.write \
        .format("delta") \
        .mode("overwrite") \
        .save(bronze_path)
    
    print(f"✅ Bronze layer written to {bronze_path}")
    
    # Verify
    bronze_read = spark.read.format("delta").load(bronze_path)
    bronze_read.show(5)
    
    return bronze_read


def process_silver_layer(spark, bronze_path, silver_path):
    """
    SILVER LAYER: Cleaned and validated data.
    - Remove duplicates
    - Handle nulls
    - Add derived fields
    - Type casting
    """
    print("\n" + "=" * 60)
    print("SILVER LAYER: Cleaned Data")
    print("=" * 60)
    
    # Read bronze
    bronze_df = spark.read.format("delta").load(bronze_path)
    print(f"Bronze records: {bronze_df.count()}")
    
    # Step 1: Remove duplicates (keep latest by ingestion time)
    window = Window.partitionBy("order_id").orderBy(col("_ingested_at").desc())
    deduped = bronze_df \
        .withColumn("_row_num", row_number().over(window)) \
        .filter(col("_row_num") == 1) \
        .drop("_row_num")
    print(f"After dedup: {deduped.count()}")
    
    # Step 2: Remove records with null critical fields
    cleaned = deduped.filter(
        col("order_id").isNotNull() & 
        col("customer_id").isNotNull()
    )
    print(f"After null removal: {cleaned.count()}")
    
    # Step 3: Type casting and validation
    silver_df = cleaned \
        .withColumn("event_time", col("event_time").cast(TimestampType())) \
        .withColumn("order_date", to_date(col("event_time"))) \
        .withColumn("total_amount", col("quantity") * col("unit_price")) \
        .withColumn("is_completed", when(col("status") == "COMPLETED", True).otherwise(False)) \
        .withColumn("quantity", when(col("quantity") < 0, 0).otherwise(col("quantity")))
    
    # Step 4: Add processing metadata
    silver_df = silver_df \
        .withColumn("_processed_at", current_timestamp())
    
    # Write to silver
    silver_df.write \
        .format("delta") \
        .mode("overwrite") \
        .partitionBy("order_date") \
        .save(silver_path)
    
    print(f"✅ Silver layer written to {silver_path}")
    
    # Verify
    silver_read = spark.read.format("delta").load(silver_path)
    silver_read.show(5, truncate=False)
    
    return silver_read


def process_gold_layer(spark, silver_path, gold_path_base):
    """
    GOLD LAYER: Business-level aggregates.
    - Daily sales summary
    - Customer analytics
    - Product performance
    """
    print("\n" + "=" * 60)
    print("GOLD LAYER: Business Aggregates")
    print("=" * 60)
    
    # Read silver
    silver_df = spark.read.format("delta").load(silver_path)
    
    # Gold Table 1: Daily Sales Summary
    daily_sales = silver_df \
        .filter(col("is_completed") == True) \
        .groupBy("order_date") \
        .agg(
            count("order_id").alias("total_orders"),
            sum("total_amount").alias("total_revenue"),
            avg("total_amount").alias("avg_order_value"),
            sum("quantity").alias("total_items")
        ) \
        .orderBy("order_date")
    
    daily_sales_path = f"{gold_path_base}/daily_sales"
    daily_sales.write \
        .format("delta") \
        .mode("overwrite") \
        .save(daily_sales_path)
    
    print(f"\n📊 Daily Sales Summary:")
    daily_sales.show()
    
    # Gold Table 2: Customer Summary
    customer_summary = silver_df \
        .filter(col("is_completed") == True) \
        .groupBy("customer_id") \
        .agg(
            count("order_id").alias("total_orders"),
            sum("total_amount").alias("lifetime_value"),
            avg("total_amount").alias("avg_order_value")
        ) \
        .orderBy(col("lifetime_value").desc())
    
    customer_path = f"{gold_path_base}/customer_summary"
    customer_summary.write \
        .format("delta") \
        .mode("overwrite") \
        .save(customer_path)
    
    print(f"👤 Customer Summary:")
    customer_summary.show()
    
    # Gold Table 3: Product Performance
    product_perf = silver_df \
        .filter(col("is_completed") == True) \
        .groupBy("product_id") \
        .agg(
            sum("quantity").alias("total_sold"),
            sum("total_amount").alias("total_revenue"),
            avg("unit_price").alias("avg_price")
        ) \
        .orderBy(col("total_revenue").desc())
    
    product_path = f"{gold_path_base}/product_performance"
    product_perf.write \
        .format("delta") \
        .mode("overwrite") \
        .save(product_path)
    
    print(f"📦 Product Performance:")
    product_perf.show()
    
    print(f"\n✅ Gold layer written to {gold_path_base}/")


def show_delta_history(spark, path, name):
    """Show Delta table history."""
    from delta.tables import DeltaTable
    
    print(f"\n📜 Delta History for {name}:")
    delta_table = DeltaTable.forPath(spark, path)
    delta_table.history(5).select(
        "version", "timestamp", "operation", "operationMetrics"
    ).show(truncate=False)


def main():
    """Main medallion architecture pipeline."""
    print("\n" + "=" * 60)
    print("    MEDALLION ARCHITECTURE PROJECT")
    print("=" * 60 + "\n")
    
    # Paths
    bronze_path = "/tmp/medallion/bronze/orders"
    silver_path = "/tmp/medallion/silver/orders"
    gold_path = "/tmp/medallion/gold"
    
    spark = create_spark_session()
    
    try:
        # Create raw data (simulating source system)
        raw_df = create_raw_data(spark)
        print("📥 Raw Data:")
        raw_df.show()
        
        # Bronze: Raw ingestion
        bronze_df = process_bronze_layer(spark, raw_df, bronze_path)
        
        # Silver: Cleaned data
        silver_df = process_silver_layer(spark, bronze_path, silver_path)
        
        # Gold: Business aggregates
        process_gold_layer(spark, silver_path, gold_path)
        
        # Show Delta history
        show_delta_history(spark, bronze_path, "Bronze")
        
        print("\n" + "=" * 60)
        print("    MEDALLION ARCHITECTURE COMPLETED!")
        print("=" * 60)
        print(f"""
        📂 Data Lake Structure:
        └── medallion/
            ├── bronze/orders     (Raw data)
            ├── silver/orders     (Cleaned, partitioned by date)
            └── gold/
                ├── daily_sales          (Daily KPIs)
                ├── customer_summary     (Customer LTV)
                └── product_performance  (Product metrics)
        """)
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        raise
        
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
