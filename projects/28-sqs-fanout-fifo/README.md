# Advanced Project 28: SQS Fan-Out & FIFO

## 🎯 Goal
Master **Enterprise Messaging Patterns**. We will implement the **Fan-Out** architecture using **SNS (Simple Notification Service)** and **SQS FIFO**, ensuring that one event can trigger multiple downstream systems (Decoupling) while maintaining strict ordering (FIFO).

## 🛑 The "Ordering" Problem
*   **Standard SQS:** Is "Best Effort" ordering. Sometimes Message B arrives before Message A.
*   **Financial Data:** If "Debit $50" arrives before "Credit $50", reading the balance might fail.
*   **Solution (FIFO):** Guarantees Exactly-Once processing in the exact order received, using `MessageGroupId`.

## 🛠️ The Solution: SNS Fan-Out
1.  **Publisher:** Sends message to **SNS Topic**.
2.  **Subscriber A (SQS FIFO):** "Billing Queue" (Needs Order).
3.  **Subscriber B (SQS Standard):** "Email Queue" (Order doesn't matter).
4.  **Result:** One message -> Multiple Systems.

## 🏗️ Architecture
```mermaid
graph LR
    App -->|Publish| SNS[SNS Topic]
    SNS -->|Sub| SQS1[SQS FIFO (Billing)]
    SNS -->|Sub| SQS2[SQS Standard (Notifications)]
```

## 🚀 How to Run (Simulation)
1.  **Code:** `fanout_architecture.py`.
2.  **Logic:** Simulates publishing to SNS and separate consumers reading from SQS.
