# ⚡ Apache Spark & PySpark - Deep Internals Course

A comprehensive, self-contained PySpark course for Data Engineers mastering big data processing at scale.

---

## 📁 Course Contents

All course materials are in the **[learning/](learning/)** folder:

| Part | File | Description |
|------|------|-------------|
| **Foundation** | [01_Foundation.md](learning/01_Foundation.md) | Spark Architecture, RDDs, DataFrames, Datasets |
| **10-Day Course** | [02_Day_00.md](learning/02_Day_00.md) - [02_Day_09.md](learning/02_Day_09.md) | Setup → Catalyst → Tungsten → Production |
| **Quick Reference** | [03_QUICK_Reference.md](learning/03_QUICK_Reference.md) | Commands, Transformations, Actions Cheatsheet |
| **Examples** | [04_Complete_Examples.md](learning/04_Complete_Examples.md) | Production ETL Patterns |
| **Practice** | [05_Practice_Exercises.md](learning/05_Practice_Exercises.md) | Coding Challenges |
| **Installation** | [06_Installation_Guide.md](learning/06_Installation_Guide.md) | Local & Cluster Setup |
| **Performance** | [07_Performance_Tuning.md](learning/07_Performance_Tuning.md) | Optimization Deep Dive |
| **Databricks** | [08_Databricks_Guide.md](learning/08_Databricks_Guide.md) | Platform-Specific Features |
| **Troubleshooting** | [09_Troubleshooting_Extended.md](learning/09_Troubleshooting_Extended.md) | Debug OOMs, Skew, Shuffles |
| **Delta Lake** | [10_Delta_Lake_Advanced.md](learning/10_Delta_Lake_Advanced.md) | ACID, Time Travel, Optimization |
| **Projects** | [projects/](learning/projects/) | 6 End-to-End Implementations |

---

## 🚀 Getting Started

1. Go to **[learning/README.md](learning/README.md)**
2. Follow the 10-day roadmap!

---

## 🎓 What You'll Master

### Core Spark Concepts
- ✅ Spark architecture (Driver, Executors, Cluster Manager)
- ✅ RDDs, DataFrames, and Datasets
- ✅ Lazy evaluation and DAG optimization
- ✅ Transformations vs Actions
- ✅ Partitioning and shuffling mechanics

### Internals & Optimization
- ✅ **Catalyst Optimizer** - Logical & physical planning
- ✅ **Tungsten Execution Engine** - Code generation & memory management
- ✅ **Adaptive Query Execution (AQE)** - Dynamic optimization
- ✅ Data skew handling with salting and broadcast joins
- ✅ Memory tuning (Heap, Off-Heap, Executor overhead)

### Advanced Topics
- ✅ Structured Streaming & watermarks
- ✅ UDFs vs Pandas UDFs performance
- ✅ Custom partitioners and accumulators
- ✅ Spark SQL optimization techniques
- ✅ Integration with Delta Lake for ACID transactions

### Production Patterns
- ✅ Small files problem solutions
- ✅ Cost-based optimization (CBO)
- ✅ Debugging OOM errors (Driver vs Executor)
- ✅ Join strategies (Broadcast, Sort-Merge, Shuffle Hash)
- ✅ Monitoring with Spark UI and Ganglia

**Total Time:** ~20-25 hours for expert proficiency.

---

## 📊 Course Structure

```
pyspark/learning/
├── README.md                       # Start here
├── 01_Foundation.md                # Spark fundamentals
├── 02_Day_00.md                    # Setup & Installation
├── 02_Day_01.md                    # RDDs and transformations
├── 02_Day_02.md                    # DataFrames and Spark SQL
├── 02_Day_03.md                    # Partitioning and shuffling
├── 02_Day_04.md                    # Joins and aggregations
├── 02_Day_05.md                    # UDFs and custom logic
├── 02_Day_06.md                    # Structured Streaming
├── 02_Day_07.md                    # Catalyst Optimizer internals
├── 02_Day_08.md                    # Tungsten & memory management
├── 02_Day_09.md                    # Production optimization
├── 03_QUICK_Reference.md           # Cheat sheet
├── 04_Complete_Examples.md         # ETL patterns
├── 05_Practice_Exercises.md        # Hands-on challenges
├── 06_Installation_Guide.md        # Setup instructions
├── 07_Performance_Tuning.md        # Deep performance guide
├── 08_Databricks_Guide.md          # Platform integration
├── 09_Troubleshooting_Extended.md  # Advanced debugging
├── 10_Delta_Lake_Advanced.md       # ACID on data lakes
└── projects/                       # 6 complete projects
    ├── 01_etl_pipeline.py
    ├── 02_streaming_analytics.py
    ├── 03_ml_churn_prediction.py
    ├── 04_data_quality_pipeline.py
    ├── 05_medallion_architecture.py
    └── 06_recommendation_engine.py
```

**Total:** 20 files + 6 projects

---

## 🎯 Learning Path

### Week 1: Foundations
- Day 0: Environment setup
- Day 1-2: RDDs and DataFrames
- Day 3: Partitioning strategies
- Day 4: Join optimization

### Week 2: Internals & Streaming
- Day 5: UDFs and custom functions
- Day 6: Structured Streaming
- Day 7: Catalyst Optimizer deep dive
- Day 8: Tungsten execution engine

### Week 3: Production Mastery
- Day 9: Performance tuning techniques
- Complete all practice exercises
- Build 2-3 projects from the projects folder
- Study troubleshooting guide

---

## 💡 Key Takeaways

After completing this course, you will:

1. **Understand Spark internals** (Catalyst, Tungsten, Execution Planning)
2. **Optimize jobs** for Petabyte-scale data
3. **Debug production issues** (OOMs, skew, shuffle explosions)
4. **Build streaming pipelines** with exactly-once semantics
5. **Master Delta Lake** for ACID on data lakes

---

## 🏆 Recommended Next Steps

1. Complete the **[10-day course](learning/README.md)**
2. Build **[6 projects](learning/projects/)**
3. Practice with **[PySpark Questions](../interview_prep/04_PySpark_Questions.md)** (100 Q's)
4. Tackle **[Hard Scaling Challenges](../interview_prep/scenarios/hard_scaling_challenges.md)**

---

## 🛠️ Sample Projects Included

| # | Project | Description |
|:--|:--------|:------------|
| 01 | ETL Pipeline | Multi-source ingestion with validation |
| 02 | Streaming Analytics | Real-time aggregations with watermarks |
| 03 | ML Churn Prediction | Feature engineering with MLlib |
| 04 | Data Quality Pipeline | Automated quality checks |
| 05 | Medallion Architecture | Bronze → Silver → Gold with Delta |
| 06 | Recommendation Engine | Collaborative filtering at scale |

---

Good luck with your PySpark mastery journey! 🎯
