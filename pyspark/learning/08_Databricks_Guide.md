# Databricks Guide

**Using PySpark on Databricks managed platform.**

---

## 🏠 What is Databricks?

Databricks is a managed Spark platform:
- **No cluster management** - scales automatically
- **Notebooks** - interactive development
- **Unity Catalog** - data governance
- **Delta Lake** - built-in
- **MLflow** - ML lifecycle management

---

## 🚀 Getting Started

### 1. Create Workspace
1. Go to [databricks.com](https://databricks.com)
2. Sign up (free trial available)
3. Create workspace

### 2. Create Cluster
1. Compute → Create Cluster
2. Select runtime (e.g., 13.3 LTS)
3. Choose node type and count
4. Create

### 3. Create Notebook
1. Workspace → Create → Notebook
2. Attach to cluster
3. Start coding!

---

## 📝 Databricks Notebooks

```python
# spark is pre-initialized!
df = spark.read.parquet("/data/sales")

# Display with rich formatting
display(df)

# Run SQL
%sql
SELECT * FROM sales LIMIT 10

# Magic commands
%python  # Python
%sql     # SQL
%scala   # Scala
%r       # R
%md      # Markdown
%sh      # Shell
```

---

## 📂 File System (DBFS)

```python
# List files
dbutils.fs.ls("/")

# Read file
df = spark.read.csv("/FileStore/data.csv")

# Write file
df.write.parquet("/FileStore/output")

# Upload via UI: Data → Add Data
```

**Paths:**
- `/FileStore/` - Persistent storage
- `/mnt/` - Mounted external storage (S3, ADLS)

---

## 🔗 Mount External Storage

### S3

```python
dbutils.fs.mount(
    source="s3a://my-bucket",
    mount_point="/mnt/my-bucket",
    extra_configs={
        "fs.s3a.access.key": dbutils.secrets.get("scope", "aws-access-key"),
        "fs.s3a.secret.key": dbutils.secrets.get("scope", "aws-secret-key")
    }
)

# Now accessible as
df = spark.read.parquet("/mnt/my-bucket/data")
```

### Azure ADLS

```python
configs = {
    "fs.azure.account.auth.type": "OAuth",
    "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
    "fs.azure.account.oauth2.client.id": "<app-id>",
    "fs.azure.account.oauth2.client.secret": dbutils.secrets.get("scope", "secret"),
    "fs.azure.account.oauth2.client.endpoint": "https://login.microsoftonline.com/<tenant>/oauth2/token"
}

dbutils.fs.mount(
    source="abfss://container@storage.dfs.core.windows.net/",
    mount_point="/mnt/data",
    extra_configs=configs
)
```

---

## 🔐 Secrets Management

```python
# Create scope (via CLI)
# databricks secrets create-scope --scope my-scope

# Add secret (via CLI)
# databricks secrets put --scope my-scope --key api-key

# Use in notebook
api_key = dbutils.secrets.get("my-scope", "api-key")
```

---

## 📊 Delta Lake on Databricks

```python
# Create Delta table
df.write.format("delta").save("/delta/my_table")

# Register as table
spark.sql("CREATE TABLE my_table USING DELTA LOCATION '/delta/my_table'")

# MERGE (upsert)
%sql
MERGE INTO target t
USING source s
ON t.id = s.id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *

# Time travel
df = spark.read.format("delta").option("versionAsOf", 5).load("/delta/my_table")

# Optimize
%sql
OPTIMIZE my_table ZORDER BY (id)
```

---

## 🤖 MLflow Integration

```python
import mlflow
import mlflow.spark

# Enable autolog
mlflow.autolog()

# Train model
from pyspark.ml.classification import LogisticRegression

lr = LogisticRegression()
model = lr.fit(train_df)

# Log manually
with mlflow.start_run():
    mlflow.log_param("maxIter", 10)
    mlflow.log_metric("accuracy", 0.95)
    mlflow.spark.log_model(model, "model")
```

---

## ⏰ Job Scheduling

### Create Job
1. Workflows → Create Job
2. Add task (notebook, Python, JAR)
3. Set schedule (cron)
4. Configure cluster
5. Create

### Programmatic
```python
# Install databricks-sdk
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()
job = w.jobs.create(
    name="Daily ETL",
    tasks=[{
        "task_key": "etl",
        "notebook_task": {"notebook_path": "/Repos/etl/main"}
    }]
)
```

---

## 🧪 Databricks Widgets (Parameters)

```python
# Create widget
dbutils.widgets.text("start_date", "2025-01-01")
dbutils.widgets.dropdown("env", "dev", ["dev", "prod"])

# Get value
start_date = dbutils.widgets.get("start_date")

# Remove
dbutils.widgets.remove("start_date")
dbutils.widgets.removeAll()
```

---

## 📦 Install Packages

```python
# In notebook
%pip install requests pandas

# Cluster-scoped: Cluster → Libraries → Install

# Init script for all clusters
dbutils.fs.put("/databricks/init/install.sh", """
pip install custom-package
""")
```

---

## 🎯 Best Practices

- [ ] Use Delta Lake for all tables
- [ ] Store secrets in Secret Scopes
- [ ] Version notebooks with Repos
- [ ] Use job clusters for production
- [ ] Enable autoscaling
- [ ] Use Unity Catalog for governance
- [ ] Set up monitoring with Overwatch

---

**Databricks makes PySpark production-ready!** 🚀
