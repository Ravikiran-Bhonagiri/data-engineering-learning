# Data Integration 🔄

[← Back to Main](README.md)

Move, transform, and orchestrate data across Azure and beyond.

---

## [Azure Data Factory](https://azure.microsoft.com/services/data-factory/)

Cloud-based ETL/ELT and data orchestration service.

- **Why it matters:** Azure's visual ETL tool (like AWS Glue, GCP Dataflow)
- **Common Task:** Extract data from sources, transform, load to destinations
- **Pricing:** $1/1,000 activities + $0.25/DIU-hour (Data Integration Units)

### ✅ When to Use (Visual ETL)

1. **No-Code/Low-Code ETL**
   - **Visual Designer:** Drag-and-drop pipelines
   - **Activities:** Copy, transform, orchestrate
   - **Cost:** 1K dailypipeline runs = $30/month (activities only)
   - **When:** Team lacks Spark expertise

2. **Data Movement at Scale**
   - **DIU:** Parallel data movement units
   - **Example:** Copy 1TB = 10 DIU × 1 hr = $2.50
   - **100+ Connectors:** SAP, Salesforce, Oracle, etc.
   - **When:** Need pre-built connectors

3. **Orchestration (Trigger & Monitor)**
   - **Schedule:** Daily, hourly, event-based
   - **Dependencies:** Chain activities
   - **Monitoring:** Built-in dashboards
   - **When:** Coordinate multi-step workflows

### ❌ When NOT to Use

- **Complex Spark logic:** Use Databricks for advanced transformations
- **Real-time (<1 min):** Use Event Hubs + Stream Analytics
- **Cost-sensitive with heavy compute:** Databricks with spot instances might be cheaper

---

## [Event Hubs](https://azure.microsoft.com/services/event-hubs/)

Big data streaming and event ingestion service.

- **Why it matters:** Ingest millions of events/second (like AWS Kinesis, GCP Pub/Sub)
- **Common Task:** Real-time clickstream, telemetry, log ingestion
- **Pricing:** Basic $0.028/hr, Standard $0.015/hr/unit, Premium $1.046/hr/unit

### ✅ When to Use (High-Throughput Streaming)

1. **Millions of Events/Second**
   - **Throughput:** 1 MB/s/unit (Standard), 8 MB/s/unit (Premium)
   - **Cost:** Standard 1 unit = $11/month (1 MB/s)
   - **Retention:** 1-7 days (Standard), 90 days (Premium)
   - **When:** Need >1 MB/s throughput

2. **Real-Time Analytics Pipeline**
   - **Pattern:** Event Hubs → Stream Analytics → Synapse
   - **Latency:** Seconds
   - **Example:** Real-time dashboard updates
   - **When:** Need <1 minute end-to-end

### ❌ When NOT to Use

- **Low volume (<100 KB/s):** Service Bus cheaper
- **Need transactions:** Use Service Bus for ACID
- **Batch acceptable:** Data Factory cheaper

---

[← Back to Main](README.md)
