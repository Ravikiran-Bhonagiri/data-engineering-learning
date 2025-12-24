-- setup_governance.sql

-- ==========================================
-- 1. Create the Top-Level Catalog
-- ==========================================
-- Matches the "Bronze/Silver/Gold" or Domain-Driven design
CREATE CATALOG IF NOT EXISTS finance_prod
COMMENT 'Production data for Finance Logic';

-- Switch context
USE CATALOG finance_prod;

-- ==========================================
-- 2. Create Schemas (Logical Grouping)
-- ==========================================
CREATE SCHEMA IF NOT EXISTS accounts_payable
COMMENT 'Data related to outgoing payments';

CREATE SCHEMA IF NOT EXISTS revenue_reporting
COMMENT 'Aggregated revenue metrics';

-- ==========================================
-- 3. Create a Managed Volume (Unstructured Data)
-- ==========================================
-- Volumes allow us to govern files (PDF invoices) using SQL
CREATE VOLUME IF NOT EXISTS accounts_payable.invoice_pdfs
COMMENT 'Scanned PDF invoices from vendors';

-- ==========================================
-- 4. Create Tables (Structured Data)
-- ==========================================
CREATE TABLE IF NOT EXISTS revenue_reporting.daily_kpis (
    date DATE,
    total_revenue DECIMAL(18,2),
    region STRING
)
USING DELTA
COMMENT 'Executive daily dashboard source';

-- ==========================================
-- 5. Access Control (The Governance)
-- ==========================================

-- Scenario: 'data_analysts' need to read reports but NOT see raw invoices.
GRANT USE CATALOG ON CATALOG finance_prod TO `data_analysts`;
GRANT USE SCHEMA ON SCHEMA revenue_reporting TO `data_analysts`;
GRANT SELECT ON TABLE revenue_reporting.daily_kpis TO `data_analysts`;

-- Scenario: 'finance_auditors' need access to PDF invoices.
GRANT READ VOLUME ON VOLUME accounts_payable.invoice_pdfs TO `finance_auditors`;

-- Dynamic View for Masking (Row/Column Security)
CREATE OR REPLACE VIEW revenue_reporting.masked_kpis AS
SELECT
    date,
    -- Mask revenue if user is not an admin
    CASE 
        WHEN is_account_group_member('admins') THEN total_revenue
        ELSE NULL 
    END as total_revenue,
    region
FROM revenue_reporting.daily_kpis;
