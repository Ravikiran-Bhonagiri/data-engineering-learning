# Orchestration 🎼

[← Back to Main](README.md)

Coordinate and schedule data workflows.

---

## [Azure Data Factory - Orchestration](https://azure.microsoft.com/services/data-factory/)

See [Data Integration](04_data_integration.md) for ETL features. This covers orchestration.

### ✅ Orchestration Features

1. **Pipeline Triggers**
   - **Schedule:** Hourly, daily, custom cron
   - **Event:** Blob created, other pipelines complete
   - **Tumbling Window:** Backfill historical data

2. **Control Flow**
   - **If/Switch:** Conditional logic
   - **ForEach:** Iterate over datasets
   - **Until:** Loop with condition

3. **Monitoring**
   - **Built-in:** Pipeline runs, activity duration
   - **Alerts:** Integration with Azure Monitor
   - **Cost:** $1/1,000 activities

### vs Alternatives

- **Simple (<10 steps):** Logic Apps for non-data workflows
- **Complex DAGs:** Consider Apache Airflow on VMs for advanced features

---

## [Logic Apps](https://azure.microsoft.com/services/logic-apps/)

Workflow automation for business processes.

- **Pricing:** $0.000025/action (Consumption), $160/month (Standard)

### ✅ When to Use

- **Business workflows:** Email notifications, approvals
- **SaaS integration:** Office 365, Salesforce, SharePoint
- **Simple automation:** Non-data-engineering tasks

### ❌ When NOT to Use

- **Data pipelines:** Use Data Factory
- **Complex transformations:** Use Databricks

[← Back to Main](README.md)
