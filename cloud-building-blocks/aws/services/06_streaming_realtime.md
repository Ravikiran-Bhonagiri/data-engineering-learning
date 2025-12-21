# Streaming & Real-time 🌊

[← Back to Main](../README.md)

For data that can't wait for "Tomorrow's batch job."

---

## [Amazon Kinesis Data Streams](https://aws.amazon.com/kinesis/data-streams/)

Collect and process large streams of data records in real-time.

- **Why it matters:** The backbone of real-time apps. It can handle millions of events per second (logs, clickstreams, IoT data).
- **Common Task:** Ingesting clickstream data from websites in real-time
### ✅ When to Use (Velocity Drives the Decision)

1. **Real-time Requirements (<1 minute latency)**
   - **Need:** Process clickstream within 30 seconds for personalization
   - **Kinesis:** Millisecond ingestion, second-level processing
   - **Vs Batch (S3):** Hourly batch = 60min lag (too slow)
   - **Cost trade-off:** $0.015/shard-hour worth it for real-time UX

2. **Multi-Consumer Pattern (Flexibility)**
   - **Use Case:** Same event stream → Lambda, Firehose, Analytics
   - **Why Kinesis:** Replay capability, multiple independent consumers
   - **Start Simple:** 1 stream (2 shards) = $22/month, 3 consumers
   - **Vs SQS:** Can't replay; Kinesis keeps data 1-365 days

3. **Start Small, Scale Predictably**
   - **Start:** 1 shard (1MB/s) = $11/month for dev/test
   - **Scale:** Auto-scale to 100 shards at peak = $1,100/month
   - **Cost:** Predictable scaling ($11 per 1MB/s throughput)
   - **Complexity:** AWS manages infrastructure

4. **When Simplicity (Firehose) Isn't Enough**
   - **Firehose limits:** Only S3/Redshift/OpenSearch/HTTP
   - **custom processing or routing needed
   - **Kinesis:** Write custom Lambda consumers, complex logic
   - **Decision:** Firehose if destination supported, Streams otherwise

5. **Ordered Processing Required (Partition keys)**
   - **Use Case:** Process all user events in order (partition by user_id)
   - **Why Kinesis:** Maintains order within shard
   - **Example:** Bank transactions must process sequentially
   - **Vs SQS Standard:** No ordering guarantees

### ❌ When NOT to Use

- **Just need data in S3:** Use Firehose ($0.029/GB) - simpler, cheaper
- **Batch acceptable (>1hr lag):** Use S3 + Glue - avoid streaming overhead
- **Very low volume (<10KB/s):** SQS cheaper for tiny volumes
- **Exactly-once semantics:** Kinesis is at-least-once; use SQS FIFO or MSK
- **Cost-sensitive + sporadic load:** Firehose pay-per-GB vs Kinesis 24/7 shard cost

### Code Example - Produce to Kinesis

```python
import boto3
import json
from datetime import datetime

kinesis = boto3.client('kinesis')

# Send a record
response = kinesis.put_record(
    StreamName='user-events',
    Data=json.dumps({
        'user_id': '12345',
        'event': 'page_view',
        'timestamp': datetime.utcnow().isoformat()
    }),
    PartitionKey='user-12345'
)

print(f"Sequence number: {response['SequenceNumber']}")
```

---

## [Amazon Kinesis Data Firehose](https://aws.amazon.com/kinesis/data-firehose/)

The easiest way to load streaming data into AWS data stores.

- **Why it matters:** It can automatically buffer streaming data and write it to S3, Redshift, or OpenSearch without you writing a single line of code.
- **Common Task:** Streaming application logs to S3 for long-term storage
- **Pricing:** $0.029 per GB ingested

---

## [Amazon Kinesis Data Analytics](https://aws.amazon.com/kinesis/data-analytics/)

Process and analyze streaming data using SQL or Apache Flink.

- **Why it matters:** Run SQL queries on streaming data for real-time analytics.
- **Common Task:** Calculating rolling averages, detecting anomalies in real-time

---

## [Amazon MSK (Managed Streaming for Apache Kafka)](https://aws.amazon.com/msk/)

Fully managed Apache Kafka service.

- **Why it matters:** When you need Kafka's ecosystem and flexibility but don't want to manage clusters.
- **Common Task:** Building event-driven architectures with Kafka topics
- **Pricing:** ~$0.21/hour per broker (kafka.m5.large)

---

## Related Topics

- **[Service Comparisons](12_service_comparisons.md)**: Kinesis Streams vs Firehose comparison
- **[Advanced Architectures](15_advanced_architectures.md)**: Lambda architecture (real-time + batch)
- **[Architecture Patterns](11_architecture_patterns.md)**: Real-time analytics pipeline

[← Back to Main](../README.md)
