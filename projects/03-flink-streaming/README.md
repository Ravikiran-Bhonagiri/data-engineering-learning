# Foundation Project 3: Stateful Streaming (Apache Flink)

## 🎯 Goal
Master **Stateful Stream Processing**. We will move beyond simple "Stateless" message passing (Kafka) to complex "Stateful" aggregations using Apache Flink.

## 🛑 The "State" Problem
Kafka moves data from A to B. But what if you need to know:
*   "What is the total trading volume **per minute**?"
*   "Has this user failed login 5 times in the **last 10 seconds**?"

To answer these, you need **State** (memory of the past) and **Time** (windows). Doing this in a simple Python script is hard (what if the script crashes? you lose the count).

## 🛠️ The Solution: Apache Flink
Flink is a distributed stream processing engine that handles:
1.  **State Management:** It remembers counts/sums on disk (RocksDB) so you don't lose data on crash.
2.  **Event Time:** It handles out-of-order data correctly (processing data based on when it *happened*, not when it *arrived*).
3.  **Exactly-Once Semantics:** Guarantees results are accurate even if nodes fail.

## 🏗️ Architecture
1.  **Source:** Kafka Topic (`trades`).
2.  **Engine:** Flink Cluster (JobManager + TaskManager).
3.  **Logic (PyFlink):**
    *   Read from Kafka.
    *   Define a **Tumbling Window** (10 seconds).
    *   Sum `quantity` per `symbol`.
    *   Print results (or write back to Kafka/S3).

## 🚀 How to Run

### 1. Start the Stack
This spins up Kafka AND Flink.
```bash
docker-compose up -d
```

### 2. Enter the JobManager Container
```bash
docker-compose exec jobmanager ./bin/flink run -py /opt/flink/usrlib/aggregator.py
```

### 3. Generate Traffic
(In a separate terminal, use the producer from Project 2 or the included generator)
```bash
python producer.py
```

### 4. Watch the Output
Check the TaskManager logs to see the calculated aggregations.
```bash
docker-compose logs -f taskmanager
```
