# ETL & Data Integration 🔗

[← Back to Main](../README.md)

Moving data from Point A to Point B is a core part of the job.

---

## [AWS DMS (Database Migration Service)](https://aws.amazon.com/dms/)

Migrate your databases to AWS quickly and securely.

- **Why it matters:** It supports **CDC (Change Data Capture)**, meaning it can stream updates from your production database into your data lake in near real-time.
- **Common Task:** Continuous replication from MySQL/PostgreSQL RDS to S3
### ✅ When to Use (Start Simple → Complex Migrations)

1. **Database Migration (Start: Test 10GB → Prod 500TB)**
   - **Start Simple:** Test migration on dev database (10GB) - validate first
   - **Cost:** $0.19/hour replication instance vs weeks of manual scripting
   - **Complexity:** Point-and-click setup vs custom ETL code
   - **Velocity:** Minimal downtime (CDC = continuous sync during cutover)

2. **Real-time CDC to Data Lake (Cost vs Batch)**
   - **Start:** Replicate 1 critical table → S3 (test: <$5/day)
   - **Scale:** All tables CDC (100GB/day changes) = ~$15/day
   - **Vs Batch:** Nightly snapshots free but 24hr lag
   - **Decision:** Pay $15/day for real-time vs accept daily lag

3. **Multi-Database Consolidation (Complexity justified)**
   - **Use Case:** Merge 5 regional MySQL DBs into one RDS
   - **Why DMS:** Handles schema mapping, data type conversions
   - **Cost:** $0.19/hr × 5 instances = $23/day vs engineer months
   - **Migration path:** Run parallel 2 weeks, validate, cutover

4. **Legacy Modernization (Simplify first, optimize later)**
   - **Start:** Replicate Oracle → PostgreSQL as-is (lift-and-shift)
   - **Benefit:** Immediate 60% cost savings (Oracle → Postgres RDS)
   - **Later:** Refactor schema after migration complete
   - **Philosophy:** Migrate first, optimize second

5. **Disaster Recovery (Low complexity, high value)**
   - **Use Case:** CDC from RDS us-east-1 → RDS eu-west-1
   - **Cost:** $5-10/day for cross-region DR
   - **RPO:** <1 minute (CDC lag)
   - **Complexity:** Set and forget, automatic lag monitoring

### ❌ When NOT to Use

- **File/API data:** DMS is for databases; use DataSync (files) or AppFlow (SaaS APIs)
- **Large BLOB columns:** Replicate slowly; extract to S3 separately
- **Complex transformations:** DMS basic only; land in S3, transform with Glue
- **NoSQL migrations:** Limited support; use native tools for MongoDB/Cassandra
- **Instant cutover needed:** CDC has seconds lag; not for zero-downtime requirements

### Code Example - DMS Task Configuration (boto3)

```python
import boto3
import json

dms = boto3.client('dms')

# Create replication task
response = dms.create_replication_task(
    ReplicationTaskIdentifier='rds-to-s3-cdc',
    SourceEndpointArn='arn:aws:dms:us-east-1:123:endpoint:SOURCE',
    TargetEndpointArn='arn:aws:dms:us-east-1:123:endpoint:TARGET',
    ReplicationInstanceArn='arn:aws:dms:us-east-1:123:rep:INSTANCE',
    MigrationType='cdc',  # Change Data Capture
    TableMappings=json.dumps({
        "rules": [{
            "rule-type": "selection",
            "rule-id": "1",
            "rule-name": "1",
            "object-locator": {
                "schema-name": "public",
                "table-name": "%"
            },
            "rule-action": "include"
        }]
    })
)
```

---

## [Amazon AppFlow](https://aws.amazon.com/appflow/)

A fully managed integration service that enables you to securely transfer data between SaaS applications (like Salesforce, Zendesk, Slack) and AWS services.

- **Why it matters:** Saves you from writing custom API scraper scripts for popular SaaS tools.
- **Common Task:** Pulling Salesforce opportunities data into S3 every hour
- **Pricing:** $0.001 per flow run + $0.001 per GB processed

---

## Related Topics

- **[Databases](03_databases.md)**: Extract data from RDS using DMS
- **[Storage Services](01_storage_services.md)**: Land data in S3
- **[Advanced Services](10_advanced_services.md)**: AWS Transfer Family for SFTP ingestion

[← Back to Main](../README.md)
