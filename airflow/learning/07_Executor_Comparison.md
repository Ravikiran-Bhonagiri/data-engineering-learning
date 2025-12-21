# Executor Comparison Guide

**Goal:** Understand and choose the right executor for your use case.

---

## 🎯 Executor Overview

| Executor | Best For | Pros | Cons |
|----------|----------|------|------|
| **Sequential** | Local dev, testing | Simple, no deps | Single task at a time |
| **Local** | Small prod, single machine | No queue needed | Limited scaling |
| **Celery** | Large prod, distributed | Mature, scalable | Needs Redis/RabbitMQ |
| **Kubernetes** | Cloud-native, auto-scale | Isolation, elastic | K8s complexity |
| **Dask** | Data science workloads | Pandas integration | Less mature |

---

## 1. SequentialExecutor (Default)

### When to Use
- Local development
- Testing DAGs
- Learning Airflow

### Configuration
```python
# airflow.cfg
[core]
executor = SequentialExecutor
```

### Pros
✅ Zero configuration  
✅ Simple debugging  

### Cons
❌ Only 1 task at a time  
❌ NOT for production  

---

## 2. LocalExecutor

### When to Use
- Small production deployments
- Single powerful machine
- <100 concurrent tasks

### Configuration
```python
# airflow.cfg
[core]
executor = LocalExecutor
parallelism = 32

[database]
sql_alchemy_conn = postgresql+psycopg2://user:pass@localhost/airflow
```

### Pros
✅ No queue infrastructure needed  
✅ Fast task startup  
✅ Easy to debug  

### Cons
❌ Single point of failure  
❌ Doesn't scale horizontally  
❌ Requires PostgreSQL/MySQL  

### Example Setup
```bash
# Install with postgres support
pip install apache-airflow[postgres]

# Update airflow.cfg
executor = LocalExecutor

# Restart scheduler
airflow scheduler
```

---

## 3. CeleryExecutor

### When to Use
- Large production deployments
- Need horizontal scaling
- 100+ concurrent tasks
- Multiple worker machines

### Architecture
```
┌──────────┐
│Scheduler │ ── Tasks ──> Redis/RabbitMQ
└──────────┘                    ↓
                        ┌───────────────┐
                        │  Worker Pool  │
                        │ ┌──┬──┬──┬──┐ │
                        │ │W1│W2│W3│W4│ │
                        │ └──┴──┴──┴──┘ │
                        └───────────────┘
```

### Configuration

**airflow.cfg:**
```ini
[core]
executor = CeleryExecutor

[celery]
broker_url = redis://localhost:6379/0
result_backend = db+postgresql://user:pass@localhost/airflow
worker_concurrency = 16
```

**Start Workers:**
```bash
# Terminal 1: Redis
redis-server

# Terminal 2: Scheduler
airflow scheduler

# Terminal 3+: Workers (can be on different machines!)
airflow celery worker --concurrency 16
```

### Monitoring with Flower
```bash
airflow celery flower
# Access: http://localhost:5555
```

### Pros
✅ Horizontal scaling (add more workers)  
✅ Mature and battle-tested  
✅ Task queues for priority  
✅ Works across multiple machines  

### Cons
❌ Requires Redis/RabbitMQ  
❌ More complex setup  
❌ Network latency  

---

## 4. KubernetesExecutor

### When to Use
- Cloud-native deployments
- Need task isolation
- Auto-scaling requirements
- Different resource needs per task

### Architecture
```
┌──────────┐
│Scheduler │ ── Creates Pod ──> Kubernetes API
└──────────┘                          ↓
                              ┌────────────────┐
                              │  K8s Cluster   │
                              │ ┌────┬────┬───┐│
                              │ │Pod1│Pod2│...││
                              │ └────┴────┴───┘│
                              └────────────────┘
```

### Configuration

**airflow.cfg:**
```ini
[core]
executor = KubernetesExecutor

[kubernetes]
namespace = airflow
pod_template_file = /path/to/pod_template.yaml
worker_container_repository = apache/airflow
worker_container_tag = 2.8.0
```

**Pod Template (pod_template.yaml):**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: airflow-worker
spec:
  containers:
    - name: base
      image: apache/airflow:2.8.0
      resources:
        requests:
          memory: "512Mi"
          cpu: "500m"
        limits:
          memory: "2Gi"
          cpu: "2000m"
```

### Task-Specific Resources
```python
@task(
    executor_config={
        "pod_override": k8s.V1Pod(
            spec=k8s.V1PodSpec(
                containers=[
                    k8s.V1Container(
                        name="base",
                        resources=k8s.V1ResourceRequirements(
                            requests={"memory": "4Gi", "cpu": "2"},
                            limits={"memory": "8Gi", "cpu": "4"},
                        ),
                    )
                ]
            )
        )
    }
)
def heavy_task():
    # This task gets 4-8GB RAM, 2-4 CPUs
    pass
```

### Pros
✅ Perfect isolation (each task = separate pod)  
✅ Auto-scaling with K8s  
✅ Different resources per task  
✅ Cloud-native  

### Cons
❌ Kubernetes expertise required  
❌ Slower task startup (pod creation)  
❌ More expensive (cloud costs)  

---

## 🔄 Hybrid: CeleryKubernetesExecutor

Run different executors for different tasks!

### Configuration
```ini
[core]
executor = CeleryKubernetesExecutor
```

### Usage
```python
# Default tasks use Celery
@task
def fast_task():
    pass

# Heavy tasks use Kubernetes
@task(queue='kubernetes')  # 'kubernetes' is special queue
def heavy_ml_task():
    # Gets its own pod with 32GB RAM
    pass
```

---

## 📊 Decision Matrix

### Choose **Sequential** if:
- Learning Airflow
- Testing DAGs locally

### Choose **Local** if:
- Small production (<50 DAGs)
- Single powerful machine
- Simple setup required

### Choose **Celery** if:
- Multiple worker machines
- Mature solution preferred
- Horizontal scaling needed

### Choose **Kubernetes** if:
- On cloud (AWS/GCP/Azure)
- Task isolation critical
- Auto-scaling required
- Different resource needs per task

---

## 🎯 Migration Path

**Typical Evolution:**
```
Sequential (Dev)
    ↓
LocalExecutor (Small Prod)
    ↓
CeleryExecutor (Scaling)
    ↓
KubernetesExecutor (Cloud-Native)
```

---

**Choose wisely based on your scale and infrastructure!** 🚀
