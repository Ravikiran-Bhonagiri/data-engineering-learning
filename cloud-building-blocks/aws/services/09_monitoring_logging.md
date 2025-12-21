# Monitoring & Logging 🕵️

[← Back to Main](../README.md)

"Is the pipeline running? Did it fail? Why?"

---

## [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/)

Monitoring and observability service that provides data and actionable insights to monitor your applications.

- **Why it matters:** This is where your logs go. You can set **Alarms** to notify you on Slack or Email if a job fails.
- **Common Task:** Setting up alerts for Glue job failures or high error rates
- **Pricing:** $0.50 per GB ingested, first 5GB free

### ✅ When to Use (Observability is Always Worth It)

1. **Start Free, Scale as Needed**
   - **Free tier:** 5GB logs/month, 10 alarms - perfect for small projects
   - **Cost evolution:** Typical app: 10GB = $2.50/month
   - **vs Downtime:** $3/month monitoring vs hours debugging outages
   - **Philosophy:** Always monitor; cost trivial compared to incident cost

2. **Operational Alerts (Catch failures fast)**
   - **Use Case:** Alert when Glue job fails
   - **Cost:** 1 alarm free, $0.10/alarm after that
   - **Value:** Know about failures in minutes vs hours/days
   - **Velocity:** Slack/PagerDuty notification < 1 minute

3. **Cost Monitoring (Save money)**
   - **Alert:** Daily spend > $100/day
   - **Catch:** Runaway EMR cluster left on ($1,000+ waste)
   - **Cost:** $0.10/alarm saves hundreds/thousands
   - **ROI:** 10,000x return on alarm cost

4. **Performance Metrics (Free for AWS services)**
   - **Free:** Glue job duration, Athena query time, Lambda invocations
   - **Graph:** Visualize trends over time
   - **Dashboards:** Create without code
   - **Complexity:** Point-and-click, no setup

5. **Log Aggregation (Centralize troubleshooting)**
   - **Start:** Lambda logs (automatic, no setup)
   - **Scale:** Index all application logs
   - **Insights:** SQL-like queries on logs
   - **vs Scattered:** One place vs SSHing into servers

### ❌ When NOT to Use

- **Long-term storage (>months):** Export to S3 ($0.023/GB cheaper than CloudWatch $0.50/GB)
- **Complex log analytics:** OpenSearch better for complex queries, full-text search
- **High-volume metrics:** Consider Prometheus/Grafana for very high cardinality
- **never skip monitoring:** CloudWatch cheap enough to always use for basics

### Code Example - Create CloudWatch Alarm

```python
import boto3

cloudwatch = boto3.client('cloudwatch')

# Create alarm for failed Glue jobs
cloudwatch.put_metric_alarm(
    AlarmName='GlueJobFailures',
    ComparisonOperator='GreaterThanThreshold',
    EvaluationPeriods=1,
    MetricName='FailedJobs',
    Namespace='AWS/Glue',
    Period=300,
    Statistic='Sum',
    Threshold=1.0,
    ActionsEnabled=True,
    AlarmActions=['arn:aws:sns:us-east-1:123456789:data-alerts'],
    AlarmDescription='Alert when Glue job fails'
)
```

---

## [AWS CloudTrail](https://aws.amazon.com/cloudtrail/)

Track user activity and API usage across your AWS infrastructure.

- **Why it matters:** Audit who made what changes and when. Essential for compliance and debugging.
- **Common Task:** Investigating who deleted a critical S3 object
- **Pricing:** First copy of management events free, then $2 per 100,000 events

### Best Practices

- Enable CloudTrail in all regions
- Send logs to a dedicated S3 bucket with strict access controls
- Use **CloudWatch Logs Insights** to query logs with SQL-like syntax

---

## Related Topics

- **[Daily Workflow](16_daily_workflow.md)**: Phase 5 - Monitoring your pipelines
- **[Governance & Catalog](07_governance_catalog.md)**: CloudTrail for security audits
- **[Cost Optimization](13_cost_optimization.md)**: Monitor costs with CloudWatch

[← Back to Main](../README.md)
