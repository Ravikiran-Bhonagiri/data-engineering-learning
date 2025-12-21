# Supplemental: CI/CD with Databricks Asset Bundles (DABs)

**Modern DevOps for Databricks Projects.**

---

## 📦 What are Asset Bundles?

Previously, deploying jobs involved messy JSON calls or Terraform. **DABs** allow you to define your entire project (jobs, pipelines, schemas) in YAML and deploy via CLI.

---

## 🛠 Project Structure

```
my-project/
├── databricks.yml      # The configuration
├── src/
│   ├── etl_job.py      # Python code
│   └── dlt_pipeline.py
├── resources/
│   └── job.yml         # Job definition
```

---

## 📄 `databricks.yml` Example

```yaml
bundle:
  name: my_etl_project

targets:
  dev:
    mode: development
    default: true
    workspace:
      host: https://adb-dev.databricks.com
  
  prod:
    mode: production
    workspace:
      host: https://adb-prod.databricks.com
      root_path: /Users/service-principal/projects

resources:
  jobs:
    daily_etl:
      name: "Daily ETL [${bundle.target}]"
      tasks:
        - task_key: main_task
          job_cluster_key: fixed_cluster
          python_wheel_task:
            package_name: my_package
            entry_point: entry_point
```

---

## 🚀 Deployment Workflow

1. **Develop (Dev Mode):**
   ```bash
   databricks bundle deploy -t dev
   databricks bundle run daily_etl -t dev
   ```
   *Note: In dev mode, it deploys to your personal folder to avoid conflicts.*

2. **Deploy (Prod Mode):**
   (Usually run by GitHub Actions / Jenkins)
   ```bash
   databricks bundle deploy -t prod
   ```

---

## 🧪 Testing

Integration tests in DABs:
You can define a "test" task in your job that runs validation logic (e.g., `pytest`) against the output tables created by the previous task.

---

## 🎯 Interview Q&A

**Q: How do you handle CI/CD in Databricks?**
A: "I use Databricks Asset Bundles (DABs). I define my infrastructure and jobs as code (YAML). My CI/CD pipeline (GitHub Actions) runs `databricks bundle validate` on PRs and `databricks bundle deploy -t prod` on merge to main. This ensures version control and reproducible deployments."

**Q: Can you use Terraform instead?**
A: "Yes, the Databricks Terraform Provider is excellent for infrastructure (Workspaces, Groups, Permissions). However, for application deployment (Jobs, Pipelines), DABs is preferred because it understands the development lifecycle better (dev vs prod modes)."
