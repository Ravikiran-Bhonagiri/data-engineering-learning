# Practice Exercises (No Solutions)

**Goal:** Test your Airflow skills with real-world challenges.  
**Format:** Problem statement + requirements only. No solutions provided!

---

## Exercise 1: Weather Data Aggregation Pipeline (Medium)

### Problem Statement
Build a DAG that fetches hourly weather data from an API, aggregates it daily, and stores historical trends.

### Requirements

1. **Extract Task:**
   - Call weather API every hour
   - Get temperature, humidity, wind speed for your city
   - Handle API rate limits and errors gracefully

2. **Transform Task:**
   - Calculate daily aggregates: min, max, avg, temperature, humidity
   - Detect anomalies (temp > 2 std deviations from mean)
   - Add weather classification (hot/cold/moderate)

3. **Load Task:**
   - Store hourly data in `weather_hourly` table
   - Store daily aggregates in `weather_daily` table
   - Use PostgreSQL with proper indexes

4. **Monitoring:**
   - Send email if API fails 3 times in a row
   - Alert if temperature anomaly detected

### Success Criteria
- [ ] DAG runs hourly without failures
- [ ] Both tables populated correctly
- [ ] Alerts working as expected
- [ ] Data quality checks pass

**Hints:**
- Use `HttpSensor` to check API availability
- Consider using `VariablegetState` for city configuration
- Implement retry logic with exponential backoff

---

## Exercise 2: Multi-Cloud Data Lake Sync (Hard)

### Problem Statement
Synchronize data between AWS S3, Google Cloud Storage, and Azure Blob Storage. Ensure data consistency across all three clouds.

### Requirements

1. **Source Detection:**
   - Monitor S3 bucket for new CSV files
   - Use `S3KeySensor` with 5-minute poke interval
   - Support wildcard patterns (e.g., `data/sales/*.csv`)

2. **Validation:**
   - Check file size (must be >1KB)
   - Validate CSV structure (specific columns required)
   - Calculate MD5 checksum

3. **Multi-Cloud Upload:**
   - Upload validated file to GCS
   - Upload validated file to Azure Blob
   - All uploads must happen in parallel
   - Use dynamic task mapping for multiple files

4. **Verification:**
   - Verify file exists in all 3 clouds
   - Compare checksums
   - Log discrepancies

5. **Cleanup:**
   - Archive source file in S3 (move to `archive/` prefix)
   - Send summary report via Slack

### Success Criteria
- [ ] Handles multiple files simultaneously
- [ ] All 3 cloud providers synced
- [ ] Checksum validation works
- [ ] Failed uploads retry automatically
- [ ] Slack notification includes file count and sizes

**Hints:**
- Use `TaskGroup` to organize cloud uploads
- Implement custom XCom backend for large metadata
- Consider using `BranchPythonOperator` for conditional cleanup

---

## Exercise 3: Real-Time Event Processing (Hard)

### Problem Statement
Build an event-driven DAG that triggers when messages arrive in a Kafka topic, processes them, and updates a dashboard.

### Requirements

1. **Event Listener:**
   - Listen to Kafka topic `user_events`
   - Trigger DAG when message count > 100
   - Use Kafka consumer in sensor

2. **Event Processing:**
   - Parse JSON events
   - Enrich with user data from PostgreSQL
   - Calculate metrics: events per user, event types, timestamps

3. **Batch Processing:**
   - Group events by user_id
   - Use dynamic task mapping to process users in parallel
   - Aggregate metrics into summary table

4. **Dashboard Update:**
   - Update Redis cache with latest metrics
   - Trigger API endpoint to refresh dashboard
   - Handle dashboard API failures gracefully

5. **Backpressure Handling:**
   - If events > 10,000, split into multiple DAG runs
   - Implement queue to avoid overwhelming downstream systems

### Success Criteria
- [ ] DAG triggers within 1 minute of event threshold
- [ ] All events processed without loss
- [ ] Parallel processing works correctly
- [ ] Dashboard shows real-time data
- [ ] System handles 50K+ events/hour

**Hints:**
- Create custom sensor by extending `BaseSensorOperator`
- Use Airflow pools to limit parallelism
- Consider using `SubDagOperator` for batch splitting

---

##Exercise 4: Incremental Data Load Pattern (Medium)

### Problem Statement
Implement an incremental load pattern for a large table (millions of rows). Only load changed/new records.

### Requirements

1. **State Management:**
   - Track last processed timestamp in Airflow Variable
   - On first run, load all data
   - On subsequent runs, load only new/updated records

2. **Extraction:**
   - Query source database with `WHERE updated_at > last_timestamp`
   - Handle pagination (1000 rows per batch)
   - Use dynamic task mapping for batches

3. **Transformation:**
   - Deduplicate records (keep latest version)
   - Apply business rules (e.g., calculate derived fields)
   - Flag deleted records (soft deletes)

4. **Loading:**
   - Use UPSERT logic (INSERT ON CONFLICT UPDATE)
   - Update metadata table with load statistics
   - Archive old versions to history table

5. **Validation:**
   - Compare row counts (source vs destination)
   - Validate no duplicates in target
   - Check for data gaps in timestamp ranges

### Success Criteria
- [ ] First run loads full table
- [ ] Incremental runs load only changes
- [ ] No data loss or duplicates
- [ ] Handles millions of rows efficiently
- [ ] Restartable (idempotent)

**Hints:**
- Use `Variable.set()` and `Variable.get()` for state
- Consider using `PostgresOperator` for UPSERT
- Implement checkpoint logic for large batches

---

## Exercise 5: Multi-DAG Orchestration (Hard)

### Problem Statement
Coordinate 5 interdependent DAGs that must run in a specific order with data passing between them.

### Requirements

1. **DAG Architecture:**
   - DAG 1: Extract raw data
   - DAG 2 & 3: Transform data (run in parallel after DAG 1)
   - DAG 4: Join transformed data from DAG 2 & 3
   - DAG 5: Generate reports (after DAG 4)

2. **Inter-DAG Communication:**
   - Use `ExternalTaskSensor` to wait for upstream DAGs
   - Pass metadata (file paths, record counts) between DAGs
   - Handle timeout scenarios gracefully

3. **Error Handling:**
   - If DAG 2 fails, DAG 3 should still complete
   - DAG 4 should only run if BOTH DAG 2 & 3 succeed
   - Implement retry logic for each DAG

4. **Scheduling:**
   - DAG 1: Runs every 6 hours
   - DAG 2-5: Triggered by upstream completion
   - All DAGs share same execution_date

5. **Monitoring:**
   - Central dashboard showing status of all 5 DAGs
   - Alert if any DAG fails
   - Track end-to-end latency

### Success Criteria
- [ ] Correct execution order maintained
- [ ] Parallel execution where possible
- [ ] Data passed successfully between DAGs
- [ ] Error in one DAG doesn't break others unnecessarily
- [ ] End-to-end automation works

**Hints:**
- Use `ExternalTaskSensor` with `execution_delta`
- Store metadata in Airflow XCom or external store
- Consider using Airflow 2.4+ Dataset feature for triggering
- Use `TriggerDagRunOperator` for programmatic triggering

---

## 🎯 Challenge Yourself!

Try to complete all exercises **without looking at the examples**!

**Rating System:**
- Complete 1-2: Beginner
- Complete 3-4: Intermediate  
- Complete all 5: Advanced  

Good luck! 🚀
