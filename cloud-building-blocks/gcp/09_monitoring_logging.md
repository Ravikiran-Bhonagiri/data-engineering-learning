# Monitoring & Logging 🕵️

[← Back to Main](README.md)

Observability for GCP data pipelines - because "it works on my machine" doesn't cut it in production.

---

## [Cloud Monitoring](https://cloud.google.com/monitoring)

Collect metrics, set alerts, visualize system health (formerly Stackdriver).

- **Why it matters:** Know when pipelines fail before your users complain
- **Common Task:** Alert when BigQuery job fails or Dataflow pipeline lags
- **Pricing:** Free for GCP services metrics; $0.258/GB for custom metrics

### ✅ When to Use (Always - Observability is Essential)

1. **GCP Service Metrics (Free)**
   - **Auto-Collected:** BigQuery query duration, Dataflow lag, Pub/Sub backlog
   - **Dashboards:** Visualize trends over time
   - **Cost:** Free for all GCP service metrics
   - **Why:** Zero cost to monitor all your services

2. **Alerting (Catch failures fast)**
   - **Free Tier:** 150MB/month ingestion, 1024 rules
   - **Alert Policies:** BigQuery job failed, Dataflow stuck, disk full
   - **Notification:** Email, Slack, PagerDuty, SMS
   - **Value:** Know about failures in minutes vs hours

3. **Cost Monitoring (Save money)**
   - **Alert:** Daily BigQuery spend > $100
   - **Catch:** Runaway queries costing thousands
   - **Cost:** Free alerting saves $$$ in waste
   - **ROI:** 10,000x return on monitoring investment

4. **SLO/SLA Tracking (Reliability)**
   - **SLIs:** Pipeline completion time, data freshness
   - **SLOs:** 99.9% of jobs complete in <1 hour
   - **Alerts:** When approaching SLO violation
   - **Dashboard:** Real-time reliability metrics

5. **Custom Application Metrics (When needed)**
   - **Use Case:** Track custom business metrics
   - **Cost:** $0.258/GB (after free tier)
   - **Example:** Records processed, data quality score
   - **When:** Standard metrics insufficient

### ❌ When to Use With Caution

- **High-cardinality metrics WARNING:** Avoid metrics with many unique label values (costs spiral)
- **Excessive custom metrics:** Use sparingly; lean on free GCP metrics first
- **Long-term storage:** Export to BigQuery for cheaper storage (>6 months)

### Code Example - Create Alert

```python
from google.cloud import monitoring_v3

client = monitoring_v3.AlertPolicyServiceClient()
project_name = f"projects/my-project"

# Alert when BigQuery job fails
alert_policy = monitoring_v3.AlertPolicy(
    display_name="BigQuery Job Failures",
    conditions=[{
        "display_name": "Job failure condition",
        "condition_threshold": {
            "filter": 'resource.type="bigquery_project" AND metric.type="bigquery.googleapis.com/job/num_failed_jobs"',
            "comparison": "COMPARISON_GT",
            "threshold_value": 0,
            "duration": {"seconds": 60}
        }
    }],
    notification_channels=[
        "projects/my-project/notificationChannels/12345"
    ]
)

policy = client.create_alert_policy(name=project_name, alert_policy=alert_policy)
print(f"Created alert policy: {policy.name}")
```

### Best Practices

- **Start with basics:** Monitor job failures, costs, latency
- **Use log-based metrics** for custom tracking (cheaper than custom metrics)
- **Set up PagerDuty** for on-call escalation
- **Dashboard for each pipeline** (BigQuery, Dataflow, Pub/Sub)
- **Alert on symptoms, not causes** (data late, not intermediate step failed)

---

## [Cloud Logging](https://cloud.google.com/logging)

Centralized logging for all GCP services.

- **Why it matters:** Debug failures, audit access, understand system behavior
- **Common Task:** View Dataflow worker logs, query BigQuery audit logs
- **Pricing:** First 50GB/month free, then $0.50/GB

### ✅ When to Use (Always - Logs Are Essential)

1. **Automatic GCP Service Logs (Free 50GB)**
   - **Auto-Collected:** BigQuery queries, Dataflow errors, API calls
   - **Retention:** 30 days default (configurable)
   - **Cost:** First 50GB free  = enough for most small teams
   - **Search:** SQL-like query language

2. **Debugging Pipeline Failures**
   - **Use Case:** DataFlow job failed - why?
   - **Logs:** Worker-level errors, stack traces
   - **Velocity:** Find root cause in minutes vs hours
   - **Filters:** Severity=ERROR, time range, specific job

3. **Audit Logging (Compliance)**
   - **Who:** Accessed sensitive BigQuery tables
   - **What:** Deleted Cloud Storage buckets
   - **When:** Made schema changes
   - **Required:** SOC2, HIPAA, GDPR compliance

4. **Log-Based Metrics (Transform logs → metrics)**
   - **Pattern:** Count ERROR logs → alert if >10/min
   - **Cost:** Free (logs already ingested)
   - **vs Custom Metrics:** Avoid $0.258/GB for simple counts
   - **Example:** Track HTTP 500 errors from logs

5. **Export for Long-Term Storage**
   - **Retention:** Default 30 days too short
   - **Export to BigQuery:** $0.01/GB storage vs $0.50/GB logs
   - **Cost Savings:** 98% cheaper for long-term
   - **Analysis:** SQL queries on historical logs

### ❌ When NOT to Use

- **Storing >50GB without optimization:** Export to BigQuery or Cloud Storage to avoid $0.50/GB
- **High-volume debug logs:** Filter at source; don't ingest everything
- **Real-time log processing:** Use Pub/Sub + Dataflow for real-time log analytics

### Code Example - Query Logs

```python
from google.cloud import logging

client = logging.Client()

# Query logs
filter_str = '''
resource.type="bigquery_project"
AND severity="ERROR"
AND timestamp>="2024-01-01T00:00:00Z"
'''

for entry in client.list_entries(filter_=filter_str, max_results=10):
    print(f"{entry.timestamp}: {entry.payload}")
```

### Best Practices

- **Export logs to BigQuery** for analysis (queries on logs!)
- **Use log exclusion filters** to avoid ingesting noisy logs
- **Retention policies** (7 days for debug, 1 year for audit)
- **Log sampling** for high-volume services (1% of requests)
- **Structured logging** (JSON) for easier querying

---

## Related Topics

- **[BigQuery](05_analytics_warehousing.md)**: Query exported logs with SQL
- **[Pub/Sub](06_streaming_messaging.md)**: Real-time log processing
- **[Cost Optimization](12_cost_optimization.md)**: Reduce logging costs

[← Back to Main](README.md)
