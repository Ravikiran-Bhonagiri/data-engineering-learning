# Advance Project 30: Log Analytics (Amazon OpenSearch)

## 🎯 Goal
Master **Full-Text Search & Observability**. We will build a pipeline that ingests server logs into **Amazon OpenSearch Service** (formerly Elasticsearch) to enable real-time dashboarding (Kibana/OpenSearch Dashboards) and error hunting.

## 🛑 The "Grep" Problem
*   **Scenario:** Production logic fails. You have 50 servers producing logs.
*   **Bad Way:** SSH into each server and run `grep "ERROR" /var/log/app.log`.
*   **Solution (ELK Stack):** Centralize all logs into OpenSearch. Search `level:ERROR` in a web UI and see hits from all 50 servers instantly.

## 🛠️ The Solution: Indexing
OpenSearch is a Document Store (JSON). We "index" documents so they are searchable.
*   **Pipeline:** App -> Firehose (or Lambda) -> OpenSearch.

## 🏗️ Architecture
1.  **Source:** Application Logs (JSON).
2.  **Indexer:** Python Script (`log_indexer.py`).
3.  **Dest:** OpenSearch Index (`app-logs-2024`).

## 🚀 How to Run (Simulation)
1.  **Code:** `log_indexer.py` (Uses `opensearch-py` library).
2.  **Run:**
    ```bash
    python log_indexer.py
    ```
