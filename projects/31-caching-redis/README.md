# Advance Project 31: Microsecond Caching (Redis)

## 🎯 Goal
Master **High-Performance Data Access**. We will implement the **Cache-Aside (Look-Aside)** pattern using Redis. This is the standard pattern for effortless scaling of read-heavy workloads (e.g., User Profiles, Feature Stores).

## 🛑 The "Database Hammer" Problem
*   **Scenario:** You have 1 Million active users. Every time they visit the home page, you query `SELECT * FROM users WHERE id = X`.
*   **Problem:** Your database CPU spikes to 100%. Latency increases to 200ms.
*   **Solution (Caching):** Store the profile in RAM (Redis). Access takes < 1ms. Database load drops by 99%.

## 🛠️ The Solution: Cache-Aside Pattern
1.  **Read:** App checks Redis.
    *   **Hit:** Return data immediately.
    *   **Miss:** Fetch from DB -> Write to Redis (with TTL) -> Return data.
2.  **Write:** Update DB -> Invalidate (Delete) Redis key.

## 🏗️ Architecture
1.  **App:** Python Script.
2.  **L1 Cache:** Redis (Cluster Mode enabled in prod).
3.  **L2 Storage:** DynamoDB / Postgres.

## 🚀 How to Run (Simulation)
1.  **Code:** `cache_aside.py` (Uses `redis-py` logic).
2.  **Run:**
    ```bash
    python cache_aside.py
    ```
