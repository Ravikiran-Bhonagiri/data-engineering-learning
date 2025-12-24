import awswrangler as wr
import pandas as pd
import time

# Configuration
DATABASE = "default"
TABLE_NAME = "iceberg_customer_profiles"
S3_BUCKET = "s3://databricks-foundations-dev-landing/iceberg/"

def run_query(sql, comment):
    print(f"\n--- {comment} ---")
    print(f"Executing: {sql}")
    # In a real run, this executes against Athena
    # query_id = wr.athena.start_query_execution(sql, database=DATABASE, wait=True)
    # print(f"Query ID: {query_id}")

def main():
    # 1. Create Iceberg Table (DDL)
    # Notice 'table_type': 'ICEBERG'
    print("Creating Iceberg Table via Athena...")
    create_sql = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        user_id STRING,
        full_name STRING,
        email STRING,
        cautious_score INT,
        last_updated TIMESTAMP
    )
    PARTITIONED BY (day(last_updated)) 
    LOCATION '{S3_BUCKET}'
    TBLPROPERTIES (
        'table_type'='ICEBERG',
        'format'='parquet'
    );
    """
    run_query(create_sql, "Creating Table with Hidden Partitioning")

    # 2. Insert Data
    insert_sql = f"""
    INSERT INTO {TABLE_NAME} VALUES
    ('u1', 'Alice', 'alice@example.com', 50, TIMESTAMP '2023-01-01 10:00:00'),
    ('u2', 'Bob',   'bob@example.com',   20, TIMESTAMP '2023-01-01 10:05:00')
    """
    run_query(insert_sql, "Inserting Initial Data")

    # 3. UPSERT / MERGE (The Power of Iceberg)
    # Alice updates her email. We merge on user_id.
    merge_sql = f"""
    MERGE INTO {TABLE_NAME} AS target
    USING (SELECT 'u1' as user_id, 'alice_new@example.com' as email) AS source
    ON target.user_id = source.user_id
    WHEN MATCHED THEN
        UPDATE SET email = source.email
    """
    run_query(merge_sql, "Performing MERGE (Upsert)")

    # 4. Time Travel Query
    # Query the table as it was 5 minutes ago (before the email update)
    time_travel_sql = f"""
    SELECT * FROM {TABLE_NAME}
    FOR SYSTEM_TIME AS OF (current_timestamp - interval '5' minute)
    WHERE user_id = 'u1'
    """
    run_query(time_travel_sql, "Time Travel Query (Snapshot)")

if __name__ == "__main__":
    main()
