# Foundation Project 15: NoSQL & State (Amazon DynamoDB)

## 🎯 Goal
Master **Single-Digit Millisecond Latency**. We will implement a "User Profile" store using **DynamoDB Single Table Design (STD)**, learning how to model specific access patterns rather than normalized tables.

## 🛑 The "RDBMS for Everything" Problem
*   **Scenario:** You have 100 Million users. You need to look up User A's profile on every login.
*   **SQL Problem:** `SELECT * FROM users WHERE id = 'A'` works, but as you scale to billions of rows or add joins (Orders, Addresses), latency spikes to 200ms+.
*   **DynamoDB Solution:** It guarantees <10ms latency at *any* scale, provided you design for the **Primary Key**.

## 🛠️ The Solution: Single Table Design
Instead of `Users` table and `Orders` table, we use one table with generic keys:
1.  **Partition Key (PK):** Groups data physically (e.g., `USER#123`).
2.  **Sort Key (SK):** Sorts data within the partition (e.g., `PROFILE`, `ORDER#999`).
3.  **Access Pattern:** `PK=USER#123` AND `SK=PROFILE` -> Get User Details.

## 🏗️ Architecture
1.  **Table:** `MegaTable` (Generic name).
2.  **Item (Profile):** `PK: USER#123`, `SK: PROFLIE`, `Data: {Name: Alice}`.
3.  **Item (Order):** `PK: USER#123`, `SK: ORDER#55`, `Data: {Total: $50}`.

## 🚀 How to Run (Simulation)
1.  **Code:** `user_profile.py` uses `boto3`.
2.  **Run:**
    ```bash
    python user_profile.py
    ```
    *Note: This script mocks the AWS response if credentials are missing.*
