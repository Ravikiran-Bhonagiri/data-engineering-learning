# Streaming & Messaging 🌊

[← Back to Main](README.md)

Real-time event streaming and enterprise messaging.

---

## [Event Hubs](https://azure.microsoft.com/services/event-hubs/) (Detailed)

See [Data Integration](04_data_integration.md) for overview.

### Tier Comparison

| Tier | Price/Hour | Throughput | Use Case |
|------|-----------|------------|----------|
| Basic | $0.028 | 1 MB/s | Dev/test |
| Standard | $0.015/unit | 1 MB/s/unit | Production |
| Premium | $1.046/unit | 8 MB/s/unit | Critical workloads |

**Decision:** Start Standard, upgrade to Premium for isolation/performance

---

## [Service Bus](https://azure.microsoft.com/services/service-bus/)

Enterprise messaging with advanced features.

- **Why it matters:** Reliable messaging with transactions, sessions, dead-lettering
- **Pricing:** Basic $0.05/million operations, Standard $10/month + operations

### ✅ When to Use

- **FIFO ordering:** Guaranteed message ordering
- **Transactions:** ACID across multiple queues
- **Sessions:** Stateful message processing
- **When:** Enterprise integration patterns

### ❌ When NOT to Use

- **High throughput (>1 MB/s):** Use Event Hubs
- **Simple queuing:** Azure Storage Queues cheaper

[← Back to Main](README.md)
