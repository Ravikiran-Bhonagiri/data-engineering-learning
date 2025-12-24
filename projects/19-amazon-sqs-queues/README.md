# Foundation Project 19: Decoupled Queues (Amazon SQS)

## 🎯 Goal
Master **Resilience**. We will implement the **Dead Letter Queue (DLQ)** pattern to handle failures gracefully. Instead of crashing the whole pipeline when bad data arrives, we shunt it aside to an SQS Queue for manual inspection and replay.

## 🛑 The "Crash Loop" Problem
*   **Scenario:** You process 10,000 orders per minute.
*   **Bug:** Order #5000 is malformed (missing 'price').
*   **Result:** The script crashes. You restart it. It processes 1-4999, hits #5000, and crashes again. The pipeline is blocked forever ("Poison Pill").

## 🛠️ The Solution: SQS Dead Letter Queue
1.  **Main Queue:** Normal traffic.
2.  **Processing Logic:** Try to process. If error -> `Try/Catch`.
3.  **On Catch:** Send the **failed** message payload to a separate `OrderDLQ`.
4.  **Redrive:** A separate Admin script reads the DLQ, fixes the data (or logs it), and re-injects it.

## 🏗️ Architecture
1.  **Producer:** Simulates incoming orders (some valid, some bad).
2.  **Processor:** Tries to "Invoice" the order. Fails on bad ones.
3.  **DLQ:** Amazon SQS Queue holding the failures.

## 🚀 How to Run (Simulation)
1.  **Process Orders:**
    ```bash
    python process_orders.py
    ```
    *Observe that it processes valid orders but "sends" bad ones to SQS.*

2.  **Redrive DLQ:**
    ```bash
    python dlq_redrive.py
    ```
    *Observe that it picks up the failed messages and retries them.*
