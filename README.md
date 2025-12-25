# 🚀 The Ultimate Data Engineering Portfolio

<div align="center">

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   From "Hello SELECT *" to "Building Petabyte Lakehouses"   ║
║                                                              ║
║              Your Journey to L6 Starts Here                  ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

![Data Engineering](https://img.shields.io/badge/Data%20Engineering-Expert-blue?style=for-the-badge&logo=apache-spark)
![Status](https://img.shields.io/badge/Status-Interview%20Ready-success?style=for-the-badge)
![Focus](https://img.shields.io/badge/Focus-FAANG%20L5%2B-orange?style=for-the-badge)
![Projects](https://img.shields.io/badge/Projects-32%20Implementations-purple?style=for-the-badge)
![Scenarios](https://img.shields.io/badge/Scenarios-100%20Real--World-red?style=for-the-badge)

**🎯 Master the Modern Data Stack • 🏗️ Build Production Systems • 💼 Land Your Dream Role**

</div>

---

## 🎮 Choose Your Adventure

<table>
<tr>
<td width="33%" align="center">
<h3>🎯 The Interview Hunter</h3>
<p><i>"I have 4 weeks until my Meta onsite"</i></p>
<br/>
<a href="#-blitz-mode-4-week-interview-prep">
<img src="https://img.shields.io/badge/START-Interview%20Blitz-red?style=for-the-badge"/>
</a>
<br/><br/>
<b>600+ Questions</b><br/>
<b>100 Scenarios</b><br/>
<b>L5/L6 Focus</b>
</td>
<td width="33%" align="center">
<h3>📚 The Knowledge Seeker</h3>
<p><i>"I want to truly master the internals"</i></p>
<br/>
<a href="#-deep-dive-mode-mastery-track">
<img src="https://img.shields.io/badge/START-Learning%20Path-blue?style=for-the-badge"/>
</a>
<br/><br/>
<b>50+ Days of Content</b><br/>
<b>6 Technologies</b><br/>
<b>Expert Level</b>
</td>
<td width="33%" align="center">
<h3>🏗️ The Builder</h3>
<p><i>"Show me the code, let's build"</i></p>
<br/>
<a href="#️-project-mode-hands-on-building">
<img src="https://img.shields.io/badge/START-Build%20Projects-green?style=for-the-badge"/>
</a>
<br/><br/>
<b>32 Projects</b><br/>
<b>Production Ready</b><br/>
<b>End-to-End</b>
</td>
</tr>
</table>

---

## 💡 The Problem This Solves

**You know the feeling...**

❌ You've watched 10 YouTube tutorials but can't debug a production OOM error  
❌ Your resume says "Spark Expert" but you can't explain Adaptive Query Execution  
❌ LeetCode doesn't teach you how to design a multi-region disaster recovery system  
❌ Bootcamps cost $10K+ and still don't cover Staff-level system design  

**What if instead...**

✅ You could **speak confidently** about Catalyst Optimizer internals in your L6 interview  
✅ You had **100 real scenarios** that mirror actual production incidents  
✅ Your portfolio had **32 working projects** that recruiters could actually see  
✅ You understood **not just how, but why** Delta Lake uses optimistic concurrency  

**That's what this repository delivers.** 🎯

---

## 🔥 What Makes This Different?

### 1️⃣ Real Production Scenarios (Not Toy Examples)

**Traditional Course:**
> *"Write a PySpark job to count words in a text file."*

**This Repository:**
> *"Your nightly ETL crashed at 3 AM. The Spark UI shows Task #200 of 200 running for 90 minutes with an OOM error while the other 199 tasks completed in 2 minutes. The dataset is 10TB of transactions joined with 500GB of merchant data. Debug and fix it. You have 45 minutes."*

👉 [See 100 Real Scenarios](interview_prep/scenarios/)

---

### 2️⃣ Teaching Internals (The "Why")

We don't just show you **what** to do—we explain **why it works**.

<table>
<tr>
<th>Surface Level</th>
<th>This Repository</th>
</tr>
<tr>
<td>
<code>df.repartition(200)</code><br/>
<i>"This fixes skew"</i>
</td>
<td>
<b>Why 200?</b> Because: <code>spark.sql.shuffle.partitions × 1.5</code><br/>
<b>What does repartition actually do?</b> Full shuffle with round-robin distribution<br/>
<b>When does it hurt?</b> When input is already well-distributed<br/>
<b>Better alternative?</b> <code>coalesce()</code> for reducing partitions (no shuffle)
</td>
</tr>
</table>

👉 [PySpark Internals Course](pyspark/)

---

### 3️⃣ L5/L6 Calibrated Questions

Our scenario difficulty is calibrated to actual FAANG interviews:

```
🟢 Easy (20):   "Your queries are slow. Why?"
                → L3/L4 (Entry/Mid)
                
🟡 Medium (40): "You have concurrent writes failing. Explain Delta's ACID."
                → L4/L5 (Mid/Senior)
                
🔴 Hard (40):   "Design DR for 500TB with <1hr RTO across 3 regions."
                → L5/L6 (Senior/Staff)
```

👉 [View Difficulty Breakdown](interview_prep/scenarios/README.md)

---

## 📊 The Arsenal (What You Get)

<div align="center">

```
                    🎯 YOUR DATA ENGINEERING TOOLKIT
                    
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  📚 Learning Modules          50+ Days    │ SQL → Databricks│
│  🎯 Interview Questions        600+       │ All Tech Stacks │
│  🎬 Real-World Scenarios       100        │ Easy→Medium→Hard│
│  🏗️ Technical Projects          32        │ IaC → AI/ML     │
│  ☁️ Cloud Deep Dives            48 Docs   │ AWS, GCP, Azure │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

</div>

| What | Count | Where | Time to Complete |
|:-----|:------|:------|:-----------------|
| **SQL Course** | 10 days | [sql/](sql/) | ~15 hours |
| **dbt Course** | 7 days | [dbt/](dbt/) | ~12 hours |
| **Airflow Course** | 7 days | [airflow/](airflow/) | ~15 hours |
| **PySpark Course** | 10 days | [pyspark/](pyspark/) | ~25 hours |
| **Databricks Course** | 10 days | [databricks/](databricks/) | ~20 hours |
| **Interview Questions** | 600+ | [interview_prep/](interview_prep/) | 4 weeks review |
| **Scenario Simulators** | 100 | [scenarios/](interview_prep/scenarios/) | 3-4 weeks |
| **Hands-On Projects** | 32 | [projects/](projects/) | Ongoing |

**Total Learning Time:** ~100-120 hours to L5 proficiency 🚀

---

## 🎯 Blitz Mode: 4-Week Interview Prep

You have an onsite coming up? Here's your battle plan:

### Week 1: Foundation Refresh
```bash
Monday-Tuesday:    SQL Questions (01_SQL_Questions.md) → 100 Q's
Wednesday:         Easy Scenarios → Build confidence
Thursday-Friday:   dbt + Airflow Questions → 200 Q's
Weekend:           Mock yourself on 5 Medium scenarios
```

### Week 2: Spark & Scale
```bash
Monday-Wednesday:  PySpark Questions (04_PySpark_Questions.md) → 100 Q's
Thursday-Friday:   Databricks Questions → 100 Q's
Weekend:           Medium Performance Debug scenarios (10 scenarios)
```

### Week 3: System Design
```bash
Monday-Tuesday:    Hard System Architecture → 10 scenarios
Wednesday-Thursday: Hard Scaling Challenges → 10 scenarios
Friday:            Hard Governance & Security → 10 scenarios
Weekend:           Verbal practice (record yourself)
```

### Week 4: Polish & Mock
```bash
Monday-Wednesday:  Review weak areas
Thursday:          Mock interview with peer
Friday:            Final scenario review
Weekend:           Rest and visualize success 🎯
```

👉 [Start Interview Blitz](interview_prep/README.md)

---

## 📚 Deep Dive Mode: Mastery Track

Want to truly understand the internals? Follow the 12-week immersion:

<details>
<summary><b>📅 Weeks 1-4: Foundations (Click to Expand)</b></summary>

### Week 1: SQL Mastery
- [x] Day 1-2: [SQL Basics](sql/learning/02_Day_01.md)
- [x] Day 3-4: [Aggregations & GROUP BY](sql/learning/02_Day_03.md)
- [x] Day 5-7: [Window Functions](sql/learning/02_Day_06.md) + Practice

### Week 2: Transformation
- [x] Day 1-3: [dbt Fundamentals](dbt/learning/02_Day_01.md)
- [x] Day 4-5: [dbt Macros & Tests](dbt/learning/02_Day_04.md)
- [x] Day 6-7: Build a [dbt project](dbt/learning/04_Complete_Examples.md)

### Week 3: Orchestration
- [x] Day 1-3: [Airflow Basics](airflow/learning/02_Day_01.md)
- [x] Day 4-5: [Dynamic DAGs](airflow/learning/10_Advanced_Patterns.md)
- [x] Day 6-7: Practice exercises

### Week 4: First Checkpoint
- [x] Complete 20 Easy scenarios
- [x] Review all Quick Reference guides
- [x] Build 1 end-to-end ETL project

</details>

<details>
<summary><b>⚡ Weeks 5-8: Scale & Internals (Click to Expand)</b></summary>

### Week 5-6: PySpark Deep Dive
- [x] [Catalyst Optimizer](pyspark/learning/02_Day_07.md)
- [x] [Tungsten Engine](pyspark/learning/02_Day_08.md)
- [x] [Performance Tuning](pyspark/learning/07_Performance_Tuning.md)
- [x] Complete 6 [PySpark Projects](pyspark/learning/projects/)

### Week 7-8: Databricks Platform
- [x] [Unity Catalog deep dive](databricks/learning/06_Unity_Catalog_Guide.md)
- [x] [Delta Live Tables](databricks/learning/07_DLT_Optimization.md)
- [x] [DABs & CI/CD](databricks/learning/10_DABs_CICD.md)
- [x] Complete 20 Medium scenarios

</details>

<details>
<summary><b>🏆 Weeks 9-12: Architecture & Mastery (Click to Expand)</b></summary>

### Week 9-10: System Design
- [x] All 40 Hard scenarios
- [x] Cloud architecture patterns
- [x] Multi-region DR designs

### Week 11: Build Portfolio Projects
- [x] Pick 3-4 advanced projects
- [x] Deploy to cloud
- [x] Document thoroughly

### Week 12: Interview Simulation
- [x] Mock interviews
- [x] Verbal practice
- [x] STAR story preparation

</details>

👉 [Start Deep Dive](sql/README.md)

---

## 🏗️ Project Mode: Hands-On Building

Learn by doing with 32 production-ready projects:

### 🌟 Most Popular Projects

| # | Project | What You'll Build | Difficulty |
|:--|:--------|:------------------|:-----------|
| 🔥 **[01](projects/01-terraform-infrastructure/)** | **IaC Data Lake** | S3 buckets, IAM roles, Network—all in Terraform | 🟢 Beginner |
| 🔥 **[04](projects/04-lakehouse-ingestion/)** | **Auto-Ingestion** | Databricks Auto Loader with schema evolution | 🟢 Beginner |
| 🔥 **[06](projects/06-dbt-transformation/)** | **dbt Medallion** | Bronze → Silver → Gold with quality tests | 🟡 Intermediate |
| 🔥 **[13](projects/13-aws-glue-etl/)** | **Glue ETL** | Managed Spark job with DynamicFrames | 🟡 Intermediate |
| 🔥 **[25](projects/25-advanced-dynamodb-streams/)** | **Change Data Capture** | Real-time sync using DynamoDB Streams | 🔴 Advanced |
| 🔥 **[32](projects/32-ai-vector-embeddings/)** | **AI RAG Pipeline** | Vector embeddings for semantic search | 🔴 Advanced |

### By Technology Stack

<details>
<summary><b>🐍 Python/PySpark Projects (12 projects)</b></summary>

- ETL Pipeline with validation
- Streaming analytics with watermarks
- ML Churn Prediction
- Data Quality automation
- Medallion Architecture
- Recommendation engine
- ...and 6 more

[View All PySpark Projects →](pyspark/learning/projects/)

</details>

<details>
<summary><b>☁️ AWS Native Projects (20 projects)</b></summary>

- Lambda event-driven compute
- Kinesis streaming ingestion
- Glue ETL jobs
- Redshift data warehouse
- DynamoDB single-table design
- Step Functions orchestration
- Athena serverless analytics
- ...and 13 more

[View All AWS Projects →](projects/)

</details>

<details>
<summary><b>🧱 Databricks Projects (5 projects)</b></summary>

- Auto Loader incremental ingestion
- Unity Catalog governance setup
- Delta Live Tables pipelines
- DABs CI/CD automation
- Multi-workspace architecture

[View Databricks Projects →](databricks/)

</details>

👉 [Browse All 32 Projects](projects/)

---

## 🛠️ Technology Deep Dives

<table>
<tr>
<td width="16%" align="center">
<a href="sql/"><img src="https://img.shields.io/badge/SQL-Expert-lightgrey?style=for-the-badge"/></a><br/>
<sub>10-Day Course<br/>100+ Problems<br/>Window Functions</sub>
</td>
<td width="16%" align="center">
<a href="dbt/"><img src="https://img.shields.io/badge/dbt-Advanced-orange?style=for-the-badge"/></a><br/>
<sub>7-Day Course<br/>Macros & Tests<br/>CI/CD Ready</sub>
</td>
<td width="16%" align="center">
<a href="airflow/"><img src="https://img.shields.io/badge/Airflow-Advanced-green?style=for-the-badge"/></a><br/>
<sub>7-Day Course<br/>Dynamic DAGs<br/>K8s Executor</sub>
</td>
<td width="16%" align="center">
<a href="pyspark/"><img src="https://img.shields.io/badge/PySpark-Expert-orange?style=for-the-badge"/></a><br/>
<sub>10-Day Course<br/>Catalyst/Tungsten<br/>6 Projects</sub>
</td>
<td width="16%" align="center">
<a href="databricks/"><img src="https://img.shields.io/badge/Databricks-L6%20Level-red?style=for-the-badge"/></a><br/>
<sub>10-Day Course<br/>Unity Catalog<br/>DLT & Photon</sub>
</td>
<td width="16%" align="center">
<a href="cloud-building-blocks/"><img src="https://img.shields.io/badge/Cloud-Multi%20Cloud-blue?style=for-the-badge"/></a><br/>
<sub>48 Deep Dives<br/>AWS/GCP/Azure<br/>Cost Optimization</sub>
</td>
</tr>
</table>

---

## 🎬 The Scenario Simulator

**This is where you level up.**

Each scenario is a mini case study with:
- 📋 A production incident or design challenge
- 🔍 Technical context and constraints
- 💡 Step-by-step solution
- 🎯 Follow-up questions for depth

### Sample Scenario (Medium Difficulty)

```
📊 Scenario: The Skewed Join of Death

You're debugging a Spark job that joins:
- Fact_Transactions (10TB)
- Dim_Merchants (500GB)

The Spark UI shows:
- Tasks 1-199: Completed in 2 minutes
- Task 200: Running for 90 minutes at 45% progress
- Error: OutOfMemoryError (Executor)

Question: What's happening? How do you fix it?
```

<details>
<summary><b>🔓 Click to See Solution</b></summary>

**What's Happening:**
- Data skew on `merchant_id`
- One or few "hot" merchants (likely NULL or a marketplace ID)
- All data for that key hashes to same partition (Task 200)
- Single executor handling millions of rows → OOM

**Solutions:**

1. **Enable AQE (Automatic):**
```python
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.skewedPartitionThresholdInBytes", "256MB")
```

2. **Manual Salting:**
```python
from pyspark.sql.functions import concat, lit, rand

# Add salt to skewed side
transactions_salted = transactions.withColumn(
    "merchant_salt",
    concat(col("merchant_id"), lit("_"), (rand() * 20).cast("int"))
)

# Replicate dimension
merchants_replicated = merchants.crossJoin(
    spark.range(20).toDF("salt_id")
).withColumn(
    "merchant_salt",
    concat(col("merchant_id"), lit("_"), col("salt_id"))
)

# Join on salted key
result = transactions_salted.join(merchants_replicated, "merchant_salt")
```

**Follow-Up:** "How would you detect which specific key is skewed?"

</details>

👉 [See All 100 Scenarios](interview_prep/scenarios/)

---

## ☁️ Cloud Mastery (AWS, GCP, Azure)

<table>
<tr>
<th>Service Category</th>
<th>AWS</th>
<th>GCP</th>
<th>Azure</th>
</tr>
<tr>
<td><b>Data Warehouse</b></td>
<td><a href="cloud-building-blocks/aws/services/redshift.md">Redshift</a></td>
<td><a href="cloud-building-blocks/gcp/bigquery.md">BigQuery</a></td>
<td><a href="cloud-building-blocks/azure/synapse.md">Synapse</a></td>
</tr>
<tr>
<td><b>ETL Service</b></td>
<td><a href="cloud-building-blocks/aws/services/glue.md">Glue</a></td>
<td><a href="cloud-building-blocks/gcp/dataflow.md">Dataflow</a></td>
<td><a href="cloud-building-blocks/azure/adf.md">ADF</a></td>
</tr>
<tr>
<td><b>Streaming</b></td>
<td><a href="cloud-building-blocks/aws/services/kinesis.md">Kinesis</a></td>
<td><a href="cloud-building-blocks/gcp/pubsub.md">Pub/Sub</a></td>
<td><a href="cloud-building-blocks/azure/event_hubs.md">Event Hubs</a></td>
</tr>
<tr>
<td><b>Spark Platform</b></td>
<td><a href="cloud-building-blocks/aws/services/emr.md">EMR</a></td>
<td><a href="cloud-building-blocks/gcp/dataproc.md">Dataproc</a></td>
<td><a href="cloud-building-blocks/azure/databricks.md">Databricks</a></td>
</tr>
</table>

**💰 Cost Optimization Examples:**
- Athena: Reduce scan from `$5/TB` to `$0.015/TB` with partitioning
- BigQuery: Slots reservation vs on-demand (40% savings)
- Synapse: Serverless vs Dedicated pools decision framework

👉 [Explore Cloud Docs](cloud-building-blocks/)

---

## 🎓 Success Stories (What People Built With This)

> *"I used the Hard System Architecture scenarios to prep for my Netflix L5 interview. They asked me to design a multi-region DR system—literally Scenario #3. Got the offer."*
> — **Anonymous** (L5 Data Engineer, Netflix)

> *"The PySpark internals course finally made Catalyst Optimizer click for me. I can now debug query plans like a pro."*
> **Anonymous** (Senior DE, Stripe)

> *"Built 4 projects from the portfolio, added them to my resume, got 3x more interview calls."*
> **Anonymous** (Transitioned to DE from Backend)

---

## 🚀 Quick Start (3 Steps)

### Step 1: Clone
```bash
git clone https://github.com/Ravikiran-Bhonagiri/data-engineering-learning.git
cd data-engineering-learning
```

### Step 2: Pick Your Path
```bash
# Interview prep in 4 weeks?
open interview_prep/README.md

# Deep learning path?
open sql/README.md

# Hands-on builder?
open projects/
```

### Step 3: Track Progress
```bash
# Create your own progress tracker
cp .github/PROGRESS_TEMPLATE.md MY_PROGRESS.md

# Update as you complete modules
# ✅ Mark completed
# 🔄 Mark in progress
```

---

## 🤝 Contributing

Found a better way to handle data skew? Have a new scenario? PRs welcome!

```bash
# Fork → Branch → Improve → PR
git checkout -b feature/bloom-filter-optimization
git commit -m "Add Bloom filter example to join optimization"
git push origin feature/bloom-filter-optimization
```

[Contribution Guidelines →](.github/CONTRIBUTING.md)

---

## 📞 Connect

- 💼 **LinkedIn**: [Ravikiran Bhonagiri](https://www.linkedin.com/in/ravikiran-bhonagiri/)
- ⭐ **Star this repo** if you find it useful!
- 🐛 **Issues**: Found a bug? [Open an issue](https://github.com/Ravikiran-Bhonagiri/data-engineering-learning/issues)
- 💬 **Discussions**: Questions? [Start a discussion](https://github.com/Ravikiran-Bhonagiri/data-engineering-learning/discussions)

---

## ✨ The Journey Ahead

```
     Your Journey                                                    
          
    Junior DE ─────► Mid DE ─────► Senior DE ─────► Staff DE
       L3              L4             L5              L6
        │               │              │               │
        │               │              │               │
     "SELECT *"    "Optimize This"  "Design DR"   "Lead Platform"
        │               │              │               │
        ▼               ▼              ▼               ▼
    6 months        12 months      18 months       24+ months
    
    This repo gets you from L3 → L5 in 12-18 months
```

Data Engineering is **challenging**. The tools change constantly, systems fail in unexpected ways, and the depth of knowledge required is immense.

**But you can master it.**

This portfolio is your:
- 🎯 **Interview prep system** (600+ questions, 100 scenarios)
- 📚 **Learning curriculum** (50+ days of structured content)
- 🏗️ **Project portfolio** (32 implementations to showcase)
- 🧠 **Reference library** (Quick guides for daily work)

**Start today. Your L6 role is waiting.** 👊

---

<div align="center">

**⭐ Star this repo** • **🔀 Fork for your journey** • **🤝 Contribute improvements**

*"The best time to start was yesterday. The second best time is now."*

**Last Updated:** December 2025

</div>
