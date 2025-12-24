-- spectrum_query.sql

-- ====================================================
-- 1. Create External Schema (The Bridge to Glue)
-- ====================================================
-- This tells Redshift: "Look at the Glue Database 'finance_db' 
-- and let me query its tables as if they were mine."
CREATE EXTERNAL SCHEMA spectrum_layer
FROM DATA CATALOG 
DATABASE 'finance_db' 
IAM_ROLE 'arn:aws:iam::123456789012:role/MyRedshiftRole'
CREATE EXTERNAL DATABASE IF NOT EXISTS;

-- ====================================================
-- 2. Define External Table (Virtual Table)
-- ====================================================
-- Usually, this table already exists in Glue (created by Crawlers).
-- But we can define it manually here too.
CREATE EXTERNAL TABLE spectrum_layer.historical_sales (
    sale_id INT,
    amount DECIMAL(10,2),
    sale_date DATE
)
STORED AS PARQUET
LOCATION 's3://my-datalake-bucket/archive/sales/';

-- ====================================================
-- 3. Local "Hot" Table
-- ====================================================
CREATE TABLE public.current_sales (
    sale_id INT,
    amount DECIMAL(10,2),
    sale_date DATE
);

-- ====================================================
-- 4. The Federated Query (Hot + Cold)
-- ====================================================
-- This is the power move. Joining local SSD data with S3 data.
SELECT 
    'HOT' as source,
    SUM(amount) as total_revenue
FROM public.current_sales
WHERE sale_date >= '2024-01-01'

UNION ALL

SELECT 
    'COLD' as source,
    SUM(amount) as total_revenue
FROM spectrum_layer.historical_sales  -- <--- Reading directly from S3!
WHERE sale_date < '2024-01-01';
