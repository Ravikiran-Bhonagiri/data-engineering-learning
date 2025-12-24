# Advanced Project 22: Kinesis Analytics (Windowed SQL)

## 🎯 Goal
Master **Serverless Streaming SQL**. We will use (Legacy) **Kinesis Data Analytics** to query live data flowing through a Kinesis Stream, calculating a **Sliding Window** average.

## 🛑 The "Micro-Batch" Problem
*   **Spark Streaming:** Process data in mini-batches (e.g., every 5 seconds).
*   **Latency:** You verify the average "every 5 seconds".
*   **Continuous:** What if you want to update the average *every time a new event arrives*?
*   **Solution:** Continuous Streaming SQL.

## 🛠️ The Solution: Sliding Windows
Unlike a **Tumbling Window** (Project 3) which resets every minute (00:00, 00:01), a **Sliding Window** moves with the data.
*   "Average price over the last 1 minute, updated every second."

## 🏗️ Architecture
1.  **Source Stream:** `INPUT_STREAM` (from Project 12 Producer).
2.  **Pump:** A continuous query logic that "pumps" data from Source to Destination.
3.  **Dest Stream:** `OUTPUT_STREAM` (Derived analytics).

## 🚀 How to Run (Simulation)
This code uses the AWS Kinesis Analytics (SQL) syntax.
1.  **SQL:** `sliding_window.sql`.
2.  **Deployment:** Only runnable in AWS Console (Kinesis Analytics Application).
