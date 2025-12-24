# Foundation Project 7: Orchestration (Apache Airflow)

## 🎯 Goal
Master **Dependency Management**. We will use **Apache Airflow** to schedule a pipeline that handles complex logic like "Wait for File A, THEN run Process B, BUT ONLY IF it's a weekday."

## 🛑 The "Cron" Problem
Cron jobs (`0 7 * * * script.sh`) are fragile:
*   **No Retries:** If the network blips, the job dies and you find out the next day.
*   **No Dependency:** If Job A takes 2 hours instead of 1, Job B starts processing partial data.
*   **No Backfill:** If you fix a bug, you have to manually run script.sh 30 times for the past month.

## 🛠️ The Solution: Airflow
Airflow defines workflows as **DAGs** (Directed Acyclic Graphs) in Python code:
1.  **Operators:** Templates for tasks (e.g., `PythonOperator`, `BashOperator`, `SqlOperator`).
2.  **Sensors:** Tasks that wait for something to happen (e.g., `FileSensor` waits for S3 file).
3.  **scheduler:** Handles retries, backfills, and SLA alerts.

## 🏗️ Architecture
1.  **Webserver:** The UI to monitor DAGs.
2.  **Scheduler:** The brain that triggers tasks.
3.  **Worker:** Executes the tasks.
4.  **DAG:** The Python file defining the logic.

## 🚀 How to Run
1.  Start Airflow:
    ```bash
    docker-compose up -d
    ```
2.  Access UI: `http://localhost:8080` (User: `airflow`, Pass: `airflow`)
3.  Enable the `example_etl_pipeline` DAG.
4.  Watch the tasks turn dark green (Success) in the Grid View.
