"""
Project 1: ETL Pipeline
=======================
Extract data from CSV, transform, and load to Parquet.

Skills: DataFrames, Transformations, Aggregations, File I/O

Run: spark-submit 01_etl_pipeline.py
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, when, sum, avg, count, 
    year, month, dayofmonth, 
    current_timestamp, lit
)
from pyspark.sql.types import (
    StructType, StructField, 
    StringType, IntegerType, DoubleType, DateType
)


def create_spark_session():
    """Create Spark session with appropriate configs."""
    return SparkSession.builder \
        .appName("ETL Pipeline Project") \
        .config("spark.sql.shuffle.partitions", 200) \
        .getOrCreate()


def create_sample_data(spark):
    """Create sample sales data for demonstration."""
    
    data = [
        ("TXN001", 1001, "P001", 2, 29.99, "2025-01-15", "S001"),
        ("TXN002", 1002, "P002", 1, 149.99, "2025-01-15", "S002"),
        ("TXN003", 1001, "P003", 3, 9.99, "2025-01-16", "S001"),
        ("TXN004", 1003, "P001", 1, 29.99, "2025-01-16", "S003"),
        ("TXN005", 1002, "P004", 2, 79.99, "2025-01-17", "S002"),
        ("TXN006", 1004, "P002", 1, 149.99, "2025-01-17", "S001"),
        ("TXN007", 1001, "P005", 5, 4.99, "2025-01-18", "S003"),
        ("TXN008", 1005, "P003", 2, 9.99, "2025-01-18", "S002"),
        ("TXN009", 1003, "P004", 1, 79.99, "2025-01-19", "S001"),
        ("TXN010", 1002, "P001", 3, 29.99, "2025-01-19", "S003"),
        # Add some edge cases
        ("TXN011", None, "P001", 1, 29.99, "2025-01-20", "S001"),  # Null customer
        ("TXN012", 1006, "P006", -1, 19.99, "2025-01-20", "S002"),  # Invalid quantity
    ]
    
    schema = StructType([
        StructField("transaction_id", StringType(), False),
        StructField("customer_id", IntegerType(), True),
        StructField("product_id", StringType(), True),
        StructField("quantity", IntegerType(), True),
        StructField("unit_price", DoubleType(), True),
        StructField("transaction_date", StringType(), True),
        StructField("store_id", StringType(), True),
    ])
    
    return spark.createDataFrame(data, schema)


def extract(spark, source_path=None):
    """
    EXTRACT: Read data from source.
    In production, this would read from CSV/Parquet/Database.
    """
    print("=" * 60)
    print("EXTRACT PHASE")
    print("=" * 60)
    
    if source_path:
        df = spark.read.csv(source_path, header=True, inferSchema=True)
    else:
        # Use sample data for demo
        df = create_sample_data(spark)
    
    print(f"Extracted {df.count()} records")
    df.printSchema()
    df.show(5)
    
    return df


def transform(df):
    """
    TRANSFORM: Clean and enrich data.
    """
    print("=" * 60)
    print("TRANSFORM PHASE")
    print("=" * 60)
    
    # Step 1: Remove nulls in critical fields
    print("Step 1: Removing records with null customer_id...")
    clean_df = df.filter(col("customer_id").isNotNull())
    print(f"  Records after null removal: {clean_df.count()}")
    
    # Step 2: Filter invalid quantities
    print("Step 2: Filtering invalid quantities (<=0)...")
    clean_df = clean_df.filter(col("quantity") > 0)
    print(f"  Records after quantity filter: {clean_df.count()}")
    
    # Step 3: Calculate total amount
    print("Step 3: Calculating total_amount...")
    enriched_df = clean_df.withColumn(
        "total_amount", 
        col("quantity") * col("unit_price")
    )
    
    # Step 4: Add customer segment based on order value
    print("Step 4: Adding customer segment...")
    enriched_df = enriched_df.withColumn(
        "order_segment",
        when(col("total_amount") > 100, "High Value")
        .when(col("total_amount") > 50, "Medium Value")
        .otherwise("Low Value")
    )
    
    # Step 5: Parse date and extract components
    print("Step 5: Parsing dates...")
    enriched_df = enriched_df \
        .withColumn("transaction_date", col("transaction_date").cast(DateType())) \
        .withColumn("year", year(col("transaction_date"))) \
        .withColumn("month", month(col("transaction_date"))) \
        .withColumn("day", dayofmonth(col("transaction_date")))
    
    # Step 6: Add processing metadata
    print("Step 6: Adding metadata...")
    enriched_df = enriched_df \
        .withColumn("processed_at", current_timestamp()) \
        .withColumn("etl_version", lit("1.0.0"))
    
    print("\nTransformed Schema:")
    enriched_df.printSchema()
    enriched_df.show(5, truncate=False)
    
    return enriched_df


def create_aggregates(df):
    """Create aggregate tables for analytics."""
    print("=" * 60)
    print("AGGREGATION PHASE")
    print("=" * 60)
    
    # Daily sales by store
    print("Creating daily store summary...")
    daily_store = df.groupBy("store_id", "transaction_date").agg(
        sum("total_amount").alias("daily_revenue"),
        count("transaction_id").alias("transaction_count"),
        avg("total_amount").alias("avg_order_value"),
        sum("quantity").alias("total_items_sold")
    ).orderBy("transaction_date", "store_id")
    
    print("Daily Store Summary:")
    daily_store.show()
    
    # Customer summary
    print("Creating customer summary...")
    customer_summary = df.groupBy("customer_id").agg(
        count("transaction_id").alias("total_orders"),
        sum("total_amount").alias("lifetime_value"),
        avg("total_amount").alias("avg_order_value")
    ).orderBy(col("lifetime_value").desc())
    
    print("Customer Summary (Top 5):")
    customer_summary.show(5)
    
    return daily_store, customer_summary


def load(df, daily_store, customer_summary, output_path="/tmp/etl_output"):
    """
    LOAD: Write data to destination.
    """
    print("=" * 60)
    print("LOAD PHASE")
    print("=" * 60)
    
    # Write detailed transactions
    transactions_path = f"{output_path}/transactions"
    print(f"Writing transactions to {transactions_path}...")
    df.write \
        .mode("overwrite") \
        .partitionBy("year", "month") \
        .parquet(transactions_path)
    
    # Write daily store summary
    store_path = f"{output_path}/daily_store_summary"
    print(f"Writing store summary to {store_path}...")
    daily_store.write \
        .mode("overwrite") \
        .parquet(store_path)
    
    # Write customer summary
    customer_path = f"{output_path}/customer_summary"
    print(f"Writing customer summary to {customer_path}...")
    customer_summary.write \
        .mode("overwrite") \
        .parquet(customer_path)
    
    print(f"\n✅ ETL Complete! Output written to {output_path}")


def validate_output(spark, output_path="/tmp/etl_output"):
    """Validate the output data."""
    print("=" * 60)
    print("VALIDATION PHASE")
    print("=" * 60)
    
    transactions = spark.read.parquet(f"{output_path}/transactions")
    print(f"✓ Transactions: {transactions.count()} records")
    
    daily_store = spark.read.parquet(f"{output_path}/daily_store_summary")
    print(f"✓ Daily Store Summary: {daily_store.count()} records")
    
    customers = spark.read.parquet(f"{output_path}/customer_summary")
    print(f"✓ Customer Summary: {customers.count()} records")
    
    print("\n✅ Validation Complete!")


def main():
    """Main ETL orchestration."""
    print("\n" + "=" * 60)
    print("    ETL PIPELINE PROJECT")
    print("=" * 60 + "\n")
    
    # Initialize
    spark = create_spark_session()
    
    try:
        # ETL Process
        raw_df = extract(spark)
        transformed_df = transform(raw_df)
        daily_store, customer_summary = create_aggregates(transformed_df)
        load(transformed_df, daily_store, customer_summary)
        validate_output(spark)
        
        print("\n" + "=" * 60)
        print("    ETL PIPELINE COMPLETED SUCCESSFULLY!")
        print("=" * 60 + "\n")
        
    except Exception as e:
        print(f"\n❌ ETL Failed: {str(e)}")
        raise
        
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
