-- load_data.sql

-- ==========================================
-- 1. DDL: Create Table with Sort/Dist Keys
-- ==========================================
-- DISTKEY: Group data by 'customer_id' so joins are local (fast)
-- SORTKEY: Sort by 'transaction_date' so we can skip old data (Block Skipping)
CREATE TABLE IF NOT EXISTS public.fact_transactions (
    transaction_id    VARCHAR(50)   NOT NULL,
    customer_id       VARCHAR(50)   NOT NULL DISTKEY,
    amount            DECIMAL(10,2) NOT NULL,
    transaction_date  TIMESTAMP     NOT NULL SORTKEY,
    category          VARCHAR(20)
);

-- ==========================================
-- 2. COPY Command (The Secret Sauce)
-- ==========================================
-- This command tells Redshift to pull directly from S3
COPY public.fact_transactions
FROM 's3://my-datalake-bucket/clean-transactions/'
IAM_ROLE 'arn:aws:iam::123456789012:role/MyRedshiftRole'
FORMAT AS PARQUET
STATUPDATE ON; -- Automatically update query optimizer statistics

-- ==========================================
-- 3. Optimization Check
-- ==========================================
-- Verify skew not present (Distribution Style success)
SELECT 
    "slice", 
    COUNT(*) 
FROM public.fact_transactions 
GROUP BY "slice";
