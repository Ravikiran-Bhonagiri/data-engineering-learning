# 🚀 The Ultimate Data Engineering Portfolio

<div align="center">

![Data Engineering](https://img.shields.io/badge/Data%20Engineering-Expert-blue?style=for-the-badge&logo=apache-spark)
![Status](https://img.shields.io/badge/Status-Interview%20Ready-success?style=for-the-badge)
![Focus](https://img.shields.io/badge/Focus-FAANG%20L5%2B-orange?style=for-the-badge)
![Projects](https://img.shields.io/badge/Projects-32%20Implementations-purple?style=for-the-badge)
![Scenarios](https://img.shields.io/badge/Scenarios-100%20Real--World-red?style=for-the-badge)

**Master the Modern Data Stack. Build Production Systems. Crack Senior Interviews.**

📖 [**Quick Start**](#-quick-start-guide) • 🎯 [**Interview Prep**](#-interview-mastery) • 🏗️ [**Projects**](#-technical-projects-portfolio) • 📚 [**Learning Paths**](#-learning-roadmap)

</div>

---

## 📑 Table of Contents

- [Why This Portfolio?](#-why-this-portfolio)
- [Quick Start Guide](#-quick-start-guide)
- [Technology Stack](#️-technology-stack-mastery)
- [Cloud Building Blocks](#️-cloud-building-blocks)
- [Learning Roadmap](#️-learning-roadmap)
- [Interview Mastery](#-interview-mastery)
- [Technical Projects](#️-technical-projects-portfolio)
- [Repository Structure](#-repository-structure)

---

## 🌟 Why This Portfolio?

Welcome to a **different kind of repository**. This isn't just a collection of code snippets—it's a **comprehensive self-service bootcamp** designed to take you from "competent data engineer" to "**Senior Staff Engineer at a top-tier tech company**."

Whether you're aiming for **Google, Databricks, Netflix**, or a high-growth startup, this portfolio bridges the gap between *theory* and *production reality*.

### 📊 What You'll Find Here

| Category | Count | Description |
|:---------|:------|:------------|
| 🔥 **[Real-World Scenarios](interview_prep/scenarios/)** | 100 | Petabyte-scale shuffles, zero-downtime migrations, idempotency challenges |
| 🧠 **[Interview Questions](interview_prep/)** | 600+ | SQL, dbt, Airflow, PySpark, Databricks—curated and tiered |
| 🏗️ **[Technical Projects](projects/)** | 32 | End-to-end implementations from IaC to AI RAG pipelines |
| 📚 **[Learning Modules](sql/)** | 50+ days | Structured courses for SQL, dbt, Airflow, PySpark, Databricks |
| ☁️ **[Cloud Guides](cloud-building-blocks/)** | 48 docs | Production-grade AWS, GCP, Azure deep dives |

### 🎯 Key Features

✅ **Deep Internals Knowledge** - Spark's Catalyst Optimizer, Delta Lake's Log Protocol, JVM memory management  
✅ **Battle-Hardened Architecture** - DR strategies, GDPR/PII governance, Blue/Green deployments  
✅ **Production-Ready Code** - All examples are designed for real-world use, not toy demos  
✅ **Interview-Focused** - Questions and scenarios modeled after FAANG L5/L6 interviews  

---

## 🚀 Quick Start Guide

### For Interview Preparation
```bash
# Clone the repository
git clone https://github.com/Ravikiran-Bhonagiri/data-engineering-learning.git

# Navigate to interview prep
cd data-engineering-learning/interview_prep

# Start with scenarios
- Easy: ./scenarios/easy_fundamentals.md
- Medium: ./scenarios/medium_performance_debug.md  
- Hard: ./scenarios/hard_system_architecture.md
```

**📋 Suggested Path:**
1. Start with [SQL Questions](interview_prep/01_SQL_Questions.md) (100 Q's)
2. Progress to [PySpark Questions](interview_prep/04_PySpark_Questions.md) (100 Q's)
3. Tackle [Easy Scenarios](interview_prep/scenarios/easy_fundamentals.md) (20 scenarios)
4. Level up with [Medium Scenarios](interview_prep/scenarios/medium_performance_debug.md) (40 scenarios)
5. Master [Hard Scenarios](interview_prep/scenarios/hard_system_architecture.md) (40 scenarios)

### For Learning & Skill Building
```bash
# Pick a technology to master
cd data-engineering-learning/sql        # SQL fundamentals
cd data-engineering-learning/dbt        # Data transformation
cd data-engineering-learning/airflow    # Orchestration
cd data-engineering-learning/pyspark    # Big data processing
cd data-engineering-learning/databricks # Lakehouse platform

# Each folder has a README with day-by-day learning plans
```

### For Hands-On Projects
```bash
# Explore project implementations
cd data-engineering-learning/projects

# Check the project index for guidance
cat PROJECTS_INDEX.md
```

---

## 🛠️ Technology Stack Mastery

We don't just touch on tools—we **master** the technologies used in modern data platforms.

| Technology | Badge | Depth | What You'll Learn | Quick Link |
|:-----------|:------|:------|:------------------|:-----------|
| **SQL** | ![SQL](https://img.shields.io/badge/SQL-Optimization-lightgrey) | **Expert** | Execution Plans, Indexing, Anti-Patterns | [📚 Start](sql/README.md) |
| **dbt** | ![dbt](https://img.shields.io/badge/dbt-Transformation-orange) | **Advanced** | Macros, Snapshots, CI/CD, Quality Gates | [📚 Start](dbt/README.md) |
| **Airflow** | ![Airflow](https://img.shields.io/badge/Airflow-Orchestration-green) | **Advanced** | Custom Operators, Dynamic DAGs, K8s Executor | [📚 Start](airflow/README.md) |
| **PySpark** | ![Spark](https://img.shields.io/badge/Apache%20Spark-Internals-orange) | **Expert** | Catalyst, Tungsten, Custom Listeners, Streaming | [📚 Start](pyspark/README.md) |
| **Databricks** | ![Databricks](https://img.shields.io/badge/Databricks-Full%20Stack-red) | **L6/Principal** | Unity Catalog, Liquid Clustering, DLT, Photon | [📚 Start](databricks/README.md) |
| **Delta Lake** | ![Delta](https://img.shields.io/badge/Delta%20Lake-ACID-blue) | **Expert** | Log Protocol, CDC, V-Order, Constraints | [📚 Included](databricks/README.md) |

---

## ☁️ Cloud Building Blocks

Production-grade cloud documentation covering **storage, compute, analytics, and governance** for the three major cloud providers.

| Cloud | Status | Content | Quick Links |
|:------|:-------|:--------|:------------|
| **AWS** | ✅ Complete (16 docs) | Redshift, Glue, EMR, Athena, Step Functions | [Explore AWS](cloud-building-blocks/aws/) |
| **GCP** | ✅ Complete (16 docs) | BigQuery, Dataflow, Dataproc, Pub/Sub | [Explore GCP](cloud-building-blocks/gcp/) |
| **Azure** | ✅ Complete (16 docs) | Synapse, ADF, Databricks, Purview | [Explore Azure](cloud-building-blocks/azure/) |

**Highlights:**
- 💰 Cost optimization strategies (e.g., Athena: `$5/TB` → `$0.015/TB`)
- 🏗️ Architecture decision frameworks (Dataflow vs Dataproc, Synapse Dedicated vs Serverless)
- 🚀 "Start Simple" patterns for each service

👉 [View Detailed Portfolio Overview](PORTFOLIO_OVERVIEW.md)

---

## 🗺️ Learning Roadmap

### 🐣 Phase 1: Foundations (4-6 weeks)
*Target: Junior to Mid-Level Data Engineer*

| Week | Focus | Resources |
|:-----|:------|:----------|
| 1-2 | **SQL Mastery** | [10-Day SQL Course](sql/README.md) + [100 Practice Problems](sql/learning/05_Practice_Exercises.md) |
| 3 | **dbt Fundamentals** | [7-Day dbt Course](dbt/README.md) - Models, Tests, Macros |
| 4 | **Airflow Basics** | [6-Day Airflow Course](airflow/README.md) - DAGs, Operators, XComs |
| 5 | **PySpark Intro** | [Days 1-5 PySpark](pyspark/README.md) - DataFrames, Basic Transformations |
| 6 | **Databricks Platform** | [Days 1-3 Databricks](databricks/README.md) - Clusters, Notebooks, Delta |

### 🦅 Phase 2: Scale & Production (6-8 weeks)
*Target: Senior Data Engineer (L5)*

| Week | Focus | Resources |
|:-----|:------|:----------|
| 1-2 | **Advanced SQL** | [Window Functions](sql/learning/02_Day_06.md), [CTEs](sql/learning/02_Day_05.md), Performance Tuning |
| 3-4 | **dbt in Production** | [Advanced Topics](dbt/learning/09_Advanced_Production_Topics.md), [CI/CD](dbt/learning/08_dbt_Cloud_Guide.md) |
| 5 | **Airflow at Scale** | [Custom Operators](airflow/learning/10_Advanced_Patterns.md), Dynamic DAGs |
| 6-7 | **PySpark Internals** | [Catalyst Optimizer](pyspark/learning/07_Performance_Tuning.md), Memory Management |
| 8 | **Databricks Advanced** | [Unity Catalog](databricks/learning/06_Unity_Catalog_Guide.md), [DLT](databricks/learning/07_DLT_Optimization.md) |

**Practice:**
- [Medium Performance Scenarios](interview_prep/scenarios/medium_performance_debug.md)
- [Medium Transformations](interview_prep/scenarios/medium_transformations.md)

### 🦁 Phase 3: Architecture & Leadership (8+ weeks)
*Target: Staff/Principal Engineer (L6+)*

| Focus Area | Key Topics | Resources |
|:-----------|:-----------|:----------|
| **System Design** | Multi-region DR, Blue/Green, Global consistency | [Hard System Architecture](interview_prep/scenarios/hard_system_architecture.md) |
| **Scaling** | Trillion-row tables, Petabyte joins, Data skew | [Hard Scaling Challenges](interview_prep/scenarios/hard_scaling_challenges.md) |
| **Governance** | RLS, PII, Audit trails, Compliance | [Hard Governance](interview_prep/scenarios/hard_governance_security.md) |
| **Cloud Mastery** | Multi-cloud strategies, Cost optimization | [Cloud Building Blocks](cloud-building-blocks/) |
| **Advanced Patterns** | CDC, WAP, Slowly Changing Dimensions | [Hard Advanced Patterns](interview_prep/scenarios/hard_advanced_patterns.md) |

---

## 🎯 Interview Mastery

Your **secret weapon** for landing Senior+ roles at FAANG companies.

### 🏆 The Question Bank (600+ Questions)

| File | Count | Topics | Quick Link |
|:-----|:------|:-------|:-----------|
| **SQL** | 100 | Window functions, CTEs, Optimization, Anti-patterns | [View Questions](interview_prep/01_SQL_Questions.md) |
| **dbt** | 100+ | Modeling, Materializations, Testing, Macros | [View Questions](interview_prep/02_dbt_Questions.md) |
| **Airflow** | 100+ | DAGs, Backfilling, XComs, Executors | [View Questions](interview_prep/03_Airflow_Questions.md) |
| **PySpark** | 100+ | Internals, Optimization, Skew, Memory | [View Questions](interview_prep/04_PySpark_Questions.md) |
| **Databricks** | 100 | Platform, Unity Catalog, Delta Lake, Photon | [View Questions](interview_prep/05_Databricks_Questions.md) |

### 🎬 Real-World Scenarios (100 Total)

Crafted to mimic the "System Design" and "Deep Dive" rounds of FAANG interviews.

#### 🟢 Easy Scenarios (20)
Perfect for warming up and building confidence.

| Scenario File | Topics |
|:-------------|:-------|
| [Easy Fundamentals](interview_prep/scenarios/easy_fundamentals.md) | Small files, Schema evolution, Duplicates |
| [Easy Operational](interview_prep/scenarios/easy_operational.md) | PII handling, Timezone issues, Common joins |

**Sample Question:**
> *"Your streaming job has been running for 3 months. Queries that took 10 seconds now take 15 minutes. The Spark UI shows 90% time in 'Listing Files'. What happened and how do you fix it?"*

#### 🟡 Medium Scenarios (40)
The daily grind of a Senior Data Engineer.

| Scenario File | Topics |
|:-------------|:-------|
| [Performance Debug](interview_prep/scenarios/medium_performance_debug.md) | Data skew, OOM errors, Concurrent writes |
| [Complex Scheduling](interview_prep/scenarios/medium_complex_scheduling.md) | Backfills, SLA monitoring, Dynamic DAGs |
| [Transformations](interview_prep/scenarios/medium_transformations.md) | Deduplication at scale, SCD Type 2, Late data |
| [Integration & Streaming](interview_prep/scenarios/medium_integration_streaming.md) | Kafka integration, Exactly-once semantics, CDC |

**Sample Question:**
> *"Two Airflow DAGs write to the same Delta table at 8 AM. One fails with `ConcurrentAppendException`. Explain Delta's ACID concurrency and provide 3 solutions."*

#### 🔴 Hard Scenarios (40)
The promotion makers—Staff/Principal level complexity.

| Scenario File | Topics |
|:-------------|:-------|
| [System Architecture](interview_prep/scenarios/hard_system_architecture.md) | Blue/Green deployments, Multi-region DR, Row-level security |
| [Scaling Challenges](interview_prep/scenarios/hard_scaling_challenges.md) | Trillion-row queries, Petabyte shuffles, 10K+ partitions |
| [Governance & Security](interview_prep/scenarios/hard_governance_security.md) | GDPR deletion, Attribute-based access, Audit systems |
| [Advanced Patterns](interview_prep/scenarios/hard_advanced_patterns.md) | Time-travel debugging, Multi-hop lineage, Incremental models |

**Sample Question:**
> *"Design a Disaster Recovery architecture for 500TB of Delta tables with <1 hour RTO. Address metadata replication, data syncing (Active-Passive vs Active-Active), and failover triggers."*

---

## 🏗️ Technical Projects Portfolio

**32 end-to-end implementations** covering the Modern Data Stack → AWS Native → Advanced Patterns → Enterprise AI.

### Phase 1: Modern Open Stack (Projects 1-10)

| # | Project | Tech Stack | Learn |
|:--|:--------|:-----------|:------|
| 01 | [IaC Data Lake](projects/01-terraform-s3-datalake/) | Terraform, S3 | Infrastructure as Code |
| 02 | [Kafka Messaging](projects/02-kafka-docker/) | Kafka, Docker | Event streaming |
| 03 | [Flink Streaming](projects/03-flink-streaming/) | Flink, Python | Real-time processing |
| 04 | [Auto-Ingestion](projects/04-databricks-autoloader/) | Databricks, Spark | Schema inference |
| 05 | [Iceberg Format](projects/05-apache-iceberg/) | Iceberg, Athena | Open table formats |
| 06 | [dbt Transformation](projects/06-dbt-core/) | dbt, SQL | Modular transformations |
| 07 | [Airflow Orchestration](projects/07-airflow-orchestration/) | Airflow, Python | Workflow management |
| 08 | [Docker Containers](projects/08-docker-ecr/) | Docker, ECR | Containerization |
| 09 | [Unity Catalog](projects/09-unity-catalog/) | Unity Catalog | Data governance |
| 10 | [GitHub Actions CI/CD](projects/10-cicd-github-actions/) | GitHub Actions | Automation pipelines |

### Phase 2: AWS Native (Projects 11-20)

| # | Project | Tech Stack | Learn |
|:--|:--------|:-----------|:------|
| 11 | [Lambda Functions](projects/11-aws-lambda-event-driven/) | Lambda, Boto3 | Serverless compute |
| 12 | [Kinesis Streaming](projects/12-amazon-kinesis-streaming/) | Kinesis, Firehose | AWS streaming |
| 13 | [Glue ETL](projects/13-aws-glue-etl/) | Glue, DynamicFrame | Managed Spark |
| 14 | [Redshift Warehouse](projects/14-amazon-redshift-warehouse/) | Redshift, COPY | MPP data warehouse |
| 15 | [DynamoDB NoSQL](projects/15-dynamodb-nosql/) | DynamoDB | Single-table design |
| 16 | [Step Functions](projects/16-step-functions-orchestration/) | State Machines | Workflow orchestration |
| 17 | [Secrets Manager](projects/17-security-secrets-manager/) | Secrets Manager | Security best practices |
| 18 | [Athena Analytics](projects/18-athena-analytics-optimization/) | Athena, Partition Projection | Serverless queries |
| 19 | [SQS Queuing](projects/19-amazon-sqs-queues/) | SQS, DLQ | Reliable messaging |
| 20 | [IAM Security](projects/20-iam-least-privilege/) | IAM Policies | Access control |

### Phase 3: Advanced AWS (Projects 21-28)

Covers Lambda batching, Kinesis Analytics SQL, Glue Data Quality, Redshift Spectrum, DynamoDB Streams, Step Functions Distributed Map, Athena CTAS, and SNS+SQS fan-out patterns.

[View All Projects →](projects/)

### Phase 4: Enterprise Scale & AI (Projects 29-32)

Kubernetes on EKS, OpenSearch log analytics, Redis caching, and AI RAG pipelines with vector embeddings.

---

## 📂 Repository Structure

```
data-engineering-portfolio/
├── 📚 sql/                        # SQL: 10-day course + 100 practice problems
│   ├── README.md                  # Course overview
│   └── learning/                  # Day-by-day lessons + solutions
├── 🔧 dbt/                        # dbt: Medallion architecture + macros
│   ├── README.md                  # Learning path
│   └── learning/                  # 7-day course + advanced topics
├── ⏱️ airflow/                     # Airflow: DAGs + custom operators
│   ├── README.md                  # Getting started
│   └── learning/                  # 6-day course + patterns
├── ⚡ pyspark/                     # PySpark: Internals + optimization
│   ├── README.md                  # Course structure
│   ├── learning/                  # 10-day deep dive
│   └── projects/                  # 6 sample projects
├── 🧱 databricks/                 # Databricks: Platform + Unity Catalog
│   ├── README.md                  # Learning roadmap
│   └── learning/                  # 10-day course + guides
├── 🎯 interview_prep/             # Interview questions + scenarios
│   ├── 01_SQL_Questions.md        # 100 SQL questions
│   ├── 02_dbt_Questions.md        # 100+ dbt questions
│   ├── 03_Airflow_Questions.md    # 100+ Airflow questions
│   ├── 04_PySpark_Questions.md    # 100+ PySpark questions
│   ├── 05_Databricks_Questions.md # 100 Databricks questions
│   └── scenarios/                 # 100 real-world scenarios
│       ├── easy_fundamentals.md
│       ├── medium_performance_debug.md
│       └── hard_system_architecture.md
├── 🏗️ projects/                   # 32 technical implementations
│   ├── 01-terraform-s3-datalake/
│   ├── ...
│   └── 32-ai-vector-embeddings/
├── ☁️ cloud-building-blocks/      # AWS, GCP, Azure deep dives
│   ├── aws/                       # 16 AWS service guides
│   ├── gcp/                       # 16 GCP service guides
│   └── azure/                     # 16 Azure service guides
├── 📖 PORTFOLIO_OVERVIEW.md       # Detailed portfolio summary
├── 📖 PORTFOLIO_DEEP_DIVE.md      # In-depth technical documentation
└── README.md                      # You are here!
```

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/Ravikiran-Bhonagiri/data-engineering-learning.git
cd data-engineering-learning
```

### 2. Pick Your Path

**🎯 For Job Seekers:**
```bash
# Start with interview prep
open interview_prep/README.md

# Practice scenarios
open interview_prep/scenarios/README.md
```

**📚 For Learners:**
```bash
# Begin with SQL fundamentals
open sql/README.md

# Or choose your technology
open dbt/README.md      # Data transformation
open airflow/README.md  # Orchestration
open pyspark/README.md  # Big data processing
```

**🏗️ For Builders:**
```bash
# Explore hands-on projects
open projects/PROJECTS_INDEX.md
```

### 3. Set Up Your Environment

Each technology folder includes setup instructions:
- [SQL Setup](sql/learning/01_Setup.md)
- [dbt Setup](dbt/learning/02_Day_00.md)
- [Airflow Docker Setup](airflow/learning/06_Docker_Setup.md)
- [PySpark Installation](pyspark/learning/06_Installation_Guide.md)
- [Databricks Platform](databricks/learning/01_Foundation.md)

---

## 💡 How to Use This Repository

### For Interview Preparation
1. **Start with fundamentals**: Review questions in your weakest areas
2. **Practice verbalization**: Read a scenario, speak your answer out loud, then compare
3. **Build breadth**: Cover all 600 questions across 5 technology areas
4. **Master depth**: Work through all 100 scenarios (Easy → Medium → Hard)
5. **Mock interviews**: Time yourself on hard scenarios (45 minutes each)

### For Skill Development
1. **Follow the learning path**: Each technology has a day-by-day course
2. **Code along**: Don't just read—type the code and run it
3. **Complete exercises**: Every module has practice problems with solutions
4. **Build projects**: Use the 32 project templates as starting points
5. **Reference back**: Use Quick Reference guides when you need a reminder

### For Portfolio Building
1. **Fork this repository**: Make it your own
2. **Complete the projects**: Add your implementations
3. **Document your work**: Write READMEs for each project
4. **Deploy solutions**: Show working demos where possible
5. **Share publicly**: Let recruiters see your work

---

## 🎓 Learning Principles

This portfolio is built on three core principles:

1. **🧠 Deep Understanding Over Surface Knowledge**
   - We explain the "why," not just the "how"
   - Every concept includes internals, trade-offs, and alternatives

2. **🏗️ Production-Ready Over Toy Examples**
   - All code is designed for real-world use
   - We cover error handling, monitoring, and optimization

3. **🎯 Interview-Focused Over Academic**
   - Questions mirror actual FAANG interview formats
   - Scenarios test system design and debugging skills

---

## 🤝 Contributing

Found a better optimization? Spotted an error? Have a new scenario to add?

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/amazing-optimization`)
3. Commit your changes (`git commit -m 'Add Bloom filter optimization example'`)
4. Push to the branch (`git push origin feature/amazing-optimization`)
5. Open a Pull Request

---

## 📞 Connect & Support

- 💼 **LinkedIn**: [Connect with me](https://www.linkedin.com/in/ravikiran-bhonagiri/)
- 🌟 **Star this repo** if you find it useful!
- 🐛 **Report issues** in the GitHub Issues tab
- 💬 **Discussions** for questions and ideas

---

## ✨ Final Words

Data Engineering is **challenging**. The technology changes constantly, systems fail in unexpected ways, and the breadth of knowledge required is immense.

**But you can master it.**

This portfolio represents **hundreds of hours** of real-world experience, distilled into actionable learning paths, practice problems, and production-ready patterns.

Use it to:
- 🎯 **Land your dream job** at FAANG or top startups
- 📈 **Level up** from Mid to Senior to Staff engineer
- 🚀 **Build confidence** in system design and architecture
- 💡 **Deepen understanding** of data platform internals

**You've got this.** 👊

---

<div align="center">

**⭐ Star this repo** • **🔗 Share with peers** • **🤝 Contribute improvements**

*Last Updated: December 2024*

</div>
