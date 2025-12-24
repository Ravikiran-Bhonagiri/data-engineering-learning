-- sliding_window.sql
-- AWS Kinesis Data Analytics (Legacy SQL) Syntax

-- 1. Create the Output Stream (Internal storage for results)
CREATE OR REPLACE STREAM "DESTINATION_SQL_STREAM" (
    event_url VARCHAR(128),
    avg_price DOUBLE,
    event_count INT,
    window_end_time TIMESTAMP
);

-- 2. Create a PUMP (Continuous Query)
-- A Pump keeps running indefinitely, inserting results into the destination.
CREATE OR REPLACE PUMP "STREAM_PUMP" AS 
INSERT INTO "DESTINATION_SQL_STREAM"

-- 3. The Window Selection
SELECT STREAM
    "url",
    AVG("price") OVER W1 AS avg_price,
    COUNT(*) OVER W1 AS event_count,
    MAX("ROWTIME") OVER W1 AS window_end_time
FROM "SOURCE_SQL_STREAM_001"

-- 4. Define the Window (Sliding)
-- RANGE INTERVAL '1' MINUTE PRECEDING: Look back 1 minute from current row.
-- This calculates the metric for the "last minute", updated for EVERY ROW.
WINDOW W1 AS (
    PARTITION BY "url" 
    RANGE INTERVAL '1' MINUTE PRECEDING
);

-- Note: In Streaming SQL, "ROWTIME" is a special system column representing 
-- the timestamp when the record was ingested by Kinesis.
