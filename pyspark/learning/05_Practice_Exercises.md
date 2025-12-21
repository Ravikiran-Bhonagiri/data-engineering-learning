# Practice Exercises (No Solutions)

**Challenge yourself with these real-world problems.**

---

## Exercise 1: Log Analytics (Medium)

### Problem Statement
Analyze web server logs to find traffic patterns and potential issues.

### Requirements

1. **Load** Apache access logs (CSV or text format)
2. **Parse** log entries: IP, timestamp, method, URL, status code, bytes
3. **Calculate:**
   - Requests per hour
   - Top 10 IPs by request count
   - Error rate (4xx, 5xx status codes)
   - Most requested URLs
4. **Output:** Write summary to Parquet

### Sample Log Format
```
192.168.1.1 - - [20/Dec/2025:10:15:30] "GET /api/users HTTP/1.1" 200 1234
```

### Success Criteria
- [ ] Parse all log fields correctly
- [ ] Handle malformed lines gracefully
- [ ] Aggregations are accurate
- [ ] Output is partitioned by date

---

## Exercise 2: E-Commerce Analytics (Medium)

### Problem Statement
Build a product recommendation preprocessor.

### Requirements

1. **Load** orders data with: order_id, customer_id, product_id, timestamp
2. **Calculate:**
   - Products frequently bought together
   - Customer purchase frequency
   - Product popularity (purchases per day)
   - Customer segments based on spending
3. **Create features** for ML:
   - Days since last purchase per customer
   - Average order value per customer
   - Product purchase count per customer

### Success Criteria
- [ ] Co-purchase pairs identified correctly
- [ ] Features are properly normalized
- [ ] No data leakage (only historical data used)
- [ ] Handles customers with single purchase

---

## Exercise 3: Real-Time Fraud Detection (Hard)

### Problem Statement
Build a streaming pipeline to flag suspicious transactions.

### Requirements

1. **Read** transactions from Kafka topic
2. **Enrich** with customer historical data (from static table)
3. **Flag** suspicious transactions:
   - Amount > 5x customer average
   - Transaction in unusual location
   - Multiple transactions within 1 minute
4. **Write** flagged transactions to separate topic/table
5. **Aggregate** fraud metrics per hour

### Success Criteria
- [ ] Stream processes in real-time
- [ ] Watermarking handles late events
- [ ] State management works correctly
- [ ] Fraud rules are accurate

---

## Exercise 4: Customer Segmentation with ML (Hard)

### Problem Statement
Build a customer segmentation model using K-Means.

### Requirements

1. **Load** customer data: demographics, transaction history
2. **Feature engineering:**
   - RFM features (Recency, Frequency, Monetary)
   - Average basket size
   - Preferred product categories
3. **Build** K-Means clustering pipeline
4. **Determine** optimal K using elbow method
5. **Profile** each cluster (avg features)
6. **Save** customer assignments

### Success Criteria
- [ ] Features properly scaled
- [ ] Multiple K values tested
- [ ] Clusters are interpretable
- [ ] Pipeline can be rerun on new data

---

## Exercise 5: Data Lake Migration (Hard)

### Problem Statement
Migrate legacy CSV data to Delta Lake with incremental updates.

### Requirements

1. **Initial Load:**
   - Read historical CSV files (TB scale simulated)
   - Clean and validate data
   - Write to Delta table with partitioning
2. **Incremental Load:**
   - Process only new files (by date)
   - Merge updates (upsert logic)
   - Handle schema evolution
3. **Data Quality:**
   - Null percentage per column
   - Duplicate detection
   - Outlier flagging
4. **Optimization:**
   - Run OPTIMIZE with Z-ORDER
   - Configure VACUUM retention

### Success Criteria
- [ ] Delta table with proper partitioning
- [ ] Merge handles all cases (insert, update)
- [ ] Schema evolution works
- [ ] Time travel verified
- [ ] Performance acceptable (<5 min for 1M rows)

---

## 🎯 Challenge Yourself!

**Rating System:**
- Complete 1-2: Beginner
- Complete 3-4: Intermediate  
- Complete all 5: PySpark Expert 🏆

**Tips:**
- Start with a small dataset, then scale
- Use `.explain()` to understand query plans
- Cache intermediate results when needed
- Test edge cases (empty data, nulls)

Good luck! 🚀
