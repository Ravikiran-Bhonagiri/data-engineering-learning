# Supplemental: Troubleshooting Guide

**Fixing the most common Databricks errors.**

---

## 1. `AnalysisException: Path does not exist`

**Context:** Reading from S3/ADLS.
**Cause:**
1. Typo in path.
2. **Mount point missing.** (Check `dbutils.fs.ls("/mnt/...")`).
3. **Permissions.** The cluster's Instance Profile (AWS) or Service Principal (Azure) cannot access the bucket.
**Fix:** Verify `dbutils.fs.ls()` works. If not, check IAM/RBAC.

---

## 2. `OutOfMemoryError: Java heap space`

**Context:** Driver or Executor crash.
**Cause:**
- **Driver OOM:** `collect()` called on big data. Solution: Don't use collect. Use `.take(100)` or write to file.
- **Executor OOM:** One partition is too big (Skew). Solution: Salt keys or use AQE skew join optimization.

---

## 3. `DeltaIcebergCompatibilityException` (or similar)

**Context:** Writing to Delta.
**Cause:** You are trying to use a newer Delta feature (like Column Mapping or Deletion Vectors) and reading it with an older client.
**Fix:** Upgrade the reader client or disable the feature on write (`delta.columnMapping.mode = none`).

---

## 4. `Stream is processing triggers too slowly`

**Context:** Structured Streaming / DLT.
**Cause:**
- Input rate > Processing rate.
- Batch duration is rising.
**Fix:**
- Increase cluster size.
- Reduce micro-batch size (`maxBytesPerTrigger`).
- Optimize the code (cache lookups).

---

## 5. `DatabricksExecutionError: Reference to database 'x' not found`

**Context:** Unity Catalog.
**Cause:** You are probably in `hive_metastore` catalog by default and trying to access a UC table without fully qualified name.
**Fix:** Use 3-level namespace: `SELECT * FROM prod.finance.users`.

---

## 6. `SparkException: Job aborted due to stage failure`

**Context:** Generic error.
**Investigation:**
1. Scroll down to "Caused by".
2. Look for **"Task not serializable"**: You are using a variable inside a UDF that isn't on the workers.
3. Look for **"Container killed by YARN for exceeding memory limits"**: Memory overhead issue. Increase `spark.executor.memoryOverhead`.

---

**Interview Tip:**
Always explain your debugging usage of the **Spark UI**. "I would check the Stages tab to see if one task is lagging (skew) or if the Input Size is huge (need more partitions)."
