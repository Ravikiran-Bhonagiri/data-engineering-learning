# Advanced Project 25: DynamoDB Streams (Change Data Capture)

## 🎯 Goal
Master **Database Triggers**. We will implement a **Change Data Capture (CDC)** pipeline. Whenever a user profile is created/updated in our DynamoDB table (Project 15), a Lambda function will immediately wake up to "Process" that change (e.g., Audit Logging or Syncing to OpenSearch).

## 🛑 The "Dual Write" Problem
*   **Scenario:** You modify a user's address. You need to update the Database AND the Search Engine (OpenSearch/Solr).
*   **Bad Approach:**
    ```python
    db.update_user(...)
    # If DB succeeds but Search fails, data is inconsistent!
    search.update_user(...)
    ```
*   **Solution (CDC):** Write to DynamoDB *only*. DynamoDB guarantees to push the change to a "Stream". Lambda consumes the Stream and updates Search. Eventual Consistency is guaranteed.

## 🛠️ The Solution: DynamoDB Streams
1.  **Stream:** An ordered log of changes (Insert/Modify/Delete).
2.  **View:** `NEW_AND_OLD_IMAGES` (We see what the item looked like before and after).
3.  **Trigger:** Lambda is invoked synchronously with a batch of changes.

## 🏗️ Architecture
1.  **Source:** DynamoDB (`MegaTable_Dev`).
2.  **Stream:** Enabled (`ViewType=NEW_AND_OLD_IMAGES`).
3.  **Consumer:** `stream_listener.py` (Lambda).

## 🚀 How to Run (Simulation)
1.  **Code:** `stream_listener.py`.
2.  **Event:** `test_stream_event.json` (Mocks the specific JSON format of a DynamoDB Stream record).
3.  **Run:**
    ```bash
    python stream_listener.py
    ```
