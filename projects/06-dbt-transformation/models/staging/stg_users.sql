-- models/staging/stg_users.sql

WITH source AS (
    -- In real life this would be: SELECT * FROM {{ source('raw', 'users') }}
    -- For this standalone demo, we select from a literal mock
    SELECT 1 as id, 'Alice' as name, 'YES' as is_active, '2023-01-01' as signup_date
    UNION ALL
    SELECT 2 as id, 'Bob' as name, 'NO' as is_active, '2023-01-02' as signup_date
    UNION ALL
    SELECT 3 as id, NULL as name, 'YES' as is_active, '2023-01-03' as signup_date
),

cleaned AS (
    SELECT
        id as user_id,
        COALESCE(name, 'Unknown') as full_name,
        CASE 
            WHEN is_active = 'YES' THEN true 
            ELSE false 
        END as is_active_flag,
        CAST(signup_date AS DATE) as joined_at
    FROM source
)

SELECT * FROM cleaned
