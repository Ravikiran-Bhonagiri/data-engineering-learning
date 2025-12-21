# dbt Cloud Guide

**Problem Solved:** Your company uses dbt Cloud instead of CLI.

This guide covers the dbt Cloud UI, IDE, jobs, and deployment.

---

## dbt Cloud vs dbt Core (CLI)

| Feature | dbt Core (CLI) | dbt Cloud |
|---------|---------------|-----------|
|**Development** | Local text editor + terminal | Web-based IDE |
| **Running models** | `dbt run` in terminal | Click "Run" button or schedule |
| **Documentation** | `dbt docs serve` locally | Auto-hosted docs site |
| **Orchestration** | Manual or external (Airflow) | Built-in scheduler |
| **Git Integration** | Manual git commands | Visual PR workflow |
| **Cost** | Free (open source) | Paid (free tier available) |
| **Best For** | Individual devs, local testing | Teams, production deployments |

---

## Getting Started with dbt Cloud

### Step 1: Sign Up

1. Go to [cloud.getdbt.com](https://cloud.getdbt.com)
2. Create account (free 14-day trial)
3. Choose tier:
   - **Developer** (free, 1 seat)
   - **Team** ($100/month, 8 seats)
   - **Enterprise** (custom pricing)

### Step 2: Connect Your Warehouse

**Snowflake Example:**
1. Click "Settings" → "Warehouse Connection"
2. Enter:
   - Account: `abc12345.us-east-1`
   - Database: `ANALYTICS`
   - Warehouse: `TRANSFORMING`
   - Role: `TRANSFORMER`
3. Test connection → Save

**BigQuery Example:**
1. Upload service account JSON
2. Enter project ID
3. Choose dataset location
4. Test → Save

### Step 3: Connect Git Repository

1. Click "Account Settings" → "Projects"
2. "Add Repository"
3. Choose:
   - **GitHub** (OAuth recommended)
   - **GitLab**
   - **Azure DevOps**
4. Select repository
5. Configure deployment credentials

---

## dbt Cloud IDE

### Interface Overview

```
┌─────────────────────────────────────────────────────────┐
│  [Project] [Branch: main ▼] [Commit] [Pull Request]    │  ← Top Bar
├──────────┬──────────────────────────────────────────────┤
│          │  models/staging/stg_customers.sql            │  ← Editor
│  Files   │  ┌──────────────────────────────────────┐    │
│  ├ models│  │ SELECT                                │    │
│  │ ├ staging│  │ id AS customer_id               │    │
│  │ └ marts│  │ FROM {{ source('raw','customers')}}│    │
│  ├ tests │  └──────────────────────────────────────┘    │
│  └ macros│                                               │
├──────────┼───────────────────────────────────────────────┤
│ Terminal │ dbt run --select stg_customers               │  ← Command Line
│          │ Running with dbt=1.7.0                        │
│          │ 1 of 1 OK created view dbt_dev.stg_customers │
└──────────┴───────────────────────────────────────────────┘
```

### Key Features

**1. File Browser (Left Panel)**
- Navigate dbt project
- Create new files
- Rename/delete files
- Search across project

**2. Code Editor (Center)**
- Syntax highlighting
- Auto-complete for `ref()` and `source()`
- Inline compilation preview
- Git diff view

**3. Command Line (Bottom)**
- Run dbt commands
- View compiled SQL
- See results/errors

**4. Top Bar**
- Commit changes
- Create Pull Request
- Switch branches
- Change environment

---

## Running dbt in Cloud IDE

### Via Command Line

```bash
# Standard commands work identically
dbt run
dbt test
dbt build --select +dim_customers

# Preview compiled SQL (without running)
dbt compile --select stg_customers
```

### Via UI Buttons

- **Build** → Runs selected model + tests
- **Preview** → Shows first 500 rows
- **Compile** → Shows compiled SQL

### Quick Actions

```bash
# Command + Enter (Mac) or Ctrl + Enter (Windows)
# Runs highlighted SQL in preview mode
```

---

## dbt Cloud Jobs (Production)

### Creating a Production Job

1. Click "Deploy" → "Jobs"
2. "Create Job"
3. Configure:

**Job Settings:**
```yaml
Name: "Daily Production Run"
Environment: Production
Commands:
  - dbt seed
  - dbt run
  - dbt test
Schedule: Every day at 2:00 AM UTC
```

**Advanced Options:**
- Threads: 4
- Target name: prod
- Generate docs: ✓
- Run on merge to main: ✓

### Continuous Integration (CI) Job

**Slim CI** (runs only changed models):

```yaml
Name: "PR Check"
Environment: Staging
Commands:
  - dbt build --select state:modified+ --defer --state ./prod
Triggers: On Pull Request
```

This runs only models that changed + their children!

---

## Development Workflow in dbt Cloud

### Step 1: Create Feature Branch

1. Click branch dropdown → "Create Branch"
2. Name: `feature/add-customer-metrics`
3. IDE switches to new branch

### Step 2: Make Changes

```sql
-- models/marts/customer_metrics.sql
SELECT
    customer_id,
    COUNT(*) AS total_orders
FROM {{ ref('stg_orders') }}
GROUP BY 1
```

### Step 3: Test Locally

```bash
dbt run --select customer_metrics
dbt test --select customer_metrics
```

### Step 4: Commit

1. Click "Commit" button
2. Write message: "Add customer metrics model"
3. Commit to branch

### Step 5: Create Pull Request

1. Click "Create Pull Request"
2. Fills out template automatically
3. CI job runs tests
4. Team reviews
5. Merge to main

### Step 6: Production Deployment

- Production job auto-runs on merge
- Or manually trigger: "Deploy" → "Run Now"

---

## dbt Cloud Features Not in CLI

### 1. Hosted Documentation

- Auto-hosted at `https://your-account.getdbt.com/docs`
- No `dbt docs serve` needed
- Shareable links for stakeholders
- Version controlled (by job run)

### 2. Job Scheduler

- Cron-like scheduling
- Dependency management (job chains)
- SLA monitoring
- Alerts (Slack, email, PagerDuty)

### 3. Visual Lineage Explorer

- Interactive DAG
- Filter by tags, folders
- Exposure tracking
- Source freshness indicators

### 4. Run History

- All past job runs
- Logs for each model
- Timing metrics
- Error tracking

### 5. dbt Semantic Layer

- Define metrics once
- Query via API
- BI tool integration (Looker, Tableau, etc.)

---

## Environment Variables in dbt Cloud

### Set in UI

1. "Deploy" → "Environments" → "Production"
2. "Environment Variables"
3. Add:
   ```
   DBT_SCHEMA_OVERRIDE = dbt_prod
   DBT_TARGET = prod
   ```

### Use in Code

```sql
-- models/example.sql
SELECT 
    *,
    '{{ env_var("DBT_TARGET") }}' AS target_name
FROM {{ ref('base_table') }}
```

---

## Best Practices for dbt Cloud

### Development

✅ **Use personal dev schema** (`dbt_yourname`)  
✅ **Commit often** (small, atomic commits)  
✅ **Test before PR** (`dbt build --select state:modified+`)  
✅ **Write good commit messages** (explain "why", not "what")  

### Production

✅ **Separate prod/staging environments**  
✅ **Use slim CI** (saves time + money)  
✅ **Monitor job runs** (set up Slack alerts)  
✅ **Version docs** (snapshot on each release)  
✅ **Use service accounts** (not personal credentials)  

### Security

✅ **Rotate passwords regularly**  
✅ **Use least-privilege warehouse roles**  
✅ **Enable SSO** (Enterprise tier)  
✅ **Audit logs** (who changed what)  

---

## dbt Cloud API

Programmatically trigger jobs:

```bash
# Trigger a job
curl -X POST \
  https://cloud.getdbt.com/api/v2/accounts/ACCOUNT_ID/jobs/JOB_ID/run/ \
  -H 'Authorization: Token YOUR_API_KEY'
```

Integrate with:
- Airflow (dbt Cloud provider)
- Prefect
- Dagster
- Custom orchestration

---

## Pricing (as of 2024)

| Tier | Price | Seats | Features |
|------|-------|-------|----------|
| **Developer** | Free | 1 | IDE, 1 job, basic support |
| **Team** | $100/mo | 8 | CI jobs, API, slack integration |
| **Enterprise** | Custom | Unlimited | SSO, audit logs, SLA |

---

## Keyboard Shortcuts

| Action | Mac | Windows |
|--------|-----|---------|
| Run selected | ⌘+Enter | Ctrl+Enter |
| Save file | ⌘+S | Ctrl+S |
| Find | ⌘+F | Ctrl+F |
| Command palette | ⌘+K | Ctrl+K |
| Format SQL | ⇧+⌥+F | Shift+Alt+F |

---

## Migrating from CLI to Cloud

1. **Push code to Git** (if not already)
2. **Sign up for dbt Cloud**
3. **Connect warehouse** (copy from `profiles.yml`)
4. **Connect Git repo**
5. **Create development environment**
6. **Open IDE** → verify connection
7. **Run `dbt run`** to test
8. **Create production job**
9. **Invite team members**

---

**dbt Cloud makes team collaboration 10x easier!** 🚀
