# Advanced Architecture Patterns 🏗️

[← Back to Main](../README.md)

Production-grade patterns for resilience, scalability, and security.

For full implementation details with code examples and Mermaid diagrams, see the comprehensive [aws_services.md](../aws_services.md#️-15-advanced-architecture-patterns) file, Section 15.

---

## Pattern 1: Multi-Region Data Replication

**Use Case:** Disaster recovery, low-latency global access

**Key Features:**
- S3 Cross-Region Replication
- RPO < 15 minutes
- RTO: Minutes (failover to secondary region)

---

## Pattern 2: Data Lake Security - Defense in Depth

**6-Layer Security Model:**
1. Network: VPC endpoints, PrivateLink
2. IAM: Least privilege policies
3. Lake Formation: Table/column/row-level security
4. S3: Bucket policies, encryption (SSE-KMS)
5. KMS: Separate keys per environment/team
6. CloudTrail: Audit all data access

---

## Pattern 3: Incremental Data Processing (SCD Type 2)

**Use Case:** Track historical changes while maintaining current state

**Medallion Architecture:**
```
Raw Zone (Bronze) → Cleaned Zone (Silver) → Curated Zone (Gold)
```

**Key Concept:** Slowly Changing Dimensions Type 2 tracks history with `is_current`, `start_date`, and `end_date` columns.

---

## Pattern 4: Real-Time + Batch Lambda Architecture

**Combine speed layer (real-time) with batch layer (accuracy)**

**Layers:**
- **Speed Layer:** Lambda/Kinesis for approximate real-time metrics (last 5 min)
- **Batch Layer:** Glue for accurate daily aggregations (reconciled)
- **Serving Layer:** Merge both for queries (DynamoDB + Athena)

---

## When to Use These Patterns

| Pattern | When to Use |
|---------|-------------|
| Multi-Region | Global compliance, DR requirements |
| Security Defense | Financial/healthcare data, PII |
| SCD Type 2 | Need historical tracking (customer changes, prices) |
| Lambda Architecture | Real-time dashboards + accurate reporting |

---

## Related Topics

- **[Architecture Patterns](11_architecture_patterns.md)**: Basic patterns for getting started
- **[Governance & Catalog](07_governance_catalog.md)**: Security fundamentals  
- **Full Guide**: [aws_services.md - Section 15](../aws_services.md#️-15-advanced-architecture-patterns)

[← Back to Main](../README.md)
