# Managed Databases 💾

[← Back to Main](README.md)

Where transactional and operational data lives before being extracted into the data lake.

---

## [Amazon RDS (Relational Database Service)](https://aws.amazon.com/rds/)

Managed relational database service supporting MySQL, PostgreSQL, Oracle, SQL Server, and MariaDB.

- **Why it matters:** RDS is for your **application's state** (users, orders, inventory). Data Engineers **extract** this operational data into the Data Lake for analysis.
- **Common Task:** Running OLTP (Online Transaction Processing) workloads
- **Pricing:** Varies by instance type; e.g., db.t3.medium ~$0.068/hour

### ✅ When to Use (Operational Workloads, Not Analytics)

1. **Application Backend (Start: Free Tier → Scale)**
   - **Start Simple:** db.t3.micro free tier (750 hrs/month) - perfect for dev/test
   - **Production:** db.t3.medium ~$50/month (On-Demand) for small app
   - **Scale:** db.r5.xlarge ~$370/month (On-Demand) for high traffic
   - **Why:** Fully managed (backups, patching, HA) vs DIY on EC2

2. **When You Need ACID Transactions**
   - **Use Case:** E-commerce orders, financial transactions
   - **Why RDS:** ACID guarantees, row-level locking
   - **NOT for:** Analytics (use Redshift), append-only logs (use S3)
   - **Cost vs DynamoDB:** RDS cheaper for complex relational queries

3. **Migrate from On-Prem (Cost savings 60%)**
   - **Oracle → RDS PostgreSQL:** Save 60% on licensing
   - **SQL Server → RDS SQL Server:** Reduce operational overhead
   - **Start:** Latest license model (BYOL vs License Included)
   - **Complexity:** DMS for minimal-downtime migration

4. **Reserved Instances (40-60% savings)**
   - **No upfront:** 1-year = 40% off
   - **All upfront:** 3-year = 60% off
   - **Decision:** Commit when usage predictable (>6 months)
   - **Example:** $250/month → $100/month (3-yr reserved)

5. **Multi-AZ for Production (HA trade-off)**
   - **Cost:** 2x price for high availability
   - **RTO:** Automatic failover <2 minutes
   - **When:** Production apps needing 99.95% uptime
   - **vs Single-AZ:** Dev/test environments to save 50%

### ❌ When NOT to Use

- **Analytics workloads:** RDS for OLTP, not OLAP; use Redshift/Athena for analytics
- **Massive scale (>10TB):** Consider Aurora or Redshift for very large databases
- **Key-value lookups only:** DynamoDB cheaper/faster for simple patterns
- **Unstructured data:** RDS for structured; use S3 for files, DynamoDB for documents
- **Cost-sensitive with variable load:** RDS runs 24/7; consider Aurora Serverless for sporadic use

### Integration with Data Engineering

- Use **AWS DMS** to replicate data from RDS to S3 in real-time (CDC)
- Schedule snapshots and export to S3 for historical analysis
- Query directly using Athena Federated Query

---

## Related Topics

- **[ETL & Integration](04_etl_integration.md)**: Extract data from RDS using DMS
- **[Advanced Services](10_advanced_services.md)**: Manage RDS credentials with Secrets Manager
- **[Cost Optimization](13_cost_optimization.md)**: Use Reserved Instances for RDS

[← Back to Main](README.md)
