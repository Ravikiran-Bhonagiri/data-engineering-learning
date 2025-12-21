# Compute & Processing ⚙️

[← Back to Main](README.md)

Azure's processing engines for data transformation at scale.

---

## [Azure Databricks](https://azure.microsoft.com/services/databricks/)

Apache Spark-based analytics platform optimized for Azure.

- **Why it matters:** Collaborative notebooks + managed Spark (like AWS EMR, GCP Dataproc)
- **Common Task:** Complex transformations, ML pipelines, interactive analysis
- **Pricing:** ~$0.15/DBU (Data Bricks Unit) + VM costs

### ✅ When to Use

1. **Complex Spark Workloads**
   - **Spark ML, GraphX:** Full Spark ecosystem
   - **Cost:** Standard cluster ≈ $0.40-0.60/hr (DBU + VM)
   - **vs Data Factory:** Better for code-heavy transformations
   - **When:** Need Spark-specific features

2. **Interactive Development**
   - **Notebooks:** Collaborative Python/Scala/SQL
   - **Auto-termination:** Stop idle clusters to save costs
   - **Integration:** Delta Lake, MLflow built-in

3. **Machine Learning Pipelines**
   - **MLflow:** Track experiments, deploy models
   - **AutoML:** Automated model training
   - **When:** Data science team needs Spark + ML

### ❌ When NOT to Use

- **Simple ETL:** Data Factory cheaper and simpler
- **Serverless preference:** Synapse Spark for tighter integration
- **No Spark expertise:** Steep learning curve

---

## [Synapse Spark Pools](https://azure.microsoft.com/services/synapse-analytics/)

Serverless Apache Spark in Synapse workspace.

- **Why it matters:** Spark without cluster management, integrated with Synapse
- **Pricing:** ~$0.319/hour for Small (4 vCores)

### ✅ When to Use

- **Integrated experience:** Same workspace as SQL pools
- **Serverless:** Auto-pause when idle
- **Start simple:** Easier than Databricks for basic Spark

### ❌ When NOT to Use

- **Advanced Spark features:** Databricks more mature
- **Cost optimization:** Databricks spot instances cheaper for long-running

---

## [Azure Functions](https://azure.microsoft.com/services/functions/)

Event-driven serverless compute (like AWS Lambda, GCP Cloud Functions).

- **Pricing:** $0.20/million executions + $0.000016/GB-sec

### ✅ When to Use

- **Lightweight processing:** <10MB files, simple logic
- **Event-driven:** Trigger on blob upload, queue message
- **Cost:** First 1M free/month

### ❌ When NOT to Use

- **Large files (>100MB):** Use Databricks/Synapse
- **Long processing (>10 min):** Functions have timeout limits

[← Back to Main](README.md)
