# Performance Tuning 🚀

[← Back to Main](README.md)

Optimize Azure data pipelines for speed and efficiency.

---

## Synapse Dedicated SQL Performance

### 1. Distribution Strategies

```sql
-- HASH distribution for large tables
CREATE TABLE Sales
WITH (DISTRIBUTION = HASH(OrderID))
AS SELECT * FROM Source;

-- ROUND_ROBIN for staging/temp
CREATE TABLE Staging
WITH (DISTRIBUTION = ROUND_ROBIN)
AS SELECT * FROM Source;

-- REPLICATE for small dimension tables (<2GB)
CREATE TABLE DimProduct
WITH (DISTRIBUTION = REPLICATE)
AS SELECT * FROM Source;
```

**Impact:** 10-100x faster joins

### 2. Partitioning

```sql
CREATE TABLE Orders
WITH (
    DISTRIBUTION = HASH(OrderID),
    PARTITION (OrderDate RANGE RIGHT 
        FOR VALUES ('2024-01-01', '2024-02-01', '2024-03-01'))
)
AS SELECT * FROM Source;
```

### 3. Statistics

```sql
-- Update statistics after large data loads
CREATE STATISTICS stat_OrderDate ON Orders(OrderDate);
```

### 4. Result Set Caching

```sql
-- Enable for frequently queried results
SET RESULT_SET_CACHING ON;
```

---

## Data Factory Performance

### 1. Increase DIU (Data Integration Units)

- **Default:** Auto (4-256 DIU)
- **Large datasets:** Manually set higher DIU
- **Cost:** More DIU = faster but more expensive

### 2. Parallel Copies

- **Partition data source** for parallel reads
- **Use multiple files** instead of one large file

### 3. Mapping Data Flows

- **Partition optimization:** Set optimal partition count
- **Cluster size:** Use larger clusters for big data

---

## Databricks Performance

### 1. Cluster Configuration

```python
# Optimize Spark configs
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
```

### 2. Delta Lake Optimization

```python
# Z-ORDER for frequently filtered columns
OPTIMIZE delta.`/path/to/table` ZORDER BY (customer_id, date)

# VACUUM to remove old files
VACUUM delta.`/path/to/table` RETAIN 168 HOURS
```

### 3. Caching

```python
# Cache frequently accessed DataFrames
df = spark.read.parquet("/path").cache()
```

---

## Blob Storage Performance

### 1. Use Premium Block Blobs

- **Standard:** Good for most workloads
- **Premium:** Low latency, high IOPS
- **When:** Performance-critical applications

### 2. Optimize File Sizes

- **Too small:** Overhead from many files
- **Too large:** Can't parallelize
- **Sweet spot:** 128-256MB per file for Spark

---

## Monitoring Performance

1. **Synapse:** Query performance insights
2. **Data Factory:** Pipeline run monitoring
3. **Databricks:** Spark UI, cluster metrics
4. **Azure Monitor:** End-to-end tracking

---

## Quick Checklist

- [ ] Synapse tables use appropriate distribution
- [ ] Large tables partitioned by date
- [ ] Statistics updated regularly
- [ ] Data Factory uses sufficient DIU
- [ ] Databricks clusters right-sized
- [ ] Delta tables optimized with Z-ORDER
- [ ] File sizes optimized (128-256MB)

[← Back to Main](README.md)
