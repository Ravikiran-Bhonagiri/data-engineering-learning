# 🔴 Hard Scenarios 01-10

**System Architecture & Design Patterns**

---

## Scenario 1: Blue/Green Deployment (Petabyte Scale)

**🏷️ Technologies:** `Databricks` `Delta Lake` `dbt`

## Scenario 1: Blue/Green Deployment (Petabyte Scale)

**🏷️ Technologies:** `Databricks` `Delta Lake` `dbt`

### Interview Question
*"You are the Lead Data Engineer for a major e-commerce platform. The business requires a schema partitioning change on the core `fact_orders` table (50TB, 200 billion rows) to support a new regional analytics dashboard. The current partitioning is by `order_date`, but query performance demands partitioning by `(region, order_date)`.
**Constraint:** The system operates 24/7 with a strict zero-downtime requirement. You cannot lock the table for more than a few seconds.
**Question:** How do you execute this migration while ensuring data consistency and zero impact on live ingestion pipelines?"*

---

## Scenario 2: Row-Level Security at Scale

**🏷️ Technologies:** `Databricks` `Unity Catalog`

### Interview Question
*"Your company provides a multi-tenant B2B analytics platform serving 50,000 corporate customers. All data resides in a single 100TB `fact_usage` table.
**Problem:** A security audit revealed that analysts often accidentally query data belonging to other customers.
**Requirement:** Implement a security mechanism where a query like `SELECT * FROM fact_usage` automatically returns ONLY the data belonging to the user's specific `tenant_id`, with zero risk of cross-tenant data leakage. This must be applied at the storage engine level, not in the BI tool. How do you design this?"*

---

## Scenario 3: Disaster Recovery (Multi-Region)

**🏷️ Technologies:** `Databricks` `Delta Lake` `Terraform` `Airflow`

### Interview Question
*"Your production data platform runs entirely in AWS `us-east-1` (Northern Virginia). New banking regulations require your critical financial reporting pipelines to survive a total regional failure of `us-east-1` with a Recovery Time Objective (RTO) of less than 1 hour.
**Scope:** 500TB of Delta tables, 50 Airflow DAGs, and 200 daily Databricks jobs.
**Question:** Design a Disaster Recovery (DR) architecture that meets this 1-hour RTO. Specifically, address how you handle metadata replication, data syncing (Active-Passive vs Active-Active), and the failover trigger mechanism."*

### Solution

**Data Replication (Every 30 min):**
```python
def replicate_table(table, source, dr):
    spark.sql(f"""
        INSERT INTO dr_{table}
        SELECT * FROM prod_{table}
        WHERE _commit_timestamp > (
            SELECT MAX(_commit_timestamp) FROM dr_{table}
        )
    """)
```

**Metadata (IaC):**
```hcl
resource "databricks_catalog" "dr_gold" {
  provider = databricks.us_west_2
  storage_location = "s3://dr-us-west-2/gold/"
}
```

**Failover (Automated):**
```bash
# 1. DNS failover
aws route53 change-resource-record-sets...

# 2. Activate Airflow in DR
kubectl set env deployment/airflow ENABLED=true --context us-west-2
```

### Follow-Up
1. **"RPO (Recovery Point Objective)?"**
   - 30 minutes (replication frequency)
2. **"How to test DR without impacting prod?"**
   - Monthly drill: point test app to DR, run synthetic queries

---

## Scenario 4-10: Additional Hard Architecture Questions

### Scenario 4: GDPR Right to Erasure
**Question:** *"User exercises GDPR delete across 500 tables, 3 regions, including ML models and backups. Implementation?"*
**Answer:** Lineage discovery → DELETE → VACUUM RETAIN 0 → Retrain models → Glacier restore/filter.

### Scenario 5: Lakehouse Federation  
**Question:** *"Join Databricks + Postgres + Snowflake without moving data?"*
**Answer:** Unity Catalog connections with predicate pushdown.

### Scenario 6: Lambda Architecture
**Question:** *"Real-time fraud detection <1sec latency + daily model retraining?"*
**Answer:** Kafka → Flink (speed) + Spark batch (accuracy). Serving layer merges.

### Scenario 7: Eventual Consistency
**Question:** *"S3 write then immediate list = file missing. Why?"*
**Answer:** Legacy object store issue. Modern S3 is strongly consistent. Use Delta Lake for ACID.

### Scenario 8: Idempotent REST API Writes
**Question:** *"Spark writes to API with no transactions. Crash creates duplicates. Fix?"*
**Answer:** Change API to PUT (upsert) or accept duplicates and dedup on read side.

### Scenario 9: Bloom Filters
**Question:** *"1PB table, fast `user_id='abc'` lookup?"*
**Answer:** Bloom filter index + ZORDER for file skipping.

### Scenario 10: CI/CD State Drift  
**Question:** *"Test incremental models on stale data causes false positives?"*
**Answer:** `SHALLOW CLONE prod` for CI to test on fresh state.

---

**Next:** [Advanced Patterns](./hard_advanced_patterns.md)
