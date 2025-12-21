# 🔴 Hard Scenarios 21-30

**Governance, Compliance & Security**

---

## Scenario 21: Implementing Data Lineage

**🏷️ Technologies:** `Unity Catalog`

### Interview Question
*"Compliance audit requires proof that sensitive PII field travels from source → transform → consumer. How do you provide complete lineage trail?"*

### Solution
```sql
-- Unity Catalog auto-tracks column-level lineage
SELECT * FROM system.access.table_lineage 
WHERE table_name = 'gold.user_metrics';

-- Show: raw.events.user_id → gold.user_metrics.user_id → Dashboard
```

Export lineage graph to prove data flow chain.

---

## Scenario 22: Secrets Management

**🏷️ Technologies:** `Databricks` `Airflow`

### Interview Question
*"Junior engineer hardcoded `db_password='1234'` in notebook committed to git. What's the secure approach?"*

### Solution
```python
# Databricks
password = dbutils.secrets.get(scope="prod", key="db_pass")

# Airflow - Secrets Backend
conn = Connection.get_connection_from_secrets("postgres_prod")

# NEVER store in Airflow Variables (visible in UI!)
```

---

## Scenario 23-30: Governance Deep Dives

### Scenario 23: Audit Logging
**Question:** *"Track who queried PII tables?"*
**Answer:** `SELECT * FROM system.access.audit WHERE query_text LIKE '%pii_table%'`.

### Scenario 24: Encryption
**Question:** *"HIPAA compliance requires encryption at rest and in transit. Implementation?"*
**Answer:** S3 AES-256 (rest) + TLS (transit) + Unity Catalog credential passthrough.

### Scenario 25: RBAC Design
**Question:** *"Design role-based access: analysts see aggregated, engineers see raw?"*
**Answer:** `GRANT SELECT ON gold TO analysts`, column masking for PII.

### Scenario 26: CDC at Scale
**Question:** *"Replicate 1000 Postgres tables to lakehouse <5min latency?"*
**Answer:** Debezium → Kafka → Spark Structured Streaming → Delta MERGE.

### Scenario 27: PII Handling
**Question:** *"4 approaches to handling PII in analytics?"*
**Answer:** Masking, tokenization, column masking (Unity), separate storage.

### Scenario 28: Cost Attribution
**Question:** *"Chargeback per team on shared Databricks cluster?"*
**Answer:** Tag jobs with `team=marketing`. Query `system.billing.usage` grouped by tag.

### Scenario 29: Data Retention
**Question:** *"GDPR: delete data after 7 years. Implementation?"*
**Answer:** Monthly Airflow DAG: `ALTER TABLE DROP PARTITION` for old dates.

### Scenario 30: Data Catalog
**Question:** *"10K tables, no one knows what's what. Solution?"*
**Answer:** Unity Catalog + tagging: `ALTER TABLE SET TAGS ('owner'='finance', 'pii'='true')`.

---

**Previous:** [Advanced Patterns](./hard_advanced_patterns.md) | **Next:** [Scaling Challenges](./hard_scaling_challenges.md)
