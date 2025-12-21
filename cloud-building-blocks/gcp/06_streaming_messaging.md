# Streaming & Messaging 🌊

[← Back to Main](README.md)

Real-time messaging and stream processing on GCP.

---

## [Pub/Sub](https://cloud.google.com/pubsub)

Asynchronous messaging service for event-driven architectures (like AWS Kinesis + SNS).

- **Why it matters:** **The** messaging backbone of GCP. Decouples publishers from subscribers.
- **Common Task:** Streaming data ingestion, event-driven triggers, microservices communication
- **Pricing:** $0.04/GB ingested + $0.08/GB delivered (first 10GB free)

### ✅ When to Use (Messaging & Streaming)

1. **Real-Time Ingestion (Start: KB/s → Scale: GB/s)**
   - **Start Simple:** Stream application logs (10KB/s) = ~$1/month
   - **Scale:** Handles millions of messages/second automatically
   - **Example:** 1MB/s continuous = ~2.6TB/month = $100+/month (ingestion + delivery)
   - **Latency:** <100ms message delivery
   - **Reliability:** At-least-once delivery, 7-day retention

2. **Event-Driven Architecture (Decoupling)**
   - **Pattern:** Pub/Sub → Cloud Functions/Dataflow
   - **Multiple Consumers:** Same message to many subscribers
   - **Why:** Publishers don't know/care about subscribers
   - **Example:** File upload → process + notify + archive

3. **Dataflow Streaming Source (Classic GCP pattern)**
   - **Pipeline:** Pub/Sub → Data flow → BigQuery
   - **Real-Time Analytics:** Sub-minute end-to-end
   - **Cost:** $0.04/GB + Dataflow worker costs
   - **When:** Need <1 min latency for analytics

4. **Global Message Bus (Multi-region)**
   - **Cross-Region:** Publish in us-central, subscribe in europe-west
   - **HA:** 99.95% SLA for message delivery
   - **Cost:** Same pricing regardless of region
   - **When:** Global applications need coordination

5. **Simplicity Over Kafka (Managed)**
   - **Zero Management:** No brokers, partitions, rebalancing
   - **Auto-Scaling:** Infinite throughput automatically
   - **vs Kafka:** Less control, but zero ops (perfect for most use cases)
   - **Decision:** Pub/Sub unless Kafka-specific features needed

### ❌ When NOT to Use

- **Batch processing (hourly+):** Cloud Storage + Dataflow cheaper for batch
- **Exactly-once semantics:** Pub/Sub is at-least-once; use Dataflow dedup logic if needed
- **Message ordering critical:** Use ordering keys (adds complexity); consider Firestore for strict ordering
- **Long retention (>7 days):** Write to Cloud Storage/BigQuery for longer history
- **Very low volume (<1KB/s):** May be overkill; direct HTTP might be simpler

### Code Example - Pub/Sub

```python
from google.cloud import pubsub_v1
import json

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path('my-project', 'my-topic')

# Publish message
data = json.dumps({'user_id': 123, 'event': 'click'}).encode('utf-8')
future = publisher.publish(topic_path, data)
print(f"Published message ID: {future.result()}")

# Subscribe
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path('my-project', 'my-subscription')

def callback(message):
    print(f"Received: {message.data}")
    message.ack()

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)

try:
    streaming_pull_future.result(timeout=60)
except TimeoutError:
    streaming_pull_future.cancel()
```

### Best Practices

- **Use message attributes** for filtering
- **Enable dead-letter topics** for failed messages
- **Monitor with Cloud Monitoring** (oldest unacked message age)
- **Batch publishes** for higher throughput (100-1000 messages)
- **Use ordering keys** only when strictly necessary (impacts scaling)
- **Set message retention** based on subscriber lag tolerance

---

## Dataflow Streaming (Refer to [Compute & Processing](02_compute_processing.md))

Streaming processing using Dataflow:
- **Pattern:** Pub/Sub → Dataflow → BigQuery
- **Latency:** Seconds to minutes
- **Cost:** Worker costs + Pub/Sub costs
- **When:** Need transformations beyond simple Pub/Sub→BigQuery

---

## Related Topics

- **[Dataflow](02_compute_processing.md)**: Process Pub/Sub streams
- **[BigQuery](05_analytics_warehousing.md)**: Pub/Sub can write directly to BigQuery
- **[Cloud Functions](02_compute_processing.md)**: Triggered by Pub/Sub messages
- **[Service Comparisons](12_service_comparisons.md)**: Pub/Sub vs Kafka

[← Back to Main](README.md)
