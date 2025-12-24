-- create_optimized_table.sql

-- ==========================================
-- Athena DDL with Partition Projection
-- ==========================================

CREATE EXTERNAL TABLE IF NOT EXISTS access_logs_optimized (
    reader_id STRING,
    doc_id STRING,
    action_type STRING,
    duration_ms INT
)
PARTITIONED BY (date_str STRING)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
LOCATION 's3://my-datalake-bucket/access-logs/'
TBLPROPERTIES (
    -- 1. Enable Projection
    'projection.enabled' = 'true',
    
    -- 2. Define the 'date_str' partition
    'projection.date_str.type' = 'date',
    'projection.date_str.format' = 'yyyy-MM-dd',
    
    -- 3. Define the Valid Range (Static or Dynamic)
    'projection.date_str.range' = '2023-01-01,NOW',
    'projection.date_str.interval' = '1',
    'projection.date_str.interval.unit' = 'DAYS',
    
    -- 4. Storage settings
    'storage.location.template' = 's3://my-datalake-bucket/access-logs/date=${date_str}'
);

-- ==========================================
-- Why is this better?
-- ==========================================
-- STANDARD WAY:
-- You upload a folder 'date=2024-01-01'.
-- You MUST run: MSCK REPAIR TABLE access_logs; (Takes 10 minutes for huge tables)
--
-- PROJECTED WAY:
-- You upload a folder.
-- You run: SELECT * FROM access_logs_optimized WHERE date_str = '2024-01-01';
-- Athena just *knows* the folder is there. Instant access.
