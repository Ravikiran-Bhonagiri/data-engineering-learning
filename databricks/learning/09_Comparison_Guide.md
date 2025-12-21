# Supplemental: Cloud Data Platform Comparison

**Understanding where Databricks fits in the modern stack.**

---

## 1. Databricks vs. Snowflake

| Feature | Databricks | Snowflake |
|---------|------------|-----------|
| **Core DNA** | Spark / Big Data Processing | SQL Data Warehouse |
| **Data Storage** | Open (Your S3/ADLS Bucket) | Proprietary (Internal Stage) |
| **Vendor Lock-in** | Low (Data is open Parquet) | High (Data format is hidden) |
| **Engine** | Photon (C++) | Proprietary SQL Engine |
| **Workloads** | AI/ML + SQL + Streaming | SQL + Light Python (Snowpark) |
| **Pricing** | DBU + Cloud VM Cost | Credits (Compute + Storage) |

**When to choose Databricks?**
- You need heavy ML/AI integration.
- You have massive streaming/engineering workloads.
- You want "Open Format" storage ownership.

**When to choose Snowflake?**
- You want a pure SQL warehouse experience.
- Ease of use is the #1 priority for analysts.

---

## 2. Databricks vs. AWS EMR / Azure Synapse

| Feature | Databricks | EMR / Synapse |
|---------|------------|---------------|
| **Performance** | Faster (Photon + Delta optimizations) | Standard Spark / Proprietary SQL |
| **User Experience** | Unified Workspaces, Notebooks | Disjointed (Storage vs Compute) |
| **Governance** | Unity Catalog (Cross-workspace) | Ranger / Purview (Complex setup) |
| **Cost** | Premium licensing | Lower (closer to raw VM cost) |

---

## 3. The "Lakehouse" Convergence

Competitors are moving towards the middle.

- **Snowflake:** Added Iceberg tables (Open format support) and Snowpark (Python).
- **Databricks:** Added SQL Warehouses (Serverless SQL) and Liquid Clustering.

**Interview Perspective:**
"I prefer Databricks for Data Engineering because of the control over the Spark configurations, the native integration with Delta Lake, and the ability to seamlessly switch between SQL and Python in the same notebook for complex ETL + ML workflows."
