# Advanced Project 21: Lambda Stream Consumer (Event Source Mapping)

## 🎯 Goal
Master **Serverless Streaming**. We will build a Lambda function designed to consume high-throughput records from a **Kinesis Data Stream** (Project 12) using **Event Source Mapping**.

## 🛑 The "One-by-One" Problem
*   **Simple Trigger (Project 11):** S3 invokes Lambda once per file.
*   **Streaming Problem:** If you invoke Lambda for *every single* clickstream event (10,000/sec), you will hit concurrency limits and go bankrupt.
*   **Solution (ESM):** The internal Lambda Poller buffers 100 or 1,000 records into a **Batch** and invokes your function *once* for the whole batch.

## 🛠️ The Solution: Bisect on Error
What if Record #50 in a batch of 100 fails?
1.  **Standard Behavior:** The whole batch fails. The poller retries the whole batch. It fails again. (Poison Pill).
2.  **Advanced Config:** `BisectBatchOnFunctionError`. The poller splits the batch into two halves (1-50, 51-100) and retries. It keeps splitting until it isolates the single bad record.

## 🏗️ Architecture
1.  **Source:** Kinesis Data Stream (`clickstream-input`).
2.  **Mapping:** Batch Size = 100, Window = 10s.
3.  **Compute:** `stream_processor.py` (Iterates through records).
4.  **Error Handling:** Raises exception to trigger Bisection.

## 🚀 How to Run (Simulation)
1.  **Code:** `stream_processor.py`.
2.  **Event:** `kinesis_batch_event.json` (Mocking a batch of encoded records).
3.  **Run:**
    ```bash
    python stream_processor.py
    ```
