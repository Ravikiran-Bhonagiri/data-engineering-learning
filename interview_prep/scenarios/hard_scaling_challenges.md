# 🔴 Hard Scenarios 31-40

**Performance at Scale & Advanced Optimization**

---

## Scenario 31: Optimizing Trillion-Row Queries

**🏷️ Technologies:** `Databricks` `Delta Lake`

### Interview Question
*"You own a 'user_events' table containing **1 trillion rows** (1PB of data). A critical application needs to lookup all events for a specific `user_id` with sub-second latency.
**The Issue:** Currently, even with partitioning by `date`, this lookup takes 10+ minutes because it has to scan TBs of data across thousands of partitions.
**Question:** Explain three distinct optimizations you would apply to the data layout to achieve sub-second point lookups for this specific `user_id` pattern. Why does each work?"*

---

## Scenario 32: Petabyte-Scale Shuffles

**🏷️ Technologies:** `PySpark`

### Interview Question
*"You are debugging a failed nightly job that joins two massive tables: `Fact_Sales` (10PB) and `Fact_Inventory` (5PB).
**Symptom:** The stage progress bar gets stuck at 99%. Examination of the executors shows that Shuffle Write I/O has exploded to 5PB, filling all available disk space, and resulting in timeouts.
**Question:** This is a 'Shuffle of Death'. Walk me through your strategy to optimize this join. What techniques can reduce this massive data movement across the network?"*

---

## Scenario 33-40: Extreme Scale Challenges

### Scenario 33: 10,000 Columns (JVM & Planner limits)
**Question:** *"Star schema with 10K columns. Query Planner hangs for 10 min then OOMs. What is happening internally?"*
**Answer:** Catalyst Optimizer trying to generate logical plan. 10K columns × complex joins = huge DAG.
- **Fix:** `spark.sql.optimizer.maxIterations=1` (disable optimizations).
- **Architecture:** Split into vertical partition tables (Data Vault style) or use Wide-Column Store (Cassandra) if 10K columns are needed.

### Scenario 34: Sub-Second Aggregations (Flink)
**Question:** *"Dashboard needs COUNT(DISTINCT users) updated every 500ms. Spark Streaming micro-batch (10s) is too slow."*
**Answer:** Move to Native Streaming (Flink).
- **Pattern:** Kafka → Flink (Tumbling Window 500ms) → Redis/Cassandra.
- **Approximation:** Use HyperLogLog (HLL) sketch in Redis to merge counts without moving data.

### Scenario 35: Cross-Region Transfer Costs
**Question:** *"$50K/month transferring 1PB AWS us-east-1 → us-west-2. Reduce?"*
**Answer:** Process locally, transfer only results. ZSTD compression (70% reduction).

### Scenario 36: 100K+ Partitions (Legacy Handling)
**Question:** *"You have a 5-year-old Hive table partitioned by (date, user_id) = 10M small partitions. 'Liquid Clustering' is not an option (legacy version). How do you query this?"*
**Answer:**
- **Manifest:** Generate a file manifest/symlink text file. Parallelize reading the list.
- **Metastore:** Use `MSCK REPAIR TABLE` carefully? NO, it will crash. Use direct file listing or partition pruning (`WHERE date=...`) to avoid full scan.

### Scenario 37: CI/CD for Spark Pipelines
**Question:** *"Design a CI/CD pipeline for a Spark job. How do you verify changes before prod?"*
**Answer:**
1. **GitHub Actions:** Trigger on PR.
2. **Unit Tests:** Run `pytest` with small mock data (no Spark connect needed).
3. **Integration Test:** Deploy to `staging` workspace, run on sample dirty data.
4. **Blue/Green:** Deploy to production but standby.
5. **Rollback:** Automated revert if health checks fail.

### Scenario 38: Snowflake vs Databricks Architecture
**Question:** *"CTO asks: Should we migrate from Databricks to Snowflake for 50PB of unstructured data ML workloads? Your advice?"*
**Answer:** Advise **staying on Databricks**.
- **Databricks:** Native support for unstructured data (images/text) and ML/AI workflows (MLflow). Stronger on "Engineering" (Spark streaming).
- **Snowflake:** Better for SQL Analysts and BI serving. Expensive/limited for unstructured deep learning.

### Scenario 39: Deeply Nested JSON (Memory Explosion)
**Question:** *"JSON has 5 levels of nested arrays. Exploding level-by-level multiplies row count by 1000x (1M rows → 1B rows), causing OOM. Optimized approach?"*
**Answer:**
- **Higher-Order Functions:** Use `transform`, `filter`, `aggregate` within the array column *without* exploding.
- **Lateral View (Generator):** Explode only what is needed, filter immediately, then join back.

### Scenario 40: Global Multi-Datacenter (Conflict Resolution)
**Question:** *"Active-Active writes in US and EU. Same record updated in both regions at t=0.01s. How do you consistently resolve conflicts without data loss?"*
**Answer:**
- **CRDTs (Conflict-free Replicated Data Types):** Merge logic (e.g., Union of sets).
- **LWW (Last Write Wins):** Requires synchronized atomic clocks (NTP isn't enough, need TrueTime).
- **Architecture:** Shard users by region (US users always write to US DB) to avoid conflict entirely.

---

**Previous:** [Governance & Security](./hard_governance_security.md) | **🎉 All 100 Scenarios Complete!**

---

## 🎯 Congratulations!

You've now covered **100 comprehensive interview scenarios** across:
- ✅ **20 Easy** - Foundational concepts
- ✅ **40 Medium** - Debugging & optimization  
- ✅ **40 Hard** - Architecture & system design

### 💡 Study Strategy
1. **Week 1-2:** Master Easy scenarios
2. **Week 3-4:** Work through Medium
3. **Week 5-6:** Study Hard scenarios
4. **Practice:** Explain solutions verbally

### 🚀 Interview Success Tips
- Focus on "What's Happening" sections to understand internals
- Practice answering follow-up questions
- Convert scenarios to STAR format for behavioral rounds
- Add your own real-world experiences

**Good luck with your interviews!** 🎯
