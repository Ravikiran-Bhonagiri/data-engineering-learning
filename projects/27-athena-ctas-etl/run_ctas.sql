-- run_ctas.sql

-- ========================================================
-- CTAS: Create Table As Select
-- ========================================================
-- Goal: Convert 'raw_json_logs' (Messy) -> 'clean_parquet_logs' (Optimized)
-- in a single serverless SQL statement.

CREATE TABLE IF NOT EXISTS clean_parquet_logs
WITH (
      format = 'PARQUET',
      parquet_compression = 'SNAPPY',
      external_location = 's3://my-datalake-bucket/optimized/logs/',
      partitioned_by = ARRAY['year', 'month']
)
AS 
SELECT
    -- 1. Simple Transformations
    UPPER(user_name) AS user_name,
    CAST(event_ts AS TIMESTAMP) AS event_time,
    
    -- 2. Logic (Case Statement)
    CASE 
        WHEN status = 200 THEN 'SUCCESS'
        ELSE 'FAILURE' 
    END AS status_code,
    
    -- 3. Partition Columns (must be at end)
    year,
    month
FROM raw_json_logs
WHERE year >= '2024';

-- ========================================================
-- Result:
-- 1. Athena scans 'raw_json_logs'.
-- 2. Athena WRITES Parquet files to s3://.../optimized/logs/
-- 3. Athena registers the table 'clean_parquet_logs'.
-- ========================================================
