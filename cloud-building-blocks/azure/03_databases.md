# Databases 💾

[← Back to Main](README.md)

Managed database services for operational workloads.

---

## [Azure SQL Database](https://azure.microsoft.com/services/sql-database/)

Fully managed SQL Server database.

- **Why it matters:** Application backend (OLTP), like AWS RDS, GCP Cloud SQL
- **Common Task:** Run transactional applications, extract to Synapse for analytics
- **Pricing:** $5-500+/month depending on tier

### ✅ When to Use

1. **Application Backend (OLTP)**
   - **Start:** Basic tier $5/month (dev/test)
   - **Production:** General Purpose 2 vCore ≈ $180/month
   - **Scale:** Business Critical 8 vCore ≈ $1,450/month
   - **When:** Need ACID transactions

2. **SQL Server Compatibility**
   - **T-SQL:** Full SQL Server features
   - **Migration:** Lift-and-shift from on-prem SQL Server
   - **Tools:** Use existing SQL Server Management Studio

### ❌ When NOT to Use

- **Analytics:** Use Synapse for OLAP
- **NoSQL needed:** Use Cosmos DB
- **Global distribution:** Use Cosmos DB

---

## [Cosmos DB](https://azure.microsoft.com/services/cosmos-db/)

Globally distributed, multi-model NoSQL database.

- **Why it matters:** Low-latency global apps (like AWS DynamoDB, GCP Firestore)
- **Pricing:** $0.008/RU (Request Unit) per hour + storage

### ✅ When to Use

- **Global distribution:** Multi-region writes
- **<10ms latency:** 99th percentile
- **Multi-model:** Document, key-value, graph, column-family

### ❌ When to Use

- **Cost-sensitive:** Can be expensive at scale
- **Complex relational queries:** Use SQL Database

[← Back to Main](README.md)
