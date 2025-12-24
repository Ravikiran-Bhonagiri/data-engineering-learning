# Foundation Project 2: The Nervous System (Apache Kafka)

## 🎯 Goal
Master the standard for **Real-Time Decoupling**. We will spin up a local Kafka cluster using Docker and implement a Producer/Consumer pattern in Python to simulate a high-speed trading feed.

## 🛑 The "Tight Coupling" Problem
In legacy systems, Service A calls Service B's API directly.
*   **Problem 1:** If Service B goes down, Service A fails (Cascading Failure).
*   **Problem 2:** If Service A sends data too fast, Service B crashes (Backpressure).
*   **Problem 3:** New consumers (Service C) can't plug in without changing Service A.

## 🛠️ The Solution: Kafka
Kafka acts as a **Log** buffer. Service A writes events to a "Topic". Service B (and C, and D) reads from that topic at its own pace.
1.  **Decoupling:** Producers don't know who Consumers are.
2.  **Durability:** Events are saved to disk (retention policy).
3.  **Scale:** Partitioning allows horizontal scaling.

## 🏗️ Architecture
1.  **Infrastructure:** Docker Compose (Zookeeper + Broker).
2.  **Producer:** Python script generating random "Trade" JSON events (`symbol`, `price`, `qty`).
3.  **Consumer:** Python script reading events and printing them (simulating a downstream processor).

## 🚀 How to Run

### 1. Start the Cluster
```bash
docker-compose up -d
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Producer (Terminal 1)
```bash
python producer.py
```
*You will see it sending trades...*

### 4. Run Consumer (Terminal 2)
```bash
python consumer.py
```
*You will see it receiving trades in real-time.*
