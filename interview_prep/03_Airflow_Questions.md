# Airflow Interview Questions Master List (100+)

**Ratio:** ~20% Simple | ~40% Medium | ~40% Hard

---

## 🟢 Simple (Concepts - 20 Questions)

1.  **What is Airflow?**
    *   Platform to programmatically author, schedule, and monitor workflows.
2.  **What does DAG stand for?**
    *   Directed Acyclic Graph.
3.  **What language is Airflow written in?**
    *   Python.
4.  **What is an Operator?**
    *   Template for a specific task (BashOperator, PythonOperator).
5.  **What is a Task?**
    *   An instantiated Operator (Node in the graph).
6.  **What is the Scheduler?**
    *   Component that triggers tasks based on time/dependencies.
7.  **What is the Webserver?**
    *   The UI for monitoring and triggering DAGs.
8.  **What is `start_date`?**
    *   The timestamp when the DAG starts being scheduled.
9.  **What is `execution_date`?**
    *   The logical past timestamp the run is for (End of interval usually).
10. **What is a "Sensor"?**
    *   A task that waits for an external event (File arrival).
11. **What is a Hook?**
    *   Interface to external platforms (AWS, JDBC) handling auth.
12. **What is XCom?**
    *   Cross-Communication. Message passing between tasks.
13. **What is a Connection?**
    *   Credentials stored in DB (URI format) to access systems.
14. **What is a Variable?**
    *   Key-Value pair stored in DB for global config.
15. **What is Backfilling?**
    *   Running DAGs for past dates.
16. **What is `catchup`?**
    *   Boolean. If True, scheduler runs non-triggered past runs from start_date.
17. **What is a worker?**
    *   The process actually executing the task logic.
18. **What is the Metadata Database?**
    *   SQL DB (Postgres/MySQL) storing DAG state.
19. **What is a "DAG Run"?**
    *   Instance of a DAG for a specific execution_date.
20. **Can you manually trigger a DAG?**
    *   Yes, via UI or CLI.

---

## 🟡 Medium (Development & Config - 40 Questions)

21. **Explain the `BashOperator`.**
    *   Executes shell commands.
22. **Explain the `PythonOperator`.**
    *   Executes a python callable (function).
23. **How do you define dependencies?**
    *   `task1 >> task2` or `task1.set_downstream(task2)`.
24. **What is `depends_on_past`?**
    *   Task instance depends on the success of the previous run's task instance.
25. **What is the default Executor?**
    *   SequentialExecutor (Dev only). Production uses Celery/K8s.
26. **Explain CeleryExecutor.**
    *   Distributes tasks to worker nodes via Queue (Redis/RabbitMQ).
27. **Explain KubernetesExecutor.**
    *   Launches a new Pod for every task.
28. **How to pass parameters to `PythonOperator`?**
    *   `op_args` or `op_kwargs`.
29. **What is the limit of XCom size?**
    *   Depends on DB (~64KB is typical limit). Don't modify big data.
30. **What is `BranchPythonOperator`?**
    *   Returns the task_id(s) of the next task to execution, skipping others.
31. **How to trigger one DAG from another?**
    *   `TriggerDagRunOperator`.
32. **What is a SLA (Service Level Agreement)?**
    *   Time by which a task should have finished. Triggers callback if missed.
33. **What is a "Pool"?**
    *   Limits concurrency for specific tasks (e.g., "db_slot_pool" = 5 slots).
34. **How do you install python packages in Airflow?**
    *   pip install in the Docker image or env where workers run.
35. **What is `schedule_interval`?**
    *   Cron expression or `@daily` preset defining frequency.
36. **Difference: Cron vs Airflow scheduling.**
    *   Cron runs at time T. Airflow (historically) runs at T + Interval (Wait for period end).
37. **What is the "TaskFlow API"?**
    *   Decorators `@task` and `@dag` in Airflow 2.0. Cleaner syntax.
38. **How to hide passwords in Connections?**
    *   Fernet Key encryption.
39. **What is `max_active_runs`?**
    *   Limit concurrent DAG runs (prevents flooding).
40. **What is `concurrency` (DAG level)?**
    *   Limit tasks running in parallel across all runs of that DAG.
41. **How to handle Timezones?**
    *   Use Pendulum/UTC.
42. **What is `retries`?**
    *   Number of times to restart functionality upon failure.
43. **What is `retry_delay`?**
    *   Time to wait between retries (Exponential backoff possible).
44. **What is a "DummyOperator" (or EmptyOperator)?**
    *   Do nothing. Used for grouping/visual organization.
45. **How to test a Task?**
    *   `airflow tasks test dag_id task_id date`.
46. **What is `airflow db init`?**
    *   Initializes the metadata tables.
47. **What is a "SubDAG"?**
    *   (Deprecated) Embedding a DAG in a DAG.
48. **What is a "TaskGroup"?**
    *   UI grouping concept (Replacement for SubDAG).
49. **What is `executor_config`?**
    *   Pass K8s specific config (RAM/CPU) to K8sExecutor.
50. **How to use Templating (Jinja) in Airflow?**
    *   `{{ ds }}` (Date string), `{{ params.x }}`. available in `template_fields`.
51. **Safe way to parse top-level code?**
    *   Don't do DB calls. Only define structure.
52. **What happens if you delete a DAG file?**
    *   Scheduler stops scheduling. Metadata remains in DB.
53. **How to clear task state?**
    *   UI -> "Clear". Resets state to None. Scheduler retries.
54. **What is `sla_miss_callback`?**
    *   Function called on SLA breach.
55. **Difference: Schedule `None` vs `@once`.**
    *   None = Manual trigger only. Once = Runs one time.
56. **Dynamic DAG generation?**
    *   Global file generating DAG objects in loop.
57. **Sensor `poke_interval`?**
    *   Time between checks.
58. **Sensor `timeout`?**
    *   Max time before failing the sensor.
59. **What implies `failed_upstream` state?**
    *   Parent failed, so child cannot run (Trigger rule default).
60. **Trigger Rule: `all_done`?**
    *   Run task regardless of parent success/fail (Cleanup task).

---

## 🔴 Hard (Production & Architecture - 40 Questions)

61. **Debug "Scheduler Heartbeat" issues.**
    *   Scheduler loop frozen. CPU overload. DB latency.
62. **Optimization: "Smart Sensors" / Deferrable Operators.**
    *   Offload wait to `Triggerer` service (Asyncio). Frees worker slot.
63. **Backfill strategy for 5 years of data?**
    *   `airflow dags backfill`. CLI command. Use `-n` (dry run). Run in chunks.
64. **Explain Celery Redis vs RabbitMQ.**
    *   Broker choice. Redis (In-memory, fast, persistence config needed). RabbitMQ (Robust queuing).
65. **Handle "Zombie Tasks".**
    *   Task running but heartbeat missing. Scheduler kills it. Cause: OOM, Network split.
66. **Scaling Airflow to 10k DAGs.**
    *   Use many Schedulers (HA). Optimize parsing speed. External DB.
67. **How does HA Scheduler work (Airflow 2.0)?**
    *   Active-Active. Uses Row-level locking on DB (`SELECT FOR UPDATE SKIP LOCKED`) to grab tasks.
68. **Secure access to UI.**
    *   RBAC + OAuth/LDAP integration.
69. **How to version DAGs?**
    *   Git Sync. Rolling updates are hard. Rename DAG (`_v2`) is safest.
70. **Race conditions in Backfills?**
    *   Tasks dependent on external global state that isn't partitioned by time.
71. **Short Lived vs Long Lived Tasks.**
    *   Airflow meant for orchestration (start job, wait), not execution (processing 10GB Dataframe).
72. **Secrets Backend.**
    *   Store connections in AWS Secrets Manager / Hashicorp Vault instead of Airflow DB.
73. **Custom Operator creation.**
    *   Inherit `BaseOperator`, implement `execute(context)`.
74. **What is `on_failure_callback`?**
    *   Function to alert PagerDuty/Slack on fail.
75. **LocalExecutor vs SequentialExecutor.**
    *   Sequential (SQLite, Single Thread). Local (Parallel processes on one machine).
76. **How to persist data between tasks (Large Data)?**
    *   Intermediate storage (S3). XCom pass the *path* `s3://bucket/file.csv`.
77. **Explain "Idempotency" in Airflow tasks.**
    *   Rerunning task implies same result. Use transaction/upsert logic.
78. **Handling "Late Arriving Data" with Sensors.**
    *   `TimeDeltaSensor` or `soft_fail=True`.
79. **Dataset-driven scheduling (Airflow 2.4+).**
    *   Producer task updates Dataset. Consumer DAG schedule=`[Dataset("uri")]`.
80. **KubernetesPodOperator benefits.**
    *   Environment isolation. Any language (Docker image).
81. **Why avoid `datetime.now()` in DAG code?**
    *   Makes runs non-deterministic. Use `execution_date` context.
    *   Also, used in top-level code breaks parsing? (No, but confusing).
82. **What is `airflow.cfg`?**
    *   Global config. Executor, sql_alchemy_conn, parallelism limits.
83. **Troubleshoot: Task stuck in "Queued".**
    *   Pool full? Concurrency limit hit? Scheduler down? Broker connection?
84. **What is `airflow db clean`?**
    *   Archiving/Deleting old logs and metadata to speed up DB.
85. **Explain `max_map_length` (Dynamic Task Mapping).**
    *   Limit on fan-out size for mapped tasks.
86. **Logging options.**
    *   Local, S3, GCS, Elasticsearch. Centralized logging essential for K8s.
87. **Difference: Variable vs Environment Variable.**
    *   Env Var (System level, faster, secrets). Variable (DB level, changable in UI).
88. **How DAG Serialization works.**
    *   Webserver reads JSON from DB (fast) instead of parsing Python (slow).
89. **Priority Weights.**
    *   Prioritize critical DAGs in queue.
90. **Running Airflow on Windows?**
    *   Not natively supported. Use Docker/WSL.
91. **What is 'Lineage' backend?**
    *   OpenLineage integration.
92. **Complex Branching Logic.**
    *   `Task A >> [B, C]`. use `Search` or `BranchPythonOperator`.
93. **What is `trigger_rule='one_success'`?**
    *   Run if at least one parent succeeded. (OR gate).
94. **Timetables (Airflow 2.2).**
    *   Custom scheduling logic (e.g., "Trading days only", exclude holidays).
95. **Plugin system.**
    *   Adding custom UI menus, blueprints, operators via `plugins` folder.
96. **Handling API Rate Limits.**
    *   Use Pools or `reschedule` sensors with delay.
97. **Cluster Policies.**
    *   Enforce default args (owner, retries) across all DAGs via `airflow_local_settings.py`.
98. **Operator Linking.**
    *   "Extra Links" button in UI to go to external system (Databricks run URL).
99. **Setup Teardown tasks (Airflow 2.7).**
    *   `setup >> work >> teardown`. Teardown runs even if work fails.
100. **The "Great Scheduling Refactor" (AIP-39).**
    *   Decoupling logical date from run date.
