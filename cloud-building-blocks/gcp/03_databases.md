# Databases 💾

[← Back to Main](README.md)

Managed relational and NoSQL databases for operational workloads.

---

## [Cloud SQL](https://cloud.google.com/sql)

Fully managed MySQL, PostgreSQL, and SQL Server databases.

- **Why it matters:** Cloud SQL is for your **application's transactional data** (OLTP). Data engineers **extract** from it into BigQuery for analytics.
- **Common Task:** Running application backends, extracting to BigQuery for analytics
- **Pricing:** Starting at ~$0.0315/hour (db-f1-micro) to ~$1.40/hour (db-n1-standard-4)

### ✅ When to Use (Operational Workloads)

1. **Application Backend (Start: Free Tier → Scale)**
   - **Start:** db-f1-micro (0.6GB RAM) ~$23/month for dev/test
   - **Production:** db-n1-standard-2 (7.5GB RAM) ~$140/month
   - **Scale:** db-n1-standard-16 (60GB RAM) ~$1,130/month
   - **Why:** Fully managed (backups, HA, patching)

2. **ACID Transactions Required**
   - **Use Case:** E-commerce orders, financial transactions, user accounts
   - **Why Cloud SQL:** Strong consistency, row-level locking
   - **NOT for:** Analytics (use BigQuery), logs (use Cloud Storage)
   - **Cost vs Firestore:** Cloud SQL cheaper for complex relational queries

3. **PostgreSQL/MySQL Compatibility**
   - **Migration:** Lift-and-shift from on-prem
   - **Ecosystem:** Use existing drivers, ORMs, tools
   - **Extensions:** PostGIS, pgvector, etc.
   - **When:** Need specific DB features not in Spanner

4. **Read Replicas for Analytics (Scale reads)**
   - **Pattern:** Write to primary, read from replicas
   - **Analytics:** Point BI tools at read replica
   - **Cost:** Each replica = full instance cost
   - **Better:** Extract to BigQuery for analytics

5. **High Availability (99.95% SLA)**
   - **Regional HA:** Automatic failover <1 minute
   - **Cost:** ~2x for HA configuration
   - **When:** Production apps needing uptime
   - **vs Single-zone:** Dev/test to save 50%

### ❌ When NOT to Use

- **Analytics workloads:** Cloud SQL for OLTP; BigQuery for OLAP
- **Massive scale (>10TB):** Consider Spanner for planet-scale
- **Key-value only:** Firestore simpler/cheaper for document storage
- **Unstructured data:** Use Cloud Storage for files
- **Cost-sensitive with variable load:** Cloud SQL runs 24/7; can't pause

### Code Example - Connect & Query

```python
import sqlalchemy
from google.cloud.sql.connector import Connector

# Initialize connector
connector = Connector()

def getconn():
    conn = connector.connect(
        "project:region:instance",
        "pg8000",
        user="postgres",
        password="secret",
        db="mydatabase"
    )
    return conn

# Create engine
engine = sqlalchemy.create_engine(
    "postgresql+pg8000://",
    creator=getconn,
)

# Query
with engine.connect() as conn:
    result = conn.execute(sqlalchemy.text("SELECT * FROM users LIMIT 10"))
    for row in result:
        print(row)

connector.close()
```

### Best Practices

- **Enable automatic backups** (configurable retention)
- **Use connection pooling** (Cloud SQL Proxy or built-in)
- **Monitor with Cloud Monitoring** for CPU, connections
- **Export to BigQuery** for analytics (not read replicas)
- **Use Private IP** for security (VPC peering)
- **Size appropriately** (start small, scale up)

---

## [Cloud Spanner](https://cloud.google.com/spanner)

Globally distributed, horizontally scalable relational database.

- **Why it matters:** When you need relational + global scale + strong consistency
- **Common Task:** Multi-region applications requiring ACID across continents
- **Pricing:** $0.90/node-hour (~$650/node/month) for regional, $3/node-hour for multi-region

### ✅ When to Use

- **Global applications:** Users in multiple continents
- **Horizontal scalability:** Need >10TB with ACID
- **Strong consistency:** Unlike eventual consistency of NoSQL
- **High availability:** 99.999% SLA (multi-region)

### ❌ When NOT to Use

- **Small datasets (<10GB):** Way too expensive; use Cloud SQL
- **Single-region apps:** Cloud SQL much cheaper
- **Analytics:** Use BigQuery
- **Cost-constrained:** Minimum $650/month vs Cloud SQL $23/month

---

## [Firestore](https://cloud.google.com/firestore)

Serverless NoSQL document database.

- **Why it matters:** Flexible schema, real-time sync, mobile/web apps
- **Common Task:** User profiles, mobile app data, real-time chat
- **Pricing:** $0.06/100K reads, $0.18/100K writes, $0.18/GB stored

### ✅ When to Use

- **Document model:** Flexible JSON-like documents
- **Real-time sync:** Changes pushed to clients instantly
- **Mobile/Web:** Offline support, easy SDKs
- **Serverless:** Auto-scales, no management

### ❌ When NOT to Use

- **Complex joins:** Use Cloud SQL
- **Analytics:** Use BigQuery (export Firestore data)
- **Large binary files:** Use Cloud Storage
- **Strong relational model:** Use Cloud SQL

---

## Related Topics

- **[BigQuery](05_analytics_warehousing.md)**: Export Cloud SQL data for analytics
- **[Data Integration](04_data_integration.md)**: Replicate Cloud SQL to Data Lake
- **[Service Comparisons](12_service_comparisons.md)**: Cloud SQL vs Spanner vs Firestore

[← Back to Main](README.md)
