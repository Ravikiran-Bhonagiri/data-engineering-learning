# Databricks Foundation & Architecture

**Understand the underlying architecture of the Unified Data Analytics Platform.**

---

## 🏛 The Lakehouse Paradigm

Databricks pioneered the **Lakehouse** architecture, combining the best of Data Warehouses and Data Lakes.

| Feature | Data Warehouse | Data Lake | **Lakehouse** |
|---------|----------------|-----------|---------------|
| **Data Type** | Structured | Structured & Unstructured | **All Types** |
| **Cost** | High ($$$) | Low ($) | **Low ($)** |
| **Performance** | Very Fast | Slow (Scan) | **Fast (Delta)** |
| **Governance** | Strong | Weak | **Strong (Unity Catalog)** |
| **Workloads** | BI/SQL | ML/AI | **BI & ML** |

---

## 🏗 E2 Architecture (Control vs. Data Plane)

Databricks uses a decoupled architecture for security and scale.

### 1. Control Plane (Databricks Account)
- Managed by Databricks (ex: AWS US-East-1).
- Houses: Web UI, Notebooks, Job Scheduler, Cluster Manager.
- **NO User Data** is stored here (except notebook code).

### 2. Data Plane (Your Cloud Account)
- Managed by You (Customer VPC).
- **Classic Data Plane:** Clusters run in your VPC (EC2/VMs).
- **Serverless Data Plane:** Compute runs in Databricks' account but processes your data securely.
- **Data Storage:** S3 / ADLS / GCS (Your buckets).

```mermaid
graph TD
    subgraph "Control Plane (Databricks)"
        UI[Web UI / Notebooks]
        Manager[Cluster Manager]
        Jobs[Job Scheduler]
    end

    subgraph "Data Plane (Your Cloud VPC)"
        Clusters[Spark Clusters (VMs)]
        Disk[EBS Volumes]
    end

    subgraph "Storage (Your Cloud Bucket)"
        S3[(S3 / ADLS / GCS)]
    end

    UI --> Clusters
    Manager --> Clusters
    Clusters --> S3
```

---

## 💻 Compute Types

### 1. All-Purpose Compute
- **Usage:** Interactive development (Notebooks).
- **Cost:** Higher (Development pricing).
- **Features:** Autotermination, Autorecovery.

### 2. Job Compute (Automated)
- **Usage:** Scheduled jobs (Production).
- **Cost:** Lower (Job pricing, ~50% specific savings).
- **Lifecycle:** Created for the job, terminated after.

### 3. Serverless SQL Warehouse
- **Usage:** BI Queries, Dashboards, SQL Editor.
- **Start-up:** Instant (seconds).
- **Management:** No cluster config needed.

---

## 📦 Databricks Runtime (DBR)

DBR is the optimized version of Apache Spark running on clusters.
- **DBR Standard:** Optimized Spark + Delta Lake.
- **DBR ML:** Standard + TensorFlow, PyTorch, Scikit-learn, MLflow.
- **Photon:** C++ vectorized query engine (native code) for extreme speed. Use for SQL/DataFrame workloads.

---

## 🔐 Unity Catalog (Governance Layer)

Centralized access control for all data and AI assets across workspaces.

- **Metastore:** Top-level container.
- **Catalog:** Logical grouping (e.g., `prod`, `dev`).
- **Schema:** Database (e.g., `finance`, `marketing`).
- **Table/Volume:** Actual data.

Hierarchy:
`catalog.schema.table` (Three-level namespace)

---

## 🎯 Interview Q&A

**Q: What is the difference between Control Plane and Data Plane?**
A: Control Plane manages the workspace and services (Databricks side). Data Plane processes the actual data (User side VPC). Data stays in the Data Plane.

**Q: Why use Delta Lake over Parquet?**
A: Delta adds ACID transactions, schema enforcement, time travel, and performance optimizations (Z-Order) on top of Parquet.

**Q: When to use Photon engine?**
A: Use Photon for SQL-heavy or DataFrame-heavy workloads. It replaces the JVM execution engine with a C++ engine for faster vectorization. Avoid for UDF-heavy Python code that doesn't use DataFrames.

---

**Next:** [Day 1: Architecture & Platform Setup](./02_Day_01.md)
