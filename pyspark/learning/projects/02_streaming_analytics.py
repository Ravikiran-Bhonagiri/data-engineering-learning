"""
Project 2: Streaming Analytics
==============================
Real-time event processing with windowed aggregations.

Skills: Structured Streaming, Windows, Watermarks

Run: 
1. Start netcat: nc -lk 9999
2. spark-submit 02_streaming_analytics.py
3. Type JSON events in netcat
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    from_json, col, window, count, avg, max, min,
    current_timestamp, expr, to_timestamp
)
from pyspark.sql.types import (
    StructType, StructField,
    StringType, IntegerType, DoubleType, LongType
)


def create_spark_session():
    """Create Spark session for streaming."""
    return SparkSession.builder \
        .appName("Streaming Analytics Project") \
        .config("spark.sql.shuffle.partitions", 10) \
        .getOrCreate()


def get_event_schema():
    """Define the schema for incoming events."""
    return StructType([
        StructField("user_id", StringType(), True),
        StructField("page", StringType(), True),
        StructField("action", StringType(), True),  # click, view, purchase
        StructField("amount", DoubleType(), True),
        StructField("timestamp", LongType(), True),  # Unix timestamp ms
    ])


def create_rate_stream(spark):
    """
    Create a simulated stream using rate source.
    Good for testing without external dependencies.
    """
    print("Creating simulated event stream...")
    
    # Rate source generates 2 rows per second
    rate_df = spark.readStream \
        .format("rate") \
        .option("rowsPerSecond", 2) \
        .load()
    
    # Transform to look like real events
    events = rate_df \
        .withColumn("user_id", expr("concat('user_', cast(value % 10 as string))")) \
        .withColumn("page", expr("""
            CASE 
                WHEN value % 5 = 0 THEN '/home'
                WHEN value % 5 = 1 THEN '/products'
                WHEN value % 5 = 2 THEN '/cart'
                WHEN value % 5 = 3 THEN '/checkout'
                ELSE '/profile'
            END
        """)) \
        .withColumn("action", expr("""
            CASE 
                WHEN value % 3 = 0 THEN 'click'
                WHEN value % 3 = 1 THEN 'view'
                ELSE 'purchase'
            END
        """)) \
        .withColumn("amount", expr("CASE WHEN value % 3 = 2 THEN (value % 100) * 1.5 ELSE 0.0 END")) \
        .withColumn("event_time", col("timestamp"))
    
    return events


def create_socket_stream(spark, schema):
    """
    Create stream from socket (for interactive testing).
    Send JSON: {"user_id":"u1","page":"/home","action":"click","amount":0,"timestamp":1234567890000}
    """
    print("Creating socket stream (localhost:9999)...")
    
    lines = spark.readStream \
        .format("socket") \
        .option("host", "localhost") \
        .option("port", 9999) \
        .load()
    
    # Parse JSON
    events = lines \
        .select(from_json(col("value"), schema).alias("event")) \
        .select("event.*") \
        .withColumn("event_time", to_timestamp(col("timestamp") / 1000))
    
    return events


def compute_page_metrics(events):
    """
    Compute real-time page metrics with 1-minute tumbling windows.
    """
    page_metrics = events \
        .withWatermark("event_time", "2 minutes") \
        .groupBy(
            window(col("event_time"), "1 minute"),
            col("page")
        ).agg(
            count("*").alias("event_count"),
            count("user_id").alias("unique_users"),
            avg("amount").alias("avg_amount")
        ) \
        .select(
            col("window.start").alias("window_start"),
            col("window.end").alias("window_end"),
            "page",
            "event_count",
            "unique_users",
            "avg_amount"
        )
    
    return page_metrics


def compute_user_activity(events):
    """
    Compute user activity with sliding windows.
    5-minute window, sliding every 1 minute.
    """
    user_activity = events \
        .withWatermark("event_time", "5 minutes") \
        .groupBy(
            window(col("event_time"), "5 minutes", "1 minute"),
            col("user_id")
        ).agg(
            count("*").alias("action_count"),
            count(expr("CASE WHEN action = 'purchase' THEN 1 END")).alias("purchases"),
            max("amount").alias("max_purchase")
        ) \
        .select(
            col("window.start").alias("window_start"),
            "user_id",
            "action_count",
            "purchases",
            "max_purchase"
        )
    
    return user_activity


def compute_conversion_funnel(events):
    """
    Real-time conversion funnel metrics.
    """
    funnel = events \
        .withWatermark("event_time", "2 minutes") \
        .groupBy(
            window(col("event_time"), "1 minute")
        ).agg(
            count("*").alias("total_events"),
            count(expr("CASE WHEN page = '/home' THEN 1 END")).alias("home_views"),
            count(expr("CASE WHEN page = '/products' THEN 1 END")).alias("product_views"),
            count(expr("CASE WHEN page = '/cart' THEN 1 END")).alias("cart_views"),
            count(expr("CASE WHEN page = '/checkout' THEN 1 END")).alias("checkouts"),
            count(expr("CASE WHEN action = 'purchase' THEN 1 END")).alias("purchases")
        ) \
        .select(
            col("window.start").alias("window_start"),
            "total_events",
            "home_views",
            "product_views",
            "cart_views",
            "checkouts",
            "purchases"
        )
    
    return funnel


def run_streaming_queries(spark, events, output_mode="console"):
    """Run all streaming queries."""
    
    queries = []
    
    # Query 1: Page Metrics
    print("Starting Page Metrics query...")
    page_metrics = compute_page_metrics(events)
    
    q1 = page_metrics.writeStream \
        .outputMode("update") \
        .format("console") \
        .option("truncate", False) \
        .queryName("page_metrics") \
        .start()
    queries.append(q1)
    
    # Query 2: Conversion Funnel
    print("Starting Conversion Funnel query...")
    funnel = compute_conversion_funnel(events)
    
    q2 = funnel.writeStream \
        .outputMode("update") \
        .format("console") \
        .option("truncate", False) \
        .queryName("conversion_funnel") \
        .trigger(processingTime="30 seconds") \
        .start()
    queries.append(q2)
    
    return queries


def main():
    """Main streaming application."""
    print("\n" + "=" * 60)
    print("    STREAMING ANALYTICS PROJECT")
    print("=" * 60 + "\n")
    
    spark = create_spark_session()
    spark.sparkContext.setLogLevel("WARN")
    
    try:
        # Use rate stream for demo (no external dependencies)
        events = create_rate_stream(spark)
        
        # Uncomment for socket stream testing:
        # schema = get_event_schema()
        # events = create_socket_stream(spark, schema)
        
        # Start queries
        queries = run_streaming_queries(spark, events)
        
        print("\n" + "=" * 60)
        print("    STREAMING STARTED - Press Ctrl+C to stop")
        print("=" * 60 + "\n")
        
        # Keep application running
        for q in queries:
            q.awaitTermination()
            
    except KeyboardInterrupt:
        print("\n\n✅ Streaming stopped by user")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        raise
        
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
