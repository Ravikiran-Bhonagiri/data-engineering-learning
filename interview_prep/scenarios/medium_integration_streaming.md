# 🟡 Medium Scenarios 31-40

**Integration, Error Handling & Edge Cases**

---

## Scenario 31: High-Frequency Updates to Delta

**🏷️ Technologies:** `Delta Lake`

### Interview Question
*"Need to update user status every second (millions of updates/day). Delta Lake performance degrading. What's wrong and what's the alternative architecture?"*

### What's Happening
Delta optimized for batch, not single-row updates. Each update creates new file version → write amplification.

### Solution
```
Lambda Architecture:
- Hot Path: Redis/DynamoDB for second-by-second updates
- Cold Path: Batch dump to Delta hourly for analytics
- Serving: Query merges hot (last hour) + cold (historical)
```

---

## Scenario 32: Custom UDF Performance

**🏷️ Technologies:** `PySpark`

### Interview Question
*"Python UDFs on 1TB dataset are bottleneck. What are 3 optimization strategies?"*

### Solutions
1. **Rewrite as Spark SQL:** 10-100× faster (no Python serialization)
2. **Pandas UDF:** Vectorized via Arrow
   ```python
   @pandas_udf("double")
   def multiply(s: pd.Series) -> pd.Series:
       return s * 2
   ```
3. **Scala UDF:** Avoid Python entirely

---

## Scenario 33-40: Advanced Integration Scenarios

### Scenario 33: Stateful Streaming
**Question:** *"Alert if temperature > 100 for 3 consecutive events. Implementation?"*
**Answer:** `mapGroupsWithState` to maintain state across micro-batches.

### Scenario 34: Kafka Schema Evolution
**Question:** *"Producer sends new field 'email' but Consumer fails. How do you prevent this contract break?"*
**Answer:** Use **Confluent Schema Registry**. Enforce compatibility mode (e.g., `BACKWARD`). Producer fails to send if schema doesn't evolve safely (e.g., deleting a required field). Consumer downloads schema ID from registry to deserialize.

### Scenario 35: Lakehouse Federation
**Question:** *"Join Databricks Delta with live Postgres data?"*
**Answer:** Unity Catalog connections with predicate pushdown.

### Scenario 36: Designing a Star Schema (Data Modeling)
**Question:** *"Design a data model for Uber Eats orders to support queries on 'Avg delivery time by restaurant' and 'Revenue by city'. Explain Fact vs Dimension choices."*
**Answer:**
- **Fact Table:** `fact_orders` (order_id, restaurant_id, user_id, time_id, revenue, delivery_seconds). Granularity: One row per order.
- **Dimensions:** `dim_restaurant` (id, name, cuisine), `dim_user` (id, name), `dim_time` (id, day, hour), `dim_location` (id, city, region).
- **Why?** Star schema optimizes for read performance in OLAP (aggregations) vs 3NF which optimizes for writing/OLTP.

### Scenario 37: Multi-Tenancy Design
**Question:** *"10K customers, shared table. Security isolation strategy?"*
**Answer:** Liquid Clustering + Unity Catalog Row Filters.

### Scenario 38: API Downtime Handling
**Question:** *"ETL depends on external API. Handle outages?"*
**Answer:** Airflow retries with exponential backoff. Final failure → PagerDuty.

### Scenario 39: Snapshot SCD Type 2
**Question:** *"Track history for a table without updated_at column in dbt?"*
**Answer:** `materialized='snapshot'` with `strategy='check'`.

### Scenario 40: ML Model Serving Latency
**Question:** *"Spark MLlib too slow for 100ms SLA REST API. Solution?"*
**Answer:** Deploy to Databricks Model Serving (serverless inference). Use Spark only for batch scoring.

---

**Previous:** [Transformations](./medium_transformations.md) | **Next:** [Hard: System Architecture](./hard_system_architecture.md)
