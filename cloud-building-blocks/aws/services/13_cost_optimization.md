# Cost Optimization 💰

[← Back to Main](../README.md)

Real-world tactics to reduce your AWS data engineering bill by 30-70%.

For full details on cost optimization strategies, see the comprehensive [aws_services.md](../aws_services.md#-13-cost-optimization-strategies) file, Section 13.

---

## Quick Wins

### S3 Storage: Save 60-80%
- Enable lifecycle policies → move to Glacier after 90 days
- **Savings:** $1,900/month for 100TB

### Athena Queries: Save 95%
- Use Parquet instead of CSV
- Partition your data
- **Savings:** $5 → $0.015 per query

### Glue Jobs: Save 20-50%
- Right-size DPUs (use 2-5 instead of 10 for small jobs)
- Enable job bookmarks
- **Savings:** $3.52/hour

### Redshift: Save 30-60%
- Use Reserved Instances (40-60% discount)
- Pause clusters during idle hours
- **Savings:** $240-300/month

### EMR: Save 60-70%
- Use Spot Instances for task nodes
- Auto-terminate clusters
- **Savings:** 70% discount on compute

---

## Cost Optimization Summary Table

| Strategy | Service | Potential Savings |
|----------|---------|-------------------|
| Use Parquet instead of CSV | Athena | 80-95% |
| Enable S3 Lifecycle Policies | S3 | 60-80% |
| Use Spot Instances | EMR | 60-70% |
| Pause idle clusters | Redshift | 30-40% |
| Right-size DPUs | Glue | 20-50% |
| Use Reserved Instances | Redshift/RDS | 40-60% |

---

## Related Topics

- **[Performance Tuning](14_performance_tuning.md)**: Faster = cheaper
- **[Service Comparisons](12_service_comparisons.md)**: Choose cost-effective services  
- **Full Guide**: [aws_services.md - Section 13](../aws_services.md#-13-cost-optimization-strategies)

[← Back to Main](../README.md)
