# Performance Tuning ⚡

[← Back to Main](../README.md)

Making your data pipelines faster and more efficient.

For full performance tuning details with code examples, see the comprehensive [aws_services.md](../aws_services.md#-14-performance-tuning-deep-dive) file, Section 14.

---

## Quick Performance Wins

### Glue Jobs
- Enable Spark adaptive execution
- Use pushdown predicates (filter at source!)
- Optimize file sizes (128MB-1GB per Parquet file)

### Redshift Queries
- Choose the right distribution keys (DISTKEY)
- Define sort keys for common query patterns
- Run VACUUM and ANALYZE regularly

### Athena Queries
- Always use partition pruning in WHERE clauses
- Enable query result reuse
- Use CTAS for complex queries

### Partition Strategy
- ✅ **Good:** `s3://bucket/data/year=2024/month=12/day=15/`
- ❌ **Bad:** `s3://bucket/data/user_id=12345/` (high cardinality)

### EMR Clusters
- Choose the right instance type:
  - **Memory-intensive**: r5 family
  - **CPU-intensive**: c5 family  
  - **General purpose**: m5 family

---

## Performance Optimization Checklist

✅ Use columnar formats (Parquet/ORC)  
✅ Partition data by time or logical keys  
✅ Right-size compute resources  
✅ Enable caching where applicable  
✅ Monitor and optimize based on metrics  

---

## Related Topics

- **[Cost Optimization](13_cost_optimization.md)**: Faster often means cheaper
- **[Compute & Processing](02_compute_processing.md)**: Glue and EMR best practices  
- **Full Guide**: [aws_services.md - Section 14](../aws_services.md#-14-performance-tuning-deep-dive)

[← Back to Main](../README.md)
