# Data Integration 🔄

[← Back to Main](README.md)

Moving and transforming data between systems in GCP.

---

## [Data Fusion](https://cloud.google.com/data-fusion)

Fully managed, cloud-native data integration service based on CDAP (Cask Data Application Platform).

- **Why it matters:** Visual ETL builder for users who don't want to write code
- **Common Task:** Build drag-and-drop pipelines to move data from Cloud SQL → BigQuery
- **Pricing:** ~$0.35/hour (Basic) to ~$3.50/hour (Enterprise) + compute costs

### ✅ When to Use (Visual ETL, No-Code)

1. **Visual Pipeline Builder (No coding required)**
   - **Users:** Business analysts, citizen data engineers
   - **Complexity:** Drag-and-drop vs writing Dataflow code
   - **Cost:** $0.35/hr × 8 hrs/day × 22 days = ~$62/month (Basic)
   - **When:** Team lacks Python/Java skills

2. **Pre-Built Connectors (150+ sources)**
   - **Databases:** Oracle, SAP, Salesforce, MySQL
   - **No Custom Code:** vs writing Dataflow connectors
   - **Time-to-Value:** Hours vs weeks
   - **Example:** SAP → BigQuery without writing code

3. **Data Quality & Lineage**
   - **Built-in:** Data profiling, validation rules
   - **Lineage:** Track data flow automatically
   - **Governance:** See where data comes from
   - **When:** Compliance/audit requirements

### ❌ When NOT to Use

- **Need custom logic:** Dataflow offers more flexibility
- **Cost-sensitive:** $0.35+/hour runs 24/7 = $250+/month minimum; Dataflow pay-per-job
- **Developers comfortable with code:** Dataflow more powerful and cost-effective
- **Simple transformations:** BigQuery SQL cheaper than running Data Fusion

---

## [Datastream](https://cloud.google.com/datastream)

Serverless change data capture (CDC) and replication service.

- **Why it matters:** Real-time replication from databases to BigQuery/Cloud Storage
- **Common Task:** Stream Oracle/MySQL changes to BigQuery for analytics
- **Pricing:** ~$0.04/GB processed

### ✅ When to Use (Real-Time CDC)

1. **Database Replication (Near real-time)**
   - **Pattern:** MySQL → Datastream → BigQuery
   - **Latency:** Seconds to minutes
   - **Cost:** 100GB/day changes = $4/day = $120/month
   - **vs Batch:** Real-time vs daily exports

2. **Change Data Capture (CDC)**
   - **Captures:** INSERT, UPDATE, DELETE operations
   - **Use Case:** Keep analytics warehouse in sync with OLTP
   - **Example:** Orders table changes → BigQuery immediately
   - **When:** Need <5 minute data freshness

3. **Minimal Impact on Source**
   - **Low Overhead:** Uses database logs (not queries)
   - **Production Safe:** Doesn't slow down application
   - **vs DMS:** Similar to AWS DMS for GCP
   - **When:** Can't afford production impact

### ❌ When NOT to Use

- **Batch acceptable:** Daily batch exports via Cloud SQL export cheaper
- **Unsupported databases:** Limited to Oracle, MySQL, PostgreSQL, SQL Server
- **Very high volume:** $0.04/GB can be expensive for TB/day changes
- **One-time migration:** Use Database Migration Service for one-time moves

---

## Native Integration Options

### BigQuery Data Transfer Service
- **Purpose:** Scheduled data loads from SaaS (Google Ads, YouTube)
- **Cost:** Free for first-party transfers
- **When:** Need Google product data

### Cloud SQL Export
- **Purpose:** Batch export to Cloud Storage
- **Cost:** Free (except storage/compute)
- **When:** Daily/hourly refresh acceptable

### Pub/Sub to BigQuery
- **Purpose:** Streaming inserts from Pub/Sub
- **Cost:** Just Pub/Sub costs
- **When:** Application publishes events

---

## Related Topics

- **[Databases](03_databases.md)**: Source systems for integration
- **[BigQuery](05_analytics_warehousing.md)**: Common destination
- **[Dataflow](02_compute_processing.md)**: Custom ETL when needed

[← Back to Main](README.md)
