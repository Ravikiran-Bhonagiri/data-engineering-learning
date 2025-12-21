# Docker Setup Guide

**Goal:** Run Airflow in Docker for local development and production.

---

## 🐳 Quick Start (Recommended)

### Step 1: Download Docker Compose

```bash
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.8.0/docker-compose.yaml'
```

### Step 2: Create Required Directories

```bash
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

### Step 3: Initialize Database

```bash
docker-compose up airflow-init
```

### Step 4: Start Airflow

```bash
docker-compose up
```

**Access UI:** `http://localhost:8080`  
**Login:** `airflow` / `airflow`

---

## 📋 Docker Compose Breakdown

### Key Services

```yaml
services:
  postgres:          # Metadata database
  redis:             # Celery broker
  airflow-webserver: # UI (port 8080)
  airflow-scheduler: # Task scheduler
  airflow-worker:    # Celery worker
  airflow-triggerer: # For deferrable operators
  airflow-init:      # DB initialization
  flower:            # Celery monitoring (port 5555)
```

---

## ⚙️ Customization

### Add Python Packages

**Method 1: requirements.txt**

```bash
# Create requirements.txt in project root
cat > requirements.txt << EOF
pandas==2.0.0
scikit-learn==1.3.0
great-expectations==0.18.0
EOF
```

Update `docker-compose.yaml`:
```yaml
x-airflow-common:
  &airflow-common
  # Add this line
  build: .
```

Create `Dockerfile`:
```dockerfile
FROM apache/airflow:2.8.0
COPY requirements.txt .
RUN pip install -r requirements.txt
```

**Method 2: Extend Image**

```dockerfile
FROM apache/airflow:2.8.0
USER root
RUN apt-get update && apt-get install -y gcc python3-dev
USER airflow
RUN pip install apache-airflow-providers-amazon
```

---

### Configure Environment Variables

Edit `.env` file:
```bash
AIRFLOW__CORE__LOAD_EXAMPLES=False
AIRFLOW__WEBSERVER__EXPOSE_CONFIG=False
AIRFLOW__CORE__PARALLELISM=32
AIRFLOW__CORE__MAX_ACTIVE_RUNS_PER_DAG=16
```

---

### Mount Local DAGs

Already configured in default docker-compose.yaml:
```yaml
volumes:
  - ${AIRFLOW_PROJ_DIR:-.}/dags:/opt/airflow/dags
  - ${AIRFLOW_PROJ_DIR:-.}/logs:/opt/airflow/logs
  - ${AIRFLOW_PROJ_DIR:-.}/plugins:/opt/airflow/plugins
```

Your local `./dags/` folder auto-syncs!

---

## 🏭 Production Considerations

### Use PostgreSQL (Not SQLite)

```yaml
services:
  postgres:
    image: postgres:14
    environment:
      POSTGRES_USER: airflow
      POSTGRES_PASSWORD: airflow
      POSTGRES_DB: airflow
    volumes:
      - postgres-db-volume:/var/lib/postgresql/data
```

### Scale Workers

```bash
# Scale to 3 workers
docker-compose up --scale airflow-worker=3
```

### Use External Database

```yaml
environment:
  AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://user:pass@external-db:5432/airflow
```

---

## 🔧 Useful Docker Commands

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (clean slate)
docker-compose down --volumes --remove-orphans

# View logs
docker-compose logs -f airflow-scheduler

# Access airflow CLI
docker-compose run airflow-worker airflow dags list

# Bash into container
docker exec -it <container_id> bash
```

---

## 🐛 Troubleshooting

### Issue: "Permission denied" errors

```bash
# Fix permissions
chmod -R 777 ./logs ./dags ./plugins
```

### Issue: Database connection refused

```bash
# Restart postgres
docker-compose restart postgres
```

### Issue: DAG not appearing

```bash
# Check for import errors
docker-compose run airflow-worker airflow dags list-import-errors
```

---

## 🎯 Production Checklist

- [ ] Use PostgreSQL, not SQLite
- [ ] Set strong passwords (change defaults!)
- [ ] Use secrets backend (AWS Secrets Manager, Vault)
- [ ] Enable HTTPS for webserver
- [ ] Configure resource limits in docker-compose
- [ ] Set up backup for postgres volume
- [ ] Use external Redis for Celery
- [ ] Monitor with Flower (`localhost:5555`)

---

**Docker is the fastest way to get production-ready Airflow!** 🐳
