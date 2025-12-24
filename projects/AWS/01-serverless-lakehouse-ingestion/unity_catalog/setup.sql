-- ==========================================
-- Phase 2: Unity Catalog Configuration (Finance)
-- ==========================================

-- 1. Create Storage Credential
CREATE STORAGE CREDENTIAL IF NOT EXISTS p1_market_data_cred
  URL 's3://serverless-lakehouse-dev-landing-zone'
  COMMENT 'Access to Market Data buckets'
  WITH (
    AWS_IAM_ROLE_ARN = 'arn:aws:iam::414351767826:role/serverless-lakehouse-uc-access-role'
  );

-- 2. Create External Locations
CREATE EXTERNAL LOCATION IF NOT EXISTS p1_landing_loc
  URL 's3://serverless-lakehouse-dev-landing-zone'
  WITH (STORAGE CREDENTIAL p1_market_data_cred)
  COMMENT 'Raw market data landing';

CREATE EXTERNAL LOCATION IF NOT EXISTS p1_bronze_loc
  URL 's3://serverless-lakehouse-dev-bronze'
  WITH (STORAGE CREDENTIAL p1_market_data_cred);

CREATE EXTERNAL LOCATION IF NOT EXISTS p1_silver_loc
  URL 's3://serverless-lakehouse-dev-silver'
  WITH (STORAGE CREDENTIAL p1_market_data_cred);

-- 3. Create Catalog
CREATE CATALOG IF NOT EXISTS p1_market_data
  MANAGED LOCATION 's3://serverless-lakehouse-dev-bronze/__managed';

-- 4. Create Schema
USE CATALOG p1_market_data;
CREATE SCHEMA IF NOT EXISTS trades;

-- 5. Grants
GRANT CREATE TABLE, USE SCHEMA ON SCHEMA trades TO `data_engineers`;
GRANT READ FILES ON EXTERNAL LOCATION p1_landing_loc TO `data_engineers`;
