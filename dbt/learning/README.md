# DBT Learning Path (For SQL Experts)

**You already know SQL. Now learn dbt in 3 steps.**

---

## 🎯 Start Here

If you're reading this, you probably:
- ✅ Write SQL queries daily
- ✅ Know JOINs, CTEs, window functions
- ❌ Have never used dbt
- ❓ Wonder what dbt even does

**Good news:** dbt is just SQL + some smart tooling. You'll pick it up fast.

---

## 📚 The 3-Part Learning Path

### Part 1: Foundation (30 minutes)
**File:** `01_Foundation.md`

**What you'll learn:**
- The problem dbt solves (for SQL users)
- SQL scripts vs dbt models
- How to install and configure dbt
- Your first dbt model

**When to read:** Start here. Don't skip this.

---

### Part 2: Hands-On Course (7 days, 1-2 hrs/day)
**Files:** `02_Day_00.md` through `02_Day_07.md` (8 files total)

**What you'll build:**
- **Day 00:** Understand why dbt exists
- **Day 01:** Install dbt, create first project
- **Day 02:** Models, `ref()`, dependencies
- **Day 03:** Sources & seeds
- **Day 04:** Testing
- **Day 05:** Documentation  
- **Day 06:** Snapshots (SCD Type 2)
- **Day 07:** Macros, incremental models, CI/CD

**When to use:** After Part 1. Work through one day at a time.

---

### Part 3: Quick Reference (ongoing)
**File:** `03_QUICK_Reference.md`

**What's inside:**
- Common dbt commands
- SQL → dbt pattern translations
- Interview cheatsheet
- Troubleshooting guide

**When to use:** As needed for quick lookups.

---

### Part 4: Complete Examples (optional)
**File:** `04_Complete_Examples.md`

**What's inside:**
- 2 end-to-end examples WITH full solutions
- Example 1: E-commerce Revenue Analytics (staging → marts)
- Example 2: Customer Cohort Analysis
- Production-ready code you can run

**When to use:** After completing Day 07, for real-world examples.

---

### Part 5: Practice Exercises (optional)
**File:** `05_Practice_Exercises.md`

**What's inside:**
- 3 practice exercises WITHOUT solutions
- Exercise 1: HR Analytics (Medium)
- Exercise 2: SaaS Subscription Analytics (Hard)
- Exercise 3: Social Media Analytics (Medium-Hard)

**When to use:** After Part 4, to test your skills independently.

---

## 🚀 Quick Start

1. **Read** `01_Foundation.md` (now)
2. **Do** `02_Day_00.md` and `02_Day_01.md` (today)
3. **Bookmark** `03_QUICK_Reference.md` (for later)

---

## 🧠 Key Mental Models

Translate your SQL knowledge to dbt:

| You Know (SQL) | You'll Learn (dbt) |
|----------------|-------------------|
| SQL script | dbt model (.sql file) |
| `CREATE TABLE AS` | `{{ config(materialized='table') }}` |
| `CREATE VIEW AS` | `{{ config(materialized='view') }}` |
| Hard-coded table: `FROM analytics.customers` | `FROM {{ ref('customers') }}` |
| Run scripts manually | `dbt run` (automatic dependencies) |
| No testing | `dbt test` (built-in framework) |
| No documentation | `dbt docs generate` (auto-created) |


---

## 📖 Supplemental Guides (Fill All Gaps)

### Gap-Filling Files
**Files:** `06` through `10`

**What's covered:**
- **06_Sample_Data_Setup.md** - Complete SQL scripts for all examples
- **07_Warehouse_Specific_Guide.md** - Snowflake, BigQuery, Redshift syntax
- **08_dbt_Cloud_Guide.md** - dbt Cloud IDE, jobs, team workflows
- **09_Advanced_Production_Topics.md** - Mesh, optimization, semantic layer
- **10_Complete_Troubleshooting.md** - All errors, edge cases, debugging

**When to use:** As needed when encountering specific situations.


```
dbt/
├── DBT-interview-plan-extracted.md         # PDF source (optional)
├── DBT-example-plan-extracted.md           # PDF source (optional)
└── learning/                                # YOUR LEARNING PATH
    ├── README.md                            # ← You are here
    │
    ├── 01_Foundation.md                     # Part 1: Start here
    ├── 02_Day_00.md                         # Day 0: Why dbt?
    ├── 02_Day_01.md                         # Day 1: Setup
    ├── 02_Day_02.md                         # Day 2: Models & ref()
    ├── 02_Day_03.md                         # Day 3: Sources & Seeds
    ├── 02_Day_04.md                         # Day 4: Testing
    ├── 02_Day_05.md                         # Day 5: Documentation
    ├── 02_Day_06.md                         # Day 6: Snapshots
    ├── 02_Day_07.md                         # Day 7: Macros, Inc, CI/CD
    ├── 03_QUICK_Reference.md                # Part 3: Quick lookup
    │
    ├── 04_Complete_Examples.md              # 2 end-to-end WITH solutions
    ├── 05_Practice_Exercises.md             # 3 exercises WITHOUT solutions
    │
    ├── 06_Sample_Data_Setup.md              # SQL scripts for sample data
    ├── 07_Warehouse_Specific_Guide.md       # Snowflake/BigQuery/Redshift
    ├── 08_dbt_Cloud_Guide.md                # dbt Cloud UI & workflows
    ├── 09_Advanced_Production_Topics.md     # Mesh, optimization, CI/CD
    └── 10_Complete_Troubleshooting.md       # All errors & fixes
```

---

## ⏱️ Time Commitment

- **Part 1:** 30 minutes reading
- **Part 2:** 7-14 hours total (1-2 hours/day for 7 days)
- **Part 3:** Ongoing reference

**Total:** ~2 weeks to dbt proficiency.

---

## 🎓 After This Course

You'll be able to:
- ✅ Transform data using dbt models
- ✅ Manage dependencies automatically
- ✅ Write and run data quality tests
- ✅ Generate documentation and lineage diagrams
- ✅ Build incremental models for large datasets
- ✅ Set up CI/CD for dbt projects

---

**Ready? Open `01_From_SQL_to_DBT.md` →**
