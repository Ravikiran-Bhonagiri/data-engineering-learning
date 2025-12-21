# Monitoring & Logging 🕵️

[← Back to Main](README.md)

Observability for Azure data pipelines.

---

## [Azure Monitor](https://azure.microsoft.com/services/monitor/)

Unified monitoring for metrics, logs, and alerts.

- **Pricing:** Metrics free, Logs $2.30/GB ingested

### ✅ When to Use (Always)

1. **Metrics & Alerts**
   - **Free:** All Azure service metrics
   - **Alerts:** Email, SMS, webhook when thresholds breached
   - **Example:** Alert when Synapse query fails

2. **Dashboards**
   - **Visualize:** Pipeline health, costs, performance
   - **Integration:** Power BI, Grafana

### Log Analytics

- **Centralized Logging:** Store logs from all services
- **Query:** Kusto Query Language (KQL)
- **Cost:** $2.30/GB ingested
- **Free Tier:** First 5 GB/month free

### ❌ Cost Management

- **High volume:** Export to Blob Storage for long-term (cheaper)

---

[← Back to Main](README.md)
